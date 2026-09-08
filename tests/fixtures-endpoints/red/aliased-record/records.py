"""상류 청구 레코드 접근 — PII 를 포함한 원본 레코드를 그대로 돌려준다.

허용 목록 적용은 이 파일의 일이 아니다. 응답으로 나가는 필드를 고르는 것은
response.py 의 build_response 하나뿐이다(단일 통로 규약).
"""

_UPSTREAM = {
    "C-1001": {
        "claim_id": "C-1001",
        "status": "심사중",
        "updated_at": "2026-09-08T09:00:00+09:00",
        "amount_krw": 128000,
        "subscriber_rrn": "900101-1234567",
        "subscriber_name": "홍길동",
        "internal_memo": "재심사 대상",
    },
}


def fetch_claim(claim_id):
    """상류에서 청구 레코드를 읽는다."""
    return _UPSTREAM.get(claim_id)
