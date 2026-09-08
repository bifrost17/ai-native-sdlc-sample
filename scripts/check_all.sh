#!/usr/bin/env bash
# scripts/check_all.sh — 게이트 정본 (= `make check`).
#
# 검사 1~6 은 W0 골격(문서 존재 · 분량 · 라이선스 · 출처 표기 · 셸 구문 ·
# README 경로 정합)이고, 7~11 은 아티팩트 검증기(scripts/check_artifacts.py)를
# 양쪽에서 잡아 둔다: 템플릿은 반드시 red · green 픽스처는 반드시 통과 ·
# red 픽스처는 **지정한 code 로** red. 한쪽만 있으면 게이트가 조용히 빈 통과가 된다.
#
# 이 게이트가 재지 않는 것: 훅 배선(W1-B 가 scripts/gates/ 로 붙인다) ·
# 산문 품질 · 「요구가 문제를 푸는가」(검증기 --help 의 배타절 참조).
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT" || exit 1

PASS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0

# run_gate <이름> <검사 함수> — 함수를 실행하고 rc 로 PASS/FAIL/SKIP 한 줄을 찍는다.
# 실패 시 함수가 표준출력/표준에러에 쓴 진단을 들여써서 함께 보여준다.
#
# rc 규약:  0 = PASS · 3 = SKIP(전제가 아직 없다 — 조용한 통과 금지) · 그 외 = FAIL.
# SKIP 은 그린이 아니다. 요약 줄이 skipped 를 따로 세는 이유가 그것이다.
# scripts/gates/*.sh 는 이 함수를 그대로 불러 쓴다(파일 끝의 확장 지점 참조).
# 인자를 하나 주면 그 검사 **함수** 하나만 돈다(`make check` 는 인자 없이 부르므로 전량).
# 시험이 「CI 모양 출력」에서 토큰을 셀 때 이 통로를 쓴다 — 전량을 다시 돌리면
# check10(시험 묶음)이 자기를 다시 불러 재귀가 된다.
#
# 🔴 어느 검사와도 안 맞으면 **죽는다**. 아무것도 재지 않고 rc=0 을 내는 통로는 이 게이트의
# 명제(「안 돌았다 ≠ 통과했다」)와 정면으로 어긋난다 — 오타 하나가 「0 passed, 0 failed」
# rc=0 이 됐다. 필터는 `run_gate` 에 넘긴 명령의 첫 낱말과 견주므로 `python3` 같은 낱말도
# 걸렸다(그러면 그 한 검사만 돌고 rc=0). 그래서 **셸 함수인 것만** 게이트 이름으로 친다.
ONLY_GATE="${1:-}"
ONLY_GATE_MATCHES=0

# check11 이 rc=0 이어도 note 는 흘려보내기 위한 통로. run_gate 는 PASS 일 때 함수
# 출력을 통째로 버리는데, fd 3 은 그 명령 치환 밖(원래 stdout)을 가리킨다.
exec 3>&1

