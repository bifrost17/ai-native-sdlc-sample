#!/usr/bin/env bash
# Trigger test runner (S3 · compliance). Runs one headless prompt per phrase and records the raw stream.
# usage: trigger-test.sh <project-dir> <raw-out-dir> <NN> <expected-skill-csv> <phrase> [<phrase>...]
# Each phrase -> <raw-out-dir>/<NN>-trigger-<k>.txt with header CMD: / AT_UTC: / RC: then the stream-json output.
# Prints one summary line per phrase: k | invoked skills | SKILL.md files Read | verdict for expected skills.
set -u
PROJ="$1"; OUT="$2"; NN="$3"; EXPECT="$4"; shift 4
MAXT="${MAX_TURNS:-6}"
k=0
for PHRASE in "$@"; do
  k=$((k+1))
  F="$OUT/${NN}-trigger-${k}.txt"
  AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  TMP=$(mktemp)
  ( cd "$PROJ" && timeout 420 claude -p "$PHRASE" --output-format stream-json --verbose --max-turns "$MAXT" < /dev/null > "$TMP" 2>&1 )
  RC=$?
  {
    echo "CMD: (cd $PROJ && claude -p \"$PHRASE\" --output-format stream-json --verbose --max-turns $MAXT)"
    echo "AT_UTC: $AT"
    echo "RC: $RC"
    cat "$TMP"
  } > "$F"
  rm -f "$TMP"
  INV=$(grep -o '"name":"Skill","input":{"skill":"[^"]*"' "$F" | sed 's/.*"skill":"//; s/"$//' | sort -u | tr '\n' ',' | sed 's/,$//')
  # 스킬은 Skill 도구 말고 Read/Bash(cat)로도 열린다 — 셋 다 센다.
  RD=$(grep -o '\.claude/skills/[A-Za-z0-9_-]*' "$F" | sed 's|.*/||' | sort -u | tr '\n' ',' | sed 's/,$//')
  VERDICT="PASS"
  EXP=()
  [ -n "$EXPECT" ] && IFS=',' read -ra EXP <<< "$EXPECT"
  for e in ${EXP+"${EXP[@]}"}; do
    [ -z "$e" ] && continue
    if ! printf '%s,%s' "$INV" "$RD" | tr ',' '\n' | grep -qx "$e"; then VERDICT="FAIL($e)"; fi
  done
  echo "$k | rc=$RC | invoked=[$INV] | read=[$RD] | $VERDICT | $PHRASE"
done
