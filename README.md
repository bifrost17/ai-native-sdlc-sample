# ai-native-sdlc-sample

A small repo that applies the fourteen lessons of Anthropic's "The AI-Native SDLC Playbook"
(Claude Academy) as written — skills that say what to do, a few hooks that block what the lessons
say to block, and an `intent/` folder where each change is recorded as intent → spec → plan.
Unofficial; not an Anthropic project.

## Read in this order
1. `docs/PLAYBOOK-MAP.md` — each lesson, the device this repo uses for it, and which layer it lives
   in (person, tool, skill, or code).
2. `docs/BOUNDARY.md` — what the machine checks, what a skill says, what a person decides, and
   why a checker inside the tree is not an approval authority.
3. `.claude/skills/` — `capture-intent`, `design-spec`, `plan`, `secure-api-review`.
4. `intent/0004-lesson-only/` — the change that made this repo look like this, recorded as its own
   chain. `intent/0001-bootstrap-repo/` is the earlier chain, kept as history in the pre-slim
   convention (frontmatter, status fields); the current template is what 0004 uses.
5. `CLAUDE.md`, `REVIEW.md`, `.claude/agents/verifier.md` — the agent-facing files.
6. `docs/METRICS.md` — the lessons' indicators as git commands.
7. `docs/ADOPTING.md` — where this template needs another organization's own values instead of
   this repo's sample ones, and who (in the playbook's terms) fills each one in.
8. `docs/RUNS.md` (on the experiment branch, see Experiments below) — actual runs against these devices, judged by each play's own governance and
   measurement sections, not a separate scorecard.

## What this repo does
- Encodes the intent, spec and plan templates in skills, with `templates/` as copies.
- Keeps the hooks the lessons name as deterministic (protected paths, test protection, secrets,
  format/lint, production gate). A plan-sync hook is optional in L4 329 ("Consider") — this repo
  does not have one.
- Runs `make check` (= `make test`) in CI; a red check is a red PR. Evals need an API key and run
  in their own workflow on config changes and on a schedule (L10 689). Without the
  `ANTHROPIC_API_KEY` secret that job exits 2 and shows red: it did not run, and "did not
  run" is not "passed". Add the secret to make it real.
- Records every change to itself as a chain under `intent/`.

## Chains
| Chain | Kind | Entry path | PR(s) |
|---|---|---|---|
| 0001 bootstrap-repo | record · pre-slim convention | this repo, self-recorded | #12 |
| 0004 lesson-only | slim | this repo, self-recorded | #16 |
| 0010 experiments-on-branches | structure | this repo, self-recorded | #55 |

## Organization skill set (`org-skills/`)
This repository is also one team's answer to the team's part of the playbook, in two layers:

- **팀 조항** — `policies/*.md`, thin on purpose (the team builds internal-only software; about a
  dozen clauses). Owner sign-off is the merge (`.github/CODEOWNERS`).
- **프로젝트 슬롯** — each project copies `policies/PROJECT-POLICY.template.md` into its own
  repository and fills six slots; skills cite the slot IDs rather than inventing values.

The skill set is one plugin under `org-skills/skills/` (root `.claude-plugin/marketplace.json`
serves it); `org-skills/examples/` holds one project's filled-in example and does **not** load.
The research behind every adopted or designed skill is under `docs/research/<skill>/`, decisions in
`docs/decisions/`. The template's own skills stay in `.claude/skills/`. Chains `intent/0011` and
`intent/0012` record the move and the split.

## Experiments
`main` is the template and the template's own chains only. Each experiment — chains run *on* the
template to see whether it works — lives on a branch `experiment/<date>-<topic>` that is never
merged, carries its raw evidence under `raw/`, and names the `main` commit it started from in
`EXPERIMENT.md`. What an experiment reveals about the template comes back to `main` as a PR.

| Branch | Started from | What it holds |
|---|---|---|
| `experiment/2026-09-09-claims-status` | `main@0daf6550` (PR #54) | chains 0002 (feature) · 0005 (defect, issue #20) · 0006 (incident, band) · 0007 (defect, issue #24, unbriefed agent) · 0008 · 0009 (human–agent runs); example app `src/claims_status/`; `docs/RUNS.md`; 172 raw files. Template feedback from it: PRs #19 #27 #29 #33 #34 #35 #40 #44–#54 |

Issues #24, #25, #26, #32 belong to that experiment's claims-status app.

## Source of truth
This repo is the source of truth (L4 380 "The repo as the source of truth"). There is no
external system of record — no Jira, no separate requirements tool — for the artifacts under
`intent/`; the commit is the timestamp authority.

## What this repo does not do
- It does not check artifact form, status or transitions in code. Approval is a merged PR;
  a missing section is caught by the skill and by the product owner reading the file.
- It does not enforce policy skills with code unless the lesson names the hook.
- It does not replace the playbook. Quotes are short and cite the line; the original is
  Claude Academy, `courses/ai-native-sdlc-playbook`, Copyright Anthropic.

## Commands
`make test` · `make evals` · `make check` (see `CLAUDE.md` for healthy output).
Plan mode headless: `claude -p --permission-mode plan` writes the plan outside the repo and has no
ExitPlanMode; the engineer's next prompt is the acceptance (chain 0008, L4 327).
Implementation turns ran in auto mode (`claude -p --permission-mode bypassPermissions`, L4 361);
the five hooks in `.claude/settings.json` were the guardrail (chains 0008 and 0009: 107 and 131
hook events in the implementation turn, `docs/RUNS.md` on the experiment branch).
`.claude/settings.json` allows this repo's own safe commands without a prompt (`permissions.allow`,
L8 545); the team replaces the list with what its organization considers safe (`docs/ADOPTING.md`).
