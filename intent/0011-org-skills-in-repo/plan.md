# Plan: bring the organization's skill set into this repository (from intent.md 2026-09-10)
Upstream: spec.md@b31e0fce4a188bb23f314c35a0e2666bea134f0c. Status: draft.
## Files that change
- `intent/0011-org-skills-in-repo/{intent,spec,plan}.md` (new).
- `org-skills/.claude-plugin/plugin.json` (new, from the second repo, `repository` URL updated) · `org-skills/skills/*` (new, 6 skills) · `.claude-plugin/marketplace.json` (new, root, `source: ./org-skills`).
- `policies/*.md` (new, 4) · `docs/research/**` (new, 403 files) · `docs/decisions/*.md` (new, 4) · `docs/work/**` (new, briefs + baselines + README note).
- `README.md` (section) · `docs/ADOPTING.md` (one paragraph) · `.github/CODEOWNERS` (two lines).
## Order of work
1. This chain, three commits.
2. Copy from `intent-sdlc-skills@43d8818`; write plugin.json/marketplace.json; validate both.
3. README · ADOPTING · CODEOWNERS; `make check`.
4. PR; `check` green; merge. Then `diff -r` against the second repo (AC3).
## Risks
Riskiest is step 2: `claude plugin validate` rejecting a nested plugin root, or `tests/test_skill_template.py` scanning a folder it did not expect. Both are caught by the two commands in step 2–3 before the PR opens.
## Proof
`claude plugin validate .` · `claude plugin validate org-skills` · `make check` outputs in the PR body; `diff -r` empty for the four copied trees.
