#!/usr/bin/env bash
# evals/check.sh — 결정론 채점기(모델·API 키 불요). L10 692행: "the checks that
# define acceptable (tests pass, lint clean, behavior unchanged, policy
# followed)". rc 0=전부 통과 1=하나 이상 실패 2=판정 불가(jq 없음·파일 없음·
# 닫힌 집합 밖 kind) — "안 돌았다" 를 "통과" 로 접지 않는다(L10 727행 머지 게이트).
# 사용법: bash evals/check.sh <케이스.json> <결과.json> | --kinds
set -uo pipefail
CHECK_KINDS="file_exists contains not_contains regex_present regex_absent frontmatter_has_keys frontmatter_equals"
die2() { echo "UNDECIDABLE: $1" >&2; exit 2; }
[ "${1:-}" = "--kinds" ] && { for k in $CHECK_KINDS; do echo "$k"; done; exit 0; }
command -v jq >/dev/null 2>&1 || die2 "jq 가 없다 — 판정 불가"
CASE_FILE="${1:-}"; RESULT_FILE="${2:-}"
[ -n "$CASE_FILE" ] && [ -n "$RESULT_FILE" ] || die2 "사용법: check.sh <케이스> <결과>"
[ -f "$CASE_FILE" ] || die2 "케이스 파일 없음: $CASE_FILE"
[ -f "$RESULT_FILE" ] || die2 "결과 파일 없음: $RESULT_FILE"
jq -e . "$CASE_FILE" >/dev/null 2>&1 || die2 "케이스 JSON 파싱 실패: $CASE_FILE"
N="$(jq -r '.checks | length' "$CASE_FILE" 2>/dev/null)"
case "$N" in ''|*[!0-9]*) die2 "checks 를 못 읽었다: $CASE_FILE" ;; esac
[ "$N" -gt 0 ] || die2 "checks 가 0건 — 판정 없는 케이스는 통과가 아니다"
CASE_ID="$(jq -r '.id // "?"' "$CASE_FILE")"
ws_field="$(jq -r '.workspace // empty' "$RESULT_FILE" 2>/dev/null)"
[ -n "$ws_field" ] || die2 "결과에 workspace 가 없다: $RESULT_FILE"
RESULT_DIR="${RESULT_FILE%/*}"; [ "$RESULT_DIR" = "$RESULT_FILE" ] && RESULT_DIR="."
case "$ws_field" in /*) WS="$ws_field" ;; *) WS="$RESULT_DIR/$ws_field" ;; esac
[ -d "$WS" ] || die2 "워크스페이스 없음: $WS"

cq() { jq -r --argjson i "$1" ".checks[\$i].$2 // empty" "$CASE_FILE"; }
fm_get() { # fm_get <파일> <키> — frontmatter 최상위 키의 값(값 끝 '#주석' 제거)
  awk -v want="$2" 'NR==1{if($0!="---"){exit 1} next}
    $0=="---"{exit} /^[a-zA-Z_]+:/{split($0,a,":"); k=a[1];
      v=substr($0,length(k)+2); sub(/ *#.*/,"",v); gsub(/^ +| +$/,"",v);
      if(k==want){print v; f=1; exit}} END{exit !f}' "$1"
}
fm_keys() { awk 'NR==1{if($0!="---"){exit 1} next} $0=="---"{exit} /^[a-zA-Z_]+:/{split($0,a,":"); print a[1]}' "$1"; }
regex_hit() { grep -qE "$2" "$1" 2>/dev/null; }

pass=0; fail=0
emit() { if [ "$2" = 0 ]; then echo "  PASS  [$1] $3"; pass=$((pass+1));
  else echo "  FAIL  [$1] $3 — $4"; fail=$((fail+1)); fi; }

echo "CASE $CASE_ID ($N 판정 · $WS)"
for ((i = 0; i < N; i++)); do
  kind="$(cq "$i" kind)"
  case " $CHECK_KINDS " in *" $kind "*) ;; *) die2 "checks[$i] kind 가 닫힌 집합 밖: '$kind'" ;; esac
  path="$(cq "$i" path)"
  [ -n "$path" ] || die2 "checks[$i]($kind) 에 path 가 없다"
  case "$path" in /*) die2 "checks[$i].path 가 절대경로: $path" ;; esac
  case "/$path/" in */../*) die2 "checks[$i].path 가 워크스페이스를 벗어난다: $path" ;; esac
  t="$WS/$path"; label="$kind $path"
  case "$kind" in
    file_exists)
      [ -e "$t" ] && emit "$i" 0 "$label" || emit "$i" 1 "$label" "파일이 없다" ;;
    contains|not_contains)
      v="$(cq "$i" value)"; [ -n "$v" ] || die2 "checks[$i] 에 value 없음"
      [ -f "$t" ] || { emit "$i" 1 "$label" "대상 없음"; continue; }
      if grep -qF -- "$v" "$t"; then hit=0; else hit=1; fi
      [ "$kind" = contains ] && { [ "$hit" = 0 ] && emit "$i" 0 "$label" || emit "$i" 1 "$label" "없어야 할/있어야 할 문자열: $v"; } \
        || { [ "$hit" = 1 ] && emit "$i" 0 "$label" || emit "$i" 1 "$label" "없어야 할 문자열이 남음: $v"; } ;;
    regex_present|regex_absent)
      p="$(cq "$i" pattern)"; [ -n "$p" ] || die2 "checks[$i] 에 pattern 없음"
      [ -f "$t" ] || { emit "$i" 1 "$label" "대상 없음"; continue; }
      if regex_hit "$t" "$p"; then hit=0; else hit=1; fi
      [ "$kind" = regex_present ] && { [ "$hit" = 0 ] && emit "$i" 0 "$label" || emit "$i" 1 "$label" "패턴 불일치: /$p/"; } \
        || { [ "$hit" = 1 ] && emit "$i" 0 "$label" || emit "$i" 1 "$label" "없어야 할 패턴이 맞음: /$p/"; } ;;
    frontmatter_has_keys)
      [ -f "$t" ] || { emit "$i" 1 "$label" "대상 없음"; continue; }
      present="$(fm_keys "$t")"; missing=""
      while IFS= read -r k; do [ -n "$k" ] || continue
        echo "$present" | grep -qx "$k" || missing="$missing $k"
      done < <(jq -r --argjson i "$i" '.checks[$i].keys[]?' "$CASE_FILE")
      [ -z "$missing" ] && emit "$i" 0 "$label" || emit "$i" 1 "$label" "누락 키:$missing" ;;
    frontmatter_equals)
      k="$(cq "$i" key)"; v="$(cq "$i" value)"; label="$kind $path ($k==$v)"
      [ -f "$t" ] || { emit "$i" 1 "$label" "대상 없음"; continue; }
      got="$(fm_get "$t" "$k")"
      [ "$got" = "$v" ] && emit "$i" 0 "$label" || emit "$i" 1 "$label" "값이 '$got'" ;;
  esac
done
echo "$CASE_ID: $pass passed, $fail failed"
[ "$fail" -gt 0 ] && exit 1
exit 0
