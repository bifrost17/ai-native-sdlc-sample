# Plan: 배정 사정인용 청구 상태 조회 (from intent.md 2026-09-09)
Upstream: spec.md@e8676509faa4925f04cc5e95861f48d3fbf52b1b. Status: draft.
Note: 엔지니어 결정(2026-09-09) — PR 은 하나(plan.md 는 자기 커밋, 구현과 같은 PR) · 뮤테이션 3건.
## Files that change
- `intent/0008-adjuster-claim-status/plan.md` (new) — 이 계획.
- `tests/test_adjuster_status.py` (new) — spec AC1~AC10 을 시험 이름으로.
- `src/claims_status/records.py` — `fetch_claim(claim_id, now=None, *, cached)` 인자 하나 추가(필수 키워드, 아래 참조); 표본 원장에 **새 행 세 개만** 추가하고 기존 `C-1001`·`C-1002` 는 손대지 않는다.
- `src/claims_status/response.py` — `ADJUSTER_FIELDS`·`STATUS_VALUES` 추가, `build_response(record, fields)` 의 필드 인자를 필수로.
- `src/claims_status/routes.py` — 호출 한 줄에 `RESPONSE_FIELDS`·`cached=True` 명시(0002 동작 불변).
- `src/claims_status/audit.py` (new) — `record_access(adjuster_id, claim_id, at)` 하나.
- `src/claims_status/adjuster_routes.py` (new) — `/adjuster/claims/<claim_id>/status` 핸들러.
- `README.md` — 사슬 표 0008 행의 PR 칸.
- 기존 시험 네 파일(`tests/test_claims_status.py`·`_defect.py`·`_format.py`·`_incident.py`)은 **한 줄도 고치지 않는다**. 규모 눈금: src 추가 ≤ 120줄, tests 추가 ≤ 220줄.
- 새 `src/` 파일의 첫 줄은 자기가 구현하는 spec 조항을 적는다(기존 `records.py` → "spec.md R5" 꼴): `audit.py` → 0008 R8, `adjuster_routes.py` → R1·R3·R4·R6·R7. 시험 파일은 기존 시험처럼 L9 625 를 인용한다.

표본에 넣을 새 행: `C-2001`(사정인 `A-3391` 배정) · `C-2002`(다른 사정인 `A-7742`) · `C-2003`(`adjuster_id` 가 빈 문자열). **`C-1003`·`C-9999` 는 쓰지 않는다** — `_incident.py` 가 「`C-1003` 은 아직 원장에 없다」를, `_format.py`·`test_claims_status.py` 가 「`C-9999` 는 없는 번호」를 전제한다. 새 행의 `status` 는 닫힌 다섯 값 안에서 고른다(AC10 이 원장 전량을 훑는다). 기존 행을 손대지 않는 이유도 같은 계열이다: `test_claims_status.py:56` 이 `C-1001` 의 키 구성을, `_defect.py:54` 가 그 행의 `subscriber_id` 삭제를 전제한다.

