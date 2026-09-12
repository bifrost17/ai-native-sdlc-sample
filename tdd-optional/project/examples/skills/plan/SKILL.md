---
name: plan
description: Turn an accepted spec and linked design documents into an executable implementation plan, revise it when work changes, or frame an authorized bounded exploration needed before a dependent design decision. Connect real paths, task-specific verification strategies, PR boundaries, release state and proof without approving the plan or implementing the product.
disable-model-invocation: true
---
# Plan

팀이 선택하여 읽거나 설치·수정할 수 있는 자체 작성 예시다. 이 위치에서는 자동 로드되지 않는다.

North star L4 317–321: name changed files, work order and proving tests; support an engineer without the conversation.
L4 329: update plan.md in the same implementation commit when work departs from it.

Read the current intent. For product planning, read spec.md and every declared required design document, actual
code/tests and applicable project policies. Confirm the spec revision and human acceptance or already-authorized draft scope.
For a bounded exploration before design acceptance, instead read the current intent/draft question, relevant product
context and recorded exploration authority; do not call it an accepted product plan. Keep Upstream at the real revision
that exists, Status draft and the authorization limitation where relevant. Follow the project's
[Git policy](../../../docs/GIT-WORKFLOW.md) for the document/SHA/decision maker/reason recorded at stage acceptance.
Initial planning does not edit production code.

Use [the project's plan form](../../../templates/plan.md) and choose the feedback order with the
[verification-strategy guide](../../../docs/TESTING-STRATEGY.md).
Write in the originator's language while retaining the four English section names. Link the four roles:
actual paths/new files and responsibilities; concrete order and dependencies; meaningful risks/detection/response;
named existing/new checks or direct observation procedures with expected results.
Do not move undecided important interfaces/classes/schema from spec into a private implementation task.
For a product plan, open with how the chosen design reaches a working product, linking its authoritative decisions rather
than copying them. For an exploration, open with the unresolved question, fixed constraints and adoption boundary.
For a task that will be handed off or whose evidence is scattered, group its purpose, required contracts, paths,
chosen strategy and reason, independent expected behavior, implementation/observation/check order and completion observation together in the relevant plan block.
Use Files/Proof as indexes and keep one authoritative statement of each detailed expectation. Small plans can remain
a few connected steps. There is no task-count threshold or requirement to repeat the same baseline at every task.

Choose TDD, incremental implement-then-test, existing-tests, exploration/direct observation, or a useful mix for the task
using its risks, contract stability, uncertainty and current coverage. Exploration can precede a stable delivery strategy;
it is not evidence that the resulting product is complete.
Record the choice and reason under Order of work or the task block; choosing non-TDD requires no extra exception approval.
Name the source of consequential expectations: accepted spec/AC, owner or policy decision, protocol, pinned reference data,
independent calculation or another trusted input. Never merely copy implementation output into tests.
For TDD, name the first behavioral test/fixture and meaningful expected failure before production changes.
For implement-then-test, finish implementation and verification of each small behavior before proceeding to the next.
For existing-tests, identify which AC they actually cover and add checks where coverage is insufficient.
For hybrid, name each task's strategy. Product-delivery choices retain acceptance checks, adjacent regressions and integration proof.
An exploration retains its learning question, fixed constraints, observations, limitations and discard/adoption decision instead.
Already-GREEN regressions and pure refactors need no artificial RED; later replay on a baseline does not establish TDD history.
For defects, encourage diagnosing the symptom before fixing; distinguish manual/temporary reproduction from permanent regression tests.
Explain reproduction limits and keep meaningful regression protection. Do not force a commit/PR per cycle or copy every test body into the plan.
For an exploratory task, state the question, fixed constraints, observation procedure and discard or product-adoption boundary.
If its result is adopted, update the affected spec/AC and create or revise the dependent product steps before implementation.
Do not turn a successful experiment, screenshot or mocked flow into a product-completion claim.

Use the project's actual test-protection mechanism when one applies; if it requires tests committed before protected fixing,
prepare and commit them before that stage. Do not assume this template installs a protection hook or mandates that stage for every defect.
When a validation temporarily mutates a fixture/source, restore the saved original bytes, not unrelated user work.

Use [execution blocks](references/execution-depth.md) only for relevant multi-PR/parallel/operational work.
Keep cohesive code/tests/docs together, main deployable and latest combined-result checks explicit. Tasks, agents,
commits and PRs need not correspond. Identify concrete shared contract revision, owned files and integration/plan
coordination for parallel sessions. Shared files need sequencing even if code work is independent.
For release controls, include the shared control/configuration, PR-specific general/test state, release/disable owner,
final whole-feature proof and cleanup conditions. A partial ON check cannot accept the whole release unit.

Read [F01](../../../docs/sdlc-authoring/examples/F01/plan.md), [B01](../../../docs/sdlc-authoring/examples/B01/plan.md),
[F03](../../../docs/sdlc-authoring/examples/F03/plan.md), or [M01](../../../docs/sdlc-authoring/examples/M01/plan.md) with the associated input and spec as needed.
For a UI/API boundary and user-visible states, use [W01](../../../docs/sdlc-authoring/examples/W01/plan.md).
For compact plan-only examples, use [existing-test refactoring](examples/refactor-existing-tests.md) or
[disposable UI exploration](examples/disposable-ui-exploration.md).
Probe what can break, the riskiest step, omitted alternatives and how to recognize success with the engineer.
Someone without the chat should execute the planned implementation or exploration using its declared references; resolve consequential gaps.
Unknown operational commands may wait until before operations when code design is independent; state that boundary.
Do not invent paths as observed facts, test results or acceptance. The engineer decides readiness.

During implementation update affected paths/order/PR/proof and reason in that implementation commit.
Contract/design changes update the appropriate spec documents through its feedback process. Repin a downstream
reference only to an existing recorded upstream revision; a document cannot refer to its own future commit hash.
Use an existing current-change linkage for simultaneous spec/plan edits, as described in execution blocks.
Preserve actual evidence in execution/PR records instead of adding a new state ledger.
Large plans may link task/PR detail documents from plan.md when reading/ownership boundaries justify it; include them
in handoff and affected-document updates. Do not split by file length or describe unresolved future work as ready to execute.
