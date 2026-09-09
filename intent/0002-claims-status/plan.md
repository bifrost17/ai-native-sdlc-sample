# Plan: 청구 상태 조회 API (from intent.md 2026-09-09)
Upstream: spec.md@e257572aac312d9b85d966fe7ddd5b9004dbc162. Status: draft.
## Files that change
- tests/test_claims_status.py (new) — spec AC1~AC5 를 시험 이름으로.
- src/claims_status/__init__.py (new) — 패키지 표시만, 로직 없음.
- src/claims_status/records.py (new) — 상류 원장 표본 + TTL 캐시 + 상류 호출 계수기.
- src/claims_status/response.py (new) — `RESPONSE_FIELDS` · `build_response()`.
- src/claims_status/routes.py (new) — `ROUTES` 등록 + `get_claim_status()`.
- 합계 src ≤ 200줄 · tests ≤ 200줄. Makefile·CI 는 손대지 않는다(`unittest discover -s tests` 가 새 파일을 그대로 줍는다).
## Order of work
1. `tests/test_claims_status.py` 를 쓰고, `src/claims_status/` 에는 시그니처만 있는 스텁(빈 응답·0 호출)을 둔다. `python3 -m unittest tests.test_claims_status` 를 돌려 **단정 실패로 red 를 실측**한다 — 임포트 실패는 red 가 아니라 계기 부재다. 시험+스텁을 한 커밋으로.
2. `records.py` — `_UPSTREAM` 표본(주민번호·계좌·메모·`subscriber_id` 포함) · `fetch_claim(claim_id, now)` · `upstream_calls()` · `reset_for_test()`. 없는 건도 캐시.
3. `response.py` — 허용 목록 튜플 하나와 `build_response(record)` 하나. 오류 응답은 고정 문자열 셋.
4. `routes.py` — 세션 → 형식 검증(`C-<숫자>`) → 상류 조회 → 소유 판정(`subscriber_id`) → 통로. 시험을 편집하지 않고 green 으로.
5. `make check` 전량 그린 원문을 raw 에. 뮤테이션 1건(소유 판정 한 줄 침묵 살해 → AC4 red → sha256 복원).
## Risks
- 가장 위험한 단계는 4 의 소유 판정이다 — 빠지면 세션만 있으면 남의 건이 보인다. AC4 시험(남의 건 = not_found)이 그것을 잡는다; 뮤테이션으로 실제로 red 가 나는지 실측한다.
- 허용 목록 시험이 구현의 `RESPONSE_FIELDS` 를 임포트하면 동어반복이다 — 시험 파일이 키 집합을 따로 적는다(spec AC3).
- TTL 시험이 실시간·sleep 을 쓰면 느리고 흔들린다 — `now` 를 인자로 주입한다.
- 오류 응답이 입력을 되비추면 형식 검증이 반사 통로가 된다 — AC4 가 입력 문자열 부재를 단정한다.
- 하지 않은 것: HTTP 서버·라우터 배선(spec Out of scope), 감사 이벤트(읽기 전용), 손해사정인 경로(carried forward).
## Proof
- AC1 ← TestAC1OwnClaim.test_ac1_own_claim_returns_exactly_the_four_fields
- AC2 ← TestAC2NoSession.test_ac2_no_session_returns_unauthenticated_without_upstream_call
- AC3 ← TestAC3Allowlist.test_ac3_new_upstream_field_does_not_widen_the_response · test_ac3_pii_values_never_appear_in_the_body
- AC4 ← TestAC4NotFound.test_ac4_foreign_and_unknown_claim_share_one_body · test_ac4_malformed_claim_id_is_rejected_without_echo
- AC5 ← TestAC5TtlCache.test_ac5_second_lookup_within_ttl_does_not_call_upstream · test_ac5_lookup_after_ttl_calls_upstream_again
- 양성 대조 ← TestSurfaceIsReachable.test_handler_is_registered_under_the_route · test_upstream_record_carries_the_pii_fields
- 출력: 단계 1 의 red 원문(FAILED, failures=N) 과 단계 5 의 `make check` rc=0 원문, PR 본문에 첨부.
