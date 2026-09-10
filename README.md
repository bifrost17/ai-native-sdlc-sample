# ai-native-sdlc-sample

## Project goal

우리의 목표는 **Anthropic의 AI-Native SDLC Playbook을 충실히 따라, 우리 팀이 실제 소프트웨어
개발에 사용할 템플릿·스킬·정책을 구축하는 것**이다. 공개된 가이드의 이론과 방법론을 우리 팀이
사용할 수 있는 개발 체계로 구체화한다.

- **템플릿** — 의도, 요구사항과 설계, 구현 계획을 기록하고 다음 단계로 이어받을 문서와 작업 구조.
- **스킬** — 플레이북의 작업 방식과 우리 팀의 지식을 AI가 개발 과정에서 적용할 수 있는 지침.
- **정책** — 브랜드·보안·컴플라이언스·UX 등에 관한 우리 팀의 실제 기준과 책임자, 이를 적용하는 스킬.
- **통제와 검증** — 플레이북이 제시한 사람의 판단·승인, 훅, 테스트, 리뷰, CI를 구현하고 실제 개발 과제로 작동을 확인.

Unofficial; not an Anthropic project.

## North star

프로젝트의 북극성은 **[AI-Native SDLC Playbook](docs/verification/north-star-playbook.html)**이다.
**플레이북 원문은 설계와 판단의 기준이고, 각 문단에 붙인 주석은 그 기준을 얼마나 충실히 따랐는지
점검한 기록**이다. 주석은 우리 프로젝트의 구현, 실제 실행 증거, 판정과 보완 내용을 담는다.

템플릿·스킬·정책을 만들거나 개선할 때는 해당 플레이북 문단과 기존 주석을 먼저 확인한다.
플레이북이 정한 원칙과 역할을 충실히 따르고, 조직이 채워야 하는 부분은 우리 팀의 실제 기준과
상황으로 채운다. 완성 여부는 각 문단이 요구하는 구현과 실행 근거로 판단하며, 주석에 그 결과를 남긴다.

## Read in this order
1. [프로젝트 북극성 — 플레이북과 충실도 평가](docs/verification/north-star-playbook.html) — 가이드 원문과 문단별 평가 근거.
2. `docs/PLAYBOOK-MAP.md` — each lesson, the device this repo uses for it, and which layer it lives
   in (person, tool, skill, or code).
3. `docs/BOUNDARY.md` — what the machine checks, what a skill says, what a person decides, and
   why a checker inside the tree is not an approval authority.
4. `.claude/skills/` — `capture-intent`, `design-spec`, `plan`, `secure-api-review`.
5. `intent/0004-lesson-only/` — the change that made this repo look like this, recorded as its own
   chain. `intent/0001-bootstrap-repo/` is the earlier chain, kept as history in the pre-slim
   convention (frontmatter, status fields); the current template is what 0004 uses.
6. `CLAUDE.md`, `REVIEW.md`, `.claude/agents/verifier.md` — the agent-facing files.
7. `docs/METRICS.md` — the lessons' indicators as git commands.
8. `docs/ADOPTING.md` — where this template needs another organization's own values instead of
   this repo's sample ones, and who (in the playbook's terms) fills each one in.
9. `docs/RUNS.md` (on the experiment branch, see Experiments below) — actual runs against these devices, judged by each play's own governance and
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
- Records each change to what the template *is* as a chain under `intent/`. Upkeep of the repo
  (factual corrections, citation refreshes, chores) is a PR, not a chain — `CLAUDE.md` scopes this.

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

## Verification (`docs/verification/`)
[북극성 문서](docs/verification/north-star-playbook.html)의 주석은 플레이북을 얼마나 충실히 따랐는지
평가한 기록이다. 가이드 문단마다 구현 파일의 경로와 축자 인용문, 실제 실험 증거, 판정
(충실 · 부분 · 팀 몫 · 보완 필요)을 연결한다. 179개 블록(`V2-01`~`V13-16`)이며,
평가에서 발견한 보완점은 PR #44~#54로 반영했다. 항목별 판정은
[INDEX.md](docs/verification/INDEX.md), 챕터별 집계와 라운드 이력은
[CHAPTERS.md](docs/verification/CHAPTERS.md)에 있다.

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
