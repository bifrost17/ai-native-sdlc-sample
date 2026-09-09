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
    # 배정 표본 — 「담당 사정인」 칸은 두 필드다(intent/0008 spec F7): 번호가 정본, 이름은 판정에
    # 쓰지 않는다. 기존 두 행은 0002·0005·0006·0007 의 시험이 전제를 잡고 있어 손대지 않는다.
    "C-2001": {
        "claim_id": "C-2001", "subscriber_id": "S-77", "status": "심사중",
        "next_step": "손해사정 결과 접수", "due_date": "2026-09-18",
        "adjuster_id": "A-3391", "adjuster_name": "이수진",
        "subscriber_rrn": "900101-1234567", "subscriber_name": "홍길동",
        "bank_account": "110-233-998877", "internal_memo": "재심사 대상 — 내부 검토중",
    },
    "C-2002": {
        "claim_id": "C-2002", "subscriber_id": "S-12", "status": "보완요청",
        "next_step": "서류 보완 대기", "due_date": "2026-09-25",
        "adjuster_id": "A-7742", "adjuster_name": "박준호",
        "subscriber_rrn": "880303-2345678", "subscriber_name": "김영희",
        "bank_account": "110-233-114455", "internal_memo": "보완 서류 미도착",
    },
    # 담당 사정인 칸이 빈 행 — 어느 사정인에게도 보이지 않아야 한다(spec R6).
    "C-2003": {
        "claim_id": "C-2003", "subscriber_id": "S-12", "status": "접수",
        "next_step": "서류 검토", "due_date": "2026-09-30",
        "adjuster_id": "", "adjuster_name": "",
        "subscriber_rrn": "880303-2345678", "subscriber_name": "김영희",
        "bank_account": "110-233-114455", "internal_memo": "접수 직후",
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


def fetch_claim(claim_id, now=None, *, cached):
    """TTL 안이면 캐시, 아니면 상류. 없는 건은 캐시하지 않는다 — intent/0006: 「없음」을 60초 들고 있으면
    그 사이 원장에 생긴 건이 not_found 로 보인다(없는 번호 반복 조회의 상류 예산은 0006 spec F1 로 넘겼다).

    `now` 는 시험이 시간을 통제하려고 주입한다; 기본은 단조 시계(벽시계가 뒤로 가도 캐시가 영생하지 않게).

    `cached` 는 기본값 없는 필수 키워드다 — intent/0008 spec F1·R7. 사정인 경로는 `cached=False` 로
    부르고 배정을 매번 원장에서 다시 읽는다(이관된 사정인이 60초 더 보면 안 된다). 기본값을 두면
    인자를 잊은 호출자가 조용히 낡은 **권한**으로 판정한다 — response.build_response 의 필드 인자를
    필수로 둔 것과 같은 이유다. `cached=False` 도 받은 레코드로 캐시를 갱신한다(고객 경로가 더
    신선해질 뿐 나빠지지 않는다).
    """
    if now is None:
        now = time.monotonic()
    if cached:
        hit = _CACHE.get(claim_id)
        if hit is not None and now < hit[0]:
            return hit[1]
    _STATS["upstream_calls"] += 1
    record = _UPSTREAM.get(claim_id)
    if record is not None:
        # 스냅샷을 든다. 실제 상류는 응답마다 새 객체를 주므로 캐시에 든 것은 그 시점의 사본이지
        # 원장 행 자체가 아니다. 표본에서 `_UPSTREAM` 의 dict 를 그대로 들면 원장이 바뀔 때 캐시를
        # 통해서도 그 변화가 보여 캐시가 실물보다 신선해진다 — 캐시 우회(0008 R7)를 잴 수 없게 된다.
        record = dict(record)
        _CACHE[claim_id] = (now + CACHE_TTL_SECONDS, record)
    return record
