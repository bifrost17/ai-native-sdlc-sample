---
id: {{ID}}
kind: intent
status: draft
author: 홍길동 (청구운영팀)
created: 2099-01-01T00:00:00+09:00    # 최초 커밋보다 미래(신고값 오류)
record: none
supersedes: none
---
# Intent: 청구 상태 자가조회

## Problem (문제)
콜센터가 청구 상태 문의를 하루 400건 받는다.

## Proposed outcome (원하는 결과)
가입자가 스스로 상태를 조회한다.

## Affected users and systems (영향 범위)
가입자 · 청구 API

## Constraints (제약)
- C1 새 PII 를 노출하지 않는다

## Open questions (미결)
- Q1 캐시 만료를 몇 초로 하는가 — 청구운영팀
