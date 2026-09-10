# Intent: the policy texts are one imagined product's, not the team's
Author: the user (product owner), via the parent session. Status: draft.
First conversation: 2026-09-10 (stated by the author).
## Problem
- `policies/*.md` v0 was drafted around the playbook's worked example (an insurance claims-status
  service). Seven of the fifteen skills under `org-skills/skills/` cite those clauses and mention
  that domain 7 to 15 times each. The author's goal is a **team-general SDLC template**: each
  project's own specialization is that project's lead's work, not this repository's.
- Because the clauses mix two levels — what holds for any project the team runs, and what one
  product decided — a project adopting the set today inherits an invented status vocabulary, an
  invented upstream budget and invented role names.
## Proposed outcome
`policies/*.md` carries only clauses that hold for any software project, each project fills a
`PROJECT-POLICY.md` from a template for the values that are its own, and the claims-status
skills move out of the loading set into `org-skills/examples/` as one project's filled-in
example. The policy content itself stays light — the owner writes the real thing separately.
## Affected users and systems
Adopters (they now receive a team-general set plus one worked example); the seven domain-bound
skills; `spec-policy-pass`, whose examples cite moved clauses; `docs/ADOPTING.md`.
## Constraints
- Light: structure and generic basics only. No invented organization-specific values.
- Nothing is lost: the claims-status skills and all research under `docs/research/` stay.
- Adopted marketplace skills are untouched (they are domain-neutral already).
- Process policy (verification, review, delivery, documentation) is out of scope here — the
  author works on it separately.
## Open questions
- Which team documents are the real source of truth for each policy area — the owner answers when
  writing the real clauses.
