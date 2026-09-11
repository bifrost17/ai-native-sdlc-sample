---
name: tdd
description: Implement new or changed behavior with an observed test-first feedback loop, or assess whether that loop was followed. Use during implementation and behavior-changing fixes; preserve existing proof for pure refactoring. This team default supports the project policy without granting approval or changing scope.
---
# Test-driven development

Read the affected spec (including its declared design documents), plan, actual code and existing test commands.
Use the team's required test-first approach for new/changed behavior. Select one meaningful behavior or boundary
at a time; do not build a batch of production changes before running their first tests.

1. Write a focused behavior test before its production change. Derive expectations from the agreed contract,
   examples, an independent calculation or a trusted reference, not by copying the implementation's answer.
   Exercise the real boundary when practical; substitute external/slow effects without mocking away what is proved.
2. Run it and inspect why it fails. Missing behavior or a deliberately not-yet-created planned boundary can be
   expected RED; syntax, wrong imports/paths, bad fixtures or unrelated environment failures are not proof.
   Resolve setup failures and confirm the behavior assertion discriminates the missing behavior.
3. Make the smallest adequate production change and rerun the same expectation to GREEN. Add the next case
   when it teaches new behavior or a material boundary. A case already GREEN is useful regression evidence;
   do not break production code just to manufacture RED.
4. Refactor where it improves the design, keeping behavior expectations stable, then rerun affected and neighboring
   tests. Before reporting completion, run the project's required checks and verify the latest combined result.

For a defect, reproduce it in a test, run and confirm the expected failure, and commit that test before the protected
fix stage. Make it pass without altering the frozen test. If a frozen test is demonstrably wrong, leave that stage
and have the engineer resolve/refix the reproduction through the existing process; do not bypass test protection.
Pure refactoring uses existing behavior tests as a baseline; add missing protection before refactoring where needed.
No new behavior means no manufactured RED.

Do not skip/delete/relax assertions merely to get GREEN. A changed requirement, a demonstrated test defect or a
retired release-control phase can justify a test change: preserve the independent basis, update the affected spec
and plan with the related implementation, and retain the still-valid regressions. Review a consequential test change
independently. Do not turn an implementation mismatch itself into a new expected value.

If implementation came first, record the deviation honestly. Add missing independent behavior proof and assess
the affected risk with the engineer/reviewer; do not claim retroactive TDD or delete/rebuild working code by ritual.
If executable test-first proof is infeasible (for example an exploratory spike or a manual-only change), expose
why before dependent implementation and obtain the engineer's bounded alternative; do not silently substitute
test-after for the team's required approach. Existing authorization for that exact alternative remains valid.

When discoveries change contracts/design, update the relevant spec documents; when paths/order/PR/proof change,
update the affected plan in the same implementation commit. Keep actual commands, revision, expected failure reason,
results and meaningful deviations in existing execution/PR records. Do not add a per-cycle state ledger or approval.
Use a model/effort suited to uncertainty and impact for difficult design/test-oracle decisions; repeat errors call for
better evidence/context or stronger review, not a rule for every possible mistake.
