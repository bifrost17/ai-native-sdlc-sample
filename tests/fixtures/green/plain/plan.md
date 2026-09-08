---
id: 0002-claims-status
kind: plan
status: accepted
upstream: spec.md@{{sha:c2}}
---
# Plan: 청구 상태 자가조회 (from intent 0002)

## Files that change
- src/claims_status/service.py
- src/claims_status/records.py
- tests/test_claims_status.py

## Order of work
1. 허용 필드 목록과 캐시 만료를 담을 자리를 만든다.
2. 실패하는 시험을 먼저 쓰고 red 를 실측한다.
3. 조회 경로를 붙이고 시험을 통과시킨다.

## Risks
캐시 만료 경계에서 값이 어긋날 수 있다. 만료 시각을 시험이 직접 밀어 확인한다.

## Proof
- AC1 ← test_only_own_claims_are_returned
- AC2 ← test_cache_expires_after_60s

## Options not taken
상류 응답을 통째로 저장하는 방법은 C1 과 충돌해 버렸다.

## Parallelisable
없음 — 파일 세 개가 한 사슬로 이어져 순서대로 간다.
