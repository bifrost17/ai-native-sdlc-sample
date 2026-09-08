#!/usr/bin/env bash
# .claude/hooks/protect-tests.sh — PreToolUse(Edit|Write|MultiEdit|NotebookEdit)
#
# 막는 것: 결함 수정 브랜치(`fix/…`)에서 tests/ 아래 파일을 고치는 것.
# 왜: 레슨 8 의 핵심 지시 — 결함은 「실패하는 시험을 먼저 커밋하고, 그 시험을 못 고치게
#     막은 상태에서 구현」해야 시험이 결함을 실제로 증언한다. 시험을 고칠 수 있으면
#     구현이 아니라 시험이 항복한다.
#
# 판정: 현재 브랜치(git rev-parse --abbrev-ref HEAD)가 fix/ 로 시작 AND 대상이 tests/ 아래.
# 대소문자는 브랜치·경로 양쪽에서 무시한다 — `FIX/…` 나 `TESTS/…` 로 넘어가지 못한다.
# git 브랜치를 못 읽으면 통과가 아니라 차단이다(fail-closed).
set -uo pipefail
. "${BASH_SOURCE[0]%/*}/_lib.sh"

hook_require_jq
hook_read_input

BRANCH="$(git -C "$HOOK_ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null)"
if [ -z "$BRANCH" ] || [ "$BRANCH" = "HEAD" ]; then
  hook_die \
"[protect-tests 차단] 현재 브랜치를 읽지 못했다(git -C $HOOK_ROOT rev-parse --abbrev-ref HEAD).
  왜: 브랜치를 모르면 「결함 수정 중인가」를 판정할 수 없다. 판정 불가는 통과가 아니다.
  승인 경로: 레포 안에서, detached HEAD 가 아닌 이름 있는 브랜치에서 작업하라
             (git switch -c fix/<NNNN>-<슬러그>). 상태·전이는 docs/STATUS.md 참조."
fi

BRANCH_LC="$(hook_lower "$BRANCH")"
case "$BRANCH_LC" in
  fix/*) ;;
  *) exit 0 ;;   # 결함 수정 브랜치가 아니면 사정거리 밖
esac

TARGET="$(hook_target_path)"
if [ -z "$TARGET" ]; then
  hook_die \
"[protect-tests 차단] 도구 입력에서 대상 경로를 찾지 못했다(file_path · path · notebook_path 전부 없음).
  왜: 결함 수정 브랜치에서는 대상이 시험 파일인지 확인돼야 편집을 허용할 수 있다.
  승인 경로: 도구 입력에 대상 경로를 넣어 다시 시도하라."
fi

REL="$(hook_rel "$TARGET")" || exit 0
REL_LC="$(hook_lower "$REL")"

case "$REL_LC" in
  tests/*)
    printf '%s\n' \
"[protect-tests 차단] 결함 수정 브랜치($BRANCH)에서 시험 파일을 고칠 수 없다: $REL
  왜: 레슨 8 — 결함은 「실패하는 시험 먼저 → 커밋 → 시험을 못 고치는 상태에서 구현」이라야
      그 시험이 결함을 증언한다. 시험을 고칠 수 있으면 구현 대신 시험이 항복하고,
      결함은 초록불 아래 남는다.
  승인 경로:
    1) 지금 필요한 것은 구현 변경이다 — src/ 를 고쳐 시험을 통과시켜라.
    2) 시험 자체가 틀렸다면 그것은 결함 수정이 아니라 별도 개선이다:
       새 intent 를 세우고 feat/<NNNN>-<슬러그> 브랜치에서 고쳐라.
    3) 재현 시험을 「추가」해야 한다면 결함 사슬의 첫 커밋(빨간 시험)에서 했어야 한다.
       놓쳤다면 그 커밋 앞으로 되돌리거나, product owner 승인을 PR 본문에 남기고
       브랜치를 feat/ 로 다시 세워라.
    4) 상태 어휘·전이·증거는 docs/STATUS.md 가 유일 정의처다." >&2
    exit 2
    ;;
esac

exit 0
