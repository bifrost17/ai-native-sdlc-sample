#!/usr/bin/env bash
# tests/test_evals.sh — evals 하네스의 게이트. **키가 필요 없다.**
#
# 이 시험이 재는 것
#   · 케이스 3건이 스키마를 지키는가(필수 키 · 판정 종류가 닫힌 집합 안 · 픽스처 실재)
#   · 결정론 채점기 evals/check.sh 의 rc 3분법 — 0 통과 / 1 결함 / 2 판정 불가
#   · evals/run.sh 의 「키 없음 = rc=2」 계약 — 「안 돌았다」를 「통과」로 내지 않는다
#   · .github/workflows/agent-evals.yml 의 비활성 트리거가 정말 비활성인가(「있는 척」 방지)
#
# 이 시험이 재지 않는 것
#   · 모델이 실제로 무엇을 쓰는가. 그건 ANTHROPIC_API_KEY 가 있어야 돌고(evals/run.sh)
#     CI 에 없다. 여기서 그린이 나와도 「evals 를 돌렸다」는 뜻이 아니다.
#
# 계기 다원화: 채점기 evals/check.sh 는 jq 로 JSON 을 읽고, 이 시험은 python3 stdlib 로
# 같은 파일을 읽는다(VERIFY 「계기 다원화」). 두 구현이 다른 답을 내면 그 자리가 결함이다.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

CASE_IDS="01-intent-placeholder 02-no-self-accept 03-spec-carries-questions"

PASS_COUNT=0
FAIL_COUNT=0

ok() {
  echo "PASS  $1"
  PASS_COUNT=$((PASS_COUNT + 1))
}

ng() {
  echo "FAIL  $1"
  shift
  if [ "$#" -gt 0 ] && [ -n "${1:-}" ]; then
    printf '%s\n' "$1" | sed 's/^/      /'
  fi
  FAIL_COUNT=$((FAIL_COUNT + 1))
}

run_case() {
  local name="$1"
  shift
  local out
  if out="$("$@" 2>&1)"; then
    ok "$name"
  else
    ng "$name" "$out"
  fi
}

# check.sh 를 돌려 rc 와 출력을 전역에 남긴다.
CHECK_RC=0
CHECK_OUT=""
run_check() {
  CHECK_OUT="$(bash evals/check.sh "$@" 2>&1)"
  CHECK_RC=$?
  return 0
}

# --- 1. 케이스 3건이 스키마를 지키는가 -----------------------------------
# 필수 키 · 판정 종류가 check.sh 가 선언한 닫힌 집합 안 · files[] 픽스처 실재
# (honghu 반례: 케이스가 첨부를 가리키는데 fixture 가 0개였다).
t1_case_schema() {
  if [ ! -f evals/check.sh ]; then
    echo "evals/check.sh 없음 — 판정 종류의 정본을 읽을 수 없다"
    return 1
  fi
  local kinds
  if ! kinds="$(bash evals/check.sh --kinds 2>&1)"; then
    echo "evals/check.sh --kinds 실패(rc≠0): $kinds"
    return 1
  fi
  if [ -z "$kinds" ]; then
    echo "evals/check.sh --kinds 가 빈 목록을 냈다 — 닫힌 집합이 비면 무엇이든 통과한다"
    return 1
  fi
  python3 - "$kinds" $CASE_IDS <<'PY'
import json, os, sys

kinds = set(sys.argv[1].split())
case_ids = sys.argv[2:]
required_top = ["schema_version", "id", "prompt", "expected_output", "files",
                "assertions", "checks"]
required_by_kind = {
    "file_exists": ["path"],
    "contains": ["path", "value"],
    "not_contains": ["path", "value"],
    "regex_present": ["path", "pattern"],
    "regex_absent": ["path", "pattern"],
    "frontmatter_has_keys": ["path", "keys"],
    "frontmatter_equals": ["path", "key", "value"],
}
errs = []
for cid in case_ids:
    p = os.path.join("evals", "cases", cid + ".json")
    if not os.path.isfile(p):
        errs.append("케이스 파일 없음: " + p)
        continue
    try:
        c = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        errs.append("%s: JSON 파싱 실패 — %s" % (p, e))
        continue
    for k in required_top:
        if k not in c:
            errs.append("%s: 필수 키 없음 — %s" % (p, k))
    if c.get("schema_version") != 1:
        errs.append("%s: schema_version 이 1 이 아님 — %r" % (p, c.get("schema_version")))
    if c.get("id") != cid:
        errs.append("%s: id 가 파일명과 다름 — %r" % (p, c.get("id")))
    if not str(c.get("prompt", "")).strip():
        errs.append("%s: prompt 가 비었다" % p)
    checks = c.get("checks")
    if not isinstance(checks, list) or not checks:
        errs.append("%s: checks 가 비었거나 배열이 아니다" % p)
        continue
    for i, ch in enumerate(checks):
        kind = ch.get("kind")
        if kind not in kinds:
            errs.append("%s: checks[%d].kind 가 닫힌 집합 밖 — %r (허용: %s)"
                        % (p, i, kind, " ".join(sorted(kinds))))
            continue
        for f in required_by_kind.get(kind, []):
            if f not in ch:
                errs.append("%s: checks[%d](%s) 에 %s 없음" % (p, i, kind, f))
        path = ch.get("path", "")
        if path.startswith("/") or ".." in path.split("/"):
            errs.append("%s: checks[%d].path 가 워크스페이스를 벗어난다 — %r" % (p, i, path))
    for f in c.get("files", []):
        if not os.path.exists(f):
            errs.append("%s: files[] 가 가리키는 픽스처가 없다 — %s" % (p, f))
if errs:
    print("\n".join(errs))
    sys.exit(1)
print("케이스 %d건 스키마 그린 (판정 종류 닫힌 집합: %s)" % (len(case_ids), " ".join(sorted(kinds))))
PY
}

