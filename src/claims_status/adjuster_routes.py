"""배정 사정인용 라우트 + 핸들러 — intent/0008-adjuster-claim-status/spec.md R1·R3·R4·R6·R7·R8.

세션 → 사정인 여부 → 청구 번호 형식 → 상류 조회 → 배정 판정 → 통로 → 기록.
고객 경로(routes.py)와 파일을 가르되 상류 문(records.py)·응답 문(response.py)·기록 문(audit.py)은
하나씩만 쓴다. 청중이 다른 것은 허용 목록과 캐시 정책뿐이다.
"""
import datetime

from .audit import record_access
from .records import fetch_claim
from .response import ADJUSTER_FIELDS, build_response, error
from .routes import CLAIM_ID_RE, route


def _utc_now():
    """기록의 시각은 벽시계다 — records.py 의 단조 시계와 다른 시계(spec R8)."""
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


@route("/adjuster/claims/<claim_id>/status")
def get_adjuster_claim_status(claim_id, session, now=None, at=None):
    """사정인 자가조회 — 포털의 기존 사정인 세션으로만 들어온다(새 토큰·권한 없음)."""
    if session is None:
        return error("unauthenticated")
    # 사정인 세션이 아니면 남의 건과 같은 답이다 — 고객 세션도 여기서는 아무것도 보지 못한다(R3).
    if not isinstance(session, dict) or session.get("role") != "adjuster":
        return error("not_found")
    adjuster_id = session.get("adjuster_id")
    if not adjuster_id:
        return error("not_found")
    if not isinstance(claim_id, str) or not CLAIM_ID_RE.match(claim_id):
        return error("invalid_claim_id")
    # cached=False 는 이 경로의 정책이다 — 이관은 다음 조회부터 즉시다(R7·spec F1).
    record = fetch_claim(claim_id, now=now, cached=False)
    # 빈 배정 표시(없음·None·"")는 어느 쪽이든 불일치다 — None == None 이 배정이 되면 안 된다(0005).
    # 판정은 사정인 번호로만 한다; adjuster_name 은 겹치므로 읽지 않는다(R6).
    assigned = record.get("adjuster_id") if record is not None else None
    if not assigned or assigned != adjuster_id:
        return error("not_found")
    body = build_response(record, ADJUSTER_FIELDS)
    # 값이 나가는 것이 확정된 뒤에만 남긴다 — 「열람 기록」이므로(R8·spec F8①).
    record_access(adjuster_id, claim_id, at if at is not None else _utc_now())
    return body
