#!/usr/bin/env bash
# .claude/hooks/production-gate.sh — PreToolUse(Bash)
#
# 막는 것: 승인 없이 `scripts/deploy.sh … production` 을 실행하는 것(레슨 11·12).
# 레슨 12 의 원칙 — *에이전트는 프로덕션 게이트까지 갈 수 있고 그 게이트를 넘지는 못한다.*
#
# 통과 조건: 환경변수 RELEASE_APPROVAL 이 비어 있지 않고 공백만도 아닐 것.
#   · 공백만("  ")은 승인이 아니다 — 「비었나」만 보던 훅이 여기서 뚫렸다.
#   · 명령 안의 인라인 대입(`RELEASE_APPROVAL=x scripts/deploy.sh production`)은
#     자기 승인이므로 통과가 아니라 차단이다. 승인은 게이트 밖에서 와야 한다.
#
# 판정 규칙: 부분 문자열이 아니라 토큰 단위다.
#   · `docs/production-notes.md` 는 production 토큰이 아니다.
#   · `--env=production` 은 값 부분이 production 이므로 토큰이다.
#   · `--dry-run=false` · `tools.yaml` 같은 무해한 인자에 걸리지 않는다.
#   · 허용목록을 차단 판정보다 먼저 돌리지 않는다 — 이 훅에는 허용목록이 없다.
set -uo pipefail
. "${BASH_SOURCE[0]%/*}/_lib.sh"

hook_require_jq
hook_read_input

TOOL="$(hook_json '.tool_name // empty')"
[ "$TOOL" = "Bash" ] || exit 0

CMD="$(hook_json '.tool_input.command // empty')"
[ -n "$CMD" ] || exit 0

TOKENS="$(hook_tokens "$CMD")"

# 세그먼트별로 「deploy.sh 호출」 · 「production 토큰」 · 「인라인 승인 대입」을 센다.
cur_seg=""
seg_has_deploy=0
seg_has_prod=0
seg_has_inline=0
seg_leading=1
VIOLATION=0
INLINE=0

flush_segment() {
  if [ "$seg_has_deploy" -eq 1 ] && [ "$seg_has_prod" -eq 1 ]; then
    VIOLATION=1
    [ "$seg_has_inline" -eq 1 ] && INLINE=1
  fi
  seg_has_deploy=0
  seg_has_prod=0
  seg_has_inline=0
  seg_leading=1
}

is_deploy_token() {
  local t
  t="$(hook_token_core "$1")"
  t="${t#./}"
  t="$(printf '%s' "$t" | sed 's|//*|/|g')"
  case "$t" in
    scripts/deploy.sh|*/scripts/deploy.sh) return 0 ;;
  esac
  return 1
}

is_production_token() {
  local t="$1" v
  [ "$t" = "production" ] && return 0
  case "$t" in
    *=*) v="${t#*=}"; [ "$v" = "production" ] && return 0 ;;
  esac
  return 1
}

while IFS=$'\t' read -r sid tok || [ -n "${sid:-}" ]; do
  [ -z "${sid:-}" ] && continue
  if [ "$cur_seg" != "$sid" ]; then
    [ -n "$cur_seg" ] && flush_segment
    cur_seg="$sid"
  fi
  # 세그먼트 머리의 VAR=value 대입 구간
  if [ "$seg_leading" -eq 1 ]; then
    case "$tok" in
      [A-Za-z_]*=*)
        case "${tok%%=*}" in
          RELEASE_APPROVAL) seg_has_inline=1 ;;
        esac
        continue
        ;;
      *) seg_leading=0 ;;
    esac
  fi
  if is_deploy_token "$tok"; then
    seg_has_deploy=1
    continue
  fi
  if is_production_token "$tok"; then
    seg_has_prod=1
  fi
done <<EOF
$TOKENS
EOF
[ -n "$cur_seg" ] && flush_segment

[ "$VIOLATION" -eq 1 ] || exit 0

APPROVAL="${RELEASE_APPROVAL-}"
APPROVAL_TRIMMED="${APPROVAL//[[:space:]]/}"

if [ "$INLINE" -eq 1 ]; then
  printf '%s\n' \
"[production-gate 차단] 프로덕션 배포 승인값을 명령 안에서 스스로 설정할 수 없다.
  본 명령: $CMD
  왜: RELEASE_APPROVAL 을 같은 명령줄에서 대입하면 게이트를 통과시키는 주체와 통과하는
      주체가 같아진다. 그건 승인이 아니라 자기 서명이다(레슨 11 — 게이트는 사람이 쥔다).
  승인 경로: 배포 승인권자가 세션 환경에 RELEASE_APPROVAL 을 넣어 준 뒤 실행하라.
             승인 근거(변경 승인 번호 · PR 링크)를 그 값으로 쓰고 PR 본문에도 남겨라." >&2
  exit 2
fi

if [ -n "$APPROVAL_TRIMMED" ]; then
  exit 0
fi

printf '%s\n' \
"[production-gate 차단] 승인 없이 프로덕션 배포를 실행할 수 없다.
  본 명령: $CMD
  왜: 레슨 12 — 에이전트는 프로덕션 게이트까지 갈 수 있고 그 게이트를 넘지는 못한다.
      프로덕션 배포는 되돌리기 비용이 가장 큰 비가역 행위라 사람의 승인이 앞에 있어야 한다.
  현재 상태: RELEASE_APPROVAL 이 ${RELEASE_APPROVAL+설정돼 있으나 공백뿐이다}${RELEASE_APPROVAL-설정돼 있지 않다}.
             (공백만인 값은 승인이 아니다 — 「비었나」만 보는 검사를 통과하려는 우회다.)
  승인 경로:
    1) 배포 승인권자가 환경변수 RELEASE_APPROVAL 에 승인 근거를 넣는다
       (예: 변경 승인 번호 CAB-2026-09-08 · 승인 PR 링크). 값은 공백만이면 안 된다.
    2) 그 값을 배포 PR 본문/커밋에 남겨 나중에 「누가 승인했는가」를 되짚을 수 있게 한다.
    3) 프로덕션이 아닌 환경(staging 등)은 승인 없이 배포할 수 있다.
    4) 조직 차원으로 굳히려면 org/managed-settings.example.json 을 보라 —
       단 allowManagedHooksOnly 를 켜면 이 프로젝트 훅이 차단되므로 관리형 파일에
       같은 게이트를 다시 정의해야 한다." >&2
exit 2
