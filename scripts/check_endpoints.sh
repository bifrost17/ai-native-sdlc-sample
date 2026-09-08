#!/usr/bin/env bash
# scripts/check_endpoints.sh — `secure-api-review` 스킬의 결정론 백스톱.
#
# 왜 있는가: 스킬은 조언적 통제다. 모델이 스킬을 안 읽거나 읽고도 다르게 쓰면
# 규칙은 지켜지지 않는다. 「언제나 지켜져야 하는 정책」은 스킬 뒤에 기계를 둔다.
#
# ── 축의 어휘 소유권 ──────────────────────────────────────────────────────
# 이 축이 열거하는 집합은 {단일 응답 통로 build_response · 단일 허용 목록
# RESPONSE_FIELDS · 단일 라우트 등록 파일 routes.py · 라우트 표 이름 _ROUTES ·
# 상류 접근 모듈 records.py · 통로 본문의 정규 형태}이고, 그것을 닫는 것은
# **소유권**이다 — 이 이름과 형태를 전부 이 레포가 정하고 이 레포만 늘린다.
#
# 열거하지 않는 것(다른 곳이 어휘를 늘리는 집합):
#   - 라우트 등록 데코레이터의 이름 전수 → 대신 「routes.py 밖에서는 데코레이터를
#     쓰지 않는다」로 뒤집는다. 프레임워크가 @app.get 을 새로 내도 규칙은 안 죽는다.
#   - 직렬화 함수 이름 전수 → 대신 「상류 레코드는 build_response() 말고 어디에도
#     넘기지 않는다」(R8)로 뒤집는다. 어떤 이름으로 직렬화하든 인자가 못 간다.
#   - 딕셔너리를 넓히는 문법 전수(update · |= · **병합 · setdefault · 아이템 대입)
#     → 대신 「통로 본문은 아래 정규 형태 문장만 쓴다」(R7)로 뒤집는다. 목록에 없는
#     새 문법은 자동으로 빨강이다.
#
# 판정은 리터럴 grep 이 아니라 파이썬 AST 구조로 한다. 별칭 변수·다른 철자·
# 다른 파일에 등록한 라우트는 문자열로는 안 잡히고 구조로는 잡힌다
# (tests/fixtures-endpoints/red/ 아홉 종이 그 반례를 상주시킨다).
#
# ── 재지 못하는 것(이 검사가 그린이어도 살아 있는 위험) ────────────────────
#   - base64·구분자 연결 등 「호출 없이」 문자열로 조립하는 인코딩 유출
#     (R8 은 레코드를 **호출에 넘기는 것**을 잡는다. f-문자열·% 서식으로 필드를
#      하나씩 꺼내 이어 붙이면 못 잡는다)
#   - 런타임 동적 등록(setattr · 문자열 exec · 플러그인 로더가 붙이는 라우트)
#   - 허용 목록의 내용이 옳은가(필드 하나하나가 PII 인가) — 사람과 리뷰의 몫
#   - 인증이 실제로 신원을 검증하는가 — 이 검사는 통로의 모양만 본다
#   - 대상 디렉터리 밖(다른 서비스·상류)에서 일어나는 유출
#   - 🔴 R3-b(E-DYNAMIC-IMPORT)가 열거하는 {__import__ · importlib.import_module ·
#     eval · exec · compile · load_module · exec_module · module_from_spec}의
#     어휘 소유자는 **CPython stdlib** 이지 우리가 아니다 — 열린 어휘다.
#     그래서 이 규칙 하나에 기대지 않는다: V5 를 실제로 닫는 것은 R8 이고,
#     R3-b 는 「동적 임포트를 쓸 이유가 이 트리엔 없다」는 규약의 집행일 뿐이다.
#     stdlib 이 새 동적 임포트 API 를 내는 날 이 목록을 늘리는 것이 절차다.
#   - 🔴 R3-c(E-SERIALIZE-OPAQUE)가 보는 {dumps · dump} 도 라이브러리 소유
#     어휘다(yaml.dump · pickle.dumps 는 우연히 같은 이름이고, msgpack.packb 는
#     다른 이름이다). 같은 이유로 R8 이 본선이다.
#
# ── 규약(위반이면 rc=1) ────────────────────────────────────────────────────
#   R1 build_response 는 레포 전체에 정확히 하나 (E-NO-GATEWAY / E-GATEWAY-DUP)
#   R2 build_response 본문이 RESPONSE_FIELDS 를 참조한다 (E-GATEWAY-NOFILTER)
#   R3 응답 직렬화(json)는 build_response 안에서만 (E-SERIALIZE-OUTSIDE
#      · 통로 파일 밖의 json 임포트는 E-SERIALIZE-IMPORT
#      · 정체를 모르는 이름으로 하는 dumps/dump 는 E-SERIALIZE-OPAQUE
#      · 동적 임포트·eval·exec 자체가 E-DYNAMIC-IMPORT)
#   R4 RESPONSE_FIELDS 대입은 정확히 한 곳 (E-ALLOWLIST-DUP / E-NO-ALLOWLIST)
#      · 그 한 곳 밖에서 이름을 **쓰기**(AugAssign · 속성 대입 · for 대상 · del)
#        하거나 메서드를 부르면 E-ALLOWLIST-MUTATE — 「정의는 한 곳」과
#        「값이 안 넓어진다」는 다른 명제다
#   R5 라우트 등록은 routes.py 에서만 (E-ROUTE-OUTSIDE / E-NO-ROUTES)
#      · routes.py 밖의 어떤 데코레이터든 E-DECORATOR-OUTSIDE
#      · 라우트 표 _ROUTES 를 routes.py 밖에서 건드리면 E-ROUTE-TABLE
#   R6 라우트 핸들러(= routes.py 의 데코레이터 붙은 함수 전부)의 return 은
#      build_response(...) 또는 빈 return 뿐 (E-GATEWAY-BYPASS)
#   R7 통로 본문의 정규 형태 — 통로는 6줄짜리 우리 코드다. 자유를 주지 않는다.
#      · 문장은 {docstring · 단일 Name 대입 · return · if · raise · pass} 뿐
#        (E-GATEWAY-SHAPE) — 목록 밖 문장 하나가 곧 위반이다
#      · RESPONSE_FIELDS 를 iter 로 쓰는 **딕셔너리 컴프리헨션 대입**이 정확히
#        하나 있어야 한다 (E-GATEWAY-BUILD) — 그 대상 이름이 「허용 딕셔너리」다
#      · 모든 return 은 허용 딕셔너리 그 자체이거나, 허용 딕셔너리와 상수만을
#        인자로 받는 호출이어야 한다 (E-GATEWAY-RETURN)
#      · 통로 안에 ** 언팩 · | 병합이 있으면 위반 (E-GATEWAY-MERGE)
#      · return 이 레코드 파라미터를 참조하면 위반 (E-GATEWAY-LEAK)
#   R8 상류 레코드는 통로 말고 어디에도 넘어가지 않는다 (E-RECORD-ESCAPE)
#      records.py 가 준 값(과 그것을 받은 별칭)은 build_response(...) 의 인자,
#      또는 None 비교/참거짓 판정에만 쓸 수 있다. 반환·다른 호출의 인자·표에
#      담기는 순간 위반이다. 이것이 「직렬화 함수 이름」을 열거하지 않고도
#      직렬화 유출을 닫는 방법이다.
#
# rc 계약: 0 위반 없음 / 1 위반 / 2 판정 불가(대상 없음 · 파이썬 파일 0개 ·
# 구문 오류 · python3 부재). rc=2 는 통과가 아니다 — fail-closed.
#
# 사용: bash scripts/check_endpoints.sh [디렉터리]   (기본 src)
set -uo pipefail

