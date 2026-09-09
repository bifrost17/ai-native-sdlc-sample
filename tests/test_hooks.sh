#!/bin/bash
# tests/test_hooks.sh — per hook: one positive control (a planted violation exits 2 and the
# stderr names a Route: to approval — playbook L12 line 825 "A block should explain itself")
# and one negative control (a normal edit exits 0); plus the settings.json wiring check
# (the #1 failure of the reference repos: hooks present, never wired). bash 3.2.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
T="$(mktemp -d "${TMPDIR:-/tmp}/hooktest.XXXXXX")"; T="$(cd "$T" && pwd -P)"; trap 'rm -rf "$T"' EXIT INT TERM
mkdir -p "$T/.claude" && cp -R "$ROOT/.claude/hooks" "$T/.claude/hooks"
H="$T/.claude/hooks"
mkdir -p "$T/intent/0001-a" "$T/intent/0002-b" "$T/.github/workflows" "$T/tests" "$T/src"
printf -- '---\nid: 0001-a\nstatus: accepted\n---\n# a\n' > "$T/intent/0001-a/intent.md"
printf -- '---\nid: 0002-b\nstatus: draft\n---\n# b\n'    > "$T/intent/0002-b/intent.md"
printf 'def ok():\n    return 1\n' > "$T/src/ok.py"
printf 'def bad(:\n'               > "$T/src/bad.py"
printf '#!/bin/bash\necho ok\n'    > "$T/src/ok.sh"
printf '#!/bin/bash\nif [ x ; then\n' > "$T/src/bad.sh"

PASS=0; FAIL=0
edit()    { printf '{"tool_name":"Edit","tool_input":{"file_path":"%s/%s","old_string":"a","new_string":"%s"},"cwd":"%s"}' "$T" "$1" "${2:-b}" "$T"; }
bashcmd() { printf '{"tool_name":"Bash","tool_input":{"command":"%s"},"cwd":"%s"}' "$1" "$T"; }
# run <name> <want rc> <hook> <stdin json> [env args...]   (a block must say "Route:")
run() {
  local name="$1" want="$2" hook="$3" json="$4" err rc; shift 4
  err="$(printf '%s' "$json" | env "$@" /bin/bash "$H/$hook" 2>&1 >/dev/null)"; rc=$?
  if [ "$rc" -eq "$want" ] && { [ "$want" -ne 2 ] || printf '%s' "$err" | grep -q 'Route:'; }; then
    PASS=$((PASS+1)); echo "ok   $name (rc=$rc)"
  else
    FAIL=$((FAIL+1)); echo "FAIL $name (want rc=$want, got rc=$rc)"; printf '%s\n' "$err" | sed 's/^/     /'
  fi
}

# protect-paths — L7 517
run "protect-paths: accepted intent blocked"   2 protect-paths.sh "$(edit intent/0001-a/intent.md)"
run "protect-paths: .github blocked"           2 protect-paths.sh "$(edit .github/workflows/ci.yml)"
run "protect-paths: Makefile blocked"          2 protect-paths.sh "$(edit Makefile)"
run "protect-paths: draft intent passes"       0 protect-paths.sh "$(edit intent/0002-b/intent.md)"
run "protect-paths: src file passes"           0 protect-paths.sh "$(edit src/ok.py)"
# protect-tests — L9 631 · L12 809
run "protect-tests: fix task, test file blocked" 2 protect-tests.sh "$(edit tests/test_x.py)" INTENT_TASK=fix
run "protect-tests: fix task, src passes"        0 protect-tests.sh "$(edit src/ok.py)"      INTENT_TASK=fix
run "protect-tests: no fix task, test passes"    0 protect-tests.sh "$(edit tests/test_x.py)" -u INTENT_TASK
# no-secrets — L7 521
run "no-secrets: AWS key blocked"   2 no-secrets.sh "$(edit src/cfg.py 'KEY = \"AKIAIOSFODNN7EXAMPLE\"')"
run "no-secrets: password literal blocked" 2 no-secrets.sh "$(edit src/cfg.py 'password = \"hunter2hunter2\"')"
run "no-secrets: plain edit passes" 0 no-secrets.sh "$(edit src/cfg.py 'password = os.environ[\"PW\"]')"
# format-lint — L7 519 (PostToolUse; exit 2 feeds stderr back to Claude)
run "format-lint: broken .py reported" 2 format-lint.sh "$(edit src/bad.py)"
run "format-lint: broken .sh reported" 2 format-lint.sh "$(edit src/bad.sh)"
run "format-lint: valid .py passes"    0 format-lint.sh "$(edit src/ok.py)"
run "format-lint: valid .sh passes"    0 format-lint.sh "$(edit src/ok.sh)"
# production-gate — L12 848~857
run "production-gate: unapproved prod deploy blocked" 2 production-gate.sh "$(bashcmd 'scripts/deploy.sh production')" -u RELEASE_APPROVAL
run "production-gate: approved prod deploy passes"    0 production-gate.sh "$(bashcmd 'scripts/deploy.sh production')" RELEASE_APPROVAL=CHG-42
run "production-gate: staging deploy passes"          0 production-gate.sh "$(bashcmd 'scripts/deploy.sh staging')"    -u RELEASE_APPROVAL
# fail-closed — no jq / broken JSON must block, never silently pass
run "fail-closed: broken JSON blocks" 2 protect-paths.sh '{not json'
run "fail-closed: no jq blocks"       2 production-gate.sh "$(bashcmd 'ls')" PATH=/nonexistent

# wiring — every hook is referenced from .claude/settings.json, which must be valid JSON
S="$ROOT/.claude/settings.json"
if python3 -m json.tool "$S" >/dev/null 2>&1; then PASS=$((PASS+1)); echo "ok   wiring: settings.json is valid JSON"
else FAIL=$((FAIL+1)); echo "FAIL wiring: settings.json is not valid JSON"; fi
for h in protect-paths protect-tests no-secrets format-lint production-gate; do
  if grep -q "hooks/$h.sh" "$S" && [ -x "$ROOT/.claude/hooks/$h.sh" ]; then PASS=$((PASS+1)); echo "ok   wiring: $h.sh wired and executable"
  else FAIL=$((FAIL+1)); echo "FAIL wiring: $h.sh not wired in settings.json or not executable"; fi
done

echo "test_hooks: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
