# Spec: organization skill set in this repository — `org-skills/` + `policies/` + `docs/research/`
Upstream: intent.md@b2a8a3352385957c803fced1bdc51109a4f4e9db. Status: draft.
Skills applied: none — no external-facing endpoint; `design-spec` read.
## Requirements
- R1 `org-skills/` is a Claude Code plugin root: `org-skills/.claude-plugin/plugin.json`, `org-skills/skills/<name>/{SKILL.md,PROVENANCE.md}`, `org-skills/commands/`. Root `.claude-plugin/marketplace.json` lists it with `source: "./org-skills"`.
- R2 `policies/{brand,compliance,ux,api-security}.md` are the source of truth (v0, owner sign-off = merge).
- R3 `docs/research/<skill>/` (README · candidates · coverage · trigger-tests · raw), `docs/research/00-method.md`, `docs/research/README.md`, `docs/decisions/`, `docs/work/` (briefs, baselines, NOTES) come over as they are.
- R4 CODEOWNERS adds `policies/**` and `org-skills/**` (L6 460 "have the policy owner sign off on the change").
- R5 README gains an "Organization skill set" section; ADOPTING points at `org-skills/` as the worked example of the team's part.
- R6 `claude plugin validate` passes for the marketplace and the plugin; `make check` stays green.
## Design
One PR: this chain (three commits) + one copy commit. Files are copied from `bifrost17/intent-sdlc-skills@43d8818` (main after S8·S1·S5·S7). Later lanes (S2·S3·S4·S6) are copied the same way, one PR each, when they merge there. The second repository is archived afterwards with a pointer here.
## Constraints
Carried from intent.md: copy not move · `.claude/skills/secure-api-review` verbatim · no behaviour change.
## Open questions from intent
- Plugin name (`intent-sdlc-skills` vs folder name) — carried forward to the author; the copy keeps `intent-sdlc-skills` so the lanes' trigger evidence (`/intent-sdlc-skills:…`) stays true.
## Flagged concerns
- `docs/research/` is 6.9 MB of raw evidence; S8 measured that a plugin install copies its plugin root only, and `org-skills/` holds none of it — the raw stays out of the plugin cache.
## Out of scope
Archiving the second repository (after the last lane) · renaming the plugin · wiring `org-skills` into `.claude/settings.json` `enabledPlugins` (the experiment decides how the template consumes it).
## Acceptance criteria
- AC1 `claude plugin validate .` and `claude plugin validate org-skills` pass on `main`.
- AC2 `make check` exits 0.
- AC3 `diff -r` between `org-skills/skills` and the second repository's `skills/` at `43d8818` is empty; same for `policies/`, `docs/research/`, `docs/decisions/`.
- AC4 CODEOWNERS contains `policies/**` and `org-skills/**`.
