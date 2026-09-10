# 챕터별 집계

## 0013 보완 — 우선순위 1·2·4 (2026-09-10)

구현 핀 `91727d2`. V3-01·V3-14·V6-05·V6-14·V8-10·V9-07·V13-02·V13-07·V13-09의 본문을 경로 보호·조직 스킬 연결·운영 분기 수정의 현재 근거로 교체했다. 그 외 주석은 v3의 핀과 판정을 유지한다. 원문은 바꾸지 않았고 블록 수와 판정 집계는 **179 · 충실 139 · 부분 23 · 팀 몫 17**로 같다.

새 회귀 시험과 전체 `make check`는 통과했다(macOS에서 대소문자를 구분하는 파일시스템 대조 1건 skipped). Sonnet·low 단일 실행에서 정책 파일 읽기·spec 적용을 확인했지만 기존 문자열 판정은 **10 통과·1 실패**다. `gateway JWT`의 한국어 표기 때문에 난 실패를 통과로 바꾸지 않았다. 3번 채점기 보완은 사용자 지시로 제외했고, 실제 운영 진단·호스티드 CI·오너 수락은 이번 관측 밖이다. [검증 기록](0013-controls.md)과 [모델 증거](0013-policy-evidence.json)를 참조한다.

## 이전 라운드 이력

| 챕터 | 블록 | 충실 | 부분 | 팀 몫 | 보완 | 반영 PR(ai-native-sdlc-sample, 옛 이름 intent-sdlc-sample) | 커밋 |
|---|---|---|---|---|---|---|---|
| 1 소개 | — | — | — | — | — | 검증 대상 아님 | — |
| 2 intent.md로 포착하기 · v1 | 16 | 12 | 3 | 0 | 1 | — | 5fb7b8d |
| 2 intent.md로 포착하기 · v2 | 16 | 12 | 3 | 1 | 0 | #44 (c76bff04 · leading 분자 · 비엔지니어 커밋 경로 · intent/** 코드오너 · H 발화 미기록) | |
| 3 요구사항과 design · v1 | 16 | 11 | 4 | 1 | 0 | — (보완 후보 2: Skills applied 에 스킬 sha · /spec 명령 안 팀 마커 이동) | 3542a00 |
| 3 요구사항과 design · v2 | 16 | 11 | 4 | 1 | 0 | #45 (409ea98 · Skills applied name@sha · 팀 마커 프롬프트 밖으로) | |
| 4 Claude Code plan mode · v1 | 18 | 13 | 5 | 0 | 0 | — (보완 후보 5: Status 문면 통일 · 고위험→tech lead 팀 자리 · 첫 패스 비율 명령 · plan 대조 명령 PR 단위로 · auto mode 한 줄 · RUNS 증거 한계 L4 317) | 239d0a6 |
| 4 Claude Code plan mode · v2 | 18 | 16 | 2 | 0 | 0 | #46 (8350fc1 · Status draft 고정 · 고위험 경로 팀 자리 · L4 측정 명령 2 · auto mode 줄 · L4 317 미측정 기록) | 54db497 |
| 5 CLAUDE.md · v1 | 11 | 7 | 3 | 1 | 0 | — (보완 후보 2: 「두 번째면 CLAUDE.md」 규칙 줄 · RUNS L5 정정 PR 목록·반복 횟수) | 5542b75 |
| 5 CLAUDE.md · v2 | 11 | 9 | 1 | 1 | 0 | #47 (6084fcf · REVIEW.md 규칙 줄 · RUNS L5 정정+반복 실측) | |
| 6 skill · v1 | 16 | 13 | 1 | 2 | 0 | — (경미 2: RUNS 에 L6 470 트리거 실측 · L6 lagging 수열) | cd71c39 |
| 6 skill · v2 | 16 | 14 | 0 | 2 | 0 | #48 (1adef5a · RUNS L6 470 · L6 505) | |
| 7 병렬 session·subagent · v1 | 12 | 8 | 4 | 0 | 0 | — (보완 후보 2: verifier 호출 계기(CLAUDE.md 한 줄) · settings.json 권한 allow 목록) | abdc58e |
| 7 병렬 session·subagent · v2 | 12 | 11 | 1 | 0 | 0 | #49 (2f00415 · CLAUDE.md verifier 줄 · permissions.allow · RUNS L8) | |
| 8 feedback loop · v1 | 17 | 14 | 2 | 1 | 0 | — (보완 후보 3: RUNS Not confirmed 의 Actions 오기 · BOUNDARY Stop hook 결정 · ADOPTING UI 도구 행) | c7a9a4d |
| 8 feedback loop · v2 | 17 | 16 | 0 | 1 | 0 | #50 (64c7100 · RUNS Actions 정정 · BOUNDARY Stop hook · ADOPTING UI 행) | |
| 9 CI 지속적 eval · v1 | 13 | 8 | 3 | 2 | 0 | — (보완 후보 3: ADOPTING required checks 행 · 워크플로 결과 artifact 보존 · METRICS L10 명령 2 · 커밋 메시지의 7/4 는 오기) | a8774b4 |
| 9 CI 지속적 eval · v2 | 13 | 10 | 1 | 2 | 0 | #51 (cd5c3af · artifact 보존 · ADOPTING branch protection 행 · METRICS L10 · RUNS) | |
| 10 PR review loop · v1 | 13 | 6 | 5 | 2 | 0 | — (보완 후보 3: ADOPTING Claude review 통합 행 + BOUNDARY · REVIEW.md 발견은 PR 코멘트로 · METRICS L11 명령 · 커밋 메시지의 5/6 은 오기) | 0876639 |
| 10 PR review loop · v2 | 13 | 8 | 3 | 2 | 0 | #52 (464bac1 · ADOPTING reviewer 통합 행 · BOUNDARY · REVIEW.md 발견은 PR 에 · METRICS L11 · RUNS) | |
| 11 approval gate hook · v1 | 15 | 12 | 0 | 3 | 0 | — (보완 없음 · v2 불요) | |
| 12 CI/CD · v1 | 16 | 2 | 9 | 5 | 0 | — (보완 후보 2: check.yml 에 실패 build 분류 단계(예시 축자, 키 게이트) · METRICS L13 leading) | d7a847b |
| 12 CI/CD · v2 | 16 | 5 | 6 | 5 | 0 | #53 (09cb128 · check.yml Triage failed build · METRICS L13 · MAP · RUNS) | |
| 13 metrics 로 loop 닫기 · v1 | 16 | 8 | 6 | 2 | 0 | — (보완 후보 3: bands.yml 2σ/3σ claude -p 진단 단계(키 게이트) · METRICS L14 leading detected_at · ADOPTING Claude Tag 행) | 22e1946 |
| 13 metrics 로 loop 닫기 · v2 | 16 | 11 | 3 | 2 | 0 | #54 (0daf655 · bands.yml 진단 단계 · ADOPTING 채널 유입 행 · METRICS L14 · RUNS) | |
| 14 맺음말과 참고 자료 | — | — | — | — | — | 검증 대상 아님(가이드 문단 없음 · 참고 자료 목록) | — |

