#!/usr/bin/env bash
# scripts/gates/30-bands.sh — Stage 6 밴드 검출기 게이트.
#
# scripts/check_all.sh 가 끝에서 scripts/gates/*.sh 를 source 하고 run_gate 를
# 제공한다는 전제다. 이 파일은 게이트 하나만 등록하고 check_all.sh 는 건드리지
# 않는다(파일 소유 1:1).
#
# ⚠️ run_gate 가 없으면 **조용히 통과하지 않고** 실패한다. 확장 지점이 아직 없거나
# 이름이 바뀌었는데 이 파일이 아무 말 없이 넘어가면, 게이트가 도는 줄 알지만
# 실제로는 아무것도 재지 않는 자리가 생긴다 — 그것이 가장 비싼 거짓 초록이다.
#
# 재는 것: tests/test_detect_bands.py (검출기 판정 · rc 계약 · σ=0 가드 ·
#          emit_intent 초안 스키마). 실행 위치는 레포 루트여야 한다
#          (check_all.sh 가 이미 cd 해 둔다).

if ! declare -F run_gate >/dev/null 2>&1; then
  echo "scripts/gates/30-bands.sh: run_gate 가 정의돼 있지 않다 — 이 파일은" >&2
  echo "  scripts/check_all.sh 가 source 해야 하고 혼자서는 아무것도 재지 않는다." >&2
  echo "  단독 실행이 필요하면: python3 -m unittest tests.test_detect_bands" >&2
  return 1 2>/dev/null || exit 1
fi

run_gate "밴드 검출 시험 (tests/test_detect_bands.py)" \
  python3 -m unittest tests.test_detect_bands
