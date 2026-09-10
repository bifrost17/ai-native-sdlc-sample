---
name: sdlc-feedback
description: Keep agreed requirements, spec, plan and implementation aligned during software work. Use when implementing a planned change, incorporating new requirements or design/review feedback, departing from a plan, receiving an updated artifact acceptance, preparing related changes for commit, reporting implementation complete, or reviewing a branch/PR against its spec and plan. Questions and status-only requests do not call for completion review.
---
# SDLC feedback

Work in the developer's conversation so that the human's decisions remain available. Read
[review-criteria.md](references/review-criteria.md) when comparing agreements, artifacts and evidence.
Use the part below that fits the current event; this is not an extra phase for every response.

## Change or acceptance

Read the applicable project instructions and current intent/spec/plan. Update the artifacts whose
meaning changed: requirements/design/acceptance criteria in spec, implementation/verification/PR
boundaries in plan, and intent only if the problem or constraints changed. A conversation or README
does not substitute for the affected artifact. Existing planning and policy skills retain their roles.

Use human decisions already supplied. If the accepted upstream version changed, update downstream
references under the project's policy. Ask only for material decisions still missing; do not turn
an already clear answer into another approval request. Leave unaffected documents alone.

## Implementation and commit

Run the relevant feedback loop as work proceeds. When implementation departs from plan, include
the changed plan and reason in the same commit as that implementation. Before committing, inspect
what will actually be included, including new files. Follow the project's upstream acceptance and
Git policy; permission to inspect or review does not itself authorize a commit, push or merge.

## Completion and review

Before reporting an implementation task complete, delegate a final check to a fresh-context
verifier. Prefer an equivalent project verifier; this plugin provides `intent-sdlc-skills:sdlc-verifier`
as a default team example. Wait for its result before a final completion report; a pending review
is still pending. Do not run both for the same purpose. A routine prose correction or a
status/decision question does not require this independent implementation review.

Give the verifier the current task scope, latest human agreements/acceptances, applicable artifact
paths, the agreed diff base, checks already run with their evidence, and the absolute path of the
review criteria read above. Include uncommitted and untracked work. Do not ask it to trust your
completion claim. It should read the current files and return findings, not edit or approve.

Choose model and effort for difficulty, impact and uncertainty within the user's limits. The default
team verifier uses Opus/high for consequential cross-artifact judgments; ordinary implementation
can use Sonnet. If that capability is unavailable, use an appropriate available verifier or hand off
with the limitation. A stronger model is not proof of correctness.

Address concrete findings in the developer session, update affected artifacts and recheck changed
evidence before completion. Reuse a relevant review only while its scope and evidence are unchanged.
If progress stalls or a human decision is needed, report the unresolved point instead of looping.
If independent execution was unavailable, say so rather than calling self-review independent.

At PR review, apply the same criteria to the submitted diff and current artifacts. Existing PR
tools/skills own comment collection, checks and pushes; this skill does not add a second PR loop.
Report the observed result, meaningful remaining issues, and relevant artifact/commit references.
