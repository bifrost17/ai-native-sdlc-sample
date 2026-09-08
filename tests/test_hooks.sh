#!/usr/bin/env bash
# tests/test_hooks.sh — 훅 5종의 차단/통과/우회 시험.
#
# 무엇을 재는가
#   ① 양성 대조 — 막아야 하는 입력에서 exit 2 가 나고, stderr 에 「사유 + 승인 경로」가 있는가
#      (레슨 11 "A block should explain itself" 를 문자열로 단정한다)
#   ② 음성 대조 — 막으면 안 되는 입력에서 exit 0 인가
#   ③ 우회 세트 — 참조 레포 7종에서 실제로 뚫린 벡터가 여기서도 뚫리는가
#      (./ · ../ · // 경로 · .path/.notebook_path 키 · 대소문자 · `git  commit`(공백2) ·
#       `git -C .` · `git ci` · 명령 조합 · 부분 문자열 함정 · 공백만인 승인값 ·
#       jq 부재 · 깨진 JSON · 빈 stdin)
#
# 무엇을 재지 않는가
#   훅이 Claude Code 에 실제로 배선됐는지는 tests/test_wiring.sh 가 잰다.
#   여기서는 스크립트를 stdin JSON 으로 직접 호출한다(사용자 설정을 건드리지 않는다).
#
# 호환: macOS 기본 bash 3.2 — mapfile/readarray/declare -A/${var,,} 를 쓰지 않는다.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
HOOKS_SRC="$ROOT/.claude/hooks"

PASS=0
FAIL=0
FAILED_LIST=""

TMPBASE="$(mktemp -d "${TMPDIR:-/tmp}/owa-hooktest.XXXXXX")"
# VERIFY 「뮤테이션 스윕의 복원은 trap 에 건다」 — 중단돼도 임시 트리를 남기지 않는다.
trap 'rm -rf "$TMPBASE"' EXIT INT TERM

# ---------------------------------------------------------------- 픽스처 레포

