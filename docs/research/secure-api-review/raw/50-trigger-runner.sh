#!/bin/bash
# S5 trigger-test runner. Usage: 50-trigger-runner.sh <NN> <label> <sandbox-dir> <prompt>
# Writes raw/<NN>-trigger-<label>.txt (CMD:/AT_UTC:/RC: header, full stream-json, then an extract of
# Skill/tool calls) and prints the skills that were loaded.
set -u
NN=$1; LABEL=$2; SANDBOX=$3; PROMPT=$4
OUT="$(cd "$(dirname "$0")" && pwd)/${NN}-trigger-${LABEL}.txt"
AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)
CMD="cd $SANDBOX && claude -p '$PROMPT' --output-format stream-json --verbose --max-turns 8 --permission-mode acceptEdits --allowedTools Read,Glob,Grep,Edit,Write,Skill,Bash(ls*),Bash(cat*) < /dev/null"
TMP=$(mktemp)
( cd "$SANDBOX" && git checkout -q -- . && env -u CLAUDECODE -u CLAUDE_CODE_ENTRYPOINT timeout 420 claude -p "$PROMPT" --output-format stream-json --verbose --max-turns 8 --permission-mode acceptEdits --allowedTools 'Read,Glob,Grep,Edit,Write,Skill,Bash(ls*),Bash(cat*)' < /dev/null ) > "$TMP" 2>&1
RC=$?
{
  printf 'CMD: %s\nAT_UTC: %s\nRC: %s\n' "$CMD" "$AT" "$RC"
  echo "SANDBOX_SKILLS: $(ls "$SANDBOX/.claude/skills" | tr '\n' ' ')"
  echo "--- extract (assistant tool_use / text / result) ---"
  python3 - "$TMP" <<'PY'
import sys,json
for line in open(sys.argv[1],encoding='utf-8',errors='replace'):
    try: m=json.loads(line)
    except Exception: print("RAW:",line.rstrip()[:300]); continue
    t=m.get("type")
    if t=="assistant":
        for b in m["message"].get("content",[]):
            if b.get("type")=="tool_use": print("TOOL_USE:", b["name"], json.dumps(b.get("input"),ensure_ascii=False)[:240])
            elif b.get("type")=="text": print("TEXT:", b["text"][:600].replace("\n"," / "))
    elif t=="result": print("RESULT:", m.get("subtype"), "turns", m.get("num_turns"), "cost_usd", m.get("total_cost_usd"), "session", m.get("session_id"))
PY
  echo "--- full stream-json ---"
  cat "$TMP"
} > "$OUT"
rm -f "$TMP"
echo "== $OUT"
grep -o 'TOOL_USE: Skill {[^}]*}' "$OUT" | sort | uniq -c
grep -q 'TOOL_USE: Skill' "$OUT" || echo "NO SKILL LOADED"
