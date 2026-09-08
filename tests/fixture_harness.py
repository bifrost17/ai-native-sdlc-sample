#!/usr/bin/env python3
"""tests/fixture_harness.py — 픽스처를 실제 git 저장소로 재현해 검증기를 태운다.

픽스처가 재는 것 중 상당수(upstream sha · 브랜치 자기 승인)는 **실제 커밋**이
없으면 존재할 수 없다. 그래서 픽스처 디렉터리는 「파일 + 만드는 순서」이고,
이 하네스가 임시 git 저장소에서 그 순서를 그대로 재생한 뒤 검증기를 돌린다.
모의(mock)는 쓰지 않는다 — `git show` 는 진짜로 돈다.

픽스처 디렉터리 구조
--------------------
    <fixture>/
      EXPECT        기대하는 error code 다중집합(한 줄에 하나 · '#' 주석 허용).
                    없으면 「error 0건」을 기대한다(green).
      SETUP         만드는 순서(아래 문법). 없으면 기본 순서가 쓰인다.
      <files...>    저장소에 써 넣을 원본들.

SETUP 문법(한 줄 한 동사 · '#' 주석 · 빈 줄 무시)
    write  <저장소경로> <픽스처파일>   파일을 써 넣는다. 내용 안의
                                       {{sha:LABEL}} 은 그 시점의 커밋 sha 로 치환.
    commit <LABEL>                     지금까지 쓴 것을 커밋하고 sha 를 LABEL 로 기록.
    branch <이름>                      새 브랜치로 이동(git checkout -b).
    check  <저장소경로>                검증기를 태울 대상(여러 줄 가능).

SETUP 이 없을 때의 기본
    픽스처 안의 모든 *.md 를 같은 상대경로로 write → commit base → 전부 check.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CHECKER = os.path.join(REPO, "scripts", "check_artifacts.py")

_SHA_TOKEN = re.compile(r"\{\{sha:([A-Za-z0-9_.-]+)\}\}")


class FixtureError(RuntimeError):
    """픽스처 자체가 잘못됐다 — 검증기의 판정이 아니라 계기 고장이다."""


def _git(cwd, *args):
    proc = subprocess.run(
        ["git"] + list(args),
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if proc.returncode != 0:
        raise FixtureError(
            "git %s 실패 (rc=%d): %s"
            % (" ".join(args), proc.returncode, proc.stdout.decode("utf-8", "replace"))
        )
    return proc.stdout.decode("utf-8", "replace")


def read_expect(fixture_dir):
    """EXPECT 파일 → 기대 code 리스트(다중집합 · 정렬해서 비교한다)."""
    path = os.path.join(fixture_dir, "EXPECT")
    if not os.path.exists(path):
        return []
    codes = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.split("#", 1)[0].strip()
            if line:
                codes.append(line)
    return codes


def _default_setup(fixture_dir):
    steps = []
    checks = []
    for root, _dirs, files in os.walk(fixture_dir):
        for name in sorted(files):
            if name in ("EXPECT", "SETUP", "README.md"):
                continue
            if not name.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(root, name), fixture_dir)
            steps.append(("write", rel, rel))
            checks.append(rel)
    steps.sort()
    steps.append(("commit", "base"))
    for rel in sorted(checks):
        steps.append(("check", rel))
    return steps


def _parse_setup(fixture_dir):
    path = os.path.join(fixture_dir, "SETUP")
    if not os.path.exists(path):
        return _default_setup(fixture_dir)
    steps = []
    with open(path, encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.split("#", 1)[0].strip()
            if not line:
                continue
            parts = line.split()
            verb = parts[0]
            if verb == "write":
                if len(parts) != 3:
                    raise FixtureError("SETUP:%d write 는 인자 2개" % lineno)
                steps.append(("write", parts[1], parts[2]))
            elif verb == "commit":
                if len(parts) != 2:
                    raise FixtureError("SETUP:%d commit 은 인자 1개" % lineno)
                steps.append(("commit", parts[1]))
            elif verb == "branch":
                if len(parts) != 2:
                    raise FixtureError("SETUP:%d branch 는 인자 1개" % lineno)
                steps.append(("branch", parts[1]))
            elif verb == "check":
                if len(parts) != 2:
                    raise FixtureError("SETUP:%d check 는 인자 1개" % lineno)
                steps.append(("check", parts[1]))
            else:
                raise FixtureError("SETUP:%d 모르는 동사 %r" % (lineno, verb))
    return steps


def materialize(fixture_dir, workdir):
    """픽스처를 workdir 에 실제 git 저장소로 재현하고 check 대상 목록을 돌려준다."""
    steps = _parse_setup(fixture_dir)
    _git(workdir, "init", "-q", "-b", "main")
    _git(workdir, "config", "user.name", "fixture")
    _git(workdir, "config", "user.email", "fixture@example.invalid")
    shas = {}
    checks = []
    for step in steps:
        if step[0] == "write":
            _, repo_rel, fixture_rel = step
            src = os.path.join(fixture_dir, fixture_rel)
            if not os.path.exists(src):
                raise FixtureError("픽스처 파일 없음: %s" % src)
            with open(src, encoding="utf-8") as fh:
                body = fh.read()

            def _sub(match):
                label = match.group(1)
                if label not in shas:
                    raise FixtureError(
                        "{{sha:%s}} 를 쓰려면 그 전에 commit %s 가 있어야 한다" % (label, label)
                    )
                return shas[label]

            body = _SHA_TOKEN.sub(_sub, body)
            dst = os.path.join(workdir, repo_rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, "w", encoding="utf-8") as fh:
                fh.write(body)
        elif step[0] == "commit":
            label = step[1]
            _git(workdir, "add", "-A")
            _git(workdir, "commit", "-q", "-m", "fixture: %s" % label)
            shas[label] = _git(workdir, "rev-parse", "HEAD").strip()
        elif step[0] == "branch":
            _git(workdir, "checkout", "-q", "-b", step[1])
        elif step[0] == "check":
            checks.append(step[1])
    if not checks:
        raise FixtureError("픽스처에 check 대상이 없다: %s" % fixture_dir)
    return checks


def run_checker(workdir, targets):
    """검증기를 --format json 으로 태우고 (rc, payload) 를 돌려준다."""
    proc = subprocess.run(
        [sys.executable, CHECKER, "--format", "json"] + list(targets),
        cwd=workdir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out = proc.stdout.decode("utf-8", "replace")
    err = proc.stderr.decode("utf-8", "replace")
    try:
        payload = json.loads(out)
    except ValueError:
        raise FixtureError(
            "검증기가 JSON 을 내지 않았다 (rc=%d)\n--- stdout ---\n%s\n--- stderr ---\n%s"
            % (proc.returncode, out, err)
        )
    return proc.returncode, payload


def codes_of(payload, severity="error"):
    codes = []
    for entry in payload.get("files", []):
        for finding in entry.get("findings", []):
            if finding.get("severity") == severity:
                codes.append(finding.get("code"))
    return codes


def run_fixture(fixture_dir):
    """픽스처 하나를 돌린다 → dict(rc, codes, expect, ok, detail)."""
    fixture_dir = os.path.abspath(fixture_dir)
    expect = read_expect(fixture_dir)
    workdir = tempfile.mkdtemp(prefix="fixture-")
    try:
        targets = materialize(fixture_dir, workdir)
        rc, payload = run_checker(workdir, targets)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
    codes = codes_of(payload, "error")
    undecidable = codes_of(payload, "undecidable")
    want_rc = 1 if expect else 0
    ok = sorted(codes) == sorted(expect) and rc == want_rc and not undecidable
    detail = {
        "rc": rc,
        "want_rc": want_rc,
        "codes": sorted(codes),
        "expect": sorted(expect),
        "undecidable": sorted(undecidable),
        "payload": payload,
    }
    return ok, detail


def format_detail(name, detail):
    lines = ["  rc=%d (기대 %d)" % (detail["rc"], detail["want_rc"])]
    lines.append("  실측 code : %s" % (", ".join(detail["codes"]) or "(없음)"))
    lines.append("  기대 code : %s" % (", ".join(detail["expect"]) or "(없음)"))
    if detail["undecidable"]:
        lines.append("  판정불가  : %s" % ", ".join(detail["undecidable"]))
    for entry in detail["payload"].get("files", []):
        for finding in entry.get("findings", []):
            lines.append(
                "    %-11s %-26s %s:%s %s"
                % (
                    finding.get("severity"),
                    finding.get("code"),
                    entry.get("path"),
                    finding.get("line"),
                    finding.get("message"),
                )
            )
    return "\n".join(lines)
