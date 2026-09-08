#!/usr/bin/env bash
# scripts/check_all.sh — 게이트 정본 (= `make check`).
#
# 이 게이트가 재지 않는 것: 아티팩트(intent/spec/plan) 검증기는 아직 없다.
# frontmatter · 상태 전이 · upstream sha 무결성 · 사슬 완결성은 W1 이 들여올
# scripts/check_artifacts.py 부터 잰다. 여기 6개는 W0 골격(문서 존재 · 분량 ·
# 라이선스 · 출처 표기 · 셸 구문 · README 경로 정합)만 확인하는 최소 게이트다.
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT" || exit 1

PASS_COUNT=0
FAIL_COUNT=0

# run_gate <이름> <검사 함수> — 함수를 실행하고 rc 로 PASS/FAIL 한 줄을 찍는다.
# 실패 시 함수가 표준출력/표준에러에 쓴 진단을 들여써서 함께 보여준다.
run_gate() {
  local name="$1"
  shift
  local out rc
  out="$("$@" 2>&1)"
  rc=$?
  if [[ "$rc" -eq 0 ]]; then
    echo "PASS  $name"
    PASS_COUNT=$((PASS_COUNT + 1))
  else
    echo "FAIL  $name"
    if [[ -n "$out" ]]; then
      echo "$out" | sed 's/^/      /'
    fi
    FAIL_COUNT=$((FAIL_COUNT + 1))
  fi
}

# --- 검사 1: docs/DESIGN.md 존재 + 200줄 이상 ---
check1_design_doc() {
  if [[ ! -f docs/DESIGN.md ]]; then
    echo "docs/DESIGN.md 없음"
    return 1
  fi
  local n
  n="$(wc -l < docs/DESIGN.md | tr -d ' ')"
  if [[ "$n" -lt 200 ]]; then
    echo "docs/DESIGN.md 이 ${n}줄뿐 — 200줄 이상 필요"
    return 1
  fi
  return 0
}

# --- 검사 2: README.md · LICENSE · NOTICE 존재 + 각 10줄 이상 ---
check2_core_docs() {
  local f n rc=0
  for f in README.md LICENSE NOTICE; do
    if [[ ! -f "$f" ]]; then
      echo "$f 없음"
      rc=1
      continue
    fi
    n="$(wc -l < "$f" | tr -d ' ')"
    if [[ "$n" -lt 10 ]]; then
      echo "$f 이 ${n}줄뿐 — 10줄 이상 필요"
      rc=1
    fi
  done
  return "$rc"
}

# --- 검사 3: LICENSE 첫 줄이 "MIT License" ---
check3_license_header() {
  if [[ ! -f LICENSE ]]; then
    echo "LICENSE 없음"
    return 1
  fi
  local first
  first="$(head -n 1 LICENSE)"
  if [[ "$first" != "MIT License" ]]; then
    echo "LICENSE 첫 줄이 '$first' — 'MIT License' 를 기대함"
    return 1
  fi
  return 0
}

# --- 검사 4: NOTICE 가 5개 출처를 전부 포함 ---
check4_notice_sources() {
  if [[ ! -f NOTICE ]]; then
    echo "NOTICE 없음"
    return 1
  fi
  local src rc=0
  for src in jcuervo jsnkle imsungbin bashebr simonsez9510; do
    if ! grep -q "$src" NOTICE; then
      echo "NOTICE 에 출처 누락: $src"
      rc=1
    fi
  done
  return "$rc"
}

# --- 검사 5: 레포 안 모든 *.sh 가 bash -n 을 통과 ---
# bash 3.2(macOS 기본) 호환: mapfile/readarray 대신 while-read + process substitution.
check5_shell_syntax() {
  local f err rc=0
  while IFS= read -r f || [[ -n "$f" ]]; do
    [[ -z "$f" ]] && continue
    if ! err="$(bash -n "$f" 2>&1)"; then
      echo "구문 오류: $f"
      if [[ -n "$err" ]]; then
        echo "$err" | sed 's/^/  /'
      fi
      rc=1
    fi
  done < <(find . -name '*.sh' -not -path './.git/*' | sort)
  return "$rc"
}

# --- 검사 6: README.md 「## 지금 상태」 절 표가 가리키는 레포 내부 경로가 실재 ---
# 대상은 하드코딩한다(동적 파싱 아님) — README 는 「앞으로 들어올 것」 절에서
# 아직 없는 파일(예: intent/, src/, .claude/)도 언급하므로, 그 절까지 긁으면
# W0 시점엔 항상 FAIL 이 나 게이트가 쓸모없어진다. 「## 지금 상태 — W0 (골격)」
# 절 표 안의 백틱 docs/…·scripts/… 경로만 대상 — 지금은 두 개뿐이다:
#   `docs/DESIGN.md`         (1행 1열)
#   `scripts/check_all.sh`   (3행 2열, "무엇을 재는지는 `scripts/check_all.sh`")
# `NOTICE`·`make check` 는 docs/·scripts/ 접두가 아니므로 대상이 아니다.
README_STATUS_PATHS="docs/DESIGN.md scripts/check_all.sh"

check6_readme_paths() {
  local p rc=0
  for p in $README_STATUS_PATHS; do
    if [[ ! -e "$p" ]]; then
      echo "README 「지금 상태」 절 표가 가리키는 경로가 실재하지 않음: $p"
      rc=1
    fi
  done
  return "$rc"
}

run_gate "docs/DESIGN.md 존재 + 200줄 이상" check1_design_doc
run_gate "README.md/LICENSE/NOTICE 존재 + 각 10줄 이상" check2_core_docs
run_gate "LICENSE 첫 줄 == 'MIT License'" check3_license_header
run_gate "NOTICE 가 5개 출처(jcuervo/jsnkle/imsungbin/bashebr/simonsez9510) 포함" check4_notice_sources
run_gate "레포 내 전체 *.sh 가 bash -n 통과" check5_shell_syntax
run_gate "README 「지금 상태」 절 표의 경로가 실재" check6_readme_paths

echo ""
echo "${PASS_COUNT} passed, ${FAIL_COUNT} failed"

if [[ "$FAIL_COUNT" -gt 0 ]]; then
  exit 1
fi
exit 0
