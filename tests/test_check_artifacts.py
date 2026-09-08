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
import shutil
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


# --------------------------------------------------------------------------
# D16 — 승인 전이 예외
# --------------------------------------------------------------------------
INTENT_TEMPLATE = """---
id: 0001-bootstrap-repo
kind: intent
status: %(status)s
author: %(author)s
created: 2026-09-08T20:00:00+09:00
record: none
supersedes: none
---
# Intent: 사슬을 기계가 지키는 레퍼런스가 없다

## Problem (문제)
참조 레포 %(count)s개를 실측했지만 아티팩트 검증기가 실효인 곳은 하나도 없었다.

## Proposed outcome (원하는 결과)
`make check` 하나로 강제가 살아 있는지 확인되는 레포가 남는다.

## Affected users and systems (영향 범위)
이 레포를 읽는 사람 · CI · 훅.

## Constraints (제약)
- C1 표준 라이브러리만 쓴다.

## Open questions (미결)
- Q1 예제 주제를 무엇으로 할 것인가 — 사용자.
"""


def intent_text(status="draft", author="부모 세션(openwebagent)", count="7"):
    return INTENT_TEMPLATE % {"status": status, "author": author, "count": count}


class AcceptTransitionD16(unittest.TestCase):
    """D16 — 브랜치 위의 `accepted` 는 「status: 줄만 바꾼 승인」일 때만 통과한다.

    설계안 §4 는 승인을 「PR 안에서 `status:` 를 고치고 머지」로 정의했는데, 그것을
    브랜치에서 전면 금지하면 **승인 PR 자체가 CI 에서 빨개져** 사슬이 한 칸도 전진하지
    못한다. 그래서 「도장만 찍는 커밋」은 통과시키고 「고치면서 승인」은 계속 막는다.
    """

    PATH = "intent/0001-bootstrap-repo/intent.md"

    def _repo(self):
        tmp = tempfile.mkdtemp(prefix="d16-")
        self.addCleanup(shutil.rmtree, tmp, True)
        git(tmp, "init", "-q", "-b", "main")
        git(tmp, "config", "user.name", "t")
        git(tmp, "config", "user.email", "t@example.invalid")
        return tmp

    def _write(self, tmp, text):
        path = os.path.join(tmp, self.PATH)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)

    def _commit(self, tmp, message):
        git(tmp, "add", "-A")
        git(tmp, "commit", "-q", "-m", message)

    def _check(self, tmp):
        rc, out, err = run_cli(["--format", "json", self.PATH], cwd=tmp)
        payload = json.loads(out)
        codes = [f["code"] for e in payload["files"] for f in e["findings"]]
        return rc, codes, out + err

    # --- 예외가 여는 자리 -------------------------------------------------

    def test_status_only_flip_on_branch_is_allowed(self):
        """기본 브랜치의 draft 를 브랜치에서 `status:` 줄만 바꿔 승인 — 통과."""
        tmp = self._repo()
        self._write(tmp, intent_text("draft"))
        self._commit(tmp, "draft")
        git(tmp, "checkout", "-q", "-b", "chore/accept-0001")
        self._write(tmp, intent_text("accepted"))
        self._commit(tmp, "accept")
        rc, codes, raw = self._check(tmp)
        self.assertNotIn("ACCEPTED_ON_BRANCH", codes, raw)
        self.assertEqual(rc, 0, raw)

    def test_chain_born_on_branch_is_allowed_when_the_accepting_commit_is_status_only(self):
        """사슬 전체가 한 브랜치에서 태어나도, 승인 커밋이 `status:` 줄만 바꿨으면 통과."""
        tmp = self._repo()
        with open(os.path.join(tmp, "README.md"), "w", encoding="utf-8") as fh:
            fh.write("base\n")
        self._commit(tmp, "base")
        git(tmp, "checkout", "-q", "-b", "feat/0001-chain-meta")
        self._write(tmp, intent_text("draft"))
        self._commit(tmp, "intent draft")
        self._write(tmp, intent_text("accepted"))
        self._commit(tmp, "intent accepted")
        rc, codes, raw = self._check(tmp)
        self.assertNotIn("ACCEPTED_ON_BRANCH", codes, raw)
        self.assertEqual(rc, 0, raw)

    def test_file_identical_to_default_branch_is_allowed(self):
        """기본 브랜치와 바이트가 같은 accepted 파일 — 예외 이전부터 통과였다."""
        tmp = self._repo()
        self._write(tmp, intent_text("accepted"))
        self._commit(tmp, "accepted on main")
        git(tmp, "checkout", "-q", "-b", "feat/other")
        with open(os.path.join(tmp, "README.md"), "w", encoding="utf-8") as fh:
            fh.write("무관한 변경\n")
        self._commit(tmp, "unrelated")
        rc, codes, raw = self._check(tmp)
        self.assertNotIn("ACCEPTED_ON_BRANCH", codes, raw)
        self.assertEqual(rc, 0, raw)

    # --- 예외가 닫아 두는 자리 --------------------------------------------

    def test_flip_with_body_edit_is_still_red(self):
        """「고치면서 승인」 — status 와 본문을 같은 커밋에서 함께 고치면 red."""
        tmp = self._repo()
        self._write(tmp, intent_text("draft"))
        self._commit(tmp, "draft")
        git(tmp, "checkout", "-q", "-b", "chore/accept-0001")
        self._write(tmp, intent_text("accepted", count="9"))
        self._commit(tmp, "accept and edit")
        rc, codes, raw = self._check(tmp)
        self.assertIn("ACCEPTED_ON_BRANCH", codes, raw)
        self.assertEqual(rc, 1, raw)

    def test_flip_with_frontmatter_edit_is_still_red(self):
        """본문이 아니라 frontmatter 의 다른 키를 함께 고쳐도 red 다."""
        tmp = self._repo()
        self._write(tmp, intent_text("draft"))
        self._commit(tmp, "draft")
        git(tmp, "checkout", "-q", "-b", "chore/accept-0001")
        self._write(tmp, intent_text("accepted", author="다른 사람"))
        self._commit(tmp, "accept and rename author")
        rc, codes, raw = self._check(tmp)
        self.assertIn("ACCEPTED_ON_BRANCH", codes, raw)
        self.assertEqual(rc, 1, raw)

    def test_born_accepted_on_branch_is_red(self):
        """draft 단계 없이 처음부터 accepted 로 태어나면 red — 도장 찍을 원본이 없다."""
        tmp = self._repo()
        with open(os.path.join(tmp, "README.md"), "w", encoding="utf-8") as fh:
            fh.write("base\n")
        self._commit(tmp, "base")
        git(tmp, "checkout", "-q", "-b", "feat/0001-chain-meta")
        self._write(tmp, intent_text("accepted"))
        self._commit(tmp, "intent accepted from birth")
        rc, codes, raw = self._check(tmp)
        self.assertIn("ACCEPTED_ON_BRANCH", codes, raw)
        self.assertEqual(rc, 1, raw)

    def test_body_edited_after_the_accepting_commit_is_red(self):
        """승인한 뒤에 내용을 고치면 red — accepted 는 이후 불변이다."""
        tmp = self._repo()
        with open(os.path.join(tmp, "README.md"), "w", encoding="utf-8") as fh:
            fh.write("base\n")
        self._commit(tmp, "base")
        git(tmp, "checkout", "-q", "-b", "feat/0001-chain-meta")
        self._write(tmp, intent_text("draft"))
        self._commit(tmp, "intent draft")
        self._write(tmp, intent_text("accepted"))
        self._commit(tmp, "intent accepted")
        self._write(tmp, intent_text("accepted", count="99"))
        self._commit(tmp, "edit after accept")
        rc, codes, raw = self._check(tmp)
        self.assertIn("ACCEPTED_ON_BRANCH", codes, raw)
        self.assertEqual(rc, 1, raw)

    def test_uncommitted_body_edit_beside_the_flip_is_red(self):
        """승인 커밋은 status 만 바꿨어도 작업 트리에 미커밋 편집이 있으면 red."""
        tmp = self._repo()
        self._write(tmp, intent_text("draft"))
        self._commit(tmp, "draft")
        git(tmp, "checkout", "-q", "-b", "chore/accept-0001")
        self._write(tmp, intent_text("accepted"))
        self._commit(tmp, "accept")
        self._write(tmp, intent_text("accepted", count="9"))  # 커밋하지 않는다
        rc, codes, raw = self._check(tmp)
        self.assertIn("ACCEPTED_ON_BRANCH", codes, raw)
        self.assertEqual(rc, 1, raw)

    def test_accepted_file_edited_on_branch_is_red(self):
        """기본 브랜치에서 이미 accepted 인 파일을 브랜치에서 고치면 red(포착 보존)."""
        tmp = self._repo()
        self._write(tmp, intent_text("accepted"))
        self._commit(tmp, "accepted on main")
        git(tmp, "checkout", "-q", "-b", "feat/rewrite")
        self._write(tmp, intent_text("accepted", count="42"))
        self._commit(tmp, "rewrite accepted artifact")
        rc, codes, raw = self._check(tmp)
        self.assertIn("ACCEPTED_ON_BRANCH", codes, raw)
        self.assertEqual(rc, 1, raw)

    # --- 못 잰 자리는 note 로 남는다 --------------------------------------

    def test_detached_head_is_a_note_not_a_silent_pass(self):
        """CI 의 detached HEAD — 판정을 포기하고 note 를 남긴다(rc 는 올리지 않는다)."""
        tmp = self._repo()
        self._write(tmp, intent_text("accepted"))
        self._commit(tmp, "accepted")
        git(tmp, "checkout", "-q", "--detach", "HEAD")
        rc, codes, raw = self._check(tmp)
        self.assertIn("ACCEPTED_BRANCH_CHECK_SKIPPED", codes, raw)
        self.assertEqual(rc, 0, raw)

    def test_git_failure_in_the_exception_is_reported_not_swallowed(self):
        """예외 판정이 git 때문에 못 돌면 조용히 통과시키지 않고 사유를 돌려준다."""
        module = load_checker()
        tmp = self._repo()
        self._write(tmp, intent_text("draft"))
        self._commit(tmp, "draft")
        ctx = module.GitContext(tmp)
        text, error = module.run_accept_diff(ctx, "0" * 40, self.PATH)
        self.assertIsNone(text, "없는 ref 로 git diff 가 성공했다: %r" % (text,))
        self.assertTrue(error, "실패했는데 사유가 비었다 — 그러면 CI 에서 자리가 조용히 빈다")

    # --- 판정 함수 자체 ---------------------------------------------------

    def test_classify_accept_diff_reads_only_the_status_line(self):
        module = load_checker()
        self.assertEqual(module.classify_accept_diff(""), "identical")
        status_only = (
            "diff --git a/x.md b/x.md\nindex 111..222 100644\n--- a/x.md\n+++ b/x.md\n"
            "@@ -3 +3 @@\n-status: draft\n+status: accepted\n"
        )
        self.assertEqual(module.classify_accept_diff(status_only), "status_only")
        with_body = status_only + "@@ -12 +12 @@\n-옛 문장\n+새 문장\n"
        self.assertEqual(module.classify_accept_diff(with_body), "content")
        new_file = (
            "diff --git a/x.md b/x.md\nnew file mode 100644\n--- /dev/null\n+++ b/x.md\n"
            "@@ -0,0 +1,2 @@\n+---\n+status: accepted\n"
        )
        self.assertEqual(module.classify_accept_diff(new_file), "content")


if __name__ == "__main__":
    unittest.main()
