#!/usr/bin/env bash
# tests/test_wiring.sh — 훅이 Claude Code 에 실제로 「배선」됐는가.
#
# 왜 있는가: 참조 레포(bashebr)는 훅 스크립트를 만들어 놓고 settings.json 에
# 한 줄도 등록하지 않았다. 파일 존재는 강제가 아니다. 이 시험은 다음을 잰다.
#   ① .claude/settings.json 이 있고 유효한 JSON 인가
#   ② PreToolUse 에 훅 5종이 전부 등록됐는가
#   ③ 파일 편집 계열 matcher 가 Edit·Write·MultiEdit·NotebookEdit 을 전부 덮는가
#      (NotebookEdit 누락이 레퍼런스의 실제 구멍이었다)
#   ④ Bash 계열 matcher 가 Bash 를 덮는가
#   ⑤ 등록된 명령이 ${CLAUDE_PROJECT_DIR} 로 시작하고 큰따옴표로 감싸였는가
#      (공백 있는 경로에서 깨진 사례)
#   ⑥ 등록된 경로의 스크립트가 실재하고 실행 비트가 있는가
#   ⑦ 고아가 없는가 — .claude/hooks/*.sh 중 settings 에 없는 것
#      (`_` 로 시작하는 파일은 공용 라이브러리로 보고, 등록된 훅이 실제로
#       source 하는지를 대신 잰다)
#
# 무엇을 재지 않는가: 훅의 판정 로직(그건 tests/test_hooks.sh) · Claude Code 가
# 이 설정을 실제로 읽는지(사용자 설정을 건드리지 않는다는 제약 때문에 확인 못 함).
#
# 호환: macOS 기본 bash 3.2.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
SETTINGS="$ROOT/.claude/settings.json"
HOOKDIR="$ROOT/.claude/hooks"

PASS=0
FAIL=0

ok()   { PASS=$((PASS + 1)); echo "PASS  $1"; }
bad()  { FAIL=$((FAIL + 1)); echo "FAIL  $1"; }

# 기대 훅 목록 — 이름 · 어느 도구 계열에 붙어야 하는가
EDIT_HOOKS="protect-accepted.sh protect-tests.sh no-secrets.sh"
BASH_HOOKS="plan-sync.sh production-gate.sh"
EDIT_TOOLS="Edit Write MultiEdit NotebookEdit"

if ! command -v jq >/dev/null 2>&1; then
  echo "FAIL  jq 가 없어 배선을 판정할 수 없다 — 못 잰 것은 통과가 아니다"
  exit 1
fi

# --- ① 파일 존재 · JSON 유효성
if [ -f "$SETTINGS" ]; then
  ok "① .claude/settings.json 존재"
else
  bad "① .claude/settings.json 없음"
  echo ""
  echo "${PASS} passed, ${FAIL} failed"
  exit 1
fi

if jq -e . "$SETTINGS" >/dev/null 2>&1; then
  ok "① settings.json 이 유효한 JSON"
else
  bad "① settings.json 이 유효한 JSON 이 아님"
  echo ""
  echo "${PASS} passed, ${FAIL} failed"
  exit 1
fi

if [ "$(jq -r '.hooks.PreToolUse | type' "$SETTINGS" 2>/dev/null)" = "array" ]; then
  ok "① hooks.PreToolUse 가 배열"
else
  bad "① hooks.PreToolUse 배열이 없음"
  echo ""
  echo "${PASS} passed, ${FAIL} failed"
  exit 1
fi

# 등록 목록을 「matcher <TAB> type <TAB> command」 줄로 뽑는다.
ENTRIES="$(jq -r '.hooks.PreToolUse[] | .matcher as $m | (.hooks // [])[] | "\($m)\t\(.type)\t\(.command)"' "$SETTINGS")"

if [ -z "$ENTRIES" ]; then
  bad "② PreToolUse 에 등록된 훅이 하나도 없다"
  echo ""
  echo "${PASS} passed, ${FAIL} failed"
  exit 1
fi

# matcher_covers <matcher> <도구명> — matcher 를 | 로 쪼개 토큰이 정확히 일치하는가
matcher_covers() {
  local m="$1" want="$2" tok
  local OLDIFS="$IFS"
  set -f
  IFS='|'
  set -- $m
  IFS="$OLDIFS"
  for tok in "$@"; do
    # 앞뒤 공백과 정규식 앵커를 벗긴다
    tok="${tok#^}"
    tok="${tok%\$}"
    tok="${tok# }"
    tok="${tok% }"
    if [ "$tok" = "$want" ]; then
      set +f
      return 0
    fi
  done
  set +f
  return 1
}

