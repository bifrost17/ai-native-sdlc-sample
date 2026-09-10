# 트리거 시험 — compliance (S3)

하네스: Claude Code **2.1.265**, `claude -p … --output-format stream-json --verbose`.
임시 프로젝트: 템플릿 레포 `bifrost17/ai-native-sdlc-sample@016705e` 사본(`/tmp/s3-trigger/t1`)에
설계한 스킬 둘을 `.claude/skills/` 로 넣고, 시험용 accepted intent `0011-claim-status-notify` 를 심었다.
그 프로젝트에는 템플릿의 스킬 넷(`capture-intent`·`design-spec`·`plan`·`secure-api-review`)이 그대로 있다 —
**우리 스킬만 있는 무균 상태가 아니라, 실제 배치 상태에서** 시험했다.

(레포는 조사 중 `intent-sdlc-sample` 에서 `ai-native-sdlc-sample` 로 이름이 바뀌었다 — 옛 URL 은 리다이렉트된다.
`raw/` 의 명령 원문에는 **그때 실제로 친 옛 이름이 그대로** 있다. 원문은 고치지 않는다.)

러너 `trigger-test.sh`(이 폴더). 원문은 `raw/10-trigger-*.txt`(claim-data-compliance),
`raw/11-trigger-*.txt`(claim-notice-compliance), `raw/12-trigger-1.txt`(집합), `raw/13-set-test-spec-output.txt`
(집합 시험 산출물). 각 파일 머리 세 줄이 `CMD:` `AT_UTC:` `RC:` 다.

## 무엇을 「로드됐다」로 셌나
처음에는 `Skill` 도구 호출만 셌는데, **집합 시험에서 모델이 `Skill` 도구를 한 번도 부르지 않고
`cat` 으로 SKILL.md 를 읽어 적용했다**(12번). 도구 호출만 세면 이 판을 「미로드」로 잘못 적을 뻔했다.
러너를 고쳐 **`Skill` 도구 호출 · `.claude/skills/<name>` 경로가 보인 모든 흔적**을 함께 센다.
아래 「Skill 도구」와 「파일로 열림」 두 열이 그것이고, 10·11번은 재실행이 아니라 **저장된 원문을 다시 센 것**이다.

## claim-data-compliance — 문구 3종
| # | 문구 | rc | Skill 도구 | 파일로 열림 | 판정 |
|---|---|---|---|---|---|
| 10-1 | 청구 상태 조회 API 의 응답 필드를 설계해 줘. 고객 포털에서 쓸 거야. | 1 | `claim-data-compliance` | 6종 전부 열어 봄 | **PASS** |
| 10-2 | Add a lookup endpoint so a call-centre agent can check a customer's claim status on their behalf. What do I need to get right? | 0 | `claim-data-compliance`, `secure-api-review` | data·notice·secure | **PASS** |
| 10-3 | 우리 청구 조회 서비스에 로깅을 붙이려고 한다. 무엇을 남기고 무엇을 남기면 안 되나? | 0 | `claim-data-compliance` | data·secure | **PASS** |

**3/3.** 한국어·영어, 그리고 「응답 필드 설계」·「대리 조회 경로」·「로깅」이라는 서로 다른 자리에서 모두 걸렸다.
10-2 는 `secure-api-review` 와 **함께** 떴다 — 노린 결과다(대리 조회는 두 정책이 만나는 자리).

**10-1 의 `rc=1` 은 스킬 실패가 아니다.** `--max-turns 6` 에 걸려 하네스가 비정상 종료 코드를 냈고,
스킬은 그 전에 로드돼 적용됐다. 빨간 rc 를 초록이라 적지 않기 위해 여기 남긴다.

## claim-notice-compliance — 문구 3종
| # | 문구 | rc | Skill 도구 | 파일로 열림 | 판정 |
|---|---|---|---|---|---|
| 11-1 | 청구 상태가 바뀌면 고객에게 보내는 SMS 문구를 써 줘. | 0 | `claim-notice-compliance` | notice | **PASS** |
| 11-2 | We need to email the customer when their claim moves to 'under review'. Draft the message and tell me how to decide whether to send it. | 0 | `claim-notice-compliance` | notice | **PASS** |
| 11-3 | 통지 발송 경로를 설계 중이다. 어떤 고객에게 어떤 채널로 보낼지 정하는 규칙이 필요해. | 0 | `claim-notice-compliance` | notice | **PASS** |

