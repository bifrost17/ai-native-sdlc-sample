"""배정 사정인용 라우트 + 핸들러 — intent/0008-adjuster-claim-status/spec.md R1·R3·R4·R6·R7.

스텁(계획 단계 2) — 라우트만 등록하고 고정 응답을 낸다. 계기(시험)가 우는지 먼저 재려는 것이다.
"""
from .response import error
from .routes import route


@route("/adjuster/claims/<claim_id>/status")
def get_adjuster_claim_status(claim_id, session, now=None, at=None):
    return error("not_found")
