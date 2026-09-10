# brand — 트리거 시험

플레이북(스킬 레슨): "Test that the skill triggers. Ask Claude to do the relevant task in different
ways and confirm the skill loads each time."

## 어떻게 쟀나
- 임시 프로젝트 `/tmp/s2-proj` = 템플릿 레포 `bifrost17/ai-native-sdlc-sample@016705e` 사본(조사 당시 이름은 `intent-sdlc-sample`, 지금은 리다이렉트) +
  받아들여진 인텐트 `intent/0011-claim-status-sms/intent.md`(청구 상태 문자 통지, 커밋 `a94389a`) +
  `.claude/skills/` 에 이 레인의 스킬 설치. 템플릿 기본 스킬 4종(capture-intent · design-spec · plan ·
  secure-api-review)은 그대로 두고 함께 걸었다 — 집합 충돌을 같이 보기 위해서다.
- 하네스 `docs/research/brand/trigger-harness.sh`:
  `claude -p "<문구>" --output-format stream-json --verbose --max-turns 8 --setting-sources project
   --strict-mcp-config --permission-mode bypassPermissions`
  **로드 판정은 `Skill` 도구 호출의 `skill` 값**이다(파일을 `cat` 한 것은 로드로 세지 않는다).
- 원문은 `raw/` 에 그대로 있다. 머리 세 줄이 `CMD:` `AT_UTC:` `RC:` 이고 마지막 줄이 `LOADED_SKILLS:`.
- `RC:` 는 `claude` 의 종료 코드다. `rc=1` 이 로드 실패를 뜻하지 않는다 — 대부분 `--max-turns` 소진이다.
- **첫 실행(T1)만 하네스가 달랐다**: `--max-turns 4` 이고 `--permission-mode` 가 없다(그래서 rc=1 = 턴 소진,
  Bash 한 번이 권한으로 막혔다). T2 부터는 위 명령 그대로다. 각 파일의 `CMD:` 줄이 그 실행의 실제 명령이다.

## 1차: 설계분 초판 (description 고치기 전)

| # | 문구(자리) | 로드된 스킬 | rc | 원문 |
|---|---|---|---|---|
| T1 | PO 프롬프트 축자, 영어 — "…Apply the skills available to you so the plan conforms to our brand guidelines…"(spec 작성) | `brand` · `design-spec` · `secure-api-review` | 1 (max_turns) | `raw/20-trigger-T1.txt` |
| T2 | "청구가 보완요청 상태로 바뀐 고객에게 보낼 문자 문구를 한 건 써 줘."(고객 통지) | `brand` | 0 | `raw/21-trigger-T2.txt` |
| T3 | "포털 화면의 상태 배지 문구를 리뷰해 줘… 문자 초안 '홍길동님 축하합니다! …🎉' 도 같이"(UI 리뷰) | `brand` | 0 | `raw/22-trigger-T3.txt` |
| T4 | "Draft the customer email we send when a claim payout finishes…"(영어, 통지 작성) | `brand` | 0 | `raw/23-trigger-T4.txt` |
| T5 | "지급완료 안내 푸시 알림 문안 두 개만 잡아 줘. 길이는 40자 안쪽."(푸시) | `brand` | 0 | `raw/24-trigger-T5.txt` |
| **T6** | "intent/0011… 을 읽고 spec.md 초안을 잡아 줘. **우리 조직 스킬을 적용해서** … 무엇을 적용했는지만 알려 줘."(spec 작성, 한국어) | **없음 — 실패** | 0 | `raw/25-trigger-T6.txt` |
| T7 | "심사가 길어져서 기다리는 고객에게 사과 문자를 보내야 해. 문구 잡아 줘."(B3 자리) | `brand` | 1 (max_turns) | `raw/26-trigger-T7.txt` |

