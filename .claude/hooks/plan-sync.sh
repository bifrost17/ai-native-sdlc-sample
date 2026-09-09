#!/usr/bin/env bash
# .claude/hooks/plan-sync.sh — PreToolUse(Bash)
#
# 막는 것: plan.md 의 `## Files that change` 목록 밖 소스를 커밋하는 것(레슨 4).
# 레슨 4 는 *"Consider using a hook"* 이라고만 말한다 — 이 파일이 그것을 실제로 만든 것이다.
#
# 판정:
#   1) 이 Bash 명령이 git commit 계열인가 — 토큰 단위로 본다.
#      `git  commit`(공백 2) · `git -C . commit` · `git ci`(별칭형) · `echo x && git commit`
#      전부 커밋으로 본다. 따옴표 안의 `"git commit"` 은 호출이 아니므로 아니다.
#   2) 현재 브랜치 이름의 마지막 구간이 `NNNN-` 로 시작하면 그 id 의 plan 을 찾는다.
#      브랜치가 그 형식이 아니면 사정거리 밖(통과).
#   3) id 는 있는데 intent/<id>/plan.md 가 없으면 차단(사슬이 끊긴 채로 커밋되는 것).
#   4) 스테이징된 파일(그리고 `-a` 면 추적 중인 미스테이징 변경까지) 중
#      intent/ 아래 아티팩트가 아닌 것이 plan 목록 밖이면 차단.
#      단 같은 커밋에 그 plan.md 가 들어 있으면 통과 — 레슨 4 의 「plan 을 같은 커밋에서 갱신하라」.
set -uo pipefail
. "${BASH_SOURCE[0]%/*}/_lib.sh"

hook_require_jq
hook_read_input

TOOL="$(hook_json '.tool_name // empty')"
[ "$TOOL" = "Bash" ] || exit 0

CMD="$(hook_json '.tool_input.command // empty')"
[ -n "$CMD" ] || exit 0

# --- 1) git commit 계열인가 ----------------------------------------------------
TOKENS="$(hook_tokens "$CMD")"

IS_COMMIT=0
COMMIT_ALL=0
cur_seg=""
state=leading        # leading(대입) → seek(git 찾기) → opts(전역옵션) → args(서브커맨드 뒤)
skip_next=0

seg_reset() { state=leading; skip_next=0; }

while IFS=$'\t' read -r sid tok || [ -n "${sid:-}" ]; do
  [ -z "${sid:-}" ] && continue
  if [ "$cur_seg" != "$sid" ]; then
    cur_seg="$sid"
    seg_reset
  fi
  core="$(hook_token_core "$tok")"

  if [ "$skip_next" -eq 1 ]; then
    skip_next=0
    continue
  fi

  case "$state" in
    leading)
      case "$tok" in
        [A-Za-z_]*=*) continue ;;
      esac
      state=seek
      ;;
  esac

  case "$state" in
    seek)
      case "$(hook_basename "$core")" in
        git) state=opts ;;
      esac
      continue
      ;;
    opts)
      case "$core" in
        -C|-c|--git-dir|--work-tree|--exec-path|--namespace|--super-prefix)
          skip_next=1; continue ;;
        --git-dir=*|--work-tree=*|--exec-path=*|--namespace=*|-C?*|-c?*)
          continue ;;
        -p|--paginate|--no-pager|--bare|--no-replace-objects|--literal-pathspecs)
          continue ;;
        commit|ci)
          IS_COMMIT=1; state=args; continue ;;
        -*)
          continue ;;
        *)
          state=args; continue ;;   # git 의 다른 서브커맨드 — 이 세그먼트는 끝
      esac
      ;;
    args)
      if [ "$IS_COMMIT" -eq 1 ]; then
        case "$core" in
          -a|--all|-am|-a[a-zA-Z]*|-[a-zA-Z]*a[a-zA-Z]*) COMMIT_ALL=1 ;;
        esac
      fi
      continue
      ;;
  esac
done <<EOF
$TOKENS
EOF

[ "$IS_COMMIT" -eq 1 ] || exit 0

# --- 2) 브랜치에서 사슬 id 를 뽑는다 -------------------------------------------
BRANCH="$(git -C "$HOOK_ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null)"
if [ -z "$BRANCH" ] || [ "$BRANCH" = "HEAD" ]; then
  hook_die \
"[plan-sync 차단] 현재 브랜치를 읽지 못했다(git -C $HOOK_ROOT rev-parse --abbrev-ref HEAD).
  왜: 브랜치를 모르면 어느 plan.md 와 대조해야 하는지 알 수 없다. 판정 불가는 통과가 아니다.
  승인 경로: 레포 안에서 이름 있는 브랜치(<유형>/<NNNN>-<슬러그>)로 작업하라."
fi

LAST_SEG="${BRANCH##*/}"
CHAIN_ID=""
case "$LAST_SEG" in
  [0-9][0-9][0-9][0-9]-*) CHAIN_ID="$LAST_SEG" ;;
esac
[ -n "$CHAIN_ID" ] || exit 0   # 사슬 브랜치가 아니면 사정거리 밖

