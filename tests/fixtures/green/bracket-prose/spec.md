---
id: 0003-retention-notice
kind: spec
status: accepted
upstream: intent.md@{{sha:c1}}
skills_applied: [secure-api-review]
---
# Spec: 보관기간 안내 문구 정합 (from intent 0003)

## Requirements (요구)
- R1 안내문 문구는 『청구 운영 지침』[Art. 4] 의 보관기간 값을 인용한다.
- R2 인용 값과 템플릿 문구가 다르면 발송이 막힌다.

## Design (설계)
지침 표를 한 곳에서 읽어 문구를 만들고, 발송 직전에 문구와 표를 다시 대조한다. 대조는 「같은가」만 보고 문장 품질은 보지 않는다.

## Constraints inherited (상속한 제약)
- C1 이미 나간 안내문은 소급 수정하지 않는다.
- C2 번역본[ja, en]은 범위 밖이다.

## Constraints discovered (발견한 제약)
- C3 【부속서 2】는 분기마다 개정되어 문구를 상수로 박으면 곧 낡는다.

## Open questions from intent (intent 의 미결)
- Q1 answered: 박민수가 기산점을 「접수일」로 확정했다 (2026-09-12).
- Q2 carried: 정정문 대상 범위는 고객지원팀장 결정 대기 — plan 의 Risks 로 넘긴다.

## Flagged concerns (플래그)
- F1 [Art. 4] 와 【부속서 2】가 어긋나는 분기가 있었다 — 준법지원팀장이 우선순위를 정한다.

## Out of scope (범위 밖)
안내문 디자인과 발송 채널[SMS, email]은 이 spec 이 다루지 않는다.

## Acceptance criteria (수용 기준)
- AC1 → R1 지침 표의 값을 바꾸면 안내문 문구도 같이 바뀐다.
- AC2 → R2 문구와 표가 어긋난 상태에서 발송하면 거부된다.