TARGET="${1:-src}"

case "$TARGET" in
  -h|--help)
    sed -n '2,78p' "${BASH_SOURCE[0]}"
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
RECORDS_BASENAME = "records.py"
ROUTE_TABLE_NAME = "_ROUTES"
ROUTE_NAMES = ("route", "register_route")
SERIALIZER_ATTRS = ("dumps", "dump")

# R3-b 의 열린 어휘 — 소유자는 CPython stdlib 이다(헤더 「재지 못하는 것」 참조).
DYNAMIC_IMPORT_NAMES = ("__import__", "eval", "exec", "compile")
DYNAMIC_IMPORT_ATTRS = ("import_module", "__import__", "load_module",
                        "exec_module", "module_from_spec")

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


def build_parents(tree):
    parents = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parents[id(child)] = node
    return parents


def names_in(node):
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}


def refers_allowlist(node):
    if any(isinstance(n, ast.Name) and n.id == ALLOWLIST_NAME for n in ast.walk(node)):
        return True
    return any(isinstance(n, ast.Attribute) and n.attr == ALLOWLIST_NAME
               for n in ast.walk(node))


class FileFacts(object):
    def __init__(self, path, rel, tree):
        self.path = path
        self.rel = rel
        self.tree = tree
        self.parents = build_parents(tree)
        self.is_routes = os.path.basename(rel) == ROUTES_BASENAME
        self.is_records = os.path.basename(rel) == RECORDS_BASENAME
        self.gateways = []          # ast.FunctionDef
        self.allowlist_defs = []    # lineno — Assign/AnnAssign 의 단일 Name 대상
        self.allowlist_mutations = []  # (lineno, 무엇)
        self.handlers = []          # ast.FunctionDef — routes.py 의 데코레이터 붙은 함수
        self.route_uses = []        # lineno
        self.foreign_decorators = []  # (lineno, 이름) — routes.py 밖의 데코레이터
        self.route_outside = []     # lineno — routes.py 밖의 라우트 어휘 데코레이터
        self.route_table_touch = [] # (lineno, 무엇)
        self.json_names = set()     # json 모듈에 묶인 이름
        self.json_from = set()      # from json import dumps → {"dumps"}
        self.json_imports = []      # lineno
        self.serialize_calls = []   # (lineno, base, attr)
        self.dynamic_imports = []   # (lineno, 이름)
        self.records_funcs = set()  # from records import X → {"X"}
        self.records_mods = set()   # import records → {"records"}


