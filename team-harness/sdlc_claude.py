#!/usr/bin/env python3
# L4 329: "When implementation departs from the plan, update plan.md in the same commit."
# L9 650: verification before completion, "both implemented as hooks where the organization wants them guaranteed".

"""Small, stdlib-only Claude Code team harness with independent review."""

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import uuid


SCHEMA_VERSION = 1
DEFAULT_TIMEOUT = 180
MAX_REVIEW_BYTES = 8 * 1024 * 1024
MAX_FILE_BYTES = 1024 * 1024
MAX_AUTOMATIC_REVISIONS = 2
CHAIN_RE = re.compile(r"^intent/[0-9]{4}-[a-z0-9][a-z0-9-]*$")
PLUGIN_SETTINGS = {
    "disableAllHooks": True,
    "enabledPlugins": {
        "clangd-lsp@claude-plugins-official": False,
        "understand-anything@understand-anything": False,
        "intent-sdlc-skills@intent-sdlc-skills": False,
    },
}
EMPTY_MCP = {"mcpServers": {}}
DEVELOPER_TOOLS = "Read,Write,Edit,Glob,Grep,Bash,Skill"
DEVELOPER_ALLOWED = ",".join([
    "Read", "Write", "Edit", "Glob", "Grep", "Skill", "Bash(python3 *)",
    "Bash(git status)", "Bash(git status *)", "Bash(git diff)", "Bash(git diff *)",
    "Bash(git show)", "Bash(git show *)", "Bash(git log)", "Bash(git log *)",
    "Bash(git rev-parse)", "Bash(git rev-parse *)", "Bash(git ls-files)",
    "Bash(git ls-files *)", "Bash(ls)", "Bash(ls *)", "Bash(pwd)",
])
REVIEW_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "verdict": {"type": "string", "enum": ["pass", "revise", "wait", "unknown"]},
        "reason": {"type": "string"},
        "feedback": {"type": "string"},
    },
    "required": ["verdict", "reason", "feedback"],
}
DEVELOPER_SYSTEM = """You are the implementation member of a two-member team. Work on the user's
request in the current repository. Follow the repository's CLAUDE.md and chain artifacts. Keep
intent/spec/plan synchronized when the work changes their design. Run relevant verification before
claiming completion. Git commits, branch changes, pushes, merges, and other history mutations belong
to the HUMAN; do not perform them. This harness has disabled hooks to prevent recursive harness
invocation, so do not infer that a missing hook event is proof. Ask for a human decision in your
final response when one is actually required."""


class HarnessError(Exception):
    pass


def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def digest_bytes(value):
    return hashlib.sha256(value).hexdigest()


