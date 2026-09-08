"""위반: 응답 직렬화를 build_response 통로 밖에서 한다."""

import json

from records import fetch_claim
from response import build_response

_ROUTES = {}
_AUDIT = []


def route(path):
    def _register(handler):
        _ROUTES[path] = handler
        return handler

    return _register


@route("/claims/<claim_id>/status")
def get_claim_status(claim_id, session):
    record = fetch_claim(claim_id)
    _AUDIT.append(json.dumps(record, ensure_ascii=False))
    return build_response(record)
