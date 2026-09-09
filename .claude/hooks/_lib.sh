#!/bin/bash
# .claude/hooks/_lib.sh — shared by the five hooks; not a hook itself.
# Decision: fail-closed. No jq, or stdin that is not JSON → exit 2 (block). "Unknown" is not "clean";
# the reference repos that did `|| exit 0` here silently switched their guardrails off.
# L12 866행: "Allow and block decisions are logged with a timestamp." L12 934행 (OTel export) is
# outside this repo's tree — logged here as a local file only.
ROOT="$(cd "${BASH_SOURCE[0]%/*}/../.." && pwd -P)"
HOOK="${0##*/}"
block() { printf '[%s] BLOCKED: %s\n' "$HOOK" "$*" >&2; exit 2; }
command -v jq >/dev/null 2>&1 || block "jq not found, so the hook input cannot be parsed and the action is refused. Route: install jq (brew install jq / apt-get install jq) and retry."
IN="$(cat)"
printf '%s' "$IN" | jq -e . >/dev/null 2>&1 || block "hook input is not valid JSON; refused. Route: run the hook with a Claude Code PreToolUse/PostToolUse JSON on stdin."
jqr() { printf '%s' "$IN" | jq -r "$1"; }
# Repo-relative path of the file an Edit/Write/MultiEdit/NotebookEdit call targets ("" if none).
rel_path() {
  local p; p="$(jqr '.tool_input.file_path // .tool_input.notebook_path // empty')"
  case "$p" in "$ROOT"/*) p="${p#"$ROOT"/}" ;; esac
  printf '%s' "$p"
}
log_verdict() { local rc=$?; local v=allow; [ "$rc" -eq 0 ] || v=block
  printf '%s %s %s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$HOOK" "$v" "$(rel_path)" >> "$ROOT/.claude/hooks.log" 2>/dev/null; }
trap log_verdict EXIT
