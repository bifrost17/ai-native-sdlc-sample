# Spec: `main` = template + its own chains; experiments on `experiment/<date>-<topic>` branches
Upstream: intent.md@4c3f0e599c1b1d08a1e61ddf901a5d2d6a5f1228. Status: draft.
Skills applied: none — no external-facing endpoint; `design-spec` read.
## Requirements
- R1 `main` keeps: `.claude/`, `CLAUDE.md`, `REVIEW.md`, `templates/`, `docs/` (minus `RUNS.md`), `Makefile`, `.github/`, `org/`, `ops/`, `scripts/`, `evals/` (cases 01–03 and their fixtures/testdata), `tests/` (hooks, evals, bands, managed settings, skill template, `tests/data/bands/` minus the 0006 sample), `intent/0001`, `intent/0004`, this chain.
- R2 `main` drops: `intent/0002`, `0005`, `0006`, `0007`, `0008`, `0009`; `src/`; `tests/test_claims_status*.py`, `tests/test_adjuster_status.py`, `tests/test_agent_status.py`; `tests/data/bands/claims-status-not-found-spike.jsonl`; `evals/cases/04-*` and `evals/fixtures/04-*`; `docs/RUNS.md`.
- R3 The experiment branch `experiment/2026-09-09-claims-status` is created from `0daf6550` before anything is removed, carries `raw/` and `EXPERIMENT.md`, and is never merged.
- R4 `README.md` gains an Experiments section (branch, base commit, rule); the chain table keeps only the template's own chains.
- R5 Every remaining reference to a removed path (`docs/RUNS.md`, eval case count, chain 0005/0006 "executed as" notes, the bands sample table) points at the experiment branch or states the new count.
- R6 `make check` is green on the stripped tree.
## Design
One PR, four commits: this chain's three artifacts, then one removal commit. Removals are `git rm` by path (no `git add -A`). Text edits are local replacements, asserted to match exactly once. The experiment branch is pushed first (done: `cebc0e5`), so the removal never touches the only copy.
## Constraints
- Nothing is lost: the experiment branch is pushed from `0daf6550` before any removal (carried from intent.md).
- Template tests do not import the example app (carried; checked by `grep` before the chain opened).
- Chain mentions in skills, CLAUDE.md and REVIEW.md stay — they are lessons, not experiment output (carried).
## Open questions from intent
- Branch or GitHub template repository for future experiments → **answered** by the author on 2026-09-09: branch. Nothing carried forward.
## Flagged concerns
- The verification document's citations of experiment paths now resolve on the branch, not `main` — its README says so (F1, resolved by a note there, not by this repo).
## Out of scope
- Turning the repo into a GitHub template repository.
- Rewriting the verification document's citations — its README notes where the paths now live.
- Any change to the template's behaviour; this chain moves files and edits references only.
## Acceptance criteria
- AC1 `git ls-files` on `main` after merge contains no `src/`, no `intent/000[25-9]-*`, no `docs/RUNS.md`, no `evals/cases/04-*`.
- AC2 `make check` exits 0 on `main` after merge.
- AC3 `origin/experiment/2026-09-09-claims-status` contains every file `main@0daf6550` had, plus `raw/` and `EXPERIMENT.md`.
- AC4 `grep -rn 'docs/RUNS.md' README.md docs CLAUDE.md REVIEW.md .claude` on `main` returns only lines that name the experiment branch.