**3/3.** 「문구를 써 줘」(카피)·「보낼지 판단」(동의)·「채널 규칙」(경로 설계) 세 자리에서 모두 걸렸다.
**합계 6/6.** 트리거 문장을 고쳐 다시 돌린 적은 없다 — 첫 판에 6/6 이었다.

## 집합 충돌 시험 (12번)
두 스킬 + 템플릿 스킬을 **함께** 넣고 둘 다 걸리는 과제 하나를 시켰다:

> intent/0011-claim-status-notify/intent.md 를 읽고 spec 을 써 줘. 우리 조직의 스킬을 모두 적용해서,
> 청구 상태 조회 API 와 고객 통지까지 포함해라.

`rc=0`, 13턴. **네 스킬이 함께 적용됐다** — 산출된 spec.md 의 `Skills applied:` 줄이
`design-spec@016705e, claim-data-compliance@f993c28, claim-notice-compliance@f993c28, secure-api-review@016705e`
다(원문 `raw/13-set-test-spec-output.txt`).

**지시가 어긋나지 않았다.** 확인한 자리:
- **C3 × `secure-api-review` 4항** — 모델이 둘을 충돌로 다루지 않고 "C3 은 같은 자리를 audit 이벤트까지
  넓힌다"로 합쳤다. `claim-data-compliance` 가 우선순위를 못박은 대로다.
- **C6 × `secure-api-review` 3항** — 스스로 구분했다: "이 chain 에는 상태를 바꾸는 엔드포인트가 없다 …
  읽기 경로의 이력은 C6 이 따로 요구하는 것". 두 스킬을 섞어 조회 이력을 빠뜨리지 않았다.
- **두 스킬의 경계** — 응답 필드·이력·로그는 data 쪽, 동의·본문은 notice 쪽으로 갈렸고 중복 서술이 없다.
- **애매한 자리에서 스킬이 시킨 대로 멈췄다** — intent 의 열린 질문(지급 예정 금액을 통지에 넣는가)에
  답을 지어내지 않고 「덜 싣는 쪽」을 기본값으로 두고 정책 오너에게 carried forward 했다.
- 모델이 **마케팅 관행을 끌어오지 않았다** — "구독 해지 문구로 발송 근거를 만들거나 … 추가 상품을
  권유하지 않는다"를 spec 에 그대로 옮겼다. 기각한 후보 4종의 가장 흔한 오발을 막으려던 문장이 작동했다.

## 남는 것 · 확인 못 한 것
- **플러그인 배치(`--plugin-dir`)로는 시험하지 않았다.** 여기 6+1 판은 전부 `.claude/skills/` 직접 배치다.
  S8 이 실측한 접두(`/intent-sdlc-skills:<name>`)와 이름 충돌 규칙은 반영했다(아래) — 그러나
  **플러그인으로 로드했을 때도 6/6 인지는 확인 못 함.**
- **이름 충돌은 피했다.** S8 발견 1(스킬 폴더명과 명령 파일명이 같으면 합쳐진다)에 따라,
  두 이름 `claim-data-compliance`·`claim-notice-compliance` 는 이 레포가 만들 명령
  (S6 의 `spec`)과 겹치지 않는다. 겹침 여부는 이름을 비교해 확인했을 뿐, 플러그인으로 로드해 재현하지 않았다.
- **한 판은 한 세션이다.** 같은 문구를 여러 번 돌렸을 때의 편차는 재지 않았다 — 문구마다 1회씩,
  스킬마다 서로 다른 문구 3개다(COMMON 의 「서로 다른 문구로 최소 셋」).
- 12번의 spec 이 든 「F6 `policies/api-security.md` 부재」는 **시험 픽스처 탓**이다. 임시 프로젝트에
  `policies/compliance.md` 만 복사했다. 이 레포에는 그 파일이 있다.
