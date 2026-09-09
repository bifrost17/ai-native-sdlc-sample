# Plan: 원장에 없던 건은 캐시하지 않는다 (from intent.md 2026-09-09)
Upstream: spec.md@11c9289829a10233cc3bfc0ff27a6ab47e1aa48d. Status: draft.
Note: spec 도 draft(PR B 가 PR A 위에 쌓인다) — 엔지니어(부모 세션) 지시로 착수. 승인은 PR A·B 의 머지.
## Files that change
- tests/test_claims_status_incident.py (new) — 인시던트 재현 시험 AC1 + AC2 대조. 기존 tests/test_claims_status.py 는 손대지 않는다.
- src/claims_status/records.py — `fetch_claim` 의 캐시 쓰기 한 줄(미스면 쓰지 않는다) + 문서 문장.
- evals/cases/04-incident-stale-not-found.json (new) + evals/fixtures/04-incident-stale-not-found/ (new) — L10 693 「인시던트마다 eval 하나」.
## Order of work
1. `tests/test_claims_status_incident.py` 를 쓰고 `python3 -m unittest tests.test_claims_status_incident` 로 **단정 실패 red 를 실측**한다(임포트 실패는 red 가 아니다). 시험만 한 커밋.
2. `INTENT_TASK=fix` 로 `records.py` 를 고쳐 green — 시험 파일은 편집하지 않는다(protect-tests 훅의 자리).
3. eval 케이스 1건 — 기존 3건 형식 그대로, 픽스처는 수정 전 `records.py` 사본 + 이 시험 파일.
4. `make check` 전량 그린 원문을 raw 에. 뮤테이션 1건(수정 자리 한 줄을 원래대로 되돌려 AC1 red → sha256 복원).
## Risks
- 가장 위험한 단계는 2 다 — 조건을 잘못 두면 있는 건까지 안 캐시돼 R2(AC5) 가 깨진다. 기존 AC5 두 시험이 그것을 잡는다.
- 시험이 `records._UPSTREAM` 을 직접 만지므로 tearDown 복원이 빠지면 다른 시험을 오염시킨다 — 0002 시험의 Base 패턴(deepcopy 백업)을 그대로 쓴다.
- 하지 않은 것: 없는 번호 전용 TTL·호출 상한(spec F1, 별도 사슬) · 밴드 설정 변경.
## Proof
- AC1 ← TestIncidentStaleNotFound.test_ac1_claim_created_after_a_miss_is_visible_on_the_next_lookup (상류 호출 2 포함)
- AC2 ← TestIncidentStaleNotFound.test_ac2_existing_claim_is_still_served_from_cache_within_ttl + 기존 TestAC5TtlCache
- AC3 ← `make check` rc=0 (기존 스위트 무편집)
- 출력: 단계 1 red 원문 · 단계 4 `make check` 원문 · 뮤테이션 red/복원 원문 — PR 본문에.
