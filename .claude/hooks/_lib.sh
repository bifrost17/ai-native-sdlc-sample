#!/usr/bin/env bash
# .claude/hooks/_lib.sh — 훅 5종이 공유하는 최소 라이브러리.
#
# 이 파일은 훅이 아니다(파일명이 `_` 로 시작하면 tests/test_wiring.sh 가
# 라이브러리로 보고, settings.json 등록 대신 「등록된 훅이 실제로 source 하는가」를 잰다).
#
# 계약(code.claude.com/docs/en/hooks.md):
#   exit 2 = 차단이고 메시지는 stderr 로 간다. exit 0 의 평문 stdout 은
#   디버그 로그로만 가고 사용자·Claude 에게 보이지 않는다 — 그래서 「경고만 하는 훅」은
#   무효다. 차단은 언제나 exit 2 + stderr 다.
#
# fail-closed 원칙: 판정에 필요한 것(jq · 유효한 JSON · 대상 경로 · git 브랜치)이
# 하나라도 없으면 통과시키지 않고 차단한다. 레퍼런스 레포 7종이 전부 여기서 뚫렸다
# (jq 부재 → `|| exit 0` · 깨진 JSON → 빈 문자열 → 매칭 실패 → 통과).
#
# 호환: macOS 기본 bash 3.2 — mapfile/readarray/declare -A/${var,,} 를 쓰지 않는다.
# 외부 명령을 쓰기 전에 jq 검사가 먼저 돌아야 하므로, 이 파일이 source 되는 동안에는
# 셸 내장(cd · pwd · printf · command)만 쓴다.

# 훅 스크립트가 놓인 레포 루트. 환경변수를 믿지 않는다 — 훅 파일 자신의 위치에서 유도한다.
HOOK_ROOT="$(cd "${BASH_SOURCE[0]%/*}/../.." 2>/dev/null && pwd -P)"
HOOK_NAME="${0##*/}"
[ -n "$HOOK_NAME" ] || HOOK_NAME="hook"
HOOK_JSON=""

# ---------------------------------------------------------------- 차단 · 경고

hook_die() {
  # 판정 불가로 인한 fail-closed 차단. 정책 차단(각 훅의 exit 2)과 구분한다.
  printf '%s\n' "$*" >&2
  exit 2
}

hook_warn() {
  printf '%s\n' "$*" >&2
}

hook_require_jq() {
  command -v jq >/dev/null 2>&1 || hook_die \
"[$HOOK_NAME 차단] jq 없음 — 훅 입력을 파스할 수 없다. 안전을 위해 차단한다.
  왜: 파스할 수 없으면 「위반이 아니다」가 아니라 「모른다」다. 모르는 것을 통과시키면
      강제층이 조용히 꺼진다(레퍼런스 레포 7종 중 5종이 여기서 뚫렸다).
  승인 경로: jq 를 설치하고(brew install jq / apt-get install jq) 다시 시도하라."
}

hook_read_input() {
  # stdin 을 전부 읽는다. 유효한 JSON 은 줄을 이어 붙여도 유효하다.
  local __l
  HOOK_JSON=""
  while IFS= read -r __l || [ -n "$__l" ]; do
    HOOK_JSON="$HOOK_JSON$__l"
  done
  if [ -z "${HOOK_JSON//[[:space:]]/}" ]; then
    hook_die \
"[$HOOK_NAME 차단] 빈 입력 — 훅 stdin 이 비어 있다. 판정할 수 없으므로 차단한다.
  승인 경로: 훅을 손으로 시험하려면 PreToolUse 이벤트 JSON 을 stdin 으로 주어라.
             예) echo '{\"tool_name\":\"Edit\",\"tool_input\":{\"file_path\":\"...\"}}' | $HOOK_NAME"
  fi
  if ! printf '%s' "$HOOK_JSON" | jq -e . >/dev/null 2>&1; then
    hook_die \
"[$HOOK_NAME 차단] 훅 입력 JSON 을 파스하지 못했다. 판정할 수 없으므로 차단한다.
  승인 경로: 입력이 유효한 JSON 인지 확인하라(jq . 로 검사). 훅 자체 문제라면
             .claude/settings.json 에서 이 훅을 일시적으로 빼되, 그 사실을 PR 에 적어라."
  fi
}

hook_json() {
  printf '%s' "$HOOK_JSON" | jq -r "$1" 2>/dev/null
}

# ---------------------------------------------------------------- 경로 정규화

