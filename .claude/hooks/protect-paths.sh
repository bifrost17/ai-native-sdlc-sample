#!/bin/bash
# .claude/hooks/protect-paths.sh — PreToolUse(Edit|Write|MultiEdit|NotebookEdit)
# Playbook L7 line 517: "Block edits to protected paths such as generated classes or a frozen package"
# Protected in this repo: intent/** files whose frontmatter says `status: accepted`, .github/**, Makefile.
# Fail-closed (no jq / bad JSON → exit 2), see _lib.sh.
. "${BASH_SOURCE[0]%/*}/_lib.sh"
set -f  # no filename globbing: the patterns below are matched by case, not expanded by the shell
PROTECTED='.github/* Makefile'
rel="$(rel_path)"; [ -n "$rel" ] || exit 0
for pat in $PROTECTED; do
  case "$rel" in $pat)
    block "$rel is a frozen path ($PROTECTED). Reason: CI wiring and the make targets are the feedback loop itself; an agent must not loosen them mid-task. Route: a human changes it in its own PR, or edits PROTECTED in this hook in that PR." ;;
  esac
done
case "$rel" in intent/*)
  if [ -f "$ROOT/$rel" ] && sed -n '2,/^---$/p' "$ROOT/$rel" | grep -q '^status:[[:space:]]*accepted'; then
    block "$rel has status: accepted and accepted artifacts are frozen. Reason: git is the audit trail of what was approved. Route: write a new intent that names supersedes: $rel, or have the product owner note in-place approval in the PR body and drop the file from this hook's scope for that PR."
  fi ;;
esac
exit 0
