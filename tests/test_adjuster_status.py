"""tests/test_adjuster_status.py — intent/0008-adjuster-claim-status/spec.md 의 AC1~AC10.

L9 625: "write the failing test first ... Commit that test. Only then ask Claude to make it pass without
editing the test." 0002·0005·0006·0007 의 시험 파일은 손대지 않는다.
규율 하나(0002 에서 이어받음): 허용 키 집합·닫힌 status 집합·기록 키 집합은 구현에서 임포트하지
않는다 — 구현이 넓어지면 여기가 빨개져야 한다. 시간은 now(캐시)·at(기록)을 주입해 통제한다.
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

from claims_status import adjuster_routes, audit, records, routes  # noqa: E402,F401

ROUTE = "/adjuster/claims/<claim_id>/status"
CUSTOMER_ROUTE = "/claims/<claim_id>/status"
# spec.md Design 의 사정인 응답 스키마를 손으로 옮긴 것. 구현에서 가져오지 않는다.
EXPECTED_KEYS = frozenset(["claim_id", "status", "due_date"])
# spec.md R8 의 접근 기록 키 집합 — 셋뿐이다.
RECORD_KEYS = frozenset(["adjuster_id", "claim_id", "timestamp"])
# spec.md R10 의 닫힌 status 집합.
STATUS_SET = frozenset(["접수", "심사중", "보완요청", "지급완료", "종결"])

ASSIGNED_CLAIM = "C-2001"    # 사정인 A-3391 에게 배정된 건
OTHER_CLAIM = "C-2002"       # 다른 사정인 A-7742 의 건
UNASSIGNED_CLAIM = "C-2003"  # 원장의 담당 사정인 칸이 비어 있는 건
UNKNOWN_CLAIM = "C-8888"     # 원장에 없다
ADJUSTER = "A-3391"
OTHER_ADJUSTER = "A-7742"
SESSION = {"role": "adjuster", "adjuster_id": ADJUSTER}
OTHER_SESSION = {"role": "adjuster", "adjuster_id": OTHER_ADJUSTER}
CUSTOMER_SESSION = {"subscriber_id": "S-77"}
NOT_FOUND = {"error": "not_found"}
AT = "2026-09-09T04:00:00+00:00"
# 원장에는 있지만 사정인 화면에 절대 나오면 안 되는 값들 — 다음 단계(내부 처리 단계)를 포함한다.
FORBIDDEN_VALUES = ("손해사정 결과 접수", "900101-1234567", "110-233-998877",
                    "재심사 대상", "홍길동", "이수진")


class Base(unittest.TestCase):
    def setUp(self):
        self._backup = copy.deepcopy(records._UPSTREAM)
        records.reset_for_test()
        audit.reset_for_test()

    def tearDown(self):
        records._UPSTREAM.clear()
        records._UPSTREAM.update(self._backup)
        records.reset_for_test()
        audit.reset_for_test()

    def body(self, claim_id=ASSIGNED_CLAIM, session=SESSION, now=0.0, at=AT):
        return routes.ROUTES[ROUTE](claim_id, session, now=now, at=at)

    def call(self, **kw):
        return json.loads(self.body(**kw))


class TestSurfaceIsReachable(Base):
    """양성 대조 — 재려는 표면이 실제로 있어야 아래 시험이 「안 쟀다」가 되지 않는다."""

    def test_adjuster_handler_is_registered_under_the_route(self):
        self.assertIn(ROUTE, routes.ROUTES)
        self.assertIs(routes.ROUTES[ROUTE], adjuster_routes.get_adjuster_claim_status)
        self.assertIsNot(routes.ROUTES[ROUTE], routes.ROUTES[CUSTOMER_ROUTE])

    def test_upstream_rows_carry_the_assignment_fields(self):
        self.assertEqual(records._UPSTREAM[ASSIGNED_CLAIM]["adjuster_id"], ADJUSTER)
        self.assertIn("adjuster_name", records._UPSTREAM[ASSIGNED_CLAIM])
        self.assertEqual(records._UPSTREAM[OTHER_CLAIM]["adjuster_id"], OTHER_ADJUSTER)
        self.assertFalse(records._UPSTREAM[UNASSIGNED_CLAIM]["adjuster_id"])


class TestAC1AssignedClaim(Base):
    def test_ac1_assigned_claim_returns_exactly_three_fields(self):
        payload = self.call()
        self.assertEqual(set(payload), set(EXPECTED_KEYS))
        self.assertEqual(payload["claim_id"], ASSIGNED_CLAIM)
        for key in ("status", "due_date"):
            self.assertTrue(payload[key], "%s 가 비어 있다" % key)


class TestAC2NoSession(Base):
    def test_ac2_no_session_returns_unauthenticated_without_upstream_call(self):
        body = self.body(session=None)
        self.assertEqual(json.loads(body), {"error": "unauthenticated"})
        self.assertEqual(records.upstream_calls(), 0)
        self.assertEqual(audit.access_records(), [])


class TestAC3NonAdjusterSession(Base):
    def test_ac3_customer_session_is_not_found_without_upstream_call(self):
        self.assertEqual(self.call(session=CUSTOMER_SESSION), NOT_FOUND)
        self.assertEqual(records.upstream_calls(), 0, "고객 세션이 상류까지 갔다")

    def test_ac3_session_without_adjuster_id_is_not_found_without_upstream_call(self):
        for session in ({"role": "adjuster"},
                        {"role": "adjuster", "adjuster_id": None},
                        {"role": "adjuster", "adjuster_id": ""},
                        {"adjuster_id": ADJUSTER},
                        {}, []):
            with self.subTest(session=session):
                records.reset_for_test()
                self.assertEqual(self.call(session=session), NOT_FOUND)
                self.assertEqual(records.upstream_calls(), 0)


class TestAC4NotFound(Base):
    def test_ac4_unassigned_and_unknown_claim_share_one_body(self):
        other = self.body(claim_id=OTHER_CLAIM)
        unassigned = self.body(claim_id=UNASSIGNED_CLAIM)
        unknown = self.body(claim_id=UNKNOWN_CLAIM)
        self.assertEqual(json.loads(other), NOT_FOUND)
        self.assertEqual(other, unknown, "남의 배정 건과 없는 건의 응답이 다르다")
        self.assertEqual(unassigned, unknown)
        for value in FORBIDDEN_VALUES:
            self.assertNotIn(value, other)

    def test_ac4_malformed_claim_id_is_rejected_without_echo(self):
        for bad in ("C-2001' OR 1=1 --", "C-2001\n", "", "C-", "c-2001"):
            with self.subTest(claim_id=bad):
                records.reset_for_test()
                body = self.body(claim_id=bad)
                self.assertEqual(json.loads(body), {"error": "invalid_claim_id"})
                # 빈 문자열은 어떤 문자열에도 들어 있으므로 되비침 단정이 항진명제가 된다.
                # 대신 오류 본문이 고정 문자열 그대로인지를 위 줄이 이미 못 박는다.
                if bad:
                    self.assertNotIn(bad, body)
                self.assertEqual(records.upstream_calls(), 0)
                self.assertEqual(audit.access_records(), [])


class TestAC5Allowlist(Base):
    def test_ac5_new_upstream_field_does_not_widen_the_response(self):
        records._UPSTREAM[ASSIGNED_CLAIM]["settlement_agent_ssn"] = "770707-2222222"
        records._UPSTREAM[ASSIGNED_CLAIM]["payout_account"] = "110-233-000000"
        body = self.body()
        self.assertEqual(set(json.loads(body)), set(EXPECTED_KEYS))
        self.assertNotIn("770707-2222222", body)
        self.assertNotIn("110-233-000000", body)

    def test_ac5_next_step_and_pii_never_appear_in_the_body(self):
        body = self.body()
        self.assertNotIn("next_step", body, "다음 단계가 사정인 화면으로 나갔다")
        for value in FORBIDDEN_VALUES:
            self.assertNotIn(value, body, "나가면 안 되는 값이 본문에 실렸다: %s" % value)


class TestAC6AssignmentMatch(Base):
    def test_ac6_empty_assignment_is_not_a_match_on_either_side(self):
        """0005 규칙 — 어느 한쪽이 비면 불일치다. None == None 이 배정이 되면 안 된다."""
        for ledger_value in (None, "", "__delete__"):
            for session_value in (None, ""):
                with self.subTest(ledger=ledger_value, session=session_value):
                    records._UPSTREAM[ASSIGNED_CLAIM] = dict(self._backup[ASSIGNED_CLAIM])
                    if ledger_value == "__delete__":
                        del records._UPSTREAM[ASSIGNED_CLAIM]["adjuster_id"]
                    else:
                        records._UPSTREAM[ASSIGNED_CLAIM]["adjuster_id"] = ledger_value
                    records.reset_for_test()
                    session = {"role": "adjuster", "adjuster_id": session_value}
                    self.assertEqual(self.call(session=session), NOT_FOUND)
                    self.assertEqual(audit.access_records(), [])

    def test_ac6_matching_name_with_different_number_is_not_found(self):
        """이름은 판정에 쓰지 않는다 — 동명이인이 남의 건을 보면 안 된다."""
        name = records._UPSTREAM[ASSIGNED_CLAIM]["adjuster_name"]
        session = {"role": "adjuster", "adjuster_id": "A-0000", "adjuster_name": name}
        self.assertEqual(self.call(session=session), NOT_FOUND)


class TestAC7ReassignmentIsImmediate(Base):
    def test_ac7_reassignment_within_ttl_flips_both_sides(self):
        """TTL(60초) 안에 이관해도 옛 사정인은 즉시 못 보고 새 사정인은 즉시 본다 — spec F1."""
        self.assertEqual(set(self.call(now=0.0)), set(EXPECTED_KEYS))
        records._UPSTREAM[ASSIGNED_CLAIM]["adjuster_id"] = OTHER_ADJUSTER
        self.assertEqual(self.call(now=30.0), NOT_FOUND, "이관된 옛 사정인이 아직 본다")
        payload = self.call(session=OTHER_SESSION, now=30.0)
        self.assertEqual(set(payload), set(EXPECTED_KEYS), "새 사정인이 아직 못 본다")


class TestAC8AccessRecord(Base):
    def test_ac8_successful_read_appends_one_record_of_exactly_three_keys(self):
        body = self.body()
        entries = audit.access_records()
        self.assertEqual(len(entries), 1)
        self.assertEqual(set(entries[0]), set(RECORD_KEYS))
        self.assertEqual(entries[0]["adjuster_id"], ADJUSTER)
        self.assertEqual(entries[0]["claim_id"], ASSIGNED_CLAIM)
        self.assertEqual(entries[0]["timestamp"], AT, "주입한 시각이 그대로 실리지 않았다")
        # 기록에 실려야 하는 것은 위 셋뿐이다. 청구 번호는 그 셋에 들어 있고(entity), 응답으로
        # 나간 상태·예정일은 들어 있으면 안 된다 — 기록은 「무엇을 봤다」지 「무엇이 보였다」가 아니다.
        payload = json.loads(body)
        blob = json.dumps(entries, ensure_ascii=False)
        for value in FORBIDDEN_VALUES + (payload["status"], payload["due_date"]):
            self.assertNotIn(value, blob, "기록이 넓어졌다: %s" % value)

    def test_ac8_failed_lookups_append_nothing(self):
        self.body(session=None)
        self.body(session=CUSTOMER_SESSION)
        self.body(claim_id=OTHER_CLAIM)
        self.body(claim_id=UNKNOWN_CLAIM)
        self.body(claim_id="C-2001\n")
        self.assertEqual(audit.access_records(), [])


class TestAC9CustomerPathUnchanged(Base):
    def test_ac9_customer_path_leaves_no_access_record(self):
        payload = json.loads(routes.ROUTES[CUSTOMER_ROUTE]("C-1001", {"subscriber_id": "S-77"},
                                                           now=0.0))
        self.assertEqual(set(payload), {"claim_id", "status", "next_step", "due_date"})
        self.assertEqual(audit.access_records(), [])


class TestAC10StatusVocabulary(Base):
    def test_ac10_every_sample_row_status_is_in_the_closed_set(self):
        for claim_id, row in records._UPSTREAM.items():
            with self.subTest(claim_id=claim_id):
                self.assertIn(row["status"], STATUS_SET,
                              "닫힌 집합 밖의 status 다 — 반출 허가는 다섯 값에만 있다")


if __name__ == "__main__":
    unittest.main()
