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
Evals' deterministic checks (`evals/check.sh` `kind`s) only judge code shape — a regex over the
diff. Behavior is judged by the LLM assertions in each case and by the unit/regression tests.

## What the seven reference repos did instead
All seven put the three layers in one place — a validator that also carried policy and approval —
and none of the seven had a validator that held (hooks unwired, `jq` fail-open, examples that broke
their own templates, routes to skills that did not exist). This file exists so that the next person
does not rebuild that.

## Lesson devices this repo does not build
The lessons name more than a small repo can stand up, and more than this change touches. Each of
these is a device the playbook names; this repo does not build it, and here is why not.
- **Intent merge → auto-PR'd spec.md** (L3 268, "commits spec.md as a pull request" on the merge
  of an accepted intent). This is the end state of a hand-run product-owner prompt codified as a
  slash command; the CI trigger and model-access wiring are an org-level infrastructure decision,
  not something the source tree alone settles.
- **An "ask" verdict from a hook** (L12 821, "allow, ask, or block" — the worked example at 850–861
  only shows block). All five hooks here are allow/block only; "ask" needs an interactive channel
  back to a human mid-tool-call, and that channel is outside this repo's tree.
- **`claude -p` triage, sandboxed jobs, MCP-exposed deploys, rehearsed rollback** (L13 961, 965,
  967, 971). All four presuppose running infrastructure — containers, network policy, a deploy
  tool with MCP tools registered, a staging environment to rehearse in — that a checked-out
  source tree cannot provide or prove.
- **20-50 real eval cases** (L10 685). `evals/cases/` holds three, enough to prove the harness
  runs; filling it to the lesson's count needs that organization's actual recent task history,
  which this sample repo does not have.
- **A test that a skill actually triggers** (L6 470, "confirm the skill loads each time"). That is
  a person running live sessions with differently-worded prompts and watching whether the skill
  loads — coding it as a deterministic check would mean hard-coding the trigger phrase, which
  proves the phrase matches itself, not that the skill fires on real, varied prompts.
