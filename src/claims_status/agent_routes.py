"""상담사 대리 조회용 라우트 + 핸들러 — intent/0009-agent-proxy-claim-status/spec.md R1·R3·R4·R5·R7·R8·R10.

세션 → 상담사 여부 → 본인확인 표시 → 청구 번호 형식 → 상류 조회 → 소유 판정 → 통로 → 기록.
고객 경로(routes.py)·사정인 경로(adjuster_routes.py)와 파일을 가르되 상류 문(records.py)·응답
문(response.py)·기록 문(audit.py)은 하나씩만 쓴다.

두 가지가 앞선 두 청중과 다르고, 둘 다 요구다:
- 허용 목록을 **공유한다**. 0008 은 사정인용 상수를 새로 만들었지만(덜 본다), 상담사는 고객이
  보는 것을 그대로 본다 — 목록이 하나여야 「똑같은 값」이 구조로 성립한다(R7). 복사하지 않는다.
- 캐시는 고객 경로와 **같다**(`cached=True`, R10). 사정인 경로가 캐시를 우회한 이유는 배정이
  권한이어서인데, 여기서 자격을 정하는 것은 세션의 본인확인 표시이고 그것은 캐시를 타지 않는다.

만료는 이 모듈이 재지 않는다(R6). 콘솔이 통화 종료·30분에 세션의 표시를 지우고, 지워진 세션은
표시 없음으로 닫힌다. 그래서 `verified_at` 은 계약에는 있어도 여기서 읽지 않는다 — 읽으면
만료의 소유자가 둘이 된다.
"""
import datetime

from .audit import record_agent_access
from .records import fetch_claim
from .response import RESPONSE_FIELDS, build_response, error
from .routes import CLAIM_ID_RE, route


def _utc_now():
    """기록의 시각은 벽시계다 — records.py 의 단조 시계와 다른 시계(R8, 0008 과 같은 자리).

    `at` 을 주지 않은 호출이 기록에 `None` 을 남기지 않게 한다. 시험은 `at` 을 주입해 시간을
    통제하고, 배선된 호출자는 이 기본값을 쓴다.
    """
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


@route("/agent/claims/<claim_id>/status")
def get_agent_claim_status(claim_id, session, now=None, at=None):
    """상담사 대리 조회 — 본인확인을 마친 통화의 상담사 콘솔 세션으로만 들어온다."""
    if session is None:
        return error("unauthenticated")
    # 상담사 세션이 아니면 남의 건과 같은 답이다 — 고객 세션도 사정인 세션도 여기서는
    # 아무것도 보지 못한다(R3). 0008 과 같은 규칙.
    if not isinstance(session, dict) or session.get("role") != "agent":
        return error("not_found")
    if not session.get("agent_id"):
        return error("not_found")
    # 본인확인 표시가 선행 조건이다(R4). 이 판정은 청구 번호를 보기 전에, 세션만으로 끝난다 —
    # 그래서 원장의 어떤 것도 흘리지 않고, 이 줄을 상류 조회 아래로 옮기면 문구는 그대로인 채
    # 존재 여부가 상류 접근으로 샌다(spec F5). AC4 가 상류 호출 수 0 으로 그 자리를 잡는다.
    verified = session.get("verified_subscriber_id")
    if not verified:
        return error("verification_required")
    if not isinstance(claim_id, str) or not CLAIM_ID_RE.match(claim_id):
        return error("invalid_claim_id")
    # cached=True 는 이 경로의 정책이다 — 고객 경로와 같은 캐시(R10).
    record = fetch_claim(claim_id, now=now, cached=True)
    # 빈 가입자 표시(None·"")는 어느 쪽이든 불일치다 — None == None 이 소유가 되면 안 된다
    # (intent 0005). 세션 쪽이 비는 갈래는 위 게이트가 이미 닫았다.
    owner = record.get("subscriber_id") if record is not None else None
    if not owner or owner != verified:
        return error("not_found")
    body = build_response(record, RESPONSE_FIELDS)
    # 값이 나가는 것이 확정된 뒤에만 남긴다 — 「열람 기록」이므로(R8·spec F7).
    record_agent_access(session["agent_id"], verified, claim_id,
                        at if at is not None else _utc_now())
    return body
