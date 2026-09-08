"""위반(V1): 통로 안에서 허용 목록을 적용한 **뒤** 원본 레코드를 도로 합친다.

R2(「통로 본문에 RESPONSE_FIELDS 라는 이름이 등장하는가」)는 이 코드를 통과시킨다 —
이름은 등장하고, 필터도 실제로 돌고, 그 결과가 한 줄 뒤에 무의미해질 뿐이다.
이름 등장 여부가 아니라 통로의 **형태**를 봐야 잡힌다.

실행하면 subscriber_rrn·internal_memo 가 그대로 응답에 실린다.
"""

import json

RESPONSE_FIELDS = ("claim_id", "status", "updated_at")


def build_response(record):
    """상류 레코드에서 허용 필드만 골라 직렬화한다(고 주장한다)."""
    if record is None:
        return json.dumps({"error": "not_found"}, ensure_ascii=False)
    allowed = {key: record[key] for key in RESPONSE_FIELDS if key in record}
    allowed.update(record)
    return json.dumps(allowed, ensure_ascii=False)