# hook_line <훅파일명> — 그 훅이 등록된 줄(첫 줄)을 돌려준다
hook_line() {
  printf '%s\n' "$ENTRIES" | grep -F "/$1" | head -n 1
}

REGISTERED=""

check_hook() {
  # check_hook <훅파일명> <계열: edit|bash>
  local h="$1" kind="$2" line m t c tool
  line="$(hook_line "$h")"
  if [ -z "$line" ]; then
    bad "② $h 이 settings.json 에 등록되지 않음"
    return
  fi
  ok "② $h 등록됨"
  REGISTERED="$REGISTERED $h"

  m="$(printf '%s' "$line" | cut -f1)"
  t="$(printf '%s' "$line" | cut -f2)"
  c="$(printf '%s' "$line" | cut -f3)"

  if [ "$t" = "command" ]; then
    ok "② $h type == command"
  else
    bad "② $h type 이 '$t' — command 를 기대함"
  fi

  if [ "$kind" = "edit" ]; then
    for tool in $EDIT_TOOLS; do
      if matcher_covers "$m" "$tool"; then
        ok "③ $h matcher 가 $tool 을 덮음"
      else
        bad "③ $h matcher('$m') 가 $tool 을 덮지 않음"
      fi
    done
  else
    if matcher_covers "$m" "Bash"; then
      ok "④ $h matcher 가 Bash 를 덮음"
    else
      bad "④ $h matcher('$m') 가 Bash 를 덮지 않음"
    fi
  fi

  # ⑤ 큰따옴표 + ${CLAUDE_PROJECT_DIR}
  case "$c" in
    '"'*'"')
      ok "⑤ $h 명령이 큰따옴표로 감싸짐" ;;
    *)
      bad "⑤ $h 명령이 큰따옴표로 감싸이지 않음: $c" ;;
  esac
  case "$c" in
    *'${CLAUDE_PROJECT_DIR}'*)
      ok "⑤ $h 명령이 \${CLAUDE_PROJECT_DIR} 를 씀" ;;
    *)
      bad "⑤ $h 명령이 \${CLAUDE_PROJECT_DIR} 를 쓰지 않음: $c" ;;
  esac

  # ⑥ 실물 존재 + 실행 비트
  local rel resolved
  rel="$(printf '%s' "$c" | sed -e 's/^"//' -e 's/"$//' -e 's|^\${CLAUDE_PROJECT_DIR}/||')"
  resolved="$ROOT/$rel"
  if [ -f "$resolved" ]; then
    ok "⑥ $h 실물 존재: $rel"
  else
    bad "⑥ $h 실물 없음: $rel"
    return
  fi
  if [ -x "$resolved" ]; then
    ok "⑥ $h 실행 비트 있음"
  else
    bad "⑥ $h 실행 비트 없음: $rel"
  fi
}

for h in $EDIT_HOOKS; do check_hook "$h" edit; done
for h in $BASH_HOOKS; do check_hook "$h" bash; done

# --- ⑦ 고아 검사
if [ -d "$HOOKDIR" ]; then
  while IFS= read -r f || [ -n "$f" ]; do
    [ -z "$f" ] && continue
    b="$(basename "$f")"
    case "$b" in
      _*)
        # 공용 라이브러리 — 등록된 훅이 실제로 source 하는지로 대신 잰다
        if grep -l -F "$b" $(printf '%s\n' $EDIT_HOOKS $BASH_HOOKS | sed "s|^|$HOOKDIR/|") >/dev/null 2>&1; then
          ok "⑦ 라이브러리 $b 를 등록된 훅이 source 함"
        else
          bad "⑦ 라이브러리 $b 를 아무 훅도 쓰지 않음 — 고아"
        fi
        ;;
      *)
        case " $REGISTERED " in
          *" $b "*) ok "⑦ $b 고아 아님" ;;
          *) bad "⑦ $b 은 .claude/hooks 에 있는데 settings.json 에 없음 — 고아" ;;
        esac
        ;;
    esac
  done < <(find "$HOOKDIR" -maxdepth 1 -name '*.sh' | sort)
else
  bad "⑦ .claude/hooks 디렉터리가 없음"
fi

echo ""
echo "${PASS} passed, ${FAIL} failed"
if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
exit 0
