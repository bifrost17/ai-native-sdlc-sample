---
name: claim-data-compliance
description: Apply the organization's compliance policy to claim data on the wire, in logs and in the access trail. Use whenever writing or reviewing a spec.md, designing or changing an endpoint or its response fields, writing a query or DTO that reads claim or customer data, adding logging, error handling or audit events, or building a lookup path for a call-centre agent or an adjuster. Covers policy clauses C1, C2, C3, C6, C7. Apply this instead of deciding field, log or retention questions from general privacy knowledge.
---
<!-- 정본: policies/compliance.md v0 (Status: draft — 오너 서명 대기). 이 스킬은 정책을 옮긴다. 조항 문면이 정본과 다르면 정본이 이긴다. -->
<!-- L6: "write a skill for institutional knowledge that must be applied consistently". L6: "A skill is a control, though an advisory one." -->

# Claim data compliance

대상: 보험 청구 상태 조회 서비스(고객 포털 · 사정인 · 상담사 경로). 고객 통지 본문·발송은
`claim-notice-compliance` 가 맡는다 — 이 스킬은 **데이터 · 로그 · 이력**만 본다.

## C1 — 식별번호는 통째로 내보내지 않는다
> **C1** 주민등록번호·계좌번호·연락처 전체는 어떤 응답·화면·통지에도 싣지 않는다. 필요하면 마스킹(뒤 4자리 등)만.

- 응답 · 화면 · 통지 어디에도 주민등록번호, 계좌번호, 연락처 **전체 값**을 쓰지 않는다.
- 내보내야 할 자리가 있으면 마스킹된 값만 — 뒤 4자리(`****-1234`)가 기본이다.
- 마스킹은 **경계에서** 한다. 상류(claims-core)에서 전체 값이 오더라도 응답 DTO 를 만들 때 자른다.
  화면단 CSS·프런트 포맷팅으로 가리는 것은 C1 을 만족하지 않는다 — 값이 이미 나갔다.
- 정렬·검색·조인 키로 전체 값이 필요하면 내부 ID 로 바꿔서 쓴다.

## C2 — 응답 필드는 허용 목록
> **C2** 응답 필드는 허용 목록으로 — 필드를 더할 때 그 근거 조항을 spec 에 적는다.

- 응답 스키마는 **내보낼 필드를 열거**한다. 상류 응답이나 도메인 객체를 그대로 직렬화하지 않는다
  (`SELECT *`, 엔티티 그대로 반환, 스프레드 `...claim` 금지). 읽기 전용 응답 모델을 따로 둔다.
- 필드를 **하나 더할 때마다** spec.md 에 그 필드가 왜 필요한지와 근거 조항을 적는다.
  spec 에 없는 필드는 응답에 없다.
- 역할마다 목록이 다르다: 고객 · 상담사 · 사정인이 같은 필드를 볼 이유가 없으면 목록을 나눈다.

## C3 — 로그·오류·audit 에 PII 를 넣지 않는다
> **C3** 로그·오류 메시지·audit 이벤트에 PII 를 넣지 않는다(식별자는 청구 번호·내부 ID 만).

- 로그·오류 메시지·audit 이벤트에 쓸 수 있는 식별자는 **청구 번호와 내부 ID** 뿐이다.
  이름 · 주민등록번호 · 계좌번호 · 연락처 · 이메일 주소는 마스킹한 형태라도 넣지 않는다.
- 요청/응답 **본문 전체를 로그로 찍지 않는다**. 무엇이 일어났는지를 기록하고 값은 기록하지 않는다.
- 고객에게 돌려주는 오류 메시지에는 상관관계 ID 만 싣는다. 자세한 것은 서버 쪽에 남긴다.
- URL 경로·질의 문자열에 개인정보를 넣지 않는다 — 접근 로그·브라우저 이력에 그대로 남는다.
- 이 조항은 `secure-api-review` 4항("fields tagged pii in the schema must never appear in logs or
  error messages")과 같은 자리를 덮는다. 둘이 어긋나면 `secure-api-review` 가 정본이고, 여기서는
  대상이 로그·오류에 더해 **audit 이벤트까지** 넓다는 점만 더한다.

## C6 — 조회·통지 이력
> **C6** 조회·통지 이력은 누가(역할·ID) · 무엇을(청구 번호) · 언제(UTC) 로 기록하고 보존 기간은 3년.

- **조회도 기록한다.** 상태를 바꾸지 않는 단순 조회에도 이력을 남긴다 — `secure-api-review` 3항의
  audit 이벤트는 상태를 바꾸는 엔드포인트만 덮으므로, 읽기 경로는 이 조항이 따로 요구하는 것이다.
- 한 줄에 세 가지가 있어야 한다: **누가**(역할 + ID) · **무엇을**(청구 번호) · **언제**(UTC).
- 시각은 UTC 로 저장한다. 현지 시각·오프셋 없는 시각은 안 된다.
- 보존 기간은 **3년**. 로그 순환·보존 정책을 짤 때 이 이력을 3년 미만으로 지우는 설정을 넣지 않는다.
- 「누가」는 C3 을 지켜 내부 ID·역할로 적는다. 이름이나 이메일로 적지 않는다.

## C7 — 대리 조회
> **C7** 제3자(상담사·사정인)의 대리 조회는 본인확인 기록이 있을 때만, 그 기록 ID 를 함께 남긴다.

- 상담사·사정인이 **고객 대신** 조회하는 경로는 본인확인 기록이 있을 때만 열린다.
  기록이 없거나 확인할 수 없으면 조회를 **거절**한다 — 통과시키고 나중에 기록하지 않는다.
- 그 경로의 이력에는 C6 의 세 가지에 더해 **본인확인 기록 ID** 를 함께 남긴다.
- 본인확인 기록 ID 자체는 식별자이므로 이력에 남겨도 C3 에 어긋나지 않는다. 확인에 쓴 값
  (고객이 불러 준 생년월일·주소 등)은 남기지 않는다.

## 어긋남을 만나면
정책끼리 부딪히거나 이 스킬로 답이 안 나오면 **스스로 정하지 않는다.** spec.md 의
「Flagged concerns」에 무엇이 부딪히는지와 누가 정해야 하는지를 적는다(`design-spec` 스킬과 같은 규칙).
정책 자체를 고쳐야 한다고 보이면 정책 오너에게 올린다 — 이 스킬을 고쳐서 해결하지 않는다.

## 이 스킬이 하지 않는 것
- 고객 통지 본문·발송 동의(C4 · C5)는 다루지 않는다 → `claim-notice-compliance`.
- 인증·입력 검증·상류 호출 예산 등 보안 조항은 다루지 않는다 → `secure-api-review`,
  `policies/api-security.md`.
- 정책을 만들거나 고치지 않는다. 문면이 정본과 어긋나면 `policies/compliance.md` 가 이긴다.
