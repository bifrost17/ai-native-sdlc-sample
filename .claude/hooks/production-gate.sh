#!/bin/bash
# .claude/hooks/production-gate.sh — PreToolUse(Bash)
# Playbook L12 lines 848~857, the playbook example itself:
#   "# Production deploys require a named release authorization
#    cmd=$(jq -r '.tool_input.command' < /dev/stdin)
#    if [[ "$cmd" == *"deploy"* && "$cmd" == *"production"* ]]; then
#      if [ -z "$RELEASE_APPROVAL" ]; then
#        echo "Production deploys need a release authorization." >&2
#        exit 2 # exit 2 blocks the action; the message goes to Claude"
# Playbook L12 line 825: "A block should explain itself" — the block names the route to approval.
# Approval = the environment variable RELEASE_APPROVAL, set by the release manager outside the session.
# Fail-closed (no jq / bad JSON → exit 2), see _lib.sh.
. "${BASH_SOURCE[0]%/*}/_lib.sh"
# TEAM: real approval process behind this gate — docs/ADOPTING.md · L18
cmd="$(jqr '.tool_input.command // empty')"
if [[ "$cmd" == *"deploy"* && "$cmd" == *"production"* ]]; then
  if [ -z "${RELEASE_APPROVAL:-}" ]; then
    block "Production deploys need a release authorization. Reason: the agent may reach the production gate but not pass it on its own. Route: the release manager sets RELEASE_APPROVAL=<change ticket id> in the session environment, then rerun the command."
  fi
fi
exit 0
