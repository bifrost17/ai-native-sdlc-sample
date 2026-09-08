#!/usr/bin/env bash
# tests/test_check_endpoints.sh — scripts/check_endpoints.sh 의 계약 시험.
#
# 재는 것: rc 3분법(0 통과 / 1 위반 / 2 판정 불가)과 위반마다의 안정 code.
# 픽스처는 tests/fixtures-endpoints/ 에 상주하며, 레퍼런스 레포에서 실제로
# 뚫린 벡터(별칭 변수로 상류 레코드 반환)를 red 케이스로 못박는다.
#
# 계기 유효성: green 케이스에서 "scanned:" 줄이 0 이 아닌 수를 보고하는지까지
# 단정한다 — 아무 파일도 안 읽고 rc=0 을 내는 검사기는 그린이 아니라 고장이다.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

SCRIPT="scripts/check_endpoints.sh"
FIX="tests/fixtures-endpoints"

PASS=0
FAIL=0
TMPDIRS=""

cleanup() {
  local d
  for d in $TMPDIRS; do
    [ -n "$d" ] && [ -d "$d" ] && rm -rf "$d"
  done
}
trap cleanup EXIT INT TERM

# ok <라벨> — 통과 한 줄
ok() {
  echo "PASS  $1"
  PASS=$((PASS + 1))
}

# ng <라벨> <사유> [출력]
ng() {
  echo "FAIL  $1"
  echo "      사유: $2"
  if [ -n "${3:-}" ]; then
    echo "$3" | sed 's/^/      | /'
  fi
  FAIL=$((FAIL + 1))
}

# expect <라벨> <기대 rc> <기대 code 또는 -> <대상 경로>
expect() {
  local label="$1" want_rc="$2" want_code="$3" target="$4"
  local out rc
  out="$(bash "$SCRIPT" "$target" 2>&1)"
  rc=$?
  if [ "$rc" -ne "$want_rc" ]; then
    ng "$label" "rc=$rc — $want_rc 를 기대함" "$out"
    return
  fi
  if [ "$want_code" != "-" ]; then
    if ! printf '%s\n' "$out" | grep -q "$want_code"; then
      ng "$label" "출력에 code '$want_code' 가 없음" "$out"
      return
    fi
  fi
  ok "$label"
}

# --- 0. 검사기가 실재하고 실행 가능한가 (계기 존재 확인) ---
if [ ! -f "$SCRIPT" ]; then
  echo "FAIL  검사기 부재: $SCRIPT"
  echo ""
  echo "0 passed, 1 failed"
  exit 1
fi

# --- 1. green: 규약을 지키는 트리는 통과 ---
expect "green — 단일 통로·허용 목록 1곳·라우트 1파일 → rc=0" 0 "-" "$FIX/green"

# --- 1b. 계기 유효성: green 이 실제로 파일을 읽었는가 ---
green_out="$(bash "$SCRIPT" "$FIX/green" 2>&1)"
if printf '%s\n' "$green_out" | grep -Eq 'scanned: [1-9][0-9]* python'; then
  ok "green — scanned 가 0 이 아님(양성 대조)"
else
  ng "green — scanned 가 0 이 아님(양성 대조)" "scanned 줄이 없거나 0" "$green_out"
fi

# --- 2. red 4종 ---
expect "red/direct-serialize — 통로 밖 직렬화 → rc=1" 1 "E-SERIALIZE-OUTSIDE" "$FIX/red/direct-serialize"
expect "red/second-allowlist — 허용 목록 재정의 → rc=1" 1 "E-ALLOWLIST-DUP" "$FIX/red/second-allowlist"
expect "red/route-elsewhere — 다른 파일에서 라우트 등록 → rc=1" 1 "E-ROUTE-OUTSIDE" "$FIX/red/route-elsewhere"
expect "red/aliased-record — 별칭 변수로 통로 우회 → rc=1" 1 "E-GATEWAY-BYPASS" "$FIX/red/aliased-record"

