# PROVENANCE — claims-ux-copy (설계분)

이 스킬은 **직접 설계**했다. 기존 스킬 중 U2·U3 를 덮는 것을 (라이선스가 깨끗한 범위에서) 찾지 못했고,
U1 을 덮는 것은 있었지만 한국어 청구 도메인의 문면까지 가지 않았기 때문이다 — 후보 30여 건의 정독과
판정은 `docs/research/ux/candidates.md`, 빈칸의 이유는 `docs/research/ux/coverage.md` 에 있다.

## 본문의 출처
- **정책 원문**: `policies/ux.md` 의 U1·U2·U3 를 조항 ID 와 함께 인용부호로 옮겼다. 인용 밖의 문장은
  그 조항을 문구·spec 에서 어떻게 확인하는지만 적는다 — 스킬은 정책을 옮기지 만들지 않는다.
- **다섯 어휘**(접수 · 심사중 · 보완요청 · 지급완료 · 종결)는 `policies/brand.md` 의 **B4** 가 정본이고,
  U2 가 그것을 가리킨다. 이 스킬은 두 조항의 관계를 한 줄로 밝히고 어휘를 되풀이하기만 한다.
- **형식**: 플레이북 「Skills as institutional knowledge」 레슨의 SKILL.md 꼴(frontmatter `name`·`description`,
  본문은 무엇을 할지) — 레슨 원문 요지는 `docs/research/ux/raw/40-lesson-notes.txt`.
  마지막 절 「In your summary」는 같은 레포의 `claims-api-security` 와 꼴을 맞췄다(한 답에서 한 형식으로 보고하도록).

## 참고한 것 (문장을 옮기지 않고, 착상만)
아래는 정독한 후보에서 가져온 착상이다. 어느 것도 문장을 그대로 옮기지 않았다 — 정책 문면이 정본이고,
전사에는 라이선스 의무가 따라붙기 때문이다. sha 는 정독 시각의 값이다.

| 착상 | 어디서 | 이 스킬의 어디에 |
|---|---|---|
| 오류 문면을 「무엇 + 왜 + 다음 행동」의 **순서 있는 형(型)** 으로 고정한다 | anthropics/knowledge-work-plugins `ux-copy` `@2d6f7e2` (Apache-2.0) — 채택분으로 함께 들어 있다 | U1 절의 세 요소를 순서대로 확인하게 한 부분 |
| 「왜」는 **알 수 있을 때만** 적고 모르면 비운다(추측 금지) | cuellarfr/design-skills `ux-writing/templates/error-message-template.md` `@b41750a` (MIT) 의 `[Why it might have failed, if known]` 구조 | U1 의 「원인을 짐작해 쓰지 않는다」 |
| 오류 문면에서 **내부 코드·예외 이름**을 걷어내되 로그에는 남긴다 | content-designer/ux-writing-skill `templates/error-message-template.md` `@a9fba52` (MIT) 의 기술/사람 말 대조 | U1 의 금지 목록과 「로그·감사에는 남기되 화면에는 넣지 않는다」 |
| 대기 문구에 **예상 시간을 수치로** 적는다("보통 N분") | talkstream/ru-text `references/ux-writing.md` `@60abab9` (MIT) 의 장시간 작업 규칙 | U3 의 「예상 시간」 |
| 대기가 길어질수록 진행·취소·소요 안내를 달리한다(지속시간 구간표) | szilu/ux-designer-skill `references/22-performance-ux.md` (MIT) · cuellarfr `interaction-design/references/error-prevention.md` (MIT) | U3 에서 「어디서 온 수치인지 근거를 남기라」고 요구한 이유 |
| 실패 분기를 **빠짐없이 열거**해 각각의 문면을 쓰게 한다 | 기준선 `secure-api-review`(항목별 확인)와 같은 레포 `claims-api-security` 의 「적지 못하면 done 이 아니다」 꼴 | U1 마지막 문단(조회 실패·권한 없음·없음·타임아웃·첨부 실패·세션 만료) |

**U2 는 참고한 곳이 없다.** 조사한 어느 스킬도 도메인 상태 어휘를 고정하지 않았다(`coverage.md` 「빈칸과 이유」).
다섯 어휘와 「다음 예정」은 정책 U2·B4 에서만 왔고, 상태별 「다음 예정」의 예시(접수→심사 시작, 보완요청→
무엇을 언제까지)는 정책 U2 의 괄호 예시(「보완요청 → 무엇을 보내야 하는지」)를 각 상태로 편 것이다.

## 일부러 따르지 않은 것
- **로딩 문구를 말줄임표로 끝내라**(vercel-labs/web-interface-guidelines `command.md` `@e3d624b`:
  `Loading states end with "…"`). U3 은 「잠시만 기다려 주세요」류 단독 표시를 금지하므로, 시간이나
  확인 시점 없는 `저장 중…` 은 이 조직에서는 충분하지 않다.
- **유머러스한 로딩 문구**(szilu `09-ux-writing.md` 의 `Reticulating splines…`). 브랜드 B1(과장·감탄 없음)과
  대상(보험 청구)에 맞지 않는다.
- **느낌표를 쓰는 성공 문구**(szilu 의 `Order placed! We'll email you when it ships.`). 브랜드 B7(이모지·느낌표 미사용).
- **어조·문체 규정**(토스 계열 3종의 해요체 강제, `Avoid mixing formal styles like 합니다, 하십시오`).
  어조는 `policies/brand.md`(B1)와 S2 의 스킬 소관이다. 이 스킬은 문면의 **구성**만 다룬다.
- **화면 밖 채널의 문안 템플릿**(알림톡·이메일 본문 전체 꼴). 정책에 근거 조항이 없다 — U3 에서 채널과
  시점을 밝히라는 데까지만 간다.

## 라이선스
`SKILL.md` 와 이 파일은 이 레포의 것이다. 위 표의 착상 제공자에게서 **문장을 옮기지 않았으므로**
그들의 라이선스 의무(MIT·Apache-2.0 의 고지)가 이 스킬에 붙지 않는다. 나중에 그 문장을 그대로 쓰려면
표시와 라이선스 사본을 달아야 하고, 그때는 정책 오너에게 먼저 묻는다.

## 트리거
`docs/research/ux/trigger-tests.md` — 문구 3종 3/3 로드(raw/20·21·22), 집합 시험 포함. 트리거 문장을 고친 적은 없다.
