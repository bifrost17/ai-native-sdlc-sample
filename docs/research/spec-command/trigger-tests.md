# trigger-tests — spec-command

헤드리스로 돌렸다. 판정 근거는 `claude -p … --output-format stream-json` 의 **도구 호출 기록**이다 —
`Skill` 도구로 `spec-policy-pass` 를 불렀는가(로드), 그리고 인용한 정책의 본문을 실제로 열었는가.
실행 원문 15건은 `raw/21-run-*.txt`, 산출 spec 9건은 `raw/22-output-*-spec.md`, 시험 판 구성은
`raw/21-fixtures.txt`. 모든 실행은 `--model claude-sonnet-5 --effort low --max-budget-usd 0.80`.

시험 판이 셋인 이유와 차이는 `raw/21-fixtures.txt` 에 있다. 요지: `base3` 은 intent 0011 이 `--no-ff`
머지로 main 에 들어온 이력을 갖는다. `base2` 에서 두 실행이 intent 본문의 `Status: draft` 만 보고
**스킬을 열기도 전에** 멈췄기 때문이다(아래 2회차). intent.md 본문은 어느 판에서도 손대지 않았다.

## 0. 기준선 (스킬 없음)

| # | 판 | 문구 | 로드된 스킬 | spec.md | 결과 |
|---|---|---|---|---|---|
| BASE-01 | base@2db39c6 | `/spec 0011-claim-status-notice` | `design-spec` | 씀 | 아래 두 흠 |

기준선은 P2·P3 를 잘 했다(일곱 절 다 채움, 우려 3건 실재, 결정자 지목, 스스로 해결 안 함). 흠 둘:
- **인용했으나 열지 않음** — `Skills applied:` 에 `secure-api-review@7c13202` 이 적혔는데 도구 호출
  전량에 그 파일의 Read 가 없다. sha 를 얻는 `git log` 만 있었다. 최종 응답은 "all opened before
  citing" 이라고 말했다. 넷 중 셋만 실제로 열렸다.
- **공백을 충돌로** — 외부 단축 URL 을 "compliance C1/C2(최소 노출)의 정신과 배치될 수 있다"고 적었다.
  C1 은 주민번호·계좌번호·연락처, C2 는 응답 필드 허용 목록 — 둘 다 단축 URL 을 다루지 않는다.
  같은 문서 다른 항목(야간 발송)에서는 공백과 위반을 옳게 갈랐다.

## 1. 1회차 — 트리거 문장 v1 (base2)

| # | 문구(요지) | `Skill` 로드 | 판정 |
|---|---|---|---|
| T1 | "요구·설계 spec 을 써 줘 … 못 지키는 지점은 분명히 적어 줘" | `design-spec` 만 | **실패** |
| T2 | "엔지니어링에 넘길 수 있게 spec.md 로 정리해 줘 …" | `spec-policy-pass` | 통과 |
| T3 | "Write the requirements and design spec for the accepted intent …" | `spec-policy-pass` | 통과 |

**2/3.** T1 은 `design-spec` 하나만 골랐다 — 둘이 같은 자리를 겨냥하는데 모델이 **하나만 고른** 것이다.
T3 은 산출까지 갔고, 그 spec 이 이 스킬이 노린 것을 그대로 보여 준다(`raw/22-output-T3-spec.md`):
스킬 8개 전량을 적용/미적용과 이유로 열거했고, 우려 6건을 충돌 1 · 공백 4 · 미확인 1 로 갈랐으며,
공백 행에 "정책 공백이지, 위반으로 단정하지 않는다"고 적었다. 90자 제약도 세어 "여유가 2자뿐"이라 적었다.

→ 고침 v2: 트리거 발화를 인용부호로 나열하고 "design-spec 을 대신하지 않고 그 위에 겹쳐 함께 쓴다"를 넣음.

## 2. 2회차 — 트리거 문장 v2 (base2) — 판이 오염돼 있었다

| # | 문구(요지) | `Skill` 로드 | 판정 |
|---|---|---|---|
| T1b | 1회차 T1 과 같은 문구 | `spec-policy-pass` | 통과(v1 실패 → v2 통과) |
| T2b | 1회차 T2 와 같은 문구 | **아무것도 안 부름** | 무효 |
| T3b | 1회차 T3 과 같은 문구 | `spec-policy-pass` | 통과 |
| T4b | "설계 문서를 만들어야 해 … 요구사항이랑 설계를 정리해 줘" | **아무것도 안 부름** | 무효 |

T2b·T4b 를 **실패가 아니라 무효**로 적는 이유: 둘 다 스킬을 고르는 데 실패한 것이 아니라, intent.md
본문의 `Status: draft` 를 보고 **과제 자체를 시작하지 않고** 되물었다. T2b 의 말: "The intent's status
is still `draft` … Per how design-spec/spec-policy-pass work, I shouldn't write spec.md against an
unaccepted intent." — 두 스킬 이름을 다 알고 있으면서 어느 것도 열지 않았다.

