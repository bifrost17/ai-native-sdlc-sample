"""라우트 등록 + 핸들러 — intent/0002-claims-status/spec.md R1·R2·R4.

세션 → 청구 번호 형식 → 상류 조회 → 소유 판정 → 통로. 남의 건과 없는 건은 같은 not_found(존재 여부가 새지 않게).
"""
import re

from .records import fetch_claim
from .response import build_response, error

# `$` 는 문자열 끝 개행 앞에서도 맞는다 — "C-1001\n" 이 형식을 통과해 상류를 부르던 자리(intent 0007).
# 문자열 끝에서만 맞는 앵커를 쓴다; 이 상수를 손볼 때 `$` 로 되돌리지 않는다.
CLAIM_ID_RE = re.compile(r"\AC-[0-9]+\Z")
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
    # 빈 가입자 표시(None·"")는 어느 쪽이든 불일치다 — None == None 이 소유가 되면 안 된다(intent 0005).
    owner = record.get("subscriber_id") if record is not None else None
    if not owner or owner != session.get("subscriber_id"):
        return error("not_found")
    return build_response(record)