run_gate() {
  local name="$1"
  shift
  if [[ -n "$ONLY_GATE" ]]; then
    if [[ "$ONLY_GATE" != "$1" ]] || ! declare -F "$1" >/dev/null 2>&1; then
      return 0
    fi
    ONLY_GATE_MATCHES=$((ONLY_GATE_MATCHES + 1))
  fi
  local out rc
  out="$("$@" 2>&1)"
  rc=$?
  if [[ "$rc" -eq 0 ]]; then
    echo "PASS  $name"
    PASS_COUNT=$((PASS_COUNT + 1))
  elif [[ "$rc" -eq 3 ]]; then
    echo "SKIP  $name"
    if [[ -n "$out" ]]; then
      echo "$out" | sed 's/^/      /'
    fi
    SKIP_COUNT=$((SKIP_COUNT + 1))
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

# --- 검사 7: templates/*.md 는 반드시 rc=1 (게이트 상주 음성 대조) ---
# 템플릿엔 자리표시자 ‹…›가 남아 있으므로 검증기가 반드시 잡아야 한다. 이 검사가
# 없으면 「검증기가 아무것도 안 잡는 상태」와 「다 통과하는 상태」를 구별할 수 없다.
check7_templates_are_red() {
  local f rc=0 out prc
  if [[ ! -d templates ]]; then
    echo "templates/ 없음"
    return 1
  fi
  while IFS= read -r f || [[ -n "$f" ]]; do
    [[ -z "$f" ]] && continue
    out="$(python3 scripts/check_artifacts.py "$f" 2>&1)"
    prc=$?
    if [[ "$prc" -ne 1 ]]; then
      echo "$f 가 rc=$prc — 템플릿은 rc=1 이어야 한다"
      echo "$out" | sed 's/^/  /'
      rc=1
    fi
  done < <(find templates -maxdepth 1 -name '*.md' | sort)
  return "$rc"
}

# --- 검사 8: tests/fixtures/green/* 는 rc=0 (거짓 양성 대조) ---
# 대괄호([Art. 4])·인용부호(「」『』【】)가 섞인 정상 문서를 반려하지 않는가.
check8_fixtures_green() {
  python3 tests/run_fixtures.py --set green
}

# --- 검사 9: tests/fixtures/red/* 는 **지정한 code** 로 rc=1 ---
# 「red 이기만 하면 통과」로 두면 엉뚱한 이유로 빨간 픽스처가 그 축을 못 재는 채
# 통과한다. EXPECT 의 code 다중집합과 정확히 대조한다.
check9_fixtures_red() {
  python3 tests/run_fixtures.py --set red
}

# --- 검사 10: 시험 묶음 일괄 실행 ---
check10_unittest() {
  python3 -m unittest discover -s tests
}

# --- 검사 11: intent/*/ 사슬이 있으면 전부 rc=0 · 없으면 SKIP ---
# 사슬은 W2 에 들어온다. 지금 없다고 조용히 통과시키지 않는다 — rc=3 으로 SKIP 을
# 명시 출력하고 요약의 skipped 로 센다.
check11_intent_chain() {
  local d files rc=0 out prc
  files=""
  # `-maxdepth 2` 는 intent/<id>/v2/intent.md 같은 깊은 경로를 안 골랐다 — 직접
  # 검사하면 red 가 나는 파일이 게이트 사정거리 밖에 있었다(E7). 넓히는 방향이라
  # 포착을 잃지 않는다.
  while IFS= read -r d || [[ -n "$d" ]]; do
    [[ -z "$d" ]] && continue
    files="$files $d"
  done < <(find intent -mindepth 2 -name '*.md' 2>/dev/null | sort)
  if [[ -z "${files// /}" ]]; then
    echo "intent/*/ 사슬이 아직 없다 (W2 에 들어온다) — 검사하지 않았다"
    return 3
  fi
  # shellcheck disable=SC2086
  out="$(python3 scripts/check_artifacts.py $files 2>&1)"
  prc=$?
  if [[ "$prc" -eq 0 ]]; then
    # 「검사가 안 돌았다」는 note 를 로그로 흘려보낸다. 버리면 그 자리가 조용히 비고,
    # 「코드가 하나라서 CI 로그에서 셀 수 있다」는 지면의 주장이 거짓이 된다(E5).
    printf '%s\n' "$out" | grep -E '^ +note ' >&3 || true
  fi
  if [[ "$prc" -ne 0 ]]; then
    echo "사슬 검증기 rc=$prc"
    echo "$out" | sed 's/^/  /'
    rc=1
  fi
  return "$rc"
}

run_gate "docs/DESIGN.md 존재 + 200줄 이상" check1_design_doc
run_gate "README.md/LICENSE/NOTICE 존재 + 각 10줄 이상" check2_core_docs
run_gate "LICENSE 첫 줄 == 'MIT License'" check3_license_header
run_gate "NOTICE 가 5개 출처(jcuervo/jsnkle/imsungbin/bashebr/simonsez9510) 포함" check4_notice_sources
run_gate "레포 내 전체 *.sh 가 bash -n 통과" check5_shell_syntax
run_gate "README 「지금 상태」 절 표의 경로가 실재" check6_readme_paths
run_gate "templates/*.md 는 반드시 rc=1 (자리표시자 잔존)" check7_templates_are_red
run_gate "fixtures/green/* 는 rc=0 (정상 문서를 반려하지 않는다)" check8_fixtures_green
run_gate "fixtures/red/* 는 지정 code 로 rc=1" check9_fixtures_red
run_gate "python3 -m unittest discover -s tests" check10_unittest
run_gate "intent/*/ 사슬 전량 rc=0 (없으면 SKIP)" check11_intent_chain

# --- 확장 지점 -------------------------------------------------------------
# scripts/gates/*.sh 가 있으면 전부 source 한다. 각 파일은 위의 run_gate 를 그대로
# 불러 자기 검사를 등록한다(rc 0=PASS · 3=SKIP · 그 외 FAIL). 디렉터리가 없으면
# 조용히 넘어간다 — 형제 레인이 아직 안 들어왔다는 뜻이고, 그건 이 게이트의 결함이
# 아니다. 여기 걸린 검사도 아래 요약과 종료 코드에 그대로 합산된다.
if [[ -d scripts/gates ]]; then
  while IFS= read -r gate_file || [[ -n "$gate_file" ]]; do
    [[ -z "$gate_file" ]] && continue
    # shellcheck disable=SC1090
    . "$gate_file"
  done < <(find scripts/gates -maxdepth 1 -name '*.sh' | sort)
fi

if [[ -n "$ONLY_GATE" && "$ONLY_GATE_MATCHES" -eq 0 ]]; then
  echo ""
  echo "인자 '${ONLY_GATE}' 와 맞는 검사 함수가 없다 — 아무것도 재지 않았다." >&2
  echo "검사 하나만 돌리려면 run_gate 에 넘기는 **셸 함수 이름**을 준다(예: check11_intent_chain)." >&2
  exit 2
fi

echo ""
echo "${PASS_COUNT} passed, ${FAIL_COUNT} failed, ${SKIP_COUNT} skipped"

if [[ "$FAIL_COUNT" -gt 0 ]]; then
  exit 1
fi
exit 0
