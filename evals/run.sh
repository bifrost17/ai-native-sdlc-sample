#!/usr/bin/env bash
# L10 687: "the checks that define acceptable (tests pass, lint clean,
# behavior unchanged, policy followed)"; L10 727: "runs are logged so results
# can be compared over time". Full evals require both deterministic and semantic checks.
# rc: 0=selected checks passed; 1=failed; 2=undecidable. Default is deterministic-only.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$ROOT" || exit 2
semantic=0
case "${1:-}" in
  "") ;;
  --semantic) semantic=1; shift ;;
  *) echo "UNDECIDABLE: usage: run.sh [--semantic]" >&2; exit 2 ;;
esac
[ "$#" -eq 0 ] || { echo "UNDECIDABLE: unexpected arguments" >&2; exit 2; }

if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  echo "SKIP: ANTHROPIC_API_KEY 없음 — evals 는 돌지 않았다(rc=2, 통과 아님)"
  exit 2
fi
command -v claude >/dev/null 2>&1 || { echo "UNDECIDABLE: claude 없음" >&2; exit 2; }
command -v jq >/dev/null 2>&1 || { echo "UNDECIDABLE: jq 없음" >&2; exit 2; }
command -v python3 >/dev/null 2>&1 || { echo "UNDECIDABLE: python3 없음" >&2; exit 2; }
PLUGIN_DIR="$ROOT/org-skills"
[ -f "$PLUGIN_DIR/.claude-plugin/plugin.json" ] || {
  echo "UNDECIDABLE: 현재 체크아웃의 조직 플러그인 없음: $PLUGIN_DIR" >&2; exit 2;
}
case_files=(evals/cases/*.json)
[ -f "${case_files[0]}" ] || { echo "UNDECIDABLE: no eval cases" >&2; exit 2; }
mkdir -p evals/out || exit 2
if [ "$semantic" -eq 1 ]; then
  OUT="$(mktemp -d evals/out/semantic-XXXXXXXX)" || exit 2
  echo "FULL EVAL: deterministic checks + semantic assertions; output=$OUT"
else
  OUT="evals/out"
  echo "DETERMINISTIC ONLY: assertions 미채점 — 전체 평가는 make evals"
fi
worst=0
bump() {
  case "$1" in
    0) ;;
    1) [ "$worst" -eq 0 ] && worst=1 ;;
    *) worst=2 ;;
  esac
}
record_case() {
  if [ "$semantic" -eq 1 ]; then
    python3 evals/record.py case --case-id "$cid" --out "$OUT/$cid.status.json" \
      --generation-rc "$crc" --deterministic-rc "$drc" --semantic-rc "$src" || worst=2
  fi
}

for case_file in "${case_files[@]}"; do
  cid="$(basename "$case_file" .json)"
  crc=2; drc=2; src=2
  echo "=== $cid"
  prompt="$(jq -r --arg out "$OUT/" '.prompt | gsub("evals/out/"; $out)' "$case_file")"
  tools="$(jq -r '.allowed_tools // "Read,Write,Glob,Grep"' "$case_file")"
  [ -n "$prompt" ] && [ "$prompt" != null ] || {
    echo "UNDECIDABLE: $cid prompt 읽기 실패" >&2; bump 2; record_case; continue;
  }
  ws="$OUT/$cid/ws"; rm -rf "$ws"; mkdir -p "$ws" || { bump 2; record_case; continue; }
  ok=1
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    if [ ! -f "$f" ]; then echo "UNDECIDABLE: $cid 픽스처 없음: $f" >&2; ok=0; break; fi
    cp "$f" "$ws/$(basename "$f")" || { ok=0; break; }
  done < <(jq -r '.files[]?' "$case_file")
  [ "$ok" -eq 1 ] || { bump 2; record_case; continue; }

  prompt="$prompt

Evaluation workspace (absolute): $ROOT/$ws
Create or change files only in this workspace. Read repository and loaded plugin guidance as
needed; use this workspace's PROJECT-POLICY.md for this case's project policy when present."
  result="$OUT/$cid.json"
  if [ "$semantic" -eq 1 ]; then
    raw="$OUT/$cid.claude.jsonl"
    claude -p "$prompt" --plugin-dir "$PLUGIN_DIR" --model sonnet --effort low \
      --tools "$tools" --allowedTools "$tools" --output-format stream-json --verbose \
      --no-session-persistence > "$raw" 2> "$OUT/$cid.claude.stderr"
  else
    raw="$OUT/$cid.claude.json"
    claude -p "$prompt" --plugin-dir "$PLUGIN_DIR" --model sonnet --effort low \
      --allowedTools "$tools" --output-format json > "$raw" 2> "$OUT/$cid.claude.stderr"
  fi
  crc=$?
  if [ "$crc" -ne 0 ]; then
    echo "UNDECIDABLE: $cid claude rc=$crc" >&2; bump 2; record_case; continue
  fi
  if [ "$semantic" -eq 1 ]; then
    python3 evals/record.py normalize --case "$case_file" --workspace "$cid/ws" \
      --trace "$raw" --out "$result"
    if [ "$?" -ne 0 ]; then crc=2; bump 2; record_case; continue; fi
  else
    jq -e 'type == "object" and (.is_error != true) and (.result | type == "string")' \
      "$raw" >/dev/null || { crc=2; bump 2; record_case; continue; }
    jq -n --arg cid "$cid" --arg ws "$cid/ws" --arg r "$(jq -r '.result' "$raw")" \
      --slurpfile raw "$raw" \
      '{schema_version: 1, case_id: $cid, workspace: $ws, result: $r, claude_raw: $raw[0]}' \
      > "$result" || { crc=2; bump 2; record_case; continue; }
  fi

  bash evals/check.sh "$case_file" "$result" > "$OUT/$cid.checks.log" 2>&1
  drc=$?; cat "$OUT/$cid.checks.log"
  bump "$drc"
  if [ "$semantic" -eq 1 ]; then
    python3 evals/grade_assertions.py --case "$case_file" --result "$result" \
      --trace "$raw" --out "$OUT/$cid.assertions.json"
    src=$?; bump "$src"
    record_case
  fi
done

if [ "$semantic" -eq 1 ]; then
  python3 evals/record.py summary --out-dir "$OUT" --cases "${case_files[@]}"
  bump "$?"
else
  case "$worst" in
    0) echo "evals (DETERMINISTIC ONLY): 결정론 검사 통과; assertions 미채점" ;;
    1) echo "evals (DETERMINISTIC ONLY): 판정 실패; assertions 미채점" ;;
    2) echo "evals (DETERMINISTIC ONLY): 판정 불가 — 통과가 아니다" ;;
  esac
fi
exit "$worst"
