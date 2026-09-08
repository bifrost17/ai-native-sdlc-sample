"""위반: 상류 레코드를 별칭 변수에 담아 통로를 거치지 않고 반환한다.

리터럴 grep 은 이 벡터를 놓친다 — 파일 어디에도 금지 문자열이 없고,
build_response 는 임포트까지 돼 있다.
"""

from records import fetch_claim
from response import build_response

_ROUTES = {}


def route(path):
    def _register(handler):
        _ROUTES[path] = handler
        return handler

    return _register


@route("/claims/<claim_id>/status")
def get_claim_status(claim_id, session):
    record = fetch_claim(claim_id)
    payload = record
    return payload


@route("/claims/<claim_id>/summary")
def get_claim_summary(claim_id, session):
    return build_response(fetch_claim(claim_id))