def gather(path, rel, tree):
    facts = FileFacts(path, rel, tree)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name == GATEWAY_NAME:
                facts.gateways.append(node)
            if node.decorator_list:
                first = node.decorator_list[0]
                if facts.is_routes:
                    # R5 뒤집기: routes.py 안의 데코레이터는 전부 라우트 등록으로 본다.
                    # 「등록 어휘」를 열거하지 않으므로 @app.get 도 여기에 걸린다.
                    facts.handlers.append(node)
                    facts.route_uses.append(first.lineno)
                else:
                    for dec in node.decorator_list:
                        name = decorator_name(dec)
                        if name in ROUTE_NAMES:
                            facts.route_outside.append(dec.lineno)
                            facts.route_uses.append(dec.lineno)
                        else:
                            facts.foreign_decorators.append((dec.lineno, name or "?"))
                    # routes.py 밖의 데코레이터 함수도 핸들러 규칙(R6)의 대상이다.
                    facts.handlers.append(node)
        elif isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == ALLOWLIST_NAME:
                    facts.allowlist_defs.append(node.lineno)
        elif isinstance(node, ast.AnnAssign):
            tgt = node.target
            if isinstance(tgt, ast.Name) and tgt.id == ALLOWLIST_NAME:
                facts.allowlist_defs.append(node.lineno)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "json" or alias.name.startswith("json."):
                    facts.json_names.add(alias.asname or alias.name.split(".")[0])
                    facts.json_imports.append(node.lineno)
                if alias.name == "records" or alias.name.endswith(".records"):
                    facts.records_mods.add(alias.asname or alias.name.split(".")[-1])
        elif isinstance(node, ast.ImportFrom):
            if node.module == "json":
                facts.json_imports.append(node.lineno)
                for alias in node.names:
                    facts.json_from.add(alias.asname or alias.name)
            if node.module == "records" or (node.module or "").endswith(".records"):
                for alias in node.names:
                    facts.records_funcs.add(alias.asname or alias.name)
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

        # R3-b — 동적 임포트·eval·exec
        if isinstance(node, ast.Call):
            fn = node.func
            if isinstance(fn, ast.Name) and fn.id in DYNAMIC_IMPORT_NAMES:
                facts.dynamic_imports.append((node.lineno, fn.id))
            elif isinstance(fn, ast.Attribute) and fn.attr in DYNAMIC_IMPORT_ATTRS:
                facts.dynamic_imports.append((node.lineno, fn.attr))

        # R4 확장 — 허용 목록을 「쓰기」 하거나 메서드를 부르는 자리.
        # Store/Del 은 파이썬 문법이 정하는 닫힌 집합이다(ast 가 ctx 로 알려 준다).
        if isinstance(node, ast.Name) and node.id == ALLOWLIST_NAME:
            if isinstance(node.ctx, (ast.Store, ast.Del)):
                if node.lineno not in facts.allowlist_defs:
                    facts.allowlist_mutations.append((node.lineno, "이름을 다시 묶는다"))
        if isinstance(node, ast.Attribute) and node.attr == ALLOWLIST_NAME:
            if isinstance(node.ctx, (ast.Store, ast.Del)):
                facts.allowlist_mutations.append(
                    (node.lineno, "모듈 속성으로 다시 묶는다"))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            recv = node.func.value
            hit = (isinstance(recv, ast.Name) and recv.id == ALLOWLIST_NAME) or \
                  (isinstance(recv, ast.Attribute) and recv.attr == ALLOWLIST_NAME)
            if hit:
                facts.allowlist_mutations.append(
                    (node.lineno, ".%s() 를 부른다" % node.func.attr))

        # R5 확장 — 라우트 표를 routes.py 밖에서 건드리는 자리.
        if not facts.is_routes:
            if isinstance(node, ast.Name) and node.id == ROUTE_TABLE_NAME:
                facts.route_table_touch.append((node.lineno, "이름으로 쓴다"))
            elif isinstance(node, ast.Attribute) and node.attr == ROUTE_TABLE_NAME:
                facts.route_table_touch.append((node.lineno, "속성으로 쓴다"))
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    if alias.name == ROUTE_TABLE_NAME:
                        facts.route_table_touch.append((node.lineno, "임포트한다"))
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


