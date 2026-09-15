#!/bin/bash
# .claude/hooks/_lib.sh — shared by the five hooks; not a hook itself.
# Decision: fail-closed. No jq, or stdin that is not JSON → exit 2 (block). "Unknown" is not "clean";
# the reference repos that did `|| exit 0` here silently switched their guardrails off.
# L12 866행: "Allow and block decisions are logged with a timestamp." L12 934행 (OTel export) is
# outside this repo's tree — logged here as a local file only.
HOOK="${0##*/}"
block() { printf '[%s] BLOCKED: %s\n' "$HOOK" "$*" >&2; exit 2; }
ROOT="$(cd "${BASH_SOURCE[0]%/*}/../.." && pwd -P)" || block "repository root cannot be resolved. Route: restore the hook directory and retry."
command -v jq >/dev/null 2>&1 || block "jq not found, so the hook input cannot be parsed and the action is refused. Route: install jq (brew install jq / apt-get install jq) and retry."
IN="$(cat)"
printf '%s' "$IN" | jq -e . >/dev/null 2>&1 || block "hook input is not valid JSON; refused. Route: run the hook with a Claude Code PreToolUse/PostToolUse JSON on stdin."
jqr() { printf '%s' "$IN" | jq -r "$1"; }
# L7 517: "Block edits to protected paths" includes aliases of the actual destination.
# Resolve once, before any verdict. Keep lexical destinations at every symlink expansion:
# a protected path stays protected even if its link points outside the repository.
PATH_REL=""; PATH_CANDIDATES=""; TARGET_PATH=""
rel_path() { printf '%s' "$PATH_REL"; }
log_verdict() { local rc=$?; local v=allow; [ "$rc" -eq 0 ] || v=block
  printf '%s %s %s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$HOOK" "$v" "$(rel_path)" >> "$ROOT/.claude/hooks.log" 2>/dev/null; }
trap log_verdict EXIT
command -v python3 >/dev/null 2>&1 || block "python3 not found, so file paths cannot be resolved. Route: install python3 and retry."
PATH_DATA="$(printf '%s' "$IN" | python3 -c '
import collections
import json
import os
import stat
import sys
import unicodedata

def path_string(value):
    if not isinstance(value, str) or not value:
        raise ValueError("paths must be nonempty strings")
    if any(ord(char) < 32 or ord(char) == 127 or 0xD800 <= ord(char) <= 0xDFFF for char in value):
        raise ValueError("paths must not contain control characters or invalid Unicode")
    return value

directory_entries = {}

def component_name(parent, name, metadata):
    # The filesystem decides whether case variants alias. Never lowercase Linux
    # paths: exact directory entries remain distinct even when casefold matches.
    if parent not in directory_entries:
        directory_entries[parent] = os.listdir(parent)
    entries = directory_entries[parent]
    if name in entries:
        return name
    folded = unicodedata.normalize("NFD", name).casefold()
    for entry in entries:
        if unicodedata.normalize("NFD", entry).casefold() == folded:
            # lstat identity also covers dangling links, without following them.
            if os.path.samestat(metadata, os.lstat(os.path.join(parent, entry))):
                return path_string(entry)
    raise ValueError("an existing path has no matching directory entry")

def resolve(path, allow_missing, candidates):
    # Walk before collapsing ..: link/.. follows the link, then its real parent.
    pending = collections.deque(path.split("/"))
    current = "/"
    links = 0
    candidates.append(os.path.normpath(path))
    while pending:
        part = pending.popleft()
        if part in ("", "."):
            continue
        if part == "..":
            current = os.path.dirname(current)
            continue
        target = os.path.join(current, part)
        try:
            metadata = os.lstat(target)
        except FileNotFoundError:
            if not allow_missing:
                raise
            # Write can create a file and parents. Still inspect later components
            # after .. returns to an existing ancestor; other OS errors propagate.
            current = target
            continue
        canonical = component_name(current, part, metadata)
        if canonical != part:
            target = os.path.join(current, canonical)
            candidates.append(os.path.normpath(os.path.join(target, *pending)))
        mode = metadata.st_mode
        if stat.S_ISLNK(mode):
            links += 1
            if links > 40:
                raise ValueError("too many symbolic links or a symbolic-link loop")
            link = path_string(os.readlink(target))
            if os.path.isabs(link):
                current = "/"
            pending.extendleft(reversed(link.split("/")))
            candidates.append(os.path.normpath(os.path.join(current, *pending)))
        else:
            if pending and not stat.S_ISDIR(mode):
                raise ValueError("a path ancestor is not a directory")
            current = target
    candidates.append(current)
    return current

try:
    payload = json.load(sys.stdin)
    if not isinstance(payload, dict) or not isinstance(payload.get("tool_input"), dict):
        raise ValueError("hook input and tool_input must be objects")
    tool_input = payload["tool_input"]
    fields = [field for field in ("file_path", "notebook_path") if field in tool_input]
    if not fields:
        if payload.get("tool_name") in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
            raise ValueError("file-edit input has no target path")
        print(json.dumps({"target": "", "rel": "", "paths": []}))
        sys.exit(0)
    cwd = path_string(payload["cwd"] if "cwd" in payload else os.getcwd())
    if not os.path.isabs(cwd):
        raise ValueError("cwd must be absolute")
    actual_cwd = resolve(cwd, False, [])
    if not stat.S_ISDIR(os.stat(actual_cwd).st_mode):
        raise ValueError("cwd is not a directory")
    candidates = []
    targets = []
    for field in fields:
        path = path_string(tool_input[field])
        targets.append(resolve(os.path.join(cwd, path), True, candidates))
    if len(set(targets)) != 1:
        raise ValueError("file_path and notebook_path identify different destinations")
    root = resolve(sys.argv[1], False, [])
    def relative(path):
        return os.path.relpath(path, root) if path == root or path.startswith(root + "/") else path
    print(json.dumps({"target": targets[0], "rel": relative(targets[0]),
                      "paths": list(dict.fromkeys(relative(path) for path in candidates))}))
except (OSError, ValueError, TypeError) as error:
    print("Path resolution failed: " + str(error), file=sys.stderr)
    sys.exit(1)
' "$ROOT")" || block "file target cannot be resolved safely. Route: provide a valid file path and absolute existing cwd, repair inaccessible paths or symbolic links, then retry."
TARGET_PATH="$(printf '%s' "$PATH_DATA" | jq -er '.target')" || block "resolved target cannot be read. Route: repair the hook input or resolver and retry."
PATH_REL="$(printf '%s' "$PATH_DATA" | jq -er '.rel')" || block "resolved path cannot be read. Route: repair the hook input or resolver and retry."
PATH_CANDIDATES="$(printf '%s' "$PATH_DATA" | jq -r '.paths[]')" || block "resolved paths cannot be read. Route: repair the hook input or resolver and retry."
