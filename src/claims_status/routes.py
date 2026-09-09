"""라우트 등록 + 핸들러 — spec 0002 R1·R2·R4. (스텁: 등록만 있고 핸들러는 구현 전)"""

ROUTES = {}


def route(path):
    def _register(handler):
        ROUTES[path] = handler
        return handler
    return _register


@route("/claims/<claim_id>/status")
def get_claim_status(claim_id, session, now=None):
    return "{}"