# --- R7 통로 정규 형태 -------------------------------------------------------
# 「무엇을 금지하는가」가 아니라 「무엇만 허용하는가」로 적는다. 딕셔너리를 넓히는
# 문법은 파이썬이 늘리는 어휘라 열거하면 다음 판에 죽는다. 통로는 우리 6줄짜리
# 코드이므로 형태를 못박는 쪽이 닫힌다.

def gateway_statements(func_node):
    """통로 본문의 문장을 if 안까지 재귀로 편다."""
    out = []

    def walk(body):
        for stmt in body:
            out.append(stmt)
            if isinstance(stmt, ast.If):
                walk(stmt.body)
                walk(stmt.orelse)

    walk(func_node.body)
    return out


def is_docstring(stmt):
    return isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant)


def constant_only(node):
    """부분트리에 이름이 하나도 없다 — 상수만으로 만들어진 식."""
    return not any(isinstance(n, ast.Name) for n in ast.walk(node))


def check_gateway_shape(found):
    """R7 — 통로 본문의 문장 형태 · 허용 딕셔너리 · return 형태 · 병합 금지."""
    for f, g in found:
        loc = "%s:%d" % (f.rel, g.lineno)

        # (a) 문장 형태 — 목록 밖은 전부 위반.
        for stmt in gateway_statements(g):
            if isinstance(stmt, (ast.Return, ast.If, ast.Raise, ast.Pass)):
                continue
            if is_docstring(stmt):
                continue
            if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 \
                    and isinstance(stmt.targets[0], ast.Name):
                continue
            if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
                continue
            add(violations, "E-GATEWAY-SHAPE", "%s:%d" % (f.rel, stmt.lineno),
                "%s() 본문에 정규 형태 밖의 문장(%s)이 있다 — 통로는 "
                "{docstring · 단일 이름 대입 · return · if · raise · pass} 뿐이다. "
                "거른 뒤에 다시 넓히는 한 줄이 정확히 여기로 들어온다"
                % (GATEWAY_NAME, type(stmt).__name__))

        # (b) 허용 딕셔너리 — RESPONSE_FIELDS 를 iter 로 쓰는 컴프리헨션 대입 1개.
        builds = []
        for stmt in gateway_statements(g):
            if not isinstance(stmt, ast.Assign) or len(stmt.targets) != 1:
                continue
            if not isinstance(stmt.targets[0], ast.Name):
                continue
            if not isinstance(stmt.value, ast.DictComp):
                continue
            if any(refers_allowlist(gen.iter) for gen in stmt.value.generators):
                builds.append(stmt)
        if len(builds) != 1:
            add(violations, "E-GATEWAY-BUILD", loc,
                "%s() 안에 「%s 를 iter 로 쓰는 딕셔너리 컴프리헨션 대입」이 %d 개다 "
                "— 정확히 하나여야 한다. 응답 본문은 허용 목록으로 **만들어진** "
                "딕셔너리 그 자체여야 하고, 다른 방식으로 만든 것은 통로가 아니다"
                % (GATEWAY_NAME, ALLOWLIST_NAME, len(builds)))
            allowed_name = None
        else:
            allowed_name = builds[0].targets[0].id

        # (c) return 형태 — 허용 딕셔너리 그 자체이거나, 그것과 상수만 받는 호출.
        record_param = None
        args = g.args
        positional = list(getattr(args, "posonlyargs", [])) + list(args.args)
        if positional:
            record_param = positional[0].arg

        for stmt in gateway_statements(g):
            if not isinstance(stmt, ast.Return) or stmt.value is None:
                continue
            value = stmt.value
            rloc = "%s:%d" % (f.rel, stmt.lineno)

            # (e) 레코드 파라미터가 return 에 새어 나오면 위반.
            if record_param is not None and record_param in names_in(value):
                add(violations, "E-GATEWAY-LEAK", rloc,
                    "%s() 의 return 이 레코드 파라미터 '%s' 를 직접 참조한다 — "
                    "나가는 것은 허용 딕셔너리뿐이어야 한다" % (GATEWAY_NAME, record_param))

            if isinstance(value, ast.Name) and allowed_name and value.id == allowed_name:
                continue
            if constant_only(value):
                continue
            if isinstance(value, ast.Call):
                bad = False
                for arg in value.args:
                    if isinstance(arg, ast.Name) and allowed_name and arg.id == allowed_name:
                        continue
                    if constant_only(arg):
                        continue
                    bad = True
                for kw in value.keywords:
                    if kw.arg is None:
                        bad = True
                        continue
                    if isinstance(kw.value, ast.Name) and allowed_name \
                            and kw.value.id == allowed_name:
                        continue
                    if constant_only(kw.value):
                        continue
                    bad = True
                if not bad:
                    continue
            add(violations, "E-GATEWAY-RETURN", rloc,
                "%s() 의 return 이 허용 형태가 아니다 — 허용 딕셔너리 그 자체이거나, "
                "허용 딕셔너리와 상수만을 인자로 받는 호출이어야 한다" % GATEWAY_NAME)

        # (d) 병합 문법 — ** 언팩 · | 결합.
        for node in ast.walk(g):
            if isinstance(node, ast.Dict) and any(k is None for k in node.keys):
                add(violations, "E-GATEWAY-MERGE", "%s:%d" % (f.rel, node.lineno),
                    "%s() 안에서 ** 로 매핑을 합친다 — 무엇이 합쳐지는지 "
                    "이 검사기는 모른다" % GATEWAY_NAME)
            elif isinstance(node, ast.Call) and any(kw.arg is None for kw in node.keywords):
                add(violations, "E-GATEWAY-MERGE", "%s:%d" % (f.rel, node.lineno),
                    "%s() 안에서 ** 로 인자를 펼친다" % GATEWAY_NAME)
            elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
                add(violations, "E-GATEWAY-MERGE", "%s:%d" % (f.rel, node.lineno),
                    "%s() 안에서 | 로 매핑을 합친다" % GATEWAY_NAME)


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
                # 정체를 모르는 이름으로 하는 dumps/dump. 동적 임포트로 들여온
                # json 이 정확히 여기로 들어온다 — 이름을 모른다고 통과시키지 않는다.
                if lineno not in span:
                    add(violations, "E-SERIALIZE-OPAQUE", "%s:%d" % (f.rel, lineno),
                        "정체를 정적으로 알 수 없는 '%s' 로 .%s() 를 부른다 — "
                        "통로 밖 직렬화일 수 있고, 아니라고 증명할 방법이 없다"
                        % (base, attr))
                continue
            if base is None and attr not in f.json_from:
                continue
            if lineno not in span:
                add(violations, "E-SERIALIZE-OUTSIDE", "%s:%d" % (f.rel, lineno),
                    "%s() 통로 밖에서 응답을 직렬화한다" % GATEWAY_NAME)
        for lineno, name in f.dynamic_imports:
            add(violations, "E-DYNAMIC-IMPORT", "%s:%d" % (f.rel, lineno),
                "동적 임포트·실행(%s)을 쓴다 — 이 트리의 모듈 바인딩은 정적 "
                "import 문에서만 생긴다는 것이 규약이다(검사기가 이름을 따라갈 수 "
                "있어야 한다)" % name)