이것은 시험 판의 결함인 동시에 **템플릿 자체의 실재하는 모순**이다. `capture-intent` 는 "Does not change
`Status: draft`. Approval is the merge." 라 하고, `design-spec` 은 "It must be accepted — merged to
main. If it is still a draft … stop and say so." 라 한다. 그래서 **정상적으로 수락된 intent 는 영원히
본문에 `draft` 라고 적혀 있고**, 모델은 그것을 미수락으로 읽는다. 정책 오너에게 넘긴다(README 4번).

→ base3 을 만들어 수락을 git 이력(`--no-ff` 머지)으로 드러냈다. 본문 `Status:` 줄은 그대로 뒀다.

## 3. 3회차 — 트리거 문장 v2 (base3)

| # | `Skill` 로드 | spec.md | 판정 |
|---|---|---|---|
| T1c | `spec-policy-pass` | 씀 | 통과 |
| T2c | `spec-policy-pass` | 씀 | 통과 |
| T4c | `design-spec` 만 | 씀 | **실패** |

**2/3.** 판의 오염은 사라졌고(셋 다 끝까지 감), T4c 가 남았다. T4c 문구는 "설계 문서" · "요구사항이랑
설계" 로 `design-spec` 쪽에 더 가깝고 「정책」이라는 낱말이 아예 없다.

→ 고침 v3: 트리거 발화에 "설계 문서 만들어 줘" · "요구사항이랑 설계 정리해 줘" 를 더하고,
"**design-spec 이 걸리는 자리에서는 반드시 함께 건다** — 둘 중 하나를 고르는 것이 아니라" 로 강화.

## 4. 4회차 — 트리거 문장 v3 (base3) · 최종

| # | 문구 | `Skill` 로드 | spec.md | 판정 |
|---|---|---|---|---|
| T1d | "요구·설계 spec 을 써 줘 … 못 지키는 지점은 분명히 적어 줘" | `spec-policy-pass` | 씀 | **통과** |
| T2d | "엔지니어링에 넘길 수 있게 spec.md 로 정리해 줘 …" | `spec-policy-pass` | 씀 | **통과** |
| T3d | "Write the requirements and design spec for the accepted intent …" | `design-spec` + `spec-policy-pass` | 씀 | **통과** |
| T4d | "설계 문서를 만들어야 해 … 요구사항이랑 설계를 정리해 줘" | `spec-policy-pass` + `design-spec` | 씀 | **통과** |

**4/4.** 서로 다른 네 문구(한국어 셋 · 영어 하나)에서 매번 로드됐다. T3d·T4d 는 두 스킬을 **함께**
불렀다 — v3 이 노린 것이다.

## 5. 집합 시험 (명령 + 두 스킬을 한 프로젝트에)

| # | 문구 | 로드 | spec.md | 지시 충돌 |
|---|---|---|---|---|
| SET-01 | `/spec-policy 0011-claim-status-notice` | `spec-policy-pass` + `design-spec` | 씀 | **없음** |

`commands/spec-policy.md` · `skills/spec-policy-pass/` · 템플릿의 `commands/spec.md` ·
`skills/design-spec/` 를 한 프로젝트에 함께 넣고 같은 과제를 시켰다. 두 스킬이 같이 로드됐고 산출은
`design-spec` 의 뼈대(`templates/spec.md` 일곱 절 · `Upstream:` · `Status: draft` 유지 · 리뷰 질문)에
`spec-policy-pass` 의 표 둘(스킬 전량 열거 · 우려 4종)이 얹힌 꼴이다. 어긋난 지시는 나타나지 않았다.
`Skills applied` 에 `design-spec@…` 과 `spec-policy-pass@…` 까지 함께 적어 메타 스킬도 판으로 남겼다.

## 6. 무엇이 실제로 나아졌나 — 같은 과제, 같은 모델, 5회

**P4(공백 vs 충돌).** 기준선이 틀린 바로 그 항목(외부 단축 URL)을 4회차 4회 + SET-01, **5/5 모두**
「공백 · 조항 없음」으로 옳게 갈랐고, 여러 실행이 왜 공백인지까지 적었다 — 예: "조항 없음(C1/C2 는
단축 URL 을 다루지 않는다)"(T3d), "조항 없음(api-security S1~S8 어디에도 외부 리디렉션/단축 도메인
조항이 없다)"(SET-01). 「정신」으로 논증한 실행은 하나도 없었다.
충돌 행에는 양쪽 조항 ID 가 붙었다 — 예: "brand B4 · ux U2 · compliance C5 · intent 의 「문자 90자
제한」"(T3d). 결정 칸은 5/5 모두 비어 있다.

**수치 제약.** 5회 중 3회가 90자를 실제로 셌다 — "약 95자"(T1d), "링크(85자)"(T1d),
"EUC-KR 단문 SMS 는 보통 90byte≈한글 45자 … intent 의 「90자」가 문자 수인지 바이트인지"(SET-01).
기준선은 90자를 우려로 적기만 하고 세지 않았다.

