#!/usr/bin/env bash
# .claude/hooks/no-secrets.sh — PreToolUse(Edit|Write|MultiEdit|NotebookEdit)
#
# 막는 것: 자격증명이 diff 에 실려 커밋으로 들어가는 것(레슨 6b).
#   · AWS 액세스 키 ID    AKIA[0-9A-Z]{16}
#   · private key 헤더    -----BEGIN … PRIVATE KEY-----
#   · sk- 접두 API 토큰
#   · URL 매립 자격증명    scheme://user:pass@host
#   · password= / token= / secret= / api_key= 대입(환경변수·플레이스홀더 참조는 제외)
#
# 무엇을 보는가: tool_input 에서 「새로 쓰이는 내용」만 본다. old_string·old_source·
# 경로 키는 지운 뒤 남은 모든 문자열을 재귀로 훑는다 — 키 이름 목록은 Anthropic 이
# 늘리는 열린 어휘라서, 아는 키만 열거하면 다음 도구에서 뚫린다. 그래서 「아는 키를
# 열거」가 아니라 「아는 예외를 빼고 나머지 전부」로 닫는다.
#
# 면제: tests/fixtures/** — 검증기 픽스처는 일부러 나쁜 값을 담는다. 면제는 조용히
# 하지 않고 stderr 에 남긴다(면제가 구멍이 되는지 사람이 볼 수 있어야 한다).
set -uo pipefail
. "${BASH_SOURCE[0]%/*}/_lib.sh"

hook_require_jq
hook_read_input

# --- 새로 쓰이는 내용만 모은다 -------------------------------------------------
CONTENT="$(printf '%s' "$HOOK_JSON" | jq -r '
  def scrub: walk(if type == "object"
                  then del(.old_string, .old_source, .file_path, .path, .notebook_path)
                  else . end);
  (.tool_input // {}) | scrub | [.. | strings] | join("\n")
' 2>/dev/null)"
JQ_RC=$?
if [ "$JQ_RC" -ne 0 ]; then
  # walk 가 없는 jq 등 — 좁히지 말고 넓힌다(fail-closed): tool_input 전체를 훑는다.
  hook_warn "[no-secrets] 주의: 새 내용만 추리지 못했다(jq walk 실패) — tool_input 전체를 검사한다."
  CONTENT="$(printf '%s' "$HOOK_JSON" | jq -r '(.tool_input // {}) | [.. | strings] | join("\n")' 2>/dev/null)"
  if [ -z "$CONTENT" ]; then
    hook_die \
"[no-secrets 차단] 도구 입력에서 검사할 내용을 뽑지 못했다. 판정 불가는 통과가 아니다.
  승인 경로: jq 버전을 확인하라(jq --version · 1.6 이상 권장). 훅 자체 문제라면 PR 에 적어라."
  fi
fi

# --- 픽스처 면제 ---------------------------------------------------------------
TARGET="$(hook_target_path 2>/dev/null)"
if [ -n "$TARGET" ]; then
  REL="$(hook_rel "$TARGET" 2>/dev/null)" || REL=""
  case "$REL" in
    tests/fixtures/*)
      hook_warn "[no-secrets] 면제: $REL 은 tests/fixtures/ 아래라 자격증명 검사를 건너뛴다. 픽스처에 실제 유효한 키를 넣지 마라."
      exit 0
      ;;
  esac
fi

# --- 패턴 검사 -----------------------------------------------------------------
FINDINGS=""
add_finding() { FINDINGS="$FINDINGS  · $1
"; }

grep_has() { printf '%s' "$CONTENT" | grep -Eq -- "$1"; }

grep_has 'AKIA[0-9A-Z]{16}'                                             && add_finding "AWS 액세스 키 ID (AKIA…)"
grep_has '-----BEGIN [A-Z ]*PRIVATE KEY-----'                           && add_finding "private key 헤더 (-----BEGIN … PRIVATE KEY-----)"
grep_has 'sk-[A-Za-z0-9_-]{16,}'                                        && add_finding "sk- 접두 API 토큰"
grep_has '[A-Za-z][A-Za-z0-9+.-]*://[^/[:space:]:@]+:[^/[:space:]@]+@'  && add_finding "URL 에 매립된 자격증명 (scheme://user:pass@host)"

# 대입 형태 — 값이 환경변수·플레이스홀더 참조면 자격증명이 아니다.
is_reference() {
  local v="$1"
  case "$v" in
    ''|'""'|"''") return 0 ;;
    \$*|\{*|\<*|%*|\!*|\**|'‹'*) return 0 ;;
    os.environ*|process.env*|getenv*|System.getenv*|Deno.env*|ENV*|env\[*) return 0 ;;
    config.*|settings.*|self.*|this.*|secrets.*|vault.*) return 0 ;;
    None|null|nil|undefined|true|false) return 0 ;;
    TODO*|CHANGEME*|REDACTED*|xxx*|XXX*|placeholder*|example*) return 0 ;;
  esac
  [ "${#v}" -ge 6 ] || return 0
  return 1
}

ASSIGN_HITS="$(printf '%s' "$CONTENT" | grep -Eio '(password|passwd|pwd|secret|token|api[_-]?key)[[:space:]]*=[[:space:]]*[^[:space:],;)}]+' 2>/dev/null)"
if [ -n "$ASSIGN_HITS" ]; then
  while IFS= read -r hit || [ -n "$hit" ]; do
    [ -z "$hit" ] && continue
    val="${hit#*=}"
    # 앞뒤 공백·따옴표를 벗긴다
    while [ "${val# }" != "$val" ] || [ "${val#	}" != "$val" ]; do
      val="${val# }"; val="${val#	}"
    done
    val="${val%\"}"; val="${val#\"}"
    val="${val%\'}"; val="${val#\'}"
    if ! is_reference "$val"; then
      add_finding "자격증명 대입으로 보이는 값: ${hit%%=*}=… (참조가 아니라 리터럴)"
      break
    fi
  done <<EOF
$ASSIGN_HITS
EOF
fi

if [ -n "$FINDINGS" ]; then
  printf '%s\n' \
"[no-secrets 차단] 쓰려는 내용에 자격증명으로 보이는 값이 있다:
$FINDINGS  왜: 자격증명이 커밋에 한 번 들어가면 git 이력에서 지우는 비용이 재발급 비용보다 크다.
      diff 는 되돌릴 수 있어도 「그 값이 있었다」는 사실은 안 되돌아간다(레슨 6b).
  승인 경로:
    1) 값을 환경변수로 빼고 코드에는 참조만 남겨라 — 예) password=\${DB_PASSWORD} ·
       os.environ[\"DB_PASSWORD\"]. 이 훅은 환경변수·플레이스홀더 참조는 막지 않는다.
    2) 문서·템플릿의 예시값이면 플레이스홀더 ‹…› 나 명백한 가짜값(예: AWS 문서의
       AKIAIOSFODNN7EXAMPLE)을 써라.
    3) 검증기 픽스처가 정말 나쁜 값을 담아야 하면 tests/fixtures/ 아래에 두어라 —
       그 경로는 면제되고, 면제 사실이 stderr 에 남는다.
    4) 이미 실키가 유출됐다면 되돌리기 전에 먼저 폐기·재발급하라." >&2
  exit 2
fi

exit 0