def check_allowlist_single(files):
    """R4 — 허용 필드 목록은 한 곳에서만 정의되고, 그 뒤로 넓어지지 않는다."""
    spots = [(f, ln) for f in files for ln in f.allowlist_defs]
    if not spots:
        add(violations, "E-NO-ALLOWLIST", TARGET,
            "허용 필드 목록 %s 가 없다" % ALLOWLIST_NAME)
    elif len(spots) > 1:
        for f, ln in spots:
            add(violations, "E-ALLOWLIST-DUP", "%s:%d" % (f.rel, ln),
                "%s 가 %d 곳에서 정의된다 — 재정의는 조용히 넓어진다"
                % (ALLOWLIST_NAME, len(spots)))
    for f in files:
        for ln, what in f.allowlist_mutations:
            add(violations, "E-ALLOWLIST-MUTATE", "%s:%d" % (f.rel, ln),
                "%s 를 정의 자리 밖에서 %s — 정의가 한 곳인 것과 값이 안 넓어지는 "
                "것은 다른 명제다" % (ALLOWLIST_NAME, what))


def check_routes_single_file(files):
    """R5 — 라우트 등록은 routes.py 에서만. 등록 어휘를 열거하지 않고 뒤집는다."""
    spots = [(f, ln) for f in files for ln in f.route_uses]
    if not spots:
        add(violations, "E-NO-ROUTES", TARGET,
            "라우트 등록이 하나도 없다 — 이 검사기는 API 소스 트리를 전제한다")
    for f in files:
        for ln in f.route_outside:
            add(violations, "E-ROUTE-OUTSIDE", "%s:%d" % (f.rel, ln),
                "%s 밖에서 라우트를 등록한다 — 등록처가 흩어지면 아무도 전수를 못 센다"
                % ROUTES_BASENAME)
        for ln, name in f.foreign_decorators:
            add(violations, "E-DECORATOR-OUTSIDE", "%s:%d" % (f.rel, ln),
                "%s 밖에서 데코레이터 @%s 를 쓴다 — 이 트리의 데코레이터는 라우트 "
                "등록뿐이라는 것이 규약이다. 등록 어휘를 열거하는 대신 등록 장소를 "
                "하나로 묶는다" % (ROUTES_BASENAME, name))
        for ln, what in f.route_table_touch:
            add(violations, "E-ROUTE-TABLE", "%s:%d" % (f.rel, ln),
                "%s 밖에서 라우트 표 %s 를 %s — 데코레이터를 안 쓰고 표에 직접 넣는 "
                "등록도 등록이다" % (ROUTES_BASENAME, ROUTE_TABLE_NAME, what))


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


