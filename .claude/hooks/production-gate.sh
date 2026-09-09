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
#   · docs/production-notes.md 는 production 토큰이 아니다(반례로 든 가상 경로다 —
#     백틱을 치면 40-skills 게이트가 「실재하지 않는 레포 경로」로 읽는다).
#   · `--env=production` 은 값 부분이 production 이므로 토큰이다.
#   · `--dry-run=false` · `tools.yaml` 같은 무해한 인자에 걸리지 않는다.
#   · 허용목록을 차단 판정보다 먼저 돌리지 않는다 — 이 훅에는 그런 목록이 없다.
#     좁힘은 하나뿐이고 차단 판정 '안'에 있다: 세그먼트의 **명령어 자리** 토큰이 인자를
#     실행할 수 없는 순수 읽기 명령이면(`cat scripts/deploy.sh production`) 인자 자리의
#     배포 스크립트를 호출로 세지 않는다. 배포 스크립트가 명령어 자리에 있으면 이 집합과
#     무관하게 차단이다. 목록을 빠뜨리면 거짓 양성이 남을 뿐 우회는 생기지 않는다.
set -uo pipefail
. "${BASH_SOURCE[0]%/*}/_lib.sh"

hook_require_jq
hook_read_input

TOOL="$(hook_json '.tool_name // empty')"
[ "$TOOL" = "Bash" ] || exit 0

CMD="$(hook_json '.tool_input.command // empty')"
[ -n "$CMD" ] || exit 0

TOKENS="$(hook_tokens "$CMD")"

# ------------------------------------------------------- 배포 스크립트 신원 · 기준 디렉터리
# 판정을 「토큰 문자열이 scripts/deploy.sh 인가」에서 「토큰이 가리키는 파일이 이 레포의
# 배포 스크립트와 같은 파일인가」로 옮긴다. 어휘 소유자가 바뀐다 — 한 파일을 가리키는
# 경로를 쓰는 방법(`/./` · `//` · `..` · 심볼릭 링크 · 대소문자 비구분 FS)은 셸과
# 파일시스템이 늘리는 열린 집합이라 열거하는 판정은 다음 변종에 죽는다. device+inode
# 동일성은 커널이 쥔 닫힌 집합이고, `[ a -ef b ]` 는 stat(2) 이라 위 다섯을 전부 커널이
# 접어 준다(bash 3.2·5.3 양쪽 실측 — raw 06).
DEPLOY_REAL="$HOOK_ROOT/scripts/deploy.sh"
[ -f "$DEPLOY_REAL" ] || DEPLOY_REAL=""

CWD="$(hook_json '.cwd // empty')"
[ -n "$CWD" ] || CWD="$HOOK_ROOT"

# 후보 기준 디렉터리. 기존 기준(cwd · 레포 루트)을 지우지 않고 cd/pushd 목적지를 더하기만
# 한다 — 넓히기만 하므로 `cd X || 다른것` 처럼 cd 가 실패하는 갈래에서도 놓치지 않는다.
BASES_N=0
BASES_MAX=16
bases_add() {
  local nb="$1" i=0
  [ -n "$nb" ] || return 0
  [ "$BASES_N" -lt "$BASES_MAX" ] || return 0
  while [ "$i" -lt "$BASES_N" ]; do
    eval "[ \"\$BASE_$i\" = \"\$nb\" ]" && return 0
    i=$((i + 1))
  done
  eval "BASE_$BASES_N=\$nb"
  BASES_N=$((BASES_N + 1))
}
bases_add "$CWD"
bases_add "$HOOK_ROOT"

# cd/pushd 의 목적지를 셸 확장 없이 알 수 없으면(예: `cd $VAR`) 기준 집합이 불완전해진다.
UNRESOLVED_CD=0

