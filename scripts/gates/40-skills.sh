#!/usr/bin/env bash
# scripts/gates/40-skills.sh — 스킬 · 서브에이전트 · 슬래시 커맨드 게이트.
#
# 두 가지로 돈다:
#   - scripts/check_all.sh 가 source 하면 그쪽이 준 run_gate 를 쓴다.
#   - 직접 실행하면(`bash scripts/gates/40-skills.sh`) 자체 run_gate 로 돌고
#     PASS/FAIL 요약과 종료 코드를 낸다.
#
# 재는 것 넷:
#   ① tests/test_check_endpoints.sh — 결정론 백스톱의 계약
#   ② frontmatter 가 확인된 허용 필드 밖 키를 쓰지 않는가 (파일 종류별)
#   ③ 스킬 description 이 배타절을 포함하는가
#   ④ .claude 문서가 가리키는 레포 경로가 실재하는가
#
# ②의 어휘 소유자는 우리가 아니라 Anthropic 문서다 — 열린 어휘다. 그래서 목록에
# 출처와 확인 시각을 박아 두고, 검사 방향을 fail-closed 로 잡는다(모르는 키가
# 나오면 빨강). 새 필드를 쓰고 싶으면 문서를 다시 받아 목록을 갱신하는 것이 절차다.
# 목록을 늘리는 커밋은 그 자체가 「문서를 다시 읽었다」의 증거가 된다.
#
# 출처(2026-09-08 UTC 수신):
#   https://code.claude.com/docs/en/skills.md
#     - "Using skill frontmatter outside Claude Code" 표: claude.ai 업로드 ·
#       Skills API · package_skill.py 가 허용하는 필드는 여섯이다
#       (allowed-tools · compatibility · description · license · metadata · name).
#       그 밖의 키를 넣으면 무시가 아니라 하드 에러로 업로드가 막힌다.
#     - ".claude/commands/ 의 파일은 스킬과 같은 frontmatter 를 지원하되
#       name 과 paths 는 무시된다."
#   https://code.claude.com/docs/en/sub-agents.md
#     - "Supported frontmatter fields" 표. name·description 만 필수.
#   https://code.claude.com/docs/en/slash-commands.md 는 skills.md 와 같은 문서를
#     돌려준다(커스텀 커맨드가 스킬로 합쳐졌다).
#
# 스킬에는 여섯 필드 집합을 쓴다 — Claude Code 는 더 많은 필드를 받지만, 여섯
# 밖을 쓰는 순간 claude.ai 업로드 경로가 죽는다. 레퍼런스 레포 한 곳이 정확히
# 그 자리에서 막혔다. 좁은 쪽에 맞춰 두면 둘 다 산다.

GATE40_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GATE40_ROOT="$(cd "$GATE40_DIR/../.." && pwd)"

GATE40_STANDALONE=0
if ! declare -F run_gate >/dev/null 2>&1; then
  GATE40_STANDALONE=1
  set -uo pipefail
  GATE40_PASS=0
  GATE40_FAIL=0
  run_gate() {
    local name="$1"
    shift
    local out rc
    out="$("$@" 2>&1)"
    rc=$?
    if [ "$rc" -eq 0 ]; then
      echo "PASS  $name"
      GATE40_PASS=$((GATE40_PASS + 1))
    else
      echo "FAIL  $name"
      if [ -n "$out" ]; then
        echo "$out" | sed 's/^/      /'
      fi
      GATE40_FAIL=$((GATE40_FAIL + 1))
    fi
  }
fi

cd "$GATE40_ROOT" || echo "40-skills: 레포 루트 이동 실패 $GATE40_ROOT" >&2

# --- 허용 필드 집합 (위 출처 표를 그대로 옮긴 것) ---
GATE40_SKILL_FIELDS="allowed-tools compatibility description license metadata name"
GATE40_AGENT_FIELDS="name description tools disallowedTools model permissionMode maxTurns skills mcpServers hooks memory background effort isolation color initialPrompt experimental"
GATE40_COMMAND_FIELDS="description when_to_use argument-hint arguments disable-model-invocation user-invocable allowed-tools disallowed-tools model effort context agent background hooks shell metadata license compatibility"