mk_repo() {
  # $1 = 레포 디렉터리명. git 레포 + 아티팩트/소스/시험 픽스처를 만든다.
  local r="$TMPBASE/$1"
  mkdir -p "$r/.claude/hooks"
  if [ -d "$HOOKS_SRC" ]; then
    cp "$HOOKS_SRC"/*.sh "$r/.claude/hooks/" 2>/dev/null || true
    chmod +x "$r/.claude/hooks"/*.sh 2>/dev/null || true
  fi

  mkdir -p "$r/intent/0002-claims-status" "$r/intent/0004-fenced-forgery" \
           "$r/src/claims_status" "$r/tests/fixtures/red" "$r/scripts" "$r/docs"

  cat > "$r/intent/0002-claims-status/intent.md" <<'EOF'
---
id: 0002-claims-status
kind: intent
status: accepted
author: 홍길동 (청구운영팀)
---
# Intent: 청구 상태 자가조회
EOF

  cat > "$r/intent/0002-claims-status/spec.md" <<'EOF'
---
id: 0002-claims-status
kind: spec
status: draft
---
# Spec: 청구 상태 자가조회
EOF

  cat > "$r/intent/0002-claims-status/plan.md" <<'EOF'
---
id: 0002-claims-status
kind: plan
status: draft
---
# Plan: 청구 상태 자가조회

## Files that change
- `src/claims_status/service.py` — 허용 필드 4 · 60초 캐시
- `docs/STATUS.md`

## Order of work
1. 시험
2. 구현
EOF

  # 아티팩트 3종(intent/spec/plan) 이 아닌 파일 — accepted 여도 protect-accepted 대상이 아니다.
  cat > "$r/intent/0002-claims-status/notes.md" <<'EOF'
---
status: accepted
---
메모
EOF

  # 코드 펜스 안의 `status: accepted` 는 위조다 — frontmatter 는 draft.
  cat > "$r/intent/0004-fenced-forgery/intent.md" <<'EOF'
---
id: 0004-fenced-forgery
kind: intent
status: draft
---
# Intent: 펜스 위조

아래는 예시일 뿐이다.

```yaml
status: accepted
```
EOF

  echo "def get(): return {}" > "$r/src/claims_status/service.py"
  echo "def other(): return 1" > "$r/src/other.py"
  echo "def test_ac1(): assert True" > "$r/tests/test_claims_status.py"
  echo "누출 픽스처 자리" > "$r/tests/fixtures/red/leak.md"
  echo "상태 어휘 정의" > "$r/docs/STATUS.md"
  printf '#!/usr/bin/env bash\necho "deploy $*"\n' > "$r/scripts/deploy.sh"
  chmod +x "$r/scripts/deploy.sh"
  # 배포 스크립트를 가리키는 파일 심링크 — 「토큰을 문자열로만 보는」 판정이 뚫리는 자리(PG18).
  ln -s scripts/deploy.sh "$r/dep.sh"

  git -C "$r" init -q
  git -C "$r" config user.email "test@example.invalid"
  git -C "$r" config user.name "hook test"
  git -C "$r" add -A >/dev/null 2>&1
  git -C "$r" commit -q -m "fixture" >/dev/null 2>&1
  git -C "$r" checkout -q -B main >/dev/null 2>&1
  printf '%s' "$r"
}

# ---------------------------------------------------------------- 실행 · 단정

RC=0
ERR=""
OUT=""
HOOK_ENV=""

run_hook() {
  # run_hook <레포> <훅파일명> <stdin JSON>
  # 추가 환경변수는 호출 전에 HOOK_ENV 배열에 담는다(빈 배열 허용 · bash 3.2 안전).
  local repo="$1" hook="$2" json="$3"
  local ef="$TMPBASE/stderr.txt" of="$TMPBASE/stdout.txt"
  : > "$ef"; : > "$of"
  printf '%s' "$json" | env ${ENVARR[@]+"${ENVARR[@]}"} "$repo/.claude/hooks/$hook" >"$of" 2>"$ef"
  RC=$?
  ERR="$(cat "$ef")"
  OUT="$(cat "$of")"
  ENVARR=()
}

ENVARR=()

expect() {
  # expect <케이스 이름> <기대 rc> [stderr 에 있어야 하는 문자열 ...]
  local name="$1" want="$2"
  shift 2
  local ok=1 why="" s
  if [ "$RC" != "$want" ]; then
    ok=0
    why="rc=$RC (기대 $want)"
  fi
  for s in "$@"; do
    case "$ERR" in
      *"$s"*) ;;
      *) ok=0; why="$why; stderr 에 '$s' 없음" ;;
    esac
  done
  if [ "$ok" -eq 1 ]; then
    PASS=$((PASS + 1))
    echo "PASS  $name"
  else
    FAIL=$((FAIL + 1))
    FAILED_LIST="$FAILED_LIST
  - $name — $why"
    echo "FAIL  $name — $why"
    if [ -n "$ERR" ]; then
      echo "$ERR" | sed 's/^/        stderr| /'
    fi
  fi
}

json_edit() {
  # json_edit <도구> <경로키> <경로> [cwd]
  local tool="$1" key="$2" path="$3" cwd="${4:-}"
  printf '{"hook_event_name":"PreToolUse","cwd":"%s","tool_name":"%s","tool_input":{"%s":"%s","new_string":"x"}}' \
    "$cwd" "$tool" "$key" "$path"
}

json_bash() {
  # json_bash <명령> [cwd]
  local cmd="$1" cwd="${2:-}"
  printf '%s' "$cmd" | jq -Rs --arg cwd "$cwd" \
    '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"Bash",tool_input:{command:.}}'
}

# jq 없는 PATH: bash 만 있는 shim 디렉터리
SHIMBIN="$TMPBASE/shimbin"
mkdir -p "$SHIMBIN"
ln -sf "$(command -v bash)" "$SHIMBIN/bash"

REPO="$(mk_repo repo)"
NOGIT="$TMPBASE/nogit"
mkdir -p "$NOGIT/.claude/hooks" "$NOGIT/tests"
if [ -d "$HOOKS_SRC" ]; then
  cp "$HOOKS_SRC"/*.sh "$NOGIT/.claude/hooks/" 2>/dev/null || true
  chmod +x "$NOGIT/.claude/hooks"/*.sh 2>/dev/null || true
fi
echo "x" > "$NOGIT/tests/t.py"

echo "== 픽스처 레포: $REPO"
echo ""
# ================================================================ 1. protect-accepted
echo "-- protect-accepted (accepted 아티팩트 불변) --"
H=protect-accepted.sh
A_MSG_1="accepted"
A_MSG_2="supersedes:"
A_MSG_3="docs/STATUS.md"

run_hook "$REPO" "$H" "$(json_edit Edit file_path "$REPO/intent/0002-claims-status/intent.md" "$REPO")"
expect "PA01 양성: accepted intent.md 편집 차단" 2 "$A_MSG_1" "$A_MSG_2" "$A_MSG_3"

run_hook "$REPO" "$H" "$(json_edit Edit file_path "$REPO/intent/0002-claims-status/spec.md" "$REPO")"
expect "PA02 음성: draft spec.md 편집 허용" 0

run_hook "$REPO" "$H" "$(json_edit Edit file_path "./intent/0002-claims-status/intent.md" "$REPO")"
expect "PA03 우회 ./ : 상대경로로도 차단" 2 "$A_MSG_1"

run_hook "$REPO" "$H" "$(json_edit Edit file_path "$REPO/tests/../intent/0002-claims-status/intent.md" "$REPO")"
expect "PA04 우회 ../ : 되짚는 경로로도 차단" 2 "$A_MSG_1"

run_hook "$REPO" "$H" "$(json_edit Edit file_path "$REPO//intent//0002-claims-status//intent.md" "$REPO")"
expect "PA05 우회 // : 이중 슬래시로도 차단" 2 "$A_MSG_1"

run_hook "$REPO" "$H" "$(json_edit Write path "$REPO/intent/0002-claims-status/intent.md" "$REPO")"
expect "PA06 우회 .path 키: 다른 키 이름으로도 차단" 2 "$A_MSG_1"

run_hook "$REPO" "$H" "$(json_edit NotebookEdit notebook_path "$REPO/intent/0002-claims-status/intent.md" "$REPO")"
expect "PA07 우회 .notebook_path 키: 노트북 도구로도 차단" 2 "$A_MSG_1"

run_hook "$REPO" "$H" "$(json_edit Edit file_path "$REPO/intent/0004-fenced-forgery/intent.md" "$REPO")"
expect "PA08 음성: 코드 펜스 안의 status: accepted 는 위조 — 허용" 0

run_hook "$REPO" "$H" "$(json_edit Edit file_path "$REPO/src/other.py" "$REPO")"
expect "PA09 음성: 아티팩트가 아닌 소스 편집 허용" 0

run_hook "$REPO" "$H" "$(json_edit Write file_path "$REPO/intent/0005-new-one/intent.md" "$REPO")"
expect "PA10 음성: 아직 없는 파일(새 intent) 생성 허용" 0

run_hook "$REPO" "$H" "$(json_edit Edit file_path "$REPO/intent/0002-claims-status/notes.md" "$REPO")"
expect "PA11 음성: intent/spec/plan 이 아닌 파일명은 대상 아님" 0

ENVARR=(PATH="$SHIMBIN")
run_hook "$REPO" "$H" "$(json_edit Edit file_path "$REPO/src/other.py" "$REPO")"
expect "PA12 fail-closed: jq 없는 PATH 에서 차단" 2 "jq"

run_hook "$REPO" "$H" '{not json'
expect "PA13 fail-closed: 깨진 JSON 차단" 2 "JSON"

run_hook "$REPO" "$H" ''
expect "PA14 fail-closed: 빈 stdin 차단" 2 "입력"

run_hook "$REPO" "$H" '{"hook_event_name":"PreToolUse","tool_name":"Edit","tool_input":{"new_string":"x"}}'
expect "PA15 fail-closed: 경로 키가 하나도 없으면 차단" 2 "경로"

echo ""

# ================================================================ 2. protect-tests
echo "-- protect-tests (결함 수정 중 시험 파일 편집 금지) --"
H=protect-tests.sh
T_MSG_1="결함 수정"
T_MSG_2="승인"
T_MSG_3="docs/STATUS.md"

git -C "$REPO" checkout -q -B fix/0003-status-cache-defect
run_hook "$REPO" "$H" "$(json_edit Edit file_path "$REPO/tests/test_claims_status.py" "$REPO")"
expect "PT01 양성: fix/ 브랜치에서 tests/ 편집 차단" 2 "$T_MSG_1" "$T_MSG_2" "$T_MSG_3"

run_hook "$REPO" "$H" "$(json_edit Edit file_path "$REPO/src/claims_status/service.py" "$REPO")"
expect "PT02 음성: fix/ 브랜치에서 소스 편집 허용" 0

run_hook "$REPO" "$H" "$(json_edit Edit file_path "$REPO/src/../tests/test_claims_status.py" "$REPO")"
expect "PT03 우회 ../ : 되짚는 경로로도 차단" 2 "$T_MSG_1"

run_hook "$REPO" "$H" "$(json_edit Edit file_path "TESTS/test_claims_status.py" "$REPO")"
expect "PT04 우회 대소문자 경로: TESTS/ 로도 차단" 2 "$T_MSG_1"

run_hook "$REPO" "$H" "$(json_edit NotebookEdit notebook_path "$REPO/tests/nb.ipynb" "$REPO")"
expect "PT05 우회 .notebook_path 키: 노트북으로도 차단" 2 "$T_MSG_1"

git -C "$REPO" checkout -q -B FIX/0003-status-cache-defect
run_hook "$REPO" "$H" "$(json_edit Edit file_path "$REPO/tests/test_claims_status.py" "$REPO")"
expect "PT06 우회 대소문자 브랜치: FIX/ 로도 차단" 2 "$T_MSG_1"

git -C "$REPO" checkout -q -B feat/0002-claims-status
run_hook "$REPO" "$H" "$(json_edit Edit file_path "$REPO/tests/test_claims_status.py" "$REPO")"
expect "PT07 음성: feat/ 브랜치에서는 시험 편집 허용" 0

ENVARR=(PATH="$SHIMBIN")
run_hook "$REPO" "$H" "$(json_edit Edit file_path "$REPO/tests/test_claims_status.py" "$REPO")"
expect "PT08 fail-closed: jq 없는 PATH 에서 차단" 2 "jq"

run_hook "$NOGIT" "$H" "$(json_edit Edit file_path "$NOGIT/tests/t.py" "$NOGIT")"
expect "PT09 fail-closed: git 레포가 아니면 브랜치를 못 재므로 차단" 2 "브랜치"

run_hook "$REPO" "$H" '{"broken'
expect "PT10 fail-closed: 깨진 JSON 차단" 2 "JSON"

run_hook "$REPO" "$H" ''
expect "PT11 fail-closed: 빈 stdin 차단" 2 "입력"

echo ""
# ================================================================ 3. no-secrets
echo "-- no-secrets (자격증명이 diff 에 드는 것 차단) --"
H=no-secrets.sh
S_MSG_1="자격증명"
S_MSG_2="환경변수"

# 아래 리터럴은 전부 공개 예시값이다(AWS 문서의 AKIAIOSFODNN7EXAMPLE 등) — 실키가 아니다.
AWSKEY="AKIAIOSFODNN7EXAMPLE"
PEMHDR="-----BEGIN RSA PRIVATE KEY-----"
SKTOK="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"

json_write() {
  # json_write <경로> <내용>
  jq -n --arg p "$1" --arg c "$2" --arg cwd "$REPO" \
    '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"Write",tool_input:{file_path:$p,content:$c}}'
}

run_hook "$REPO" "$H" "$(json_write "$REPO/src/other.py" "AWS_KEY = \"$AWSKEY\"")"
expect "NS01 양성: AWS 액세스 키 차단" 2 "$S_MSG_1" "$S_MSG_2"

run_hook "$REPO" "$H" "$(json_write "$REPO/src/other.py" "$PEMHDR
MIIEow==")"
expect "NS02 양성: private key 헤더 차단" 2 "$S_MSG_1"

run_hook "$REPO" "$H" "$(json_write "$REPO/src/other.py" "client = X(\"$SKTOK\")")"
expect "NS03 양성: sk- 접두 토큰 차단" 2 "$S_MSG_1"

run_hook "$REPO" "$H" "$(json_write "$REPO/src/other.py" 'URL = "https://svc:hunter2@internal.example.com/api"')"
expect "NS04 양성: URL 매립 자격증명 차단" 2 "$S_MSG_1"

run_hook "$REPO" "$H" "$(json_write "$REPO/src/other.py" 'password=hunter2000')"
expect "NS05 양성: password= 대입 차단" 2 "$S_MSG_1"

run_hook "$REPO" "$H" "$(json_write "$REPO/src/other.py" 'token = "abcdef1234567890"')"
expect "NS06 양성: token= 대입 차단" 2 "$S_MSG_1"

run_hook "$REPO" "$H" "$(jq -n --arg k "$AWSKEY" --arg cwd "$REPO" --arg p "$REPO/src/other.py" \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"MultiEdit",tool_input:{file_path:$p,edits:[{old_string:"a",new_string:"b"},{old_string:"c",new_string:$k}]}}')"
expect "NS07 양성: MultiEdit edits[].new_string 안쪽까지 본다" 2 "$S_MSG_1"

run_hook "$REPO" "$H" "$(jq -n --arg k "$AWSKEY" --arg cwd "$REPO" --arg p "$REPO/nb.ipynb" \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"NotebookEdit",tool_input:{notebook_path:$p,new_source:$k}}')"
expect "NS08 양성: NotebookEdit new_source 도 본다" 2 "$S_MSG_1"

run_hook "$REPO" "$H" "$(jq -n --arg k "$AWSKEY" --arg cwd "$REPO" --arg p "$REPO/src/other.py" \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"Edit",tool_input:{file_path:$p,old_string:"a",new_string:"b",future_unknown_field:$k}}')"
expect "NS09 열린 어휘: 모르는 키에 실린 자격증명도 차단" 2 "$S_MSG_1"

run_hook "$REPO" "$H" "$(jq -n --arg k "$AWSKEY" --arg cwd "$REPO" --arg p "$REPO/src/other.py" \
  '{hook_event_name:"PreToolUse",cwd:$cwd,tool_name:"Edit",tool_input:{file_path:$p,old_string:$k,new_string:"REDACTED"}}')"
expect "NS10 음성: old_string(지우는 쪽)의 자격증명은 막지 않는다" 0

run_hook "$REPO" "$H" "$(json_write "$REPO/src/other.py" 'password=${DB_PASSWORD}')"
expect "NS11 음성: 환경변수 참조는 자격증명이 아니다" 0

run_hook "$REPO" "$H" "$(json_write "$REPO/src/other.py" 'password=os.environ["DB_PASSWORD"]')"
expect "NS12 음성: os.environ 참조는 자격증명이 아니다" 0

run_hook "$REPO" "$H" "$(json_write "$REPO/templates/intent.md" 'password=‹비밀번호›')"
expect "NS13 음성: 플레이스홀더 ‹› 는 자격증명이 아니다" 0

run_hook "$REPO" "$H" "$(json_write "$REPO/tests/fixtures/red/leak.md" "$AWSKEY")"
expect "NS14 면제: tests/fixtures/** 는 통과하되 면제 사실을 stderr 에 남긴다" 0 "면제" "tests/fixtures"

run_hook "$REPO" "$H" "$(json_write "$REPO/src/other.py" 'def add(a, b): return a + b')"
expect "NS15 음성: 평범한 소스는 통과" 0

ENVARR=(PATH="$SHIMBIN")
run_hook "$REPO" "$H" "$(json_write "$REPO/src/other.py" 'x')"
expect "NS16 fail-closed: jq 없는 PATH 에서 차단" 2 "jq"

run_hook "$REPO" "$H" '{"tool_input":'
expect "NS17 fail-closed: 깨진 JSON 차단" 2 "JSON"

run_hook "$REPO" "$H" ''
expect "NS18 fail-closed: 빈 stdin 차단" 2 "입력"

echo ""

# ================================================================ 4. production-gate
echo "-- production-gate (승인 없는 프로덕션 배포 차단) --"
H=production-gate.sh
G_MSG_1="RELEASE_APPROVAL"
G_MSG_2="승인"

run_hook "$REPO" "$H" "$(json_bash 'scripts/deploy.sh production' "$REPO")"
expect "PG01 양성: 승인값 없이 production 배포 차단" 2 "$G_MSG_1" "$G_MSG_2"

ENVARR=(RELEASE_APPROVAL=" ")
run_hook "$REPO" "$H" "$(json_bash 'scripts/deploy.sh production' "$REPO")"
expect "PG02 우회 공백만인 승인값: 차단" 2 "$G_MSG_1"

ENVARR=(RELEASE_APPROVAL="CAB-2026-09-08")
run_hook "$REPO" "$H" "$(json_bash 'scripts/deploy.sh production' "$REPO")"
expect "PG03 음성: 유효한 승인값이면 통과" 0

run_hook "$REPO" "$H" "$(json_bash 'scripts/deploy.sh staging' "$REPO")"
expect "PG04 음성: staging 배포는 승인 없이 통과" 0

run_hook "$REPO" "$H" "$(json_bash './scripts/deploy.sh production' "$REPO")"
expect "PG05 우회 ./ : 상대경로 호출도 차단" 2 "$G_MSG_1"

run_hook "$REPO" "$H" "$(json_bash 'bash scripts/deploy.sh --env=production' "$REPO")"
expect "PG06 우회 --env=production: 토큰 값 부분도 본다" 2 "$G_MSG_1"

run_hook "$REPO" "$H" "$(json_bash 'echo 준비 && scripts/deploy.sh production' "$REPO")"
expect "PG07 우회 명령 조합: && 뒤 세그먼트도 본다" 2 "$G_MSG_1"

run_hook "$REPO" "$H" "$(json_bash 'RELEASE_APPROVAL=self scripts/deploy.sh production' "$REPO")"
expect "PG08 우회 인라인 승인값: 명령 안에서 자기 승인 금지" 2 "$G_MSG_1"

run_hook "$REPO" "$H" "$(json_bash 'scripts/deploy.sh staging --config tools.yaml' "$REPO")"
expect "PG09 부분 문자열 함정: tools.yaml 이 걸리지 않는다" 0

run_hook "$REPO" "$H" "$(json_bash 'ls --dry-run=false' "$REPO")"
expect "PG10 부분 문자열 함정: --dry-run=false 가 걸리지 않는다" 0

run_hook "$REPO" "$H" "$(json_bash 'cat docs/production-notes.md' "$REPO")"
expect "PG11 토큰 단위: production-notes.md 는 production 토큰이 아니다" 0

ENVARR=(RELEASE_APPROVAL="CAB-2026-09-08")
run_hook "$REPO" "$H" "$(json_bash 'scripts/deploy.sh production --dry-run=false' "$REPO")"
expect "PG12 음성: 승인값이 있으면 인자가 붙어도 통과" 0

run_hook "$REPO" "$H" "$(json_bash 'scripts/deploy.sh staging --changelog docs/production-notes.md' "$REPO")"
expect "PG13 부분 문자열 함정: deploy 호출이어도 production-notes.md 는 production 이 아니다" 0

ENVARR=(PATH="$SHIMBIN")
run_hook "$REPO" "$H" "$(json_bash 'echo hi' "$REPO")"
expect "PG14 fail-closed: jq 없는 PATH 에서 차단" 2 "jq"

run_hook "$REPO" "$H" '{"tool_name":'
expect "PG15 fail-closed: 깨진 JSON 차단" 2 "JSON"

run_hook "$REPO" "$H" ''
expect "PG16 fail-closed: 빈 stdin 차단" 2 "빈 입력"

# --- 경로 해석 우회 세트(RD1 리뷰 F6-1) -----------------------------------------
# 아래 넷은 「배포 토큰을 문자열로 대조」하는 판정이 전부 뚫린 자리다. 판정은 어휘가 아니라
# 경로 해석이라야 한다 — 토큰을 절대경로로 풀어 scripts/deploy.sh 의 실경로와 대조한다.
run_hook "$REPO" "$H" "$(json_bash 'scripts/./deploy.sh production' "$REPO")"
expect "PG17 우회 /./ (리뷰 H14): 경로 접기가 //만 접고 /./ 를 안 접는다" 2 "$G_MSG_1"

run_hook "$REPO" "$H" "$(json_bash './dep.sh production' "$REPO")"
expect "PG18 우회 파일 심링크 (리뷰 H16): dep.sh → scripts/deploy.sh 도 배포다" 2 "$G_MSG_1"

run_hook "$REPO" "$H" "$(json_bash 'cd scripts && ./deploy.sh production' "$REPO")"
expect "PG19 우회 cd 세그먼트 (리뷰 H17): 작업 디렉터리를 옮겨도 같은 파일이다" 2 "$G_MSG_1"

run_hook "$REPO" "$H" "$(json_bash 'SCRIPTS/DEPLOY.SH production' "$REPO")"
expect "PG20 우회 대소문자 (리뷰 H23): 대소문자 비구분 FS 에서 같은 파일에 닿는다" 2 "$G_MSG_1"

# --- 경로 해석이 거짓 양성을 만들지 않는가(음성 대조) ---------------------------
run_hook "$REPO" "$H" "$(json_bash 'cd scripts && ./deploy.sh staging' "$REPO")"
expect "PG21 음성: cd 를 따라가도 staging 은 승인 없이 통과" 0

run_hook "$REPO" "$H" "$(json_bash 'cd docs && cat production-notes.md' "$REPO")"
expect "PG22 음성: cd 가 섞여도 배포 호출이 아니면 통과" 0

run_hook "$REPO" "$H" "$(json_bash 'cd src && python3 -m pytest -k production' "$REPO")"
expect "PG23 음성: production 토큰만 있고 배포 호출이 없으면 통과" 0

# --- 공백 판정 관용구의 행동 계약(성능 처방이 바꾸는 두 자리) ----------------------
# _lib.sh 의 빈-입력 검사와 production-gate.sh 의 승인값 검사는 둘 다 「공백을 전부
# 지우면 비는가」로 판정한다. 그 관용구를 bash 3.2 에서 폭발하지 않는 형태로 바꾸므로,
# 바꾸기 전에 바깥에서 보이는 행동을 못박는다(기존 행동의 계약 고정 — 이미 그린이다).
run_hook "$REPO" "$H" "$(printf ' \t \n\t ')"
expect "PG24 공백만인 stdin 은 빈 입력과 같다 — 차단" 2 "빈 입력"

ENVARR=(RELEASE_APPROVAL="$(printf '\t')")
run_hook "$REPO" "$H" "$(json_bash 'scripts/deploy.sh production' "$REPO")"
expect "PG25 탭만인 승인값: 차단(공백은 승인이 아니다)" 2 "$G_MSG_1"

ENVARR=(RELEASE_APPROVAL="$(printf '\n')")
run_hook "$REPO" "$H" "$(json_bash 'scripts/deploy.sh production' "$REPO")"
expect "PG26 개행만인 승인값: 차단" 2 "$G_MSG_1"

ENVARR=(RELEASE_APPROVAL="  CAB-2026-09-08  ")
run_hook "$REPO" "$H" "$(json_bash 'scripts/deploy.sh production' "$REPO")"
expect "PG27 음성: 앞뒤 공백이 껴도 알맹이가 있으면 승인이다" 0

# --- 해석 불가한 cd 목적지는 fail-closed(F6-1 설계) -------------------------------
# cd $VAR 는 기준 디렉터리 집합을 불완전하게 만든다 — 그 뒤의 ./deploy.sh 가 어느 파일에
# 닿는지 훅이 증명할 수 없다. 「모르는 것을 통과시키지 않는다」(_lib.sh 머리말)에 따라
# production 토큰이 함께 있을 때만 차단한다. 승인값이 있으면 통과한다는 계약은 그대로다.
run_hook "$REPO" "$H" "$(json_bash 'cd $DEPLOY_DIR && ./deploy.sh production' "$REPO")"
expect "PG28 해석 불가 cd + production: 기준 디렉터리를 모르므로 차단" 2 "$G_MSG_1"

run_hook "$REPO" "$H" "$(json_bash 'cd $SOMEWHERE && echo hello' "$REPO")"
expect "PG29 음성: 해석 불가 cd 라도 production 토큰이 없으면 통과" 0

run_hook "$REPO" "$H" "$(json_bash 'cd nosuchdir && python3 -m pytest -k production' "$REPO")"
expect "PG30 음성: 리터럴이지만 없는 cd 대상은 「해석 불가」가 아니다(cd 가 실패한다)" 0

ENVARR=(RELEASE_APPROVAL="CAB-2026-09-08")
run_hook "$REPO" "$H" "$(json_bash 'cd $DEPLOY_DIR && ./deploy.sh production' "$REPO")"
expect "PG31 음성: 해석 불가 cd 라도 유효한 승인값이면 통과" 0

echo ""
# ================================================================ 5. plan-sync
echo "-- plan-sync (plan 의 Files that change 밖 소스를 커밋 금지) --"
H=plan-sync.sh
L_MSG_1="plan.md"
L_MSG_2="Files that change"
L_MSG_3="같은 커밋"

reset_tree() {
  git -C "$REPO" reset -q >/dev/null 2>&1
  git -C "$REPO" checkout -q -- . >/dev/null 2>&1
}

git -C "$REPO" checkout -q -B feat/0002-claims-status

reset_tree
echo "# touched" >> "$REPO/src/other.py"
git -C "$REPO" add src/other.py
run_hook "$REPO" "$H" "$(json_bash 'git commit -m "wip"' "$REPO")"
expect "PS01 양성: plan 목록 밖 소스를 스테이징한 커밋 차단" 2 "$L_MSG_1" "$L_MSG_2" "$L_MSG_3"

reset_tree
echo "# touched" >> "$REPO/src/claims_status/service.py"
git -C "$REPO" add src/claims_status/service.py
run_hook "$REPO" "$H" "$(json_bash 'git commit -m "in plan"' "$REPO")"
expect "PS02 음성: plan 목록 안 소스는 통과" 0

reset_tree
echo "# touched" >> "$REPO/src/other.py"
echo "- \`src/other.py\`" >> "$REPO/intent/0002-claims-status/plan.md"
git -C "$REPO" add src/other.py intent/0002-claims-status/plan.md
run_hook "$REPO" "$H" "$(json_bash 'git commit -m "plan updated too"' "$REPO")"
expect "PS03 음성: 같은 커밋에 plan.md 가 있으면 통과(레슨 4)" 0

reset_tree
echo "# touched" >> "$REPO/src/other.py"
git -C "$REPO" add src/other.py
run_hook "$REPO" "$H" "$(json_bash 'git  commit -m "double space"' "$REPO")"
expect "PS04 우회 공백 2개: git  commit 도 커밋으로 본다" 2 "$L_MSG_1"

run_hook "$REPO" "$H" "$(json_bash 'git -C . commit -m x' "$REPO")"
expect "PS05 우회 git -C . : 전역 옵션을 건너뛰고 서브커맨드를 찾는다" 2 "$L_MSG_1"

run_hook "$REPO" "$H" "$(json_bash 'git ci -m x' "$REPO")"
expect "PS06 우회 별칭형 git ci: 커밋으로 본다" 2 "$L_MSG_1"

run_hook "$REPO" "$H" "$(json_bash 'echo 준비 && git commit -m x' "$REPO")"
expect "PS07 우회 명령 조합: && 뒤 세그먼트도 본다" 2 "$L_MSG_1"

run_hook "$REPO" "$H" "$(json_bash 'git status' "$REPO")"
expect "PS08 음성: 커밋이 아닌 git 명령은 통과" 0

run_hook "$REPO" "$H" "$(json_bash 'echo "git commit"' "$REPO")"
expect "PS09 부분 문자열 함정: 따옴표 안의 git commit 은 호출이 아니다" 0

run_hook "$REPO" "$H" "$(json_edit Edit file_path "$REPO/src/other.py" "$REPO")"
expect "PS10 범위 밖: Bash 도구가 아니면 통과" 0

reset_tree
run_hook "$REPO" "$H" "$(json_bash 'git commit -m nothing' "$REPO")"
expect "PS11 음성: 스테이징된 것이 없으면 통과" 0

reset_tree
echo "# unstaged" >> "$REPO/src/other.py"
run_hook "$REPO" "$H" "$(json_bash 'git commit -a -m "commit all"' "$REPO")"
expect "PS12 우회 git commit -a: 스테이징 안 한 추적 변경도 본다" 2 "$L_MSG_1"

reset_tree
echo "노트" >> "$REPO/intent/0002-claims-status/spec.md"
git -C "$REPO" add intent/0002-claims-status/spec.md
run_hook "$REPO" "$H" "$(json_bash 'git commit -m "artifact only"' "$REPO")"
expect "PS13 음성: intent/ 아티팩트만 바뀐 커밋은 plan 목록 대상 밖" 0

reset_tree
git -C "$REPO" checkout -q -B main
echo "# touched" >> "$REPO/src/other.py"
git -C "$REPO" add src/other.py
run_hook "$REPO" "$H" "$(json_bash 'git commit -m x' "$REPO")"
expect "PS14 음성: 브랜치에 NNNN- 이 없으면 범위 밖" 0

reset_tree
git -C "$REPO" checkout -q -B feat/9999-no-such-plan
echo "# touched" >> "$REPO/src/other.py"
git -C "$REPO" add src/other.py
run_hook "$REPO" "$H" "$(json_bash 'git commit -m x' "$REPO")"
expect "PS15 양성: 브랜치 id 는 있는데 plan.md 가 없으면 차단" 2 "$L_MSG_1"

reset_tree
git -C "$REPO" checkout -q -B feat/0002-claims-status

ENVARR=(PATH="$SHIMBIN")
run_hook "$REPO" "$H" "$(json_bash 'git commit -m x' "$REPO")"
expect "PS16 fail-closed: jq 없는 PATH 에서 차단" 2 "jq"

run_hook "$REPO" "$H" '{"tool_name":"Bash"'
expect "PS17 fail-closed: 깨진 JSON 차단" 2 "JSON"

run_hook "$REPO" "$H" ''
expect "PS18 fail-closed: 빈 stdin 차단" 2 "입력"

run_hook "$NOGIT" "$H" "$(json_bash 'git commit -m x' "$NOGIT")"
expect "PS19 fail-closed: git 레포가 아니면 차단" 2 "브랜치"

echo ""

# ================================================================ 합계
echo "================================================================"
echo "${PASS} passed, ${FAIL} failed  (총 $((PASS + FAIL)) 케이스)"
if [ "$FAIL" -gt 0 ]; then
  echo "실패 목록:$FAILED_LIST"
  exit 1
fi
exit 0
