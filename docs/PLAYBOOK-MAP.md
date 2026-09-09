# Playbook map — 14 lessons, this repo's device for each, and which layer it lives in

Layer vocabulary (docs/BOUNDARY.md): **person** · **tool** (git, GitHub, plan mode) · **skill**
(advisory text the agent reads) · **code** (hook, script or CI check). Line numbers are the
playbook's. Files owned by other lanes are named as found on `origin/main`
(3de08318) or as the three-lane contract names them (`evals/`, `tests/test_hooks.sh`); the parent confirms them at integration.

| # | Lesson (lines) | Device in this repo | File | Layer |
|---|---|---|---|---|
| 1 | Introduction | The chain itself: each stage writes a file the next reads | `intent/<NNNN>-<slug>/` | tool (git) |
| 2 | Capture as intent.md (167–239) | Template embedded in a skill; approval = merge | `.claude/skills/capture-intent/`, `templates/intent.md` | skill · person |
| 3 | Requirements and design (241–294) | Skill that refuses an unaccepted intent, restates constraints, answers or carries questions, flags concerns; `/spec` command with the lesson's prompt | `.claude/skills/design-spec/`, `.claude/commands/spec.md`, `templates/spec.md` | skill · person |
| 4 | Plan mode (296–388) | Skill for the four-section plan; plan mode itself records acceptance. A plan-sync hook is optional (329 "Consider using a hook") — this repo does not have one | `.claude/skills/plan/`, `templates/plan.md` | skill · tool |
| 5 | CLAUDE.md (390–448) | Four sections + verification block, under a page | `CLAUDE.md` | skill |
| 6 | Skills as institutional knowledge (450–509) | The playbook's `secure-api-review` example, verbatim; advisory, no backstop | `.claude/skills/secure-api-review/` | skill |
| 7 | Hooks as guardrails (511–529) | Hooks the lesson names, wired in settings.json | `.claude/hooks/`, `.claude/settings.json` | code |
| 8 | Parallel sessions and subagents (531–594) | Verifier subagent (report, do not fix) | `.claude/agents/verifier.md` | skill |
| 9 | Feedback loop (596–660) | `make check` with healthy output in CLAUDE.md; test-protection hook (631) | `Makefile`, `CLAUDE.md`, `.claude/hooks/protect-tests.sh` | code · skill |
| 10 | Evals in CI (662–740) | `make evals` with the key, in its own workflow on config change and schedule (689); the key-free half runs in `make test` | `evals/`, `.github/workflows/agent-evals.yml`, `tests/test_evals.sh` | code |
| 11 | PR review (742–801) | REVIEW.md with three passes; findings inform, the merge decides | `REVIEW.md` | skill · person |
| 12 | Hooks as approval gate (803–940) | Production gate hook | `.claude/hooks/production-gate.sh` | code |
| 13 | CI/CD (942–1005) | CI runs `make check`; a red check is a red PR | `.github/workflows/` | code |
| 14 | Bands (1007–1070) | Band config as the record; detection script only where the lesson names it | `ops/bands.yaml`, `scripts/` | code · person |

Not in this repo, by decision (docs/BOUNDARY.md): a checker for artifact form, status or
transitions; a metrics script (docs/METRICS.md is git commands); managed settings and the managed
code-review service (need an organization account).
