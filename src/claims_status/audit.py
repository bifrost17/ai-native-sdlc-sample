"""접근 기록 단일 통로 — intent/0008-adjuster-claim-status/spec.md R8 · intent/0009-agent-proxy-claim-status/spec.md R8.

보안팀·법무 결정: 값이 실제로 나간 조회는 열람 기록을 남긴다. 남기는 것은 사정인 경로가 사정인
번호·청구 번호·시각 **셋뿐**(0008 R8), 상담사 경로가 상담사 사번·고객 가입자 번호·청구 번호·
시각 **넷뿐**(0009 R8)이고, 그 값들은 고객 개인정보가 아니라 접근 기록이라 「새 개인정보 저장
금지」와 충돌하지 않는다. 청중마다 키 집합이 닫혀 있고, 그래서 함수도 청중마다 하나다 — 한
함수에 인자를 더하면 키 집합이 호출자에 따라 달라진다(0009 plan.md 의 안 고른 선택지 ①).

두 가지가 설계다:
- 원장 레코드를 인자로 받지 않는다. 스칼라만 받으면 기록이 넓어지는 실수가 문법으로 막힌다
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


def record_agent_access(agent_id, subscriber_id, claim_id, at):
    """열람 한 건 = 기록 한 건. 키는 이 넷에서 늘지 않는다 — intent/0009 spec R8.

    사정인용 `record_access` 에 인자를 더하지 않고 함수를 하나 더 둔다: 기본값을 주면 기록의
    키 집합이 호출자에 따라 달라지고, 안 주면 사정인 기록이 넷이 되어 0008 AC8(키가 정확히
    셋)이 깨진다. 청중마다 키 집합이 닫혀 있어야 넓히는 실수가 문법으로 막힌다(plan.md ①).
    """
    _ACCESS.append({"agent_id": agent_id, "subscriber_id": subscriber_id,
                    "claim_id": claim_id, "timestamp": at})

