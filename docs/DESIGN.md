# intent-sdlc-sample 설계안 v0.2 — 플레이북 14 플레이 전수 반영 (2026-09-08)

> 상태: **초안 · 사용자 검토 대기**. 승인되면 이 문서가 레포의 첫 커밋(`docs/DESIGN.md`)이 되고, 레포를 만드는 일 자체가 첫 사슬 `intent/0001` 이 된다.
> 정본: Claude Academy 「The AI-Native SDLC Playbook」 14레슨 전문(사용자 제공 아티팩트 · Fetched 2026-09-08 · 407 blocks · 13 code · 3 figures). 부속 근거: 딥 리서치 보고서 · 레퍼런스 레포 7종 실측 분석.
> v0.1 → v0.2 변경: 레슨 4~12 의 구체 지시(healthy output · test-file 훅 · REVIEW.md 패스 구성 · managed settings 함정 · source of truth 3구성 · 플레이별 지표 14쌍)를 전부 반영. 사슬 2본 → **3본**(메타 · 기능 · 결함). 플레이 전수 판정표(§8) 신설.

---

## 0. 결정 요약

| # | 결정 | 선택 | 근거 |
|---|---|---|---|
| D1 | 형태 | **샘플** — 사슬 **3본** + 그 사슬을 강제하는 최소 장치 | 사용자 지시. N=1 샘플은 규칙과 우연을 못 가른다(JHashimoto 실측) |
| D2 | 정본 | **Academy 14레슨**(slug 이 좌표) | 블로그 정본은 자체 좌표 발명을 부른다(imsungbin) |
| D3 | 언어 | 산문 **한국어** · 파일명·frontmatter 키·상태 어휘·절 영문 토큰은 **영어 고정** | 리터럴 검사가 언어를 타면 죽는다(honghu: `待团队填写`→`TODO` 로 전량 통과) |
| D4 | intent 스키마 | `# Intent:` 접두 + **YAML frontmatter**(7키) + 5절(영문 토큰 + 한국어 병기) · 플레이스홀더 `‹…›` | 레슨 7필드 보존 · `[…]` 는 정상 산문 거짓 양성(jcuervo 실측 6건) |
| D5 | 상태 어휘 | **`draft \| accepted \| rejected \| superseded`** 한 곳 정의 · accepted 파일 불변 | 참조 레포 상태 어휘 최대 5벌 공존(bashebr) |
| D6 | 승인 기록 | 레슨 그대로 **merge / close** · 별도 원장 파일 없음 | bashebr 원장 해시체인은 재체인 위조 rc=0 |
| D7 | 검증기 | `scripts/check_artifacts.py`(stdlib) — 닫힌 어휘만 · 코드 펜스 제거 후 판정 · **레퍼런스에서 뚫린 8종을 픽스처로 상주** | 7개 후보 중 실효 검증기 0 |
| D8 | 강제층 | 훅(exit 2 · realpath · fail-closed) + CI 차단 + 브랜치 보호/CODEOWNERS + **배선 검사** | jq 부재 fail-open(jsnkle·imsungbin) · 배선 안 된 훅(bashebr) |
| D9 | 메트릭 | 플레이북 14쌍 전부 `docs/METRICS.md` 에 적고, **git 으로 계산 가능한 것만** 스크립트로 | 7개 후보 전부 Stage 1 지표 0 |
| D10 | 비엔지니어 경로 | 이슈 폼까지 · 폼→PR 자동화·커넥터는 이월 원장에 | 내장 GitHub 커넥터는 공식 문서상 읽기 전용 |
| D11 | 라이선스 | **MIT** + `NOTICE`(차용 출처) | 참조 레포 2곳이 무라이선스라 반쪽 |
| D12 | 도그푸딩 | `intent/0001` = 이 레포 자체 · 예제는 검증기 픽스처 1호 | 참조 레포 4곳이 자기 예제에서 자기 규칙을 어겼다 |
| **D13** | **인용 정책** | 플레이북 원문은 **짧은 축자 인용 + 출처 표기**만. 예제 코드 블록을 통째 복사하지 않고 **우리 소재로 재작성** | 아티팩트 말미 *"Copyright Anthropic. Personal reading copy."* — 사설 레포라도 전문 복제는 하지 않는다 |
| **D14** | **source of truth** | 레슨 4의 3구성 중 **「The repo as the source of truth」** 를 명시 선언(`docs/SOURCE-OF-TRUTH.md`) · 외부 기록 ID 는 `record:` 필드로 링크만 | 레슨이 「artifact 마다 하나를 정본으로 지명하라」고 요구 — 안 정하면 다음 사람이 추측한다 |
| **D15** | **사슬 3본** | 0001 메타(레포 자체) · 0002 기능(청구 상태) · **0003 결함**(레슨 8의 「실패 시험 먼저 + test-file 훅」 시연) | 레슨 8의 핵심 지시는 결함 사슬 없이는 시연 불가 |
| **D16** | **승인 전이 예외** | 브랜치에서 `accepted` 는 `git diff <기본브랜치> -- <파일>` 이 `status:` 줄 하나만 바꾼 경우에만 허용 | 승인 PR 이 자기 CI 에 막히는 것을 실측으로 발견 |

