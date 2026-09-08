"""응답 단일 통로.

규약(scripts/check_endpoints.sh 가 기계로 재는 것과 같은 문장이다):
  - 응답 직렬화는 build_response 안에서만 한다.
  - 허용 필드 목록 RESPONSE_FIELDS 는 레포 전체에서 이 한 곳에만 둔다. 이름을
    다시 묶거나(`+=` · 모듈 속성 대입) 메서드로 넓히는 것은 정의가 한 곳인 것과
    다른 명제이고, 둘 다 금지다.
  - build_response 본문은 정규 형태만 쓴다: docstring · 단일 이름 대입 · return ·
    if · raise · pass. 거른 뒤 다시 넓히는 한 줄(`allowed.update(record)`)이
    들어올 자리를 문법 차원에서 없앤다.
  - 나가는 것은 허용 목록으로 **만들어진** 딕셔너리 그 자체다. 레코드 파라미터가
    return 에 다시 나타나면 통로가 아니다.

허용 목록을 넓히는 것은 결정이지 구현이 아니다 — 이 튜플에 이름을 더하는 커밋이
곧 「그 필드를 내보내기로 했다」의 기록이다(spec 0002 R2).
"""

import json

RESPONSE_FIELDS = ("claim_id", "status", "next_step", "due_date")


def build_response(record, denied=False):
    """상류 레코드에서 허용 필드만 골라 직렬화한다."""
    if denied:
        return json.dumps({"error": "unauthenticated"}, ensure_ascii=False)
    if record is None:
        return json.dumps({"error": "not_found"}, ensure_ascii=False)
    allowed = {key: record[key] for key in RESPONSE_FIELDS if key in record}
    return json.dumps(allowed, ensure_ascii=False)
