#!/usr/bin/env python3
"""Public transport only: pass one HUMAN prompt, preserve public events; no grading or follow-up."""
import argparse
import json
import os
import re
import subprocess
import threading
import time
from pathlib import Path

DROP = {"thinking", "signature", "reasoning", "reasoning_content", "encrypted_content", "redacted_thinking"}
PUBLIC = {"step_start", "step_finish", "text", "tool_use", "error"}

def clean(value):
    if isinstance(value, dict):
        if value.get("type") in DROP:
            return None
        return {k: clean(v) for k, v in value.items()
                if not (k in DROP or "signature" in k.lower() or "encrypted" in k.lower()
                        or k.lower().startswith("reasoning"))}
    if isinstance(value, list):
        return [clean(v) for v in value if not (isinstance(v, dict) and v.get("type") in DROP)]
    if isinstance(value, str):
        return re.sub(r"(?i)(bearer\s+)[A-Za-z0-9_.-]+", r"\1[REDACTED]", value)
    return value

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--cwd", required=True)
    p.add_argument("--prompt", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--model", default="opencode-go/gpt-5.6-luna")
    p.add_argument("--variant", default="medium")
    p.add_argument("--agent", default="build")
    p.add_argument("--session")
    p.add_argument("--timeout", type=int, default=600)
    a = p.parse_args()
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    if out.with_suffix(".jsonl").exists():
        raise SystemExit("Refusing to overwrite an existing turn")
    prompt = Path(a.prompt).read_text()
    cmd = ["opencode", "run", "--dir", a.cwd, "--format", "json", "--model", a.model, "--variant", a.variant, "--agent", a.agent]
    if a.session:
        cmd += ["--session", a.session]
    cmd += [prompt]
    start = time.time()
    env = dict(os.environ, PWD=str(Path(a.cwd).resolve()))
    process = subprocess.Popen(cmd, cwd=a.cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    errors = []
    def stderr_reader():
        for line in process.stderr:
            errors.append(clean(line))
    thread = threading.Thread(target=stderr_reader, daemon=True); thread.start()
    timed_out = []
    def stop():
        timed_out.append(True)
        process.terminate()
        try: process.wait(timeout=5)
        except subprocess.TimeoutExpired: process.kill()
    timer = threading.Timer(a.timeout, stop); timer.start()
    sessions = set(); counts = {}; dropped = {}; summaries = []; invalid = 0; errors_seen = 0
    try:
        with out.with_suffix(".jsonl").open("w") as sink:
            for line in process.stdout:
                try: event = json.loads(line)
                except json.JSONDecodeError:
                    invalid += 1
                    continue
                kind = event.get("type", "unknown")
                if kind not in PUBLIC:
                    dropped[kind] = dropped.get(kind, 0) + 1
                    continue
                event = clean(event)
                sink.write(json.dumps(event, ensure_ascii=False) + "\n"); sink.flush()
                counts[kind] = counts.get(kind, 0) + 1
                if event.get("sessionID"): sessions.add(event["sessionID"])
                part = event.get("part") or {}
                if kind == "step_finish": summaries.append(part)
                if kind == "error": errors_seen += 1
                if kind == "text": print(part.get("text", ""), flush=True)
                if kind == "tool_use": print("TOOL " + str(part.get("tool", "?")), flush=True)
                if kind == "error": print(json.dumps(event, ensure_ascii=False), flush=True)
        rc = process.wait()
    finally:
        timer.cancel()
        thread.join(timeout=2)
    out.with_suffix(".stderr.txt").write_text("".join(errors))
    meta = {"command": cmd[:-1] + ["<prompt-file>"], "prompt_path": a.prompt,
            "cwd": a.cwd, "model_requested": a.model, "variant_requested": a.variant,
            "session_requested": a.session, "session_ids": sorted(sessions),
            "started_unix": start, "elapsed_seconds": round(time.time()-start, 3),
            "exit_code": rc, "timed_out": bool(timed_out), "events": counts,
            "dropped_event_types": dropped, "invalid_line_count": invalid,
            "error_events": errors_seen, "step_finishes": summaries}
    out.with_suffix(".meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({k:v for k,v in meta.items() if k != "step_finishes"},ensure_ascii=False), flush=True)
    return rc or (1 if errors_seen or invalid or timed_out else 0)

if __name__ == "__main__":
    raise SystemExit(main())
