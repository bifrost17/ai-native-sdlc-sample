#!/usr/bin/env bash
# 트리거 시험 하네스 — 임시 프로젝트에서 claude -p 를 헤드리스로 돌리고 Skill 도구 호출을 기록한다.
# 사용: trigger-harness.sh <project-dir> <out-file> <phrase>
# 출력 파일 머리 세 줄: CMD: / AT_UTC: / RC:  이어서 stream-json 원문. 마지막 줄 LOADED_SKILLS: 는 Skill 도구 호출의 skill 값 목록.
# --setting-sources project : 사용자 수준 스킬·플러그인을 빼고 프로젝트 .claude/ 만 본다. --strict-mcp-config : 사용자 MCP 제외.
set -u
proj="$1"; out="$2"; phrase="$3"
at=$(date -u +%Y-%m-%dT%H:%M:%SZ)
cmd="cd $proj && claude -p \"$phrase\" --output-format stream-json --verbose --max-turns 8 --setting-sources project --strict-mcp-config --permission-mode bypassPermissions"
tmp=$(mktemp)
( cd "$proj" && command claude -p "$phrase" --output-format stream-json --verbose --max-turns 8 --setting-sources project --strict-mcp-config --permission-mode bypassPermissions ) > "$tmp" 2>&1
rc=$?
loaded=$(grep -o '"name":"Skill","input":{"skill":"[^"]*"' "$tmp" | sed 's/.*"skill":"//; s/"$//' | tr '\n' ',' | sed 's/,$//')
{ echo "CMD: $cmd"; echo "AT_UTC: $at"; echo "RC: $rc"; cat "$tmp"; echo; echo "LOADED_SKILLS: ${loaded:-없음}"; } > "$out"
rm -f "$tmp"
echo "rc=$rc loaded=${loaded:-없음}"
