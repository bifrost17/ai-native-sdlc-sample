#!/usr/bin/env bash
# scripts/gates/50-metrics.sh — 지표 계기(scripts/metrics.py) 게이트 2종.
#
# 정상 경로: scripts/check_all.sh 가 이 파일을 source 하고 `run_gate <이름> <함수>` 를
# 제공한다. 이 파일은 check_all.sh 를 고치지 않는다(소유가 다른 레인이다).
#
# 직접 실행하면(= source 가 아니면) 같은 계약의 최소 대역 run_gate 를 스스로 세워
# 단독으로도 돈다. 대역은 **단독 실행 전용**이고, 게이트 정본은 언제나 check_all.sh
# 쪽 run_gate 다 — 두 구현이 갈라지면 정본이 이긴다.
#
# 무엇을 재는가:
#   ① tests/test_metrics.py 전량이 그린인가.
#   ② `python3 scripts/metrics.py --format json` 이 rc=0 이고, 그 출력이 파싱 가능한
#      JSON 이며 `schema_version` 을 담는가. (사슬이 0개여도 rc=0 이어야 한다 —
#      「아직 잴 것이 없다」와 「계기가 죽었다」는 다른 일이다.)

GATE50_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# --- 검사 ①: 지표 계기 시험 전량 -------------------------------------------
gate50_metrics_unittest() {
  if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 이 PATH 에 없다 — 지표 계기를 돌릴 수 없다"
    return 1
  fi
  ( cd "$GATE50_ROOT" && python3 -m unittest tests.test_metrics ) 2>&1
}

# --- 검사 ②: CLI 가 rc=0 이고 파싱 가능한 JSON 을 내는가 ---------------------
gate50_metrics_cli_json() {
  if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 이 PATH 에 없다 — 지표 계기를 돌릴 수 없다"
    return 1
  fi
  local tmp err rc
  tmp="$(mktemp "${TMPDIR:-/tmp}/metrics-gate.XXXXXX")" || {
    echo "mktemp 실패"
    return 1
  }
  err="${tmp}.err"
  # 판정할 명령을 파이프 왼쪽에 두지 않는다 — `cmd | tail` 의 rc 는 tail 의 것이다.
  ( cd "$GATE50_ROOT" && python3 scripts/metrics.py --format json ) >"$tmp" 2>"$err"
  rc=$?
  if [ "$rc" -ne 0 ]; then
    echo "scripts/metrics.py --format json 이 rc=$rc (0 을 기대함)"
    sed -n '1,20p' "$err"
    sed -n '1,20p' "$tmp"
    rm -f "$tmp" "$err"
    return 1
  fi
  if ! python3 - "$tmp" <<'PYCHECK'
import json
import sys

with open(sys.argv[1], "r", encoding="utf-8") as fh:
    doc = json.load(fh)
missing = [k for k in ("schema_version", "chains", "repo_metrics") if k not in doc]
if missing:
    sys.stderr.write("JSON 에 필수 키가 없다: %s\n" % ", ".join(missing))
    raise SystemExit(1)
PYCHECK
  then
    echo "출력이 파싱 가능한 JSON 이 아니거나 필수 키가 없다"
    sed -n '1,20p' "$tmp"
    rm -f "$tmp" "$err"
    return 1
  fi
  rm -f "$tmp" "$err"
  return 0
}

# --- 등록 ------------------------------------------------------------------
# check_all.sh 에서 source 되면 그쪽 run_gate 를 쓰고, 직접 실행되면 대역을 세운다.
GATE50_STANDALONE=0
if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  GATE50_STANDALONE=1
fi

if ! declare -F run_gate >/dev/null 2>&1; then
  if [ "$GATE50_STANDALONE" -eq 0 ]; then
    echo "50-metrics.sh: source 됐는데 run_gate 가 없다 — 게이트 하네스를 확인하라" >&2
    return 1
  fi
  PASS_COUNT=0
  FAIL_COUNT=0
  # 단독 실행 전용 대역. 정본은 scripts/check_all.sh 의 run_gate 다.
  run_gate() {
    local name="$1"
    shift
    local out rc
    out="$("$@" 2>&1)"
    rc=$?
    if [ "$rc" -eq 0 ]; then
      echo "PASS  $name"
      PASS_COUNT=$((PASS_COUNT + 1))
    else
      echo "FAIL  $name"
      if [ -n "$out" ]; then
        echo "$out" | sed 's/^/      /'
      fi
      FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
  }
fi

run_gate "지표 계기 시험 전량(tests/test_metrics.py)" gate50_metrics_unittest
run_gate "scripts/metrics.py --format json 이 rc=0 · 파싱 가능한 JSON" gate50_metrics_cli_json

if [ "$GATE50_STANDALONE" -eq 1 ]; then
  echo ""
  echo "${PASS_COUNT} passed, ${FAIL_COUNT} failed  (단독 실행 — 정본은 scripts/check_all.sh)"
  if [ "$FAIL_COUNT" -gt 0 ]; then
    exit 1
  fi
  exit 0
fi
