# Plan: 상담사 대리 청구 상태 조회 (from intent.md 2026-09-09)
Upstream: spec.md@43e298eb489685bdd1b4b7865948e9e578151fb8. Status: accepted (PR #39 가 9d6c954 로 머지됨).
Note: 엔지니어 결정(2026-09-09) — PR 은 하나(plan.md 는 자기 커밋, 구현과 같은 PR) · 뮤테이션 5건.
## Files that change
- `intent/0009-agent-proxy-claim-status/plan.md` (new) — 이 계획.
- `tests/test_agent_status.py` (new) — spec AC1~AC10 을 시험 이름으로.
- `src/claims_status/records.py` — 표본 원장에 **새 행 둘만** 추가(`C-3001`·`C-3002`). 함수 시그니처·캐시 동작은 그대로다.
- `src/claims_status/audit.py` — `record_agent_access(agent_id, subscriber_id, claim_id, at)` 하나 추가. 기존 `record_access`(셋)는 **한 글자도 고치지 않는다**. 머리글에 이 파일이 이제 0009 R8 도 구현한다는 한 줄을 더한다.
- `src/claims_status/agent_routes.py` (new) — `/agent/claims/<claim_id>/status` 핸들러.
- `README.md` — 사슬 표 0009 행의 PR 칸.
- **손대지 않는 것:** `src/claims_status/response.py`(R7 이 상수를 공유하라고 했으므로 더할 것이 없다) · `src/claims_status/routes.py` · 기존 시험 다섯 파일(`test_claims_status.py`·`_defect.py`·`_format.py`·`_incident.py`·`test_adjuster_status.py`). 규모 눈금: `src/` 추가 ≤ 60줄, `tests/` 추가 ≤ 230줄.
- 새 `src/` 파일의 첫 줄은 자기가 구현하는 spec 조항을 적는다(기존 파일들과 같은 꼴): `agent_routes.py` → 0009 R1·R3·R4·R5·R7·R8·R10. 시험 파일은 기존 시험처럼 L9 625 를 인용한다.

표본에 넣을 새 행 — `C-3001`(가입자 `S-77`) · `C-3002`(가입자 `S-12`, 「확인된 고객의 건이 아님」 판정용).
두 행 모두 `subscriber_rrn`·`subscriber_name`·`bank_account`·`internal_memo` 를 갖는다(AC7 이 그 값들의
부재를 재려면 원장에 있어야 한다). `adjuster_id` 는 넣지 않는다 — 사정인 경로에서 이 행들은 보이지
않아야 한다. **`C-1003`·`C-8888`·`C-9999` 는 쓰지 않는다**: `_incident.py:23` 이 `C-1003` 의 부재를,
`test_claims_status.py`·`_format.py` 가 `C-9999` 를, `test_adjuster_status.py:33` 이 `C-8888` 을
「원장에 없는 번호」로 전제한다. 이 사슬의 「없는 번호」는 `C-7777` 로 새로 잡는다. 새 행의 `status` 는
닫힌 다섯 값 안에서 고른다 — 0008 의 AC10 이 원장 전량을 훑는다. 기존 행을 손대지 않는 이유도 같은
계열이다(`test_claims_status.py:56` 이 `C-1001` 의 키 구성을, `_defect.py:54` 가 그 행의
`subscriber_id` 삭제를 전제한다).

**세션 계약(spec Design 확정분) — 시험이 손으로 적는다:**
`{"role": "agent", "agent_id": "E-4410", "verified_subscriber_id": "S-77", "verified_at": "<ISO-8601>"}`.
핸들러가 읽는 키는 앞의 셋뿐이고 `verified_at` 은 읽지 않는다(R6).
## Order of work
0. 세션 전제: `INTENT_TASK=fix` 를 **설정하지 않는다** — feature 사슬이고 새 시험 파일을 만들어야 하는데, `fix` 면 `.claude/hooks/protect-tests.sh` 가 `tests/*` 쓰기를 막는다. 파일 변경은 Edit/Write 도구로 한다(훅은 도구 호출을 보지 효과를 보지 않는다 — 사슬 0007). `Makefile`·`.github/**`·`.claude/hooks/**`·`.claude/settings.json` 은 frozen path 다(`protect-paths.sh`).
1. `plan.md` 커밋 — 사슬 규약은 intent → spec → plan, 각자 자기 커밋.
2. **시험 먼저 + 스텁 → red 실측.** `tests/test_agent_status.py` 를 다 쓰고, `agent_routes.py` 는 라우트 등록과 시그니처만 있는 스텁(`not_found` 고정), `audit.record_agent_access` 는 무동작 스텁으로 둔다. 새 표본 행 둘도 이 단계에서 들어간다 — 양성 대조가 그 행들을 읽기 때문이다. `python3 -m unittest tests.test_agent_status` 로 **단정 실패**를 확인한다: 임포트 실패는 red 가 아니라 계기 부재다. 시험+스텁을 한 커밋으로.
3. `audit.py` — `record_agent_access` 본체. 스칼라 넷만 받고 원장 레코드를 받지 않는다(못 받으면 실수로도 못 싣는다). 시각은 인자 `at` — `records.py` 의 `now` 는 캐시 만료용 단조 시계라 기록의 시각이 될 수 없다. 기존 `record_access` 와 같은 `_ACCESS` 리스트에 쌓는다.
4. `agent_routes.py` 본체 → green. 판정 순서(spec Design 그대로):
   세션 `None` → `unauthenticated` ·
   dict 가 아니거나 `role != "agent"` 이거나 `agent_id` 가 비었으면 → `not_found` ·
   `verified_subscriber_id` 가 비었으면 → `verification_required` ·
   `CLAIM_ID_RE` 불일치 → `invalid_claim_id` · (여기까지 상류 호출 0 · 기록 0) ·
   `fetch_claim(claim_id, now=now, cached=True)` ·
   가입자 불일치·없는 건 → `not_found`(기록 0) ·
   `build_response(record, RESPONSE_FIELDS)` 뒤에 `record_agent_access(...)`.
   소유 판정은 0005 규칙 그대로 — 어느 한쪽이 비면(`None`·`""`·없음) 불일치. `route`·`CLAIM_ID_RE` 는 `routes.py` 에서, `RESPONSE_FIELDS` 는 `response.py` 에서 **임포트한다**(복사하지 않는다). 시험은 편집하지 않고 초록으로 만든다.
5. 뮤테이션 5건 — 한 줄 침묵 살해 → 지정 시험 red 확인 → **`sha256` 대조로 복원**(`git checkout --` 은 쓰지 않는다: 커밋 안 한 수정까지 버린다, 사슬 0008).
   M1 소유 판정 한 줄 삭제 → AC5 red · M2 본인확인 게이트 삭제 → AC4 red · M3 `record_agent_access(...)` 호출 삭제 → AC8 red · M4 `RESPONSE_FIELDS` 임포트를 같은 내용의 리터럴 튜플로 교체 → AC7 red · **M5 본인확인 게이트를 `fetch_claim` 호출 아래로 옮긴다(지우지 않고 순서만 바꾼다) → AC4 의 상류 호출 수 0 단정 red**. M5 가 M2 와 다른 것을 잰다: M2 는 게이트의 존재를, M5 는 게이트의 **자리**를 잰다.
6. `README.md` 사슬 표 0009 행 PR 칸.
7. `make check` 전량, 원문을 PR 본문에.
## Risks
- **가장 위험한 단계는 4 의 판정 세 줄 — 게이트·소유 판정, 그리고 그 둘의 자리다.** 소유 판정(R5)이 빠지거나 뒤집히면 상담사 세션 하나로 원장의 모든 건이 보이고, 본인확인 게이트(R4)가 빠지면 확인 없는 통화에서 남의 건이 나간다. 둘 다 범위가 무제한이고 조용하다. 0005 가 고친 함정이 같은 모양으로 여기 다시 있다 — 원장의 `subscriber_id` 와 세션의 `verified_subscriber_id` 가 둘 다 비면 `None == None` 으로 통과한다. AC5 가 양쪽을 재고 M1·M2 가 계기를 실증한다.
- **게이트의 「자리」는 코드 배치가 아니라 시험이 잡는다(spec F5).** 게이트가 `fetch_claim` **뒤로** 내려가면 응답 문구는 그대로 `verification_required` 라서 문구만 보는 시험은 전부 초록인데, 그 사이 상류가 불려 청구 번호의 존재 여부가 상류 접근 패턴으로 샌다 — 보안팀이 F5 를 허가한 근거("상류 조회 전에 돌아가니 존재 여부가 새지 않는다")가 무너진다. 계기는 `records.upstream_calls()` 다: AC4 는 **없는 번호**(`C-7777`)를 본인확인 없는 세션으로 조회해 `verification_required` 와 함께 **상류 호출 수 0** 을 단정한다. 배치만으로는 아무것도 보장되지 않으므로 M5 가 그 단정이 실제로 죽이는지 실증한다(게이트를 지우지 않고 아래로 옮기기만 한다). 같은 계기를 0002 가 이미 쓴다(`tests/test_claims_status.py:110`).
- **2순위는 허용 목록을 복사하는 것이다.** 복사해도 당장은 전부 초록이고, 갈라지는 것은 나중이다. 게다가 0008 이 `ADJUSTER_FIELDS` 를 만든 직후라 「청중마다 상수 하나」가 이 코드베이스의 관성이다 — 다음 사람이 `AGENT_FIELDS` 를 만들고 싶어질 자리다. AC7 은 값이 같은지가 아니라 **같은 객체인지**를 재고(`is`), M4 가 그 시험이 실제로 죽이는지 보인다. 이것이 R1(「고객이 보는 것과 똑같은 값」)의 유일한 구조적 보증이다.
- **3순위는 만료를 친절하게 다시 넣는 것이다.** spec F4 에서 뒤집힌 자리라 초안만 읽은 사람은 30분 검사를 넣는 것이 맞다고 생각한다. 넣으면 만료의 소유자가 둘이 되고 콘솔과 시계가 어긋나는 순간 29분대 조회가 닫힌다. AC6 이 「`verified_at` 을 무엇으로 채워도 응답이 같다」를 재서 막는다.
- **0008 의 접근 기록을 고치고 싶어지는 자리.** `record_access` 에 `subscriber_id` 를 선택 인자로 끼우는 것이 가장 짧은 길처럼 보이지만, 0008 AC8 이 키 집합을 정확히 셋으로 못 박고 있어 그 순간 red 다. AC9② 가 그것을 명시적으로 다시 잰다.
- **`_ACCESS` 가 이제 두 모양의 줄을 담는다 — 무엇이 격리를 보장하는지 실측했다.** 0008 의 AC8 은 `audit.access_records()` **전량**에 대해 `len(entries) == 1` 과 「키가 정확히 셋」을 단정한다(`tests/test_adjuster_status.py:220-233`). 상담사 시험이 남긴 넷짜리 줄이 리스트에 남아 있으면 그 두 단정이 바로 깨진다. 깨지지 않는 유일한 근거는 **0008 의 `Base.setUp` 이 매 시험 `audit.reset_for_test()` 를 부른다는 것**이다(`tests/test_adjuster_status.py:47-56`) — 파일 실행 순서(`test_adjuster_status` < `test_agent_status`)나 클래스 이름에 기대는 것이 아니다. 그러므로 **새 시험 파일의 `Base` 도 같은 `setUp`/`tearDown` 을 그대로 갖는다**: `records._UPSTREAM` 깊은 복사 백업·복원 + `records.reset_for_test()` + `audit.reset_for_test()`. 이 네 줄을 빠뜨리면 0008 이 우리 때문에 빨개진다. 더해서, 새 파일은 사정인 경로를 AC9② 한 곳에서만 부르고 그 시험은 사정인 조회 1건만 만든다.
- **`records.py` 에 행을 더하는 것이 앞선 사슬에 닿는지 실측했다.** ① 0008 AC10 은 `records._UPSTREAM.items()` 전량을 훑어 `row["status"]` 를 닫힌 다섯과 대조한다(`tests/test_adjuster_status.py:252-257`) — 새 행에 `status` 키가 없으면 `KeyError`, 다섯 밖의 값이면 단정 실패다. 그래서 두 행 모두 `status` 를 갖고 값은 다섯 안에서 고른다. ② 0002 AC5 는 `records.upstream_calls()` 를 세는데(`tests/test_claims_status.py:113-124`) 세는 대상은 **호출 수**이지 원장 크기가 아니고, 그 시험은 `C-1001` 만 조회한다 — 행이 늘어도 값이 변하지 않는다. ③ 원장의 **행 수**를 단정하는 시험은 저장소 전량에 없다(`grep -n 'len(records._UPSTREAM)' tests/` → 0건). ④ `_incident.py:42` 는 `C-1003` 의 부재를 단정하므로 그 번호만 피하면 된다. 결론: 새 행 둘은 ①의 제약(닫힌 status)만 지키면 앞선 시험 어디에도 닿지 않는다.
- **AC10 은 상류 호출 수를 세므로 순서에 취약하다** — `records.reset_for_test()` 로 매 시험 격리하고 `now` 를 주입한다(실시간·`sleep` 금지).
- **닿지 않는다고 실측할 것:** `RESPONSE_FIELDS` 를 임포트하는 곳은 지금 `routes.py:8` 하나뿐이고 이 사슬이 두 번째를 만든다 — 그 목록을 넓히는 커밋은 이제 두 청중을 동시에 넓힌다는 뜻이고, 그것이 R7 의 내용이다. evals 는 `src/` 를 보지 않는다(`evals/run.sh` 가 케이스의 `files` 만 새 워크스페이스로 복사한다 — 0008 plan 이 실측).
- **안 고른 선택지.**
  ① **`record_access` 를 네 인자로 넓히기** (새 함수 대신). 두 갈래 다 나쁘다. 인자에 기본값을 주면(`subscriber_id=None`) 0008 의 호출은 살지만 기록의 키 집합이 **호출자에 따라 달라지는** 함수가 되고, 그것은 0008 Design 이 `build_response` 의 필드 인자를 필수로 만들며 배제한 바로 그 모양이다 — 빠뜨린 호출자가 조용히 다른 기록을 남긴다. 기본값을 안 주면 0008 의 호출부를 고쳐야 하는데, 그 순간 사정인 기록이 넷이 되어 0008 AC8(「키가 정확히 셋」)이 빨개지고 그건 0008 spec 을 바꾸는 일이다(별건의 사슬). 함수를 하나 더 두면 **청중마다 키 집합이 닫힌 채로** 남고, 넓히는 실수가 문법으로 막힌다 — 0008 이 `audit.py` 를 세운 원리 그대로다.
  ② **`adjuster_routes.py` 를 `role` 로 분기해 일반화하기.** 두 경로가 다른 것이 네 가지다 — 허용 목록(셋 vs 넷), 캐시 정책(`False` vs `True`), 소유 판정에 쓰는 원장 필드(`adjuster_id` vs `subscriber_id`)와 세션 필드, 기록의 모양(셋 vs 넷). 일반화하면 그 네 정책이 한 함수의 분기표로 모이고, 한쪽을 고치다 다른 쪽을 조용히 깨는 길이 열린다. 0008 이 고객 경로와 파일을 가른 이유가 이것이고(spec 0008 Design), 그때 세운 규율은 「청중별 규칙은 각자의 라우트 파일, 상류 문·응답 문·기록 문은 하나씩」이다. 이 사슬은 그 규율의 세 번째 적용이지 예외가 아니다. 덤으로: 일반화는 `adjuster_routes.py` 를 고치는 일이라 R9①(0008 시험 무편집 통과)의 위험을 공짜로 떠안는다.
  ③ **상담사 경로에 `cached=False`.** 0008 이 캐시를 우회한 이유는 배정이 **권한**이고 이관이 즉시여야 했기 때문이다. 여기서 권한을 정하는 것은 세션의 본인확인 표시이고 그것은 캐시를 타지 않는다 — 캐시가 드는 것은 「이 건의 가입자가 누구인가」뿐이고, 보안팀이 「고객 경로와 같은 의미론이면 된다」고 답했다(spec F6). 더 결정적인 것은 R1 이다: 상담사 응답은 고객 응답과 **바이트 단위로 같아야** 하는데, 캐시 정책을 다르게 하면 TTL 창 안에서 두 경로가 서로 다른 값을 내는 것이 **설계된 동작**이 된다 — 통화 중에 상담사와 고객이 다른 화면을 보는 것이고, 그것이 이 사슬이 없애려는 바로 그 문제다(F2 의 결정: 「같은 캐시가 정확히 원하는 바」). `cached=False` 는 요구를 어기는 쪽으로 더 부지런한 코드다.
  ④ **`AGENT_FIELDS` 새 상수** — R7 이 금지한다. 값이 같은 두 상수는 언젠가 갈라지고, 갈라지는 순간 「고객이 보는 것과 똑같은 값」이 깨진다.
  ⑤ **앱에서 30분 만료 재기** — spec F4 가 콘솔 소유로 결정했다(초안과 반대로 뒤집힌 자리).
  ⑥ **실패한 조회도 기록** — F7·이슈 #32 의 답을 0008 과 함께 기다린다; 지금 넣으면 두 경로가 갈린다.
- **하지 않는 것:** 상담 화면·프론트엔드(F9) · 실제 HTTP 서버·라우터 배선 · 접근 기록의 저장소와 보존 기간 · 실패한 조회의 기록(F7 — AC8 이 「0건」으로 현재 선택을 못 박아, 뒤집으려면 시험이 빨개져 결정이 남는다) · 0002·0008 경로의 동작 변경 · 청구 번호 목록.
## Proof
시험은 `tests/test_agent_status.py` 한 파일. AC ↔ 시험 이름:
- 양성 대조 ← `TestSurfaceIsReachable.test_agent_handler_is_registered_under_the_route` · `test_upstream_carries_the_new_subscriber_rows`
- AC1 ← `TestAC1SameAsCustomer.test_ac1_agent_body_is_byte_identical_to_customer_body` · `test_ac1_body_has_exactly_four_fields_with_values`
- AC2 ← `TestAC2NoSession.test_ac2_no_session_returns_unauthenticated_without_upstream_call`
- AC3 ← `TestAC3NonAgentSession.test_ac3_customer_and_adjuster_sessions_are_not_found_without_upstream_call` · `test_ac3_session_without_agent_id_is_not_found`
- AC4 ← `TestAC4VerificationRequired.test_ac4_missing_marker_returns_verification_required_without_upstream_call` · `test_ac4_same_body_for_known_unknown_and_malformed_claim_ids`
- AC5 ← `TestAC5Ownership.test_ac5_other_customers_claim_and_unknown_claim_share_one_body` · `test_ac5_empty_subscriber_on_either_side_is_not_a_match` · `test_ac5_malformed_claim_id_is_rejected_without_echo`
- AC6 ← `TestAC6ExpiryIsNotMeasuredHere.test_ac6_response_is_the_same_for_any_verified_at_including_absent`
- AC7 ← `TestAC7SharedAllowlist.test_ac7_agent_path_uses_the_customer_allowlist_object` · `test_ac7_new_upstream_field_does_not_widen_the_response_and_pii_never_appears`
- AC8 ← `TestAC8AccessRecord.test_ac8_successful_read_appends_one_record_of_exactly_four_keys` · `test_ac8_failed_lookups_append_nothing`
- AC9 ← `TestAC9EarlierPathsUnchanged.test_ac9_adjuster_record_still_has_exactly_three_keys` · `test_ac9_agent_session_on_customer_route_is_not_found_and_records_nothing` + 기존 다섯 파일 무편집(`git diff --stat`)
- AC10 ← `TestAC10SharedCache.test_ac10_agent_lookup_reuses_the_customer_cache_within_ttl`

**규율(0002 에서 이어받음):** 시험은 허용 키 집합·기록 키 집합·세션 계약을 **구현에서 임포트하지
않고** 손으로 적는다 — 구현이 넓어지면 여기가 빨개져야 한다.

**결정 하나, 그리고 그 이유 — AC7 은 `==` 가 아니라 `is` 로 잰다.** 이 규율에 대한 의도된 예외이고,
plan.md 에 적어 두지 않으면 다음 사람이 「임포트해서 비교하는 건 규율 위반」이라고 읽고 `==` 로
바꾼다. 바꾸면 시험은 계속 초록인데 R7 이 죽는다:

- R7 이 요구하는 것은 「같은 값의 목록」이 아니라 「**같은 목록**」이다 — 고객 목록을 넓히는 커밋이
  상담사 화면도 같이 넓혀야 「고객이 보는 것과 똑같은 값」이 구조로 성립한다(spec R7·F2).
- `agent_routes` 가 `("claim_id","status","next_step","due_date")` 를 리터럴로 복사해도 `==` 는
  통과한다. 그 상태에서 누가 `response.RESPONSE_FIELDS` 에 필드를 더하면 고객 화면만 넓어지고
  상담사 화면은 조용히 뒤처진다 — 초록인 채로 요구가 깨진 상태다.
- `is` 는 그 복사본을 잡는 유일한 계기다. M4(임포트를 같은 내용의 리터럴로 교체)가 이 시험이
  실제로 죽이는지 실증한다. `==` 로 바꾸면 M4 가 살아남고, 그것이 곧 「바꾸면 안 되는 이유」의 증거다.
- 그래서 이 한 시험만 구현을 임포트한다. 나머지 단정(키 집합·기록 키·세션 계약)은 손으로 적은
  값을 쓴다 — 두 규율이 충돌하지 않는다: 손으로 적는 규율은 **응답이 넓어지는 것**을 잡고,
  `is` 는 **두 청중이 갈라지는 것**을 잡는다.

**AC4 의 계기 하나 더:** 본인확인 없는 세션으로 조회하는 번호는 원장에 **없는** 번호(`C-7777`)를
쓰고, 응답 문구와 함께 `records.upstream_calls() == 0` 을 단정한다. 문구만 보면 게이트가 상류 뒤로
내려가도 초록이기 때문이다(위 Risks·M5).

붙일 출력: ① 단계 2 의 red 원문(`FAILED (failures=N)`) ② 단계 5 의 뮤테이션 5건 — 죽인 줄, red 가 된
시험 이름, 복원 `sha256` 대조 ③ 단계 7 의 `make check` rc=0 원문(`Ran N tests / OK` ·
`test_hooks: 28 passed, 0 failed` · `8 passed, 0 failed` · `PASS  managed-settings 키·훅 계약`).
