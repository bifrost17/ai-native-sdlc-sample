---
name: plan
description: Turn an accepted spec and its linked design documents into an executable implementation plan, or revise it when work changes. Connect real paths, test-first work, PR boundaries, release state and integration proof without approving the plan or implementing the product.
disable-model-invocation: true
---
# Plan

팀이 선택하여 읽거나 설치·수정할 수 있는 자체 작성 예시다. 이 위치에서는 자동 로드되지 않는다.

North star L4 317–321: name changed files, work order and proving tests; support an engineer without the conversation.
L4 329: update plan.md in the same implementation commit when work departs from it.

Read intent, spec.md and every declared required design document, actual code/tests and applicable project policies.
Confirm the spec revision and human acceptance or already-authorized draft scope. Keep Upstream at that real revision,
Status draft and the authorization limitation where relevant. Follow the project's
[Git policy](../../../docs/GIT-WORKFLOW.md) for the document/SHA/decision maker/reason recorded at stage acceptance.
Initial planning does not edit production code.

Use [the project's plan form](../../../templates/plan.md).
Write in the originator's language while retaining the four English section names. Link the four roles:
actual paths/new files and responsibilities; concrete order and dependencies; meaningful risks/detection/response;
named existing/new checks with commands and expected results.
Do not move undecided important interfaces/classes/schema from spec into a private implementation task.
Open with how the chosen design reaches a working product, linking its authoritative decisions rather than copying them.
For a task that will be handed off or whose evidence is scattered, group its purpose, required contracts, paths,
first behavioral test/expected failure, minimal change and completion observation together under its PR.
Use Files/Proof as indexes and keep one authoritative statement of each detailed expectation. Small plans can remain
a few connected steps. There is no task-count threshold or requirement to repeat the same baseline at every task.

Start each new/changed behavior with its named first test/fixture and expected failure before the production change.
Sequence behavior slices, minimal implementation and necessary refactoring; the team's TDD method owns the recurring
mechanics. Already-GREEN regressions and pure refactors need no artificial RED. Defects require the observed
reproduction test committed before protected fixing. Protection that blocks new tests needs the tests before that stage.
Do not force a commit/PR per cycle or copy every test body into the plan.

Use the project's actual test-protection mechanism when one exists; prepare and commit reproduction
tests before entering a protected fix stage. Do not assume this template installs a protection hook.
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
Probe what can break, the riskiest step, omitted alternatives and how to recognize success with the engineer.
Someone without the chat should implement using the plan and its declared references; resolve consequential gaps.
Unknown operational commands may wait until before operations when code design is independent; state that boundary.
Do not invent paths as observed facts, test results or acceptance. The engineer decides readiness.

During implementation update affected paths/order/PR/proof and reason in that implementation commit.
Contract/design changes update the appropriate spec documents through its feedback process. Repin a downstream
reference only to an existing recorded upstream revision; a document cannot refer to its own future commit hash.
Use an existing current-change linkage for simultaneous spec/plan edits, as described in execution blocks.
Preserve actual evidence in execution/PR records instead of adding a new state ledger.
Large plans may link task/PR detail documents from plan.md when reading/ownership boundaries justify it; include them
in handoff and affected-document updates. Do not split by file length or describe unresolved future work as ready to execute.
