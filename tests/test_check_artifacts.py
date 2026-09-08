#!/usr/bin/env python3
"""tests/test_check_artifacts.py — 아티팩트 검증기의 계약 시험 (stdlib unittest).

여기서 재는 것
  - red 픽스처 8종이 **각자 지정한 code** 로 red 인가(엉뚱한 이유로 빨간 것은 실패).
  - green 픽스처 2종이 통과하는가(대괄호·인용부호 산문을 반려하지 않는가).
  - templates/*.md 는 반드시 rc=1 인가(자리표시자가 남아 있으므로).
  - rc 3분법: 0 통과 / 1 결함 / 2 판정 불가.
  - 상류(upstream) 검사는 **실물 git** 을 태운다 — 모의하지 않는다.
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CHECKER = os.path.join(REPO, "scripts", "check_artifacts.py")

sys.path.insert(0, HERE)

from fixture_harness import format_detail, run_fixture  # noqa: E402


def load_checker():
    """검증기를 모듈로 읽어 순수 함수 단위로도 잰다."""
    spec = importlib.util.spec_from_file_location("check_artifacts", CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_cli(args, cwd=None):
    proc = subprocess.run(
        [sys.executable, CHECKER] + list(args),
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return (
        proc.returncode,
        proc.stdout.decode("utf-8", "replace"),
        proc.stderr.decode("utf-8", "replace"),
    )


def git(cwd, *args):
    proc = subprocess.run(
        ["git"] + list(args), cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    if proc.returncode != 0:
        raise AssertionError(
            "git %s 실패: %s" % (" ".join(args), proc.stdout.decode("utf-8", "replace"))
        )
    return proc.stdout.decode("utf-8", "replace")


class CheckerExists(unittest.TestCase):
    def test_checker_file_exists(self):
        self.assertTrue(os.path.exists(CHECKER), "scripts/check_artifacts.py 가 없다")

    def test_help_states_what_it_does_not_measure(self):
        rc, out, err = run_cli(["--help"])
        self.assertEqual(rc, 0, "--help 가 rc=%d\n%s" % (rc, err))
        for token in ["해법", "산문", "문제를"]:
            self.assertIn(token, out, "--help 에 「하지 않는 것」 서술이 없다: %r" % token)

    def test_module_docstring_states_non_goals(self):
        module = load_checker()
        doc = module.__doc__ or ""
        for token in ["하지 않는 것", "해법", "산문"]:
            self.assertIn(token, doc, "모듈 docstring 에 %r 이 없다" % token)


class Contract(unittest.TestCase):
    def test_missing_file_is_undecidable(self):
        rc, out, _err = run_cli(["--format", "json", "없는-파일.md"])
        self.assertEqual(rc, 2, "없는 파일은 rc=2 여야 한다 (판정 불가)\n%s" % out)
        payload = json.loads(out)
        codes = [
            f["code"] for e in payload["files"] for f in e["findings"]
        ]
        self.assertIn("FILE_MISSING", codes)

    def test_json_carries_schema_version_and_codes(self):
        fixture = os.path.join(HERE, "fixtures", "red", "placeholder-left")
        ok, detail = run_fixture(fixture)
        self.assertTrue(ok, format_detail("placeholder-left", detail))
        payload = detail["payload"]
        self.assertIn("schema_version", payload)
        self.assertIsInstance(payload["schema_version"], int)
        for entry in payload["files"]:
            for finding in entry["findings"]:
                self.assertIn("code", finding)
                self.assertIn("severity", finding)

    def test_type_is_inferred_from_filename_and_can_be_forced(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = os.path.join(tmp, "0002-claims-status")
            os.makedirs(d)
            path = os.path.join(d, "intent.md")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("---\nid: 0002-claims-status\nkind: intent\n---\n# Intent: x\n")
            rc, out, _err = run_cli(["--format", "json", path])
            payload = json.loads(out)
            self.assertEqual(payload["files"][0]["type"], "intent")
            rc, out, _err = run_cli(["--format", "json", "--type", "spec", path])
            payload = json.loads(out)
            self.assertEqual(payload["files"][0]["type"], "spec")

    def test_unresolvable_upstream_sha_is_undecidable(self):
        with tempfile.TemporaryDirectory() as tmp:
            git(tmp, "init", "-q", "-b", "main")
            git(tmp, "config", "user.name", "t")
            git(tmp, "config", "user.email", "t@example.invalid")
            d = os.path.join(tmp, "intent", "0002-claims-status")
            os.makedirs(d)
            src = os.path.join(HERE, "fixtures", "green", "plain")
            with open(os.path.join(src, "intent.md"), encoding="utf-8") as fh:
                intent = fh.read()
            with open(os.path.join(d, "intent.md"), "w", encoding="utf-8") as fh:
                fh.write(intent)
            with open(os.path.join(src, "spec.md"), encoding="utf-8") as fh:
                spec = fh.read()
            spec = spec.replace("{{sha:c1}}", "0" * 40)
            with open(os.path.join(d, "spec.md"), "w", encoding="utf-8") as fh:
                fh.write(spec)
            git(tmp, "add", "-A")
            git(tmp, "commit", "-q", "-m", "t")
            rc, out, _err = run_cli(
                ["--format", "json", "intent/0002-claims-status/spec.md"], cwd=tmp
            )
            self.assertEqual(rc, 2, "없는 sha 는 rc=2 여야 한다\n%s" % out)
            payload = json.loads(out)
            codes = [f["code"] for e in payload["files"] for f in e["findings"]]
            self.assertIn("UPSTREAM_UNRESOLVABLE", codes)

    def test_upstream_accepted_is_read_through_real_git(self):
        """상류 검사는 실물 `git show` 를 태운다 — 커밋 뒤에 파일을 draft 로
        되돌려도 sha 가 가리키는 판이 accepted 면 통과해야 한다."""
        with tempfile.TemporaryDirectory() as tmp:
            git(tmp, "init", "-q", "-b", "main")
            git(tmp, "config", "user.name", "t")
            git(tmp, "config", "user.email", "t@example.invalid")
            d = os.path.join(tmp, "intent", "0002-claims-status")
            os.makedirs(d)
            src = os.path.join(HERE, "fixtures", "green", "plain")
            with open(os.path.join(src, "intent.md"), encoding="utf-8") as fh:
                intent = fh.read()
            with open(os.path.join(d, "intent.md"), "w", encoding="utf-8") as fh:
                fh.write(intent)
            git(tmp, "add", "-A")
            git(tmp, "commit", "-q", "-m", "accepted intent")
            sha = git(tmp, "rev-parse", "HEAD").strip()
            with open(os.path.join(src, "spec.md"), encoding="utf-8") as fh:
                spec = fh.read().replace("{{sha:c1}}", sha)
            with open(os.path.join(d, "spec.md"), "w", encoding="utf-8") as fh:
                fh.write(spec)
            git(tmp, "add", "-A")
            git(tmp, "commit", "-q", "-m", "spec")
            rc, out, _err = run_cli(
                ["--format", "json", "intent/0002-claims-status/spec.md"], cwd=tmp
            )
            self.assertEqual(rc, 0, "실물 git 상류가 accepted 인데 rc=%d\n%s" % (rc, out))


class Templates(unittest.TestCase):
    """템플릿은 자리표시자가 남아 있으므로 반드시 red 다 — 게이트 상주 음성 대조."""


def _template_case(name):
    def case(self):
        path = os.path.join(REPO, "templates", name)
        self.assertTrue(os.path.exists(path), "%s 가 없다" % path)
        rc, out, err = run_cli(["--format", "json", path])
        self.assertEqual(rc, 1, "%s 가 rc=%d — 템플릿은 rc=1 이어야 한다\n%s%s" % (name, rc, out, err))
        payload = json.loads(out)
        codes = [f["code"] for e in payload["files"] for f in e["findings"]]
        self.assertIn("PLACEHOLDER_LEFT", codes, "%s 에 자리표시자 잔존이 안 잡혔다" % name)

    return case


for _name in [
    "intent.md",
    "intent-defect.md",
    "intent-incident.md",
    "spec.md",
    "plan.md",
]:
    setattr(
        Templates,
        "test_template_%s_is_red" % _name.replace(".", "_").replace("-", "_"),
        _template_case(_name),
    )


class RedFixtures(unittest.TestCase):
    """레퍼런스 레포 7종에서 실제로 뚫린 8자리."""


class GreenFixtures(unittest.TestCase):
    """정상 문서를 반려하지 않는가."""


def _fixture_case(kind, name):
    def case(self):
        path = os.path.join(HERE, "fixtures", kind, name)
        ok, detail = run_fixture(path)
        self.assertTrue(ok, "\n" + format_detail(name, detail))

    return case


for _kind, _cls in (("red", RedFixtures), ("green", GreenFixtures)):
    _base = os.path.join(HERE, "fixtures", _kind)
    for _entry in sorted(os.listdir(_base)) if os.path.isdir(_base) else []:
        if os.path.isdir(os.path.join(_base, _entry)):
            setattr(
                _cls,
                "test_%s" % _entry.replace("-", "_"),
                _fixture_case(_kind, _entry),
            )


class CodeStripping(unittest.TestCase):
    """펜스·인라인 코드 제거는 판정 **전에** 돈다."""

    def setUp(self):
        self.module = load_checker()

    def test_fenced_block_is_removed_but_line_count_survives(self):
        text = "a\n```\nstatus: accepted\n```\nb\n"
        out = self.module.strip_code_spans(text)
        self.assertNotIn("status: accepted", out)
        self.assertEqual(len(out.split("\n")), len(text.split("\n")))

    def test_inline_code_is_removed(self):
        out = self.module.strip_code_spans("보관: `status: accepted` 는 예시다\n")
        self.assertNotIn("status: accepted", out)
        self.assertIn("예시다", out)

    def test_brackets_and_quotes_survive(self):
        text = "『지침』[Art. 4] 와 【부속서 2】 · 「보관」\n"
        self.assertEqual(self.module.strip_code_spans(text), text)

    def test_tilde_fence_is_removed(self):
        out = self.module.strip_code_spans("a\n~~~\n‹자리표시자›\n~~~\nb\n")
        self.assertNotIn("‹", out)


if __name__ == "__main__":
    unittest.main()
