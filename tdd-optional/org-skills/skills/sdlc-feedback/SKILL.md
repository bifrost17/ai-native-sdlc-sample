---
name: sdlc-feedback
description: Keep agreed requirements, spec, plan and implementation aligned. Use when preparing a spec or plan handoff, reviewing or revising important design contracts, implementing or departing from a plan, incorporating follow-up requirements, acceptance changes or design-changing brainstorming choices and recommendations, updating plans after test/review evidence, preparing related commits, reporting implementation complete, or reviewing a branch/PR. Questions and status-only requests do not call for completion review.
---
# SDLC feedback

Work in the developer's conversation so that the human's decisions remain available. Read
the **Review criteria** section of [sdlc-verifier.md](../../agents/sdlc-verifier.md) when comparing
agreements, artifacts and evidence. Its reviewer-only permissions apply to the verifier, not to
your developer session.
Use the part below that fits the current event; this is not an extra phase for every response.

## Spec and plan handoff review

Before handing a spec to planning or reporting design complete, apply the common Review criteria to the
current intent, complete declared spec document set and required existing contracts. State the actual
revision and whether the scope is a design slice or the handoff-ready spec. Make required linked criteria
and references accessible; a skill name, file hash or prior PASS does not establish that their content
was read or that the contracts are sufficient. Report inaccessible material as a limitation.

Small changes may use the author's check and existing owner review. Prefer a capable fresh-context
reviewer for consequential shared contracts or independent lifetimes, authority and recovery. This is
not a mandatory reviewer count or a new gate for every spec edit. When delegating design-only review,
use the verifier setup below and supply those inputs, agreements and scope; do not require a nonexistent
plan, implementation diff or execution results. Wait for the result before using it in the handoff conclusion. Keep the existing
implementation-completion check below: mixed work is scoped by its actual changes and completion claim,
not a design-only label.

At the existing design or plan handoff, compare cumulative effects with the current intent and constraints
when individually small choices materially change the target, meaning of success or cost; use that review's
scope rather than reviewing or recording every choice or adding approval steps.

Summarize the important contracts/branches examined, findings and their resolution, justified deferrals
and remaining limits in the existing review/handoff record. Do not total PASS votes as proof of readiness.
Distinguish design sufficiency, executed verification and human acceptance; reuse supplied authorization.

For a plan handoff, supply the current intent and authoritative design set, the actual revision to use,
the first deliverable, task order and dependencies, real implementation method, risks and rejected
alternatives, verification and handoff conditions. Review whether the next developer can start the first
task and reach the stated result. Do not require code, tests or execution results that do not exist yet.
Keep this scoped plan review separate from implementation completion and from human plan acceptance.

## Change or acceptance

Before incorporating a follow-up requirement, design-changing brainstorming choice or recommendation,
compare its reason and important factual premises with the current intent's problem, desired outcome and
constraints. Distinguish the human's request and actual decision from an agent proposal or unverified assumption;
do not invent a why or treat adoption of a solution as authorization to change its goal or constraints.
Reuse relevant intent passages and latest decisions already checked in this conversation while their revision
and meaning remain current; refresh them when the revision/decisions change or context is lost.
Proceed within clear delegation and supplied decisions. For a material conflict with the purpose or fixed
constraints, a disproved important premise, or an unclear reason with substantial impact, explain the effect
and ask only for the missing decision. Keep that incorporation open while independent work can proceed.
Do not ask again for a clear current decision or add a separate review to every choice.

Read the applicable project instructions and current intent/spec and any applicable plan, including the
complete design document set declared by spec. Check the current intent constraints against the changed behavior even
when the problem and goal are unchanged. Apply the common Review criteria to update the artifacts whose
meaning changed: requirements/design/acceptance criteria and the important choice's reason, intent connection
and preserved or weakened outcomes in the actual spec/design documents; affected execution/verification/PR
boundaries in plan. Revise the relevant intent prose first only when its purpose, constraints or core background
changed or need correction, then align downstream artifacts. A conversation or README does not substitute
for the affected artifact. Existing planning and policy skills retain their roles.
For implementation planning, record the chosen verification strategy (TDD, behavior-by-behavior implementation then tests, existing-test
reuse or a mix), its reason and coverage in plan. Selection does not create an exception or approval gate.
Make affected spec/design documents and the plan current before starting the changed behavior's implementation
and verification cycle; if a discovery changes them during implementation, update them before the next dependent change.

Start from the actual diff and trace its meaning through the applicable plan task (T), authoritative
design unit (SP), requirements/AC and current intent constraints. Do not infer consistency from which
documents changed. Existing IDs remain valid; older artifacts may use readable paths and sections, and
no all-ID gate is implied. Distinguish a spec-only or plan-only change, a missing real decision and a code
bug against an unchanged contract. Leave intent unchanged when its purpose, outcome, constraints and core background did not change.

Use human decisions already supplied. If the accepted upstream version changed, update downstream
references under the project's policy. Ask only for material decisions still missing; do not turn
an already clear answer into another approval request. Leave unaffected documents alone.
Distinguish an accepted baseline from current changes the human has already authorized drafting or
implementing; identify the actual current upstream content used by readable document paths and relevant
sections, without attributing later amendments to the baseline SHA.
A draft label does not erase that authorization or create a new acceptance gate.

When later test or review evidence changes what remains, update the current plan/handoff summary
and next steps, linking the actual tested revision and the existing evidence record. Preserve earlier
records and their authors as history. Passing checks do not themselves accept, merge or complete
outstanding work; keep the full execution results in their existing record.

