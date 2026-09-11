---
name: design-spec
description: Turns an accepted intent into a combined requirements and design spec, or revises that spec when facts and decisions change. Uses the organization's applicable skills, preserves constraints and questions, and makes behavior, design choices, acceptance criteria and material concerns reviewable by people and agents. Leaves implementation planning and approval to their own stages.
---
# Design spec

> L3 245: "Once the product owner approves the intent.md, Claude takes it and produces a
> requirements and design spec. This is guided by the organization's skills for brand, security,
> compliance, and UX."
> L3 270: "Does the spec solve the stated problem, and are the open questions from intent.md
> answered or carried forward?"
> L3 276: "A human teammate always makes this call, and accepting the spec is what starts the
> plan mode play"

## Before writing
1. Open the intended chain's `intent.md` and identify the accepted revision from the project's
   actual acceptance record. `Status: draft` is not an approval test: merge records approval.
   An older revision on main does not approve newer branch or working-tree changes. Use an
   acceptance already supplied; ask only when the required acceptance is missing or unclear.
   An engineer may authorize work on a draft, including stacked work. In that case record who
   authorized which scope and why directly below the Upstream/Status line and in the PR body.
   This permission is not a fabricated merge. Otherwise wait for acceptance before authoring the spec.
2. Read the relevant existing code, interfaces, tests and design references. Understand the changed
   path and its important neighbors; do not reverse-specify the whole product. Distinguish observed
   facts from assumptions. If essential context is unavailable, expose the gap and its effect.
3. Find the applicable team skills in the project's local skills and the session's loaded plugin
   catalog. A source directory is not proof of installation. Open each applicable skill's actual
   body before applying it; record selection and meaningful exclusions with reasons. If this team's
   `spec-policy-pass` procedure is available, read and apply it alongside this authoring skill.
   Keep its findings in the relevant requirements/design/concerns, not only a list of names.
   Record the source and verified version under `Skills applied`; use `none` or an explicit
   limitation when appropriate. For Git, cache or uncommitted versions, use
   [the provenance reference](references/skill-provenance.md). Do not invent versions or policy values.
4. Keep line 2 as `Upstream: intent.md@<actual-revision>. Status: draft.` and leave it draft.
   The upstream identifies what you used; a draft exception does not turn it into accepted input.
   Keep the originating prompt and applied skill versions with the versioned spec/PR record (L3 279).

## Writing
Use `templates/spec.md` in the chain beside intent.md. Write in the originator's language and
retain the six English section names. Brief prose, bullets and tables are all valid. Start with
the important change and choice; put a concern needing human decision up front when one exists.

- **Requirements**: name the changed behavior and important preserved contracts with R identifiers.
  Ground them in the intent, confirmed constraints or applicable policy, not only the Problem
  paragraph. Clarify the outcome beneath a proposed solution before turning it into a design choice.
  User-visible behavior, system invariants and supported quality requirements can all be verifiable.
- **Acceptance criteria**: link AC identifiers to the R identifiers they cover. Use representative
  conditions, actions and expected results, including material failure and neighboring behavior.
  One criterion may cover several requirements and a requirement may need several cases. Avoid
  merely repeating every R as an AC or inventing numerical success targets. Manual observation
  can be appropriate; concrete test files, commands and task order belong in plan.md.
- **Design**: explain the selected approach, existing assets reused, important interfaces and flow,
  and why significant choices fit this change. Include a credible alternative or accepted drawback
  when it clarifies a real decision. No fixed number of alternatives. Separate binding contracts
  from illustrative names/code; leave incidental implementation choices to planning and implementation.
  Add detail when changing it could change acceptance or implementation direction. For API/UI,
  migration, staged exposure, performance or shared boundaries, consult [conditional depth](references/design-depth.md)
  when relevant; do not add every heading from it to every spec.
- **Constraints and scope**: preserve every upstream limit and explicit exclusion. State discovered
  constraints with their basis. Refer to an already clear R/design clause instead of duplicating its
  text. Current environment facts and unconfirmed preferences are not automatically new prohibitions.
- **Open questions**: account for every intent question, retaining supplied identifiers, and add new
  material questions found during design. `answered:` needs an actual answer and its basis; an agent's
  unconfirmed assumption is not a human answer. `carried forward:` says what is unknown, its impact
  and who can answer, or that the owner is unassigned. Explain why it can wait and when it is needed.
- **Flagged concerns**: expose policy conflicts and material issues needing human decision, with
  evidence, consequence and the responsible person/role when known. Do not invent an owner or
  resolve a policy conflict yourself. An addressed technical risk can stay in Design/AC; it need
  not become a new approval gate. No important concern is a valid result with the scope examined.

If an unanswered question could invalidate the selected design, or a policy conflict remains,
bring it to the product owner and relevant owner before handing it to planning. A name under
`carried forward` is not resolution. A draft can expose incomplete decisions honestly without
claiming readiness. Use decisions already given and reflect them; do not ask for approval twice.

When useful, read one complete synthetic example: [small feature](examples/feature/spec.md),
[precise bug fix](examples/bug/spec.md), or [migration with a discovered consumer](examples/migration/spec.md).
Each has its input and context beside it. Their facts, constraints and choices are not project defaults.

## Review question
Show the spec beside the intent and ask the product owner the lesson's question, verbatim:
"Does the spec solve the stated problem, and are the open questions from intent.md answered or
carried forward?"

The product owner decides whether to proceed, resolving flagged concerns with the relevant owner
and involving a tech lead where the organization considers the change high risk. A model review
does not grant this acceptance.

## When the design changes
Put material answers and revised behavior/choices into the affected requirements, design,
constraints and acceptance criteria; update the question or concern too. A discussion appendix
alone does not change the contract. Preserve the reason in the relevant text and Git history.
Align an existing plan when its execution/verification changes, and revisit intent if its purpose
or constraints changed. Use the project's feedback procedure; update affected upstream references
to the supplied accepted revision. Leave unaffected documents alone. Do not build a new state ledger.

## What this skill does not do
- Does not proceed without accepted intent or the explicitly recorded draft authorization above.
- Does not create plan.md — initial planning follows the product owner's acceptance of the spec.
  Changes to an existing plan follow the project's feedback procedure.
- Does not set the spec to accepted. The product owner signs off; the merge records it.
