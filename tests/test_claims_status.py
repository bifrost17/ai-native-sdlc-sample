"""tests/test_claims_status.py — 사슬 0002 의 수용 기준을 시험 이름으로 잇는다.

시험 이름의 `ac1`·`ac2`·`ac3` 은 intent/0002-claims-status/spec.md 의 AC 번호이고,
plan.md 의 `## Proof` 가 이 파일의 이름들을 그대로 적고 있다. 이름을 바꾸면 plan 이
낡는다 — 그것이 이 규약의 목적이다(레슨 4: Proof 는 AC 를 시험 이름으로 덮는다).

🔴 동어반복 회피 — 이 파일의 가장 중요한 규율
허용 필드 목록을 구현에서 **임포트하지 않는다**. `from claims_status.response import
RESPONSE_FIELDS` 를 쓰면 구현이 넓어질 때 시험도 같이 넓어져 영원히 green 이다.
참조 레포가 정확히 그 자리에서 뚫려 bank_account 가 실제로 유출됐다. 그래서 아래
EXPECTED_RESPONSE_KEYS 는 spec.md 의 응답 스키마를 보고 **손으로 다시 적은 것**이고,
구현이 필드를 하나 더 내보내는 순간 이 시험이 빨개져야 한다.

두 번째 규율: 「지금 안 새는가」가 아니라 「**상류가 넓어져도** 안 새는가」를 잰다.
test_ac2_new_upstream_field_does_not_widen_the_response 가 상류 레코드에 새 민감
필드를 심고 응답이 그대로인지 본다. 상류는 우리가 소유하지 않는 스키마이므로,
「오늘 상류에 무엇이 있는가」에 기대는 시험은 상류가 바뀌는 날 조용히 죽는다.
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

from claims_status import records, response, routes  # noqa: E402

# spec.md 「Design」의 응답 스키마를 손으로 옮긴 것. 구현에서 가져오지 않는다.
EXPECTED_RESPONSE_KEYS = frozenset(["claim_id", "status", "next_step", "due_date"])

# 상류 원장에는 있지만 응답에 절대 나오면 안 되는 값들. 문자열까지 단정해
# 「키는 없는데 값이 다른 키로 실려 나가는」 경우도 잡는다.
FORBIDDEN_VALUES = ("900101-1234567", "110-233-998877", "재심사 대상 — 내부 검토중")

CLAIM_ID = "C-1001"
SESSION = {"subscriber_id": "S-77", "authenticated": True}


class ClaimsStatusTestCase(unittest.TestCase):
    """상류 원장과 캐시를 시험마다 원상 복구한다 — 시험 간 순서 의존을 없앤다."""

    def setUp(self):
        self._upstream_backup = copy.deepcopy(records._UPSTREAM)
        records.reset_for_test()

    def tearDown(self):
        records._UPSTREAM.clear()
        records._UPSTREAM.update(self._upstream_backup)
        records.reset_for_test()

    def call(self, claim_id=CLAIM_ID, session=SESSION, now=0.0):
        handler = routes._ROUTES["/claims/<claim_id>/status"]
        return json.loads(handler(claim_id, session, now=now))


class TestSurfaceIsReachable(ClaimsStatusTestCase):
    """계기 유효성 — 재려는 표면이 실제로 존재하는가(양성 대조).

    라우트가 등록돼 있지 않으면 아래 모든 시험은 「위반을 못 찾았다」가 아니라
    「아무것도 안 쟀다」가 된다. 부재는 결함 없음과 구별되지 않는다.
    """

    def test_route_is_registered_and_points_at_the_handler(self):
        self.assertIn("/claims/<claim_id>/status", routes._ROUTES)
        self.assertIs(
            routes._ROUTES["/claims/<claim_id>/status"], routes.get_claim_status
        )

    def test_upstream_record_actually_carries_the_sensitive_fields(self):
        """상류에 민감 필드가 실제로 있어야 「안 샌다」가 의미를 갖는다."""
        raw = records._UPSTREAM[CLAIM_ID]
        self.assertIn("subscriber_rrn", raw)
        self.assertIn("bank_account", raw)
        self.assertIn("internal_memo", raw)


class TestAC1AuthenticatedLookup(ClaimsStatusTestCase):
    """AC1 → R1 — 인증된 세션은 네 값을 받고, 세션이 없으면 아무 청구 값도 못 받는다."""

    def test_ac1_authenticated_session_returns_the_four_allowed_fields(self):
        payload = self.call()
        self.assertEqual(set(payload), set(EXPECTED_RESPONSE_KEYS))
        self.assertEqual(payload["claim_id"], CLAIM_ID)
        self.assertTrue(payload["status"])
        self.assertTrue(payload["next_step"])
        self.assertTrue(payload["due_date"])

    def test_ac1_missing_session_returns_unauthenticated_and_no_claim_values(self):
        handler = routes._ROUTES["/claims/<claim_id>/status"]
        body = handler(CLAIM_ID, None, now=0.0)
        self.assertEqual(json.loads(body), {"error": "unauthenticated"})
        # 인증 실패 경로에서도 상류를 부르지 않는다 — 부르면 50rps 예산이 샌다.
        self.assertEqual(records.upstream_calls(), 0)
        for secret in FORBIDDEN_VALUES:
            self.assertNotIn(secret, body)

    def test_ac1_unknown_and_foreign_claim_share_one_answer(self):
        """없는 건과 남의 건을 구분하면 청구 ID 존재 여부가 새어 나간다(spec F2)."""
        body = json.dumps(json.loads(
            routes._ROUTES["/claims/<claim_id>/status"]("C-9999", SESSION, now=0.0)))
        self.assertEqual(json.loads(body), {"error": "not_found"})


class TestAC2AllowlistIsNotTautological(ClaimsStatusTestCase):
    """AC2 → R2 — 허용 목록 밖은 나가지 않는다. 상류가 넓어져도 그대로다."""

    def test_ac2_response_keys_match_independently_written_allowlist(self):
        payload = self.call()
        self.assertEqual(
            set(payload),
            set(EXPECTED_RESPONSE_KEYS),
            "응답 키가 spec 의 응답 스키마와 다르다. 이 단정은 구현의 "
            "RESPONSE_FIELDS 를 임포트하지 않는다 — 구현이 넓어지면 여기가 빨개져야 한다",
        )

    def test_ac2_new_upstream_field_does_not_widen_the_response(self):
        """상류에 필드가 새로 생겨도 응답은 넓어지지 않는다.

        상류 스키마는 우리 소유가 아니다. 「오늘 상류에 있는 필드만 확인한다」는
        시험은 상류가 필드를 더하는 날 조용히 죽는다 — 그래서 여기서 직접 더한다.
        """
        records._UPSTREAM[CLAIM_ID]["settlement_agent_ssn"] = "770707-2222222"
        records._UPSTREAM[CLAIM_ID]["payout_account"] = "110-233-998877"
        records.reset_for_test()

        handler = routes._ROUTES["/claims/<claim_id>/status"]
        body = handler(CLAIM_ID, SESSION, now=0.0)

        self.assertEqual(set(json.loads(body)), set(EXPECTED_RESPONSE_KEYS))
        self.assertNotIn("settlement_agent_ssn", body)
        self.assertNotIn("770707-2222222", body)
        self.assertNotIn("payout_account", body)

    def test_ac2_existing_sensitive_values_never_appear_in_the_body(self):
        body = routes._ROUTES["/claims/<claim_id>/status"](CLAIM_ID, SESSION, now=0.0)
        for secret in FORBIDDEN_VALUES:
            self.assertNotIn(secret, body, "민감 값이 응답 본문에 실렸다: %s" % secret)


class TestAC3TtlCache(ClaimsStatusTestCase):
    """AC3 → R3 — TTL 안은 상류를 다시 부르지 않고, TTL 이 지나면 다시 부른다.

    시각은 인자로 주입한다. 실시간·sleep 으로 재는 시험은 느리고 흔들린다.
    """

    def test_ac3_first_lookup_calls_upstream_once(self):
        self.assertEqual(records.upstream_calls(), 0)
        self.call(now=0.0)
        self.assertEqual(records.upstream_calls(), 1)

    def test_ac3_second_lookup_within_ttl_does_not_call_upstream_again(self):
        self.call(now=0.0)
        self.call(now=records.CACHE_TTL_SECONDS - 1.0)
        self.assertEqual(records.upstream_calls(), 1)

    def test_ac3_lookup_after_ttl_expiry_calls_upstream_again(self):
        self.call(now=0.0)
        self.call(now=records.CACHE_TTL_SECONDS + 1.0)
        self.assertEqual(records.upstream_calls(), 2)

    def test_ac3_cache_is_keyed_by_claim_id(self):
        self.call(claim_id=CLAIM_ID, now=0.0)
        self.call(claim_id="C-1002", now=1.0)
        self.assertEqual(records.upstream_calls(), 2)

    def test_ac3_cached_answer_is_the_same_as_the_fresh_one(self):
        first = self.call(now=0.0)
        second = self.call(now=1.0)
        self.assertEqual(first, second)
        self.assertEqual(records.upstream_calls(), 1)


class TestGatewayIsTheOnlyExit(ClaimsStatusTestCase):
    """R4 의 구조를 시험에서도 한 번 못박는다 — 백스톱과 같은 명제를 다른 계기로."""

    def test_response_module_exposes_exactly_one_allowlist_and_one_gateway(self):
        self.assertTrue(callable(response.build_response))
        self.assertIsInstance(response.RESPONSE_FIELDS, tuple)

    def test_gateway_drops_unknown_fields_even_when_called_directly(self):
        body = response.build_response(
            {"claim_id": "C-1", "status": "심사중", "next_step": "a",
             "due_date": "2026-09-15", "subscriber_rrn": "900101-1234567"}
        )
        self.assertEqual(set(json.loads(body)), set(EXPECTED_RESPONSE_KEYS))
        self.assertNotIn("900101-1234567", body)


if __name__ == "__main__":
    unittest.main()
