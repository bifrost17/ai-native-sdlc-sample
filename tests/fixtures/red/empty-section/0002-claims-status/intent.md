---
id: 0002-claims-status
kind: intent
status: draft
author: 홍길동 (청구운영팀)
created: 2026-09-09T10:12:00+09:00
record: none
supersedes: none
---
# Intent: 청구 상태를 사람이 전화로 묻는다

## Problem (문제)
청구 담당자가 상태를 확인하려면 콜센터에 전화한다. 지난 30일 동안 이런 문의가 1,240건이었고 한 건에 평균 6분이 걸렸다.

## Proposed outcome (원하는 결과)
담당자가 사람 개입 없이 30초 안에 자기 청구 건의 상태를 확인한다.

## Affected users and systems (영향 범위)

## Constraints (제약)
- C1 새 개인식별정보를 노출하지 않는다. 화면에 나가는 필드는 이미 승인된 목록 안에서만 고른다.
- C2 과금 로직은 이번 범위 밖이다.

## Open questions (미결)
- Q1 상류 청구 API 의 초당 호출 한도를 누가 확정하는가 — 플랫폼팀 김철수.
