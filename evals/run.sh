#!/usr/bin/env bash
# L10 687: "the checks that define acceptable (tests pass, lint clean,
# behavior unchanged, policy followed)"; L10 727: "runs are logged so results
# can be compared over time". Full evals require both deterministic and semantic checks.
# rc: 0=selected checks passed; 1=failed; 2=undecidable. Default is deterministic-only.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$ROOT" || exit 2
EDITION="${SDLC_EDITION:-tdd-first}"
case "$EDITION" in
  tdd-first|tdd-optional) ;;
  *) echo "UNDECIDABLE: invalid SDLC_EDITION: $EDITION (expected tdd-first or tdd-optional)" >&2; exit 2 ;;
esac
EDITION_ROOT="$ROOT/$EDITION"
PROJECT_DIR="$EDITION_ROOT/project"
PLUGIN_DIR="$EDITION_ROOT/org-skills"
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
[ -f "$PROJECT_DIR/CLAUDE.md" ] || {
  echo "UNDECIDABLE: 선택한 제품 템플릿 없음: $PROJECT_DIR" >&2; exit 2;
}
[ -f "$PLUGIN_DIR/.claude-plugin/plugin.json" ] || {
  echo "UNDECIDABLE: 선택한 에디션의 조직 플러그인 없음: $PLUGIN_DIR" >&2; exit 2;
}
PLUGIN_NAME="$(jq -er '.name | select(type == "string" and length > 0)' \
  "$PLUGIN_DIR/.claude-plugin/plugin.json")" || {
  echo "UNDECIDABLE: 선택한 플러그인 이름을 확인할 수 없음" >&2; exit 2;
}
case_files=(evals/cases/*.json)
[ -f "${case_files[0]}" ] || { echo "UNDECIDABLE: no eval cases" >&2; exit 2; }
EDITION_OUT="evals/out/$EDITION"
mkdir -p "$EDITION_OUT" || exit 2
if [ "$semantic" -eq 1 ]; then
  OUT="$(mktemp -d "$EDITION_OUT/semantic-XXXXXXXX")" || exit 2
  echo "FULL EVAL: edition=$EDITION; deterministic checks + semantic assertions; output=$OUT"
else
  OUT="$EDITION_OUT"
  echo "DETERMINISTIC ONLY: edition=$EDITION; assertions 미채점 — 전체 평가는 make evals"
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
      --edition "$EDITION" --generation-rc "$crc" --deterministic-rc "$drc" \
      --semantic-rc "$src" || worst=2
  fi
}

for case_file in "${case_files[@]}"; do
  cid="$(basename "$case_file" .json)"
  crc=2; drc=2; src=2
  echo "=== $cid"
  prompt="$(jq -r --arg out "$OUT/" --arg project "$EDITION/project" \
    --arg skills "$EDITION/org-skills" --arg plugin "$PLUGIN_NAME" \
    '.prompt | gsub("evals/out/"; $out) | gsub("SDLC_PROJECT"; $project) | gsub("SDLC_ORG_SKILLS"; $skills) | gsub("SDLC_PLUGIN_NAME"; $plugin)' \
    "$case_file")"
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
    claude --bare -p "$prompt" --plugin-dir "$PLUGIN_DIR" --model sonnet --effort low \
      --tools "$tools" --allowedTools "$tools" --output-format stream-json --verbose \
      --setting-sources "" --no-session-persistence > "$raw" 2> "$OUT/$cid.claude.stderr"
  else
    raw="$OUT/$cid.claude.json"
    claude --bare -p "$prompt" --plugin-dir "$PLUGIN_DIR" --model sonnet --effort low \
      --allowedTools "$tools" --setting-sources "" --output-format json \
      > "$raw" 2> "$OUT/$cid.claude.stderr"
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
    python3 evals/grade_assertions.py --case "$case_file" --edition "$EDITION" --result "$result" \
      --trace "$raw" --out "$OUT/$cid.assertions.json"
    src=$?; bump "$src"
    record_case
  fi
done

if [ "$semantic" -eq 1 ]; then
  python3 evals/record.py summary --edition "$EDITION" --out-dir "$OUT" --cases "${case_files[@]}"
  bump "$?"
else
  case "$worst" in
    0) echo "evals (DETERMINISTIC ONLY): 결정론 검사 통과; assertions 미채점" ;;
    1) echo "evals (DETERMINISTIC ONLY): 판정 실패; assertions 미채점" ;;
    2) echo "evals (DETERMINISTIC ONLY): 판정 불가 — 통과가 아니다" ;;
  esac
fi
exit "$worst"
