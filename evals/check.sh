#!/usr/bin/env bash
# evals/check.sh — 결정론 채점기. **모델도 API 키도 쓰지 않는다.**
#
#   사용법: bash evals/check.sh <케이스 json> <결과 json>
#           bash evals/check.sh --kinds          # 판정 종류의 닫힌 집합을 출력
#
# 반환값 (레슨 9 의 「gate configuration changes on the results」가 서려면
#          「안 돌았다」와 「통과했다」가 절대 같은 값이면 안 된다)
#   0  판정 전부 통과
#   1  판정 중 하나 이상 실패
#   2  판정 불가 — jq 없음 · 파일 없음 · 스키마 위반 · 닫힌 집합 밖 판정 종류
#
# 축의 어휘 소유권(ORCHESTRATION §10.3): 이 채점기가 열거하는 집합은
# CHECK_KINDS 7종이고, 그것을 닫는 것은 **소유권**이다 — 판정 종류를 늘리는 것은
# 이 파일뿐이고 케이스 파일은 늘릴 수 없다. 임의 셸 조각을 실행하는 판정을
# 두지 않는 이유가 그것이다(그 순간 어휘 소유자가 케이스 작성자로 넘어간다).
#
# 판정 대상은 전부 **워크스페이스 안의 파일**이다. 모델이 낸 산문 응답은
# 케이스의 assertions[] 에 두고 이 채점기는 채점하지 않는다 — 산문 판정은
# 결정론이 아니고, 결정론인 척하면 그 자리가 거짓 그린이 된다.
#
# 외부 의존은 jq 하나뿐이다(나머지는 bash 내장). jq 가 없으면 rc=2 로 죽는다 —
# 참조 레포 두 곳이 jq 부재에서 fail-open 으로 조용히 통과했다.
set -uo pipefail

# 판정 종류의 닫힌 집합 — 이 목록이 정본이다.
CHECK_KINDS="file_exists contains not_contains regex_present regex_absent frontmatter_has_keys frontmatter_equals"

die2() {
  echo "UNDECIDABLE: $1" >&2
  exit 2
}

if [ "${1:-}" = "--kinds" ]; then
  for _k in $CHECK_KINDS; do
    echo "$_k"
  done
  exit 0
fi

# jq 가 없으면 여기서 죽는다. 이 검사보다 앞서 실행되는 외부 명령은 없다 —
# 그래야 PATH 가 비어도 「명령 없음」이 아니라 이 사유로 rc=2 가 나온다.
if ! command -v jq >/dev/null 2>&1; then
  die2 "jq 가 없다 — JSON 을 읽을 수 없으므로 판정 불가(rc=2). 조용히 통과시키지 않는다."
fi

CASE_FILE="${1:-}"
RESULT_FILE="${2:-}"

if [ -z "$CASE_FILE" ] || [ -z "$RESULT_FILE" ]; then
  die2 "사용법: bash evals/check.sh <케이스 json> <결과 json>"
fi
[ -f "$CASE_FILE" ]   || die2 "케이스 파일 없음: $CASE_FILE"
[ -f "$RESULT_FILE" ] || die2 "결과 파일 없음: $RESULT_FILE"

jq -e . "$CASE_FILE"   >/dev/null 2>&1 || die2 "케이스 JSON 파싱 실패: $CASE_FILE"
jq -e . "$RESULT_FILE" >/dev/null 2>&1 || die2 "결과 JSON 파싱 실패: $RESULT_FILE"

# --- 케이스 스키마 -------------------------------------------------------
case_sv="$(jq -r '.schema_version // empty' "$CASE_FILE")"
[ "$case_sv" = "1" ] || die2 "케이스 schema_version 이 1 이 아님: '${case_sv}' ($CASE_FILE)"
CASE_ID="$(jq -r '.id // empty' "$CASE_FILE")"
[ -n "$CASE_ID" ] || die2 "케이스에 id 가 없다: $CASE_FILE"
case_prompt="$(jq -r '.prompt // empty' "$CASE_FILE")"
[ -n "$case_prompt" ] || die2 "케이스에 prompt 가 없다: $CASE_FILE"
jq -e '.checks | type == "array"' "$CASE_FILE" >/dev/null 2>&1 \
  || die2 "케이스의 checks 가 배열이 아니다: $CASE_FILE"

N="$(jq -r '.checks | length' "$CASE_FILE")"
case "$N" in
  ''|*[!0-9]*) die2 "checks 길이를 읽지 못했다: $CASE_FILE" ;;
esac
[ "$N" -gt 0 ] || die2 "checks 가 0건이다 — 판정이 없는 케이스는 통과가 아니라 판정 불가다: $CASE_FILE"