# --- 2. 통과 픽스처에 rc=0 ------------------------------------------------
t2_pass_fixtures() {
  local rc=0 pair cid dir
  for pair in "01-intent-placeholder:01-pass" \
              "02-no-self-accept:02-pass" \
              "03-spec-carries-questions:03-pass"; do
    cid="${pair%%:*}"
    dir="${pair##*:}"
    run_check "evals/cases/$cid.json" "evals/testdata/$dir/result.json"
    if [ "$CHECK_RC" -ne 0 ]; then
      echo "$dir: rc=$CHECK_RC (0 을 기대) — 출력:"
      printf '%s\n' "$CHECK_OUT" | sed 's/^/  /'
      rc=1
    fi
  done
  return "$rc"
}

# --- 3. 위반 픽스처에 rc=1 이고 「무엇이 왜」를 출력하는가 ------------------
t3_violation_fixtures() {
  local rc=0 triple cid dir want
  for triple in "01-intent-placeholder:01-fail-placeholder:not_contains" \
                "02-no-self-accept:02-fail-accepted:frontmatter_equals" \
                "03-spec-carries-questions:03-fail-carry:regex_present"; do
    cid="$(echo "$triple" | cut -d: -f1)"
    dir="$(echo "$triple" | cut -d: -f2)"
    want="$(echo "$triple" | cut -d: -f3)"
    run_check "evals/cases/$cid.json" "evals/testdata/$dir/result.json"
    if [ "$CHECK_RC" -ne 1 ]; then
      echo "$dir: rc=$CHECK_RC (1 을 기대) — 출력:"
      printf '%s\n' "$CHECK_OUT" | sed 's/^/  /'
      rc=1
      continue
    fi
    if ! printf '%s\n' "$CHECK_OUT" | grep -q "FAIL"; then
      echo "$dir: rc=1 인데 출력에 FAIL 줄이 없다 — 무엇이 실패했는지 못 읽는다"
      rc=1
    fi
    if ! printf '%s\n' "$CHECK_OUT" | grep -q "$want"; then
      echo "$dir: 실패 줄이 판정 종류 '$want' 를 이름으로 대지 않는다 — 출력:"
      printf '%s\n' "$CHECK_OUT" | sed 's/^/  /'
      rc=1
    fi
  done
  return "$rc"
}

