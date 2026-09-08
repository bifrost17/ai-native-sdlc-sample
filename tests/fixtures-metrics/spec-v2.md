---
id: {{ID}}
kind: spec
status: draft
upstream: intent.md@0000000
skills_applied: [secure-api-review]
---
# Spec: 청구 상태 자가조회 (from intent {{ID}})

## Requirements (요구)
- R1 상태 조회 엔드포인트
- R2 캐시 무효화

## Design (설계)
stdlib 서비스 + 60초 캐시

## Constraints inherited (상속한 제약)
- C1 새 PII 를 노출하지 않는다

## Constraints discovered (발견한 제약)
해당 없음 — 새로 발견한 제약 없음

## Open questions from intent (intent 의 미결)
- Q1 answered: 60초

## Flagged concerns (플래그)
해당 없음 — 정책 충돌 없음

## Out of scope (범위 밖)
결제 상태

## Acceptance criteria (수용 기준)
- AC1 → R1 허용 필드 4개만 반환한다
