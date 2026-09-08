"""위반: 라우트를 routes.py 밖에서 등록한다."""

from records import fetch_claim
from response import build_response
from routes import route


@route("/admin/claims/<claim_id>")
def admin_get_claim(claim_id, session):
    return build_response(fetch_claim(claim_id))