# --- 4. 없는 파일 → rc=2 --------------------------------------------------
# 인자로 받은 파일이 없을 때(케이스·결과 둘 다)와 워크스페이스 디렉터리가
# 없을 때. 셋 다 「판정 불가」이지 「통과」가 아니다.
t4_missing_files() {
  local rc=0
  run_check "evals/cases/does-not-exist.json" "evals/testdata/01-pass/result.json"
  if [ "$CHECK_RC" -ne 2 ]; then
    echo "없는 케이스 파일: rc=$CHECK_RC (2 를 기대)"; rc=1
  fi
  run_check "evals/cases/01-intent-placeholder.json" "evals/testdata/01-pass/does-not-exist.json"
  if [ "$CHECK_RC" -ne 2 ]; then
    echo "없는 결과 파일: rc=$CHECK_RC (2 를 기대)"; rc=1
  fi
  run_check "evals/cases/01-intent-placeholder.json" "evals/testdata/no-workspace/result.json"
  if [ "$CHECK_RC" -ne 2 ]; then
    echo "없는 워크스페이스: rc=$CHECK_RC (2 를 기대)"; rc=1
  fi
  return "$rc"
}

# --- 5. 지원하지 않는 판정 종류 → rc=2 ------------------------------------
t5_unknown_kind() {
  run_check "evals/testdata/bad-kind/case.json" "evals/testdata/02-pass/result.json"
  if [ "$CHECK_RC" -ne 2 ]; then
    echo "닫힌 집합 밖 kind: rc=$CHECK_RC (2 를 기대) — 조용히 건너뛰면 안 된다. 출력:"
    printf '%s\n' "$CHECK_OUT" | sed 's/^/  /'
    return 1
  fi
  return 0
}

# --- 6. run.sh 는 키가 없으면 rc=2 이고 SKIP 문구를 찍는다 -----------------
# 「안 돌았다」와 「통과했다」를 같은 값으로 내지 않는다는 계약.
t6_runsh_without_key() {
  if [ ! -f evals/run.sh ]; then
    echo "evals/run.sh 없음"
    return 1
  fi
  local out rc
  out="$(env -u ANTHROPIC_API_KEY bash evals/run.sh 2>&1)"
  rc=$?
  local err=0
  if [ "$rc" -ne 2 ]; then
    echo "run.sh(키 없음): rc=$rc (2 를 기대) — rc=0 이면 「안 돌았다」가 「통과」로 새어 나간다"
    err=1
  fi
  if ! printf '%s\n' "$out" | grep -q 'SKIP: ANTHROPIC_API_KEY 없음 — evals 는 돌지 않았다'; then
    echo "run.sh(키 없음): 표준출력에 SKIP 문구가 없다 — 출력:"
    printf '%s\n' "$out" | sed 's/^/  /'
    err=1
  fi
  return "$err"
}

# --- 7. jq 없는 PATH 에서도 rc=2 로 정직하게 죽는가 ------------------------
# jsnkle·imsungbin 반례: jq 부재에서 fail-open 으로 조용히 통과했다.
t7_no_jq_dies() {
  local emptydir out rc
  emptydir="$(mktemp -d)"
  out="$(PATH="$emptydir" "$BASH" "$ROOT/evals/check.sh" \
        "$ROOT/evals/cases/01-intent-placeholder.json" \
        "$ROOT/evals/testdata/01-pass/result.json" 2>&1)"
  rc=$?
  rmdir "$emptydir" 2>/dev/null
  if [ "$rc" -ne 2 ]; then
    echo "jq 없는 PATH: rc=$rc (2 를 기대) — 출력:"
    printf '%s\n' "$out" | sed 's/^/  /'
    return 1
  fi
  if ! printf '%s\n' "$out" | grep -qi 'jq'; then
    echo "jq 없는 PATH: rc=2 인데 사유에 jq 가 없다 — 출력:"
    printf '%s\n' "$out" | sed 's/^/  /'
    return 1
  fi
  return 0
}

# --- 8. 워크플로의 schedule·pull_request 가 활성이 아닌가 ------------------
# 레슨 9 는 스케줄·PR 트리거를 요구하지만 이 레포엔 키·예산이 없다(설계안 §10).
# 주석으로 남긴 트리거가 「있는 척」이 되지 않게, 활성 상태가 아님을 기계가 잰다.
WORKFLOW=".github/workflows/agent-evals.yml"

