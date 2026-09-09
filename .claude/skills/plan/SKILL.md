---
name: plan
description: In plan mode, turns an accepted spec.md into plan.md — the files that change, the order of work, the risks, and the proof — and iterates with the engineer until someone who never saw the conversation could implement from the plan alone. Does not write code, and does not accept the plan.
---
# Plan

> L4 317: "The engineer gives Claude the intent.md and the spec.md and asks for an implementation
> plan that names the files that change, the order of the work, and the tests that prove it."
> L4 321: "Iterate until an engineer who has never seen the conversation could implement the
> change from the plan alone."
> L4 329: "When implementation departs from the plan, update plan.md in the same commit."

## Inputs
`intent/<NNNN>-<slug>/intent.md` and `spec.md`, both accepted (merged — a commit on `origin/main`
for each file; the `Status:` line stays `draft` by design and is not the test). For a defect chain
(L9 625 failing test first) the engineer opens the session with `INTENT_TASK=fix`; nothing sets
it for you, and without it the test-file hook (L9 631) is off. For a feature chain do **not** set
it — with `INTENT_TASK=fix` on, the hook also blocks creating the new test file (chain 0008). Record
`Upstream: spec.md@<sha>. Status: draft.` at the top of plan.md, and leave it `draft`: approval
is the merge of the PR that carries the plan (L2 231), nothing flips this line by hand. (Chain 0009
wrote `accepted` there for the upstream spec's PR, and the line stopped saying whose status it was.)
One exception: an engineer may tell you to start on a draft (a single worker stacking PR B on
the intent PR A). Immediately below the Upstream/Status line, write one line naming who told
you and why, and repeat it in the PR body — approval is still the merge, not this note.
Read the codebase without changing anything — that is what plan mode is for.

## Write `plan.md` with four sections (`templates/plan.md`)
- **Files that change** — real paths, `(new)` where new.
- **Order of work** — the failing test comes before the change that makes it pass.
- **Risks** — what the change could break, which step is riskiest, how you would notice.
- **Proof** — tests by name, and the output or screenshot that shows the behaviour.
  Mutation checks restore the original bytes you saved (compare sha256), never `git checkout --` —
  that also discards your uncommitted fix (chain 0008).

## Interrogate before accepting
Ask, and write the answers into Risks and Proof: what could this break? which step is most
risky? what did you choose not to do, and why? Iterate until the plan stands without the
conversation. Then the engineer accepts the plan — plan mode itself records that; nothing else does.

## While implementing
If the work departs from the plan, edit plan.md in the same commit. The PR review (REVIEW.md,
compliance pass) reads the diff against plan.md.

## What this skill does not do
- Does not write code while the plan is being written.
- Does not accept the plan — the engineer does, in plan mode.
- Does not write spec.md or intent.md.
