# Plan: keep only what the lessons name as code (from intent.md 2026-09-09)
Upstream: spec.md@26633a6ee344c3fd80596a6b987ef2c0a4617619. Status: draft.
## Files that change
Lane B (this branch): .claude/skills/capture-intent/SKILL.md, .claude/skills/design-spec/SKILL.md
(new), .claude/skills/plan/SKILL.md (new), .claude/skills/secure-api-review/SKILL.md,
.claude/commands/spec.md, .claude/agents/verifier.md, CLAUDE.md, README.md, REVIEW.md (new),
NOTICE, templates/{intent,spec,plan}.md, docs/PLAYBOOK-MAP.md (new), docs/BOUNDARY.md (new),
docs/METRICS.md (new), tests/test_skill_template.py (new), intent/0001-bootstrap-repo/* (copied),
intent/0004-lesson-only/* (new).
Removed: docs/DESIGN.md, docs/STATUS.md, docs/SOURCE-OF-TRUTH.md, scripts/metrics.py,
tests/test_metrics.py, tests/fixtures-metrics/, templates/intent-{defect,incident}.md.
Lane A: .claude/hooks/, .claude/settings.json, Makefile, scripts/, tests/ (rest), evals/.
Lane C: .github/workflows/.
## Order of work
1. Write tests/test_skill_template.py; run it — red (no fence in the skill yet).
2. Write the three templates and the four skills; run it — green.
3. Write docs, agent, CLAUDE.md, README.md, REVIEW.md, NOTICE; delete the listed files.
4. Copy chain 0001 byte for byte; write this chain (intent → spec → plan, one commit each).
5. Parent integrates A, B, C; fills the healthy-output lines in CLAUDE.md; runs make check.
## Risks
- The verbatim secure-api-review skill cites a script that does not exist (spec F1). Noticed by
  anyone who runs the skill; decided at merge.
- Lane A renames a test this plan names under Proof; the parent aligns names at integration.
- Line budget is only provable after all three lanes merge (spec AC5).
## Proof
- AC1 ← tests/test_skill_template.py::SkillTemplateMatchesCopy::test_skill_embeds_template_verbatim
  (green), plus one mutation of templates/intent.md → red, restored (raw 06).
- AC2 ← grep -c "What this skill does not do" .claude/skills/*/SKILL.md = 1 for each of the three.
- AC3, AC5 ← run by the parent after integration (make check; git ls-files | xargs wc -l).
- Hook behaviour ← tests/test_hooks.sh cases as lane A names them; the parent maps names here at
  integration.