# --- 결과 스키마 · 워크스페이스 -----------------------------------------
res_sv="$(jq -r '.schema_version // empty' "$RESULT_FILE")"
[ "$res_sv" = "1" ] || die2 "결과 schema_version 이 1 이 아님: '${res_sv}' ($RESULT_FILE)"
ws_field="$(jq -r '.workspace // empty' "$RESULT_FILE")"
[ -n "$ws_field" ] || die2 "결과에 workspace 가 없다: $RESULT_FILE"

# 상대 workspace 는 **결과 파일이 있는 디렉터리** 기준으로 푼다 —
# 그래야 시험 픽스처가 어느 CWD 에서 돌아도 같은 것을 가리킨다.
RESULT_DIR="${RESULT_FILE%/*}"
[ "$RESULT_DIR" = "$RESULT_FILE" ] && RESULT_DIR="."
case "$ws_field" in
  /*) WS="$ws_field" ;;
  *)  WS="$RESULT_DIR/$ws_field" ;;
esac
[ -d "$WS" ] || die2 "워크스페이스 디렉터리 없음: $WS (결과 파일 $RESULT_FILE 의 workspace='$ws_field')"

# --- 도우미 (bash 내장만 쓴다) -------------------------------------------
cq() { # cq <index> <필드명> — 케이스의 checks[i].<필드> 를 낸다(없으면 빈 문자열)
  jq -r --argjson i "$1" ".checks[\$i].$2 // empty" "$CASE_FILE"
}

cq_keys() { # cq_keys <index> — checks[i].keys[] 를 한 줄씩
  jq -r --argjson i "$1" '.checks[$i].keys[]?' "$CASE_FILE"
}

fm_scan() { # fm_scan <파일> <'get'|'keys'> [키] — frontmatter 를 한 줄씩 훑는다
  local f="$1" mode="$2" want="${3:-}" line first=1 inblock=0 k v
  while IFS= read -r line || [ -n "$line" ]; do
    line="${line%$'\r'}"
    if [ "$first" -eq 1 ]; then
      first=0
      if [ "$line" = "---" ]; then
        inblock=1
        continue
      fi
      return 1   # 첫 줄이 --- 가 아니면 frontmatter 가 없다
    fi
    [ "$inblock" -eq 1 ] || break
    if [ "$line" = "---" ]; then
      break
    fi
    case "$line" in
      ' '*|$'\t'*) continue ;;   # 들여쓴 줄은 최상위 키가 아니다
      *:*) : ;;
      *) continue ;;
    esac
    k="${line%%:*}"
    v="${line#*:}"
    # 값 끝의 ' #주석' 을 떼어낸다 — 우리 템플릿은 status 줄에 어휘 목록을 주석으로 단다
    case "$v" in
      *" #"*) v="${v%% #*}" ;;
    esac
    k="${k#"${k%%[![:space:]]*}"}"; k="${k%"${k##*[![:space:]]}"}"
    v="${v#"${v%%[![:space:]]*}"}"; v="${v%"${v##*[![:space:]]}"}"
    if [ "$mode" = "keys" ]; then
      echo "$k"
    elif [ "$k" = "$want" ]; then
      printf '%s' "$v"
      return 0
    fi
  done < "$f"
  [ "$mode" = "keys" ] && return 0
  return 1
}

regex_hit() { # regex_hit <파일> <ERE> — 한 줄이라도 맞으면 0. ^ · $ 는 줄 단위로 문다.
  local f="$1" pat="$2" line
  while IFS= read -r line || [ -n "$line" ]; do
    line="${line%$'\r'}"
    if [[ "$line" =~ $pat ]]; then
      return 0
    fi
  done < "$f"
  return 1
}

# --- 판정 -----------------------------------------------------------------
n_pass=0
n_fail=0
i=0

emit_pass() { echo "  PASS  [$1] $2"; n_pass=$((n_pass + 1)); }
emit_fail() { echo "  FAIL  [$1] $2 — $3"; n_fail=$((n_fail + 1)); }

echo "CASE $CASE_ID  ($N 판정 · 워크스페이스 $WS)"

while [ "$i" -lt "$N" ]; do
  kind="$(cq "$i" kind)"

  known=0
  for _k in $CHECK_KINDS; do
    if [ "$_k" = "$kind" ]; then
      known=1
    fi
  done
  if [ "$known" -ne 1 ]; then
    die2 "checks[$i] 의 판정 종류가 닫힌 집합 밖: '$kind' (허용: $CHECK_KINDS) — 건너뛰지 않고 죽는다"
  fi

  path="$(cq "$i" path)"
  [ -n "$path" ] || die2 "checks[$i]($kind) 에 path 가 없다"
  case "$path" in
    /*) die2 "checks[$i].path 가 절대경로다: $path" ;;
  esac
  case "/$path/" in
    */../*) die2 "checks[$i].path 가 워크스페이스를 벗어난다: $path" ;;
  esac

  target="$WS/$path"
  label="$kind $path"

  case "$kind" in
    file_exists)
      if [ -e "$target" ]; then
        emit_pass "$i" "$label"
      else
        emit_fail "$i" "$label" "파일이 없다"
      fi
      ;;

    contains|not_contains)
      value="$(cq "$i" value)"
      [ -n "$value" ] || die2 "checks[$i]($kind) 에 value 가 없다"
      if [ ! -f "$target" ]; then
        emit_fail "$i" "$label" "대상 파일이 없다(판정 대상 부재는 통과가 아니다)"
      else
        content="$(<"$target")"
        if [ "$kind" = "contains" ]; then
          if [[ "$content" == *"$value"* ]]; then
            emit_pass "$i" "$label" 
          else
            emit_fail "$i" "$label" "있어야 할 문자열이 없다: '$value'"
          fi
        else
          if [[ "$content" == *"$value"* ]]; then
            emit_fail "$i" "$label" "없어야 할 문자열이 남아 있다: '$value'"
          else
            emit_pass "$i" "$label"
          fi
        fi
      fi
      ;;

    regex_present|regex_absent)
      pattern="$(cq "$i" pattern)"
      [ -n "$pattern" ] || die2 "checks[$i]($kind) 에 pattern 이 없다"
      if [ ! -f "$target" ]; then
        emit_fail "$i" "$label" "대상 파일이 없다(판정 대상 부재는 통과가 아니다)"
      elif regex_hit "$target" "$pattern"; then
        if [ "$kind" = "regex_present" ]; then
          emit_pass "$i" "$label"
        else
          emit_fail "$i" "$label" "없어야 할 패턴이 맞았다: /$pattern/"
        fi
      else
        if [ "$kind" = "regex_present" ]; then
          emit_fail "$i" "$label" "있어야 할 패턴이 한 줄도 맞지 않았다: /$pattern/"
        else
          emit_pass "$i" "$label"
        fi
      fi
      ;;

    frontmatter_has_keys)
      if ! jq -e --argjson i "$i" '.checks[$i].keys | type == "array" and length > 0' \
           "$CASE_FILE" >/dev/null 2>&1; then
        die2 "checks[$i](frontmatter_has_keys) 의 keys 가 비었거나 배열이 아니다"
      fi
      if [ ! -f "$target" ]; then
        emit_fail "$i" "$label" "대상 파일이 없다(판정 대상 부재는 통과가 아니다)"
      else
        present="$(fm_scan "$target" keys)"
        missing=""
        while IFS= read -r fk || [ -n "$fk" ]; do
          [ -n "$fk" ] || continue
          found=0
          while IFS= read -r pk || [ -n "$pk" ]; do
            [ "$pk" = "$fk" ] && found=1
          done <<EOF
$present
EOF
          if [ "$found" -ne 1 ]; then
            missing="$missing $fk"
          fi
        done <<EOF
$(cq_keys "$i")
EOF
        if [ -z "$missing" ]; then
          emit_pass "$i" "$label"
        else
          emit_fail "$i" "$label" "frontmatter 에 없는 키:$missing"
        fi
      fi
      ;;

    frontmatter_equals)
      fkey="$(cq "$i" key)"
      fval="$(cq "$i" value)"
      [ -n "$fkey" ] || die2 "checks[$i](frontmatter_equals) 에 key 가 없다"
      [ -n "$fval" ] || die2 "checks[$i](frontmatter_equals) 에 value 가 없다"
      label="$kind $path ($fkey == $fval)"
      if [ ! -f "$target" ]; then
        emit_fail "$i" "$label" "대상 파일이 없다(판정 대상 부재는 통과가 아니다)"
      else
        if got="$(fm_scan "$target" get "$fkey")"; then
          if [ "$got" = "$fval" ]; then
            emit_pass "$i" "$label"
          else
            emit_fail "$i" "$label" "frontmatter 의 $fkey 가 '$got' 다"
          fi
        else
          emit_fail "$i" "$label" "frontmatter 에 $fkey 가 없다"
        fi
      fi
      ;;
  esac

  i=$((i + 1))
done

echo "$CASE_ID: ${n_pass} passed, ${n_fail} failed"

if [ "$n_fail" -gt 0 ]; then
  exit 1
fi
exit 0
