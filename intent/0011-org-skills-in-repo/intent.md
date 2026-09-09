# Intent: the organization's skill set lives in a second repository, away from the template it serves
Author: the user (product owner), via the parent session. Status: draft.
First conversation: 2026-09-10 (stated by the author).
## Problem
- On 2026-09-09 the organization's skill set (policy skills, adopted marketplace skills, the
  research behind each choice, the policy texts) was started in a separate repository,
  `bifrost17/intent-sdlc-skills`, on the reading that the template must not carry organization
  policy. The author's intent is different: this repository is the organization's, and its skill
  set belongs here, in its own folder, with the research documented under `docs/`.
- Four of eight skill lanes are merged there (S8 plugin skeleton, S1 intent-template,
  S5 secure-api-review, S7 pr-loop); four are still running or queued (S2 brand, S3 compliance,
  S4 ux, S6 spec-command). Nothing here points at that work.
## Proposed outcome
This repository holds the organization's skill set as a plugin under `org-skills/`
(`.claude-plugin/plugin.json`, `skills/<name>/`, `commands/`), the policy texts under `policies/`,
the research and decisions under `docs/research/` and `docs/decisions/`, and the lane briefs under
`docs/work/`. The root `.claude-plugin/marketplace.json` serves `./org-skills`. The template's own
skills stay in `.claude/skills/`. Later lane results are copied in the same way; the second
repository is archived once the last lane lands.
## Affected users and systems
Adopters cloning `main` (they now receive one organization's worked example of the team's part);
the running lanes (unaffected — they keep working in the second repository until they finish);
CI (`make check` must stay green); CODEOWNERS (policy owner signs off on `policies/**` and
`org-skills/**`, L6 460).
## Constraints
- Copy, do not move history: the second repository keeps the lane history and is referenced from
  the decision record; this repository gets the files.
- The playbook example skill `secure-api-review` under `.claude/skills/` stays verbatim; its copy
  under `org-skills/skills/` is the organization's set and is byte-identical today.
- No template behaviour changes: hooks, tests, evals untouched.
## Open questions
- Whether the plugin keeps the name `intent-sdlc-skills` (the slash prefix the lanes tested) or
  takes the folder name — the author decides; S8's open question 3.
