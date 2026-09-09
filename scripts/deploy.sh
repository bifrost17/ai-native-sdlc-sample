#!/usr/bin/env bash
# scripts/deploy.sh — the deploy target that .claude/hooks/production-gate.sh guards. It deploys nothing.
# L12 line 855: `if [ -z "$RELEASE_APPROVAL" ]; then` — approval is checked by the hook before this
# runs, never in here (a target that checks itself can be bypassed by a path that skips the target).
echo "deploy.sh: args = $*  (stub — no real deploy target in this sample)"
exit 0
