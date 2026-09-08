"""상류 claims-core 접근 — 뼈대. 캐시는 아직 없다.

원장 레코드를 **거르지 않고** 그대로 돌려준다. 응답으로 나가는 필드를 고르는 것은
response.py 의 build_response 하나뿐이다(단일 통로 규약).
"""

CACHE_TTL_SECONDS = 60

_UPSTREAM = {
    "C-1001": {
        "claim_id": "C-1001",
        "status": "심사중",
        "next_step": "손해사정 결과 접수",
        "due_date": "2026-09-15",
        "amount_krw": 128000,
        "subscriber_rrn": "900101-1234567",
        "subscriber_name": "홍길동",
        "bank_account": "110-233-998877",
        "internal_memo": "재심사 대상 — 내부 검토중",
    },
    "C-1002": {
        "claim_id": "C-1002",
        "status": "지급완료",
        "next_step": "없음",
        "due_date": "2026-09-02",
        "amount_krw": 54000,
        "subscriber_rrn": "880303-2345678",
        "subscriber_name": "김영희",
        "bank_account": "110-233-114455",
        "internal_memo": "정상 지급",
    },
}

_CACHE = {}
_STATS = {"upstream_calls": 0}


def upstream_calls():
    """상류를 실제로 부른 횟수 — AC3 은 이 계기로 판정한다."""
    return _STATS["upstream_calls"]


def reset_for_test():
    """캐시와 계기를 비운다. 시험이 서로의 상태를 물려받지 않게 한다."""
    _CACHE.clear()
    _STATS["upstream_calls"] = 0


def fetch_claim(claim_id, now=None):
    """상류에서 청구 레코드를 읽는다. — 아직 캐시가 없다(뼈대)."""
    _STATS["upstream_calls"] += 1
    return _UPSTREAM.get(claim_id)
