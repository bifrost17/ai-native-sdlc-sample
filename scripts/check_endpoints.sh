#!/usr/bin/env bash
# scripts/check_endpoints.sh — `secure-api-review` 스킬의 결정론 백스톱.
#
# 왜 있는가: 스킬은 조언적 통제다. 모델이 스킬을 안 읽거나 읽고도 다르게 쓰면
# 규칙은 지켜지지 않는다. 「언제나 지켜져야 하는 정책」은 스킬 뒤에 기계를 둔다.
#
# 이 축이 열거하는 집합은 {단일 응답 통로 build_response · 단일 허용 목록
# RESPONSE_FIELDS · 단일 라우트 등록 파일 routes.py · 핸들러의 반환 형태}이고,
# 그것을 닫는 것은 소유권(우리 코드 규약)이다 — 네 이름 전부 이 레포가 정하고
# 이 레포만 늘린다. 프레임워크·언어가 늘리는 어휘(직렬화 함수 이름 전수,
# 라우트 등록 문법 전수)를 열거하지 않는다. 그 축은 다음 판에 죽는다.
#
# 판정은 리터럴 grep 이 아니라 파이썬 AST 구조로 한다. 별칭 변수·다른 철자·
# 다른 파일에 등록한 라우트는 문자열로는 안 잡히고 구조로는 잡힌다
# (tests/fixtures-endpoints/red/aliased-record 가 그 반례를 상주시킨다).
#
# 재지 못하는 것(이 검사가 그린이어도 살아 있는 위험):
#   - base64·구분자 연결 등 직렬화 함수를 거치지 않는 인코딩 유출
#   - 런타임 동적 등록(setattr · 문자열 exec · 플러그인 로더가 붙이는 라우트)
#   - 허용 목록의 내용이 옳은가(필드 하나하나가 PII 인가) — 사람과 리뷰의 몫
#   - 인증이 실제로 신원을 검증하는가 — 이 검사는 통로의 모양만 본다
#   - 대상 디렉터리 밖(다른 서비스·상류)에서 일어나는 유출
#
# 규약(위반이면 rc=1):
#   R1 build_response 는 레포 전체에 정확히 하나 (E-NO-GATEWAY / E-GATEWAY-DUP)
#   R2 build_response 본문이 RESPONSE_FIELDS 를 참조한다 (E-GATEWAY-NOFILTER)
#   R3 응답 직렬화(json)는 build_response 안에서만 (E-SERIALIZE-OUTSIDE
#      · 통로 파일 밖의 json 임포트는 E-SERIALIZE-IMPORT)
#   R4 RESPONSE_FIELDS 대입은 정확히 한 곳 (E-ALLOWLIST-DUP / E-NO-ALLOWLIST)
#   R5 라우트 등록은 routes.py 에서만 (E-ROUTE-OUTSIDE / E-NO-ROUTES)
#   R6 라우트 핸들러의 return 은 build_response(...) 또는 빈 return 뿐
#      (E-GATEWAY-BYPASS) — 상류 레코드를 별칭에 담아도 잡힌다
#
# rc 계약: 0 위반 없음 / 1 위반 / 2 판정 불가(대상 없음 · 파이썬 파일 0개 ·
# 구문 오류 · python3 부재). rc=2 는 통과가 아니다 — fail-closed.
#
# 사용: bash scripts/check_endpoints.sh [디렉터리]   (기본 src)
set -uo pipefail

TARGET="${1:-src}"

case "$TARGET" in
  -h|--help)
    sed -n '2,45p' "${BASH_SOURCE[0]}"
    exit 0
    ;;
esac

if ! command -v python3 >/dev/null 2>&1; then
  echo "UNDECIDABLE E-NO-PYTHON3 python3 이 없어 판정할 수 없다 (fail-closed)"
  exit 2
fi

python3 - "$TARGET" <<'PY'
import ast
import os
import sys

TARGET = sys.argv[1]

GATEWAY_NAME = "build_response"
ALLOWLIST_NAME = "RESPONSE_FIELDS"
ROUTES_BASENAME = "routes.py"
ROUTE_NAMES = ("route", "register_route")
SERIALIZER_ATTRS = ("dumps", "dump")

violations = []          # (code, location, message)
undecidable = []         # (code, location, message)


def add(bucket, code, loc, msg):
    bucket.append((code, loc, msg))


# ---------------------------------------------------------------- 수집 단계

def collect_python_files(root):
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d != "__pycache__")
        for name in sorted(filenames):
            if name.endswith(".py"):
                found.append(os.path.join(dirpath, name))
    return found


def decorator_name(node):
    """데코레이터 노드에서 이름을 뽑는다. @route · @route(...) · @app.route(...)"""
    if isinstance(node, ast.Call):
        node = node.func
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def is_route_decorated(func_node):
    for dec in func_node.decorator_list:
        if decorator_name(dec) in ROUTE_NAMES:
            return True
    return False