# --- 참조 대기 목록 ---
# .claude 문서가 가리키지만 아직 이 브랜치에 없는 경로. 각 줄의 주인은 형제 레인이다.
# 영구 면제가 아니라 카운트다운이다: 경로가 실재하게 되면 ④가 STALE 로 빨개지고,
# 그때 이 줄을 지우는 것이 닫는 방법이다. 지우지 않으면 게이트가 계속 빨갛다.
#   templates/intent.md        · templates/spec.md      — 템플릿 레인
#   scripts/check_artifacts.py — 검증기 레인
#   src/claims_status/         — 0002 기능 구현 레인
GATE40_PENDING="templates/intent.md templates/spec.md scripts/check_artifacts.py src/claims_status/"

gate40_contains() {
  local word
  for word in $1; do
    if [ "$word" = "$2" ]; then
      return 0
    fi
  done
  return 1
}

# gate40_fm_keys <파일> — frontmatter 최상위 키를 한 줄에 하나씩.
# rc 3 = 첫 줄이 --- 가 아님(frontmatter 없음) · rc 4 = 닫는 --- 없음.
gate40_fm_keys() {
  awk '
    NR == 1 { if ($0 != "---") { bad = 1; exit } ; next }
    !closed && /^---[[:space:]]*$/ { closed = 1; next }
    !closed && /^[A-Za-z_][A-Za-z0-9_-]*:/ { key = $0; sub(/:.*/, "", key); print key }
    END { if (bad) exit 3; if (!closed) exit 4 }
  ' "$1"
}

# gate40_check_one <파일> <허용 필드> <필수 필드> — 위반을 출력하고 rc 로 알린다.
gate40_check_one() {
  local file="$1" allowed="$2" required="$3"
  local keys rc key
  keys="$(gate40_fm_keys "$file")"
  rc=$?
  if [ "$rc" -eq 3 ]; then
    echo "$file: frontmatter 가 없다 — 첫 줄이 --- 여야 한다"
    return 1
  fi
  if [ "$rc" -eq 4 ]; then
    echo "$file: frontmatter 를 닫는 --- 가 없다"
    return 1
  fi
  local bad=0
  for key in $keys; do
    if ! gate40_contains "$allowed" "$key"; then
      echo "$file: 확인된 허용 필드 밖의 키 '$key' — 허용: $allowed"
      bad=1
    fi
  done
  for key in $required; do
    if ! gate40_contains "$keys" "$key"; then
      echo "$file: 필수 필드 '$key' 가 없다"
      bad=1
    fi
  done
  return "$bad"
}

# --- ① 백스톱 계약 ---
gate40_endpoint_tests() {
  bash tests/test_check_endpoints.sh
}