## v3 라운드 — 핀 이동

핀 `main@0daf655` → `main@5599dcf`. 그 사이 커밋 32개(체인 0010 실험 분리 · 0011 org-skills · 0012 팀 정책
· PR #55~#65). 대상은 충실이 아닌 43 블록의 재판정이고, 인용 갱신은 그에 딸린다.

라운드의 작업 목록은 `git diff --name-only 0daf655..HEAD` 하나에서 나온다 — 주석판이 인용한 실제 경로
86개 중 **13개만** 그 사이 바뀌었다(`CLAUDE.md` · `README.md` · `docs/{ADOPTING,BOUNDARY,PLAYBOOK-MAP,RUNS}.md`
· `.claude/skills/{design-spec,plan}/SKILL.md` · `.github/CODEOWNERS` · `evals/cases/04-*` ·
`intent/0002·0008`). 나머지 파일로 간 인용은 줄이 밀리지 않았으므로 손대지 않는다.

| | 블록 |
|---|---|
| 충실 아닌 블록 | 43 |
| 그 중 바뀐 파일을 인용 — 인용 대조 + 재판정 | 18 |
| 인용은 그대로 — 판정만 재검토 | 25 |

### v3 집계 (챕터 2~13 전부 이 핀으로 옮겼다)

| 챕터 · v3 | 블록 | 충실 | 부분 | 팀 몫 | 보완 | v2 대비 |
|---|---|---|---|---|---|---|
| 2 intent.md로 포착하기 | 16 | 13 | 2 | 1 | 0 | 충실 +1 — `V2-05` 부분 → 충실 |
| 3 요구사항과 design | 16 | 12 | 3 | 1 | 0 | 충실 +1 — `V3-05` 부분 → 충실 |
| 4 Claude Code plan mode | 18 | 16 | 2 | 0 | 0 | 판정 동일 |
| 5 CLAUDE.md | 11 | 9 | 1 | 1 | 0 | 판정 동일 |
| 6 skill | 16 | **16** | 0 | 0 | 0 | 충실 +2 — `V6-02`·`V6-03` 팀 몫 → 충실 |
| 7 병렬 session·subagent | 12 | 11 | 1 | 0 | 0 | 판정 동일 |
| 8 feedback loop | 17 | 16 | 0 | 1 | 0 | 판정 동일 |
| 9 CI 지속적 eval | 13 | 10 | 1 | 2 | 0 | 판정 동일 |
| 10 PR review loop | 13 | 8 | 3 | 2 | 0 | 판정 동일(`V10-07` 에 `pr-loop` 추가) |
| 11 approval gate hook | 15 | 12 | 1 | 2 | 0 | `V11-13` 팀 몫 → 부분 |
| 12 CI/CD | 16 | 5 | 6 | 5 | 0 | 판정 동일 |
| 13 metrics 로 loop 닫기 | 16 | 11 | 3 | 2 | 0 | 판정 동일 |

**블록 179 · 충실 139 · 부분 23 · 팀 몫 17 · 보완 필요 0.** 판정이 바뀐 블록 다섯은 summary 에
`이전 → 새` 로 전이를 남겼다.

전환의 원인은 전부 체인 0011·0012 다. 「팀 몫」이던 정책 인프라를 이 레포가 자기 몫으로 채웠다 —
`policies/` 가 오너(`Owner:` 줄)와 문서화된 정본을, `.github/CODEOWNERS` 의 `policies/**` 가 서명을,
`docs/decisions/S1`~`S8` 이 「어느 지식을 골라 무엇을 채택·설계했는가」를 기록한다.
`V2-05` 는 유일한 미결(비엔지니어 접근 수단)이 PR #44 로 닫혀 있었는데 판정만 갱신되지 않은 경우였다.

### 준비물 문단과 작동 문단을 가른다

같은 스킬 세트를 놓고도 문단이 무엇을 묻느냐에 따라 판정이 갈린다. 이 구분을 v3 에서 세웠다.

- **준비물** — 「전제 조건: … 정책을 skill 로 **써 둔다**」(`V3-05`), 「인프라: 오너와 문서화된
  source of truth 가 있는 정책 하나」(`V6-02`). 갖췄으면 **충실**. 그 스킬로 무엇을 했는지는 묻지 않는다.
- **작동** — 「이 과정은 … 조직의 skill 이 **이끈다**」(`V3-01`). 사슬이 돌아야 보이므로 **부분**.

「부분」 23 의 다수는 여전히 **문면은 갖췄고 그 위에서 돈 사슬이 아직 없다** 는 부류다.

### 인용에서 줄 번호를 뺐다

이 라운드가 드러낸 것은 줄 번호 자체가 유지보수 대상이라는 점이다. 검증 블록의 인용 267 곳이
줄 번호를 달고 있었고, 핀을 옮길 때마다 바뀐 파일로 간 것을 전부 다시 매겨야 했다. 핀이 있으면
그 일은 필요가 없다 — 위치는 인용문이 잡고, 번호는 `git grep -F "‹인용문›" ‹핀› -- ‹경로›` 가 준다.

결정적인 이유는 아래 「라운드 안 삽입」이다: **줄 번호는 조용히 틀릴 수 있고 인용문은 그럴 수 없다.**
그래서 인용 꼴을 `경로 + 축자 인용문` 으로 바꾸고 267 곳에서 줄 번호를 뺐다. 분량을 말하는 수
(`CODEOWNERS` 27줄)는 위치가 아니라 사실이므로 남겼다.

### 인용 정정 — 라운드 안 삽입이 만든 어긋남

핀 이동과 무관하게 v2 라운드 **안에서** 생긴 어긋남을 이 라운드가 걷어냈다. `docs/ADOPTING.md` 는
두 핀 사이에 줄이 하나도 밀리지 않았는데도, v2 후반 PR(#51·#52·#54)이 표 아래쪽에 행을 끼워 넣으면서
앞서 쓰인 블록의 `:27`·`:28` 인용이 뒤로 밀린 행을 가리키게 됐다. 아홉 블록을 실제 행으로 맞췄다
(`:28` reviewer · `:29` branch protection · `:30` UI · `:31` 비엔지니어 커밋 경로 · `:22` CODEOWNERS 사람).
같은 원인으로 `BOUNDARY.md:62→68`·`:76-78→80`, `plan/SKILL.md:38→41`·`:34-35→37-38`,
`design-spec/SKILL.md:20→24-25`, `README.md:29-32→31-33`·`:27→28` 을 정정했다.

## 최종 집계 (2026-09-09, 챕터 2~13 마지막 라운드 기준)

블록 179 · 충실 135 · 부분 24 · 팀 몫 20 · 보완 필요 0. 샘플 레포 반영 PR: #44 #45 #46 #47 #48 #49 #50 #51 #52 #53 #54 (main `0daf655`).
「부분」은 단일 계정·API 키 없음으로 이 검증에서 실행하지 못한 것(코드오너 승인 · required checks · evals/triage/진단 단계 · 다음 사슬에서 확인할 문면)이고, 「팀 몫」은 조직 정책·인프라(정책 스킬 · 승인 목록 · 배포·sandbox·MCP · 채널 유입 · 20~50 eval · /init)로 ADOPTING.md 에 자리가 적힌 것이다.
