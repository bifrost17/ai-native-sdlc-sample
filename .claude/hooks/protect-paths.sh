#!/bin/bash
# .claude/hooks/protect-paths.sh — PreToolUse(Edit|Write|MultiEdit|NotebookEdit)
# Playbook L7 line 517: "Block edits to protected paths such as generated classes or a frozen package"
# Protected here, a static list only: .github/**, Makefile, .claude/hooks/**, .claude/settings.json.
# No `status: accepted` branch: an accepted intent is the product owner's to re-read on the PR
# (L2 231 "recorded as the merge"), not a hook's — a hook that reads artifact status is the checker
# this repo decided not to build (docs/BOUNDARY.md).
# Fail-closed (no jq / bad JSON → exit 2), see _lib.sh.
. "${BASH_SOURCE[0]%/*}/_lib.sh"
set -f  # no filename globbing: the patterns below are matched by case, not expanded by the shell
PROTECTED='.github/* Makefile .claude/hooks/* .claude/settings.json'
rel="$(rel_path)"; [ -n "$rel" ] || exit 0
for pat in $PROTECTED; do
  case "$rel" in $pat)
    block "$rel is a frozen path ($PROTECTED). Reason: CI wiring, the make targets and the hooks are the feedback loop itself; an agent must not loosen them mid-task. Route: a human changes it in its own PR, or edits PROTECTED in this hook in that PR." ;;
  esac
done
exit 0
