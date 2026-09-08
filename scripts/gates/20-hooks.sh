#!/usr/bin/env bash
# scripts/gates/20-hooks.sh — 강제층(훅) 게이트.
#
# scripts/check_all.sh 가 끝에서 scripts/gates/*.sh 를 source 하면 여기 두 줄이
# 게이트 정본에 붙는다. check_all.sh 자체는 이 레인이 만지지 않는다(파일 소유 1:1).
#
# check_all.sh 안에서 source 되면 그쪽의 run_gate 를 그대로 쓴다. 홀로 실행하면
# (bash scripts/gates/20-hooks.sh) 같은 의미의 최소 run_gate 를 임시로 정의해
# 단독 실행도 되게 한다 — 그래야 형제 레인이 확장 지점을 넣기 전에도 이 게이트를
# 원문으로 돌려 볼 수 있다.

if ! declare -f run_gate >/dev/null 2>&1; then
  __OWA_STANDALONE=1
  PASS_COUNT=${PASS_COUNT:-0}
  FAIL_COUNT=${FAIL_COUNT:-0}
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
  cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)" || exit 1
fi

run_gate "훅 우회 시험" bash tests/test_hooks.sh
run_gate "훅 배선" bash tests/test_wiring.sh

if [ "${__OWA_STANDALONE:-0}" = "1" ]; then
  echo ""
  echo "${PASS_COUNT} passed, ${FAIL_COUNT} failed"
  [ "$FAIL_COUNT" -gt 0 ] && exit 1
  exit 0
fi
