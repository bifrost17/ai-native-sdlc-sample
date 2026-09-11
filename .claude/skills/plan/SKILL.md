---
name: plan
description: Turns accepted requirements and design into an implementation plan before code changes, or revises that plan when execution changes. Reads real files, connects work and PR boundaries to proof, and iterates with the engineer for a handoff that stands without the conversation. Does not approve the plan.
---
# Plan

> L4 317: "The engineer gives Claude the intent.md and the spec.md and asks for an implementation
> plan that names the files that change, the order of the work, and the tests that prove it."
> L4 321: "Iterate until an engineer who has never seen the conversation could implement the
> change from the plan alone."
> L4 329: "When implementation departs from the plan, update plan.md in the same commit."

## Read before writing
Read the change's intent.md, spec.md and the actual code, checks and relevant project policies.
Confirm the spec revision and the human decision that permits this next step; a previous accepted
revision does not approve unreviewed edits. Follow docs/GIT-WORKFLOW.md: stage acceptance records
the document/SHA, decision maker, decision and reason in the Draft PR or preserved decision record.
It does not require a PR per document or replace final integration approval. Keep
`Upstream: spec.md@<sha>. Status: draft.`. If the engineer has already authorized work from a draft,
record that scope and reason without asking again. Plan mode is a reading mode, not approval evidence.
While initially planning, inspect the product without editing it; write the plan only as authorized.

## Record enough to execute
Use templates/plan.md in the change's intent folder. The four sections are information roles, not
a demand for four independent lists. Connect files, steps and proof so the next reader can act.

- **Files that change:** verified paths and each change's role; mark new files, including relevant tests/docs.
- **Order of work:** concrete results and needed inputs, including wiring into the product. A small change
  can be a few steps in one PR. For multiple PRs, name each reviewable purpose, included work,
  dependency/merge order, working main state after merge, remaining scope and proof. Keep one behavior's
  implementation/tests/docs together unless there is a substantive reason to split.
- **Risks:** material neighboring regressions, the riskiest step, its detection/response and significant
  rejected execution alternatives. Do not duplicate the spec's entire design discussion.
- **Proof:** checks by name, command/observation and expected result tied to the relevant AC or behavior.
  Distinguish checks that exist from ones to add. Put feedback at meaningful steps, not only at the end;
  include combined-result verification. Planned evidence is not observed success.

For defects, add the regression test, observe failure for the expected reason and commit it before
the fix; then make it pass without weakening it. Other changes use the appropriate baseline and
feedback loop. In this maker repo, write and commit the reproduction test before the engineer starts
the fix session with INTENT_TASK=fix: the hook also blocks creating new tests while that mode is on.
Do not enable fix mode for ordinary features. When using mutation checks, restore saved original
bytes rather than discarding unrelated uncommitted work.

For multi-PR, parallel or operational changes, read [conditional guidance](references/execution-depth.md).
Choose only needed examples: [small feature](examples/feature.md), [defect](examples/bug.md),
[two PRs](examples/two-pr.md), [migration/parallel work](examples/migration.md).

## Review and revise with the engineer
Probe what could break, the riskiest step, omitted alternatives and how success will be recognized.
Resolve consequential missing information; do not invent paths, test results or decisions. The
engineer should be able to hand the plan and its declared references to someone who saw no chat.
Record the answers in the plan rather than relying on a final chat message. The engineer accepts it;
this skill does not write product code as part of initial planning or approve its own work.

During implementation, changes to files/order/PR boundaries/proof update the affected plan and reason
in the same implementation commit. If behavior, design, scope or acceptance criteria change, update
the spec through that authoring flow; revisit intent when purpose/constraints change. Record any
required revised upstream decision and commit before repinning. Do not reapprove every allowed
implementation detail or edit unaffected documents. Use the team's available review methods with
model/effort appropriate to the decision; no particular external skill or tool is required.
