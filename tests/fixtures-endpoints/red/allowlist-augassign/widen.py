"""위반(V3): 허용 목록을 대입이 아니라 **증분**으로 넓힌다.

R4 는 Assign/AnnAssign 만 「정의 자리」로 세므로 AugAssign 은 자리 수를 늘리지
않는다 — 정의는 여전히 한 곳이고, 그 한 곳의 값이 임포트 시점에 조용히 커진다.

실행하면 build_response 가 subscriber_rrn·subscriber_name 까지 내보낸다.
"""

import response

response.RESPONSE_FIELDS += ("subscriber_rrn", "subscriber_name")
