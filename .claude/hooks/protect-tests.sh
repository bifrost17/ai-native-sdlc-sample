#!/bin/bash
# .claude/hooks/protect-tests.sh — PreToolUse(Edit|Write|MultiEdit|NotebookEdit)
# Playbook L9 line 631: "A hook that blocks edits to test files during a fix task does this"
# Playbook L12 line 809: "stop the agent editing test files during a fix task"
# "Fix task" = the environment variable INTENT_TASK=fix, set by whoever starts the session. Nothing else.
# Fail-closed (no jq / bad JSON → exit 2), see _lib.sh.
. "${BASH_SOURCE[0]%/*}/_lib.sh"
[ "${INTENT_TASK:-}" = "fix" ] || exit 0
rel="$(rel_path)"
case "$rel" in tests/*)
  block "$rel is a test file and INTENT_TASK=fix. Reason: the failing test committed before the fix is the proof the bug is gone; if the fix can rewrite it, it proves nothing. Route: fix the code, not the test. If the test itself is wrong, that is a separate task — start a session without INTENT_TASK=fix and say so in the PR." ;;
esac
exit 0
