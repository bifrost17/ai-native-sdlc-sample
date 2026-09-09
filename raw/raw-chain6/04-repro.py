import sys; sys.path.insert(0, "src")
from claims_status import records, routes
h = routes.ROUTES["/claims/<claim_id>/status"]; S = {"subscriber_id": "S-77"}
print("t=0   C-1003 은 아직 원장에 없다 ->", h("C-1003", S, now=0.0), "upstream_calls=", records.upstream_calls())
records._UPSTREAM["C-1003"] = {"claim_id": "C-1003", "subscriber_id": "S-77", "status": "접수",
                               "next_step": "서류 검토", "due_date": "2026-09-20"}
print("      원장에 C-1003 이 생겼다")
print("t=30  같은 고객이 다시 조회 ->", h("C-1003", S, now=30.0), "upstream_calls=", records.upstream_calls())
print("t=59  ->", h("C-1003", S, now=59.0), "upstream_calls=", records.upstream_calls())
print("t=61  TTL 이 지나야 ->", h("C-1003", S, now=61.0), "upstream_calls=", records.upstream_calls())
print("자리: src/claims_status/records.py fetch_claim — record 가 None 이어도 _CACHE[claim_id]=(now+60, None)")
