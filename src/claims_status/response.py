"""응답 단일 통로 — 뼈대. 허용 목록이 아직 한 개뿐이다.

규약: 응답 직렬화는 build_response 안에서만 하고, 허용 필드 목록 RESPONSE_FIELDS 는
레포 전체에서 이 한 곳에만 둔다.
"""

import json

RESPONSE_FIELDS = ("claim_id",)


def build_response(record, denied=False):
    """상류 레코드에서 허용 필드만 골라 직렬화한다."""
    if denied:
        return json.dumps({"error": "unauthenticated"}, ensure_ascii=False)
    if record is None:
        return json.dumps({"error": "not_found"}, ensure_ascii=False)
    allowed = {key: record[key] for key in RESPONSE_FIELDS if key in record}
    return json.dumps(allowed, ensure_ascii=False)