PLAN="$HOOK_ROOT/intent/$CHAIN_ID/plan.md"
if [ ! -f "$PLAN" ]; then
  # 슬러그가 조금 다를 수 있다 — 같은 번호의 디렉터리를 찾아 본다(정확히 하나일 때만).
  NUM="${CHAIN_ID%%-*}"
  MATCHES="$(find "$HOOK_ROOT/intent" -maxdepth 2 -type f -name plan.md -path "*/$NUM-*/plan.md" 2>/dev/null)"
  COUNT="$(printf '%s' "$MATCHES" | grep -c . | tr -d ' ')"
  if [ "$COUNT" = "1" ]; then
    PLAN="$MATCHES"
  else
    hook_die \
"[plan-sync 차단] 브랜치 $BRANCH 의 사슬 id 는 $CHAIN_ID 인데 그 plan.md 를 찾지 못했다(${COUNT}개 후보).
  왜: 레슨 4 — 커밋은 plan 이 예고한 파일만 건드려야 한다. plan 이 없으면 대조할 기준이 없다.
      기준 없는 커밋을 통과시키면 사슬(intent → spec → plan → diff)이 끊긴다.
  승인 경로:
    1) intent/$CHAIN_ID/plan.md 를 만들고 '## Files that change' 절에 바꿀 파일을 적어라
       (templates/plan.md 참조).
    2) 이 브랜치가 사슬 작업이 아니라면 이름에서 NNNN- 를 빼라 — 그러면 이 훅의 사정거리 밖이다."
  fi
fi

# --- 3) plan 의 Files that change 목록 -----------------------------------------
PLAN_FILES="$(awk '
  BEGIN { inseg = 0 }
  /^##[ \t]+Files that change[ \t]*$/ { inseg = 1; next }
  /^##[ \t]+/ { if (inseg) exit }
  {
    if (!inseg) next
    l = $0
    if (l !~ /^[ \t]*([-*]|[0-9]+\.)[ \t]+/) next
    sub(/^[ \t]*([-*]|[0-9]+\.)[ \t]+/, "", l)
    gsub(/`/, "", l)
    # 첫 필드만 — 뒤에 붙은 설명(— …)은 버린다
    split(l, a, /[ \t]+/)
    p = a[1]
    sub(/^\.\//, "", p)
    if (p != "") print p
  }
' "$PLAN")"

PLAN_REL="$(hook_rel "$PLAN")"

# --- 4) 이 커밋이 건드리는 파일 -------------------------------------------------
STAGED="$(git -C "$HOOK_ROOT" diff --cached --name-only 2>/dev/null)"
if [ "$COMMIT_ALL" -eq 1 ]; then
  STAGED="$STAGED
$(git -C "$HOOK_ROOT" diff --name-only 2>/dev/null)"
fi

# plan.md 자신이 같은 커밋에 있으면 통과 — 레슨 4 의 「같은 커밋에서 plan 을 갱신하라」
case "
$STAGED
" in
  *"
$PLAN_REL
"*) exit 0 ;;
esac

OUTSIDE=""
while IFS= read -r f || [ -n "$f" ]; do
  [ -z "$f" ] && continue
  case "$f" in
    intent/*) continue ;;   # 사슬 아티팩트 자체는 plan 목록 대상이 아니다
  esac
  hit=0
  while IFS= read -r p || [ -n "$p" ]; do
    [ -z "$p" ] && continue
    case "$p" in
      */) [ "${f#$p}" != "$f" ] && hit=1 ;;
      *)  if [ "$f" = "$p" ] || [ "${f#$p/}" != "$f" ]; then hit=1; fi ;;
    esac
    [ "$hit" -eq 1 ] && break
  done <<EOF2
$PLAN_FILES
EOF2
  if [ "$hit" -eq 0 ]; then
    OUTSIDE="$OUTSIDE  · $f
"
  fi
done <<EOF3
$STAGED
EOF3

[ -n "$OUTSIDE" ] || exit 0

printf '%s\n' \
"[plan-sync 차단] 이 커밋이 $PLAN_REL 의 '## Files that change' 목록 밖 파일을 건드린다:
$OUTSIDE  브랜치: $BRANCH  (사슬 $CHAIN_ID)
  plan 이 예고한 파일:
$(printf '%s\n' "$PLAN_FILES" | sed 's/^/    /')
  왜: 레슨 4 — plan 은 「무엇이 바뀔지」의 약속이고, diff 가 그 약속을 넘으면 리뷰어가
      본 것과 머지되는 것이 달라진다. 사슬(intent → spec → plan → diff)의 마지막 고리가 끊긴다.
  승인 경로:
    1) 범위가 정말 늘었으면 $PLAN_REL 의 '## Files that change' 에 그 파일을 적고
       **같은 커밋에** plan.md 를 함께 스테이징하라 — 그러면 이 훅은 통과시킨다.
       (git add $PLAN_REL)
    2) 범위가 는 게 아니라면 그 파일을 커밋에서 빼라(git restore --staged <파일>).
    3) 아예 다른 일이면 별도 intent 를 세우고 그 브랜치에서 하라." >&2
exit 2