def subtree_ids(node):
    return {id(n) for n in ast.walk(node)}


class FileFacts(object):
    def __init__(self, path, rel, tree):
        self.path = path
        self.rel = rel
        self.tree = tree
        self.gateways = []        # ast.FunctionDef
        self.allowlists = []      # lineno
        self.handlers = []        # ast.FunctionDef
        self.route_uses = []      # lineno
        self.json_names = set()   # json 모듈에 묶인 이름
        self.json_from = set()    # from json import dumps → {"dumps"}
        self.json_imports = []    # lineno
        self.serialize_calls = [] # lineno


def gather(path, rel, tree):
    facts = FileFacts(path, rel, tree)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name == GATEWAY_NAME:
                facts.gateways.append(node)
            if is_route_decorated(node):
                facts.handlers.append(node)
                for dec in node.decorator_list:
                    if decorator_name(dec) in ROUTE_NAMES:
                        facts.route_uses.append(dec.lineno)
        elif isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == ALLOWLIST_NAME:
                    facts.allowlists.append(node.lineno)
        elif isinstance(node, ast.AnnAssign):
            tgt = node.target
            if isinstance(tgt, ast.Name) and tgt.id == ALLOWLIST_NAME:
                facts.allowlists.append(node.lineno)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "json" or alias.name.startswith("json."):
                    facts.json_names.add(alias.asname or alias.name.split(".")[0])
                    facts.json_imports.append(node.lineno)
        elif isinstance(node, ast.ImportFrom):
            if node.module == "json":
                facts.json_imports.append(node.lineno)
                for alias in node.names:
                    facts.json_from.add(alias.asname or alias.name)
        elif isinstance(node, ast.Call):
            fn = node.func
            if isinstance(fn, ast.Attribute) and fn.attr in SERIALIZER_ATTRS:
                base = fn.value
                if isinstance(base, ast.Name):
                    facts.serialize_calls.append((node.lineno, base.id, fn.attr))
            elif isinstance(fn, ast.Name):
                facts.serialize_calls.append((node.lineno, None, fn.id))
        # 등록 함수 직접 호출: register_route(...)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == "register_route":
                facts.route_uses.append(node.lineno)
    return facts


# ---------------------------------------------------------------- 규칙 단계
# 규칙은 규칙마다 함수 하나다. 뮤테이션(침묵 살해)은 본문을 주석 처리해
# 그 규칙만 죽이고 나머지는 살려 둔다.

def check_gateway_unique(files):
    """R1 — build_response 는 정확히 하나."""
    found = [(f, g) for f in files for g in f.gateways]
    if not found:
        add(violations, "E-NO-GATEWAY", TARGET,
            "응답 단일 통로 %s() 가 없다 — 규약상 정확히 하나여야 한다" % GATEWAY_NAME)
    elif len(found) > 1:
        for f, g in found:
            add(violations, "E-GATEWAY-DUP", "%s:%d" % (f.rel, g.lineno),
                "%s() 가 %d 곳에 있다 — 통로가 둘이면 통로가 아니다" % (GATEWAY_NAME, len(found)))
    return found


def check_gateway_filters(found):
    """R2 — 통로가 허용 목록을 실제로 참조하는가."""
    for f, g in found:
        names = {n.id for n in ast.walk(g) if isinstance(n, ast.Name)}
        names |= {n.attr for n in ast.walk(g) if isinstance(n, ast.Attribute)}
        if ALLOWLIST_NAME not in names:
            add(violations, "E-GATEWAY-NOFILTER", "%s:%d" % (f.rel, g.lineno),
                "%s() 가 %s 를 참조하지 않는다 — 거르지 않는 통로는 통로가 아니다"
                % (GATEWAY_NAME, ALLOWLIST_NAME))


def check_serialization_confined(files, found):
    """R3 — 응답 직렬화는 통로 안에서만."""
    gateway_files = {f.rel for f, _ in found}
    inside = {}
    for f, g in found:
        inside.setdefault(f.rel, set()).update(
            getattr(n, "lineno", None) for n in ast.walk(g)
        )
    for f in files:
        if f.rel not in gateway_files and f.json_imports:
            add(violations, "E-SERIALIZE-IMPORT", "%s:%d" % (f.rel, f.json_imports[0]),
                "통로 파일 밖에서 json 을 임포트한다 — 직렬화는 %s() 의 일이다" % GATEWAY_NAME)
        span = inside.get(f.rel, set())
        for lineno, base, attr in f.serialize_calls:
            if base is not None and base not in f.json_names:
                continue
            if base is None and attr not in f.json_from:
                continue
            if lineno not in span:
                add(violations, "E-SERIALIZE-OUTSIDE", "%s:%d" % (f.rel, lineno),
                    "%s() 통로 밖에서 응답을 직렬화한다" % GATEWAY_NAME)