**캐시 정책은 기본값을 갖지 않는다 — spec Design 문면에서 한 걸음.** spec Design 은 `cached=True` 기본값을 적었다("기본값이 `True` 라서 0002 의 호출부와 AC5 의 호출 수 계산은 그대로다"). 이 계획은 필수 키워드 인자로 간다. 근거는 spec 이 `build_response` 의 필드 인자를 필수로 만든 그 문장과 같다 — 빠뜨리면 조용히 위험한 쪽으로 떨어지는 기본값을 두지 않는다. 잊은 호출자는 60초 낡은 **권한**으로 판정하고, 그것이 spec F1 이 안 된다고 한 바로 그 상태다. 대가는 `routes.py` 호출 한 줄이고 R1~R10·AC1~AC10 은 바뀌지 않는다. 요구가 아니라 Design 문면에서 벗어나는 것이므로 여기에 적고 PR 본문에서 제품 오너에게 보인다.
## Order of work
0. 세션 전제: `INTENT_TASK=fix` 를 **설정하지 않는다** — feature 사슬이고 새 시험 파일을 만들어야 하는데, `fix` 면 `.claude/hooks/protect-tests.sh` 가 `tests/*` 쓰기를 막는다. 파일 변경은 Edit/Write 도구로 한다(훅은 도구 호출을 보지 효과를 보지 않는다 — 사슬 0007). `Makefile`·`.github/**`·`.claude/hooks/**`·`.claude/settings.json` 은 frozen path 다.
1. `plan.md` 커밋 — 사슬 규약은 intent → spec → plan, 각자 자기 커밋.
2. **시험 먼저 + 스텁 → red 실측.** `tests/test_adjuster_status.py` 를 다 쓰고 `audit.py`·`adjuster_routes.py` 는 시그니처만 있는 스텁으로 둔다(핸들러는 `not_found` 고정, `record_access` 는 무동작). `python3 -m unittest tests.test_adjuster_status` 로 **단정 실패**를 확인한다 — 임포트 실패는 red 가 아니라 계기 부재다. 라우트 등록과 새 표본 행은 이 단계에서 살아 있어야 양성 대조가 초록이다. 시험+스텁을 한 커밋으로.
3. `records.py` — `cached` 필수 키워드 인자. `cached=False` 면 TTL 을 보지 않고 상류를 부르며 받은 레코드로 캐시를 갱신한다. (구현 중 조정: 표본 새 행 셋은 단계 2 에서 함께 들어갔다 — 단계 2 의 양성 대조가 그 행들을 읽기 때문이다.)
4. `response.py` + `routes.py` **한 커밋으로**. 나누면 그 사이 커밋에서 0002 의 시험 전부가 red 다. (구현 중 조정: 같은 이유로 단계 3 도 이 커밋에 합쳤다 — `cached` 를 필수로 만든 순간 `routes.py` 의 호출이 깨지므로 3 과 4 사이에 초록인 커밋이 없다.)
5. `audit.py` 본체 — 모듈 상태는 리스트 하나. **원장 레코드를 인자로 받지 않는다**(못 받으면 실수로도 못 싣는다). 시각은 인자 `at`: `records.py` 의 `now` 는 캐시 만료용 단조 시계라 기록의 시각이 될 수 없다. 시험용 `access_records()`·`reset_for_test()`.
6. `adjuster_routes.py` 본체 → green. 판정 순서: 세션 `None` → `unauthenticated` · dict 가 아니거나 `role != "adjuster"` 이거나 `adjuster_id` 가 비었으면 → `not_found` · `CLAIM_ID_RE` 불일치 → `invalid_claim_id` (여기까지 상류 호출 0 · 기록 0) · `fetch_claim(claim_id, now=now, cached=False)` · 배정 불일치·없는 건 → `not_found`(기록 0) · `build_response(record, ADJUSTER_FIELDS)` 뒤에 `record_access(...)`. 배정 판정은 0005 규칙 그대로 — 어느 한쪽이 비면(`None`·`""`·없음) 불일치. `adjuster_name` 은 읽지 않는다. `route` 와 `CLAIM_ID_RE` 는 `routes.py` 에서 임포트한다(번호 형식 규칙은 0007 이 고친 `\A…\Z` 하나뿐이어야 한다). 시험은 편집하지 않고 초록으로 만든다.
7. 뮤테이션 3건 — 한 줄 침묵 살해 → 지정 시험 red 확인 → `sha256` 대조로 복원. M1 배정 판정 한 줄 삭제 → AC4 red · M2 `cached=False` → `cached=True` → AC7 red · M3 `record_access(...)` 호출 삭제 → AC8 red.
8. `README.md` 사슬 표 0008 행 PR 칸.
9. `make check` 전량, 원문을 PR 본문에.
## Risks
- **가장 위험한 단계는 6 의 배정 판정이다.** 빠지거나 뒤집히면 사정인 세션 하나로 원장의 모든 건이 보인다 — 범위가 무제한이고 조용하며 되돌릴 수 없다. 0005 가 고친 함정이 같은 모양으로 여기 다시 있다: 원장의 `adjuster_id` 와 세션의 `adjuster_id` 가 둘 다 비면 `None == None` 으로 통과한다. AC6 이 양쪽을 재고 M1 이 계기를 실증한다.
- **캐시 우회가 2순위인 근거.** 잊힌 `cached` 인자의 노출은 경계가 있다 — 이관된 건 하나, 최대 60초, 그 창에 조회한 사정인 한 명. 배정 판정 결함은 경계가 없다. 다만 「인자를 잊으면 위험한 쪽으로 떨어진다」는 모양은 동일하고 그것이 필수 키워드로 만든 이유다. 남는 위험은 「잊는다」가 아니라 「`True` 라고 명시적으로 잘못 적는다」이고 그건 리뷰에서 보인다. AC7 이 양방향(옛 사정인 `not_found`·새 사정인 세 필드)을 재고 M2 가 실증한다.
- **접근 기록이 넓어지거나 시계가 섞이면** 원장 값이 기록에 실리거나 시각이 「부팅 후 12.3초」가 된다. AC8 이 키 집합을 정확히 셋으로 못 박고 주입한 `at` 이 그대로 실리는지 본다.
- **`build_response` 의 필드 인자를 누가 기본값으로 되돌리면** 인자를 잊은 호출이 고객용 목록(=`next_step` 포함)을 조용히 내보낸다. AC5 가 사정인 경로에서만 잡는다 — 세 번째 청중이 생기면 그 경로의 시험이 또 필요하다.
- **`STATUS_VALUES` 는 런타임에 막지 않는다**(시험만 본다). 원장에 여섯 번째 값이 생기면 응답으로 나간 **뒤에** CI 가 빨개진다 — 값을 막는 장치가 아니라 결정을 강제하는 장치다(spec R10 의 선택).
- **0002 회귀.** 4 단계를 쪼개면 중간 커밋이 red 다. 기존 시험 파일이 `git diff --stat` 에 뜨면 그 자체가 compliance 발견이다(REVIEW.md).
- **닿지 않는다고 실측한 것:** `build_response`/`RESPONSE_FIELDS` 를 부르거나 임포트하는 곳은 저장소 전량에서 `routes.py:35` 하나뿐이다(0005·0006·0007 시험은 `routes.ROUTES` 로만 들어간다). evals 도 닿지 않는다 — `evals/run.sh:33` 이 케이스의 `files` 를 새 워크스페이스로 복사하고 `evals/check.sh:40-42` 가 워크스페이스 상대경로만 허용하므로, 케이스 04 는 `evals/fixtures/04-incident-stale-not-found/records.py`(0006 이전 판본의 동결 사본)만 읽고 `src/` 를 보지 않는다.
- **시험이 실시간·`sleep` 을 쓰면 흔들린다** — `now`·`at` 을 주입한다.
- **안 고른 선택지.** ① `routes.py` 안에 분기 — 한 함수가 두 청중을 맡으면 허용 목록·캐시 정책·기록 규칙이 한 몸에서 갈라지고, 사정인 쪽을 고치다 고객 쪽을 조용히 깨는 길이 열린다. ② 기존 로거 — 이 저장소에 로거가 없고 `records.py` 머리글이 로그·진단 함수를 금지한다(캐시가 거르기 전 원장 레코드를 들고 있다); 범용 로거는 원장 값을 쓸 수 있는 두 번째 문이 되고 secure-api-review ④와 부딪힌다. `audit.py` 는 스칼라 셋만 받아 구조적으로 그럴 수 없다. ③ 사정인 경로에 짧은 TTL(5초) — F1 의 답이 「60초 더 보는 건 안 된다」였고 0 이 아닌 TTL 은 같은 결함의 축소판이며, 아무도 고르지 않은 숫자와 두 번째 캐시 정책이 생긴다. ④ 별도 패키지 `src/adjuster_status/` — 상류 문과 응답 문이 복제된다. ⑤ `STATUS_VALUES` 런타임 강제 — 실재하는 청구를 아무도 정하지 않은 오류 뒤로 숨긴다.
- **하지 않는 것:** 실제 HTTP 배선 · 배정 건 목록 · 화면(spec F6) · 접근 기록의 저장소와 보존 기간(F8②) · 실패한 조회의 기록(F8① — AC8 이 「0건」으로 현재 선택을 못 박아, 뒤집으려면 시험이 빨개져 결정이 남는다) · 0002 spec 파일의 F3 갱신.
## Proof
시험은 `tests/test_adjuster_status.py` 한 파일. AC ↔ 시험 이름:
- 양성 대조 ← `TestSurfaceIsReachable.test_adjuster_handler_is_registered_under_the_route` · `test_upstream_rows_carry_the_assignment_fields`
- AC1 ← `TestAC1AssignedClaim.test_ac1_assigned_claim_returns_exactly_three_fields`
- AC2 ← `TestAC2NoSession.test_ac2_no_session_returns_unauthenticated_without_upstream_call`
- AC3 ← `TestAC3NonAdjusterSession.test_ac3_customer_session_is_not_found_without_upstream_call` · `test_ac3_session_without_adjuster_id_is_not_found_without_upstream_call`
- AC4 ← `TestAC4NotFound.test_ac4_unassigned_and_unknown_claim_share_one_body` · `test_ac4_malformed_claim_id_is_rejected_without_echo`
- AC5 ← `TestAC5Allowlist.test_ac5_new_upstream_field_does_not_widen_the_response` · `test_ac5_next_step_and_pii_never_appear_in_the_body`
- AC6 ← `TestAC6AssignmentMatch.test_ac6_empty_assignment_is_not_a_match_on_either_side` · `test_ac6_matching_name_with_different_number_is_not_found`
- AC7 ← `TestAC7ReassignmentIsImmediate.test_ac7_reassignment_within_ttl_flips_both_sides` · `test_ac7_every_adjuster_lookup_reads_upstream` (구현 중 추가: 첫 판은 원장 행을 **제자리 수정**해서 재려 했는데, 캐시가 같은 dict 객체를 들고 있어 캐시를 통해서도 수정이 보였다 — M2(`cached=True`)가 살아남았다. 행을 갈아 끼우도록 고치고, 상류 호출 수를 직접 세는 시험을 하나 더 붙였다. 지금은 M2 가 둘을 죽인다.)
- AC8 ← `TestAC8AccessRecord.test_ac8_successful_read_appends_one_record_of_exactly_three_keys` · `test_ac8_failed_lookups_append_nothing`
- AC9 ← `TestAC9CustomerPathUnchanged.test_ac9_customer_path_leaves_no_access_record` + 기존 네 파일 무편집(`git diff --stat`)
- AC10 ← `TestAC10StatusVocabulary.test_ac10_every_sample_row_status_is_in_the_closed_set`

규율(0002 에서 이어받음): 시험은 허용 키 집합·닫힌 status 다섯 값·기록 키 셋을 **구현에서 임포트하지 않고** 손으로 적는다. 구현이 넓어지면 여기가 빨개져야 한다.

붙일 출력: ① 단계 2 의 red 원문(`FAILED (failures=N)`) ② 단계 7 의 뮤테이션 3건 — 죽인 줄, red 가 된 시험 이름, 복원 `sha256` 대조 ③ 단계 9 의 `make check` rc=0 원문(`Ran N tests / OK` · `test_hooks: 28 passed, 0 failed` · `8 passed, 0 failed` · `PASS  managed-settings 키·훅 계약`).
