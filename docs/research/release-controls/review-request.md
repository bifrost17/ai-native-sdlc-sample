Read-only independent design review. Maker candidate 88b367b (base65a509a) is the current directory;
adopter /Users/jake/Projects/ai-native-sdlc-use-0023 candidate f89a92a (base82d7ad2).
Review only the changed release-control policy, spec/plan conditional guidance, skill references and
review/adoption consumers. Start with intent/0023-release-controls/spec.md and this folder README.md,
then docs/RELEASE-CONTROL.md, docs/GIT-WORKFLOW.md, docs/PR-SIZE.md, templates/{spec,plan}.md,
.claude/skills/{design-spec,plan}/SKILL.md and respective design-depth/execution-depth references,
REVIEW.md, docs/ADOPTING.md. Check semantic adopter counterparts under examples/skills, PROJECT-POLICY.

User wants unfinished agreed feature units hidden from ordinary users while executable for testing,
small PRs to deployable main, one stable control reused through config rather than hiding-code edits per PR.
Independent complete approved features may ship. Keep internal-service policy thin and conditional:
no mandatory SDK/SaaS, no new semantic checker, flags do not replace auth/data recovery. Root authored;
you review. Source attribution must not claim Anthropic or GitHub Flow mandates release flags.
Preserve prior F02 history. Runtime is pending, do not claim its success. Report PASS or concrete
important findings with path and minimum correction. At most three optional nits. No file writes,
no other tools/agents/CLI/network/installs. The input files are sufficient for bounded review.
