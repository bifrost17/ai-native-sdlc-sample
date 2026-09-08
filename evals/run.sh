#!/usr/bin/env bash
# evals/run.sh — 실행기. **모델을 태운다 = API 키가 필요하다.**
#
# 🔴 이 파일의 「키가 있는 갈래」는 이 레포에서 아직 한 번도 실행되지 않았다.
#    코드로만 존재한다. 지금까지 실제로 돌아 본 것은 키 없음 갈래(rc=2)뿐이고,
#    그것은 tests/test_evals.sh 6번이 매 게이트마다 잰다. 키가 붙는 날
#    처음 도는 코드이므로, 첫 실행은 「검증된 경로」가 아니라 「처음 재는 경로」다.
#    (설계안 §10: evals 20~50 케이스 · 스케줄 · 머지 게이트화는 API 키 예산 확보까지 이월)
#
# 반환값
#   0  전 케이스 판정 통과
#   1  케이스 중 하나 이상 판정 실패
#   2  판정 불가 — 키 없음 · claude 없음 · jq 없음 · 채점기가 rc=2
#
# 🔴 rc=0 은 「전부 통과」만 뜻한다. 「안 돌았다」는 절대 rc=0 이 아니다.
#    imsungbin 은 워크플로를 만들어 놓고 disabled_manually 로 두어 한 번도 돌리지
#    않았는데, 레포만 보면 evals 가 있는 것처럼 보였다. 그 구멍을 rc 로 막는다.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

# --- 1. 키 확인 — 다른 무엇보다 먼저 -------------------------------------
# CI 러너에는 대화형 로그인이 없다. 키가 이 하네스의 유일한 인증 경로다.
if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  echo "SKIP: ANTHROPIC_API_KEY 없음 — evals 는 돌지 않았다"
  echo "      이것은 통과가 아니라 판정 불가(rc=2)다. 결정론 부분은 tests/test_evals.sh 가 잰다."
  exit 2
fi

# --- 2. 도구 확인 ---------------------------------------------------------
if ! command -v claude >/dev/null 2>&1; then
  echo "UNDECIDABLE: claude 실행 파일이 없다 — evals 는 돌지 않았다" >&2
  exit 2
fi
if ! command -v jq >/dev/null 2>&1; then
  echo "UNDECIDABLE: jq 가 없다 — 케이스 JSON 을 읽을 수 없다" >&2
  exit 2
fi

OUT_DIR="evals/out"
mkdir -p "$OUT_DIR" || exit 2

worst=0     # 0 통과 · 1 실패 · 2 판정 불가 (판정 불가가 가장 세다)
bump() {
  if [ "$1" -eq 2 ]; then
    worst=2
  elif [ "$1" -eq 1 ] && [ "$worst" -ne 2 ]; then
    worst=1
  fi
}

for case_file in evals/cases/*.json; do
  [ -f "$case_file" ] || continue
  base="${case_file##*/}"
  cid="${base%.json}"

  echo "=== $cid"

  prompt="$(jq -r '.prompt' "$case_file")"
  tools="$(jq -r '.allowed_tools // "Read,Write,Glob,Grep"' "$case_file")"
  if [ -z "$prompt" ] || [ "$prompt" = "null" ]; then
    echo "UNDECIDABLE: $cid 의 prompt 를 읽지 못했다" >&2
    bump 2
    continue
  fi

  ws="$OUT_DIR/$cid/ws"
  rm -rf "$ws"
  mkdir -p "$ws" || { bump 2; continue; }

  # 케이스가 가리키는 입력 픽스처를 워크스페이스 루트로 복사한다(basename 그대로).
  # 프롬프트는 이 사본을 가리킨다 — 픽스처가 없는데 프롬프트가 첨부를 가리키는
  # honghu 의 구멍을 막으려고, 여기서 복사가 실패하면 판정 불가로 죽는다.
  while IFS= read -r f || [ -n "$f" ]; do
    [ -n "$f" ] || continue
    if [ ! -f "$f" ]; then
      echo "UNDECIDABLE: $cid 의 files[] 픽스처가 없다: $f" >&2
      bump 2
      continue 2
    fi
    cp "$f" "$ws/${f##*/}" || { bump 2; continue 2; }
  done <<EOF
$(jq -r '.files[]?' "$case_file")
EOF

  raw="$OUT_DIR/$cid.claude.json"
  # 공식 비대화형 플래그 3종(code.claude.com/docs/en/headless.md · cli-reference.md):
  #   -p/--print · --allowedTools · --output-format json
  # 판정할 명령을 파이프 왼쪽에 두지 않는다 — rc 는 claude 의 것이어야 한다.
  claude -p "$prompt" --allowedTools "$tools" --output-format json > "$raw"
  claude_rc=$?
  if [ "$claude_rc" -ne 0 ]; then
    echo "UNDECIDABLE: $cid — claude 가 rc=$claude_rc 로 끝났다. 원문: $raw" >&2
    bump 2
    continue
  fi

  # 채점기가 읽는 결과 파일(evals/SCHEMA.md 「결과 파일」 참조).
  # workspace 는 결과 파일이 있는 디렉터리 기준 상대경로다.
  result="$OUT_DIR/$cid.json"
  if ! jq -n \
      --arg cid "$cid" \
      --arg ws "$cid/ws" \
      --arg result "$(jq -r '.result // ""' "$raw")" \
      --slurpfile raw "$raw" \
      '{schema_version: 1, case_id: $cid, workspace: $ws, result: $result, claude_raw: $raw[0]}' \
      > "$result"; then
    echo "UNDECIDABLE: $cid — 결과 파일을 만들지 못했다" >&2
    bump 2
    continue
  fi

  bash evals/check.sh "$case_file" "$result"
  bump $?
done

echo ""
case "$worst" in
  0) echo "evals: 전 케이스 통과" ;;
  1) echo "evals: 판정 실패가 있다" ;;
  2) echo "evals: 판정 불가가 있다 — 통과가 아니다" ;;
esac
exit "$worst"