### T6 은 왜 실패했나
모델이 `Skill` 도구를 부르는 대신 **`ls .claude/skills/` 와 `cat SKILL.md` 로 파일을 뒤졌다**(원문의 도구
호출 기록). 본문은 결국 `brand` 의 규칙대로 판정했지만 스킬은 「로드되지 않았다」. 이것은 S8 이 이미 실측한
실패 꼴이다(`docs/work/NOTES.md` 3: 「organization skills are loaded?」 문구에 모델이 스킬 대신 파일을 뒤졌다).
초판 description 의 부정 지시는 「사용자에게 스타일 가이드를 묻지 말라」까지였고, **「스킬 목록을 뒤지지 말라」가
없었다.**

### 고친 것 (트리거 문장 한 곳)
`skills/brand/SKILL.md` 의 `description` 에 두 문장을 더했다.
- 자리 추가: `Also use when asked which organization skills apply to customer copy, or whether a draft is on-brand.`
- 부정 지시 확장: `…instead of listing or reading files under .claude/skills to work out what the policy is
  — the transcribed policy is inside this skill.`

## 2차: 고친 뒤 (최종판 · 채택 집합 = `brand` + `stop-slop-ko`)

| # | 문구(자리) | 로드된 스킬 | rc | 원문 |
|---|---|---|---|---|
| T6b | T6 과 **같은 문구** | `brand` · `design-spec` · `secure-api-review` | 0 | `raw/27-trigger-T6b.txt` |
| P2 | "청구가 보완요청 상태로 바뀐 고객에게 보낼 문자 문구를 한 건 써 줘." | `brand` | 0 | `raw/40-final-P2.txt` |
| P3 | "포털 화면의 상태 배지 문구를 리뷰해 줘: '처리중', '완료', '서류미비'." | `brand` | 0 | `raw/41-final-P3.txt` |
| P4 | "Draft the customer email we send when a claim payout finishes…"(영어) | `brand` · `stop-slop-ko` | 0 | `raw/42-final-P4.txt` |
| SS2 | "이 문단 AI가 쓴 티가 심해. 자연스럽게 윤문해 줘: …"(윤문) | `stop-slop-ko` · `brand` | 0 | `raw/44-final-SS2.txt` |
| SS3 | "청구 안내 페이지에 올릴 소개 글을 새로 써 줘. 판에 박힌 문장 말고."(생성) | `brand` · `stop-slop-ko` | 1 (max_turns) | `raw/45-final-SS3.txt` |

**`brand` 6/6 · `stop-slop-ko` 3/3**(P4 · SS2 · SS3; 집합 시험 S3 을 더하면 4/4).
서로 다른 문구 · 서로 다른 자리 · 한국어와 영어 양쪽에서 매번 로드됐다.

## 집합 시험 (같은 과제를 여러 스킬을 함께 걸고 한 번 더)

| # | 걸어 둔 스킬 | 문구 | 로드 | 어긋난 지시가 있었나 | 원문 |
|---|---|---|---|---|---|
| S1 | `brand` + `stop-slop-ko` + `brand-review` + 템플릿 4종 | 상태 배지 · 문자 초안 리뷰(T3 과 같은 문구) | `brand` 만 | 없음. 조항 번호 표로 판정하고, 배지 3종 대 어휘 5종 문제를 **스스로 Flagged concerns 로 올렸다** | `raw/30-set-S1.txt` |
| S2 | 같음 | "Review this customer email copy against our brand guidelines and style guide before it ships…"(영어) | `brand` 만 | 없음 | `raw/31-set-S2.txt` |
| S3 | 같음 | "이 고객 안내문 AI 티가 나는데 자연스럽게 다듬어줘: '…처리중에 있으며… 최고의 서비스로 보답하겠습니다!'" | `stop-slop-ko` + `brand` | **없음** — 두 스킬이 같은 방향으로 붙었다: `처리중`→`심사중`(B4), `최고의` 삭제(B1), 느낌표 삭제(B7), 「이를 통해」 삭제(slop) | `raw/32-set-S3.txt` |
| S4 | 같음 | "Audit our product launch blog post against our messaging pillars…"(마케팅 감사) | `brand-review` 만 | 해당 없음 | `raw/33-set-S4.txt` |

