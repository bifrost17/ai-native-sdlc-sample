"""라우트 등록 + 핸들러 — intent/0002-claims-status/spec.md R1·R2·R4.

세션 → 청구 번호 형식 → 상류 조회 → 소유 판정 → 통로. 남의 건과 없는 건은 같은 not_found(존재 여부가 새지 않게).
"""
import re

from .records import fetch_claim
from .response import build_response, error

CLAIM_ID_RE = re.compile(r"^C-[0-9]+$")
ROUTES = {}


def route(path):
    def _register(handler):
        ROUTES[path] = handler
        return handler
    return _register


@route("/claims/<claim_id>/status")
def get_claim_status(claim_id, session, now=None):
    """청구 상태 자가조회 — 포털의 기존 인증 세션으로만 들어온다(새 토큰·권한 없음)."""
    if session is None:
        return error("unauthenticated")
    if not isinstance(claim_id, str) or not CLAIM_ID_RE.match(claim_id):
        return error("invalid_claim_id")
    record = fetch_claim(claim_id, now=now)
    if record is None or record.get("subscriber_id") != session.get("subscriber_id"):
        return error("not_found")
    return build_response(record)
