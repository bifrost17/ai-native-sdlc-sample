#!/usr/bin/env bash
# Usage: run-trigger.sh <project-dir> <raw-basename NN-name> <prompt> [max-turns]
# Runs headless claude in <project-dir>, saves stream-json to raw/<NN-name>.jsonl and a
# header+summary to raw/<NN-name>.txt. Prints which skills were invoked (Skill tool_use).
set -u
PROJ="$1"; NAME="$2"; PROMPT="$3"; TURNS="${4:-4}"
RAW="$(cd "$(dirname "$0")" && pwd)"
AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
CMD="cd $PROJ && claude -p '<prompt>' --output-format stream-json --verbose --max-turns $TURNS < /dev/null"
( cd "$PROJ" && timeout 420 claude -p "$PROMPT" --output-format stream-json --verbose --max-turns "$TURNS" < /dev/null ) > "$RAW/$NAME.jsonl" 2>&1
RC=$?
{
  echo "CMD: $CMD"
  echo "AT_UTC: $AT"
  echo "RC: $RC"
  echo "PROMPT: $PROMPT"
  echo "PROJECT: $PROJ"
  echo "--- tool_use / text summary (from $NAME.jsonl)"
  python3 - "$RAW/$NAME.jsonl" <<'PY'
import json,sys
skills=[]
for l in open(sys.argv[1]):
    try: d=json.loads(l)
    except Exception: continue
    if d.get('type')=='assistant':
        for c in d['message']['content']:
            if c['type']=='tool_use':
                print("TOOL_USE:",c['name'],json.dumps(c['input'],ensure_ascii=False)[:240])
                if c['name']=='Skill': skills.append(c['input'].get('skill'))
            elif c['type']=='text':
                print("TEXT:",c['text'][:400].replace('\n',' '))
    elif d.get('type')=='result':
        print("RESULT:",d.get('subtype'),"turns=",d.get('num_turns'))
print("SKILLS_LOADED:",skills if skills else "NONE")
PY
} > "$RAW/$NAME.txt"
grep -E '^(RC|SKILLS_LOADED):' "$RAW/$NAME.txt"
