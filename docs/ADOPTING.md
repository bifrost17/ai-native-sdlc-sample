# Adopting this template

This repo is one organization's answer to each lesson (`docs/PLAYBOOK-MAP.md`). Adopting it for
another organization means filling in the spots below, not copying the sample values. Each row is
a place the sample repo answered for itself; the "who" column names the playbook role who owns
that answer, not this session. `# TEAM:` / `<!-- TEAM: -->` comments mark the same spots in the
files themselves — `grep -rn 'TEAM:'` finds all of them.

| Spot (path) | What the sample gives | What the team puts in | Who (playbook role) | Playbook line |
|---|---|---|---|---|
| `.claude/commands/spec.md` + new `.claude/skills/<policy>/` | one policy skill, `secure-api-review` | a skill per policy that is enforced inconsistently today (brand, compliance, UX, …): named owner, documented source of truth → skill, a trigger test, owner sign-off | technical team member writes it from the policy owner's source of truth (L6 452) | L6 452-460, L3 253 |
| `.claude/skills/secure-api-review/SKILL.md` (head) | the playbook's worked example verbatim, minus the `check-endpoints.sh` line | the org's actual API standard, replacing the four checklist items; restore a script line only if one exists | engineer, from the security policy owner's standard | L6 466-484 |
| `.claude/skills/capture-intent/SKILL.md` (above the template) | a generic intent.md template (problem / outcome / users / constraints) | the org's own intent template, adjusted to what a lead needs to sign off on | technical team member writes it, a lead signs off | L2 197-202 |
| `CLAUDE.md` (head, Commands section) | this repo's `make test`/`make evals`/`make check` and their exact healthy output | the team's real build/test/lint commands and healthy output, plus its own conventions, architecture and "things Claude gets wrong" | engineer, cut from `/init` output to a day-one page | L5 397-401 |
| `.claude/hooks/protect-paths.sh` (above `PROTECTED`) | a static list: `.github/*`, `Makefile`, `.claude/hooks/*`, `.claude/settings.json` | the team's actual frozen/generated paths | platform engineer expresses the gate as a hook | L7 517, L12 791-801 |
| `.claude/hooks/no-secrets.sh` (above the patterns) | six generic credential regexes (AWS key, PEM, `sk-`, `gh*_`, URL creds, `password=`) | the org's own secret shapes (internal gateway tokens, etc.) | platform engineer | L7 521 |
| `.claude/hooks/format-lint.sh` (above the commands) | `py_compile` for `.py`, `bash -n` for `.sh` only | the team's real formatter/linter commands per file type | platform engineer | L7 519 |
| `.claude/hooks/production-gate.sh` (above the approval check) | one env var, `RELEASE_APPROVAL` | the org's actual written approval process this gate should check against | eng leadership + change management + compliance list the gates (L12 791 "a written list of the approvals") | L12 791-801, L12 838-895 |
| `org/README.md` (head) | one inactive managed-settings example, keyed to this repo's five hooks | the org's real managed-settings deployment (MDM/admin console) and its own hook names re-listed in the `hooks` block | platform or IT admin | L12 799, L12 838-895 |
| `.claude/settings.json` (`permissions.allow`) | this repo's own safe commands: `make test`/`check`/`evals`, `git status`/`diff`/`log` | the commands the organization considers safe, so parallel sessions are not waiting on approval prompts | platform engineer, with the security policy owner | L8 545 |
| `.claude/agents/verifier.md` | `make check` stands in for "start the app" (this repo has no app) | the team's actual `make run`/start command and its two nearest neighboring flows | engineer defines the subagent | L8 550-565 |
| `REVIEW.md` (above Passes) | three passes (bugs, security, compliance); no design-principles pass, no CODEOWNERS | a design-principles pass if the org wants one, and the real people in CODEOWNERS; `intent/**`'s PO account, and if more than one, a ruleset with `require_code_owner_review=true`; the paths the org classifies as high-risk, with a tech lead or architect as their owner (routine changes the engineer approves) | tech lead writes the review policy | L11 739-741, L4 351 |
| `evals/README.md` | 3 cases (the incident eval from chain 0006 is on the experiment branch); no `ANTHROPIC_API_KEY` secret set | 20-50 cases from the org's real recent tasks, and the API key secret in CI | platform engineer collects the tasks | L10 662, L10 666 |
| `ops/bands.yaml` (above `metric:`) | one metric (`ci_test_failure_rate`) with Western Electric rules 1-3 | the org's own metric and baseline (5xx rate, PR cycle time, …), wired to a real metrics store and trigger | service owner / platform engineer | L14 990, L14 994-1000 |
| `README.md` ("Source of truth" section, no marker — prose already answers it) | "this repo is the source of truth" | if the org has Jira/a requirements tool/a change board, pick repo / legacy-system / linkage-only per artifact instead | the org, per artifact | L4 367-377 |
| no file — deployment infrastructure, no marker | nothing (`docs/BOUNDARY.md` names this as a device the sample does not build) | MCP deploy/status/rollback tools, sandboxed job containers, a rehearsed staging rollback | platform engineer + release manager | L13 933-939 |
| no file — incidents arriving through a channel or webhook (this sample's only trigger is `bands.yml`) | nothing | Claude Tag in the incident channel (Slack/Teams), or a webhook from the monitoring stack into the same detect → intent path; the version-controlled lessons file the post-mortem is written to | platform engineer + on-call owner | L14 1034, L14 1078-1086 |
| no file — Claude as the reviewer | nothing; in the sample runs a person read `REVIEW.md` and reviewed | the managed Code Review service enabled by an admin, or `claude-code-action` in the org's own CI (model calls via Bedrock/Vertex/Foundry where required), the `@claude` fix loop, and the slash command that works a PR until it is green and waiting on the code owner | admin or platform engineer; tech lead owns `REVIEW.md` | L11 750-758 |
| no file — branch protection (this repo has one owner, so none is on) | nothing; `check` and `agent evals` run on every PR but block nothing, and `agent evals` is red without the key | a ruleset on `main` with `check` and `agent evals` as required status checks and the `ANTHROPIC_API_KEY` secret set — until the secret is in, the red `agent evals` job blocks every config PR, which is the point | platform engineer | L10 727, L13 963 |
| no file — UI visual check tool (this sample has no UI) | nothing | a browser tool or a screenshot utility wired in via MCP, and the mock Claude compares against | engineer setting up the loop | L9 612, L9 627 |
| no file — non-engineer contributor's commit path | nothing (this sample commits `intent/` from a CLI session via `git`/`gh`, not from a non-engineer) | a claude.ai/Cowork setup with a GitHub connector configured to commit Markdown to `intent/`, and who is allowed to use it | platform engineer | L2 185-189 |

## The worked example of the team's part
Since 2026-09-10 this repository carries one team's own answers under `org-skills/`, `policies/`
and `docs/research/` — adopted marketplace skills with provenance, designed skills transcribing
`policies/*.md`, and the research that chose them. Two layers: team clauses in `policies/*.md`
(thin — this team builds internal-only software) and per-project values in a `PROJECT-POLICY.md`
filled from `policies/PROJECT-POLICY.template.md`. A project adopting this template fills that
file first; `org-skills/examples/claims-status/` shows one filled-in example. Treat all of it as an
example of *how* to fill the rows below, not as the answer for another team.

## Why the sample does not fill these in
Policy is the organization's, not this repo's: the playbook requires a named owner, a documented
source of truth and a sign-off for each policy skill (L6 448, L6 460) — a sample repo has none of
the three. The same holds for the hook values, the review roster, the eval corpus and the metric
baseline: each is drawn from an organization's actual standard, actual people or actual task
history, none of which a template can invent without lying about where the check came from.

## Order to fill them in
`intent.md`'s home (L2 183, no prerequisites) and CLAUDE.md (L5 389, no prerequisites) first — every
other lesson in the map builds on one or both. Policy skills go in before the first `spec.md` is
written (L3 253 lists them as a `spec.md` prerequisite). Hook values go in before the first real
`make check`/`make build` run, since an unfilled `PROTECTED` or credential pattern is a gate that
does not gate anything yet.
