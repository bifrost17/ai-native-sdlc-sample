---
id: 0002-claims-status
kind: spec
status: draft
upstream: intent.md@{{sha:upstream}}
skills_applied: [secure-api-review]
---
# Spec: 청구 상태 자가조회 (from intent 0002)

## Requirements (요구)
- R1 담당자는 자기 청구 건의 상태를 조회할 수 있다.
- R2 조회 결과는 60초 이내에 갱신된 값이다.

## Design (설계)
기존 세션 인증을 그대로 쓰고, 청구 API 응답에서 허용 목록에 있는 필드만 골라 60초 캐시에 담는다.

## Constraints inherited (상속한 제약)
- C1 새 개인식별정보를 노출하지 않는다 — 허용 목록을 코드와 시험 양쪽에 따로 적는다.
- C2 과금 로직은 건드리지 않는다.

## Constraints discovered (발견한 제약)
- C3 상류 청구 API 는 초당 50회를 넘기면 429 를 돌려준다.

## Open questions from intent (intent 의 미결)
- Q1 answered: 플랫폼팀 김철수가 초당 50회로 확정했다 (2026-09-10).

## Flagged concerns (플래그)
- F1 캐시 60초 동안 실제 상태와 어긋날 수 있다 — 청구운영팀장이 수용 여부를 판단한다.

## Out of scope (범위 밖)
결제 취소와 환불 흐름은 이 spec 이 다루지 않는다.

## Acceptance criteria (수용 기준)
- AC1 → R1 담당자 계정으로 조회하면 자기 건만 돌아온다.
- AC2 → R2 캐시가 60초를 넘기면 상류를 다시 부른다.