# --- R8 상류 레코드 흐름 -----------------------------------------------------
# 「직렬화 함수 이름」을 열거하지 않고 직렬화 유출을 닫는 방법. records.py 가 준
# 값은 build_response(...) 의 인자 말고 어디에도 못 간다. 어떤 이름으로 무엇을
# 부르든, 인자가 못 가면 나갈 수 없다.

def is_record_source_call(node, facts):
    if not isinstance(node, ast.Call):
        return False
    fn = node.func
    if isinstance(fn, ast.Name) and fn.id in facts.records_funcs:
        return True
    if isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name) \
            and fn.value.id in facts.records_mods:
        return True
    return False


def is_gateway_call(node):
    if not isinstance(node, ast.Call):
        return False
    fn = node.func
    if isinstance(fn, ast.Name) and fn.id == GATEWAY_NAME:
        return True
    if isinstance(fn, ast.Attribute) and fn.attr == GATEWAY_NAME:
        return True
    return False


def tainted_names(facts):
    """단순 별칭 전파 — 고정점까지 돈다."""
    tainted = set()
    for _ in range(8):
        before = len(tainted)
        for node in ast.walk(facts.tree):
            if not isinstance(node, ast.Assign) or len(node.targets) != 1:
                continue
            tgt = node.targets[0]
            if not isinstance(tgt, ast.Name):
                continue
            val = node.value
            if is_record_source_call(val, facts):
                tainted.add(tgt.id)
            elif isinstance(val, ast.Name) and val.id in tainted:
                tainted.add(tgt.id)
        if len(tainted) == before:
            break
    return tainted


