Note: intent·spec 이 아직 draft(같은 PR 안, 머지 전)다. 엔지니어(부모 세션)가 2026-09-09 이슈 #24 해결을 지시해 draft 위에서 계획한다(plan Inputs 「one exception」) — 승인은 이 PR 의 머지다.
# Plan: 청구 번호 형식 검사를 문자열 끝까지 (from intent.md 2026-09-09)
Upstream: spec.md@2e5099ce4a341b16da2946a0b3e418c8891e4346. Status: draft.
## Files that change
- tests/test_claims_status_format.py (new) — spec AC1~AC4 를 시험 이름으로. 0002·0005·0006 의 시험 파일은 건드리지 않는다.
- src/claims_status/routes.py — `CLAIM_ID_RE` 상수 한 줄(앵커).
- 그 밖엔 없다. 새 모듈도, 새 헬퍼도, 새 오류 문구도 없다.
## Order of work
1. `tests/test_claims_status_format.py` 를 쓰고 `python3 -m unittest tests.test_claims_status_format` 로 **단정 실패 red 를 실측**한다(0002 의 표본 원장·핸들러를 그대로 쓰므로 임포트는 성공한다). AC3·AC4 는 현행에서도 통과한다 — 기존 행동의 계약 고정이고, red 는 AC1·AC2 에서만 난다. 시험만 한 커밋.
2. `INTENT_TASK=fix` 를 켠 채 `routes.py` 의 `CLAIM_ID_RE` 를 `r"\AC-[0-9]+\Z"` 로 바꾼다. 시험 파일은 편집하지 않는다(protect-tests 훅이 막는다 — stdin JSON 으로 한 번 태워 BLOCKED 를 확인한다).
3. `make check` 전량 그린. 뮤테이션 1건: 앵커를 `^…$` 로 되돌려(침묵 살해) 새 시험이 red 로 돌아오는지 실측한 뒤 복원한다.
4. README 의 사슬 표에 0007 행(defect · 티켓 · 이슈 #24 · PR 번호)을 더한다 — PR 을 연 뒤 실제 번호로 쓴다.
## Risks
- 가장 위험한 단계는 2 — 앵커를 잘못 쓰면(예: `\A` 만, 또는 `\Z` 대신 `\z` 오타로 `re.error`) 정상 번호 조회(0002 AC1)까지 `invalid_claim_id` 가 되거나 임포트가 깨진다. `make check` 의 0002 시험 10건과 새 시험의 양성 대조(AC4)가 그것을 잡는다.
- 입력을 `strip()` 해서 통과시키고 싶어질 수 있다 — 하지 않는다(spec F1: 형식 규칙 변경은 포털·보안 결정).
- 형식 검사를 세션 검사 앞으로 옮기고 싶어질 수 있다 — 하지 않는다. 0002 AC2(세션 `None` → 상류 0)와 얽힌다.
- 하지 않은 것: 세션이 dict 가 아닐 때의 예외(이슈 #25) · 미스 조회의 상류 예산(이슈 #26) · eval 추가(사슬 0006 은 인시던트라 eval 을 더했다; 이 건은 티켓 결함이라 사슬 0005 와 같이 회귀 시험까지다).
## Proof
- AC1 ← TestTrailingNewlineClaimId.test_ac1_trailing_newline_is_invalid_without_upstream_call · test_ac1_trailing_newline_with_empty_session_is_invalid
- AC2 ← TestTrailingNewlineClaimId.test_ac2_error_body_does_not_echo_input_or_ledger_values
- AC3 ← TestNeighbouringMalformedIds.test_ac3_neighbouring_malformed_ids_stay_invalid_without_upstream_call
- AC4 ← TestFormatPositiveControl.test_ac4_well_formed_id_still_returns_four_fields · test_ac4_unknown_well_formed_id_is_not_found_after_one_upstream_call
- 출력: 단계 1 의 red 원문(FAILED, failures=3 — AC1 두 건과 AC2) · 단계 3 의 `make check` rc=0 원문 · 뮤테이션 red 원문 · protect-tests 훅 BLOCKED 원문, PR 본문에 첨부.
