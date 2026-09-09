---
id: 9001-eval-sample
kind: intent
status: draft
author: 김민수 (청구운영팀)
created: 2026-09-09T10:12:00+09:00
record: none
supersedes: none
---
# Intent: 청구 상태 알림 재발송

## Problem (문제)
‹오늘 무엇이 안 되는가 — 관찰된 사실·건수·시간›

## Proposed outcome (원하는 결과)
상태가 바뀐 시점부터 10분 안에 신청인이 등록한 채널로 알림이 나가고, 상담 콜 중 상태 문의 비중이 월 20% 아래로 내려간다.

## Affected users and systems (영향 범위)
신청인 · 상담원 · 청구 상태 저장소 · 알림 발송 게이트웨이. 개인정보는 기존에 이미 보유한 연락처만 쓴다.

## Constraints (제약)
- C1 새 개인정보를 추가로 수집하지 않는다
- C2 상류 청구 시스템에 초당 50건을 넘겨 호출하지 않는다

## Open questions (미결)
- Q1 「보류」 외에 어떤 상태 전이를 알릴지 — 청구운영팀장
- Q2 야간(22~08시) 발송을 미룰지 — 고객경험팀
