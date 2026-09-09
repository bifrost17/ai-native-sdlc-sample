# Intent: experiment output sits on `main` next to the template it was testing
Author: the user (product owner), via the parent session. Status: draft.
First conversation: 2026-09-09 (stated by the author).
## Problem
- `main` at `0daf6550` holds the template (~1,900 lines: `.claude/`, `CLAUDE.md`, `REVIEW.md`,
  `templates/`, `docs/`, `Makefile`, `.github/`, `org/`, `ops/`, `scripts/`, the evals harness) and,
  mixed in, the output of the 2026-09-09 experiments (~2,500 lines): chains `intent/0002`, `0005`,
  `0006`, `0007`, `0008`, `0009`, the example app `src/claims_status/`, its tests, the incident eval
  `evals/cases/04-*`, and the run record `docs/RUNS.md`. The raw evidence those records cite is not
  in the repo at all.
- The chain branches were deleted at merge, so nothing on the remote separates "the template" from
  "what one experiment produced on it". Someone cloning `main` receives a claims-status app they
  did not ask for.
## Proposed outcome
`main` is the template plus the template's own chains (`0001`, `0004`, this one). Each experiment
lives on its own branch `experiment/<date>-<topic>` that never merges, carries its raw evidence,
and names the `main` commit it ran on; what an experiment reveals about the template returns to
`main` as a PR.
## Affected users and systems
Whoever clones `main` (adopters); the verification document, whose citations of experiment paths
must keep resolving; CI (`make check` must stay green without the example app).
## Constraints
- Nothing is lost: the experiment branch starts from `0daf6550` and adds only `raw/` and a note.
- The template's tests (hooks, evals harness, bands detector, managed settings, skill template) do
  not depend on the example app — verified before this chain was opened.
- Playbook citations in the template that mention chains 0002–0009 stay; they are the lessons the
  experiments taught the template.
## Open questions
- Whether future experiments should instead start from a GitHub template repository — decided
  2026-09-09 by the author: branches (this chain), not repositories.
