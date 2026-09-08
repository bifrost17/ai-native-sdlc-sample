#!/usr/bin/env bash
# scripts/gates/10-docs.sh — 문서 게이트(W1-D).
#
# check_all.sh 가 scripts/gates/*.sh 를 source 하고 run_gate 함수 · PASS_COUNT ·
# FAIL_COUNT 를 제공하는 확장점은 아직 없다(W1-A 몫, 이 파일은 건드리지 않는다).
# 그 전까지 이 파일은 단독 `bash scripts/gates/10-docs.sh` 실행으로도 완결
# 동작해야 하므로, run_gate 가 이미 정의돼 있지 않을 때만(=단독 실행) 최소
# 호환 버전을 자체 정의한다. check_all.sh 가 나중에 이 파일을 source 하면
# 그 쪽의 run_gate·카운터를 그대로 쓴다.
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT" || exit 1

STANDALONE=0
if ! declare -F run_gate >/dev/null 2>&1; then
  STANDALONE=1
  PASS_COUNT=${PASS_COUNT:-0}
  FAIL_COUNT=${FAIL_COUNT:-0}
  run_gate() {
    local name="$1"
    shift
    local out rc
    out="$("$@" 2>&1)"
    rc=$?
    if [[ "$rc" -eq 0 ]]; then
      echo "PASS  $name"
      PASS_COUNT=$((PASS_COUNT + 1))
    else
      echo "FAIL  $name"
      if [[ -n "$out" ]]; then
        echo "$out" | sed 's/^/      /'
      fi
      FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
  }
fi

# --- 검사 1: CLAUDE.md 가 60줄 이하 ---
check_claude_md_length() {
  if [[ ! -f CLAUDE.md ]]; then
    echo "CLAUDE.md 없음"
    return 1
  fi
  local n
  n="$(wc -l < CLAUDE.md | tr -d ' ')"
  if [[ "$n" -gt 60 ]]; then
    echo "CLAUDE.md 이 ${n}줄 — 60줄 이하여야 함"
    return 1
  fi
  return 0
}

# --- 검사 2: docs/PLAYBOOK-MAP.md 가 14개 slug 를 전부 포함 ---
PLAYBOOK_SLUGS="introduction capture-intent requirements-and-design plan-mode claude-md skills-as-institutional-knowledge parallel-sessions-and-subagents give-claude-a-feedback-loop continuous-evals-in-ci ai-in-the-pr-review-loop hooks-as-approval-gates ci-cd-integration-and-deployment closing-the-loop-on-metrics closing-thoughts-and-resources"

check_playbook_map_slugs() {
  if [[ ! -f docs/PLAYBOOK-MAP.md ]]; then
    echo "docs/PLAYBOOK-MAP.md 없음"
    return 1
  fi
  local slug rc=0
  for slug in $PLAYBOOK_SLUGS; do
    if ! grep -q "$slug" docs/PLAYBOOK-MAP.md; then
      echo "docs/PLAYBOOK-MAP.md 에 slug 누락: $slug"
      rc=1
    fi
  done
  return "$rc"
}

# --- 검사 3: docs/PHASES.md 의 모든 항목 행에 승격 조건 열이 비어 있지 않음 ---
check_phases_promotion_conditions() {
  if [[ ! -f docs/PHASES.md ]]; then
    echo "docs/PHASES.md 없음"
    return 1
  fi
  local rc=0
  local line last
  while IFS= read -r line; do
    case "$line" in
      '|'*) ;;
      *) continue ;;
    esac
    case "$line" in
      *'---'*) continue ;;
      *'승격 조건'*) continue ;;
    esac
    # 마지막 열(승격 조건) 추출: 끝 '|' 제거 후 마지막 '|' 뒤 텍스트.
    last="${line%|}"
    last="${last##*|}"
    last="$(printf '%s' "$last" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
    if [[ -z "$last" ]]; then
      echo "docs/PHASES.md 행에 승격 조건이 비어 있음: $line"
      rc=1
    fi
  done < docs/PHASES.md
  return "$rc"
}

# --- 검사 4: REVIEW.md 가 패스 3 이름(bugs · security · compliance)을 포함 ---
check_review_passes() {
  if [[ ! -f REVIEW.md ]]; then
    echo "REVIEW.md 없음"
    return 1
  fi
  local p rc=0
  for p in bugs security compliance; do
    if ! grep -qi "$p" REVIEW.md; then
      echo "REVIEW.md 에 패스 누락: $p"
      rc=1
    fi
  done
  return "$rc"
}

# --- 검사 5: .github/CODEOWNERS 가 intent/** 규칙을 포함 ---
check_codeowners_intent_rule() {
  if [[ ! -f .github/CODEOWNERS ]]; then
    echo ".github/CODEOWNERS 없음"
    return 1
  fi
  if ! grep -q 'intent/\*\*' .github/CODEOWNERS; then
    echo ".github/CODEOWNERS 에 intent/** 규칙 누락"
    return 1
  fi
  return 0
}

run_gate "CLAUDE.md <= 60줄" check_claude_md_length
run_gate "PLAYBOOK-MAP.md 가 14 slug 전부 포함" check_playbook_map_slugs
run_gate "PHASES.md 모든 행에 승격 조건 존재" check_phases_promotion_conditions
run_gate "REVIEW.md 가 패스 3 이름 포함" check_review_passes
run_gate "CODEOWNERS 가 intent/** 포함" check_codeowners_intent_rule

if [[ "$STANDALONE" -eq 1 ]]; then
  echo ""
  echo "${PASS_COUNT} passed, ${FAIL_COUNT} failed"
  if [[ "$FAIL_COUNT" -gt 0 ]]; then
    exit 1
  fi
  exit 0
fi
