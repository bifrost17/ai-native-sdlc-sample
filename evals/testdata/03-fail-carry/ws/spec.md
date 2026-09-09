---
id: 9003-eval-spec-carry
kind: spec
status: draft
upstream: intent.md@0000000000000000000000000000000000000000
skills_applied: [secure-api-review]
---
# Spec: 청구 상태 알림 재발송 (from intent 9003)

## Requirements (요구)
- R1 상태 전이 이벤트를 구독해 10분 안에 알림을 만든다
- R2 발송 실패는 3회까지 지수 백오프로 재시도한다

## Design (설계)
상태 저장소의 변경 이벤트를 큐로 받아 발송 게이트웨이에 넘긴다. 큐는 기존 것을 쓴다.

## Constraints inherited (상속한 제약)
- C1 새 개인정보를 추가로 수집하지 않는다
- C2 상류 청구 시스템에 초당 50건을 넘겨 호출하지 않는다

## Constraints discovered (발견한 제약)
- C3 발송 게이트웨이의 분당 한도가 600건이다

## Open questions from intent (intent 의 미결)
- Q2 carried: 야간 발송 유예는 이 스펙에서 정하지 않는다 — 고객경험팀 결정 대기

## Flagged concerns (플래그)
- F1 알림 문구가 청구 사유를 유추 가능하게 하면 C1 과 충돌한다 — 개인정보보호 담당

## Out of scope (범위 밖)
알림 채널 추가(카카오·앱푸시)는 범위 밖이다.

## Acceptance criteria (수용 기준)
- AC1 → R1 상태 전이 후 10분 이내 발송 레코드가 생성된다
- AC2 → R2 발송 실패 시 재시도 3회가 기록된다
