#!/usr/bin/env bash
# tests/test_managed_settings.sh — org/managed-settings.example.json 계약 시험 (설계안 §6.3).
#
# 왜 있는가: 레슨 11(관리형 설정)의 예시 파일은 docs/PHASES.md 가 "예시 파일만 비활성으로
# 둠"이라 적어 org/managed-settings.example.json 이 있다고 전제하지만, main·열린 PR 어디에도
# 없었다(W1-K 착수 사유). 이 시험은 그 파일이 (a) 유효하고 (b) 레슨 11 키를 전부 담고
# (c) 레슨이 경고한 함정(allowManagedHooksOnly 가 프로젝트 훅을 죽인다)을 기계로 고정하고
# (d) 사용자 자신의 ~/.claude 를 실수로 가리키지 않는지를 잰다.
#
# 무엇을 재는가:
#   ① org/managed-settings.example.json 이 존재하고 유효한 JSON
#   ② 레슨 11 키 목록이 전부 존재(키 이름 하드코딩)
#   ③ allowManagedHooksOnly 가 true 이면 hooks 블록이 반드시 있어야 한다
#      (없으면 FAIL — 레슨의 함정을 기계로 고정)
#   ④ hooks 블록이 가리키는 스크립트 경로가 .claude/hooks/ 에 실재하는가
#      (main 에 아직 없으면 FAIL 이 아니라 SKIP — 조용한 통과 금지, 사유를 출력)
#   ⑤ org/README.md 가 "비활성 예시" 와 "allowManagedHooksOnly" 함정을 언급하는가
#   ⑥ 안전 검사 — JSON 파일이 사용자 홈 경로(~/.claude)를 가리키지 않는가
#      (실수로 자기 설정에 적용되는 사고를 막는다)
#
# 무엇을 재지 않는가: 이 예시가 실제 조직(Team/Enterprise) 관리 콘솔에 배포됐을 때의
# 동작(조직 계정이 없어 라이브 대조 불가 — docs/PHASES.md 레슨 11 행의 승격 조건과 동일
# 이유) · Claude Code 가 이 스키마를 런타임에 정확히 그렇게 해석하는지(문서 대조로만
# 확인했다 — https://code.claude.com/docs/en/settings-reference · managed-settings,
# 2026-09-08 실측. 라이브 Claude Code 인스턴스 대조 아님).
#
# rc 규약(scripts/check_all.sh 의 run_gate 확장 지점과 동일):
#   0 = PASS(FAIL 없음. SKIP 이 있어도 0 은 아니다 — 아래 참조)
#   3 = SKIP(FAIL 은 없지만 SKIP 이 1건 이상 — 못 잰 것은 통과가 아니다)
#   1 = FAIL(FAIL 이 1건 이상)
#
# 호환: macOS 기본 bash 3.2. JSON 파싱은 python3 표준 라이브러리(json.tool 포함) —
# jq 비의존(이 시험만 실행할 환경에 jq 가 없을 수 있어서다; tests/test_wiring.sh 는
# 별도 레인 소유라 여기서 그 판단을 재사용하지 않는다).
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
JSONFILE="$ROOT/org/managed-settings.example.json"
README="$ROOT/org/README.md"
HOOKDIR="$ROOT/.claude/hooks"

PASS_COUNT=0
FAIL_COUNT=0
SKIP_COUNT=0

ok() {
  PASS_COUNT=$((PASS_COUNT + 1))
  echo "PASS  $1"
}
bad() {
  FAIL_COUNT=$((FAIL_COUNT + 1))
  echo "FAIL  $1"
  if [ -n "${2:-}" ]; then
    echo "$2" | sed 's/^/      /'
  fi
}
skip() {
  SKIP_COUNT=$((SKIP_COUNT + 1))
  echo "SKIP  $1"
  if [ -n "${2:-}" ]; then
    echo "      사유: $2"
  fi
}

finish() {
  echo ""
  echo "${PASS_COUNT} passed, ${FAIL_COUNT} failed, ${SKIP_COUNT} skipped"
  if [ "$FAIL_COUNT" -gt 0 ]; then
    exit 1
  elif [ "$SKIP_COUNT" -gt 0 ]; then
    exit 3
  fi
  exit 0
}

