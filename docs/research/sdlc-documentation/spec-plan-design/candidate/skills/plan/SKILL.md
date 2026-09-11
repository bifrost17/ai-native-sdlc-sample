---
name: plan
description: Turn an accepted spec and its linked design documents into an executable implementation plan, or revise it when work changes. Connect real paths, test-first work, PR boundaries, release state and integration proof without approving the plan or implementing the product.
---
# Plan

Read intent, spec.md and every declared required design document, actual code/tests and applicable project policies.
Confirm the spec revision and human acceptance or already-authorized draft scope. Keep Upstream at that real revision,
Status draft and the authorization limitation where relevant. Initial planning does not edit production code.

Use the project's templates/plan.md; this candidate's copy is [the form](../../templates/plan.md).
Keep four roles linked, not four disconnected lists: actual paths/new files and responsibilities; concrete order and
dependencies; meaningful risks/detection/response; named existing/new checks with commands and expected results.
Do not move undecided important interfaces/classes/schema from spec into a private implementation task.

Start each new/changed behavior with its named first test/fixture and expected failure before the production change.
Sequence behavior slices, minimal implementation and necessary refactoring; the team's TDD method owns the recurring
mechanics. Already-GREEN regressions and pure refactors need no artificial RED. Defects require the observed
reproduction test committed before protected fixing. Protection that blocks new tests needs the tests before that stage.
Do not force a commit/PR per cycle or copy every test body into the plan.

Use [execution blocks](../../guidance/execution-blocks.md) only for relevant multi-PR/parallel/operational work.
Keep cohesive code/tests/docs together, main deployable and latest combined-result checks explicit. Tasks, agents,
commits and PRs need not correspond. Identify concrete shared contract revision, owned files and integration/plan
coordination for parallel sessions. Shared files need sequencing even if code work is independent.
For release controls, include the shared control/configuration, PR-specific general/test state, release/disable owner,
final whole-feature proof and cleanup conditions. A partial ON check cannot accept the whole release unit.

Read [F01](../../examples/F01/plan.md), [B01](../../examples/B01/plan.md),
[F03](../../examples/F03/plan.md), or [M01](../../examples/M01/plan.md) with the associated input and spec as needed.
Probe what can break, the riskiest step, omitted alternatives and how to recognize success with the engineer.
Someone without the chat should implement using the plan and its declared references; resolve consequential gaps.
Unknown operational commands may wait until before operations when code design is independent; state that boundary.
Do not invent paths as observed facts, test results or acceptance. The engineer decides readiness.

During implementation update affected paths/order/PR/proof and reason in that implementation commit.
Contract/design changes update the appropriate spec documents through its feedback process. Repin a downstream
reference only to an existing recorded upstream revision; a document cannot refer to its own future commit hash.
Use an existing current-change linkage for simultaneous spec/plan edits, as described in execution blocks.
Preserve actual evidence in execution/PR records instead of adding a new state ledger.