# --- ② frontmatter 허용 필드 ---
gate40_frontmatter_fields() {
  local rc=0 file seen=0
  for file in .claude/skills/*/SKILL.md; do
    [ -e "$file" ] || continue
    seen=$((seen + 1))
    gate40_check_one "$file" "$GATE40_SKILL_FIELDS" "name description" || rc=1
  done
  for file in .claude/agents/*.md; do
    [ -e "$file" ] || continue
    seen=$((seen + 1))
    gate40_check_one "$file" "$GATE40_AGENT_FIELDS" "name description" || rc=1
  done
  for file in .claude/commands/*.md; do
    [ -e "$file" ] || continue
    seen=$((seen + 1))
    gate40_check_one "$file" "$GATE40_COMMAND_FIELDS" "description" || rc=1
  done
  if [ "$seen" -eq 0 ]; then
    echo "검사 대상 파일이 0개 — 계기 고장이다(부재는 「위반 없음」이 아니다)"
    return 1
  fi
  echo "frontmatter 검사 $seen 파일"
  return "$rc"
}

# --- ③ 스킬 description 의 배타절 ---
# 배타절이 없는 description 은 모델이 스킬을 「무엇에도 쓸 수 있는 것」으로 읽는다.
# 이 스킬이 하지 않는 일을 description 이 말해야 라우팅이 좁아진다.
gate40_skill_exclusion() {
  local rc=0 file desc seen=0
  for file in .claude/skills/*/SKILL.md; do
    [ -e "$file" ] || continue
    seen=$((seen + 1))
    desc="$(grep -m 1 '^description:' "$file")"
    if [ -z "$desc" ]; then
      echo "$file: description 줄이 없다"
      rc=1
      continue
    fi
    if printf '%s\n' "$desc" | grep -q '쓰지 않는다'; then
      continue
    fi
    if printf '%s\n' "$desc" | grep -q 'Does not'; then
      continue
    fi
    echo "$file: description 에 배타절이 없다 — 이 스킬이 하지 않는 일을 '쓰지 않는다' 또는 'Does not' 로 적어라"
    rc=1
  done
  if [ "$seen" -eq 0 ]; then
    echo "스킬이 0개 — 계기 고장이다"
    return 1
  fi
  echo "배타절 검사 $seen 스킬"
  return "$rc"
}

# --- ④ 문서가 가리키는 경로가 실재하는가 ---
# 레퍼런스 레포 한 곳이 존재하지 않는 스킬로 라우팅했다. 가리키는 곳이 없는
# 문서는 틀린 문서가 아니라 작동하지 않는 문서다.
# 백틱 안의 레포 상대 경로만 본다. 꺾쇠 플레이스홀더(intent/<NNNN>-.../)는
# 경로가 아니라 서식이므로 대상이 아니다.
gate40_referenced_paths() {
  local rc=0 refs path seen=0
  refs="$(grep -rhoE '`(scripts|templates|src|tests|ops|docs|evals|intent)/[A-Za-z0-9._/-]+`' .claude 2>/dev/null | tr -d '`' | sort -u)"
  for path in $refs; do
    seen=$((seen + 1))
    if [ -e "$path" ]; then
      continue
    fi
    if gate40_contains "$GATE40_PENDING" "$path"; then
      continue
    fi
    echo "$path — .claude 문서가 가리키는데 실재하지 않는다"
    rc=1
  done
  for path in $GATE40_PENDING; do
    if [ -e "$path" ]; then
      echo "STALE $path — 이제 실재한다. 40-skills.sh 의 GATE40_PENDING 에서 이 항목을 지워라"
      rc=1
    fi
  done
  if [ "$seen" -eq 0 ]; then
    echo ".claude 에서 참조 경로를 하나도 못 찾았다 — 계기 고장이다"
    return 1
  fi
  echo "참조 경로 $seen 건"
  return "$rc"
}

# 대기 항목은 run_gate 가 삼키지 않도록 바깥에서 한 줄로 알린다.
if [ -n "$GATE40_PENDING" ]; then
  gate40_pending_open=""
  for gate40_p in $GATE40_PENDING; do
    if [ ! -e "$gate40_p" ]; then
      gate40_pending_open="$gate40_pending_open $gate40_p"
    fi
  done
  if [ -n "$gate40_pending_open" ]; then
    echo "NOTE  40-skills 참조 대기(형제 레인 미착지):$gate40_pending_open"
  fi
fi

run_gate "결정론 백스톱 계약 (tests/test_check_endpoints.sh)" gate40_endpoint_tests
run_gate "스킬·에이전트·커맨드 frontmatter 가 확인된 허용 필드 안" gate40_frontmatter_fields
run_gate "스킬 description 에 배타절이 있다" gate40_skill_exclusion
run_gate ".claude 문서가 가리키는 레포 경로가 실재" gate40_referenced_paths

if [ "$GATE40_STANDALONE" -eq 1 ]; then
  echo ""
  echo "${GATE40_PASS} passed, ${GATE40_FAIL} failed"
  if [ "$GATE40_FAIL" -gt 0 ]; then
    exit 1
  fi
  exit 0
fi
