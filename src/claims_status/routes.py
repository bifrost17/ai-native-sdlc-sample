"""라우트 등록은 이 파일에서만 한다(단일 등록처 규약)."""

from .records import fetch_claim
from .response import build_response

_ROUTES = {}


def route(path):
    """이 레포의 라우트 등록 데코레이터."""

    def _register(handler):
        _ROUTES[path] = handler
        return handler

    return _register


@route("/claims/<claim_id>/status")
def get_claim_status(claim_id, session, now=None):
    """청구 상태 자가조회 — 포털의 기존 인증 세션으로만 들어온다."""
    if session is None:
        return build_response(None, denied=True)
    record = fetch_claim(claim_id, now=now)
    return build_response(record)