**P1(연 것만 인용) — 개선했으나 완전하지 않다.** 4회차 5회 중 4회는 인용한 정책의 본문을 모두 열었다
(T2d·SET-01 은 `cat`, T3d·T4d 는 Read). **T1d 는 예외다**: `Skills applied:` 에 네 스킬을 적었는데
`.claude/skills/` 아래에서 연 것은 `secure-api-review` 뿐이고, brand·compliance·ux 는 sha 만
`git log` 로 얻었다. 대신 저장소 뿌리의 `policies/{brand,compliance,ux,api-security}.md` 를 Read 로
열었다 — 이 시험 판에서 스킬 본문은 그 정책 파일의 축자 사본이라 **내용은 다 본 셈**이지만, 연 것은
정책 파일이고 적은 것은 스킬 이름이다. 스킬의 description 이 금지한 "policies 파일을 직접 뒤지는" 길로
간 것이다.
→ 기준선(BASE-01)은 인용한 스킬의 **내용을 아예 보지 못한 채** 이름을 적었다. 4회차에서는 그런 실행이
없었다. 그러나 「연 스킬만 적는다」가 0 이 되지는 않았다. 이 시험 판에 `policies/` 가 함께 있었던 것이
그 길을 열어 준 면도 있다(실제 배포 프로젝트에는 `.claude/skills/` 만 간다). **확인 못 함**: `policies/`
가 없는 판에서도 같은 일이 생기는지는 돌려 보지 않았다.

## 6b. 배포 경로 시험 — 플러그인으로 로드되는가 (`--plugin-dir`)

앞의 시험은 모두 프로젝트의 `.claude/skills/` 에 파일을 두고 돌린 것이다. 이 저장소의 실제 배포 경로는
플러그인이므로(NOTES 4·S8 PR #1), 산출물을 프로젝트에서 **빼고** `--plugin-dir` 로만 얹어 다시 쟀다.
판은 `base4` = base3 에서 `skills/spec-policy-pass/`·`commands/spec-policy.md` 를 지운 것(수락 머지
이력은 보존). 플러그인 디렉터리는 이 레인의 저장소 뿌리(@5678ea9) — 즉 **머지된 다른 레인의 스킬 8종이
함께 얹힌 상태**다.

| # | 판 | 로드된 스킬 | spec.md | 결과 |
|---|---|---|---|---|
| PLUGIN-01 | base4(머지 이력 없음 — 판 결함) | `intent-sdlc-skills:spec-policy-pass` + `design-spec` | 안 씀 | **로드 확인**, 산출은 무효 |
| PLUGIN-02 | base4(머지 이력 보존) | `intent-sdlc-skills:spec-policy-pass` | 씀 | **통과** |

- **접두가 붙어 로드된다** — `intent-sdlc-skills:spec-policy-pass`. NOTES 2 대로 템플릿의 `design-spec`
  과 이름이 갈려 공존한다. 두 스킬 폴더명·명령 파일명이 다르므로 NOTES 1 의 합쳐짐도 일어나지 않았다.
- **PLUGIN-01 은 판 결함으로 무효다.** base4 를 만들 때 `.git` 을 새로 만들어 수락 머지 이력이 사라졌고,
  모델은 2절과 같은 이유로 과제를 시작하지 않았다. 이력을 보존해 다시 만든 것이 PLUGIN-02 다.
  (로드 여부만 놓고 보면 PLUGIN-01 에서도 스킬은 떴다.)
- **PLUGIN-02 는 끝까지 갔다.** 정책 스킬 넷을 모두 Read 로 열었고(P1 흠 없음), 우려 6건을
  충돌 1 · 공백 3 · 미확인 2 로 갈랐다. 외부 단축 URL 은 또 「공백」이고, 이번에는 왜인지까지 적었다 —
  "C1/C2 는 마스킹·응답 필드 허용 목록을 다루지 링크 서비스를 다루지 않는다". 결정 칸은 6/6 비어 있다.
- **다른 레인 스킬과 충돌하지 않았다.** 같은 세션에 `intent-sdlc-skills:{accessibility, claims-api-security,
  claims-ux-copy, claims-ux-interaction, pr-loop, secrets-scan, ux-copy}` 가 함께 올라와 있었는데
  어긋난 지시는 나타나지 않았다. 원문 `raw/23-run-PLUGIN-02.txt`, 산출 `raw/23-output-PLUGIN-02-spec.md`.

## 7. 실행 요약

| 회차 | 트리거 문장 | 통과 | 무효 | 실패 |
|---|---|---|---|---|
| 1회차 (base2) | v1 | 2 | 0 | 1 (T1) |
| 2회차 (base2) | v2 | 2 | 2 (판 오염) | 0 |
| 3회차 (base3) | v2 | 2 | 0 | 1 (T4c) |
| **4회차 (base3)** | **v3** | **4** | 0 | 0 |
| 집합 (base3) | v3 | 1 | 0 | 0 |
| 배포 경로 (base4, `--plugin-dir`) | v3 | 1 | 1 (판 결함) | 0 |

기준선 1회를 더해 총 **18회** 실행했다. 최종 판정은 **트리거 4/4 · 집합 1/1 · 배포 경로 1/1**.
