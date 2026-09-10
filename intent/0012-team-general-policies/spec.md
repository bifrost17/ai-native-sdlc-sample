# Spec: team-general policy clauses + per-project slots
Upstream: intent.md@3a6e1c9a72dc35a84c69272e3f92022c7ed0794f. Status: draft.
Skills applied: none — no external-facing endpoint; `design-spec` read.
## Requirements
- R1 `policies/{brand,compliance,ux,api-security}.md` hold **team clauses only** — each one true for any software project the team runs. Clause IDs stay `B`/`C`/`U`/`S` + number.
- R2 Each policy file ends with a **project slots** list: what a project must decide, named, with no value filled in.
- R3 `policies/PROJECT-POLICY.template.md` is the file a project lead copies into their repository and fills; slot IDs are `P` + number and are what project-specific skill text cites.
- R4 `policies/README.md` states the two levels, the sign-off rule (merge = signature, CODEOWNERS `policies/**`) and the version bump rule for the plugin.
- R5 `org-skills/skills/` holds only skills that load for every project. The six claims-status skills move to `org-skills/examples/claims-status/` (a plugin does not load skills outside `skills/`), with a README naming them as one project's specialization.
- R6 The team set keeps one skill per policy area: `brand` (generalized), `data-compliance` (generalized from `claim-data-compliance`, covering C1-C5), `secure-api-review` + `secrets-scan` (already generic), `ux-copy` + `accessibility` (adopted, generic), plus `spec-policy-pass`, `pr-loop` and the three adopted intent-stage skills.
- R7 No clause, skill or example is deleted; `docs/research/` and `docs/decisions/` are untouched.
- R8 `claude plugin validate` and `make check` pass.
## Design
Rewrite the four policy files short (about 20 lines each: clauses, then slots). Generalize two skills by editing their bodies to cite team clauses and defer values to `PROJECT-POLICY.md`; `git mv` the rest into `examples/`. Patch `spec-policy-pass`'s example citations. One PR, this chain plus one restructure commit.
## Constraints
Carried from intent.md: light · nothing lost · adopted skills untouched · process policy out of scope.
## Open questions from intent
- Real source of truth per policy area — carried forward to the owner (`docs/decisions/OWNER-QUESTIONS.md`).
## Flagged concerns
- The generic clauses are the parent session's wording, not an owner's policy. They are a scaffold to be replaced, and `policies/README.md` says so.
## Out of scope
Process policy (verification/review/delivery/docs) · the 51 owner questions · the experiment.
## Acceptance criteria
- AC1 No file under `policies/` names a claim, an adjuster, an agent-proxy or a rate budget.
- AC2 `org-skills/skills/` contains no skill whose body cites a project value; `org-skills/examples/claims-status/` contains the six.
- AC3 Every `P`-slot cited by an example skill exists in `PROJECT-POLICY.template.md`.
- AC4 `claude plugin validate org-skills` and `make check` exit 0.
