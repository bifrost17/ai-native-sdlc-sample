#!/usr/bin/env python3
"""SP08 (FR09/AC08): check declared documents against a reviewed Git index."""

import hashlib
import json
import os
import re
import subprocess
import sys


class CheckError(Exception):
    pass


def git(*args, cwd=None, env=None, input_bytes=None, allowed=(0,)):
    result = subprocess.run(
        ["git", *args], cwd=cwd, env=env, input=input_bytes,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if result.returncode not in allowed:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise CheckError(detail or "Git 명령이 실패했습니다: " + " ".join(args))
    return result


def repository():
    # Git's relative environment paths are resolved from the caller's directory.
    env = os.environ.copy()
    for name in ("GIT_INDEX_FILE", "GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR"):
        value = env.get(name)
        if value and not os.path.isabs(value):
            env[name] = os.path.abspath(value)
    root = git("rev-parse", "--show-toplevel", env=env).stdout.decode("utf-8", "surrogateescape").strip()
    if not root:
        raise CheckError("작업 트리의 Git 저장소가 필요합니다.")
    return root, env


def head_identity(root, env):
    result = git("rev-parse", "--verify", "HEAD^{commit}", cwd=root, env=env, allowed=(0, 128))
    if result.returncode == 0:
        return result.stdout.strip()
    # A missing HEAD is valid only for a new branch's first commit.
    branch = git("symbolic-ref", "-q", "HEAD", cwd=root, env=env, allowed=(0, 1))
    if branch.returncode != 0:
        raise CheckError("HEAD를 확인할 수 없습니다. Git 상태를 복구한 뒤 다시 검토하세요.")
    return b"unborn"


def staged(root, env):
    if git("ls-files", "-u", "-z", cwd=root, env=env).stdout:
        raise CheckError("충돌이 해결되지 않은 index입니다. 충돌을 해결한 뒤 다시 검토하세요.")
    head = head_identity(root, env)
    entries = git("ls-files", "--stage", "-z", cwd=root, env=env).stdout
    names = git("diff", "--cached", "--name-only", "-z", "--no-renames",
                "--no-ext-diff", "--no-textconv", "--no-relative", "--no-color",
                "--ignore-submodules=none", "--", cwd=root, env=env).stdout
    if head_identity(root, env) != head:
        raise CheckError("검사 중 HEAD가 바뀌었습니다. staged 범위를 다시 검토하세요.")
    paths = set()
    for raw in names.split(b"\0"):
        if not raw:
            continue
        try:
            paths.add(raw.decode("utf-8"))
        except UnicodeDecodeError as exc:
            raise CheckError("staged 경로가 UTF-8이 아닙니다. 경로를 확인하세요.") from exc
    changed_paths = b"\0".join(path.encode("utf-8") for path in sorted(paths)) + b"\0"
    digest = hashlib.sha256(b"sdlc-doc-sync-v2\0" + len(head).to_bytes(4, "big") + head
                            + len(entries).to_bytes(8, "big") + entries
                            + len(changed_paths).to_bytes(8, "big") + changed_paths).hexdigest()
    return digest, paths


def valid_path(path):
    if not isinstance(path, str) or not path or "\0" in path or "\\" in path:
        return False
    if path.startswith("/") or re.match(r"^[A-Za-z]:", path):
        return False
    if any(part in ("", ".", "..") for part in path.split("/")):
        return False
    # Git pathspec syntax and shell globs must not turn an exact name into a pattern.
    if any(char in path for char in "*?[]") or path.startswith(":"):
        return False
    return True


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def check():
    signal = os.environ.get("SDLC_DOC_SYNC")
    if signal is None:
        raise CheckError("SDLC_DOC_SYNC 신호가 없습니다. 현재 세션에서 문서 영향을 검토하고 이번 커밋에만 전달하세요.")
    try:
        payload = json.loads(signal, object_pairs_hook=unique_object)
    except (ValueError, UnicodeError) as exc:
        raise CheckError("SDLC_DOC_SYNC가 유효한 JSON이 아닙니다. snapshot과 documents를 다시 만드세요.") from exc
    if not isinstance(payload, dict) or set(payload) != {"snapshot", "documents"}:
        raise CheckError("SDLC_DOC_SYNC에는 snapshot과 documents 두 필드만 필요합니다.")
    snapshot, documents = payload["snapshot"], payload["documents"]
    if not isinstance(snapshot, str) or not re.fullmatch(r"[0-9a-f]{64}", snapshot):
        raise CheckError("snapshot은 64자리 소문자 SHA-256 문자열이어야 합니다.")
    if not isinstance(documents, list) or any(not valid_path(path) for path in documents):
        raise CheckError("documents는 중복 없는 정확한 저장소 상대 경로 문자열 목록이어야 합니다.")
    if len(documents) != len(set(documents)):
        raise CheckError("documents에 중복 경로가 있습니다.")
    root, env = repository()
    current, paths = staged(root, env)
    if current != snapshot:
        raise CheckError("HEAD 또는 staged index가 검토한 snapshot과 다릅니다. 현재 범위를 다시 검토하고 지문을 새로 만드세요.")
    missing = sorted(set(documents) - paths)
    if missing:
        raise CheckError("필수 문서가 staged 변경에 없습니다: " + ", ".join(missing)
                         + ". 필요한 부분을 stage하고 새 snapshot으로 다시 검토하세요.")


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("snapshot", "check"):
        print("사용법: document_sync.py snapshot|check", file=sys.stderr)
        return 2
    try:
        if sys.argv[1] == "snapshot":
            root, env = repository()
            print(staged(root, env)[0])
        else:
            check()
    except CheckError as exc:
        print("document-sync: " + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
