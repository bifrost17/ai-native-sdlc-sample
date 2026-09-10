#!/usr/bin/env python3
# L4 329: "When implementation departs from the plan, update plan.md in the same commit."
# L9 650: verification before completion, "both implemented as hooks where the organization wants them guaranteed".

"""Install the team harness without changing shell or Claude configuration."""

import argparse
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile


RUNTIME_FILES = ("sdlc_claude.py", "reviewer.md")
MARKER = "# intent-sdlc-harness managed entrypoint\n"
RUNTIME_MARKERS = {
    "sdlc_claude.py": "Small, stdlib-only Claude Code team harness",
    "reviewer.md": "# Independent SDLC review",
}


def managed_entrypoint(runtime):
    return ("#!/usr/bin/env python3\n" + MARKER + "import runpy\n" +
            "runpy.run_path(%r, run_name='__main__')\n" % str(runtime / "sdlc_claude.py"))


def copy_atomic(source, target):
    descriptor, name = tempfile.mkstemp(prefix=".intent-sdlc-harness-", dir=str(target.parent))
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as output, source.open("rb") as source_stream:
            shutil.copyfileobj(source_stream, output)
        temporary.chmod(source.stat().st_mode)
        os.replace(str(temporary), str(target))
    finally:
        if temporary.exists():
            temporary.unlink()


def write_atomic(target, content, mode):
    descriptor, name = tempfile.mkstemp(prefix=".intent-sdlc-harness-", dir=str(target.parent))
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as output:
            output.write(content)
        temporary.chmod(mode)
        os.replace(str(temporary), str(target))
    finally:
        if temporary.exists():
            temporary.unlink()


def install(prefix, source):
    prefix = prefix.expanduser().resolve()
    source = source.expanduser().resolve()
    runtime = prefix / "share/intent-sdlc-harness"
    bindir = prefix / "bin"
    entrypoint = bindir / "sdlc-claude"
    for name in RUNTIME_FILES:
        if not (source / name).is_file():
            raise RuntimeError("installer source is missing %s" % name)
        target = runtime / name
        if target.exists():
            if target.is_symlink() or not target.is_file():
                raise RuntimeError("refusing to replace non-file %s" % target)
            existing = target.read_text(encoding="utf-8", errors="replace")
            if RUNTIME_MARKERS[name] not in existing:
                raise RuntimeError("refusing to replace existing non-harness file %s" % target)
    if entrypoint.exists():
        if entrypoint.is_symlink() or not entrypoint.is_file():
            raise RuntimeError("refusing to replace non-file %s" % entrypoint)
        existing = entrypoint.read_text(encoding="utf-8", errors="replace")
        if MARKER not in existing:
            raise RuntimeError("refusing to replace existing non-harness file %s" % entrypoint)
    runtime.mkdir(parents=True, exist_ok=True)
    bindir.mkdir(parents=True, exist_ok=True)
    for name in RUNTIME_FILES:
        copy_atomic(source / name, runtime / name)
    write_atomic(entrypoint, managed_entrypoint(runtime),
                 stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
                 stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    return entrypoint, runtime


def main(argv=None):
    parser = argparse.ArgumentParser(description="install sdlc-claude under a user prefix")
    parser.add_argument("--prefix", type=Path, default=Path.home() / ".local")
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parent,
                        help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        entrypoint, runtime = install(args.prefix, args.source)
    except (OSError, RuntimeError) as exc:
        print("install.py: %s" % exc, file=sys.stderr)
        return 2
    print("Installed %s" % entrypoint)
    print("Runtime: %s" % runtime)
    print("PATH was not changed; ensure %s is already on PATH." % entrypoint.parent)
    return 0


if __name__ == "__main__":
    sys.exit(main())