부모 결정(비고위험 · 되돌릴 수 있음): 레포 이름 `intent-sdlc-sample`(private · `bifrost17`) · 예제 = 플레이북 자체 예제의 한국어 재현(청구 상태 자가조회) · 구현 언어 Python stdlib + bash/jq · PO = `@bifrost17`(단일 소유자 · §6.4 에 self-review 한계와 실증 방법).

---

## 1. 목표 · 비목표

**목표** — 레슨 1의 주장 *"Each stage ends by writing [an artifact] to version control … and the next stage begins by reading it. The chain of commits is also the audit trail"* 를 **기계가 지키는 레포**로 시연한다. 읽는 사람이 ① `git log --reverse` 로 사슬을 따라가고 ② `make check` 하나로 강제가 살아 있는지 확인하고 ③ `make metrics` 로 플레이북 지표를 실제 수치로 본다.

**비목표** — 제품이 아니다. 예제 코드는 사슬을 보여줄 최소한(stdlib)이고, 배포 대상·외부 서비스·조직 계정을 요구하는 플레이는 §10 이월 원장에 이름으로 남긴다.

---

## 2. 레포 구조

```
intent-sdlc-sample/                       (private · MIT)
├── README.md                     30분 투어 · 사슬 읽는 법 · 「검증기가 보지 않는 것」
├── CLAUDE.md                     ≤60줄 · Commands(healthy output 포함) · Conventions · Architecture · Things Claude gets wrong
├── REVIEW.md                     리뷰 패스 3(bugs · security · compliance) · Important vs Nit · 보고하지 않을 것
├── LICENSE (MIT) · NOTICE        차용 조각 출처(MIT · CC BY 4.0 · 아이디어)
├── Makefile                      check · test · lint · metrics · build
├── docs/
│   ├── DESIGN.md                 이 문서
│   ├── STATUS.md                 상태 어휘 · 전이 · 증거 (유일 정의처)
│   ├── SOURCE-OF-TRUTH.md        D14 선언 + 레거시 연동 시 갈림길
│   ├── PLAYBOOK-MAP.md           14레슨 slug ↔ 이 레포 파일 · 구현/부분/없음 (§8 이 정본)
│   ├── PHASES.md                 의도적 미구현 원장 + 승격 조건 (§10)
│   ├── METRICS.md                플레이북 지표 14쌍 · 계산 가능/불가 · 실측표
│   └── plays/                    플레이별 1장: 무엇이 강제되나 · 증거 · 어디에 기록 · 누가 승인 (레슨 8 의 4항 구조)
├── intent/
│   ├── README.md                 홈 규약 · 이슈 폼 → 파일 경로 · ID 규칙
│   ├── 0001-bootstrap-repo/      {intent,spec,plan}.md      ← 레포 자체(메타)
│   ├── 0002-claims-status/       {intent,spec,plan}.md      ← 기능
│   └── 0003-status-cache-defect/ {intent,spec,plan}.md      ← 결함(레슨 8 시연)
├── templates/                    intent.md · spec.md · plan.md · intent-defect.md · intent-incident.md
├── src/claims_status/            예제 구현(stdlib) · service.py · records.py
├── scripts/
│   ├── check_artifacts.py        아티팩트 검증기 (rc 0/1/2 · --format json)
│   ├── check_endpoints.sh        secure-api-review 스킬의 결정론 백스톱
│   ├── metrics.py                지표 계산(git + gh)
│   ├── detect_bands.py           Stage 6 결정론 검출기(모델 미개입)
│   ├── emit_intent.py            검출 결과 → Stage 1 형식 intent 초안
│   ├── deploy.sh                 배포 흉내(승인 게이트 시연 대상)
│   └── check_all.sh              게이트 정본 (= make check)
├── ops/bands.yaml                1σ log · 2σ diagnose · 3σ propose
├── evals/                        cases/*.json · check.sh (수동 실행 · 키 필요)
├── tests/
│   ├── test_check_artifacts.py · fixtures/{green,red}/   ← 뚫린 8종 픽스처
│   ├── test_claims_status.py    AC ↔ 시험 이름
│   ├── test_detect_bands.py     밴드 규칙 단위 시험
│   ├── test_hooks.sh            차단/통과/우회 세트
│   └── test_wiring.sh           훅이 settings 에 실제 등록됐는가
├── .claude/
│   ├── settings.json            훅 5개 배선
│   ├── hooks/                   protect-accepted · protect-tests · plan-sync · no-secrets · production-gate
│   ├── skills/{capture-intent,secure-api-review}/SKILL.md
│   ├── agents/verifier.md       레슨 7 의 verifier 서브에이전트
│   └── commands/spec.md         레슨 3 의 프롬프트를 슬래시 커맨드로
├── org/managed-settings.example.json   레슨 11 관리형 설정 예시(비활성 · 함정 주석)
└── .github/
    ├── workflows/check.yml      PR·push → make check (필수 상태 체크)
    ├── workflows/agent-evals.yml  workflow_dispatch 전용(키 필요 · 비활성 사유 명시)
    ├── ISSUE_TEMPLATE/intent.yml  비엔지니어용 5절 폼
    ├── PULL_REQUEST_TEMPLATE.md   사슬 4문 체크
    └── CODEOWNERS                 intent/** · .claude/skills/** · CLAUDE.md
```

