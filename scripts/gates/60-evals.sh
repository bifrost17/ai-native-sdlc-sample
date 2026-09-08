#!/usr/bin/env bash
# scripts/gates/60-evals.sh — 게이트 조각. scripts/check_all.sh 가 source 한다.
#
# 등록하는 것: evals 하네스의 결정론 게이트(tests/test_evals.sh · 키 불요).
# 등록하지 않는 것: evals/run.sh — 모델과 API 키가 필요해 CI 에 없다.
#   그 갈래는 .github/workflows/agent-evals.yml 을 손으로 돌릴 때만 도는데,
#   키가 없으면 rc=2(판정 불가)를 내고 그 사실을 명시적으로 보고한다.
#   「안 돌았다」를 「통과했다」로 바꾸지 않는 것이 이 하네스의 계약이다.
#
# 이 파일은 실행 파일이 아니다 — run_gate 는 check_all.sh 가 정의한다.
# 직접 실행하면 무엇이 잘못됐는지 말하고 rc=2 로 죽는다(조용한 no-op 금지).

if ! declare -F run_gate >/dev/null 2>&1; then
  echo "60-evals.sh: run_gate 가 정의돼 있지 않다 — 이 파일은 scripts/check_all.sh 가 source 한다." >&2
  echo "             단독으로 재려면: bash tests/test_evals.sh" >&2
  exit 2
fi

run_gate "evals 하네스" bash tests/test_evals.sh
