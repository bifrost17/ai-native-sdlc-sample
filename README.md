# ai-native-sdlc-sample

## Project goal

우리의 목표는 **Anthropic의 AI-Native SDLC Playbook을 충실히 따라, 우리 팀이 실제 소프트웨어
개발에 사용할 템플릿·스킬·정책을 구축하는 것**이다. 공개된 가이드의 이론과 방법론을 우리 팀이
사용할 수 있는 개발 체계로 구체화한다.

목표 수준은 **사람이 개입하는 실제 개발에서 플레이북의 주요 흐름이 대체로 잘 작동하는 것**이다.
템플릿만으로 모든 가이드를 완벽하게 재현하려 하지 않는다. 누락을 없애려고 템플릿을 프로그램처럼
키우거나 검증 스크립트와 절차를 계속 추가하지 않는다. 사람의 판단과 에이전트의 창의적 재량을
유지하고, 실제 개발 흐름이나 결과에 중요한 차이를 만드는 보완을 우선한다.

하네스를 사용하는 에이전트와 독립 검토자도 실수할 수 있다. **모든 실수를 없애는 것을 하네스의
목표로 삼지 않는다.** 작업의 난도·영향·불확실성에 맞는 모델과 추론 수준을 선택하고, 중요한 판단이나
실수가 반복되는 작업에는 더 역량 높은 모델과 높은 추론 수준을 사용한다. 중요한 실수는 발견·수정하고
근거를 남기되, 개별 실수마다 템플릿 규칙이나 검사기를 추가하지 않는다.

우리 팀은 사내 동료에게 프로그램을 제공하며 소프트웨어 판매나 유료 라이브 서비스를 운영하지 않는다.
문제가 생겨도 비교적 직접 대응할 수 있는 환경이므로 정책은 의도적으로 얇게 유지한다. 외부 고객용
서비스의 절차를 기본값으로 가져오지 않고 실제 영향과 대응 가능성에 맞는 최소 기준을 적용한다.

- **템플릿** — 의도, 요구사항과 설계, 구현 계획을 기록하고 다음 단계로 이어받을 문서와 작업 구조.
- **스킬** — 플레이북의 작업 방식과 우리 팀의 지식을 AI가 개발 과정에서 적용할 수 있는 지침.
- **정책** — 브랜드·보안·컴플라이언스·UX 등에 관한 우리 팀의 실제 기준과 책임자, 이를 적용하는 스킬.
- **브랜치·PR 전략** — GitHub Flow를 템플릿에 포함하고 목적·의존성·검증을 기준으로 PR을 나눈다.
  사람의 읽기 속도나 고정 줄 수만으로 크기를 강제하지 않는다.
- **통제와 검증** — 플레이북이 제시한 사람의 판단·승인, 훅, 테스트, 리뷰, CI를 구현하고 실제 개발 과제로 작동을 확인.

