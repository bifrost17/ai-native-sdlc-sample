#!/bin/bash
# .claude/hooks/no-secrets.sh — PreToolUse(Edit|Write|MultiEdit|NotebookEdit)
# Playbook L7 line 521: "Keep credentials out of the diff"
# Looks only at the text being written (content / new_string / new_source), against six patterns.
# Fail-closed (no jq / bad JSON → exit 2), see _lib.sh.
. "${BASH_SOURCE[0]%/*}/_lib.sh"
text="$(jqr '.tool_input | [.content?, .new_string?, .new_source?, (.edits // [])[].new_string?] | map(select(. != null)) | join("\n")')"
[ -n "$text" ] || exit 0
PATTERNS='AKIA[0-9A-Z]{16}
-----BEGIN [A-Z ]*PRIVATE KEY-----
\bsk-[A-Za-z0-9_-]{20,}
\bgh[pousr]_[A-Za-z0-9]{36}
://[^/:@[:space:]]+:[^@[:space:]]+@
(password|passwd|secret|token|api_key)[[:space:]]*[=:][[:space:]]*["'"'"'][^"'"'"'$<{]{8,}["'"'"']'
hit="$(printf '%s\n' "$PATTERNS" | while IFS= read -r p; do
  printf '%s' "$text" | grep -Eiq -- "$p" && printf '%s\n' "$p"; done)"
[ -z "$hit" ] || block "the text being written looks like a credential (pattern: $hit). Reason: anything in the diff ends up in git history for everyone. Route: read the value from the environment or a secret store; if this is a documented placeholder, change it so it does not match the pattern."
exit 0
