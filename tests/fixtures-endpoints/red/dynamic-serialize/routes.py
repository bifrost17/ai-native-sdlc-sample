"""위반(V5): json 을 정적으로 임포트하지 않고 동적으로 들여와 직렬화한다.

ast.Import/ImportFrom 으로 json 을 식별하는 축은 이 이름을 못 묶는다 —
`_j` 는 그냥 지역 변수이고, 검사기는 그 변수가 무엇인지 모른다.

실행하면 상류 레코드 전량(주민번호 포함)이 감사 로그로 새어 나간다.
"""

from records import fetch_claim
from response import build_response

_j = __import__("json")

_ROUTES = {}
_AUDIT = []


def route(path):
    """이 레포의 라우트 등록 데코레이터."""

    def _register(handler):
        _ROUTES[path] = handler
        return handler

    return _register


@route("/claims/<claim_id>/status")
def get_claim_status(claim_id, session):
    """청구 상태 자가조회 — 기존 인증 세션을 거쳐서만 들어온다."""
    if session is None:
        return build_response(None)
    record = fetch_claim(claim_id)
    _AUDIT.append(_j.dumps(record, ensure_ascii=False))
    return build_response(record)
