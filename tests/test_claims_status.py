"""tests/test_claims_status.py — intent/0002-claims-status/spec.md 의 AC1~AC5 를 시험 이름으로.

L9 625: "write the failing test first ... Only then ask Claude to make it pass without editing the test."
규율 하나: 허용 키 집합은 구현에서 임포트하지 않는다 — 구현이 넓어지면 여기가 빨개져야 한다.
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
# spec.md Design 의 응답 스키마를 손으로 옮긴 것. 구현에서 가져오지 않는다.
EXPECTED_KEYS = frozenset(["claim_id", "status", "next_step", "due_date"])
# 원장에는 있지만 응답에 절대 나오면 안 되는 값들(키가 바뀌어 실려 나가는 경우까지 잡는다).
PII_VALUES = ("900101-1234567", "110-233-998877", "재심사 대상", "홍길동")

OWN_CLAIM = "C-1001"      # subscriber S-77 의 건
FOREIGN_CLAIM = "C-1002"  # 다른 가입자의 건
UNKNOWN_CLAIM = "C-9999"
SESSION = {"subscriber_id": "S-77"}


class Base(unittest.TestCase):
    def setUp(self):
        self._backup = copy.deepcopy(records._UPSTREAM)
        records.reset_for_test()

    def tearDown(self):
        records._UPSTREAM.clear()
        records._UPSTREAM.update(self._backup)
        records.reset_for_test()

    def body(self, claim_id=OWN_CLAIM, session=SESSION, now=0.0):
        return routes.ROUTES[ROUTE](claim_id, session, now=now)

    def call(self, **kw):
        return json.loads(self.body(**kw))


class TestSurfaceIsReachable(Base):
    """양성 대조 — 재려는 표면이 실제로 있어야 아래 시험이 「안 쟀다」가 되지 않는다."""

    def test_handler_is_registered_under_the_route(self):
        self.assertIn(ROUTE, routes.ROUTES)
        self.assertIs(routes.ROUTES[ROUTE], routes.get_claim_status)

    def test_upstream_record_carries_the_pii_fields(self):
        raw = records._UPSTREAM[OWN_CLAIM]
        for key in ("subscriber_rrn", "bank_account", "internal_memo", "subscriber_id"):
            self.assertIn(key, raw)


class TestAC1OwnClaim(Base):
    def test_ac1_own_claim_returns_exactly_the_four_fields(self):
        payload = self.call()
        self.assertEqual(set(payload), set(EXPECTED_KEYS))
        self.assertEqual(payload["claim_id"], OWN_CLAIM)
        for key in ("status", "next_step", "due_date"):
            self.assertTrue(payload[key], "%s 가 비어 있다" % key)


class TestAC2NoSession(Base):
    def test_ac2_no_session_returns_unauthenticated_without_upstream_call(self):
        body = self.body(session=None)
        self.assertEqual(json.loads(body), {"error": "unauthenticated"})
        self.assertEqual(records.upstream_calls(), 0)
        for secret in PII_VALUES:
            self.assertNotIn(secret, body)


class TestAC3Allowlist(Base):
    def test_ac3_new_upstream_field_does_not_widen_the_response(self):
        records._UPSTREAM[OWN_CLAIM]["settlement_agent_ssn"] = "770707-2222222"
        records._UPSTREAM[OWN_CLAIM]["payout_account"] = "110-233-000000"
        body = self.body()
        self.assertEqual(set(json.loads(body)), set(EXPECTED_KEYS))
        self.assertNotIn("settlement_agent_ssn", body)
        self.assertNotIn("770707-2222222", body)
        self.assertNotIn("110-233-000000", body)

    def test_ac3_pii_values_never_appear_in_the_body(self):
        body = self.body()
        for secret in PII_VALUES:
            self.assertNotIn(secret, body, "민감 값이 본문에 실렸다: %s" % secret)


class TestAC4NotFound(Base):
    def test_ac4_foreign_and_unknown_claim_share_one_body(self):
        foreign = self.body(claim_id=FOREIGN_CLAIM)
        unknown = self.body(claim_id=UNKNOWN_CLAIM)
        self.assertEqual(json.loads(foreign), {"error": "not_found"})
        self.assertEqual(foreign, unknown)
        for secret in PII_VALUES:
            self.assertNotIn(secret, foreign)

    def test_ac4_malformed_claim_id_is_rejected_without_echo(self):
        bad = "C-1001' OR 1=1 --"
        body = self.body(claim_id=bad)
        self.assertEqual(json.loads(body), {"error": "invalid_claim_id"})
        self.assertNotIn(bad, body)
        self.assertNotIn("OR 1=1", body)
        self.assertEqual(records.upstream_calls(), 0)


class TestAC5TtlCache(Base):
    def test_ac5_second_lookup_within_ttl_does_not_call_upstream(self):
        self.call(now=0.0)
        self.call(now=59.0)
        self.assertEqual(records.upstream_calls(), 1)

    def test_ac5_lookup_after_ttl_calls_upstream_again(self):
        self.call(now=0.0)
        self.call(now=59.0)
        self.call(now=61.0)
        self.assertEqual(records.upstream_calls(), 2)


if __name__ == "__main__":
    unittest.main()
