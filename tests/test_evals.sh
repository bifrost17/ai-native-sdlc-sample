#!/usr/bin/env bash
# tests/test_evals.sh — evals 하네스 게이트. 키 불요 (레슨 9·10).
# L10 727행: "the pass-rate threshold is enforced as a merge check" — 이 시험이
# 그 결정론 반쪽(케이스 스키마·채점기 rc 3분법·run.sh 의 "키 없음=rc=2" 계약)이다.
# 모델이 실제로 무엇을 쓰는지는 ANTHROPIC_API_KEY 가 있어야 돌아 CI 밖.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$ROOT" || exit 1
PASS=0; FAIL=0
ok() { echo "PASS  $1"; PASS=$((PASS+1)); }
ng() { echo "FAIL  $1: $2"; FAIL=$((FAIL+1)); }

# 1. 케이스 전량 스키마(evals/cases/*.json 발견 — 하드코딩 아님) — 필수 키 · kind 가 닫힌 집합 안 · 픽스처 실재.
out="$(python3 - <<'PY'
import glob, json, os, sys
kinds = set(l for l in os.popen("bash evals/check.sh --kinds").read().splitlines() if l)
req = ["schema_version", "id", "prompt", "expected_output", "files", "assertions", "checks"]
errs = []
for p in sorted(glob.glob("evals/cases/*.json")):
    cid = os.path.basename(p)[:-len(".json")]
    c = json.load(open(p, encoding="utf-8"))
    for k in req:
        if k not in c: errs.append("%s: 키 없음 %s" % (p, k))
    if c.get("id") != cid: errs.append("%s: id 불일치" % p)
    for ch in c.get("checks", []):
        if ch.get("kind") not in kinds: errs.append("%s: kind 밖 %r" % (p, ch.get("kind")))
    for f in c.get("files", []):
        if not os.path.exists(f): errs.append("%s: 픽스처 없음 %s" % (p, f))
print("\n".join(errs))
sys.exit(1 if errs else 0)
PY
)"
[ -z "$out" ] && ok "1. 케이스 전량 스키마" || ng "1. 케이스 전량 스키마" "$out"

# 2. 통과 픽스처 3건 → rc=0.
rc=0
for pair in "01-intent-placeholder:01-pass" "02-no-self-accept:02-pass" "03-spec-carries-questions:03-pass"; do
  cid="${pair%%:*}"; dir="${pair##*:}"
  bash evals/check.sh "evals/cases/$cid.json" "evals/testdata/$dir/result.json" >/dev/null 2>&1 || rc=1
done
[ "$rc" -eq 0 ] && ok "2. 통과 픽스처 rc=0 (01-pass = capture-intent 스킬대로 손으로 쓴 intent)" || ng "2. 통과 픽스처 rc=0" "하나 이상 rc≠0"

# 3. 위반 픽스처 3건 → rc=1 + FAIL 줄.
rc=0
for pair in "01-intent-placeholder:01-fail-placeholder" "02-no-self-accept:02-fail-accepted" "03-spec-carries-questions:03-fail-carry"; do
  cid="${pair%%:*}"; dir="${pair##*:}"
  o="$(bash evals/check.sh "evals/cases/$cid.json" "evals/testdata/$dir/result.json" 2>&1)"
  c="$?"
  [ "$c" -eq 1 ] && echo "$o" | grep -q FAIL || rc=1
done
[ "$rc" -eq 0 ] && ok "3. 위반 픽스처 rc=1+FAIL" || ng "3. 위반 픽스처 rc=1+FAIL" "계약 위반"

# 4. 없는 케이스/결과/워크스페이스 → rc=2.
rc=0
bash evals/check.sh evals/cases/does-not-exist.json evals/testdata/01-pass/result.json >/dev/null 2>&1; [ "$?" -eq 2 ] || rc=1
bash evals/check.sh evals/cases/01-intent-placeholder.json evals/testdata/no-workspace/result.json >/dev/null 2>&1; [ "$?" -eq 2 ] || rc=1
[ "$rc" -eq 0 ] && ok "4. 없는 파일/워크스페이스 → rc=2" || ng "4. 없는 파일/워크스페이스 → rc=2" "계약 위반"

# 5. 닫힌 집합 밖 kind → rc=2.
bash evals/check.sh evals/testdata/bad-kind/case.json evals/testdata/02-pass/result.json >/dev/null 2>&1
[ "$?" -eq 2 ] && ok "5. 닫힌 집합 밖 kind → rc=2" || ng "5. 닫힌 집합 밖 kind → rc=2" "건너뛰었다"

# 6. run.sh 키 없음 → rc=2 + SKIP.
o="$(env -u ANTHROPIC_API_KEY bash evals/run.sh 2>&1)"; c="$?"
[ "$c" -eq 2 ] && echo "$o" | grep -q "SKIP: ANTHROPIC_API_KEY" \
  && ok "6. run.sh 키 없음 → rc=2+SKIP" || ng "6. run.sh 키 없음 → rc=2+SKIP" "$o"

# 7. jq 없는 PATH → rc=2.
empty="$(mktemp -d)"
PATH="$empty" "$(command -v bash)" evals/check.sh evals/cases/01-intent-placeholder.json \
  evals/testdata/01-pass/result.json >/dev/null 2>&1
c="$?"; rmdir "$empty" 2>/dev/null
[ "$c" -eq 2 ] && ok "7. jq 없는 PATH → rc=2" || ng "7. jq 없는 PATH → rc=2" "rc=$c"

# 8. 셸 구문.
rc=0
for f in evals/check.sh evals/run.sh tests/test_evals.sh; do bash -n "$f" || rc=1; done
[ "$rc" -eq 0 ] && ok "8. 셸 구문" || ng "8. 셸 구문" "bash -n 실패"

echo ""; echo "${PASS} passed, ${FAIL} failed"
[ "$FAIL" -gt 0 ] && exit 1
exit 0
