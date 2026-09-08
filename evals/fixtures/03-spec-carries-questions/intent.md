---
id: 9003-eval-spec-carry
kind: intent
status: accepted
author: 김민수 (청구운영팀)
created: 2026-09-09T10:12:00+09:00
record: none
supersedes: none
---
# Intent: 청구 상태 알림 재발송

## Problem (문제)
청구 상태가 「보류」로 바뀌어도 신청인에게 알림이 가지 않는다. 8월 한 달간 상담 콜 214건 중 61건이 상태 문의였고, 상담원이 화면을 열어 읽어 주는 데 평균 3분 20초가 걸린다.

## Proposed outcome (원하는 결과)
상태가 바뀐 시점부터 10분 안에 신청인이 등록한 채널로 알림이 나가고, 상담 콜 중 상태 문의 비중이 월 20% 아래로 내려간다.

## Affected users and systems (영향 범위)
신청인 · 상담원 · 청구 상태 저장소 · 알림 발송 게이트웨이.

## Constraints (제약)
- C1 새 개인정보를 추가로 수집하지 않는다
- C2 상류 청구 시스템에 초당 50건을 넘겨 호출하지 않는다

## Open questions (미결)
- Q1 「보류」 외에 어떤 상태 전이를 알릴지 — 청구운영팀장
- Q2 야간(22~08시) 발송을 미룰지 — 고객경험팀