문서 갱신의 목표는 **중요한 요구·설계·계획 누락을 사람의 별도 상기 없이 발견하고 보완하는 것**이다.
기본 팀 경로는 별도 설치하는 [sdlc-feedback 스킬과 네이티브 검증자](org-skills/README.md)다.
변경 시에는 영향받는 문서를 갱신하고, 관련 커밋에서 계획과 구현을 함께 기록하며, 구현 완료 전에는
새 문맥에서 실제 근거를 검토한다. 질문·수락 대기와 영향 없는 문서에 불필요한 수정을 요구하지 않는다.
스킬은 사용을 판단하는 지침이며 무오류나 호출 강제를 보장하지 않는다. 조직의 사람 승인과 병합 권한은
별개다. 기존 [팀 CLI](team-harness/README.md)는 0018의 선택적인 실행·기록 실험 도구로 보존한다.

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
설치·갱신 명령과 이벤트별 사용법은 [팀 스킬 안내](org-skills/README.md)에 있다.
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
실험 방법·HUMAN 역할·초기 사례 데이터는 [실험 가이드](docs/experiments/README.md)에 있다.
`main`에는 제작 자산과 방법·데이터·실행 색인을 두고, 실제 개발 사슬의 대화·제품 코드·시험 결과는
실험 브랜치에 보존한다. 새 전체 프로세스 실험은 제작 자료를 제외한 사용 템플릿의 고정 커밋에서
시작한다. Codex가 HUMAN, Claude Code가 개발 AGENT를 맡아 실제 응답에 따라 대화한다.
계획에서 정한 PR 단위로 실험 통합 브랜치에 합치며 그 브랜치를 제작 `main`으로 머지하지 않는다.
현재 사용 후보는 `codex/use-template-0021@ca87cdb`다. 이전 `0017@add296d`에서 파생했으며
검토한 intent·spec 양식과 선택형 작성 예시를 전달했다. [spec 양식 설계·리뷰·부분 실험](docs/research/sdlc-documentation/spec-design/README.md)에
실제 반영 범위와 한계를 남긴다. 별도 스킬·플러그인 설치는 이 사용판의 필수 조건이 아니다.
[PR 크기 가이드](docs/PR-SIZE.md)와
[GitHub Flow 정책](docs/GIT-WORKFLOW.md)은 채택 제품용 배포 원문이며 사용 후보의 docs/에도 동일하게 둔다.
[조사 보고서](docs/research/pr-size/README.md)는 근거·사례·반례와 한계를 담는다.
[F02 최종 실험](docs/experiments/0016-flow-pilot.md)은 원래 후보 210bcfa에서 8회 대화와 실제 제품 PR 2건의
순차 통합을 수행했다. 계획에 PR 묶음·의존성·머지 순서를 반영하고, 전체 시험 8개·독립 동작 7개·
새 복제본 인도·두 번째 PR 코드 되돌리기가 통과했다. 호스티드 CI·실제 조직 승인·운영 배포는 미관측이다.
후속 부분 실험의 spec/plan 누락은 **중요한 실패**다. HUMAN이 지적한 뒤 복구된 것을 자발적 갱신
통과로 계산하지 않는다. 현재 후보는 후속 요구를 받을 때와 완료를 보고할 때 문서 갱신을 연결한다.
[두 새 사례의 재검증](docs/experiments/0017-artifact-sync.md)은 문서 갱신을 상기하지 않은 업무 대화,
spec 수락·plan 참조·구현과 같은 커밋, 제품 결함 발견과 복구를 각각 기록한다.
[설치한 팀 실행 경로](docs/experiments/0018-team-harness.md)는 독립 검토와 같은 개발 세션의 자동
보완을 실제 실행했다. 현재 문서 누락·옛 수락 참조를 각각 자동 피드백으로 복구했고 정상 대기와
문서 영향 없는 작업도 확인했다. 초기 오판과 검토 오류를 보존하며 개발 Sonnet/low·검토 Sonnet/medium을
사용한다. 일반 Claude 호출은 그 CLI 실험의 적용 범위 밖이다.
[이벤트 기반 스킬 실험](docs/experiments/0019-event-review-skill.md)은 영구 설치한 팀 플러그인을
일반 Claude Code 세션에서 사용한다. 주 개발 대화의 문서 개정과 새 문맥의 완료·브랜치 검토를
분리하고 실제 Skill/Agent 호출, 미호출·인계 실패, 관련 커밋과 회귀를 기록한다.
[F01 첫 대화형 실험](docs/experiments/0015-f01-pilot.md)은
Sonnet·low와 같은 세션에서 9회 주고받고 로컬 인도까지 통과했다. 실제 실행 핀은 de1b1b7이며,
후속 후보의 정책 표 제목 두 곳은 정적 리뷰로 확인했다. 전체 플레이북이나 운영 배포의 성공률을 뜻하지 않는다.
아래 기존 실험은 당시 `main`에서 시작한 역사적 실행이다. 실험에서 얻은 템플릿 개선만 별도 변경으로 가져온다.

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
