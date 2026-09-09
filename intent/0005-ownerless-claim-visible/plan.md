Note: intent(PR #20)·spec 이 아직 draft 다. 엔지니어(부모 세션)가 2026-09-09 draft 위에 착수를 지시했다(design-spec 「one exception」·plan Inputs).
# Plan: 소유 판정에서 빈 가입자 표시는 불일치다 (from intent.md 2026-09-09)
Upstream: spec.md@8cce821c4ef059fa7ba7f6ba6719c1e71754b5a1. Status: draft.
## Files that change
- tests/test_claims_status_defect.py (new) — spec AC1·AC2 를 시험 이름으로. 0002 의 시험 파일과 사슬 0006 의 파일은 건드리지 않는다.
- src/claims_status/routes.py — `get_claim_status` 의 소유 판정 한 자리.
- 그 밖엔 없다. `tests/test_claims_status.py` 는 sha256 으로 불변을 잰다.
## Order of work
1. `tests/test_claims_status_defect.py` 를 쓰고 `python3 -m unittest tests.test_claims_status_defect` 로 **단정 실패 red 를 실측**한다(0002 의 표본 원장·핸들러를 그대로 쓰므로 임포트는 성공한다). 시험만 한 커밋.
2. `INTENT_TASK=fix` 를 켠 채 `routes.py` 의 소유 판정을 「원장 `subscriber_id` 가 truthy 이고 세션 값과 같을 때만」으로 바꾼다. 시험 파일은 편집하지 않는다(protect-tests 훅이 막는다 — stdin JSON 으로 한 번 태워 BLOCKED 를 확인).
3. `make check` 전량 그린. 뮤테이션 1건: 고친 조건에서 truthy 검사를 지워(침묵 살해) 새 시험이 red 로 돌아오는지 실측 후 sha256 복원.
## Risks
- 가장 위험한 단계는 2 — 조건을 잘못 쓰면 정상 세션의 자기 건(0002 AC1)이 `not_found` 가 된다. `make check` 의 0002 시험 10건이 그것을 잡는다.
- 빈 세션을 `unauthenticated` 로 바꾸고 싶어질 수 있다 — 하지 않는다(spec carried forward). 판정 순서를 옮기면 0002 AC2 와 얽힌다.
- 하지 않은 것: 리스트 세션 예외 · 끝 개행 번호(spec Out of scope) · 세션 검증 헬퍼 신설(한 자리 수정으로 충분하다).
## Proof
- AC1 ← TestOwnerlessLedgerRow.test_ac1_ledger_row_without_subscriber_is_not_found_for_empty_session
- AC2 ← TestOwnerlessSession.test_ac2_session_without_subscriber_is_not_found_for_owned_row · test_ac2_none_on_both_sides_is_not_a_match
- 양성 대조 ← TestOwnerlessLedgerRow.test_positive_control_owned_row_still_returns_four_fields
- 출력: 단계 1 의 red 원문(FAILED, failures=3) · 단계 3 의 `make check` rc=0 원문 · 뮤테이션 red 원문, PR 본문에 첨부.
