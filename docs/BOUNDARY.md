# Boundary — what the machine sees, what a skill says, what a person decides

The user's rule for this repo (2026-09-09): procedure checking does not go into code; the agent must
stay flexible; code is added only where a lesson says a check matters and code can keep it from
breaking. The test is one sentence: **code stays only where the lesson itself names a
deterministic layer** — a hook, a deterministic script, or a CI merge check.

## The three layers

| Layer | Lives in | Lesson sentence that puts it there |
|---|---|---|
| The machine sees | `.claude/hooks/` wired in `settings.json`; `tests/`, `evals/`, `.github/` | L7 513 "a hook is the deterministic layer behind it"; L9 631 "A hook that blocks edits to test files during a fix task"; L12 821 "each gate as a hook … allow, ask, or block"; L13 963 "arrives as a PR through branch protection" |
| A skill says | `.claude/skills/*/SKILL.md`, `CLAUDE.md`, `REVIEW.md` | L6 503 "A skill is a control, though an advisory one." |
| A person decides | the PR: merge or close | L2 231 approval "is recorded as the merge or the closing review"; L3 276 "A human teammate always makes this call"; L11 762 "Findings do not approve or block a PR" |

## Why a checker inside the tree is not an approval authority
An in-tree validator reads the same tree the PR changes. A PR can edit the validator, its fixtures
and its expectations in the same diff it is meant to judge, and the check goes green. This repo's
first build (chain 0001) had an approval-status check; its "accepted on a branch" axis was
rewritten three times and each time a variant passed. The only check a PR cannot rewrite is the
one outside the tree: a person merging or closing it. That is where the lessons put approval.

So: artifact form, status and transitions are **not** checked by code here. The skill says what the
file must contain, the product owner reads it, and the merge records the decision.

## What the machine may still see
- A fix task editing a test file (L9 631) — hook.
- A credential in the diff (L7 521 "Keep credentials out of the diff") — hook.
- A protected path edited (L7 517), a broken file after an edit (L7 519), a production deploy
  without a release authorization (L12 848–857) — hook.
- Not here: a plan-sync hook. L4 329 says "Consider using a hook" — optional; this repo does not
  have one, the plan skill says to update plan.md in the same commit.
- `make check` red on a PR (L13 963, through branch protection) — CI.
Each of these is named by the lesson as a hook or a check. Nothing else is.

## What the seven reference repos did instead
All seven put the three layers in one place — a validator that also carried policy and approval —
and none of the seven had a validator that held (hooks unwired, `jq` fail-open, examples that broke
their own templates, routes to skills that did not exist). This file exists so that the next person
does not rebuild that.
