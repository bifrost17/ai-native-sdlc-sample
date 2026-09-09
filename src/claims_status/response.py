"""응답 단일 통로 — intent/0002-claims-status/spec.md R3.

응답 JSON 은 여기서만 만든다. RESPONSE_FIELDS 에 이름을 더하는 커밋이 곧 「그 필드를 내보내기로 했다」의 기록이다.
오류 문구는 고정 문자열뿐 — 입력도 원장 값도 되비추지 않는다(secure-api-review ④).
"""
import json

RESPONSE_FIELDS = ("claim_id", "status", "next_step", "due_date")


def error(code):
    return json.dumps({"error": code})


def build_response(record):
    """원장 레코드에서 허용 필드만 골라 직렬화한다."""
    allowed = {key: record[key] for key in RESPONSE_FIELDS if key in record}
    return json.dumps(allowed, ensure_ascii=False)