### 교차 레인 집합 시험 (S4 의 UX 스킬과 함께)
`main` 이 S4(ux) 를 머지한 뒤 한 번 더 걸었다 — `brand` + `stop-slop-ko` + S4 의 `claims-ux-copy` ·
`ux-copy` · `accessibility` + 템플릿 4종.

| # | 문구 | 로드 | 어긋난 지시가 있었나 | 원문 |
|---|---|---|---|---|
| S5 | "청구 상태 화면의 문구를 잡아 줘. 상태 다섯 가지 각각에 라벨과 설명 한 줄씩, 그리고 보완요청일 때 보여 줄 안내 문구." | `claims-ux-copy` · `brand` | **없음.** 두 스킬이 자기 자리를 지켰다 — 라벨은 B4 의 다섯 낱말 그대로, 각 상태에 U2 가 요구하는 「다음 예정」 한 줄. 금액 `1,250,000원`·날짜 `2026-09-24`(B6), 호칭 「{홍길동} 고객님」(B7), 느낌표·이모지 0. 모르는 값은 지어내지 않고 `‹… — 사정팀›` 으로 남겼다 | `raw/46-set-S5-crosslane.txt` |

S4 의 `claims-ux-copy` 는 본문에 "If no skill in this repo carries the brand clauses yet, read
`policies/brand.md` itself before you write customer-facing words" 라고 적어 두었다 — 이 레인이 그 자리를
채운다. 실측에서 두 스킬은 서로를 조항 번호로 가리키며 붙었다(답변 첫 줄: "`brand`(B1–B7)와
`claims-ux-copy`(U1·U2·U3) 정책대로 잡았습니다").

### 집합 시험이 바꾼 결정 셋
1. **`brand-review` 를 기각했다.** 우리 자리(고객 통지 · 상태 배지 리뷰)에서 2/2 로드되지 않았고(S1 · S2),
   마케팅 블로그 감사에서만 로드됐다(S4) — 정책 대상(`청구 상태 조회 서비스와 그 고객 통지`) 밖이다.
   로드되지 않는 통제는 통제가 아니다. **T6**(`raw/25-trigger-T6.txt` — 스킬을 부르는 대신 파일을 뒤진
   그 실행이다) 에서 모델이 파일을 읽고 스스로 적은 이유도 같다:
   "조직 정책이 붙어 있지 않은 범용 스킬이라… `brand` 가 '묻지 말고 이걸 쓰라'고 명시하고 있어
   B1~B7 밖의 어조 규칙이 섞일 위험만 있습니다."
2. **`check-brand-copy.sh` 의 B4 정규식을 고쳤다.** S1 에서 단독 `완료` 가 그물을 빠져나갔다.
   `(^|[^급])완료`·`종료`·`마감` 을 더했고 `지급완료`·`종결` 은 여전히 통과한다(`raw/13-checker-run.txt`
   뒤에 이어 붙인 재확인). **그 시점의 「오탐 0」은 두 줄짜리 픽스처만 본 것이었다** — 뒤에 적대 검토가
   오탐 12건을 찾아냈고, 예외 규칙을 넣어 다시 쟀다(아래 「적대 검토가 바꾼 것」).
3. **스킬 안의 경로 두 곳을 고쳤다.** S1 이 짚었다 — 스크립트 경로가 배포 위치(`.claude/skills/brand/`)와
   달랐고, 정본 `policies/brand.md` 가 이 스킬을 쓰는 레포에는 없을 수 있다. 둘 다 문장을 고쳤다.

## 적대 검토가 바꾼 것 (스킬을 깨 보라고 시킨 뒤)
다 쓴 뒤 다른 세션에 「이 레인을 깨 보라」고 시켰다(정책 대조 · 주장 대 증거 · 채택분 무결 · 체커 ·
coverage · 범위). 21건이 나왔고 전부 고쳤다. 시험과 관련된 것만 적는다.

| 무엇 | 어떻게 고쳤나 |
|---|---|
| 체커가 **grep 실패를 초록으로 냈다** — `-` 로 시작하는 파일명에서 `grep: invalid option`(rc=2)이 `2>/dev/null` 로 삼켜지고 「걸린 것 없음 rc=0」이 나왔다 | `--` 를 붙이고 rc≥2 를 실패로 갈라 rc=2 로 멈추게 했다. 이진 파일도 조용한 초록 대신 rc=2 로 거절한다 |
| 정상 문구 12줄이 오탐으로 걸렸다(영업 종료 · 마감일 · 본인인증 완료 · IP `192.168.0.1` · 버전 `14.2.3` · `a != b` · `#!/usr/bin` · 마크다운 이미지 · 진행률 100% · 근거 조항을 병기한 「즉시」…) | 조항마다 **예외 패턴**을 넣었고(Vale 의 `exceptions` 를 본떴다), 느낌표는 `[가-힣] ?!` 로 좁혔으며, 점 찍은 날짜는 IP·버전과 구분할 수 없어 **보지 않기로 하고 스크립트 머리에 적어 뒀다** |
| 위반 8종이 그물을 빠져나갔다(반려 · 추가요청 · 청구중 · `진행 중` 띄어쓰기 · 천 단위 없는 `1250000원` · `2026/09/10` · `1,250,000 KRW` · ⭐⚠♥➡㊗) | 패턴을 넓혔다. 이모지는 바이트 앞머리를 11개로 늘렸다 |
| 「오탐 0」을 두 줄 픽스처로 주장했다 | 적대 검토가 든 12줄을 그대로 픽스처로 만들어 다시 쟀다 — `raw/15-fixture-legit.txt`(정상 15줄, 오탐 0) · `raw/15-fixture-violations.txt`(위반 18줄, 18건 전부 검출) · 가장자리 8경우. 실행 원문 `raw/15-checker-run-v2.txt` |

검토 뒤 최종판으로 한 번 더 걸었다: P6 "지급이 끝난 고객에게 보낼 문자 문구와, 화면에 보일 상태
라벨을 같이 잡아 줘." → `brand` · `claims-ux-copy` 로드, rc=0(`raw/47-final-P6-afterreview.txt`).
**`brand` 7/7 · `stop-slop-ko` 3/3.**

## 음성 대조 (물리지 말아야 할 자리)
`raw/43-final-P5-negative.txt` — "Audit our product launch blog post…"(영어 마케팅 문구, 정책 대상 밖).
**`brand` 가 로드됐다.** 해롭게 굴지는 않았다: 조항을 그대로 적용해 `the best`·`perfect`(B1),
`instant`(B2)를 잡았고, **자기 체커가 한국어 전용이라 영어 문구에 낸 초록은 뜻이 없다고 스스로 밝혔다**
("Every pattern in that script is Korean… so it slid past a checker that would have flagged all three").
다만 마케팅 문구가 B1~B7 대상인지는 정책이 답하지 않았다 → `README.md` 「정책 오너에게 묻는다」 4번.

## 확인 못 한 것
- 플러그인 배포 경로(`--plugin-dir` · 마켓플레이스)로는 시험하지 않았다. 이 레인은 `.claude/skills/` 설치
  기준으로만 쟀다. 플러그인 접두(`intent-sdlc-skills:brand`)에서의 로드는 S8 의 자리다(`docs/work/NOTES.md` 2 · 4).
- 대화형(비헤드리스) 세션에서의 로드는 재지 않았다.
- `composio-qa-response` 는 `disable-model-invocation: true` 라 트리거 시험 자체가 불가능했다.
