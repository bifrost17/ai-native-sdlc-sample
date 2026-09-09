"""tests/test_claims_status_incident.py — intent/0006-claims-status-stale-not-found/spec.md AC1·AC2.

L10 693: "Each production incident gets an eval ... and stays in the suite as a regression test."
L9 625: "write the failing test first ... Only then ask Claude to make it pass without editing the test."
인시던트: 원장에 없던 번호를 한 번 조회하면 「없음」이 60초 캐시돼, 그 사이 원장에 생긴 건이 not_found 로 보였다.
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
EXPECTED_KEYS = frozenset(["claim_id", "status", "next_step", "due_date"])  # 구현에서 가져오지 않는다.
SESSION = {"subscriber_id": "S-77"}
NEW_CLAIM = "C-1003"  # 시험 시작 시점엔 원장에 없다 — 양성 대조가 그것을 잰다.
NEW_RECORD = {"claim_id": NEW_CLAIM, "subscriber_id": "S-77", "status": "접수",
              "next_step": "서류 검토", "due_date": "2026-09-20"}


class TestIncidentStaleNotFound(unittest.TestCase):
    def setUp(self):
        self._backup = copy.deepcopy(records._UPSTREAM)
        records.reset_for_test()

    def tearDown(self):
        records._UPSTREAM.clear()
        records._UPSTREAM.update(self._backup)
        records.reset_for_test()

    def call(self, claim_id, now):
        return json.loads(routes.ROUTES[ROUTE](claim_id, SESSION, now=now))

    def test_positive_control_new_claim_is_absent_before_filing(self):
        self.assertNotIn(NEW_CLAIM, records._UPSTREAM)
        self.assertEqual(self.call(NEW_CLAIM, now=0.0), {"error": "not_found"})

    def test_ac1_claim_created_after_a_miss_is_visible_on_the_next_lookup(self):
        self.assertEqual(self.call(NEW_CLAIM, now=0.0), {"error": "not_found"})
        records._UPSTREAM[NEW_CLAIM] = dict(NEW_RECORD)  # 원장에 건이 생긴다 (TTL 60초 안)
        payload = self.call(NEW_CLAIM, now=30.0)
        self.assertEqual(set(payload), set(EXPECTED_KEYS), "원장에 생긴 건이 아직 not_found 다: %r" % payload)
        self.assertEqual(payload["claim_id"], NEW_CLAIM)
        self.assertEqual(records.upstream_calls(), 2)

    def test_ac2_existing_claim_is_still_served_from_cache_within_ttl(self):
        self.call("C-1001", now=0.0)
        self.call("C-1001", now=59.0)
        self.assertEqual(records.upstream_calls(), 1)


if __name__ == "__main__":
    unittest.main()
