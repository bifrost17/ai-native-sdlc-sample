"""red 픽스처가 **실제로** 민감 필드를 흘리는지 실행으로 확인한다 — 계기 유효성.

check_endpoints.sh 가 red 픽스처를 rc=1 로 잡는 것만으로는 부족하다. 그 픽스처가
애초에 유출을 일으키지 않는 코드였다면 검사기는 「아무것도 아닌 것」을 잡고 있는
것이고, 픽스처를 조용히 무해하게 고치는 것만으로 축 하나가 죽는다.

그래서 여기서 픽스처를 **실행해** 주민번호가 실제로 응답·감사로그에 실리는지 재고,
green 픽스처에서는 실리지 않는지(음성 대조)를 함께 잰다. 둘 다여야 계기가 산다.

실행: python3 tests/fixtures-endpoints/leak_probe.py   (레포 루트에서)
rc: 0 = 5종 전부 유출 + green 무유출 · 1 = 그 밖(계기 고장)
"""
import importlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "red")
SECRET = "900101-1234567"   # subscriber_rrn


def fresh(path):
    for m in list(sys.modules):
        if m in ("records", "response", "routes", "admin", "widen", "report"):
            del sys.modules[m]
    sys.path.insert(0, path)
    return path


def probe(name, fn):
    d = os.path.join(FIX, name)
    fresh(d)
    try:
        leaked, where = fn()
    finally:
        sys.path.remove(d)
    print("%-22s 유출=%-5s  %s" % (name, leaked, where))
    return leaked


def v1():
    records = importlib.import_module("records")
    response = importlib.import_module("response")
    out = response.build_response(records.fetch_claim("C-1001"))
    return SECRET in out, "build_response() 반환 = %s" % out


def v2():
    routes = importlib.import_module("routes")
    out = routes.admin_get_claim("C-1001", object())
    return SECRET in json.dumps(out, ensure_ascii=False), "admin_get_claim() 반환 키 = %s" % sorted(out)


def v3():
    records = importlib.import_module("records")
    response = importlib.import_module("response")
    importlib.import_module("widen")          # 임포트만으로 허용 목록이 넓어진다
    out = response.build_response(records.fetch_claim("C-1001"))
    return SECRET in out, "build_response() 반환 = %s" % out


def v4():
    routes = importlib.import_module("routes")
    importlib.import_module("admin")          # 표에 등록된다
    handler = routes._ROUTES["/admin/claims/<claim_id>"]
    out = handler("C-1001", object())
    return SECRET in json.dumps(out, ensure_ascii=False), "표 등록 핸들러 반환 키 = %s" % sorted(out)


def v5():
    routes = importlib.import_module("routes")
    routes.get_claim_status("C-1001", object())
    return SECRET in routes._AUDIT[0], "_AUDIT[0] = %s" % routes._AUDIT[0]


cases = [("gateway-widen", v1), ("foreign-decorator", v2), ("allowlist-augassign", v3),
         ("route-table", v4), ("dynamic-serialize", v5)]
bad = 0
for n, f in cases:
    if not probe(n, f):
        bad += 1

# 음성 대조: green 픽스처는 새지 않는다 (계기가 무조건 True 를 내는 게 아님을 보인다)
d = os.path.join(HERE, "green")
fresh(d)
records = importlib.import_module("records")
response = importlib.import_module("response")
out = response.build_response(records.fetch_claim("C-1001"))
sys.path.remove(d)
print("%-22s 유출=%-5s  %s" % ("green(음성 대조)", SECRET in out, "build_response() 반환 = %s" % out))
if SECRET in out:
    bad += 1

print("")
print("민감 필드 %s — 5종 전부 유출 + green 무유출 이면 0" % SECRET)
sys.exit(1 if bad else 0)
