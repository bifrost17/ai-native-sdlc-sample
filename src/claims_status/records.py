"""상류 claims-core 접근 + TTL 캐시 — spec 0002 R5. (스텁: 표본 원장만 있고 조회·캐시는 구현 전)"""

CACHE_TTL_SECONDS = 60

# 상류 원장 표본. 주민번호·계좌·내부 메모·이름은 원장에 있지만 포털로 나가면 안 되는 값(spec R3).
_UPSTREAM = {
    "C-1001": {
        "claim_id": "C-1001", "subscriber_id": "S-77", "status": "심사중",
        "next_step": "손해사정 결과 접수", "due_date": "2026-09-15",
        "subscriber_rrn": "900101-1234567", "subscriber_name": "홍길동",
        "bank_account": "110-233-998877", "internal_memo": "재심사 대상 — 내부 검토중",
    },
    "C-1002": {
        "claim_id": "C-1002", "subscriber_id": "S-12", "status": "지급완료",
        "next_step": "없음", "due_date": "2026-09-02",
        "subscriber_rrn": "880303-2345678", "subscriber_name": "김영희",
        "bank_account": "110-233-114455", "internal_memo": "정상 지급",
    },
}
_STATS = {"upstream_calls": 0}


def upstream_calls():
    return _STATS["upstream_calls"]


def reset_for_test():
    _STATS["upstream_calls"] = 0


def fetch_claim(claim_id, now=None):
    return None
