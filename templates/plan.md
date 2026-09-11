# Plan: ‹what is built› (from intent ‹NNNN-slug›)
Upstream: spec.md@‹commit sha of the accepted spec›. Status: draft.
‹Name the scope and references needed to implement without the conversation. Keep this brief.›

## Files that change
‹Real paths and what changes in each; mark new files. Include tests and usage/operations docs when affected.›

## Order of work
1. ‹Establish the relevant baseline or reproduce the defect; name the result needed for the next step.›
2. ‹Implement and connect the concrete behavior, with its checks.›
3. ‹Verify the integrated result and prepare the handoff.›
‹For multiple PRs, group by reviewable purpose: scope, dependencies/merge order, what works on main
after each merge, what remains, and its proof. When release is controlled, include ordinary/test exposure
after each PR and the shared control/configuration, release/disable steps, owner and removal condition
(docs/RELEASE-CONTROL.md). Tasks, commits, agents and PRs need not map one-to-one.
For parallel work, identify worktree/file boundaries, shared contract references and integration/plan coordination.
Use only the detail this change needs; follow docs/GIT-WORKFLOW.md and docs/PR-SIZE.md.›

## Risks
‹Material regressions and the riskiest step; how to notice and respond. Refer to spec decisions instead of copying them.›

## Proof
‹Connect the planned results to named checks/commands or observations and expected outcomes.
Distinguish existing checks from checks to add. Include relevant neighboring behavior and combined-result checks;
reference these at risky steps/PR boundaries. Record any verification limit and what resolves it.›

‹These are planned checks; keep actual evidence in the implementation/PR record. If implementation departs
from the plan, update the affected plan and reason in that implementation commit. Revisit spec/intent when affected.›
