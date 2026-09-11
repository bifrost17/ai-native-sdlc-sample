---
name: design-spec
description: Create or revise a combined requirements and design spec from the accepted intent and real product context. Produce concrete contracts, acceptance criteria and linked design documents that people and agents can implement from; leave execution planning and approval to their own stages.
---
# Design spec

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
findings belong in the spec. Use the existing [provenance reference](references/skill-provenance.md) for tracked,
cached or directory-loaded versions. Do not invent policy values or require a particular external skill.

Use the project's templates/spec.md. This candidate's review copy is [the form](../../templates/spec.md);
[conditional design blocks](../../guidance/design-blocks.md) provide fillable contracts and diagrams.
Write in the originator's language and retain the six English section names and their information roles.
Small changes can fit one file; spec.md is the entrypoint, not a one-file limit.
List each authoritative design document, what decision it owns and what must be read. Keep one source per decision.
A split document is part of the same spec scope/revision/review; an external moving reference needs an identified
revision or snapshot. Do not put architecture/classes/contracts in plan merely to shorten spec.md.

- Requirements: changed and preserved contracts with their intent/answer/policy basis.
- Acceptance criteria: representative input, action, observable outcome and important failure/neighbor invariants.
  Map AC/R many-to-many as useful. Do not invent metrics or copy a vague R sentence as its own proof.
- Design: actual structure, important interfaces/data/errors/flows and meaningful choice/reason/tradeoff.
  Use conditional blocks only where a decision matters; distinguish binding contracts from illustrative internals.
- Constraints and scope: all upstream limits, discovered restrictions with evidence, explicit exclusions.
- Open questions: account for every input Q as answered with basis or carried forward with impact/owner/needed time.
  A question that can invalidate this design must be resolved before dependent handoff, not merely assigned.
- Flagged concerns: material conflicts/decisions with evidence, effect and responsible role; if none, state examined scope.

Choose a worked example by need: [small F01](../../examples/F01/spec.md), [defect B01](../../examples/B01/spec.md),
[staged release F03](../../examples/F03/spec.md), [multi-document M01](../../examples/M01/spec.md).
Read its input too; example facts are not universal policy. No mandatory class/diagram or private-method catalogue.

Review with the owner: "Does the spec solve the stated problem, and are the open questions from intent.md answered
or carried forward?" Show linked design documents with it. Model review does not grant owner acceptance.
When decisions change, update the actual affected requirements/AC/design documents, not only a discussion appendix.
Align affected plan and reason in the related implementation commit; revisit intent when purpose/constraints change.
Record required revised decisions and then repin downstream to a resolvable upstream commit. Leave unrelated documents alone.