def json_bytes(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def git(project, *args):
    proc = subprocess.run(["git", *args], cwd=str(project), text=True, capture_output=True)
    if proc.returncode:
        raise HarnessError("git %s failed: %s" % (" ".join(args), proc.stderr.strip()))
    return proc.stdout


def within(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def checked_project_path(path, project, label):
    if path.is_symlink():
        raise HarnessError("symlink %s is unsupported: %s" % (label, path))
    try:
        resolved = path.resolve()
    except RuntimeError as exc:
        raise HarnessError("cannot resolve %s %s: %s" % (label, path, exc))
    if not within(resolved, project):
        raise HarnessError("unsafe %s: %s" % (label, path))
    return path


def resolve_inputs(project_arg, chain_arg, base_arg):
    project = Path(project_arg).expanduser().resolve()
    if not project.is_dir():
        raise HarnessError("project is not a directory: %s" % project)
    top = Path(git(project, "rev-parse", "--show-toplevel").strip()).resolve()
    if top != project:
        raise HarnessError("--project must be the Git worktree root: %s" % top)
    chain_text = chain_arg.rstrip("/")
    if not CHAIN_RE.fullmatch(chain_text):
        raise HarnessError("--chain must look like intent/NNNN-slug")
    chain = (project / chain_text).resolve()
    if not within(chain, project) or not chain.is_dir():
        raise HarnessError("chain directory does not exist: %s" % chain_text)
    base = git(project, "rev-parse", "--verify", "%s^{commit}" % base_arg).strip()
    return project, chain_text, base


def state_root():
    configured = os.environ.get("SDLC_HARNESS_STATE_ROOT")
    return Path(configured).expanduser() if configured else Path.home() / ".local/state/intent-sdlc-harness"


def read_bounded(path, label, budget):
    if path.is_symlink() or not path.is_file():
        raise HarnessError("unsupported %s: %s" % (label, path))
    size = path.stat().st_size
    if size > MAX_FILE_BYTES:
        raise HarnessError("%s exceeds %d bytes: %s" % (label, MAX_FILE_BYTES, path))
    raw = path.read_bytes()
    if b"\x00" in raw:
        raise HarnessError("binary %s is unsupported: %s" % (label, path))
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise HarnessError("non-UTF-8 %s is unsupported: %s" % (label, path))
    budget[0] += len(raw)
    if budget[0] > MAX_REVIEW_BYTES:
        raise HarnessError("review evidence exceeds %d bytes; no evidence was truncated" % MAX_REVIEW_BYTES)
    return text


def relevant_paths(project, chain_text):
    fixed = ["intent.md", "spec.md", "plan.md"]
    paths = [Path(chain_text) / name for name in fixed]
    candidates = git(project, "ls-files", "-co", "--exclude-standard", "-z").split("\0")
    names = {"CLAUDE.md", "REVIEW.md", "PROJECT-POLICY.md", "GIT-WORKFLOW.md", "PROCESS.md"}
    paths.extend(Path(item) for item in candidates if item and Path(item).name in names)
    unique = []
    for path in paths:
        if path not in unique and (project / path).exists():
            unique.append(path)
    return unique


def workspace_snapshot(project, chain_text, base):
    budget = [0]
    diff = git(project, "diff", "--no-ext-diff", "--no-textconv", base, "--")
    budget[0] += len(diff.encode("utf-8"))
    if budget[0] > MAX_REVIEW_BYTES:
        raise HarnessError("Git diff exceeds review evidence limit; no evidence was truncated")
    numstat = git(project, "diff", "--no-ext-diff", "--no-textconv", "--numstat", base, "--")
    if any(line.startswith("-\t-") for line in numstat.splitlines()):
        raise HarnessError("binary content in Git diff is unsupported")
    untracked = []
    for item in git(project, "ls-files", "--others", "--exclude-standard", "-z").split("\0"):
        if not item:
            continue
        path = checked_project_path(project / item, project, "untracked path")
        untracked.append({"path": item, "content": read_bounded(path, "untracked file", budget)})
    changed = []
    changed_names = git(project, "diff", "--no-ext-diff", "--no-textconv", "--name-only", "-z",
                        base, "--").split("\0")
    for item in changed_names:
        if not item:
            continue
        path = checked_project_path(project / item, project, "changed path")
        content = None if not path.exists() else read_bounded(path, "changed file", budget)
        changed.append({"path": item, "content": content})
    documents = []
    for relative in relevant_paths(project, chain_text):
        path = checked_project_path(project / relative, project, "project document")
        documents.append({"path": relative.as_posix(), "content": read_bounded(path, "project document", budget)})
    status = git(project, "status", "--short", "--untracked-files=all")
    snapshot = {
        "base_commit": base,
        "head_commit": git(project, "rev-parse", "HEAD").strip(),
        "status": status,
        "diff_from_base": diff,
        "changed_files": changed,
        "untracked_files": untracked,
        "documents": documents,
    }
    snapshot["digest"] = digest_bytes(json_bytes(snapshot))
    return snapshot


def sanitize(value):
    if isinstance(value, list):
        return [clean for item in value if (clean := sanitize(item)) is not None]
    if isinstance(value, dict):
        if value.get("type") in ("thinking", "redacted_thinking"):
            return None
        return {key: clean for key, item in value.items()
                if key not in ("thinking", "signature") and (clean := sanitize(item)) is not None}
    return value


def sanitize_event(event):
    if event.get("type") == "system" and event.get("subtype") == "init":
        keys = ("type", "subtype", "cwd", "session_id", "tools", "mcp_servers", "model",
                "permissionMode", "skills", "plugins", "plugin_errors", "mcp_server_errors",
                "claude_code_version", "output_style", "capabilities")
        return sanitize({key: event[key] for key in keys if key in event})
    return sanitize(event)


def save_stream(raw, path):
    events = []
    lines = []
    for number, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except ValueError as exc:
            raise HarnessError("developer stream line %d is not JSON: %s" % (number, exc))
        if not isinstance(event, dict):
            raise HarnessError("developer stream line %d is not an object" % number)
        clean = sanitize_event(event)
        if clean is not None:
            events.append(clean)
            lines.append(json.dumps(clean, ensure_ascii=False, separators=(",", ":")))
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return events


def successful_developer_result(events, expected_session):
    results = [event for event in events if event.get("type") == "result"]
    if len(results) != 1:
        raise HarnessError("developer stream must contain exactly one result event")
    result = results[0]
    if result.get("subtype") != "success" or result.get("is_error") is not False:
        raise HarnessError("developer returned an unsuccessful result")
    if result.get("session_id") != expected_session:
        raise HarnessError("developer session id does not match harness session")
    if not isinstance(result.get("result"), str):
        raise HarnessError("developer result text is missing")
    return result


def run_command(command, cwd, prompt, timeout):
    started = time.monotonic()
    try:
        proc = subprocess.run(command, cwd=str(cwd), input=prompt, text=True, capture_output=True,
                              timeout=timeout)
        return {"returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr,
                "timed_out": False, "elapsed_ms": round((time.monotonic() - started) * 1000)}
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", "replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", "replace")
        return {"returncode": None, "stdout": stdout, "stderr": stderr, "timed_out": True,
                "elapsed_ms": round((time.monotonic() - started) * 1000)}


def transport_record(run, command=None):
    """Return transport metadata without persisting a raw stream that may contain thinking."""
    record = {key: run.get(key) for key in
              ("returncode", "stderr", "timed_out", "elapsed_ms")}
    if command is not None:
        record["command"] = command
    return record


def developer_command(claude, session, resume):
    command = [claude, "-p", "--model", "sonnet", "--effort", "low",
               "--tools", DEVELOPER_TOOLS, "--allowedTools", DEVELOPER_ALLOWED,
               "--restricted",
               "--permission-mode", "acceptEdits", "--permission-prompts", "none",
               "--setting-sources", "project,local", "--settings", json.dumps(PLUGIN_SETTINGS),
               "--strict-mcp-config", "--mcp-config", json.dumps(EMPTY_MCP), "--no-chrome",
               "--append-system-prompt", DEVELOPER_SYSTEM,
               "--output-format", "stream-json", "--verbose"]
    command.extend(["--resume", session] if resume else ["--session-id", session])
    return command


def reviewer_command(claude, reviewer_prompt):
    return [claude, "-p", "--model", "sonnet", "--effort", "medium", "--tools", "",
            "--safe-mode", "--disable-slash-commands", "--restricted", "--strict-mcp-config",
            "--mcp-config", json.dumps(EMPTY_MCP), "--setting-sources", "",
            "--settings", json.dumps(PLUGIN_SETTINGS), "--no-session-persistence", "--no-chrome",
            "--permission-prompts", "none", "--system-prompt", reviewer_prompt,
            "--json-schema", json.dumps(REVIEW_SCHEMA), "--output-format", "json"]


def tool_blocks(event):
    message = event.get("message") if isinstance(event, dict) else None
    content = message.get("content", []) if isinstance(message, dict) else []
    return content if isinstance(content, list) else []


def project_tool_evidence(events):
    uses, results = {}, {}
    for event in events:
        for block in tool_blocks(event):
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use" and isinstance(block.get("id"), str):
                uses[block["id"]] = block
            elif block.get("type") == "tool_result" and isinstance(block.get("tool_use_id"), str):
                results[block["tool_use_id"]] = block
    projected = []
    for tool_id, use in uses.items():
        name = use.get("name") if isinstance(use.get("name"), str) else "unknown"
        inputs = use.get("input") if isinstance(use.get("input"), dict) else {}
        if name == "Bash":
            selected_input = {key: inputs[key] for key in ("command", "timeout", "description")
                              if key in inputs}
        else:
            selected_input = {key: inputs[key] for key in
                              ("file_path", "path", "pattern", "glob", "skill") if key in inputs}
        result = results.get(tool_id)
        status = "missing" if result is None else "error" if result.get("is_error") is True else "success"
        item = {"tool_use_id": tool_id, "name": name, "input": selected_input, "status": status}
        if name == "Bash" and result is not None:
            item["result"] = {key: result[key] for key in
                              ("content", "is_error", "stdout", "stderr", "exit_code") if key in result}
        projected.append(item)
    return projected


def load_turns(session_dir):
    turns = []
    turn_dirs = sorted(session_dir.glob("turn[0-9][0-9]"))
    for turn_dir in turn_dirs:
        input_path, stream_path = turn_dir / "input.json", turn_dir / "development-stream.jsonl"
        summary_path = turn_dir / "summary.json"
        if not input_path.is_file() or (not stream_path.is_file() and not summary_path.is_file()):
            raise HarnessError("incomplete saved turn: %s" % turn_dir.name)
        item = json.loads(input_path.read_text(encoding="utf-8"))
        summary = (json.loads(summary_path.read_text(encoding="utf-8"))
                   if summary_path.is_file() else {"verdict": "pending_review"})
        stream_bytes = stream_path.read_bytes() if stream_path.is_file() else b""
        events = [json.loads(line) for line in stream_bytes.decode("utf-8").splitlines()
                  if line.strip()]
        final_results = [event.get("result") for event in events
                         if event.get("type") == "result" and isinstance(event.get("result"), str)]
        final_claim = final_results[-1] if final_results else None
        is_current = turn_dir == turn_dirs[-1]
        reference_path = stream_path if stream_path.is_file() else turn_dir / "development-transport.json"
        reference_bytes = (stream_bytes if stream_path.is_file() else
                           reference_path.read_bytes() if reference_path.is_file() else b"")
        outcome = {key: summary[key] for key in ("turn", "kind", "verdict", "finished_at")
                   if key in summary}
        outcome["execution_failed"] = summary.get("verdict") == "unknown"
        if isinstance(summary.get("failure_reason"), str):
            outcome["failure_reason"] = summary["failure_reason"]
        projected = {"turn": item.get("turn"), "kind": item.get("kind"),
                     "prompt": item.get("prompt"), "tool_evidence": project_tool_evidence(events),
                     "recorded_outcome": outcome,
                     "source_log": {"path": str(reference_path.relative_to(session_dir)),
                                    "sha256": digest_bytes(reference_bytes)}}
        if is_current:
            projected["current_final_claim"] = final_claim
        elif summary.get("verdict") == "wait" and final_claim is not None:
            projected["human_decision_context"] = final_claim
        elif final_claim is not None:
            projected["superseded_final_claim_sha256"] = digest_bytes(final_claim.encode("utf-8"))
        turns.append(projected)
    return turns


def make_review_packet(session_dir, metadata, snapshot):
    turns = load_turns(session_dir)
    packet = {
        "schema_version": SCHEMA_VERSION,
        "purpose": "Independent semantic review of current SDLC work",
        "session": {key: metadata[key] for key in ("session_id", "project", "chain", "base_commit")},
        "human_conversation": [
            {"turn": item["turn"], "prompt": item["prompt"]}
            for item in turns if item["kind"] == "human"
        ],
        "developer_turns": turns,
        "workspace": snapshot,
        "evidence_rules": {
            "developer_final_is_untrusted": True,
            "tool_results_are_execution_evidence": True,
            "logs_are_outside_project": True,
            "evidence_was_not_truncated": True,
            "workspace_snapshot_is_authoritative_for_current_file_content": True,
            "prior_final_claim_text_is_omitted_as_superseded": True,
            "prior_wait_text_is_preserved_only_as_human_decision_context": True,
            "read_edit_write_bodies_are_omitted_to_avoid_stale_file_content": True,
            "bash_commands_and_results_are_preserved_as_historical_execution_evidence": True,
            "source_log_paths_and_hashes_identify_the_complete_preserved_public_records": True,
        },
    }
    if len(json_bytes(packet)) > MAX_REVIEW_BYTES:
        raise HarnessError("cumulative review input exceeds %d bytes; no evidence was truncated" % MAX_REVIEW_BYTES)
    return packet


def parse_reviewer(run, developer_session):
    if run["timed_out"]:
        raise HarnessError("reviewer timed out")
    if run["returncode"] != 0:
        raise HarnessError("reviewer exited %s" % run["returncode"])
    try:
        envelope = json.loads(run["stdout"])
    except ValueError as exc:
        raise HarnessError("reviewer output is not JSON: %s" % exc)
    if not isinstance(envelope, dict) or envelope.get("subtype") != "success" or \
            envelope.get("is_error") is not False or envelope.get("status") not in (None, "success"):
        raise HarnessError("reviewer returned an unsuccessful envelope")
    reviewer_session = envelope.get("session_id")
    if not isinstance(reviewer_session, str) or not reviewer_session:
        raise HarnessError("reviewer session id is missing")
    if reviewer_session == developer_session:
        raise HarnessError("reviewer is not an independent session")
    output = envelope.get("structured_output")
    if not isinstance(output, dict) or output.get("verdict") not in REVIEW_SCHEMA["properties"]["verdict"]["enum"]:
        raise HarnessError("reviewer structured_output is malformed")
    if set(output) != {"verdict", "reason", "feedback"} or not all(
            isinstance(output[key], str) for key in ("reason", "feedback")):
        raise HarnessError("reviewer structured_output fields are malformed")
    if not output["reason"].strip():
        raise HarnessError("reviewer reason is empty")
    return envelope, output


def update_session_summary(session_dir, metadata):
    summaries = []
    for path in sorted(session_dir.glob("turn[0-9][0-9]/summary.json")):
        summaries.append(json.loads(path.read_text(encoding="utf-8")))
    write_json(session_dir / "summary.json", {
        "schema_version": SCHEMA_VERSION,
        "session_id": metadata["session_id"],
        "project": metadata["project"],
        "chain": metadata["chain"],
        "base_commit": metadata["base_commit"],
        "reviewer_prompt_sha256": metadata["reviewer_prompt_sha256"],
        "runtime_sha256": metadata["runtime_sha256"],
        "turns": summaries,
        "updated_at": utc_now(),
    })


def record_failure(turn_dir, metadata, kind, reason, run=None, command=None):
    result = {"schema_version": SCHEMA_VERSION, "verdict": "unknown", "reason": reason,
              "feedback": "Review the saved evidence and continue with --resume %s." % metadata["session_id"]}
    write_json(turn_dir / "review-result.json", {
        "transport": transport_record(run, command) if run is not None else None, "error": reason})
    summary = {"turn": int(turn_dir.name[4:]), "kind": kind, "verdict": "unknown",
               "reason": reason, "failure_reason": reason,
               "reviewer_prompt_sha256": metadata["reviewer_prompt_sha256"],
               "runtime_sha256": metadata["runtime_sha256"], "finished_at": utc_now()}
    write_json(turn_dir / "summary.json", summary)
    update_session_summary(turn_dir.parent, metadata)
    print("unknown: %s" % reason)
    print("Handoff: inspect %s and resume with --resume %s." % (turn_dir, metadata["session_id"]))
    return 2


def create_or_resume(args, project, chain, base):
    root = state_root()
    root.mkdir(parents=True, exist_ok=True)
    if args.resume:
        try:
            uuid.UUID(args.resume)
        except ValueError:
            raise HarnessError("--resume must be a UUID")
        session_dir = root / args.resume
        metadata_path = session_dir / "session.json"
        if not metadata_path.is_file():
            raise HarnessError("saved session does not exist: %s" % args.resume)
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        expected = {"project": str(project), "chain": chain, "base_commit": base,
                    "session_id": args.resume}
        if any(metadata.get(key) != value for key, value in expected.items()):
            raise HarnessError("resume project, chain, or base does not match the saved session")
        return session_dir, metadata, True
    session = str(uuid.uuid4())
    session_dir = root / session
    session_dir.mkdir(parents=False, exist_ok=False)
    metadata = {"schema_version": SCHEMA_VERSION, "session_id": session,
                "project": str(project), "chain": chain, "base_commit": base,
                "created_at": utc_now(), "model": "sonnet", "effort": "low", "reviewer_effort": "medium",
                "max_automatic_revisions_per_human_turn": MAX_AUTOMATIC_REVISIONS}
    write_json(session_dir / "session.json", metadata)
    return session_dir, metadata, False


def execute(args):
    project, chain, base = resolve_inputs(args.project, args.chain, args.base)
    claude = shutil.which("claude")
    if not claude:
        raise HarnessError("claude executable was not found on PATH")
    reviewer_path = Path(__file__).with_name("reviewer.md")
    if not reviewer_path.is_file():
        raise HarnessError("reviewer prompt is missing: %s" % reviewer_path)
    reviewer_bytes = reviewer_path.read_bytes()
    try:
        reviewer_prompt = reviewer_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise HarnessError("reviewer prompt is not UTF-8: %s" % reviewer_path)
    session_dir, metadata, resuming = create_or_resume(args, project, chain, base)
    metadata["reviewer_prompt_sha256"] = digest_bytes(reviewer_bytes)
    metadata["runtime_sha256"] = digest_bytes(Path(__file__).read_bytes())
    metadata["reviewer_effort"] = "medium"
    write_json(session_dir / "session.json", metadata)
    original_prompt = sys.stdin.read()
    if not original_prompt:
        raise HarnessError("read an empty user prompt from stdin")
    next_turn = len(list(session_dir.glob("turn[0-9][0-9]"))) + 1
    automatic_revisions = 0
    prompt, kind = original_prompt, "human"

    while True:
        turn_dir = session_dir / ("turn%02d" % next_turn)
        turn_dir.mkdir(parents=True, exist_ok=False)
        input_record = {"schema_version": SCHEMA_VERSION, "turn": next_turn, "kind": kind,
                        "prompt": prompt, "input_digest": digest_bytes(prompt.encode("utf-8")),
                        "received_at": utc_now(), "automatic_revision_index": automatic_revisions}
        write_json(turn_dir / "input.json", input_record)
        (turn_dir / "reviewer-instructions.md").write_bytes(reviewer_bytes)
        print("[%s] development turn %02d" % (metadata["session_id"], next_turn), file=sys.stderr)
        dev_command = developer_command(claude, metadata["session_id"], resuming or next_turn > 1)
        dev_run = run_command(dev_command, project, prompt, args.timeout)
        write_json(turn_dir / "development-transport.json", transport_record(dev_run, dev_command))
        if dev_run["timed_out"]:
            return record_failure(turn_dir, metadata, kind, "developer timed out", dev_run, dev_command)
        if dev_run["returncode"] != 0:
            return record_failure(turn_dir, metadata, kind,
                                  "developer exited %s" % dev_run["returncode"], dev_run, dev_command)
        try:
            events = save_stream(dev_run["stdout"], turn_dir / "development-stream.jsonl")
            dev_result = successful_developer_result(events, metadata["session_id"])
            snapshot = workspace_snapshot(project, chain, base)
            packet = make_review_packet(session_dir, metadata, snapshot)
        except (HarnessError, OSError, ValueError) as exc:
            return record_failure(turn_dir, metadata, kind, str(exc))
        write_json(turn_dir / "review-input.json", packet)
        print("[%s] independent review turn %02d" % (metadata["session_id"], next_turn), file=sys.stderr)
        review_command = reviewer_command(claude, reviewer_prompt)
        review_run = run_command(review_command, project, json.dumps(packet, ensure_ascii=False),
                                 args.timeout)
        try:
            envelope, verdict = parse_reviewer(review_run, metadata["session_id"])
            after = workspace_snapshot(project, chain, base)
            if after["digest"] != snapshot["digest"]:
                raise HarnessError("workspace changed during review; verdict is stale")
        except (HarnessError, OSError, ValueError) as exc:
            return record_failure(turn_dir, metadata, kind, str(exc), review_run, review_command)
        write_json(turn_dir / "review-result.json", {"transport": transport_record(review_run, review_command),
            "envelope": envelope, "verdict": verdict})
        summary = {
            "schema_version": SCHEMA_VERSION, "turn": next_turn, "kind": kind,
            "input_digest": input_record["input_digest"], "base_commit": base,
            "review_input_digest": digest_bytes(json_bytes(packet)),
            "reviewer_prompt_sha256": metadata["reviewer_prompt_sha256"],
            "runtime_sha256": metadata["runtime_sha256"],
            "head_commit": snapshot["head_commit"], "workspace_digest": snapshot["digest"],
            "developer": {key: dev_result.get(key) for key in
                          ("session_id", "total_cost_usd", "duration_ms", "duration_api_ms",
                           "num_turns", "usage", "modelUsage") if key in dev_result},
            "developer_elapsed_ms": dev_run["elapsed_ms"],
            "reviewer": {key: envelope.get(key) for key in
                         ("session_id", "total_cost_usd", "duration_ms", "duration_api_ms",
                          "num_turns", "usage", "modelUsage") if key in envelope},
            "reviewer_elapsed_ms": review_run["elapsed_ms"], "verdict": verdict["verdict"],
            "reason": verdict["reason"], "finished_at": utc_now(),
        }
        write_json(turn_dir / "summary.json", summary)
        update_session_summary(session_dir, metadata)

        if verdict["verdict"] in ("pass", "wait"):
            print(dev_result["result"])
            print("Review: %s — %s" % (verdict["verdict"], verdict["reason"]))
            if verdict["verdict"] == "wait" and verdict["feedback"].strip():
                print("Needed from HUMAN: %s" % verdict["feedback"])
            print("Session: %s" % metadata["session_id"])
            return 0
        if verdict["verdict"] == "unknown":
            print(dev_result["result"])
            print("unknown: %s" % verdict["reason"])
            print("Handoff: inspect %s and resume with --resume %s." %
                  (turn_dir, metadata["session_id"]))
            return 2
        if automatic_revisions >= MAX_AUTOMATIC_REVISIONS:
            print(dev_result["result"])
            print("unresolved after %d automatic revisions: %s" %
                  (MAX_AUTOMATIC_REVISIONS, verdict["reason"]))
            print("Handoff: inspect %s and resume with --resume %s." %
                  (turn_dir, metadata["session_id"]))
            return 2
        automatic_revisions += 1
        prompt = ("Independent reviewer feedback for automatic revision %d/%d. This is reviewer "
                  "feedback, not a new HUMAN request. Correct the current work, rerun relevant "
                  "verification, and report the current result.\n\nReason: %s\n\nFeedback: %s" %
                  (automatic_revisions, MAX_AUTOMATIC_REVISIONS,
                   verdict["reason"], verdict["feedback"]))
        kind = "reviewer_feedback"
        next_turn += 1
        resuming = True


def main(argv=None):
    parser = argparse.ArgumentParser(description="run Claude Code with an independent SDLC reviewer")
    parser.add_argument("--project", required=True)
    parser.add_argument("--chain", required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--resume")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                        help="per Claude invocation timeout in seconds (default: 180)")
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    try:
        return execute(args)
    except (HarnessError, OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print("sdlc-claude: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
