"""위반: 허용 필드 목록을 두 번째 자리에서 다시 정의한다."""

RESPONSE_FIELDS = ("claim_id", "status", "updated_at", "subscriber_name")


def render_row(record):
    return [record.get(key) for key in RESPONSE_FIELDS]
