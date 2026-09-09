# Runs

This is a record of runs against this repo's playbook devices — actual agent sessions, not a
description of intended behavior. The judgment on each run is whatever that play's own
"Governance considerations" and "How to measure it" sections say to check; there is no separate
scorecard invented for this document.

Numbers come from four sources only: commit timestamps (`git log --format=%cI`), PR merge
timestamps (`gh pr view --json mergedAt`), `.claude/hooks.log` line counts, and the session `.jsonl`
transcripts (`num_turns`, `duration_ms`, `total_cost_usd`, tool-call extracts). Raw command output for
every number below lives outside this repo, under the harness scratchpad's `raw-live/`, `raw-liveR/`
and `raw-hac/` directories (file names cited per number); those directories are not committed here.

## Run A — chain 0007 · unbriefed solo agent · ticket route (issue #24)

One `claude -p` invocation, prompt "resolve issue #24, open a PR when done", no brief beyond that.
46 turns, 6 min 15 s (374713 ms), $2.21 (`total_cost_usd` 2.205662) — `raw-live/10-inner-session.jsonl`.
PR #28, merged 2026-09-09T04:09:22Z.

The agent read `CLAUDE.md`, `REVIEW.md`, `docs/BOUNDARY.md` and three skills (`capture-intent`,
`design-spec`, `plan`) on its own initiative — 0 explicit `Read` tool calls but the content shows up
quoted in its output (`raw-live/17-tool-calls.txt`, `20-checklist.jsonl` item ①②) — then produced
intent → spec → plan → a failing test committed alone → the fix, one commit per stage
(`fcaf6b1` test, red: `FAILED (failures=2)`, then `c5dd79c` fix, test file untouched —
`raw-live/21-red-at-test-commit.txt`, `24-per-commit-stat.txt`). Root cause: `^C-[0-9]+$` matches
before a trailing newline; fixed with `\A…\Z` anchors, not `.strip()` (spec F1).

All 45 tool calls were `Bash`; every file write went through shell heredoc/python, so the
`Edit`/`Write` hook matchers (protect-paths, no-secrets, format-lint) fired 0 times even though
`production-gate.sh` allowed all 45 — the gate only sees invocations that route through those
matchers, not the effect on disk (`raw-live/19-upstream-sha-prchecks-hookcounts.txt`, checklist
item ⑦). This gap became PR #29's finding, item 1 below. Full checklist: 11 items, all PASS/YES
except ① (`raw-live/20-checklist.jsonl`); reviewer transcripts: `raw-liveR/`.

## Run B — chain 0008 · human–agent · idea route (adjuster lookup)