Treat pause, handoff and resume as explicit work events. Without creating a new ledger, update the current
plan summary and existing execution record with the actual revision, completed and unverified work, pending
dependencies and the next step. On resume, compare that account with current artifacts, Git state and evidence
before dependent work. Expose conflicts without claiming forced-stop prevention or an all-work-ready verdict.
A status question alone does not trigger execution or artifact revision.

## Implementation and commit

Run the chosen feedback loop as work proceeds: use tests, permitted browser interaction or direct observation
suited to the behavior, with independent expectations, actual results and relevant regression evidence.
For exploration, record the learning question, constraints, observations and unresolved decisions. Answering
that question is not product completion; adopting the result requires current spec/AC, regression and integration
proof. A screenshot alone does not establish interactive behavior. Include affected intent/spec documents and plan changes, with the reason,
in the same commit as the related implementation. Before committing, inspect the actual staged scope and
related unstaged or untracked work without sweeping unrelated WIP into the commit. After committing, inspect
the resulting content. Follow the project's upstream acceptance and
Git policy; permission to inspect or review does not itself authorize a commit, push or merge.

If the project adopts the optional document-sync Git hook example, complete the existing pre-commit
meaning check in this session, stage only the needed changes, and pass its snapshot plus required
companion-document paths for that commit. Use an empty list when no companion amendment is needed;
do not create token edits or run a fresh verifier for every commit. Follow the project's actual installed
example instructions. The hook checks the declared staged scope and inclusion, not whether this review
occurred or the declaration/content is correct; it does not invoke this skill or grant completion.

## Completion and review

At a meaningful implementation delivery boundary, before requesting the existing final review, refresh the
current plan summary from the actual work and existing evidence: completed work, unverified scope, remaining
dependencies and the next step. Align the related row of the project's adopted change index when present.
Identify the checked commit/base and current amendments where relevant; do not require the commit's own future
SHA, overwrite historical records or copy full logs. Passing checks do not mean human acceptance, integration
or release. Update the existing account without adding a ledger or a review for every commit or prose edit.

Before reporting that implementation task complete, delegate the existing final check to a fresh-context
verifier. Prefer an equivalent project verifier; this plugin provides `intent-sdlc-skills-optional:sdlc-verifier`
as a default team example. Wait for its result before a final completion report; a pending review
is still pending. Do not run both for the same purpose. A routine prose correction or a
status/decision question does not require this independent implementation review. Do not repeat it for
every helper task or commit. A prior plan-handoff review does not replace this fresh completion review.
This completion check is a deliberate rule of this adopted team skill, not a requirement to use a
particular verifier tool in every project. A fresh context or different model does not guarantee
independent expectations or a correct verdict.

For implementation review, give the verifier the current task scope, latest human agreements/acceptances, applicable artifact
paths, the agreed diff base, and checks already run with their evidence. Also include the declared
spec document set and the current PR, integration or whole-release scope.
Include the current plan summary, the related adopted index row and existing execution evidence in that same
review's scope. Check their agreement with the actual work even when code and tests pass; do not narrow an
implementation-completion claim to code behavior alone. Do not demand an index the project has not adopted.
Provide the expectation sources and relevant browser/manual procedures, observations and tool limitations.
The verifier should understand those expectations before inspecting implementation and test diffs.
This review still reads implementation; it is not an implementation-hidden test-generation experiment.
Distinguish the tested combined/merged revision from planned checks or a previous branch result.
The default team verifier receives the common criteria in its own definition; confirm or supply
equivalent criteria when using a project verifier. Include uncommitted and untracked work. Do not ask it to trust your
completion claim. It should read the current files and return findings, not edit or approve.

Choose model and effort for difficulty, impact and uncertainty within the user's limits. The default
team verifier uses Opus/high for consequential cross-artifact judgments; ordinary implementation
can use Sonnet. If that capability is unavailable, use an appropriate available verifier or hand off
with the limitation. A stronger model is not proof of correctness.

Address concrete findings in the developer session, update affected artifacts and recheck changed
evidence before completion. When a finding requires a behavior-changing fix, follow the selected strategy and reassess its coverage.
For a TDD slice, return to [tdd](../tdd/SKILL.md) and observe the automated reproduction test's expected failure
before changing production code. For another strategy, diagnose the symptom first where practical, then
retain meaningful independent behavior and regression proof in the planned order. A manual or temporary
reproduction is not a permanent regression test or automated RED. Non-use of TDD alone is not a finding;
missing acceptance coverage or implementation-derived expectations remain findings under every strategy.
Reuse a relevant review only while its scope and evidence are unchanged.
A design PASS does not replace the fresh implementation-completion review.
If progress stalls or a human decision is needed, report the unresolved point instead of looping.
If independent execution was unavailable, say so rather than calling self-review independent.

At PR review, apply the same criteria to the submitted diff and current artifacts. Existing PR
tools/skills own comment collection, checks and pushes; this skill does not add a second PR loop.
Report the observed result, meaningful remaining issues, and relevant artifact/commit references.
Keep the PR description aligned with the final diff and latest tested revision after review changes.
Use the project's commit/PR format and development-case index when present; update the affected summary
at a meaningful delivery or handoff without copying full execution logs. Historical change specs are
revision-bound evidence: reconcile preserved contracts with current code, policy and authoritative design
before using them for a new change. Code alone does not authorize changing an agreed contract.
