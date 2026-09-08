"""위반(V4): 데코레이터를 쓰지 않고 라우트 표에 직접 넣는다.

데코레이터를 세는 축은 등록 자체를 못 본다. 표에 값을 넣는 문법은
파이썬이 정하는 어휘이고 우리가 열거할 수 있는 것이 아니다.

실행하면 /admin/claims/<id> 가 상류 레코드를 통째로 돌려준다.
"""

from records import fetch_claim
from routes import _ROUTES


def dump_claim(claim_id, session):
    return fetch_claim(claim_id)


_ROUTES["/admin/claims/<claim_id>"] = dump_claim
