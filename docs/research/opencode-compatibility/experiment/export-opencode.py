#!/usr/bin/env python3
"""Export one OpenCode session as cleaned public JSON without storing raw output."""

import argparse
import errno
import importlib.util
import json
import os
import pty
import select
import subprocess
import time
from pathlib import Path


def load_clean():
    runner = Path(__file__).with_name("run-opencode.py")
    spec = importlib.util.spec_from_file_location("run_opencode", runner)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Could not load sanitizer: {runner}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.clean


def terminate(process):
    process.terminate()
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


def read_pty(command, cwd, timeout):
    master_fd, slave_fd = pty.openpty()
    env = dict(os.environ, PWD=str(cwd))
    try:
        process = subprocess.Popen(
            command,
            cwd=cwd,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=slave_fd,
            stderr=subprocess.PIPE,
        )
    finally:
        os.close(slave_fd)

    stdout = bytearray()
    streams = {master_fd: True}
    if process.stderr is not None:
        streams[process.stderr.fileno()] = False
    for fd in streams:
        os.set_blocking(fd, False)

    deadline = time.monotonic() + timeout
    drain_deadline = None
    timed_out = False
    try:
        while streams:
            now = time.monotonic()
            if process.poll() is None and now >= deadline:
                timed_out = True
                terminate(process)
                drain_deadline = time.monotonic() + 2
            elif process.poll() is not None and drain_deadline is None:
                drain_deadline = now + 2

            read_deadline = drain_deadline if drain_deadline is not None else deadline
            remaining = read_deadline - time.monotonic()
            if remaining <= 0:
                break

            readable, _, _ = select.select(list(streams), [], [], min(0.2, remaining))
            for fd in readable:
                try:
                    chunk = os.read(fd, 65536)
                except BlockingIOError:
                    continue
                except OSError as exc:
                    if fd == master_fd and exc.errno == errno.EIO:
                        chunk = b""
                    else:
                        raise
                if not chunk:
                    streams.pop(fd, None)
                elif streams[fd]:
                    stdout.extend(chunk)

        if process.poll() is None:
            remaining = deadline - time.monotonic()
            try:
                process.wait(timeout=max(0, remaining))
            except subprocess.TimeoutExpired:
                timed_out = True
                terminate(process)
    finally:
        os.close(master_fd)
        if process.stderr is not None:
            process.stderr.close()

    if timed_out:
        raise SystemExit(f"Export timed out after {timeout:g}s")
    if process.returncode:
        raise SystemExit(f"OpenCode export failed with exit code {process.returncode}")
    return bytes(stdout)


def main():
    parser = argparse.ArgumentParser(
        description="Export an OpenCode session and write only recursively cleaned JSON."
    )
    parser.add_argument("--cwd", required=True, help="OpenCode project directory")
    parser.add_argument("--session", required=True, help="completed OpenCode session ID")
    parser.add_argument("--out", required=True, help="new public JSON output path")
    parser.add_argument("--timeout", type=float, default=30, help="seconds (default: 30)")
    args = parser.parse_args()

    cwd = Path(args.cwd).expanduser().resolve()
    out = Path(args.out).expanduser().resolve()
    if not cwd.is_dir():
        raise SystemExit(f"Not a directory: {cwd}")
    if out.exists():
        raise SystemExit(f"Refusing to overwrite: {out}")
    if args.timeout <= 0:
        raise SystemExit("--timeout must be greater than zero")

    raw = read_pty(["opencode", "export", args.session], cwd, args.timeout)
    try:
        document = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"OpenCode export was not valid UTF-8 JSON: {exc}") from None

    cleaned = load_clean()(document)
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        with out.open("x", encoding="utf-8") as sink:
            json.dump(cleaned, sink, ensure_ascii=False, indent=2)
            sink.write("\n")
    except FileExistsError:
        raise SystemExit(f"Refusing to overwrite: {out}") from None
    print(f"Wrote cleaned public export: {out}")


if __name__ == "__main__":
    main()
