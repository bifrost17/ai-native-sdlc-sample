---
id: 0003-retention-notice
kind: plan
status: accepted
upstream: spec.md@{{sha:c2}}
---
# Plan: 보관기간 안내 문구 정합 (from intent 0003)

## Files that change
- src/notice/retention.py
- tests/test_retention_notice.py

## Order of work
1. 지침 표를 읽는 자리를 만든다 [Art. 4 · 부속서 2].
2. 어긋난 문구가 발송을 막는 실패 시험을 먼저 쓴다.
3. 대조를 붙이고 시험을 통과시킨다.

## Risks
Q2(정정문 대상 범위)가 아직 열려 있다 — 결정 전에는 정정문 발송을 켜지 않는다.

## Proof
- AC1 ← test_notice_text_follows_guideline_table
- AC2 ← test_send_blocked_when_text_diverges

## Options not taken
문구를 상수로 박는 방법은 【부속서 2】 개정 때마다 죽는다. 템플릿 자리표시자만 남기는 안도 검토했으나 아래 형태는 채워지지 않은 채 나갈 위험이 있어 버렸다.

```markdown
보관기간: ‹지침 표의 값›
```

## Parallelisable
문구 대조와 정정문 발송은 서로 독립이다 — Q2 가 닫히면 나눠서 간다.
