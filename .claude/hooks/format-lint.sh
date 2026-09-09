#!/bin/bash
# .claude/hooks/format-lint.sh — PostToolUse(Edit|Write|MultiEdit|NotebookEdit)
# Playbook L7 line 519: "Run the formatter and linter after file edits so drift never accumulates"
# Scoped to the one file that changed: .py → py_compile, .sh → bash -n. Nothing more.
# exit 2 on PostToolUse feeds stderr back to Claude (the edit already happened; this is the loop, not a wall).
# Fail-closed (no jq / bad JSON → exit 2), see _lib.sh.
. "${BASH_SOURCE[0]%/*}/_lib.sh"
rel="$(rel_path)"; f="$ROOT/$rel"
[ -n "$rel" ] && [ -f "$f" ] || exit 0
case "$rel" in
  *.py) out="$(PYTHONPYCACHEPREFIX="${TMPDIR:-/tmp}/pycache" python3 -m py_compile "$f" 2>&1)" ;;
  *.sh) out="$(bash -n "$f" 2>&1)" ;;
  *) exit 0 ;;
esac
[ -z "$out" ] || block "$rel does not compile after this edit. Reason: drift must be fixed in the same step it appears. Route: fix the syntax error below and re-run; $out"
exit 0
