"""접근 기록 단일 통로 — intent/0008-adjuster-claim-status/spec.md R8.

보안팀·법무 결정: 값이 실제로 나간 조회는 열람 기록을 남긴다. 남기는 것은 사정인 번호·청구 번호·
시각 **셋뿐**이고, 그 셋은 고객 개인정보가 아니라 접근 기록이라 「새 개인정보 저장 금지」와
충돌하지 않는다.

두 가지가 설계다:
- 원장 레코드를 인자로 받지 않는다. 스칼라 셋만 받으면 기록이 넓어지는 실수가 문법으로 막힌다
  (response.py 의 허용 목록과 같은 장치).
- 시각을 인자로 받는다. records.py 의 `now` 는 캐시 만료용 단조 시계라 기록의 시각이 될 수 없다 —
  섞으면 기록에 「부팅 후 12.3초」가 남는다. 호출자가 UTC 벽시계를 넘긴다.

기록을 어디에 쌓고 얼마나 보관하는가는 이 사슬의 범위 밖이다(spec Out of scope · F8②).
"""

_ACCESS = []  # 프로세스 메모리 표본. 저장소 배선은 범위 밖이다.


def access_records():
    """남은 기록의 사본 — 시험의 계기. 원본 리스트를 내주지 않는다."""
    return [dict(entry) for entry in _ACCESS]


def reset_for_test():
    _ACCESS.clear()


def record_access(adjuster_id, claim_id, at):
    """열람 한 건 = 기록 한 건. 키는 이 셋에서 늘지 않는다."""
    _ACCESS.append({"adjuster_id": adjuster_id, "claim_id": claim_id, "timestamp": at})