def record_use_is_allowed(node, facts):
    parent = facts.parents.get(id(node))
    if parent is None:
        return False
    # (a) 단일 이름에 담는다 — 별칭이므로 그 이름이 다시 오염된다.
    if isinstance(parent, ast.Assign) and parent.value is node \
            and len(parent.targets) == 1 and isinstance(parent.targets[0], ast.Name):
        return True
    # (b) 통로 호출의 인자다 — 유일하게 허락된 목적지.
    if isinstance(parent, ast.Call) and is_gateway_call(parent) and node in parent.args:
        return True
    # (c) 참거짓·None 비교로만 쓴다.
    if isinstance(parent, ast.Compare):
        return True
    if isinstance(parent, (ast.If, ast.While, ast.IfExp)) and parent.test is node:
        return True
    if isinstance(parent, ast.BoolOp):
        return True
    if isinstance(parent, ast.UnaryOp) and isinstance(parent.op, ast.Not):
        return True
    return False


def check_record_flow(files):
    """R8 — 상류 레코드는 통로 말고 어디에도 넘어가지 않는다."""
    for f in files:
        if f.is_records:
            continue
        if not f.records_funcs and not f.records_mods:
            continue
        tainted = tainted_names(f)
        for node in ast.walk(f.tree):
            if is_record_source_call(node, f):
                if not record_use_is_allowed(node, f):
                    add(violations, "E-RECORD-ESCAPE", "%s:%d" % (f.rel, node.lineno),
                        "상류 레코드가 %s() 를 거치지 않고 다른 곳으로 간다 — "
                        "%s 가 준 값은 통로의 인자이거나 None 판정에만 쓸 수 있다"
                        % (GATEWAY_NAME, RECORDS_BASENAME))
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) \
                    and node.id in tainted:
                if not record_use_is_allowed(node, f):
                    add(violations, "E-RECORD-ESCAPE", "%s:%d" % (f.rel, node.lineno),
                        "상류 레코드를 담은 이름 '%s' 가 %s() 밖으로 나간다 — "
                        "직렬화 함수의 이름이 무엇이든 인자가 못 가면 나갈 수 없다"
                        % (node.id, GATEWAY_NAME))


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
    check_gateway_shape(found)
    check_serialization_confined(files, found)
    check_allowlist_single(files)
    check_routes_single_file(files)
    check_handler_returns_gateway(files)
    check_record_flow(files)

    if violations:
        for code, loc, msg in violations:
            print("VIOLATION %s %s %s" % (code, loc, msg))
        print("")
        print("위반 %d 건" % len(violations))
        return 1

    print("위반 0 건 — 단일 통로 · 단일 허용 목록 · 단일 등록처 · 레코드 무유출")
    return 0


sys.exit(main())
PY