# --- 2b. red 5종 — 독립 리뷰어가 백스톱을 직접 깨서 통과시킨 우회 벡터 (V1~V5) ---
# 이 다섯은 경화 전 전부 rc=0 이었고, 실행하면 주민번호가 실제로 응답·감사로그에
# 실려 나갔다(tests/fixtures-endpoints/leak_probe.py 가 그 사실을 상주시킨다).
# 각 줄의 code 는 그 벡터를 닫은 규칙을 지목한다 — 「빨갛기만 하면 통과」로 두면
# 엉뚱한 이유로 빨간 픽스처가 그 축을 못 재는 채 통과한다.
expect "red/gateway-widen (V1) — 통로 안에서 필터 무력화 → rc=1" 1 "E-GATEWAY-SHAPE" "$FIX/red/gateway-widen"
expect "red/foreign-decorator (V2) — 다른 데코레이터로 등록 → rc=1" 1 "E-GATEWAY-BYPASS" "$FIX/red/foreign-decorator"
expect "red/allowlist-augassign (V3) — 허용 목록 증분 확대 → rc=1" 1 "E-ALLOWLIST-MUTATE" "$FIX/red/allowlist-augassign"
expect "red/route-table (V4) — 데코레이터 없이 표에 등록 → rc=1" 1 "E-ROUTE-TABLE" "$FIX/red/route-table"
expect "red/dynamic-serialize (V5) — 동적 임포트 직렬화 → rc=1" 1 "E-RECORD-ESCAPE" "$FIX/red/dynamic-serialize"
expect "red/dynamic-serialize (V5) — 동적 임포트 자체도 빨강" 1 "E-DYNAMIC-IMPORT" "$FIX/red/dynamic-serialize"

# --- 2c. 계기 유효성: red 픽스처가 실제로 유출을 일으키는가 (양성 대조) ---
# 검사기가 red 를 잡는 것과 그 red 가 진짜 위험인 것은 다른 명제다. 픽스처를 조용히
# 무해하게 고치면 검사기는 그대로 빨간데 재는 것이 없어진다 — 그것을 이 시험이 막는다.
probe_out="$(python3 "$FIX/leak_probe.py" 2>&1)"
probe_rc=$?
if [ "$probe_rc" -eq 0 ]; then
  ok "red 픽스처 5종이 실행 시 실제로 민감 필드를 흘린다 + green 은 흘리지 않는다"
else
  ng "red 픽스처 5종이 실행 시 실제로 민감 필드를 흘린다 + green 은 흘리지 않는다" "leak_probe rc=$probe_rc" "$probe_out"
fi

# --- 3. 판정 불가 rc=2 ---
expect "missing/ — 없는 디렉터리 → rc=2" 2 "E-TARGET-MISSING" "$FIX/missing"

empty_dir="$(mktemp -d)"
TMPDIRS="$TMPDIRS $empty_dir"
expect "빈 디렉터리 — 파이썬 파일 0개 → rc=2" 2 "E-NO-PYTHON-FILES" "$empty_dir"

broken_dir="$(mktemp -d)"
TMPDIRS="$TMPDIRS $broken_dir"
printf 'def build_response(\n' > "$broken_dir/response.py"
expect "구문 오류 파일 — 판정 불가 → rc=2" 2 "E-PARSE" "$broken_dir"

# --- 4. 인자 없으면 기본 대상은 src/ ---
default_dir="$(mktemp -d)"
TMPDIRS="$TMPDIRS $default_dir"
mkdir -p "$default_dir/src"
cp "$FIX"/green/*.py "$default_dir/src/"
default_out="$(cd "$default_dir" && bash "$ROOT/$SCRIPT" 2>&1)"
default_rc=$?
if [ "$default_rc" -eq 0 ] && printf '%s\n' "$default_out" | grep -q 'src'; then
  ok "인자 없음 — 기본 대상이 src/ 이고 rc=0"
else
  ng "인자 없음 — 기본 대상이 src/ 이고 rc=0" "rc=$default_rc" "$default_out"
fi

echo ""
echo "${PASS} passed, ${FAIL} failed"
[ "$FAIL" -gt 0 ] && exit 1
exit 0
