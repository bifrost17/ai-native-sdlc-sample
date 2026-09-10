# ai-native-sdlc-sample
<!-- TEAM: real build/test/lint commands, healthy output, conventions — docs/ADOPTING.md · L14 -->

<!-- L5 414-436: the four sections of the playbook's CLAUDE.md. L5 412: "Keep it under a page" -->

## Commands
- Test: `make test` (python unittest, `tests/test_hooks.sh`, `tests/test_evals.sh`,
  `tests/test_managed_settings.sh`; healthy: rc=0, the four suites end with `OK`,
  `test_hooks: 28 passed, 0 failed`, `8 passed, 0 failed`, `PASS  managed-settings 키·훅 계약`)
- Evals: `make evals` (`bash evals/run.sh`, needs `ANTHROPIC_API_KEY`; healthy: `evals: 전 케이스 통과`)
- Check: `make check` (= `make test`; non-zero on any failure). Evals are not in it: without
  `ANTHROPIC_API_KEY` `make evals` prints `SKIP: ANTHROPIC_API_KEY 없음` and exits 2; CI runs them
  with the key in `.github/workflows/agent-evals.yml` (L10 689).

## Conventions
- Prose in artifacts is in the originator's language (L2 179 "in the originator's own terms";
  chain 0002 is Korean); file names, section names and `Status:` words are fixed English tokens.
- One chain per change under `intent/<NNNN>-<slug>/` — intent.md, spec.md, plan.md, in that
  order, each its own commit. `Status: draft` until the PR merges; the merge is the approval.
  A chain is for a change to what the template *is* (0001 · 0004 · 0010 · 0011 · 0012); upkeep —
  factual corrections, citation refreshes, chores — is a PR, not a chain. Ask the engineer rather
  than opening one on your own reading of this line.
- Every code file under `.claude/hooks/`, `scripts/`, `evals/` opens with the lesson sentence it
  implements, quoted with its line number. No sentence, no file. Files under `src/` and `tests/`
  open with the spec clause (R/AC) they implement instead — no lesson line there (0002 and 0007
  each guessed differently; this settles it).
- Change files with the Edit/Write tools, not shell redirection or heredocs. The hooks in
  `.claude/settings.json` watch tool calls, not effects: chain 0007 wrote 45/45 files through
  Bash and the Edit/Write hooks fired zero times. A fix task is declared by the engineer, not
  detected: start the session with `INTENT_TASK=fix` (e.g. `INTENT_TASK=fix claude`).
- python3 standard library only; bash 3.2 (no `mapfile`, no `declare -A`; `wc -l | tr -d ' '`).

## Architecture
- `.claude/skills/` — what the agent is told (advisory). `.claude/hooks/` + `settings.json` —
  what the machine blocks. `tests/`, `evals/`, `.github/` — what CI proves. See docs/BOUNDARY.md.
- `intent/` — the artifact chains; `templates/` — copies of the skill-embedded templates.
- `docs/PLAYBOOK-MAP.md` maps the 14 lessons to files; `docs/METRICS.md` is git commands.

## Verifying your work

- Build: make build (must finish with "Build succeeded")
- Test: make test (all green; never skip or delete a failing test)
- Lint: make lint (zero warnings)

Run all three before reporting any task complete, and paste the output.
If a test fails, fix the code, not the test.

(L9 635-645 verbatim. This repo has no `make build`/`make lint`; run `make check` and paste it.)
Before reporting a chain done, hand the check to the `verifier` subagent (`.claude/agents/verifier.md`)
and paste its report — chains 0007-0009 never invoked it (L8 564).

## Things Claude gets wrong
- Applying the process this template prescribes to *adopting teams* to this repo's own upkeep.
  **This repo builds the template; it is not a product repo run by it.** Chains are for changes to
  the template (see Conventions). Separation of duties (`REVIEW.md`, `docs/BOUNDARY.md` "approval
  is a person merging") prescribes a team's account structure; here the engineer directing the work
  *is* the owner, and a merge they asked for is their approval. Twice in one session: a chain
  proposed for a two-line fix, and an owner-requested merge refused on separation grounds.
- Writing a checker for artifact sections, status or transitions. The skill says it, the product
  owner reads it, the merge records it. Do not build the machine again.
- Setting `Status: accepted` in a file. Only a merged PR means accepted.
- Pointing a skill or a doc at a script that does not exist. Run `ls` before you cite a path.
- Editing a sample ledger row that a test already pins. Once a test asserts a row's key set or
  that a claim id is absent, the next chain cannot touch that row. Twice now: 0005 pinned
  `C-1001`, and 0008 had to add `C-2001`-`C-2003` instead. A new chain uses new rows; a chain
  that must change an existing row finds the tests that pin it first (`grep -n _UPSTREAM tests/`).