if ! command -v python3 >/dev/null 2>&1; then
  bad "python3 이 없어 JSON 을 판정할 수 없다 — 못 잰 것은 통과가 아니다"
  finish
fi

# --- ① 존재 + 유효 JSON ---------------------------------------------------
if [ ! -f "$JSONFILE" ]; then
  bad "① org/managed-settings.example.json 없음"
  finish
fi

JSON_ERR="$(python3 -m json.tool "$JSONFILE" 2>&1 >/dev/null)"
if [ -z "$JSON_ERR" ]; then
  ok "① org/managed-settings.example.json 이 유효한 JSON (python3 -m json.tool)"
else
  bad "① JSON 파싱 실패" "$JSON_ERR"
  finish
fi

# --- ② 레슨 11 키 목록 전수 존재 -------------------------------------------
MISSING_KEYS="$(python3 - "$JSONFILE" <<'PY'
import json, sys

path = sys.argv[1]
with open(path) as f:
    data = json.load(f)


def get(d, dotted):
    cur = d
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None, False
        cur = cur[part]
    return cur, True


# 축자 목록 — 브리프 W1-K / 설계안 §6.3.
required = [
    "permissions.deny",
    "permissions.allow",
    "permissions.disableBypassPermissionsMode",
    "allowManagedPermissionRulesOnly",
    "sandbox.enabled",
    "sandbox.failIfUnavailable",
    "sandbox.allowUnsandboxedCommands",
    "sandbox.network.allowedDomains",
    "sandbox.credentials.files",
    "sandbox.credentials.envVars",
    "allowManagedHooksOnly",
    "disableSideloadFlags",
    "strictKnownMarketplaces",
    "allowManagedMcpServersOnly",
    "requiredMinimumVersion",
]

missing = []
for key in required:
    _, found = get(data, key)
    if not found:
        missing.append(key)

files, found = get(data, "sandbox.credentials.files")
if found and isinstance(files, list):
    for i, entry in enumerate(files):
        if not isinstance(entry, dict) or "mode" not in entry:
            missing.append("sandbox.credentials.files[%d].mode" % i)

envvars, found = get(data, "sandbox.credentials.envVars")
if found and isinstance(envvars, list):
    for i, entry in enumerate(envvars):
        if not isinstance(entry, dict) or "mode" not in entry:
            missing.append("sandbox.credentials.envVars[%d].mode" % i)

for m in missing:
    print(m)
sys.exit(1 if missing else 0)
PY
)"
MISSING_RC=$?
if [ "$MISSING_RC" -eq 0 ]; then
  ok "② 레슨 11 키 15종 전부 존재(permissions·sandbox·allowManaged*·disableSideloadFlags·strictKnownMarketplaces·requiredMinimumVersion)"
else
  bad "② 레슨 11 키 누락" "$MISSING_KEYS"
fi

# --- ③ allowManagedHooksOnly=true → hooks 블록 필수(레슨의 함정을 기계로 고정) ---
HOOKS_TRAP_ERR="$(python3 - "$JSONFILE" <<'PY'
import json, sys

data = json.load(open(sys.argv[1]))
only = data.get("allowManagedHooksOnly")
hooks = data.get("hooks")
if only is True and not hooks:
    print("allowManagedHooksOnly=true 인데 hooks 블록이 없다 — 관리형 설정이 프로젝트 훅 5개를 죽이는데 대체 정의가 없다(레슨 11 함정 미방어)")
    sys.exit(1)
sys.exit(0)
PY
)"
HOOKS_TRAP_RC=$?
if [ "$HOOKS_TRAP_RC" -eq 0 ]; then
  ok "③ allowManagedHooksOnly=true 일 때 hooks 블록 필수 — 만족(레슨 11 함정 방어)"
else
  bad "③ allowManagedHooksOnly=true 인데 hooks 블록 없음" "$HOOKS_TRAP_ERR"
fi

# --- ④ hooks 블록이 가리키는 스크립트가 레포에 실재하는가 -----------------
HOOK_CMDS="$(python3 - "$JSONFILE" <<'PY'
import json, sys

