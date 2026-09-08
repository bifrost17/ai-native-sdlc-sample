---
id: ‹0002-claims-status›
kind: plan
status: draft
upstream: spec.md@‹accepted 된 spec 커밋 sha›
---
# Plan: ‹무엇을 만드는가› (from intent ‹0002›)

> 제목에 **두 홉을 다 적는다** — `upstream` 은 spec 을 가리키고 제목은 intent 를 가리킨다.
> intent 가 바뀌면 plan 이 낡았다는 것을 기계가 잰다.
> plan 은 「어떻게 만들까」가 아니라 **무엇을 어떤 순서로 건드리는가**다.

## Files that change
> 실제 경로를 적는다. 훅(`plan-sync`)이 이 목록 밖의 소스 커밋을 막는다 — 목록을 늘려야
> 하면 같은 커밋에서 plan 을 함께 고친다. 「여러 파일」(집행 불가) ✗ · 실경로 ✓.
- ‹src/…›
- ‹tests/…›

## Order of work
> 실패 시험이 **먼저** 오는 순서를 적는다. red 를 실측하지 않은 green 은 아무것도 증언하지 않는다.
1. ‹준비 — 자리 만들기›
2. ‹실패 시험을 쓰고 red 를 실측›
3. ‹구현하고 green›

## Risks
> 「위험 없음」은 쓰지 않는다. 아직 안 닫힌 Q 가 있으면 여기로 내려온다.
‹무엇이 어긋날 수 있는가 · 어떻게 알아챌 것인가›

## Proof
> spec 의 AC 를 시험 이름에 이어 붙인다. 검증기는 Proof 가 AC 를 최소 하나 덮는지 잰다 —
> 「전체 시험을 돌린다」(무엇도 안 가리킴) ✗ · 「AC1 ← test_…」 ✓.
- AC1 ← ‹시험 이름›

## Options not taken
> 버린 길과 **버린 이유**. 안 적으면 다음 사람이 같은 길을 다시 걷는다.
‹검토했으나 택하지 않은 안 · 이유›

## Parallelisable
> 나눠 갈 수 있는 덩어리. 없으면 「없음 — ‹이유›」.
‹동시에 갈 수 있는 작업 · 또는 없음 — 이유›
