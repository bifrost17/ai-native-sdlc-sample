"""응답 단일 통로 — intent/0002-claims-status/spec.md R3.

응답 JSON 은 여기서만 만든다. RESPONSE_FIELDS 에 이름을 더하는 커밋이 곧 「그 필드를 내보내기로 했다」의 기록이다.
오류 문구는 고정 문자열뿐 — 입력도 원장 값도 되비추지 않는다(secure-api-review ④).
"""
import json

RESPONSE_FIELDS = ("claim_id", "status", "next_step", "due_date")
# 사정인 청중의 허용 목록 — intent/0008 spec R5. next_step 은 내부 처리 단계라 여기 없다.
ADJUSTER_FIELDS = ("claim_id", "status", "due_date")
# status 가 취할 수 있는 값 — intent/0008 spec R10. claims-core 가 닫아 둔 집합이고 법무·보안이
# 다섯 값 전부의 반출을 허가했다. 런타임에 막지 않는다; 여섯 번째 값이 원장에 생기면
# tests/test_adjuster_status.py 의 AC10 이 빨개져 「넓히는 것」이 결정으로 남는다.
STATUS_VALUES = ("접수", "심사중", "보완요청", "지급완료", "종결")


def error(code):
    return json.dumps({"error": code})


def build_response(record, fields):
    """원장 레코드에서 허용 필드만 골라 직렬화한다.

    `fields` 는 기본값이 없다 — intent/0008 spec Design. 청중이 둘이 된 뒤로 목록을 고르지 않은
    호출은 성립하면 안 된다: 기본값이 있으면 인자를 잊은 새 호출자가 고객용 목록(=next_step 포함)을
    조용히 내보낸다. 빠뜨리면 터지는 쪽으로 둔다.
    """
    allowed = {key: record[key] for key in fields if key in record}
    return json.dumps(allowed, ensure_ascii=False)
