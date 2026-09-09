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
`intent/<NNNN>-<slug>/intent.md` and `spec.md`, both accepted (merged) — or, if an engineer
started you on a draft (see design-spec, "one exception"), say so at the top. Read the codebase
without changing anything — that is what plan mode is for.

## Write `plan.md` with four sections (`templates/plan.md`)
- **Files that change** — real paths, `(new)` where new.
- **Order of work** — the failing test comes before the change that makes it pass.
- **Risks** — what the change could break, which step is riskiest, how you would notice.
- **Proof** — tests by name, and the output or screenshot that shows the behaviour.

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
