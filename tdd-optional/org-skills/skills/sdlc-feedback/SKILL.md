---
name: sdlc-feedback
description: Keep agreed requirements, spec, plan and implementation aligned. Use when preparing a spec handoff, reviewing or revising important design contracts, implementing or departing from a plan, incorporating requirement or acceptance changes, updating plans after test/review evidence, preparing related commits, reporting implementation complete, or reviewing a branch/PR. Questions and status-only requests do not call for completion review.
---
# SDLC feedback

Work in the developer's conversation so that the human's decisions remain available. Read
the **Review criteria** section of [sdlc-verifier.md](../../agents/sdlc-verifier.md) when comparing
agreements, artifacts and evidence. Its reviewer-only permissions apply to the verifier, not to
your developer session.
Use the part below that fits the current event; this is not an extra phase for every response.

## Spec handoff and design review

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

Summarize the important contracts/branches examined, findings and their resolution, justified deferrals
and remaining limits in the existing review/handoff record. Do not total PASS votes as proof of readiness.
Distinguish design sufficiency, executed verification and human acceptance; reuse supplied authorization.

## Change or acceptance

Read the applicable project instructions and current intent/spec and any applicable plan, including the
complete design document set declared by spec. Check the current intent constraints against the changed behavior even
when the problem and goal are unchanged. Apply the common Review criteria to update the artifacts whose
meaning changed: requirements/design/acceptance criteria in their spec documents, implementation/verification/PR
boundaries in plan, and intent only if the problem or constraints changed. A conversation or README
does not substitute for the affected artifact. Existing planning and policy skills retain their roles.
For implementation planning, record the chosen verification strategy (TDD, behavior-by-behavior implementation then tests, existing-test
reuse or a mix), its reason and coverage in plan. Selection does not create an exception or approval gate.
Make affected spec/design documents and the plan current before starting the changed behavior's implementation
and verification cycle; if a discovery changes them during implementation, update them before the next dependent change.

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

## Implementation and commit

Run the chosen feedback loop as work proceeds: use tests, permitted browser interaction or direct observation
suited to the behavior, with independent expectations, actual results and relevant regression evidence.
For exploration, record the learning question, constraints, observations and unresolved decisions. Answering
that question is not product completion; adopting the result requires current spec/AC, regression and integration
proof. A screenshot alone does not establish interactive behavior. Include affected spec documents and plan changes, with the reason,
in the same commit as the related implementation. Before committing, inspect
what will actually be included, including new files. Follow the project's upstream acceptance and
Git policy; permission to inspect or review does not itself authorize a commit, push or merge.

## Completion and review

Before reporting an implementation task complete, delegate a final check to a fresh-context
verifier. Prefer an equivalent project verifier; this plugin provides `intent-sdlc-skills-optional:sdlc-verifier`
as a default team example. Wait for its result before a final completion report; a pending review
is still pending. Do not run both for the same purpose. A routine prose correction or a
status/decision question does not require this independent implementation review.
This completion check is a deliberate rule of this adopted team skill, not a requirement to use a
particular verifier tool in every project. A fresh context or different model does not guarantee
independent expectations or a correct verdict.

For implementation review, give the verifier the current task scope, latest human agreements/acceptances, applicable artifact
paths, the agreed diff base, and checks already run with their evidence. Also include the declared
spec document set and the current PR, integration or whole-release scope.
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
