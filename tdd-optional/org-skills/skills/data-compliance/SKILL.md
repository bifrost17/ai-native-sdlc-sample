---
name: data-compliance
description: Apply the team's data-handling policy to credentials, personal data, logs and the access trail. Use whenever writing or reviewing a spec.md, designing or changing an endpoint and its response fields, writing a query or DTO, adding logging or audit events, or wiring anything that leaves the service. Covers team clauses C1-C3 and defers sensitive-field and retention values to the project's PROJECT-POLICY.md slots P2 and P3. Apply this instead of deciding logging, field or retention questions from general privacy knowledge.
---
<!-- 정본: policies/compliance.md (팀 조항 C1~C3) · 프로젝트 값: PROJECT-POLICY.md 슬롯 P2 · P3.
     전제: 사내 임직원용 소프트웨어. 사외로 나가는 것이 있으면 P3 이 규칙을 갖는다.
     이 스킬은 법·규제를 해석하지 않는다. -->

# 데이터 취급 — 팀 조항

먼저 그 프로젝트의 `PROJECT-POLICY.md` 의 **P2**(민감 데이터 · 보존 기간)와 **P3**(사내 전제를 벗어나는 것)을 연다.
값이 비어 있으면 **지어내지 말고** spec 의 Flagged concerns 로 올린다. 보존 기간·통지 의무 같은 수치는 P2·P3 에 근거와 함께 적힌 것만 쓴다.

## C1 자격증명은 어디에도 두지 않는다
- 토큰 · 키 · 비밀번호 · 접속 문자열을 코드 · 설정 · 로그 · 화면 · diff 에 두지 않는다.
- 값을 말해야 할 때는 길이와 해시 앞자리까지만. 말줄임 축약도 유출이다.
- 스캔은 `secrets-scan` 이 맡는다 — 이 조항은 「애초에 쓰지 않는다」쪽이다.

## C2 민감 데이터는 필요한 자리에만
- P2 가 민감이라 한 것은 필요한 경로에만 두고, 로그 · 오류 메시지 · 감사 이벤트에는 **내부 ID** 만 남긴다.
- 예외를 통째로 찍지 않는다 — 요청 본문 · 헤더 · 쿼리 파라미터가 함께 나간다.
- 엔티티를 그대로 반환하지 않는다(`SELECT *` · 스프레드 · 엔티티 직렬화). 읽기 전용 응답 모델을 둔다.
- 가려야 하면 **경계에서** 가린다 — 화면단에서 감추는 것은 이미 나간 값이다.

## C3 이력은 누가·무엇을·언제
- 접근·변경 이력 한 줄에 셋이 다 있어야 한다: 누가(역할 + ID) · 무엇을(업무 식별자) · 언제(UTC).
- 보존 기간은 P2 의 값과 근거를 따른다.

## 사내 전제를 벗어나면
사외 사용자·외부망·규제 대상이면 **P3** 의 추가 규칙이 먼저다(동의 확인 · 통지 본문 제한 · 대리 접근 · 열거 방지 등).
P3 이 「해당 없음」인데 사외로 나가는 설계가 보이면 그것이 Flagged concern 이다.

## 이 스킬이 하지 않는 것
- 법·규제를 해석하지 않는다. 보존 기간·통지 의무를 스스로 정하지 않는다.
- 엔드포인트 보안 4항목은 `secure-api-review`, 자격증명 스캔은 `secrets-scan`.
- 강제하지 않는다 — 권고적 통제다.