data = json.load(open(sys.argv[1]))
hooks = data.get("hooks", {})
cmds = []


def walk(node):
    if isinstance(node, dict):
        cmd = node.get("command")
        if isinstance(cmd, str):
            cmds.append(cmd)
        for v in node.values():
            walk(v)
    elif isinstance(node, list):
        for v in node:
            walk(v)


walk(hooks)
for c in cmds:
    print(c)
PY
)"

REL_PATHS="$(printf '%s\n' "$HOOK_CMDS" | grep -oE '\.claude/hooks/[^"[:space:]]+\.sh' | sort -u)"

if [ -z "$REL_PATHS" ]; then
  skip "④ hooks 블록 참조 경로 실재" ".claude/hooks/*.sh 형식의 경로를 hooks 블록에서 못 찾음(hooks 블록이 비었거나 형식이 다르다)"
elif [ ! -d "$HOOKDIR" ]; then
  skip "④ hooks 블록 참조 경로 실재" "main 에 .claude/hooks/ 자체가 아직 없음(PR feat/0001-enforcement-hooks 미병합). 케이스 ③(함정 방어)은 이미 확인됐고, 참조 파일의 실재는 그 PR 병합 후 재측정해야 한다"
else
  MISSING_PATHS=""
  while IFS= read -r rel; do
    [ -z "$rel" ] && continue
    if [ ! -f "$ROOT/$rel" ]; then
      MISSING_PATHS="${MISSING_PATHS}${rel}
"
    fi
  done <<REL_EOF
$REL_PATHS
REL_EOF
  if [ -n "$MISSING_PATHS" ]; then
    bad "④ hooks 블록 참조 경로 중 레포에 없는 것이 있다" "$MISSING_PATHS"
  else
    ok "④ hooks 블록이 가리키는 스크립트 전부 레포에 실재"
  fi
fi

# --- ⑤ org/README.md 가 함정을 언급하는가 ----------------------------------
if [ ! -f "$README" ]; then
  bad "⑤ org/README.md 없음"
else
  README_OK=1
  README_MISSING=""
  if ! grep -q "비활성 예시" "$README"; then
    README_OK=0
    README_MISSING="${README_MISSING}\"비활성 예시\" 문구 없음\n"
  fi
  # 단순히 "allowManagedHooksOnly" 문자열이 어딘가(표의 값 칸 등)에 있는 것만으로는
  # "함정을 언급"했다고 보지 않는다 — allowManagedHooksOnly 가 프로젝트 훅을 "죽인다"는
  # 함정 설명 자체가 있어야 통과한다. 이 마커라야 함정 문단 삭제 뮤테이션에 red 로 운다
  # 재현: 이 함정 설명 문단(위 "죽인다" 문장)을 org/README.md 에서 지우고
  # bash tests/test_managed_settings.sh 를 돌리면 이 케이스 ⑤가 red 로 운다.
  if ! grep -q "allowManagedHooksOnly" "$README"; then
    README_OK=0
    README_MISSING="${README_MISSING}\"allowManagedHooksOnly\" 언급 없음\n"
  fi
  if ! grep -q "죽인다" "$README"; then
    README_OK=0
    README_MISSING="${README_MISSING}함정 설명(\"죽인다\") 없음 — allowManagedHooksOnly 가 프로젝트 훅에 하는 일을 설명하는 문단이 없다\n"
  fi
  if [ "$README_OK" -eq 1 ]; then
    ok "⑤ org/README.md 가 비활성 예시·allowManagedHooksOnly 함정을 언급"
  else
    bad "⑤ org/README.md 언급 누락" "$(printf "$README_MISSING")"
  fi
fi

# --- ⑥ 안전 검사 — 사용자 홈 경로(~/.claude)를 가리키지 않는가 ------------
if grep -q '~/\.claude' "$JSONFILE" 2>/dev/null; then
  bad "⑥ 안전 검사 — JSON 이 사용자 홈 경로(~/.claude)를 가리킨다(실수로 적용될 위험)"
else
  ok "⑥ 안전 검사 — JSON 이 ~/.claude 를 가리키지 않음"
fi

finish
