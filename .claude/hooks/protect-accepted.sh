#!/usr/bin/env bash
# .claude/hooks/protect-accepted.sh — PreToolUse(Edit|Write|MultiEdit|NotebookEdit)
#
# 막는 것: `status: accepted` 인 아티팩트(intent/*/{intent,spec,plan}.md) 편집.
# 왜: 설계안 D5 — accepted 는 불변이다. 승인된 것을 조용히 고치면 사슬이 감사 추적을
#     못 한다. 바꾸려면 새 intent 를 만들고 `supersedes:` 로 옛것을 가리킨다.
#
# 판정 순서(중요): 「읽기 전용 허용목록」을 먼저 돌리지 않는다. 이 훅에는 허용목록이
# 아예 없다 — 대상이 아티팩트인지 먼저 판정하고, 아티팩트일 때만 디스크의 실제
# frontmatter 를 읽는다. 상태 판정은 코드 펜스를 걷어낸 뒤에 한다(펜스 안의
# `status: accepted` 는 위조다).
set -uo pipefail
. "${BASH_SOURCE[0]%/*}/_lib.sh"

hook_require_jq
hook_read_input

TARGET="$(hook_target_path)"
if [ -z "$TARGET" ]; then
  hook_die \
"[protect-accepted 차단] 도구 입력에서 대상 경로를 찾지 못했다(file_path · path · notebook_path 전부 없음).
  왜: 경로를 모르면 accepted 아티팩트인지 판정할 수 없다. 모르는 것은 통과가 아니다.
  승인 경로: 도구 입력에 대상 경로를 넣어 다시 시도하라."
fi

REL="$(hook_rel "$TARGET")" || exit 0   # 레포 밖 파일은 이 훅의 사정거리가 아니다

case "$REL" in
  intent/*/intent.md|intent/*/spec.md|intent/*/plan.md) ;;
  *) exit 0 ;;
esac

[ -f "$TARGET" ] || exit 0   # 아직 없는 파일(새 intent 생성)은 막지 않는다

# frontmatter 의 status 를 읽는다. 코드 펜스(``` / ~~~) 안쪽은 전부 버린다.
STATUS="$(awk '
  BEGIN { fence = 0; started = 0; fm = 0; st = "" }
  {
    l = $0
    if (l ~ /^[ \t]*(```|~~~)/) { fence = 1 - fence; next }
    if (fence) next
    if (!started) {
      if (l ~ /^[ \t]*$/) next
      if (l ~ /^---[ \t]*$/) { started = 1; fm = 1; next }
      exit
    }
    if (fm) {
      if (l ~ /^(---|\.\.\.)[ \t]*$/) { fm = 0; exit }
      if (l ~ /^status:[ \t]*/) {
        sub(/^status:[ \t]*/, "", l)
        sub(/[ \t]*(#.*)?$/, "", l)
        gsub(/^["'"'"']|["'"'"']$/, "", l)
        st = l
      }
    }
  }
  END { print st }
' "$TARGET")"

if [ "$STATUS" = "accepted" ]; then
  printf '%s\n' \
"[protect-accepted 차단] $REL 은 status: accepted 다 — accepted 아티팩트는 불변이다.
  왜: 승인된 intent/spec/plan 을 제자리에서 고치면 「무엇이 승인됐는가」의 기록이 사라진다.
      git 이 사슬의 감사 추적인데, 그 사슬의 마디를 덮어쓰는 셈이다(설계안 D5).
  승인 경로:
    1) 바꾸고 싶으면 새 intent 를 만들고 frontmatter 에 supersedes: $REL 을 적어라.
    2) 옛 파일의 status: 는 같은 PR 안에서 superseded 로 바꾼다.
    3) 상태 어휘와 전이·증거는 docs/STATUS.md 가 유일 정의처다.
    4) 오탈자 수정 등 정말 제자리 편집이 필요하면 product owner 승인을 PR 본문에 남기고
       이 훅을 그 PR 동안만 .claude/settings.json 에서 빼라 — 뺀 사실이 diff 에 남는다." >&2
  exit 2
fi

exit 0
