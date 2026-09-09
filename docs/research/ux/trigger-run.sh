#!/usr/bin/env bash
# 트리거 시험 러너 — 임시 프로젝트에서 claude -p 를 헤드리스로 돌리고 Skill 도구 호출을 raw/ 에 남긴다.
# 레포를 플러그인으로 로드한다(--plugin-dir, 개발·시험 전용 · docs/decisions/S8-plugin.md 2).
# 사용: trigger-run.sh <임시프로젝트dir> <플러그인루트> <raw 파일 경로> "<프롬프트>" "<기대 스킬 쉼표구분>"
set -u
PROJ="$1"; PLUG="$2"; OUT="$3"; PROMPT="$4"; EXPECT="${5:-}"
MAXTURNS="${MAXTURNS:-6}"   # 집합 시험처럼 일이 큰 과제는 MAXTURNS=20 으로 올려 부른다
AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)
CMD="(cd $PROJ && claude -p \"$PROMPT\" --plugin-dir $PLUG --output-format stream-json --verbose --max-turns $MAXTURNS < /dev/null)"
TMP=$(mktemp)
( cd "$PROJ" && timeout 420 claude -p "$PROMPT" --plugin-dir "$PLUG" --output-format stream-json --verbose --max-turns $MAXTURNS < /dev/null > "$TMP" 2>&1 )
RC=$?
SKILLS=$(python3 - "$TMP" <<'PY'
import json,sys
names=[]
for line in open(sys.argv[1]):
    try: o=json.loads(line)
    except Exception: continue
    if o.get('type')=='assistant':
        for b in o['message'].get('content',[]):
            if b.get('type')=='tool_use' and b.get('name')=='Skill':
                names.append(b['input'].get('skill',''))
print(','.join(names) if names else '(none)')
PY
)
{
  echo "CMD: $CMD"
  echo "AT_UTC: $AT"
  echo "RC: $RC"
  echo "SKILL_CALLS: $SKILLS"
  echo "EXPECT: $EXPECT"
  echo "----- stream-json -----"
  cat "$TMP"
} > "$OUT"
rm -f "$TMP"
echo "$AT rc=$RC skills=[$SKILLS] expect=[$EXPECT] -> $OUT"
