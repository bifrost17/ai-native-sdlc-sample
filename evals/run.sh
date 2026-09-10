#!/usr/bin/env bash
# evals/run.sh — 실행기. 모델을 태운다 = API 키가 필요하다.
# L10 727행: "the pass-rate threshold is enforced as a merge check, runs are
# logged so results can be compared over time" — rc=2("안 돌았다")를 rc=0
# ("통과")으로 접지 않는다(SKIP 문구를 반드시 찍는다).
# rc: 0=전 케이스 통과 1=판정 실패 있음 2=판정 불가(키·claude·jq 없음)
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$ROOT" || exit 1

if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  echo "SKIP: ANTHROPIC_API_KEY 없음 — evals 는 돌지 않았다(rc=2, 통과 아님)"
  exit 2
fi
command -v claude >/dev/null 2>&1 || { echo "UNDECIDABLE: claude 없음" >&2; exit 2; }
command -v jq >/dev/null 2>&1 || { echo "UNDECIDABLE: jq 없음" >&2; exit 2; }
PLUGIN_DIR="$ROOT/org-skills"
[ -f "$PLUGIN_DIR/.claude-plugin/plugin.json" ] || {
  echo "UNDECIDABLE: 현재 체크아웃의 조직 플러그인 없음: $PLUGIN_DIR" >&2; exit 2;
}

OUT="evals/out"; mkdir -p "$OUT" || exit 2
worst=0
bump() { [ "$1" -eq 2 ] && worst=2 || { [ "$1" -eq 1 ] && [ "$worst" -ne 2 ] && worst=1; }; }

for case_file in evals/cases/*.json; do
  [ -f "$case_file" ] || continue
  cid="$(basename "$case_file" .json)"
  echo "=== $cid"
  prompt="$(jq -r '.prompt' "$case_file")"
  tools="$(jq -r '.allowed_tools // "Read,Write,Glob,Grep"' "$case_file")"
  [ -n "$prompt" ] && [ "$prompt" != null ] || { echo "UNDECIDABLE: $cid prompt 읽기 실패" >&2; bump 2; continue; }
  ws="$OUT/$cid/ws"; rm -rf "$ws"; mkdir -p "$ws" || { bump 2; continue; }
  ok=1
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    if [ ! -f "$f" ]; then echo "UNDECIDABLE: $cid 픽스처 없음: $f" >&2; ok=0; break; fi
    cp "$f" "$ws/$(basename "$f")" || { ok=0; break; }
  done < <(jq -r '.files[]?' "$case_file")
  [ "$ok" -eq 1 ] || { bump 2; continue; }

  # Keep the repository cwd for the existing prompts and project guidance. Each case writes
  # into its own workspace; the fixture PROJECT-POLICY.md, when present, belongs to that case.
  prompt="$prompt

Evaluation workspace (absolute): $ROOT/$ws
Create or change files only in this workspace. Read repository and loaded plugin guidance as
needed; use this workspace's PROJECT-POLICY.md for this case's project policy when present."
  raw="$OUT/$cid.claude.json"
  claude -p "$prompt" --plugin-dir "$PLUGIN_DIR" --allowedTools "$tools" --output-format json > "$raw"
  crc=$?
  if [ "$crc" -ne 0 ]; then echo "UNDECIDABLE: $cid claude rc=$crc" >&2; bump 2; continue; fi

  result="$OUT/$cid.json"
  jq -n --arg cid "$cid" --arg ws "$cid/ws" --arg r "$(jq -r '.result // ""' "$raw")" \
    --slurpfile raw "$raw" \
    '{schema_version: 1, case_id: $cid, workspace: $ws, result: $r, claude_raw: $raw[0]}' \
    > "$result" || { bump 2; continue; }

  bash evals/check.sh "$case_file" "$result"
  bump $?
done

case "$worst" in
  0) echo "evals: 전 케이스 통과" ;;
  1) echo "evals: 판정 실패가 있다" ;;
  2) echo "evals: 판정 불가가 있다 — 통과가 아니다" ;;
esac
exit "$worst"
