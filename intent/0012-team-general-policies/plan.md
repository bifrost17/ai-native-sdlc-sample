# Plan: split team clauses from project values (from intent.md 2026-09-10)
Upstream: spec.md@a861f7069f87ef0618de136e2ce18fc63582b3f7. Status: draft.
## Files that change
- `intent/0012-team-general-policies/{intent,spec,plan}.md` (new).
- `policies/{brand,compliance,ux,api-security}.md` — rewritten short. `policies/README.md` · `policies/PROJECT-POLICY.template.md` (new).
- `org-skills/skills/brand/SKILL.md` · `org-skills/skills/spec-policy-pass/SKILL.md` — citations.
- `org-skills/skills/claim-data-compliance/` → `org-skills/skills/data-compliance/` (generalized).
- `org-skills/skills/{claim-notice-compliance,claims-api-security,claims-ux-copy,claims-ux-interaction}/` → `org-skills/examples/claims-status/`; `org-skills/examples/README.md` (new).
- `docs/ADOPTING.md` — one row pointing at PROJECT-POLICY.
## Order of work
1. This chain, three commits.
2. Policy files + template + README.
3. Skill moves and citation edits.
4. `claude plugin validate org-skills` · `make check` · AC1-AC3 greps.
5. PR; check green; merge.
## Risks
Riskiest is step 3: a moved skill leaving a dangling citation, or the plugin still loading an example. Step 4's greps and `claude plugin details` catch both.
## Proof
`claude plugin validate org-skills`, `make check`, and the three AC greps in the PR body.