def check_allowlist_single(files):
    """R4 — 허용 필드 목록은 한 곳에만."""
    spots = [(f, ln) for f in files for ln in f.allowlists]
    if not spots:
        add(violations, "E-NO-ALLOWLIST", TARGET,
            "허용 필드 목록 %s 가 없다" % ALLOWLIST_NAME)
    elif len(spots) > 1:
        for f, ln in spots:
            add(violations, "E-ALLOWLIST-DUP", "%s:%d" % (f.rel, ln),
                "%s 가 %d 곳에서 정의된다 — 재정의는 조용히 넓어진다"
                % (ALLOWLIST_NAME, len(spots)))


def check_routes_single_file(files):
    """R5 — 라우트 등록은 routes.py 에서만."""
    spots = [(f, ln) for f in files for ln in f.route_uses]
    if not spots:
        add(violations, "E-NO-ROUTES", TARGET,
            "라우트 등록이 하나도 없다 — 이 검사기는 API 소스 트리를 전제한다")
        return
    for f, ln in spots:
        if os.path.basename(f.rel) != ROUTES_BASENAME:
            add(violations, "E-ROUTE-OUTSIDE", "%s:%d" % (f.rel, ln),
                "%s 밖에서 라우트를 등록한다 — 등록처가 흩어지면 아무도 전수를 못 센다"
                % ROUTES_BASENAME)


def handler_returns(func_node):
    """핸들러 자기 스코프의 return 만 모은다(중첩 함수는 다른 스코프)."""
    out = []

    def walk(node, top):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
                if not top:
                    continue
                if child is not func_node:
                    continue
            if isinstance(child, ast.Return):
                out.append(child)
            walk(child, False)

    for stmt in func_node.body:
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            continue
        if isinstance(stmt, ast.Return):
            out.append(stmt)
        walk(stmt, False)
    return out


def returns_through_gateway(ret):
    value = ret.value
    if value is None:
        return True
    if isinstance(value, ast.Constant) and value.value is None:
        return True
    if isinstance(value, ast.Await):
        value = value.value
    if isinstance(value, ast.Call):
        fn = value.func
        if isinstance(fn, ast.Name) and fn.id == GATEWAY_NAME:
            return True
        if isinstance(fn, ast.Attribute) and fn.attr == GATEWAY_NAME:
            return True
    return False


def check_handler_returns_gateway(files):
    """R6 — 핸들러는 통로를 거쳐서만 반환한다. 별칭 변수도 여기서 잡힌다."""
    for f in files:
        for handler in f.handlers:
            for ret in handler_returns(handler):
                if not returns_through_gateway(ret):
                    add(violations, "E-GATEWAY-BYPASS", "%s:%d" % (f.rel, ret.lineno),
                        "핸들러 %s() 가 %s() 를 거치지 않고 반환한다 — 이름이 무엇이든 "
                        "상류 레코드가 그대로 나갈 수 있다" % (handler.name, GATEWAY_NAME))


# ---------------------------------------------------------------- 실행

def main():
    if not os.path.isdir(TARGET):
        print("UNDECIDABLE E-TARGET-MISSING %s 검사 대상 디렉터리가 없다" % TARGET)
        return 2

    paths = collect_python_files(TARGET)
    if not paths:
        print("UNDECIDABLE E-NO-PYTHON-FILES %s 에 파이썬 파일이 하나도 없다" % TARGET)
        return 2

    files = []
    for path in paths:
        rel = os.path.relpath(path, TARGET)
        try:
            with open(path, "r", encoding="utf-8") as fh:
                source = fh.read()
            tree = ast.parse(source, filename=path)
        except SyntaxError as exc:
            add(undecidable, "E-PARSE", "%s:%s" % (rel, exc.lineno or 0),
                "구문 오류로 파싱할 수 없다: %s" % exc.msg)
            continue
        except (OSError, UnicodeDecodeError) as exc:
            add(undecidable, "E-PARSE", rel, "읽을 수 없다: %s" % exc)
            continue
        files.append(gather(path, rel, tree))

    print("check_endpoints: target=%s" % TARGET)
    print("scanned: %d python files" % len(files))

    if undecidable:
        for code, loc, msg in undecidable:
            print("UNDECIDABLE %s %s %s" % (code, loc, msg))
        print("")
        print("판정 불가 %d 건 — rc=2 는 통과가 아니다" % len(undecidable))
        return 2

    found = check_gateway_unique(files)
    check_gateway_filters(found)
    check_serialization_confined(files, found)
    check_allowlist_single(files)
    check_routes_single_file(files)
    check_handler_returns_gateway(files)

    if violations:
        for code, loc, msg in violations:
            print("VIOLATION %s %s %s" % (code, loc, msg))
        print("")
        print("위반 %d 건" % len(violations))
        return 1

    print("위반 0 건 — 단일 통로 · 단일 허용 목록 · 단일 등록처")
    return 0


sys.exit(main())
PY
