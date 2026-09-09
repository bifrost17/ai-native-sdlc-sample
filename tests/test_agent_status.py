"""tests/test_agent_status.py — intent/0009-agent-proxy-claim-status/spec.md 의 AC1~AC10.

L9 625: "write the failing test first ... Commit that test. Only then ask Claude to make it pass without
editing the test." 0002·0005·0006·0007·0008 의 시험 파일은 손대지 않는다.
규율(0002 에서 이어받음): 허용 키 집합·기록 키 집합·세션 계약은 구현에서 임포트하지 않고 손으로
적는다. 예외 하나가 AC7 이다 — 「같은 값의 목록」이 아니라 「같은 목록」인지를 재려면 임포트해서
`is` 로 봐야 한다(plan.md Proof 의 결정). 시간은 now(캐시)·at(기록)을 주입해 통제한다.
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

from claims_status import adjuster_routes, agent_routes, audit, records, response, routes  # noqa: E402,F401

ROUTE = "/agent/claims/<claim_id>/status"
CUSTOMER_ROUTE = "/claims/<claim_id>/status"
ADJUSTER_ROUTE = "/adjuster/claims/<claim_id>/status"
# spec.md R1·R7 — 상담사가 보는 것은 고객이 보는 넷 그대로다(next_step 포함). 손으로 적는다.
EXPECTED_KEYS = frozenset(["claim_id", "status", "next_step", "due_date"])
# spec.md R8 의 접근 기록 키 집합 — 넷이다.
RECORD_KEYS = frozenset(["agent_id", "subscriber_id", "claim_id", "timestamp"])
# 0008 R8 의 사정인 기록 키 집합 — 셋 그대로여야 한다(spec.md R9②).
ADJUSTER_RECORD_KEYS = frozenset(["adjuster_id", "claim_id", "timestamp"])

OWN_CLAIM = "C-3001"      # 본인확인된 가입자 S-77 의 건
OTHER_CLAIM = "C-3002"    # 다른 가입자 S-12 의 건
UNKNOWN_CLAIM = "C-7777"  # 원장에 없다
SUBSCRIBER = "S-77"
AGENT_ID = "E-4410"
VERIFIED_AT = "2026-09-09T03:30:00+00:00"
AT = "2026-09-09T04:00:00+00:00"
# spec.md Design 의 세션 계약을 손으로 옮긴 것. 핸들러가 읽는 키는 앞의 셋뿐이다(R6).
SESSION = {"role": "agent", "agent_id": AGENT_ID,
           "verified_subscriber_id": SUBSCRIBER, "verified_at": VERIFIED_AT}
UNVERIFIED_SESSION = {"role": "agent", "agent_id": AGENT_ID}  # 콘솔이 표시를 지운 세션
CUSTOMER_SESSION = {"subscriber_id": SUBSCRIBER}
ADJUSTER_SESSION = {"role": "adjuster", "adjuster_id": "A-3391"}
ADJUSTER_CLAIM = "C-2001"  # 0008 의 표본 — AC9② 에서만 쓴다

UNAUTHENTICATED = {"error": "unauthenticated"}
NOT_FOUND = {"error": "not_found"}
VERIFICATION_REQUIRED = {"error": "verification_required"}
INVALID = {"error": "invalid_claim_id"}
# 원장에는 있지만 상담 화면에 절대 나오면 안 되는 값들. next_step 은 여기 없다 — 고객이 보는
# 값이라 상담사도 본다(클레임 운영팀장·법무 결정).
FORBIDDEN_VALUES = ("900101-1234567", "110-233-998877", "상담 이력 다수", "홍길동")


class Base(unittest.TestCase):
    """0008 의 Base 와 같은 격리다. `audit.reset_for_test()` 가 빠지면 넷짜리 기록이 남아
    0008 의 AC8(리스트 전량에 len==1·키 셋)이 우리 때문에 빨개진다 — plan.md Risks."""

    def setUp(self):
        self._backup = copy.deepcopy(records._UPSTREAM)
        records.reset_for_test()
        audit.reset_for_test()

    def tearDown(self):
        records._UPSTREAM.clear()
        records._UPSTREAM.update(self._backup)
        records.reset_for_test()
        audit.reset_for_test()

    def body(self, claim_id=OWN_CLAIM, session=SESSION, now=0.0, at=AT):
        return routes.ROUTES[ROUTE](claim_id, session, now=now, at=at)

    def customer_body(self, claim_id=OWN_CLAIM, session=CUSTOMER_SESSION, now=0.0):
        return routes.ROUTES[CUSTOMER_ROUTE](claim_id, session, now=now)


class TestSurfaceIsReachable(Base):
    """양성 대조 — 계기가 실제로 무언가에 닿아 있는지."""

    def test_agent_handler_is_registered_under_the_route(self):
        self.assertIn(ROUTE, routes.ROUTES)

    def test_upstream_carries_the_new_subscriber_rows(self):
        self.assertEqual(records._UPSTREAM[OWN_CLAIM]["subscriber_id"], SUBSCRIBER)
        self.assertEqual(records._UPSTREAM[OTHER_CLAIM]["subscriber_id"], "S-12")
        self.assertNotIn(UNKNOWN_CLAIM, records._UPSTREAM)
        for claim_id in (OWN_CLAIM, OTHER_CLAIM):
            self.assertFalse(records._UPSTREAM[claim_id].get("adjuster_id"),
                             "이 행들은 사정인 경로에서 보이면 안 된다 (0008 R6)")


class TestAC1SameAsCustomer(Base):
    def test_ac1_agent_body_is_byte_identical_to_customer_body(self):
        agent = self.body()
        customer = self.customer_body()
        self.assertEqual(agent, customer,
                         "상담사가 읽어 주는 말과 고객 화면의 말이 갈렸다")

    def test_ac1_body_has_exactly_four_fields_with_values(self):
        payload = json.loads(self.body())
        self.assertEqual(set(payload), set(EXPECTED_KEYS))
        for key, value in payload.items():
            self.assertTrue(value, "%s 가 비어 있다" % key)


class TestAC2NoSession(Base):
    def test_ac2_no_session_returns_unauthenticated_without_upstream_call(self):
        self.assertEqual(json.loads(self.body(session=None)), UNAUTHENTICATED)
        self.assertEqual(records.upstream_calls(), 0)
        self.assertEqual(audit.access_records(), [])


class TestAC3NonAgentSession(Base):
    def test_ac3_customer_and_adjuster_sessions_are_not_found_without_upstream_call(self):
        for session in (CUSTOMER_SESSION, ADJUSTER_SESSION, {}, {"role": "supervisor"}):
            with self.subTest(session=session):
                self.assertEqual(json.loads(self.body(session=session)), NOT_FOUND)
        self.assertEqual(records.upstream_calls(), 0)
        self.assertEqual(audit.access_records(), [])

    def test_ac3_session_without_agent_id_is_not_found(self):
        for agent_id in (None, "", "__absent__"):
            session = dict(SESSION)
            if agent_id == "__absent__":
                del session["agent_id"]
            else:
                session["agent_id"] = agent_id
            with self.subTest(agent_id=agent_id):
                self.assertEqual(json.loads(self.body(session=session)), NOT_FOUND)
        self.assertEqual(records.upstream_calls(), 0)
        self.assertEqual(audit.access_records(), [])


class TestAC4VerificationRequired(Base):
    def test_ac4_missing_marker_returns_verification_required_without_upstream_call(self):
        # 조회하는 번호는 원장에 **없는** 번호다. 게이트가 상류 뒤로 내려가면 문구는 그대로인데
        # 상류가 불린다 — 그 자리를 잡는 계기는 문구가 아니라 호출 수다(spec F5·plan M5).
        for marker in (None, "", "__absent__"):
            session = dict(SESSION)
            if marker == "__absent__":
                del session["verified_subscriber_id"]
            else:
                session["verified_subscriber_id"] = marker
            with self.subTest(marker=marker):
                body = self.body(claim_id=UNKNOWN_CLAIM, session=session)
                self.assertEqual(json.loads(body), VERIFICATION_REQUIRED)
        self.assertEqual(records.upstream_calls(), 0,
                         "본인확인 게이트가 상류 조회보다 뒤에 있다")
        self.assertEqual(audit.access_records(), [])

    def test_ac4_same_body_for_known_unknown_and_malformed_claim_ids(self):
        known = self.body(claim_id=OWN_CLAIM, session=UNVERIFIED_SESSION)
        unknown = self.body(claim_id=UNKNOWN_CLAIM, session=UNVERIFIED_SESSION)
        malformed = self.body(claim_id="C-3001\n", session=UNVERIFIED_SESSION)
        self.assertEqual(json.loads(known), VERIFICATION_REQUIRED)
        self.assertEqual(known, unknown)
        self.assertEqual(known, malformed)
        self.assertEqual(records.upstream_calls(), 0)


class TestAC5Ownership(Base):
    def test_ac5_other_customers_claim_and_unknown_claim_share_one_body(self):
        other = self.body(claim_id=OTHER_CLAIM)
        unknown = self.body(claim_id=UNKNOWN_CLAIM)
        self.assertEqual(json.loads(other), NOT_FOUND)
        self.assertEqual(other, unknown)
        for secret in FORBIDDEN_VALUES:
            self.assertNotIn(secret, other)
        self.assertEqual(audit.access_records(), [])

    def test_ac5_empty_subscriber_on_either_side_is_not_a_match(self):
        # (가) 원장 쪽이 비어 있다 — 정상 세션으로도 보이면 안 된다.
        for ledger_value in ("__absent__", None, ""):
            records._UPSTREAM[OWN_CLAIM] = dict(self._backup[OWN_CLAIM])
            if ledger_value == "__absent__":
                del records._UPSTREAM[OWN_CLAIM]["subscriber_id"]
            else:
                records._UPSTREAM[OWN_CLAIM]["subscriber_id"] = ledger_value
            records.reset_for_test()
            with self.subTest(ledger_value=ledger_value):
                self.assertEqual(json.loads(self.body()), NOT_FOUND,
                                 "빈 가입자 표시끼리 일치로 판정됐다 (intent 0005)")
        # (나) 양쪽이 다 비어 있다 — 게이트가 먼저 닫으므로 원장에 닿지도 않는다.
        records.reset_for_test()
        session = dict(SESSION, verified_subscriber_id="")
        self.assertEqual(json.loads(self.body(session=session)), VERIFICATION_REQUIRED)
        self.assertEqual(records.upstream_calls(), 0)
        self.assertEqual(audit.access_records(), [])

    def test_ac5_malformed_claim_id_is_rejected_without_echo(self):
        bad = "C-3001' OR 1=1 --"
        body = self.body(claim_id=bad)
        self.assertEqual(json.loads(body), INVALID)
        self.assertNotIn(bad, body)
        self.assertNotIn("OR 1=1", body)
        self.assertEqual(json.loads(self.body(claim_id="C-3001\n")), INVALID)
        self.assertEqual(records.upstream_calls(), 0)
        self.assertEqual(audit.access_records(), [])


class TestAC6ExpiryIsNotMeasuredHere(Base):
    def test_ac6_response_is_the_same_for_any_verified_at_including_absent(self):
        """만료의 소유자는 콘솔이다(spec R6·F4). 이 모듈이 시각을 읽으면 안 된다."""
        baseline = self.body()
        self.assertEqual(set(json.loads(baseline)), set(EXPECTED_KEYS))
        for verified_at in ("2020-01-01T00:00:00+00:00", "2999-12-31T23:59:59+00:00",
                            "방금", 12345, None, "__absent__"):
            session = dict(SESSION)
            if verified_at == "__absent__":
                del session["verified_at"]
            else:
                session["verified_at"] = verified_at
            with self.subTest(verified_at=verified_at):
                self.assertEqual(self.body(session=session), baseline,
                                 "이 모듈이 확인 시각을 읽고 있다 — 만료는 콘솔 소유다")


class TestAC7SharedAllowlist(Base):
    def test_ac7_agent_path_uses_the_customer_allowlist_object(self):
        # 값 비교가 아니라 객체 동일성이다 — 리터럴 복사본은 `==` 를 통과한 뒤 고객 목록만
        # 넓어질 때 조용히 뒤처진다(plan.md Proof 의 결정).
        self.assertIs(agent_routes.RESPONSE_FIELDS, response.RESPONSE_FIELDS)
        self.assertIs(routes.RESPONSE_FIELDS, response.RESPONSE_FIELDS)

    def test_ac7_new_upstream_field_does_not_widen_the_response_and_pii_never_appears(self):
        records._UPSTREAM[OWN_CLAIM]["settlement_agent_ssn"] = "770707-2222222"
        records._UPSTREAM[OWN_CLAIM]["payout_account"] = "110-233-000000"
        records.reset_for_test()
        body = self.body()
        self.assertEqual(set(json.loads(body)), set(EXPECTED_KEYS))
        for secret in FORBIDDEN_VALUES + ("770707-2222222", "110-233-000000"):
            self.assertNotIn(secret, body)


class TestAC8AccessRecord(Base):
    def test_ac8_successful_read_appends_one_record_of_exactly_four_keys(self):
        body = self.body()
        entries = audit.access_records()
        self.assertEqual(len(entries), 1)
        self.assertEqual(set(entries[0]), set(RECORD_KEYS))
        self.assertEqual(entries[0]["agent_id"], AGENT_ID)
        self.assertEqual(entries[0]["subscriber_id"], SUBSCRIBER)
        self.assertEqual(entries[0]["claim_id"], OWN_CLAIM)
        self.assertEqual(entries[0]["timestamp"], AT, "주입한 시각이 그대로 실리지 않았다")
        # 기록은 「무엇을 봤다」지 「무엇이 보였다」가 아니다.
        payload = json.loads(body)
        blob = json.dumps(entries, ensure_ascii=False)
        for value in FORBIDDEN_VALUES + (payload["status"], payload["next_step"],
                                         payload["due_date"]):
            self.assertNotIn(value, blob, "기록이 넓어졌다: %s" % value)

    def test_ac8_failed_lookups_append_nothing(self):
        self.body(session=None)
        self.body(session=CUSTOMER_SESSION)
        self.body(session=UNVERIFIED_SESSION)
        self.body(claim_id=OTHER_CLAIM)
        self.body(claim_id=UNKNOWN_CLAIM)
        self.body(claim_id="C-3001\n")
        self.assertEqual(audit.access_records(), [])


class TestAC9EarlierPathsUnchanged(Base):
    def test_ac9_adjuster_record_still_has_exactly_three_keys(self):
        routes.ROUTES[ADJUSTER_ROUTE](ADJUSTER_CLAIM, ADJUSTER_SESSION, now=0.0, at=AT)
        entries = audit.access_records()
        self.assertEqual(len(entries), 1)
        self.assertEqual(set(entries[0]), set(ADJUSTER_RECORD_KEYS),
                         "상담사 기록이 넷이라고 사정인 기록까지 넓어졌다 (0008 R8)")

    def test_ac9_agent_session_on_customer_route_is_not_found_and_records_nothing(self):
        # 상담사 세션에는 `subscriber_id` 키가 없다 — 0002 핸들러가 통과시키면 접근 기록이
        # 없는 조회 경로가 생긴다(spec F1). 콘솔 팀이 키를 바꾸면 이 시험이 먼저 빨개진다.
        body = routes.ROUTES[CUSTOMER_ROUTE](OWN_CLAIM, SESSION, now=0.0)
        self.assertEqual(json.loads(body), NOT_FOUND)
        self.assertEqual(audit.access_records(), [])


class TestAC10SharedCache(Base):
    def test_ac10_agent_lookup_reuses_the_customer_cache_within_ttl(self):
        self.customer_body(now=0.0)
        self.assertEqual(records.upstream_calls(), 1)
        self.body(now=30.0)
        self.assertEqual(records.upstream_calls(), 1, "상담사 경로가 고객 캐시를 안 쓴다")
        self.body(now=61.0)
        self.assertEqual(records.upstream_calls(), 2, "TTL 이 지나도 상류를 다시 안 부른다")


if __name__ == "__main__":
    unittest.main()
