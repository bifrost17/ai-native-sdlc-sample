---
name: design-spec
description: Create or revise a combined requirements and design spec from the accepted intent and real product context. Produce concrete contracts, acceptance criteria and linked design documents that people and agents can implement from; leave execution planning and approval to their own stages.
disable-model-invocation: true
---
# Design spec

팀이 선택하여 읽거나 설치·수정할 수 있는 자체 작성 예시다. 이 위치에서는 자동 로드되지 않는다.

North star L3 245: "requirements and design spec"; L3 270: open questions must be answered or carried forward.
Human acceptance starts planning (L3 276). These source principles remain separate from the team's concrete form.

Confirm the actual intent revision and recorded human acceptance, or the already-authorized draft scope.
Keep Upstream with the actual input revision and Status draft. An old accepted version does not approve new edits.
Do not ask twice when authorization already covers this work; do not invent acceptance.
Preserve the originating prompt, applied skill versions, and any required draft authorization (who, scope, reason)
with the versioned spec/PR record (L3 279); a final summary alone does not preserve the original request.

Read the changed code, neighboring flows, interfaces and tests. Find applicable installed team skills, read their
bodies, and apply their decisions to the artifact. A source folder is not proof of installation. Record actual
skill source/version (or Git revision + dirty hash/limitation), not just a list of names. Use the team's policy review
method when available. In this team's default set, that is spec-policy-pass when actually available; its material
findings belong in the spec. It reviews policy decisions without overriding document structure. Use the existing [provenance reference](references/skill-provenance.md) for tracked,
cached or directory-loaded versions. Do not invent policy values or require a particular external skill.

Use [the project's spec form](../../../templates/spec.md);
[conditional design blocks](references/design-depth.md) provide fillable contracts and diagrams.
Use [traceability rules](../../../docs/sdlc-authoring/traceability.md) for stable FR/NFR, SP and existing IDs.
Write in the originator's language and retain the six English section names and their information roles.
Small changes can fit one file; spec.md is the entrypoint, not a one-file limit.
List each authoritative design document, what decision it owns and what must be read. Keep one source per decision.
A split document is part of the same spec scope/revision/review; an external moving reference needs an identified
revision or snapshot. Do not put architecture/classes/contracts in plan merely to shorten spec.md.

- Requirements: assign FR/NFR in new specs; retain existing R/AC IDs. Derive changed and preserved contracts from
  intent passages, answers, policy and current contracts; keep intent prose and do not backfill every requirement into it.
- Acceptance criteria: representative input, action, observable outcome and important failure/neighbor invariants.
  Map AC/requirements many-to-many as useful. Do not invent metrics or copy a vague requirement as its own proof.
- Design: connect the current problem and constraints to the chosen structure, a representative flow and exact
  contracts. Give each material design contract/decision or component responsibility a stable SP, defined once at its
  authoritative path and linked there to the requirements it serves. Explain meaningful alternatives and accepted
  operating/maintenance costs; do not invent numerical goals.
  Use prose for causal explanation and tables for comparable fields/contracts. A small change may combine these in
  one paragraph/table. Distinguish confirmed context, proposed decisions and illustrative internals.
- Constraints and scope: all upstream limits, discovered restrictions with evidence, explicit exclusions.
- Open questions: account for every input Q as answered with basis or carried forward with impact/owner/needed time.
  A question that can invalidate this design must be resolved before dependent handoff, not merely assigned.
- Flagged concerns: material conflicts/decisions with evidence, effect and responsible role; if none, state examined scope.

Choose a worked example by need: [small F01](../../../docs/sdlc-authoring/examples/F01/spec.md), [defect B01](../../../docs/sdlc-authoring/examples/B01/spec.md),
[staged release F03](../../../docs/sdlc-authoring/examples/F03/spec.md), [multi-document M01](../../../docs/sdlc-authoring/examples/M01/spec.md),
[web/API W01](../../../docs/sdlc-authoring/examples/W01/spec.md).
Read its input too; example facts are not universal policy. No mandatory class/diagram or private-method catalogue.
Explain names and ownership when they matter to the flow; label current/target/transitional states in a shared diagram.
Link required current contracts directly. History is supporting evidence, not an implicit detour needed for implementation.
Keep provenance/authorization findable in the existing record without overwhelming the product explanation.

Before handing the spec to planning or reporting the design ready, apply [the project's review criteria](../../../REVIEW.md)
to the complete declared design set. Use [design-depth](references/design-depth.md) for shared-contract or recovery questions.
Confirm needed references are accessible; source names or prior PASS counts do not establish that their contents were reviewed.
For important shared boundaries or independent lifetimes, prefer a capable fresh-context reviewer. Keep small changes proportionate.
Report the contracts/branches actually checked, resolved findings and justified deferrals; design readiness is not runtime proof or acceptance.

Review with the owner: "Does the spec solve the stated problem, and are the open questions from intent.md answered
or carried forward?" Show linked design documents with it. Model review does not grant owner acceptance.
When decisions change, update the actual affected requirements/AC/design documents, not only a discussion appendix.
Align affected plan and reason in the related implementation commit; revisit intent when purpose/constraints change.
Record required revised decisions and then repin downstream to a resolvable upstream commit. Leave unrelated documents alone.