---

## 3. 아티팩트 스키마

### 3.1 intent.md
```markdown
---
id: 0002-claims-status
kind: intent
status: draft                         # draft | accepted | rejected | superseded
author: 홍길동 (청구운영팀)
created: 2026-09-09T10:12:00+09:00    # 첫 대화 시각(발의자 신고) — 레슨 2 leading 지표의 기점
record: none                          # 외부 기록 ID(Jira 등) 또는 none — D14 링크
supersedes: none
---
# Intent: 청구 상태 자가조회

## Problem (문제)
‹오늘 무엇이 안 되는가 — 관찰된 사실·건수·시간›

## Proposed outcome (원하는 결과)
‹끝났을 때 무엇이 달라지는가 — 검수 가능한 문장›

## Affected users and systems (영향 범위)
‹사용자 · 시스템 · 데이터›

## Constraints (제약)
- C1 ‹지켜야 할 선›
- C2 ‹범위 밖›

## Open questions (미결)
- Q1 ‹아직 답이 없는 것 — 답할 사람›
```
레슨 2 의 7필드(`# Intent:` · Author · Status · 5절)를 전부 보존하고 `id · kind · created · record · supersedes` 를 더한다. **더한 필드는 전부 검증기가 읽는다**(안 읽는 필드는 두지 않는다 — jcuervo 의 `Date:` 반례). 제약 `C#`·미결 `Q#` 번호는 spec 이 ID 로 이어받는 유일한 기계 흔적.

변형 템플릿 2: **defect**(기대/실제/재현 · 하류 오염 · 규제 통지) · **incident**(Stage 6 이 쓰는 형식 — 이상과 증거 · 제안 결과 · 영향 시스템 · 미결 · 「완화는 맥락이지 결과가 아니다」).

### 3.2 spec.md
```markdown
---
id: 0002-claims-status
kind: spec
status: draft
upstream: intent.md@<sha>             # 그 커밋의 intent 가 accepted 여야 통과
skills_applied: [secure-api-review]   # 레슨 3 "skill versions in force are logged"
---
# Spec: 청구 상태 자가조회 (from intent 0002)

## Requirements (요구)              - R1 …
## Design (설계)
## Constraints inherited (상속한 제약)   ← intent 의 C# 전부 재수록(누락 = red)
## Constraints discovered (발견한 제약)
## Open questions from intent (intent 의 미결)  ← Q# 마다 answered:/carried: (누락 = red)
## Flagged concerns (플래그)          - F1 ‹정책 충돌 · 담당자›
## Out of scope (범위 밖)
## Acceptance criteria (수용 기준)     - AC1 → R1 ‹관찰 가능한 결과›
```
레슨 3 의 요구 4가지를 절로 고정: 「flagged concerns 를 요구한다」 · 「intent 의 미결이 answered 또는 carried forward 인가」 · 「skill 버전 기록」 · 「spec 과 intent 를 나란히 커밋」. 빈 절 금지 — 해당 없으면 *「해당 없음 — 이유」* 를 쓴다.