t8_workflow_triggers_inactive() {
  if [ ! -f "$WORKFLOW" ]; then
    echo "$WORKFLOW 없음"
    return 1
  fi
  local uncommented active rc=0
  uncommented="$(grep -vE '^[[:space:]]*#' "$WORKFLOW")"
  active="$(printf '%s\n' "$uncommented" | grep -nE '^[[:space:]]*(schedule|pull_request)[[:space:]]*:' || true)"
  if [ -n "$active" ]; then
    echo "$WORKFLOW: schedule/pull_request 가 주석 밖(활성)에 있다 —"
    printf '%s\n' "$active" | sed 's/^/  /'
    rc=1
  fi
  # 양성 대조 1: workflow_dispatch 는 활성이어야 한다(전부 비활성이면 이 검사는 공허하다).
  if ! printf '%s\n' "$uncommented" | grep -qE '^[[:space:]]*workflow_dispatch[[:space:]]*:'; then
    echo "$WORKFLOW: workflow_dispatch 가 활성이 아니다 — imsungbin 은 disabled_manually 로 두어 한 번도 안 돌았다"
    rc=1
  fi
  # 양성 대조 2: 주석 처리된 schedule·pull_request 가 실제로 있어야 한다
  # (지워 버리면 이 검사엔 잡을 대상이 없어 항상 그린이 된다).
  if ! grep -qE '^[[:space:]]*#.*schedule' "$WORKFLOW"; then
    echo "$WORKFLOW: 주석 처리된 schedule 트리거가 없다 — 검사 대상이 사라졌다"
    rc=1
  fi
  if ! grep -qE '^[[:space:]]*#.*pull_request' "$WORKFLOW"; then
    echo "$WORKFLOW: 주석 처리된 pull_request 트리거가 없다 — 검사 대상이 사라졌다"
    rc=1
  fi
  return "$rc"
}

# --- 9. 워크플로가 「비활성 사유」를 이름·설명에 밝히는가 -------------------
t9_workflow_declares_inactive() {
  if [ ! -f "$WORKFLOW" ]; then
    echo "$WORKFLOW 없음"
    return 1
  fi
  local rc=0
  if ! grep -qE '^name:.*(수동|workflow_dispatch|manual)' "$WORKFLOW"; then
    echo "$WORKFLOW: name: 이 「수동 전용」임을 밝히지 않는다"
    rc=1
  fi
  if ! grep -q 'ANTHROPIC_API_KEY' "$WORKFLOW"; then
    echo "$WORKFLOW: 비활성 사유(키 없음)를 문면에 적지 않았다"
    rc=1
  fi
  if ! grep -qE '^permissions:' "$WORKFLOW"; then
    echo "$WORKFLOW: permissions: 선언이 없다"
    rc=1
  fi
  return "$rc"
}

# --- 10. 셸 구문 ----------------------------------------------------------
t10_shell_syntax() {
  local f rc=0
  for f in evals/check.sh evals/run.sh scripts/gates/60-evals.sh tests/test_evals.sh; do
    if [ ! -f "$f" ]; then
      echo "$f 없음"
      rc=1
      continue
    fi
    if ! bash -n "$f" 2>&1; then
      echo "구문 오류: $f"
      rc=1
    fi
  done
  return "$rc"
}

run_case "1. 케이스 3건 스키마(필수 키 · 닫힌 집합 · 픽스처 실재)" t1_case_schema
run_case "2. check.sh 가 통과 픽스처 3건에 rc=0" t2_pass_fixtures
run_case "3. check.sh 가 위반 픽스처 3건에 rc=1 + 사유 출력" t3_violation_fixtures
run_case "4. 없는 케이스/결과/워크스페이스 → rc=2" t4_missing_files
run_case "5. 닫힌 집합 밖 판정 종류 → rc=2" t5_unknown_kind
run_case "6. run.sh 는 키 없으면 rc=2 + SKIP 문구" t6_runsh_without_key
run_case "7. jq 없는 PATH 에서 check.sh 가 rc=2" t7_no_jq_dies
run_case "8. 워크플로의 schedule·pull_request 가 비활성" t8_workflow_triggers_inactive
run_case "9. 워크플로가 수동 전용·비활성 사유를 문면에 명시" t9_workflow_declares_inactive
run_case "10. evals 하네스 셸 파일이 bash -n 통과" t10_shell_syntax

echo ""
echo "${PASS_COUNT} passed, ${FAIL_COUNT} failed"

if [ "$FAIL_COUNT" -gt 0 ]; then
  exit 1
fi
exit 0