H = the four original-playbook roles played in sequence (originator L2 193–201 → product owner L2
223, L3 259–269 → engineer L4 311–323 → code owner L11 739–745); A = a headless session opened
with the repo as its project directory. Gate timestamps below are copied as-recorded from
`raw-hac/30-gate-timeline.txt` — the harness's own measurement, not re-derived: **G0** 04:15:07Z
(turn 1 start) … **G7** 05:21:39Z (PR #33 merge) — 1 h 6 min 32 s across 8 gate points.

Turn 1: clarifying questions only, 0 files written. Turn 2: intent.md drafted in the originator's
own words, separating "what they know" from "what they believe". Turn 4: spec flags 7 concerns
(F1 cached lookup vs. immediate cutoff = "stale authorization", not the F1 already accepted in
0002; F2 an allow-list of field *names* doesn't bound field *values*) — `raw-hac/16-turn4.jsonl`.
Turn 7: interrogation ("what could this break") changed the plan in 2 places — `cached` became a
required keyword argument, and the sample-record additions moved to fresh IDs (`C-2001`–`C-2003`)
to avoid existing tests' assumptions about the old rows — `raw-hac/22-turn7.jsonl`. Turn 8: mutation
M2 survived (`cached=False→True`, 59/59 still green) — the cache held the *same dict object* as the
ledger row, so an in-place edit leaked through the cache; fixing the instrument (not the code) made
M2 kill two tests — `raw-hac/23-turn8.jsonl`. Turn 9: the code owner pointed out the fix was to the
implementation, not just the instrument (the cache needed a real snapshot, `dict(record)`), which
the agent applied plus a second `CLAUDE.md` line (L11 745, "flags a mistake for the second time") —
`raw-hac/25-turn9.jsonl`, `26-turn9-pr33-newcommit.txt`. PRs #30, #31, #33.

## Run C — chain 0009 · human–agent · idea route (agent-proxy lookup)

Same roles and harness as run B; new originator (call-centre operations lead). Gate times from commit
timestamps and `gh pr view --json mergedAt` (`raw-hac/60-gate-timeline-exp2.txt`):
G0 first utterance 05:50:25Z → G1 intent commit 61669a1 05:57:34Z → G2 PR #38 merged 06:00:01Z →
G3 spec commit 2b11007 06:08:23Z → G4 PR #39 merged 06:18:50Z → G5 plan commit 0f8aa06 06:31:59Z →
G6 test commit 18c321d 06:34:58Z → G7 PR #42 merged 06:43:23Z. **G0→G7 52 min 58 s** (run B: 66 min 32 s).
Observed (raw turn files in `raw-hac/41`–`57`): turn 1 asked before writing and named identity
verification as the chain's "throat"; turn 2 left `next_step` as an open question rather than deciding
(the customer sees it, 0008 hid it from adjusters); turn 4 spec flagged F1 as blocking — a console session
carrying the verified customer under `subscriber_id` would slip through the customer handler with no
record — and F9 said honestly that only security was checked because the repo has no brand/UX skill;
turn 5 reversed R6 on the owner's answer (expiry belongs to the console; `verified_at` is in the contract
but not read, AC6 pins that); turn 7 interrogation changed the plan in three places (AC4 measures
`upstream_calls == 0`, M5 moves the gate instead of deleting it, the `is` decision written into Proof);
turn 8 build: red 13 (no errors) → green, `response.py`/`routes.py` untouched, five mutations each red
with sha256 restore, M4 killed only the `is` test — the measured reason for `is`; turn 9 code-owner
review found nothing. Hooks fired +271 lines in this run (`raw-hac/61-hooks-log-totals-exp2.txt`).
Left open: issue #32 (failed lookups unrecorded, shared with 0008).

## Feedback loop

| Run | What it hit | Where it was fixed | PR |
|---|---|---|---|
| 0002 | skill/CLAUDE.md wording, 3 places | docs | #19 |
| 0005, 0006 | design corrections | docs | #27 |
| 0007 | hooks see tool calls, not effects — 5 lines of doc | docs | #29 |
| 0008 A (self) | CLAUDE.md, 1 line | docs | #33 (in-PR commit) |
| 0008 | experiment-surfaced doc issues, 3 lines | docs | #34 |
| 0008 | the three findings caught a second time (L11 745 "second time", L5 401) | docs | #35 |
| — | adoption guide | docs | #40 |

## Per-play measured indicators (against each play's "How to measure it")

- L2 227 leading (first conversation → committed intent.md): run B 11 min (G0→G1), run C 9 min 36 s.
- L3 283 leading (intent.md → spec.md): run B 21 min 9 s (G2→G4), run C 18 min 49 s.
- L4 355 leading (plan approval → merged PR): run B 23 min, run C 11 min 24 s (G5→G7).
- L5 432 (CLAUDE.md correction count): PRs #16, #19, #29, #33, #35 (`git log --oneline -- CLAUDE.md`;
  #34 changed a skill and the README, not CLAUDE.md).
- L5 432 leading (a mistake CLAUDE.md should have caught, repeated): Edit/Write rule (#29) — 0 repeats
  in runs B and C (hook events 107 and 131 in the implementation turns, against 0 in run A);
  "Setting `Status: accepted` in a file" (CLAUDE.md since #16) — 1 repeat, 0009 `plan.md:2`
  (the skill wording was tightened in #46).
- L9 642 (first-pass CI success): runs A, B and C — all green on the first CI run.
- L11 773 (time to first review): run B turn 9 (one finding, fixed in-PR), run C turn 9 (no finding) — same session, no wait.
- L12 901 (time waiting per approval gate): `hooks.log` per-gate totals — `raw-hac/31-hooks-log-totals.txt`.
- Unmeasurable here (outside this repo — OTel export, an incident tracker): not invented.

## Not confirmed

Live GitHub Actions (no self-hosted runner registered; every check above ran locally). Linux.
Live `evals` (no `ANTHROPIC_API_KEY` in this session). In runs B and C, "H" is the parent session
role-playing the original playbook's human actors in sequence — not an actual separate person at
each gate. Runs B and C's H turns are not in the raw jsonl — a `claude -p` stream does not echo
its own input back, so what H said is known only indirectly, through the response quoting it and
through the drafts it produced. A later harness should record H's turns to raw separately.
L4 317 (an engineer who never saw the conversation implements from plan.md alone) was not
measured: in runs B and C the implementation turn resumed the plan-mode session (0008
`836163ef`, 0009 `f643bd77`), so the implementer had seen the conversation. A next run starts
the implementation turn as a fresh session given plan.md only.
