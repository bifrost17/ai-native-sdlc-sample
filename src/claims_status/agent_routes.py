"""상담사 대리 조회용 라우트 + 핸들러 — intent/0009-agent-proxy-claim-status/spec.md R1·R3·R4·R5·R7·R8·R10.

스텁 — 시험 먼저(L9 625). 라우트만 등록하고 아무것도 판정하지 않는다.
"""
from .audit import record_agent_access  # noqa: F401
from .records import fetch_claim  # noqa: F401
from .response import RESPONSE_FIELDS, build_response, error  # noqa: F401
from .routes import CLAIM_ID_RE, route  # noqa: F401


@route("/agent/claims/<claim_id>/status")
def get_agent_claim_status(claim_id, session, now=None, at=None):
    """상담사 대리 조회 — 본인확인을 마친 통화의 상담사 콘솔 세션으로만 들어온다."""
    return error("not_found")
