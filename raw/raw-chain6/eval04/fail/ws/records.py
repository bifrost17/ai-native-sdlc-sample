"""상류 claims-core 접근 + TTL 캐시 — intent/0002-claims-status/spec.md R5.

원장 레코드를 거르지 않고 그대로 돌려준다; 필드를 고르는 것은 response.py 하나다.
캐시는 거르기 전 레코드를 들고 있으므로 이 모듈 밖으로 꺼내 보이지 않는다(로그·진단 함수 금지).
"""
import time

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
_CACHE = {}  # claim_id → (만료 시각, 레코드 또는 None). 프로세스 메모리를 벗어나지 않는다.
_STATS = {"upstream_calls": 0}


def upstream_calls():
    """상류를 실제로 부른 횟수 — AC5 의 계기."""
    return _STATS["upstream_calls"]


def reset_for_test():
    _CACHE.clear()
    _STATS["upstream_calls"] = 0


def fetch_claim(claim_id, now=None):
    """TTL 안이면 캐시, 아니면 상류. 없는 건도 캐시한다(없는 번호 반복 조회로 예산을 태우지 못하게).

    `now` 는 시험이 시간을 통제하려고 주입한다; 기본은 단조 시계(벽시계가 뒤로 가도 캐시가 영생하지 않게).
    """
    if now is None:
        now = time.monotonic()
    cached = _CACHE.get(claim_id)
    if cached is not None and now < cached[0]:
        return cached[1]
    _STATS["upstream_calls"] += 1
    record = _UPSTREAM.get(claim_id)
    _CACHE[claim_id] = (now + CACHE_TTL_SECONDS, record)
    return record