collect_bases() {
  local sid tok prev_sid="" leading=1 want_dest=0 lit i n nb
  while IFS=$'\t' read -r sid tok || [ -n "${sid:-}" ]; do
    [ -z "${sid:-}" ] && continue
    if [ "$sid" != "$prev_sid" ]; then
      prev_sid="$sid"; leading=1; want_dest=0
    fi
    if [ "$want_dest" -ne 0 ]; then
      lit="$want_dest"    # 2 = `--` 뒤. `-` 로 시작해도 목적지다.
      want_dest=0
      if [ "$lit" -eq 1 ]; then
        case "$tok" in
          -)  # `cd -` 의 목적지는 OLDPWD 라 셸 실행 시각에만 안다 — `cd $VAR` 와 같은
              # 부류(해석 불가)이지 옵션이 아니다. 「모른다」는 통과가 아니다.
              UNRESOLVED_CD=1
              continue ;;
          --) want_dest=2                      # 옵션 끝. 다음 토큰이 목적지다.
              continue ;;
          -*) # `cd -P` · `cd -L` · `pushd -n` … 옵션이지 목적지가 아니다. 여기서 목적지
              # 찾기를 그만두면 바로 뒤의 목적지를 통째로 놓쳐 `cd -P scripts` 가
              # PG19 와 같은 자리로 가는데도 기준 디렉터리에 안 들어온다. 계속 찾는다
              # (넓히는 방향 — 옵션을 하나 더 만나면 또 넘긴다).
              want_dest=1
              continue ;;
        esac
      fi
      case "$tok" in
        *'$'*|*'`'*|*'*'*|*'?'*|'~'*)
          # 확장해야 알 수 있는 목적지 — 「모른다」이지 「없다」가 아니다.
          UNRESOLVED_CD=1
          continue ;;
      esac
      # 리터럴 목적지. 실재하지 않으면 cd 자체가 실패하므로 해석 불가가 아니다.
      i=0; n="$BASES_N"
      while [ "$i" -lt "$n" ]; do
        eval "nb=\$BASE_$i"
        i=$((i + 1))
        case "$tok" in
          /*) nb="$tok" ;;
          *)  nb="$nb/$tok" ;;
        esac
        [ -d "$nb" ] || continue
        bases_add "$(hook_norm_path "$nb" "$CWD")"
        case "$tok" in /*) break ;; esac
      done
      continue
    fi
    if [ "$leading" -eq 1 ]; then
      case "$tok" in
        [A-Za-z_]*=*) continue ;;
        *) leading=0 ;;
      esac
    else
      continue                                # 세그먼트의 첫 명령만 cd 로 본다
    fi
    case "$(hook_token_core "$tok")" in
      cd|pushd) want_dest=1 ;;
    esac
  done <<COLLECT_EOF
$TOKENS
COLLECT_EOF
}
collect_bases

# 세그먼트별로 「deploy.sh 호출」 · 「production 토큰」 · 「인라인 승인 대입」을 센다.
cur_seg=""
seg_has_deploy=0
seg_has_prod=0
seg_has_inline=0
seg_leading=1
seg_reader=0
VIOLATION=0
INLINE=0
ANY_PROD=0
UNRESOLVED_BLOCK=0

flush_segment() {
  if [ "$seg_has_deploy" -eq 1 ] && [ "$seg_has_prod" -eq 1 ]; then
    VIOLATION=1
    [ "$seg_has_inline" -eq 1 ] && INLINE=1
  fi
  seg_has_deploy=0
  seg_has_prod=0
  seg_has_inline=0
  seg_leading=1
  seg_reader=0
}

is_deploy_token() {
  local t lex i n cand
  t="$(hook_token_core "$1")"
  # (A) 어휘 판정 — 기존 검사를 그대로 둔다(지우지 않는다). 배포 스크립트가 아직 없는
  #     트리나 다른 레포를 가리키는 절대경로에서도 계속 잡는다.
  lex="${t#./}"
  lex="$(printf '%s' "$lex" | sed 's|//*|/|g')"
  case "$lex" in
    scripts/deploy.sh|*/scripts/deploy.sh) return 0 ;;
  esac
  # (A2) 대소문자 변형. 대소문자 비구분 FS 에서는 아래 (B) 가 잡지만, 구분 FS(리눅스)에서는
  #      같은 철자가 다른 파일이라 (B) 가 못 잡는다 — 실측으로 PG20 이 리눅스에서만 빨갰다
  #      (debian:bookworm-slim · 93 passed 1 failed · raw-rdC/23). protect-tests.sh 가
  #      TESTS/… · FIX/… 를 hook_lower 로 접는 것과 같은 처리를 여기서도 한다.
  case "$(hook_lower "$lex")" in
    scripts/deploy.sh|*/scripts/deploy.sh) return 0 ;;
  esac
  # (B) 신원 판정 — 커널 stat 이 `.` · `..` · `//` · 심볼릭 링크 · 대소문자 비구분 FS 를
  #     전부 접는다. 어휘 판정이 놓친 우회는 여기서 잡힌다.
  [ -n "$DEPLOY_REAL" ] || return 1
  [ -n "$t" ] || return 1
  case "$t" in
    /*) [ "$t" -ef "$DEPLOY_REAL" ] && return 0
        return 1 ;;
  esac
  i=0; n="$BASES_N"
  while [ "$i" -lt "$n" ]; do
    eval "cand=\$BASE_$i"
    i=$((i + 1))
    [ "$cand/$t" -ef "$DEPLOY_REAL" ] && return 0
  done
  return 1
}

# 인자를 실행할 수 없는 순수 읽기 명령. 인터프리터(bash · sh · env · sudo · xargs)와
# 자기 안에서 셸을 부를 수 있는 것(less · vi · awk · perl · GNU sed 의 `e`)은 넣지 않는다 —
# 그쪽을 잘못 넣으면 우회가 생긴다. 이쪽을 빠뜨리면 거짓 양성이 남을 뿐이다.
READ_ONLY_CMDS=" cat head tail nl wc file stat cmp diff od xxd grep egrep fgrep "

is_read_only_cmd() {
  local b
  b="$(hook_basename "$(hook_token_core "$1")")"
  case "$READ_ONLY_CMDS" in
    *" $b "*) return 0 ;;
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
  is_cmdword=0
  if [ "$seg_leading" -eq 1 ]; then
    case "$tok" in
      [A-Za-z_]*=*)
        case "${tok%%=*}" in
          RELEASE_APPROVAL) seg_has_inline=1 ;;
        esac
        continue
        ;;
      *) seg_leading=0
         is_cmdword=1
         seg_reader=0
         is_read_only_cmd "$tok" && seg_reader=1
         ;;
    esac
  fi
  if is_deploy_token "$tok"; then
    # 명령어 자리의 배포 스크립트는 언제나 호출이다. 인자 자리라면, 그 세그먼트의 명령어가
    # 인자를 실행할 수 없는 순수 읽기 명령일 때만 호출이 아니다 — `cat A B` 는 읽기다.
    if [ "$is_cmdword" -eq 1 ] || [ "$seg_reader" -eq 0 ]; then
      seg_has_deploy=1
    fi
    continue
  fi
  if is_production_token "$tok"; then
    seg_has_prod=1
    ANY_PROD=1
  fi
done <<EOF
$TOKENS
EOF
[ -n "$cur_seg" ] && flush_segment

# 기준 디렉터리 집합이 불완전한데(해석 불가한 cd) production 토큰이 있으면, 뒤따르는
# 상대경로 호출이 배포 스크립트에 닿는지 증명할 수 없다. 판정 불가는 통과가 아니다
# (_lib.sh 머리말의 fail-closed 원칙). 승인값이 있으면 통과한다는 계약은 그대로다.
if [ "$VIOLATION" -eq 0 ] && [ "$UNRESOLVED_CD" -eq 1 ] && [ "$ANY_PROD" -eq 1 ]; then
  VIOLATION=1
  UNRESOLVED_BLOCK=1
fi

[ "$VIOLATION" -eq 1 ] || exit 0

APPROVAL="${RELEASE_APPROVAL-}"
# 공백만인 값은 승인이 아니다. 판정은 「비공백이 하나라도 있는가」이고, 같은 뜻인
# ${APPROVAL//[[:space:]]/} 는 bash 3.2 에서 길이에 대해 폭발하므로 쓰지 않는다.
APPROVAL_HAS_CONTENT=0
case "$APPROVAL" in *[![:space:]]*) APPROVAL_HAS_CONTENT=1 ;; esac

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

if [ "$APPROVAL_HAS_CONTENT" -eq 1 ]; then
  exit 0
fi

UNRESOLVED_NOTE=""
if [ "$UNRESOLVED_BLOCK" -eq 1 ]; then
  UNRESOLVED_NOTE="
    * 이 명령은 cd/pushd 의 목적지를 셸 확장 없이 알 수 없다(예: cd \$VAR). 그래서 뒤따르는
      상대경로 호출이 배포 스크립트에 닿는지 훅이 증명할 수 없고, 「모른다」는 통과가 아니다.
      배포가 아니라면 cd 목적지를 리터럴 경로로 쓰거나 스크립트를 절대경로로 불러라 —
      그러면 훅이 실경로(device+inode)로 판정한다."
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
       (예: 변경 승인 번호 CAB-2026-09-08 · 승인 PR 링크). 값은 공백만이면 안 된다.$UNRESOLVED_NOTE
    2) 그 값을 배포 PR 본문/커밋에 남겨 나중에 「누가 승인했는가」를 되짚을 수 있게 한다.
    3) 프로덕션이 아닌 환경(staging 등)은 승인 없이 배포할 수 있다.
    4) 조직 차원으로 굳히려면 org/managed-settings.example.json 을 보라 —
       단 allowManagedHooksOnly 를 켜면 이 프로젝트 훅이 차단되므로 관리형 파일에
       같은 게이트를 다시 정의해야 한다." >&2
exit 2