### 3.3 plan.md
레슨 4 의 4절 그대로 + 2절: `## Files that change` · `## Order of work` · `## Risks` · `## Proof`(AC# ← 시험 이름) · `## Options not taken` · `## Parallelisable`. 머리에 `upstream: spec.md@<sha>` 와 레슨 예시대로 `(from intent 0002)` 를 함께 적는다(두 홉 다 표기 — intent 가 바뀌면 plan 이 낡았음을 기계가 잰다).

---

## 4. 상태 · 전이 · 증거 (`docs/STATUS.md` 요지)

| 전이 | 누가 | 증거 | 기계 검사 |
|---|---|---|---|
| — → draft | 발의자(또는 이슈 폼) | 첫 커밋 | frontmatter 필수 키 · `created` ISO8601(오프셋 필수) |
| draft → accepted | product owner | `status:` 를 바꾼 커밋이 **머지된 PR** 안에 | 브랜치에서 accepted 금지(**D16** 예외) · accepted 파일 이후 변경 불가 · 훅이 로컬 편집 차단 |
| draft → rejected | product owner | PR close | 동일 |
| accepted → superseded | 새 intent 발의자 | 새 intent 의 `supersedes:` + 옛 파일 상태 변경이 같은 PR | 대상 존재 · 대상이 accepted 였는가 |

`accepted_at` 은 두지 않는다 — git 이 안다(`git log -S'status: accepted'`). 자기 신고 필드는 `created` 하나뿐이고, 그것이 git 이 모르는 유일한 값이다.

**D16** — 브랜치에서 `accepted` 는, 그 파일의 `git diff <기본브랜치> -- <파일>` 이 **`status:` 줄 하나만** 바꾼 경우에만 허용한다. 내용이 함께 바뀌면 여전히 red — 승인은 이미 검토된 문서에 도장을 찍는 행위이지 「고치면서 승인」이 아니다. 내용을 바꾸려면 `draft` 로 되돌려 다시 검토받는다. 기본 브랜치 참조가 없거나 detached HEAD 이면 이 판정은 note 로 빠지고 그 자리는 브랜치 보호가 맡는다.

---

## 5. 검증기 — 축의 어휘 소유권

| 검사 | 열거 집합 | 닫는 것 |
|---|---|---|
| 디렉터리 `NNNN-slug` · `id == dirname` · `kind == 파일명` | 우리 규약 | 소유권 |
| frontmatter 키 집합 · `status` enum · `created` ISO8601 | 우리 규약 | 소유권 |
| 절 집합(영문 토큰 5/8/6) · 순서 · 빈 절 금지 · 플레이스홀더 `‹›` 잔존 | 우리 템플릿·토큰 | 소유권 |
| **코드 펜스·인라인 코드 제거 후** 위 판정 | 펜스 문법 하나만 | 기계 유도(명시) |
| `upstream: <file>@<sha>` — sha 존재 · 그 커밋 파일이 `accepted` · id 일치 | git | 단일 통로(`git show`) |
| C#/Q# 이어받기 · AC#→R# 고아 없음 · Proof 가 AC# 를 덮음 · Files that change 경로 실재 | 우리 ID 규약 | 소유권 |
| spec 본문 ≠ intent 본문(정규화 후 동일 = red) | — | 단일 검사 |
| 브랜치 규칙: accepted 는 main 에서만 · accepted 파일 불변 | git diff | 단일 통로 |

**하지 않는 것(README 에 명시)**: 해법 제목 여부 · 산문 품질 · 「요구가 문제를 푸는가」 — 사람과 리뷰의 몫. 안 보는 것을 보는 척하지 않는다.

**계약**: rc 0 통과 / 1 결함 / 2 판정 불가 · `--format json` + `schema_version` · 안정 `code`.

**게이트 상주 대조**: `templates/*` 는 반드시 rc=1 · `intent/**` 와 `fixtures/green/*` 는 rc=0 · `fixtures/red/*` 8종은 지정 code 로 red — 펜스 상태 위조 / 대괄호 산문(green) / 브랜치 자기 승인 / 플레이스홀더 잔존 / 무관 상류 / spec=intent 복사 / Proof 0 / 빈 절·Q 누락.

---

## 6. 강제층 (레슨 6b · 8 · 11)

### 6.1 훅 5 — 전부 `exit 2` + stderr, `realpath` 정규화, `command -v jq || exit 2`(fail-closed), matcher 에 `NotebookEdit` 포함
| 훅 | 무엇을 막나 | 레슨 |
|---|---|---|
| `protect-accepted.sh` | accepted 아티팩트 편집 | 4·11(protected paths) |
| `protect-tests.sh` | **결함 수정 중 시험 파일 편집** — 레슨 8 의 핵심 지시 | 8 |
| `plan-sync.sh` | plan 의 `Files that change` 밖 소스를 커밋(같은 커밋에서 plan 을 고치면 통과) | 4 |
| `no-secrets.sh` | 자격증명이 diff 에 드는 것 | 6b |
| `production-gate.sh` | `scripts/deploy.sh … production` 을 승인 없이 실행 | 11 |

레슨 11 의 *"A block should explain itself"* 를 계약으로: 차단 메시지에 **사유 + 승인 경로**를 반드시 넣고, 그것을 `tests/test_hooks.sh` 가 문자열로 단정한다.

우회 시험(참조 레포에서 실제로 뚫린 벡터): `./` `../` `//` 경로 · `.path` 키 · Bash 페이로드 · `git  commit`(공백 2) · `git -C .` · 대소문자 · `--dry-run=false` 류 부분 문자열 · jq 부재 · 깨진 JSON · 빈 stdin. **판정은 토큰 단위 앵커**로 하고, 허용 목록을 차단 판정보다 먼저 돌리지 않는다.

### 6.2 배선 — `tests/test_wiring.sh`
훅 파일 존재로 끝내지 않는다. `.claude/settings.json` 에 5개가 등록됐는지, matcher 에 `NotebookEdit` 이 있는지를 시험이 잰다(bashebr 는 스캐폴드에 배선이 0이었다).

### 6.3 관리형 설정 — 예시 + 함정 문서화
`org/managed-settings.example.json` 에 레슨 11 의 키(permissions deny/allow · `disableBypassPermissionsMode` · `allowManagedPermissionRulesOnly` · sandbox(`failIfUnavailable`·`allowUnsandboxedCommands`·network·credentials) · `allowManagedHooksOnly` · `disableSideloadFlags` · `strictKnownMarketplaces` · `allowManagedMcpServersOnly` · `requiredMinimumVersion`)를 **비활성 예시**로 싣고, 레슨이 경고한 함정을 주석과 문서에 축자로 남긴다:
> `allowManagedHooksOnly` 를 켜면 프로젝트 `.claude/settings.json` 의 훅은 **차단된다** — 이 레포의 승인 게이트를 유지하려면 관리형 파일의 hooks 블록에 다시 정의해야 한다.

### 6.4 CI · 브랜치 보호
`check.yml`(PR·push) → `make check` 를 **필수 상태 체크**로. ruleset(`protect-main`)에서 **켜져 있는 것**: PR 필수 · 필수 상태 체크 `check` · 삭제 금지 · non-fast-forward 금지 · `current_user_can_bypass: never`. **켜지 못한 것**: CODEOWNER 필수 승인(`require_code_owner_review: false`) · 승인 수 ≥1(`required_approving_review_count: 0`) — **단일 소유자**라 켜면 자기 PR 을 자기가 승인 못 해 모든 머지가 영구 차단되기 때문이다. 그 자리는 **CI 필수 체크 + 검증기(§5) + 훅(§6.1)** 이 대신한다. `.github/CODEOWNERS` 는 소유자를 이름으로 적는 문서로 남고, 기계 강제는 아니다. 레슨 12 의 원칙 *"the agent may act up to the production gate and cannot pass it"* 를 브랜치 보호로 구현한다.
단일 소유자 한계: GitHub 은 자기 PR 을 자기가 승인 못 한다 → 실증은 「리뷰 없는 PR 이 머지 불가」를 스크린샷·API 응답으로 1회 남기고, 관리자 bypass 를 쓰면 그 사실을 `docs/STATUS.md` 에 적는다.

---

## 7. 메트릭 (`docs/METRICS.md` · `scripts/metrics.py`)

플레이북의 **leading/lagging 14쌍을 전부 적고**, 이 샘플에서 계산 가능한지 표로 가른다.

| 플레이 | leading | lagging | 샘플에서 |
|---|---|---|---|
| 2 intent | 첫 대화 → 커밋 시간 | survival rate · 첫 spec 이후 intent 변경 수 | **계산**(`created` + git + PR 상태) |
| 3 spec | intent→spec 커밋 간격 | 첫 plan 이후 spec 커밋 수 | **계산**(git) |
| 4 plan | 1차 통과 머지 비율 · plan 승인→머지 | 재작업 회차 · diff↔plan 일치 | **부분**(git · PR 3본뿐) |
| 5 CLAUDE.md | 같은 실수 반복 횟수 | 신규 참여자 첫 머지까지 | **불가**(1인) — 지면에 명시 |
| 6 skills | 정책 승인→스킬 머지 | 정책 인용 리뷰 지적 수 | **불가**(정책 소유자 없음) |
| 7 병렬 | 동시 세션 수(OTel) | 주당 머지 수 | **불가**(OTel 없음) |
| 8 피드백 | 1차 CI 성공률 | PR 리뷰 시간 · 변경 실패율 | **부분**(CI 성공률만) |
| 9 evals | 통과율 추이 | CI 포착 vs 프로덕션 유출 | **불가**(키·인시던트 없음) |
| 10 리뷰 | 첫 리뷰까지 시간 | 머지 전 결함 vs 유출 | **불가** |
| 11 게이트 | 게이트 대기 시간(OTel) | 게이트 위반 도달 수 | **불가** |
| 12 CI/CD | 사람 없이 트리아지된 실패 비율 | DORA | **불가** |
| 13 루프 | 밴드 위반 → intent 큐 시간 | 발견→머지 비율 · 반복 사고 | **부분**(합성 입력으로 시연) |

「불가」를 빈칸으로 두지 않고 **왜 불가인지**를 적는 것이 이 표의 목적이다(레포가 계기보다 강하게 말하지 않기).

---

## 8. 플레이북 14 플레이 전수 판정 (`docs/PLAYBOOK-MAP.md` 정본)

| # | 레슨(slug) | 판정 | 이 레포에서 | 근거 |
|---|---|---|---|---|
| 1 | introduction | 해당없음(서술) | 「사슬 = 감사 추적」 주장을 README + CI 가 시연 | — |
| 2 | capture-intent | **구현** | 템플릿 3변형 · `capture-intent` 스킬 · `intent/` 홈 · 이슈 폼 · PO merge/close · 지표 3 | 전부 |
| 3 | requirements-and-design | **구현(사람 실행)** | spec 템플릿 · `/spec` 슬래시 커맨드(레슨 프롬프트를 우리 말로) · flagged concerns · `skills_applied` 기록 · intent 미결 이어받기 | 자동 job·Claude Design 은 §10 |
| 4 | plan-mode | **구현** | plan 템플릿 · `plan-sync` 훅(레슨의 *"Consider using a hook"* 을 실제로) · `docs/SOURCE-OF-TRUTH.md` 에 3구성 중 「repo」 선언 | auto mode·worktree 병렬은 문서만 |
| 5 | claude-md | **구현** | ≤60줄 게이트 · Commands 에 **healthy output** 예시 · Conventions · Architecture · **Things Claude gets wrong** · 「두 번 틀리면 등재」 규칙 | 전부 |
| 6 | skills-as-institutional-knowledge | **구현** | `capture-intent` + `secure-api-review` 스킬 · `check_endpoints.sh` 결정론 백스톱 · CODEOWNERS = 정책 소유자 | 「스킬이 트리거되는지 시험」은 모델 발화라 **장치 없음**으로 명시 |
| 6b | hooks as build-time guardrails | **구현** | protect-accepted · protect-tests · no-secrets · (포맷터는 lint 로 대체) · 빠르고 파일 단위 | 무거운 검사는 커밋·PR 로(레슨 지시) |
| 7 | parallel-sessions-and-subagents | **부분** | `.claude/agents/verifier.md`(레슨 예시를 우리 명령으로) | 병렬 세션·worktree 는 문서만(1인 샘플) |
| 8 | give-claude-a-feedback-loop | **구현** | `make build/test/lint` + CLAUDE.md 검증 블록(healthy output) · **0003 결함 사슬이 「실패 시험 먼저 → 커밋 → 시험 못 고치게 훅」 전 과정을 시연** | UI 시각 루프는 해당없음(UI 없음) |
| 9 | continuous-evals-in-ci | **부분** | `evals/cases/*.json` 3건 + `check.sh` + `workflow_dispatch` 워크플로 · 키 없으면 skip 을 **명시적 skip 메시지**로 | 20~50 케이스·스케줄·게이트화는 §10 |
| 10 | ai-in-the-pr-review-loop | **부분** | `REVIEW.md`(패스 3 · Important vs Nit · 보고 제외 · nit 상한) · PR 템플릿 · CODEOWNERS | claude-code-action·관리형 리뷰·@claude 픽스 루프는 §10 |
| 11 | hooks-as-approval-gates | **구현** | `production-gate.sh` + `scripts/deploy.sh` 대상 + 우회 시험 세트 · 차단 메시지에 사유+승인 경로 · `org/managed-settings.example.json` + `allowManagedHooksOnly` 함정 문서화 | 실제 MDM 배포는 §10 |
| 12 | ci-cd-integration-and-deployment | **부분** | 「에이전트는 게이트까지만」을 브랜치 보호로 · 배포는 흉내 스크립트 | 샌드박스·MCP 배포·롤백 리허설·환경별 티어는 §10(배포 대상 없음) |
| 13 | closing-the-loop-on-metrics | **구현(오프라인)** | `ops/bands.yaml`(1σ/2σ/3σ) · `detect_bands.py`(모델 미개입 · 단위 시험) · `emit_intent.py` → Stage 1 형식 초안 · 0003 이 그 산출로 시작 | 라이브 스케줄·Claude Tag·runbook 롤백은 §10 |
| 14 | closing-thoughts-and-resources | 해당없음 | 레슨 14 의 리소스 14링크를 `PLAYBOOK-MAP.md` 말미에 | — |

**집계: 구현 8 · 부분 4 · 해당없음 2.** 「없음」이 0인 이유는 없음을 §10 이월 원장으로 옮겼기 때문이고, 이월 항목마다 승격 조건이 붙는다.

---

## 9. 사슬 3본

**0001-bootstrap-repo(메타)** — intent: 「사슬을 기계가 지키는 샘플이 없다」 · spec: R1 검증기 · R2 훅 5 + 배선 · R3 CI 차단 · R4 지표 · R5 사슬 3본 · C1 stdlib · C2 한국어 산문/영문 키 · Q1 예제 주제 · plan: 위 트리 · Proof: 픽스처 8 red + green. **이 사슬의 diff 가 레포 자체다.**

**0002-claims-status(기능)** — 플레이북 예제의 한국어 재현. 제약: 새 PII 노출 금지 · 기존 인증만 · 상류 50rps 캐시. 구현은 stdlib(`service.py` 허용 필드 4 · 60초 캐시). 시험은 AC↔이름 매핑 + **허용 목록을 시험에 독립적으로 다시 적어** 동어반복 회피(JHashimoto M3b 반례: 상류에 새 필드가 생겨도 새지 않음을 잰다).

**0003-status-cache-defect(결함)** — `detect_bands.py` 가 합성 CI 실패율에서 3σ 를 잡고 `emit_intent.py` 가 Stage 1 형식 intent 초안을 쓴다 → 사람이 triage(Fix now) → **실패 시험 먼저 커밋(red 실측 출력 첨부) → protect-tests 훅이 켜진 상태에서 구현 → green**. 레슨 8·13 을 한 사슬로 잇는다.

---

## 10. 의도적 미구현 원장 `docs/PHASES.md`

| 항목 | 레슨 | 승격 조건 |
|---|---|---|
| intent merge → spec PR 자동 생성 job | 3 | 손으로 3회 반복될 때 |
| Claude Design 목업 → Code 핸드오프 | 3 | UI 있는 예제가 생길 때 |
| auto mode · worktree 병렬 세션 | 4·7 | 동시 작업자 2인 이상 |
| 스킬 트리거 시험(모델 발화) | 6 | evals 가 키를 얻을 때 |
| evals 20~50 케이스 · 스케줄 · 머지 게이트화 | 9 | API 키 예산 확보 |
| claude-code-action / 관리형 코드 리뷰 · @claude 픽스 루프 · babysit | 10 | 리뷰어 2인 이상 또는 조직 계정 |
| 관리형 설정 MDM 배포 · 플러그인 마켓플레이스 | 11 | 조직(Team/Enterprise) 계정 |
| 샌드박스 · MCP 배포 도구 · 롤백 리허설 · 환경별 티어 | 12 | 실제 배포 대상 |
| 라이브 스케줄 밴드 감시 · Claude Tag 온콜 · 사전 승인 runbook | 13 | 30일 기준선이 쌓일 때 |
| 비엔지니어 폼 → intent PR 자동화 · claude.ai 커넥터 | 2 | 폼 발의 3건 이상 |
| OpenTelemetry 지표(세션·게이트 대기) | 7·11 | 조직 계정 |

---

## 11. 차용 · 출처 (`NOTICE`)

MIT: jcuervo(게이트 상주 양성/음성 대조 · rc 3분법 · description 배타절 · 「해당 없음 — 이유」 규율) · jsnkle(플레이 문서 골격 · 사슬 1장 표 · 검출기 형태) · imsungbin(정본 문장↔파일 표 · 설치기 마커 병합 · 「Open questions from intent」) · bashebr(규칙→집행 매트릭스). CC BY 4.0: intent-md-ko(한국어 절 이름 · 「완료 판정 = 숫자」 · 발주서 대응표). 아이디어(무라이선스 · 출처만 표기): JHashimoto(상속/발견 제약 분리 · 의도적 미구현 원장 · 시험 이름에 요건 ID) · honghu-ai(change-ID 규약 · frontmatter 발상). 플레이북 인용은 D13.

---

## 12. 작업 계획

| 웨이브 | 내용 | 레인 | 게이트 |
|---|---|---|---|
| W0 | 비공개 레포 생성 · 설계안·LICENSE·NOTICE 커밋 · `make check` 골격(첫 검사부터 실질) · 브랜치 보호 | exec(sonnet/low) 1 | `make check` rc=0 · 빈 통과 아님을 뮤테이션 1건으로 확인 |
| W1 | 검증기 TDD(red 픽스처 8 먼저) · 템플릿 5 · STATUS/SOURCE-OF-TRUTH · 훅 5 + 우회 시험 + 배선 시험 · CI | impl(opus/medium) 2 + review(opus/high) 1 | 픽스처 8/8 지정 code · 우회 12/12 exit 2 · 배선 green |
| W2 | 0001·0002 사슬을 **실제 순서**로 · `src/` · 시험 · CLAUDE.md · REVIEW.md · 스킬 2 · verifier | impl 1 + exec 1(PR 흐름 실증) | 검증기 전량 green · 동어반복 뮤테이션 red |
| W3 | 0003 결함 사슬(detect→emit→red 시험→구현) · bands/detect/emit + 시험 · evals 하네스 · metrics · 문서 5종 · PLAYBOOK-MAP | impl 1 + mech(sonnet) 1 + review 1 | 전량 게이트 · 지표 실값 · 브랜치 보호 실증 |

**완료 정의**: ① 픽스처 8종 지정 code red + 정상 green ② 훅 5 차단 + 우회 12 exit 2 + 배선 green ③ 사슬 3본이 실제 시간축 커밋으로 main 에 ④ `make metrics` 가 실값 표 출력 ⑤ 브랜치 보호 실증 1회 ⑥ `PHASES.md` 11항 + 승격 조건 ⑦ `PLAYBOOK-MAP.md` 가 14레슨 전부 판정 ⑧ README 에 「검증기가 보지 않는 것」.

---

## 13. 사용자 확인 대기

1. 레포 이름 `intent-sdlc-sample` 로 갈지(대안: `ai-native-sdlc-sample-ko`).
2. 예제 주제를 플레이북 예제(청구 상태)로 둘지, openWebAgent 의 실제 작은 요구로 바꿀지.
3. `created`(첫 대화 시각)를 자기 신고로 두는 것 — 대안이 없음을 인정하고 「신고값」으로 라벨.
4. 사슬 3본 규모가 과한지(2본으로 줄이면 레슨 8 의 결함 루프 시연을 잃는다).
