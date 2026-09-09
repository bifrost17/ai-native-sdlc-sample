"""tests/test_claims_status_defect.py — intent/0005-ownerless-claim-visible/spec.md 의 AC1·AC2.

L9 625: "write the failing test first ... Commit that test. Only then ask Claude to make it pass without
editing the test." 티켓 경로의 결함 시험 — 0002 의 tests/test_claims_status.py 는 손대지 않는다.
결함: 원장 행의 subscriber_id 와 세션의 subscriber_id 가 둘 다 비어 있으면 None == None 으로 소유 판정이 통과한다.
"""
import copy
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
OWNER_SESSION = {"subscriber_id": "S-77"}
NOT_FOUND = {"error": "not_found"}
# 이 건의 원장 값 — 본문에 실리면 청구 건이 나간 것이다(구현에서 임포트하지 않고 손으로 옮겼다).
LEDGER_VALUES = ("심사중", "손해사정 결과 접수", "2026-09-15")


class Base(unittest.TestCase):
    def setUp(self):
        self._backup = copy.deepcopy(records._UPSTREAM)
        records.reset_for_test()

    def tearDown(self):
        records._UPSTREAM.clear()
        records._UPSTREAM.update(self._backup)
        records.reset_for_test()

    def body(self, session, claim_id=CLAIM):
        return routes.ROUTES[ROUTE](claim_id, session, now=0.0)

    def assert_not_found(self, body):
        self.assertEqual(json.loads(body), NOT_FOUND)
        for value in LEDGER_VALUES:
            self.assertNotIn(value, body, "원장 값이 본문에 실렸다: %s" % value)


class TestOwnerlessLedgerRow(Base):
    def test_positive_control_owned_row_still_returns_four_fields(self):
        """양성 대조 — 정상 세션의 자기 건은 네 필드가 돌아온다(아래 시험이 「안 쟀다」가 되지 않게)."""
        payload = json.loads(self.body(OWNER_SESSION))
        self.assertEqual(set(payload), {"claim_id", "status", "next_step", "due_date"})

    def test_ac1_ledger_row_without_subscriber_is_not_found_for_empty_session(self):
        del records._UPSTREAM[CLAIM]["subscriber_id"]
        self.assert_not_found(self.body({}))


class TestOwnerlessSession(Base):
    def test_ac2_session_without_subscriber_is_not_found_for_owned_row(self):
        self.assert_not_found(self.body({"subscriber_id": None}))
        self.assert_not_found(self.body({}))

    def test_ac2_none_on_both_sides_is_not_a_match(self):
        records._UPSTREAM[CLAIM]["subscriber_id"] = None
        self.assert_not_found(self.body({"subscriber_id": None}))


if __name__ == "__main__":
    unittest.main()
