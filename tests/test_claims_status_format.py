"""tests/test_claims_status_format.py — intent/0007-claim-id-trailing-newline/spec.md 의 AC1~AC4.

L9 625: "write the failing test first ... Commit that test. Only then ask Claude to make it pass without
editing the test." 티켓 경로(이슈 #24)의 결함 시험 — 0002·0005·0006 의 시험 파일은 손대지 않는다.
결함: `^C-[0-9]+$` 의 `$` 가 문자열 끝 개행 앞에서도 맞아 "C-1001\n" 이 형식 검사를 통과하고 상류를 1회 부른다.
"""
import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from claims_status import records, routes  # noqa: E402

ROUTE = "/claims/<claim_id>/status"
CLAIM = "C-1001"  # 표본 원장에서 subscriber S-77 의 건
UNKNOWN_CLAIM = "C-9999"  # 형식은 맞고 원장에 없다
OWNER_SESSION = {"subscriber_id": "S-77"}
INVALID = {"error": "invalid_claim_id"}
NOT_FOUND = {"error": "not_found"}
EXPECTED_KEYS = frozenset(["claim_id", "status", "next_step", "due_date"])  # 구현에서 가져오지 않는다.
# 이 건의 원장 값 — 오류 본문에 실리면 안 된다(구현에서 임포트하지 않고 손으로 옮겼다).
LEDGER_VALUES = ("심사중", "손해사정 결과 접수", "2026-09-15")


class Base(unittest.TestCase):
    def setUp(self):
        records.reset_for_test()

    def tearDown(self):
        records.reset_for_test()

    def body(self, claim_id, session=OWNER_SESSION):
        return routes.ROUTES[ROUTE](claim_id, session, now=0.0)


class TestTrailingNewlineClaimId(Base):
    def test_ac1_trailing_newline_is_invalid_without_upstream_call(self):
        body = self.body(CLAIM + "\n")
        self.assertEqual(json.loads(body), INVALID)
        self.assertEqual(records.upstream_calls(), 0, "형식이 틀린 번호가 상류까지 갔다")

    def test_ac1_trailing_newline_with_empty_session_is_invalid(self):
        """세션이 비어도 형식 단계에서 끊긴다 — 소유 판정의 not_found 로 덮이지 않는다."""
        body = self.body(CLAIM + "\n", session={})
        self.assertEqual(json.loads(body), INVALID)
        self.assertEqual(records.upstream_calls(), 0)

    def test_ac2_error_body_does_not_echo_input_or_ledger_values(self):
        bad = CLAIM + "\n"
        body = self.body(bad)
        self.assertNotIn(bad, body)
        self.assertNotIn("\\n", body)
        self.assertNotIn(CLAIM, body)
        for value in LEDGER_VALUES:
            self.assertNotIn(value, body, "원장 값이 본문에 실렸다: %s" % value)


class TestNeighbouringMalformedIds(Base):
    def test_ac3_neighbouring_malformed_ids_stay_invalid_without_upstream_call(self):
        """이웃 입력은 현행에서도 걸린다 — 앵커를 바꾼 뒤에도 그대로여야 한다(계약 고정)."""
        for bad in ("\n" + CLAIM, CLAIM + "\nX", CLAIM + "\r", CLAIM + "\n\n", "", "C-", "c-1001"):
            with self.subTest(claim_id=bad):
                records.reset_for_test()
                self.assertEqual(json.loads(self.body(bad)), INVALID)
                self.assertEqual(records.upstream_calls(), 0)


class TestFormatPositiveControl(Base):
    def test_ac4_well_formed_id_still_returns_four_fields(self):
        """양성 대조 — 정상 번호는 그대로다(위 시험이 「아무것도 통과 못 한다」가 되지 않게)."""
        payload = json.loads(self.body(CLAIM))
        self.assertEqual(set(payload), set(EXPECTED_KEYS))
        self.assertEqual(records.upstream_calls(), 1)

    def test_ac4_unknown_well_formed_id_is_not_found_after_one_upstream_call(self):
        self.assertEqual(json.loads(self.body(UNKNOWN_CLAIM)), NOT_FOUND)
        self.assertEqual(records.upstream_calls(), 1)


if __name__ == "__main__":
    unittest.main()