hook_norm_path() {
  # hook_norm_path <경로> <상대 기준 디렉터리>
  # `.` · `..` · `//` 를 접고, 존재하는 디렉터리 부분은 pwd -P 로 심볼릭 링크까지 푼다.
  # macOS 기본에는 `realpath -m`(없는 경로 정규화)이 없다 — 그래서 손으로 접는다.
  local p="$1" base="$2" abs seg out d b dp OLDIFS
  [ -n "$p" ] || return 1
  case "$p" in
    /*) abs="$p" ;;
    *)  abs="$base/$p" ;;
  esac
  OLDIFS="$IFS"
  set -f
  IFS='/'
  set -- $abs
  IFS="$OLDIFS"
  out=""
  for seg in "$@"; do
    case "$seg" in
      ""|".") ;;
      "..") out="${out%/*}" ;;
      *) out="$out/$seg" ;;
    esac
  done
  set +f
  [ -n "$out" ] || out="/"
  if [ -d "$out" ]; then
    dp="$(cd "$out" 2>/dev/null && pwd -P)"
    if [ -n "$dp" ]; then printf '%s\n' "$dp"; return 0; fi
  fi
  d="${out%/*}"
  b="${out##*/}"
  [ -n "$d" ] || d="/"
  if [ -d "$d" ]; then
    dp="$(cd "$d" 2>/dev/null && pwd -P)"
    if [ -n "$dp" ]; then
      case "$dp" in
        /) printf '/%s\n' "$b" ;;
        *) printf '%s/%s\n' "$dp" "$b" ;;
      esac
      return 0
    fi
  fi
  printf '%s\n' "$out"
}

hook_rel() {
  # hook_rel <절대경로> — 레포 루트 기준 상대경로. 레포 밖이면 rc=1.
  local abs="$1"
  case "$abs" in
    "$HOOK_ROOT")   printf '.\n'; return 0 ;;
    "$HOOK_ROOT"/*) printf '%s\n' "${abs#"$HOOK_ROOT"/}"; return 0 ;;
  esac
  return 1
}

hook_lower() {
  printf '%s' "$1" | tr '[:upper:]' '[:lower:]'
}

hook_target_path() {
  # 도구 입력에서 대상 경로를 읽는다 — file_path · path · notebook_path 를 전부 본다
  # (`.path` 만 보던 훅이 Write 를 놓쳤고, `.file_path` 만 보던 훅이 NotebookEdit 을 놓쳤다).
  local raw cwd
  raw="$(hook_json '.tool_input.file_path // .tool_input.path // .tool_input.notebook_path // empty')"
  [ -n "$raw" ] || return 1
  cwd="$(hook_json '.cwd // empty')"
  [ -n "$cwd" ] || cwd="$HOOK_ROOT"
  hook_norm_path "$raw" "$cwd"
}

# ---------------------------------------------------------------- 명령 토큰화

hook_tokens() {
  # hook_tokens <셸 명령> → `<세그먼트번호><TAB><토큰>` 줄을 찍는다.
  #
  # 왜 토큰화하는가: 부분 문자열로 판정하면 `tools.yaml` 안의 `ls` 나
  # `--dry-run=false` 안의 `ls` 에 걸려 허용목록이 뚫린다(bashebr 실측).
  # 따옴표 안의 내용은 한 토큰으로 묶는다 — `echo "git commit"` 은 git 호출이 아니다.
  # 세그먼트는 `;` `\n` `&&` `||` `|` `&` 로 나눈다 — 조합 명령의 뒤쪽도 봐야 한다.
  printf '%s' "$1" | awk '
    BEGIN { sq = sprintf("%c", 39); dq = sprintf("%c", 34); bs = sprintf("%c", 92); s = ""; seg = 0 }
    { s = s $0 "\n" }
    END {
      n = length(s); q = ""; tok = ""; had = 0
      for (i = 1; i <= n; i++) {
        c = substr(s, i, 1)
        if (q != "") {
          if (c == bs && q == dq) { i++; tok = tok substr(s, i, 1); had = 1; continue }
          if (c == q) { q = ""; continue }
          tok = tok c; had = 1; continue
        }
        if (c == bs) { i++; tok = tok substr(s, i, 1); had = 1; continue }
        if (c == sq || c == dq) { q = c; had = 1; continue }
        if (c == " " || c == "\t") { if (had) { print seg "\t" tok; tok = ""; had = 0 }; continue }
        if (c == "\n" || c == ";") { if (had) { print seg "\t" tok; tok = ""; had = 0 }; seg++; continue }
        if (c == "&" || c == "|") {
          if (had) { print seg "\t" tok; tok = ""; had = 0 }
          if (substr(s, i + 1, 1) == c) i++
          seg++
          continue
        }
        tok = tok c; had = 1
      }
      if (had) print seg "\t" tok
    }'
}

hook_token_core() {
  # `$(git` · `` `git `` · `(git` 같은 껍질을 벗겨 알맹이를 돌려준다.
  local t="$1"
  t="${t#\$(}"
  t="${t#\`}"
  t="${t#(}"
  t="${t%\`}"
  t="${t%)}"
  printf '%s' "$t"
}

hook_basename() {
  local t="$1"
  printf '%s' "${t##*/}"
}
