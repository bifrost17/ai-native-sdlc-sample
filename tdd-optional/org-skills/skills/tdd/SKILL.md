---
name: tdd
description: Apply or review an observed RED-to-GREEN feedback loop when the user or current plan selects TDD for a behavior or work slice. Use automatically within that selected scope, including behavior-changing review fixes; other verification strategies do not activate this skill. Preserve existing proof for pure refactoring.
---
# Test-driven development

Read the affected spec (including its declared design documents), plan, actual code and existing test commands.
Apply this procedure only to the scope for which the user or plan selected TDD. The project may choose
TDD, behavior-by-behavior implementation followed by tests, existing-test reuse or a mix with reasons;
choosing another strategy is not an exception or an approval event. An explicit request to use this skill
selects TDD for that requested scope. In a mixed plan, apply it only to the TDD slices.
If the current request or discovery changes the contract/design or plan, reflect the authorized change in the
affected spec documents and plan before starting its test-first cycle.
For the selected TDD scope, use test-first for new/changed behavior. Select one meaningful behavior or boundary
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

For a defect in a TDD slice, reproduce it in a test and confirm the expected failure before the fix.
If this project already uses a protected reproduction/fix stage, preserve its frozen-test boundary;
a demonstrably wrong frozen test must be corrected through that existing process. This skill does not
introduce such a stage or a separate test commit into a project that has not adopted it.
Pure refactoring uses existing behavior tests as a baseline; add missing protection before refactoring where needed.
No new behavior means no manufactured RED.

Do not skip/delete/relax assertions merely to get GREEN. A changed requirement, a demonstrated test defect or a
retired release-control phase can justify a test change: preserve the independent basis, update the affected spec
and plan with the related implementation, and retain the still-valid regressions. Review a consequential test change
independently. Do not turn an implementation mismatch itself into a new expected value.

If implementation came first in a slice selected for TDD, record the deviation honestly. Add missing independent behavior proof and assess
the affected risk with the engineer/reviewer; do not claim retroactive TDD or delete/rebuild working code by ritual.
If executable test-first proof is infeasible (for example an exploratory spike or a manual-only change),
record why and update the chosen strategy and its independent proof in the plan before dependent work.
Reuse existing authority for technical choices; ask only for a material decision outside that authority.
Do not label implementation-then-test or a later baseline replay as historical TDD.

When discoveries change contracts/design, update the relevant spec documents; when paths/order/PR/proof change,
update the affected plan in the same implementation commit. Keep actual commands, revision, expected failure reason,
results and meaningful deviations in existing execution/PR records. Do not add a per-cycle state ledger or approval.
Use a model/effort suited to uncertainty and impact for difficult design/test-oracle decisions; repeat errors call for
better evidence/context or stronger review, not a rule for every possible mistake.
