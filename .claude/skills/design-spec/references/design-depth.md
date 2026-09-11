# Add only the design detail that changes a decision

Use the rows that fit the change. They are prompts for judgment, not headings to copy or a checklist
requiring an N/A explanation for every row. Keep the important decision and its consequences in the spec.

| Change | Detail worth considering |
|---|---|
| API, UI or integration boundary | Who can do what; request/response or state meaning; representative full user journey; empty, denied and failure behavior; compatibility with existing consumers. Link an actual approved mock/contract when used and distinguish its binding parts from illustration. |
| Stored data or migration | Current and target representation, invariants and ownership, partial failure, retries, coexistence or downtime, conditions for cutover and recovery. Account for writes after cutover and preserve the important invariants when service resumes. Exact run commands and operator steps belong in plan. |
| Incomplete integration or staged exposure | Agreed release unit, ordinary default and trusted test audience, directly reachable/effect boundaries, failure/default behavior and release/disable contract. Follow docs/RELEASE-CONTROL.md; the plan owns the control/configuration, responsible person, verification and eventual removal steps. A flag does not replace authorization or data recovery. |
| Concurrency or shared state | Which updates must be atomic, what a repeat/conflict means, and what readers can see. Identify the shared contract so separately implemented parts do not choose incompatible assumptions. |
| Performance or external dependency | Actual workload/measurement basis when known, acceptable degradation or failure, important limits and operating cost. If evidence is missing, state the uncertainty and what decision it affects rather than inventing a target. |
| Several modules or teams | Shared interfaces and constraints, existing components reused, changes that must agree and the integration result to verify. Let plan own work packages, file ownership and PR order. |

A short decision paragraph can explain context, the chosen option, a meaningful rejected option and
the drawback. Add tables, examples or a diagram only when they improve understanding. Internal
method names or sample pseudocode are illustrative unless the contract depends on them.

Prefer relevant subsections inside Design. If an existing external artifact carries contract detail,
identify its exact source/version and which part is authoritative; distinguish background references.
Keep important behavior, choices and concerns visible in this spec so a short summary does not conceal
a different contract. This does not require a second design approval workflow or a new document type.
