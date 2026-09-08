"""상류 claims-core 접근 + TTL 캐시.

원장 레코드를 **거르지 않고** 그대로 돌려준다. 응답으로 나가는 필드를 고르는 것은
response.py 의 build_response 하나뿐이다(단일 통로 규약).

왜 캐시가 여기 있는가 (spec 0002 C3·C4)
---------------------------------------
상류 claims-core 는 계약상 50rps 다. 포털 트래픽을 그대로 흘리면 한도를 넘긴다.
캐시를 **통로 앞**(= 상류 접근 계층)에 두면 상류 호출이 실제로 줄고, 통로 뒤에
두면(= 조립된 응답을 캐시하면) 핸들러가 통로를 거치지 않고 반환하는 경로가 하나
생긴다. 통로를 우회하는 반환 경로를 만들어 두면 다음 사람이 그 자리에 다른 것을
넣는다 — 그래서 캐시가 거르기 전 레코드를 들고 있는 쪽을 택했다(plan 의 버린 안).

그 대가로 캐시에는 PII 가 들어 있다. 그래서 캐시는 이 모듈 밖으로 나가지 않는다:
세션에도, 디스크에도, 로그에도 넣지 않는다. 캐시를 꺼내 보여 주는 진단 함수를
누가 추가하면 그것이 통로를 우회하는 두 번째 출구이고, 백스톱의 레코드 흐름
규칙(R8)이 그 커밋을 빨갛게 만든다.
"""

import time

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

# claim_id → (만료 시각, 레코드). 프로세스 메모리를 벗어나지 않는다.
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
    """상류에서 청구 레코드를 읽는다. TTL 안이면 상류를 다시 부르지 않는다.

    `now` 를 인자로 받는 이유: 시험이 시간을 통제할 수 있어야 한다. sleep 으로
    TTL 을 재는 시험은 느리고 흔들린다. 기본값은 단조 시계다 — 벽시계를 쓰면
    시스템 시각이 뒤로 갈 때 캐시가 영원히 살아 있다.

    없는 건도 캐시한다. 없는 건을 캐시하지 않으면 존재하지 않는 ID 를 반복해
    던지는 것만으로 상류 예산을 태울 수 있다.
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
