## Who is submitting this PR? (required)

| Field | Value |
|-------|-------|
| Your model + version | Claude Opus 4.8 (`claude-opus-4-8[1m]`) |
| Harness + version | Claude Code 2.1.170 |
| All plugins installed | **superpowers**@claude-plugins-official (the plugin modified here); plus agent-sdk-dev, elements-of-style, episodic-memory, frontend-design, plugin-dev, superpowers-developing-for-claude-code, superpowers-lab, code-simplifier, claude-code-setup, primeradiant-ops, superpowers-chrome, claude-session-driver, github-triage, summarize-meetings, release-radar, linear, context7, mcp-server-dev, worldview-synthesis, {gopls,rust-analyzer,swift}-lsp |
| Human partner who reviewed this diff | Jesse Vincent (@obra) — original maintainer partner/direction for the Claude pass; Drew Ritter (@drewritter) — follow-up human partner who reviewed/directed the final Codex hardening pass before maintainer review |
| Follow-up model + version | Codex (GPT-5) |
| Follow-up harness + version | Codex desktop/API coding-agent environment (harness version not exposed) |
| Follow-up plugins used | GitHub, Codex Security, Browser, Linear, Prime Radiant Ops |

## What problem are you trying to solve?

The brainstorming **visual companion** (`skills/brainstorming/scripts/`) had a cluster of real, separately-reported problems. Grounded in a working session (an apparent reload failure that root-caused to a wedged `fseventsd` on the dev machine — not a companion bug) plus a triage of open issues/PRs:

- **Security:** the WebSocket/HTTP server accepted connections from any origin and any host with no authentication. A malicious browser tab — or, on a `--host 0.0.0.0` bind, any host that can route to the port — could read brainstorm screens and inject fake `click` events into `state/events`, which the agent reads next turn as the user's selection (prompt injection into a live session). (#1014; DNS-rebinding/origin angles in #1553 / #1110)
- **Crash:** a 4-byte `null` WebSocket payload threw an uncaught `TypeError` and killed the server process. (#1504, bundled in #1446)
- **Garbage served:** on macOS / ExFAT / SMB, `._*.html` resource-fork sidecars passed the `.html` filter and got served as the newest screen — binary metadata instead of the mockup. (#950)
- **Silent mid-session expiry:** the 30-minute idle timeout was too short; the server died with no signal, the browser showed a bare "can't be reached," and the agent kept referring to a dead URL. (#1237)
- **No graceful reconnection / no auto-open / offered too eagerly:** the browser client reconnected on a dumb fixed 1s timer with no status feedback (and showed "Connected" over a dead socket); nothing opened the browser for the user; and the companion was pitched upfront before any visual question arose, wasting tokens and a turn.
- **`stop-server.sh`** killed whatever PID was in its file with no ownership check — a recycled PID after a reboot could kill an unrelated process.

## What does this PR change?

Hardens and modernizes the visual-companion server and skill: per-session secret-key auth on every endpoint (+ cookie bootstrap, friendly 403, null-payload guard); resource-fork dotfile filtering; ownership-checked `stop-server.sh`; a 4h configurable idle timeout that closes WebSockets cleanly on shutdown; exponential-backoff reconnect with a live status indicator and a "paused" overlay; same-port + same-key restart so an already-open tab reconnects on its own; opt-in `--open` browser launch on the first screen with an argv-safe Windows/WSL launcher; and offering the companion **just-in-time** (the first time a visual question arises) instead of upfront.

## Is this change appropriate for the core library?

Yes. The visual companion is core brainstorming infrastructure shipped with superpowers — every user who accepts the companion benefits, regardless of project type. No new dependencies (the server stays zero-dep), no third-party services. The security fix protects every companion session.

## What alternatives did you consider?

- **Security — Host/Origin allowlist** (the #1110 / #1553 approach). Rejected: it only defends the loopback browser-confused-deputy; a direct client on a `--host 0.0.0.0` bind just sends the expected `Host`, so the allowlist is theater for remote use. A per-session secret authenticates the real client uniformly across loopback, SSH tunnel, and remote binds, and defeats DNS rebinding.
- **Reload reliability — replace `fs.watch` with polling.** Built and tested, then **dropped** after root-causing the symptom to a wedged `fseventsd` daemon on the dev machine (a 100%-CPU spin starving FSEvents). `fs.watch` was fine; the OS daemon needed a kick. No reason to carry polling.
- **Vendoring Alpine.js** for interactive mockups (#1639): out of scope; not pursued (keeps the runtime zero-dep).
- **Consent timing — keep the upfront offer.** Rejected via eval (see Evaluation) — upfront pitches the companion before the problem is understood.

## Does this PR contain multiple unrelated changes?

They are all changes to **one subsystem** — the brainstorming visual companion (`server.cjs`, `helper.js`, `frame-template.html`, `start-server.sh`, `stop-server.sh`, and the companion skill docs) — developed and consolidated as one coherent overhaul. The branch is structured as focused commits, each with its own tests, so it can be split into per-issue PRs if you'd prefer that over a single subsystem PR.

## Existing PRs
- [x] I have reviewed all open AND closed PRs for duplicates or prior art
- Related PRs (this PR implements the underlying fixes directly and reconciles their intent — see `docs/superpowers/plans/2026-06-09-visual-companion-issues.md` for the per-item triage): **#950, #1703, #856, #1689, #759, #1037, #1110, #1553, #1504, #1639**. Each was an alternative single-fix implementation or an adjacent concern; e.g. a session key supersedes the #1110/#1553 Host/Origin allowlist, and #1446's frame-length DoS is already fixed on `dev`.

## Environment tested

| Harness | Harness version | Model | Model version/ID |
|---|---|---|---|
| Claude Code | 2.1.170 | Claude Opus | claude-opus-4-8 (1M context) |
| Codex desktop/API | version not exposed | Codex | GPT-5 |

Original Claude pass: macOS (Darwin 25.2.0), Node v26.0.0.

Follow-up Codex pass: macOS (Darwin 25.5.0 arm64), Node v24.14.0; Windows on `ballmer` via Git Bash / MINGW64_NT-10.0-26200, Node v26.2.0.

## New harness support (required if this PR adds a new harness)

N/A — this PR does not add a new harness.

## Evaluation

The one behavior-shaping change (offering the companion **just-in-time**, in `SKILL.md`) was eval'd with the `evals/` harness. The scenario asks the agent to design a dashboard and judges *when* the companion is offered.

Exact eval scenario reference:

- Repo/branch/commit: `superpowers-evals`, `round3-boundary-scenarios`, `f1ac859` (`scenarios: convert companion just-in-time eval to Quorum format`)
- Scenario path: `scenarios/brainstorming-companion-just-in-time/story.md`
- Current Quorum command shape: `SUPERPOWERS_ROOT=<superpowers checkout> uv run quorum run scenarios/brainstorming-companion-just-in-time --coding-agent claude`
- Artifact note: the original 4-run Drill result artifacts are not part of this PR diff and were not present in the current worktree; the retained evidence from that pass is the RED/GREEN outcome summary below. The evals submodule is intentionally absent from this PR diff.

- **RED** (`dev`, upfront-offer text): **0/4 pass** — the agent offers the companion as its "very next action," before any clarifying questions.
- **GREEN** (this branch, just-in-time text): **4/4 pass** — the agent explores and clarifies first; never offers prematurely.
- The `brainstorming` skill triggered correctly in **all** runs, both arms — the change moves the offer without regressing triggering.

Server/client behavior on the current rebased branch:

- TDD regressions were verified RED then GREEN for the final hardening pass: root-screen containment blocked symlink/hardlink escapes from being selected as the newest screen; fallback tokens now rotate and fail closed when `BRAINSTORM_TOKEN` is explicit; `stop-server.sh` now requires exact PID + server-instance-id ownership proof before killing; successful/stale stops clear alive metadata and write `server-stopped`; persisted `.last-token` files are hardened back to owner-only permissions; and Windows/WSL `--open` no longer routes a URL through `cmd.exe /c start`.
- macOS Codex pass (Darwin 25.5.0 arm64, Node v24.14.0): `npm test` in `tests/brainstorm-server` green across ws-protocol 32, helper 15, browser-launcher 3, auth 20, server 33, lifecycle 13, start-server 4, stop-server 7; standalone `windows-lifecycle.test.sh` 9 passed / 0 failed / 3 skipped. Static checks passed: `git diff --check`, `node --check` for server/helper/lifecycle/browser-launcher test files, and shell lint for the companion scripts/tests.
- Windows Git Bash pass on `ballmer` (MINGW64_NT-10.0-26200, Node v26.2.0, npm 11.13.0): `npm --prefix tests/brainstorm-server ci` exited 0 (existing moderate `ws` audit warning), `npm --prefix tests/brainstorm-server test` green across ws-protocol 32, helper 15, browser-launcher 3, auth 20, server 33, lifecycle 13, start-server 4, stop-server 7; `bash tests/brainstorm-server/windows-lifecycle.test.sh` 13 passed / 0 failed / 0 skipped; post-run process sweep found no matching leftover Node/npm/bash/sh/cmd processes. This caught and fixed both the MSYS `/proc/$pid/cmdline` final-argument edge case in the instance-id ownership check and the Windows launcher `cmd.exe` metacharacter risk.
- Additional Windows smoke on `ballmer`: `start-server.sh --project-dir ... --open --foreground` produced a keyed URL, the first screen triggered a real `rundll32.exe` process-start event, keyed bootstrap then `/` returned 200, and `stop-server.sh` returned `{"status": "stopped"}`; a fresh persistent project stop wrote `server-stopped`, restart reused the same port/key, and a stale-PID simulation returned `stale_pid` while leaving the unrelated process alive; Edge headless loaded a screen with a local `/files/vendor-lib.js` asset, blocked unauthenticated `/files` with 403, fetched authenticated `/files` with 200, executed both external and inline JS, and received a WebSocket `reload` after the HTML changed. Final sweep found no matching leftover test/server/browser processes.
- Manual browser smoke was run last: `start-server.sh --open --foreground` produced a keyed URL, the browser stripped `?key=` to `/`, served a screen, survived `stop-server.sh`, reconnected automatically after same-port/same-key restart, and live-reloaded a new HTML screen after reconnect.

The branch also survived multiple adversarial review rounds: the original Claude pass, the Codex security/design/test review pass, and final subagent reviewer gates for each hardening slice. Those reviews surfaced real bugs that were then fixed with teeth-verified regression tests — including a same-port-restart token mismatch, an uncaught `/files/` EISDIR crash, stale fallback-token reuse, unsafe root-screen selection, Windows/MSYS lifecycle edge cases, and the Windows auto-open command-interpreter edge case.

## Rigor

- [x] Skills change: used eval evidence (drill RED/GREEN above) for the one behavior-shaping change.
- [x] Tested adversarially, not just the happy path (multiple adversarial review rounds; each accepted finding fixed with a regression test verified to fail on the pre-fix code).
- [x] Did not modify carefully-tuned content (Red Flags tables, rationalization lists, "human partner" language). The `SKILL.md` change only moves *when* the companion offer happens — it does not touch the Red Flags / rationalization content.

## Human review
- [x] A human has reviewed the COMPLETE proposed diff before submission — original Claude pass had Jesse Vincent (@obra), maintainer, as human partner/direction; the final Codex hardening pass was reviewed/directed in-session with Drew Ritter (@drewritter) before maintainer review.

---

/cc @arittr — requesting your review.

