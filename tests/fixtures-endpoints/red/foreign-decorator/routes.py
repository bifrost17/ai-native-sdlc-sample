"""위반(V2): 라우트를 「등록 어휘 목록」에 없는 데코레이터로 붙인다.

@route 만 핸들러로 세는 검사기는 @app.get 으로 붙은 핸들러를 아예 못 본다 —
못 본 핸들러에는 「통로를 거쳐 반환하라」는 규칙이 적용되지 않는다.
등록 어휘(프레임워크가 정한다)를 열거하는 축은 이 자리에서 죽는다.

실행하면 /admin/claims/<id> 가 상류 레코드를 통째로 돌려준다.
"""

from records import fetch_claim
from response import build_response

_ROUTES = {}


def route(path):
    """이 레포의 라우트 등록 데코레이터."""

    def _register(handler):
        _ROUTES[path] = handler
        return handler

    return _register


class _App:
    """프레임워크 흉내 — 자기 등록 데코레이터를 들고 온다."""

    def get(self, path):
        def _register(handler):
            _ROUTES[path] = handler
            return handler

        return _register


app = _App()


@route("/claims/<claim_id>/status")
def get_claim_status(claim_id, session):
    """청구 상태 자가조회 — 기존 인증 세션을 거쳐서만 들어온다."""
    if session is None:
        return build_response(None)
    record = fetch_claim(claim_id)
    return build_response(record)


@app.get("/admin/claims/<claim_id>")
def admin_get_claim(claim_id, session):
    return fetch_claim(claim_id)
