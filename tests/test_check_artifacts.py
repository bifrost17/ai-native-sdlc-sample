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


def scrubbed_env(**extra):
    """검증기가 읽는 브랜치 힌트 env 를 걷어낸 환경. CI 가 그것을 켜 두므로,
    「env 가 없을 때」를 재는 시험은 스스로 지워야 한다(계기가 환경을 타면 죽는다)."""
    env = os.environ.copy()
    for key in ("INTENT_CHECK_BRANCH", "INTENT_CHECK_DEFAULT_BRANCH"):
        env.pop(key, None)
    env.update(extra)
    return env


def run_cli(args, cwd=None, env=None):
    proc = subprocess.run(
        [sys.executable, CHECKER] + list(args),
        cwd=cwd,
        env=env,
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

    def _check(self, tmp, path=None, env=None):
        target = path or self.PATH
        rc, out, err = run_cli(
            ["--format", "json", target], cwd=tmp, env=env or scrubbed_env()
        )
        payload = json.loads(out)
        codes = [f["code"] for e in payload["files"] for f in e["findings"]]
        return rc, codes, out + err

    def _write_bytes(self, tmp, data, path=None):
        target = os.path.join(tmp, path or self.PATH)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wb") as fh:
            fh.write(data)

    def _write_at(self, tmp, relpath, text):
        target = os.path.join(tmp, relpath)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(text)

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

    def test_flip_not_yet_committed_is_allowed(self):
        """승인 커밋을 아직 만들지 않았어도, 작업 트리의 변경이 `status:` 줄뿐이면 통과.

        기준점은 「그 파일을 건드린 가장 최근 커밋」이 아니라 「아직 accepted 가 아니었던
        가장 최근 판」이어야 한다. 전자로 잡으면 승인을 커밋하기 직전의 작업 트리가
        red 로 읽혀, 승인 커밋을 만들 수조차 없다.
        """
        tmp = self._repo()
        with open(os.path.join(tmp, "README.md"), "w", encoding="utf-8") as fh:
            fh.write("base\n")
        self._commit(tmp, "base")
        git(tmp, "checkout", "-q", "-b", "feat/0001-chain-meta")
        self._write(tmp, intent_text("draft"))
        self._commit(tmp, "intent draft")
        self._write(tmp, intent_text("accepted"))  # 커밋하지 않는다
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
        """기준점 blob 을 못 열면 조용히 통과시키지 않고 사유를 돌려준다.

        판정 통로가 `git diff` 텍스트에서 `git show <ref>:<경로>` 바이트로 바뀌었어도
        「실패를 삼키지 않는다」는 계약은 그대로다 — 삼키면 CI 에서 자리가 조용히 빈다.
        """
        module = load_checker()
        tmp = self._repo()
        self._write(tmp, intent_text("draft"))
        self._commit(tmp, "draft")
        ctx = module.GitContext(tmp)
        rc, out, err = ctx.show("0" * 40, self.PATH)
        self.assertNotEqual(rc, 0, "없는 ref 로 git show 가 성공했다: %r" % (out,))
        self.assertTrue(err, "실패했는데 사유가 비었다 — 그러면 CI 에서 자리가 조용히 빈다")

    # --- 축: diff 의 모양이 아니라 두 blob 의 frontmatter ------------------

    def test_binary_diff_cannot_hide_a_rewrite(self):
        """NUL 바이트를 넣어 git 이 `Binary files … differ` 를 내게 해도 red.

        diff 의 텍스트 모양을 어휘로 삼으면 그 어휘의 소유자는 우리가 아니라 git 이다
        — binary 판정 한 번에 전면 개작이 「바뀐 줄 0」으로 읽힌다.
        """
        tmp = self._repo()
        self._write_bytes(tmp, intent_text("draft").encode("utf-8") + b"\x00\n")
        self._commit(tmp, "draft (NUL 포함 — git 은 binary 로 본다)")
        git(tmp, "checkout", "-q", "-b", "chore/accept-0001")
        self._write_bytes(
            tmp, intent_text("accepted", count="9999").encode("utf-8") + b"\x00\n"
        )
        self._commit(tmp, "accept + 전면 개작")
        rc, codes, raw = self._check(tmp)
        self.assertIn("ACCEPTED_ON_BRANCH", codes, raw)
        self.assertEqual(rc, 1, raw)

    def test_gitattributes_diff_driver_cannot_hide_a_rewrite(self):
        """`.gitattributes` 의 `*.md -diff` 로 diff 를 막아도 red."""
        tmp = self._repo()
        self._write(tmp, intent_text("draft"))
        self._write_at(tmp, ".gitattributes", "*.md -diff\n")
        self._commit(tmp, "draft + .gitattributes(*.md -diff)")
        git(tmp, "checkout", "-q", "-b", "chore/accept-0001")
        self._write(tmp, intent_text("accepted", count="9999"))
        self._commit(tmp, "accept + 전면 개작")
        rc, codes, raw = self._check(tmp)
        self.assertIn("ACCEPTED_ON_BRANCH", codes, raw)
        self.assertEqual(rc, 1, raw)

    def test_body_line_deleted_behind_a_diff_prefix_is_still_red(self):
        """본문 줄이 `---` 로 시작하면 diff 접두 필터가 그것을 걸러 낸다 — 그래도 red."""
        tmp = self._repo()
        base = intent_text("draft").replace(
            "## Constraints (제약)", "---\n## Constraints (제약)"
        )
        self.assertIn("---\n## Constraints", base)
        self._write(tmp, base)
        self._commit(tmp, "draft (본문에 수평선)")
        git(tmp, "checkout", "-q", "-b", "chore/accept-0001")
        # 줄 수까지 같게 지운다 — diff 에는 `-` 한 줄과 status 한 줄만 남는다.
        self._write(tmp, intent_text("accepted"))
        self._commit(tmp, "accept + 수평선 삭제")
        rc, codes, raw = self._check(tmp)
        self.assertIn("ACCEPTED_ON_BRANCH", codes, raw)
        self.assertEqual(rc, 1, raw)

    def test_body_line_added_behind_a_diff_prefix_is_still_red(self):
        """`++` 로 시작하는 본문 줄을 승인과 함께 몰래 넣어도 red."""
        tmp = self._repo()
        self._write(tmp, intent_text("draft"))
        self._commit(tmp, "draft")
        git(tmp, "checkout", "-q", "-b", "chore/accept-0001")
        # 한 줄만 넣는다 — diff 에서 `+` + `++…` 는 `+++…` 가 되어 접두 필터에 걸린다.
        forged = intent_text("accepted").replace(
            "## Open questions (미결)", "++ 승인 뒤 몰래 붙인 줄\n## Open questions (미결)"
        )
        self.assertIn("++ 승인 뒤", forged)
        self._write(tmp, forged)
        self._commit(tmp, "accept + '++' 줄 추가")
        rc, codes, raw = self._check(tmp)
        self.assertIn("ACCEPTED_ON_BRANCH", codes, raw)
        self.assertEqual(rc, 1, raw)

    def test_editing_an_accepted_artifact_through_a_fenced_status_line_is_red(self):
        """이미 accepted 인 정본을, 바뀐 줄이 **펜스 안 pseudo-status 하나**가 되게 편집 — red.

        「바뀐 줄이 status 모양 하나뿐」을 도장으로 읽으면, 그 줄이 frontmatter 밖에
        있어도 도장으로 읽힌다. 도장은 frontmatter 의 status 키에서만 일어난다.
        """
        tmp = self._repo()
        fenced = intent_text("accepted").replace(
            "## Open questions (미결)\n",
            "## Open questions (미결)\n예시 frontmatter:\n```yaml\nstatus: draft\n```\n",
            1,
        )
        self.assertIn("```yaml", fenced)
        self._write(tmp, fenced)
        self._commit(tmp, "accepted on main (PO 정본)")
        git(tmp, "checkout", "-q", "-b", "feat/edit-fenced-line")
        self._write(tmp, fenced.replace("status: draft\n```", "status: superseded\n```", 1))
        self._commit(tmp, "accepted 파일을 브랜치에서 편집(펜스 줄 1개)")
        rc, codes, raw = self._check(tmp)
        self.assertIn("ACCEPTED_ON_BRANCH", codes, raw)
        self.assertEqual(rc, 1, raw)

    def test_editing_an_accepted_artifact_through_a_body_status_line_is_red(self):
        """같은 것을, 펜스가 아니라 본문의 `status:` 모양 줄로 해도 red."""
        tmp = self._repo()
        seeded = intent_text("accepted").replace(
            "## Open questions (미결)\n", "status: draft\n\n## Open questions (미결)\n", 1
        )
        self._write(tmp, seeded)
        self._commit(tmp, "accepted on main + 본문에 status 모양 줄")
        git(tmp, "checkout", "-q", "-b", "feat/edit-body-line")
        self._write(
            tmp,
            seeded.replace(
                "status: draft\n\n## Open questions", "status: rejected\n\n## Open questions", 1
            ),
        )
        self._commit(tmp, "accepted 파일을 브랜치에서 편집(본문 status 모양 줄 1개)")
        rc, codes, raw = self._check(tmp)
        self.assertIn("ACCEPTED_ON_BRANCH", codes, raw)
        self.assertEqual(rc, 1, raw)

    def test_inline_comment_on_the_status_line_is_not_a_stamp(self):
        """`status: accepted  # PO 승인 …` 은 도장이 아니다 — red (기존 포착 보존).

        승인 커밋에 함께 들어온 산문은 아무도 검토하지 않았다.
        """
        tmp = self._repo()
        self._write(tmp, intent_text("draft"))
        self._commit(tmp, "draft")
        git(tmp, "checkout", "-q", "-b", "chore/accept-0001")
        self._write(tmp, intent_text("accepted  # PO 승인 2026-09-08"))
        self._commit(tmp, "accept with an inline comment")
        rc, codes, raw = self._check(tmp)
        self.assertIn("ACCEPTED_ON_BRANCH", codes, raw)
        self.assertEqual(rc, 1, raw)

    def test_trailing_whitespace_on_the_status_line_is_still_a_stamp(self):
        """`status: accepted   ` — 값 뒤의 공백뿐이면 여전히 도장이다(거짓 양성 없음)."""
        tmp = self._repo()
        self._write(tmp, intent_text("draft"))
        self._commit(tmp, "draft")
        git(tmp, "checkout", "-q", "-b", "chore/accept-0001")
        self._write(tmp, intent_text("accepted   "))
        self._commit(tmp, "accept (status 줄 끝 공백)")
        rc, codes, raw = self._check(tmp)
        self.assertNotIn("ACCEPTED_ON_BRANCH", codes, raw)
        self.assertEqual(rc, 0, raw)

    # --- 기준점은 경로가 아니라 사슬 id 로 찾는다 -------------------------

    def test_baseline_is_found_by_chain_id_not_by_file_path(self):
        """main 의 accepted 정본을 다른 파일명으로 옮겨 개작하고 재도장 — red.

        경로로 기준점을 찾으면 개명 한 번에 기준점이 브랜치 자기 커밋으로 후퇴한다.
        사슬 id 는 우리가 소유하는 어휘라 경로가 움직여도 살아남는다.
        """
        tmp = self._repo()
        self._write(tmp, intent_text("accepted"))
        self._commit(tmp, "accepted on main (PO 정본)")
        git(tmp, "checkout", "-q", "-b", "feat/rename-file")
        moved = "intent/0001-bootstrap-repo/intent-defect.md"
        os.remove(os.path.join(tmp, self.PATH))
        self._write_at(tmp, moved, intent_text("draft", count="9999"))
        self._commit(tmp, "파일명을 바꾸고 개작해 draft 로 심는다")
        self._write_at(tmp, moved, intent_text("accepted", count="9999"))
        self._commit(tmp, "재도장 (status 줄만)")
        rc, codes, raw = self._check(tmp, path=moved)
        self.assertIn("ACCEPTED_ON_BRANCH", codes, raw)
        self.assertEqual(rc, 1, raw)

    def test_shedding_an_accepted_artifact_by_switching_ids_is_red(self):
        """accepted 정본을 지우고 **새 id 로 갈아타** 그 자리에서 자기 승인 — red.

        파일 하나만 보면 「이 브랜치에서 태어난 새 사슬」로 읽힌다. 사라진 것은
        기본 브랜치의 승인 기록이고, 그 사라짐은 사슬 id 로 셀 수 있다.
        """
        tmp = self._repo()
        self._write(tmp, intent_text("accepted"))
        self._commit(tmp, "accepted on main (PO 정본)")
        git(tmp, "checkout", "-q", "-b", "feat/rename-dir")
        moved = "intent/0001-bootstrap/intent.md"
        forged = intent_text("draft", count="9999").replace(
            "id: 0001-bootstrap-repo", "id: 0001-bootstrap", 1
        )
        os.remove(os.path.join(tmp, self.PATH))
        self._write_at(tmp, moved, forged)
        self._commit(tmp, "디렉터리 개명 + 개작 + draft 로 심기")
        self._write_at(tmp, moved, forged.replace("status: draft", "status: accepted", 1))
        self._commit(tmp, "재도장 (status 줄만)")
        rc, codes, raw = self._check(tmp, path=moved)
        self.assertIn("ACCEPTED_ARTIFACT_VANISHED", codes, raw)
        self.assertEqual(rc, 1, raw)

    # --- 상태 전이표 — 허용 목록 밖은 전부 거부 ---------------------------

    def test_rejected_to_accepted_is_denied(self):
        """`rejected` → `accepted` 는 되살리기다 — 전이표에 없으므로 red (spec F2)."""
        tmp = self._repo()
        self._write(tmp, intent_text("rejected"))
        self._commit(tmp, "rejected on main")
        git(tmp, "checkout", "-q", "-b", "chore/revive")
        self._write(tmp, intent_text("accepted"))
        self._commit(tmp, "rejected -> accepted")
        rc, codes, raw = self._check(tmp)
        self.assertIn("ACCEPT_TRANSITION_NOT_ALLOWED", codes, raw)
        self.assertEqual(rc, 1, raw)

    def test_superseded_to_accepted_is_denied(self):
        """`superseded` → `accepted` 도 되살리기다 — 지면 어디에도 없던 갈래."""
        tmp = self._repo()
        self._write(tmp, intent_text("superseded"))
        self._commit(tmp, "superseded on main")
        git(tmp, "checkout", "-q", "-b", "chore/revive2")
        self._write(tmp, intent_text("accepted"))
        self._commit(tmp, "superseded -> accepted")
        rc, codes, raw = self._check(tmp)
        self.assertIn("ACCEPT_TRANSITION_NOT_ALLOWED", codes, raw)
        self.assertEqual(rc, 1, raw)

    def test_transition_table_is_the_single_edit_point(self):
        """전이표는 한 곳에 데이터로 있고, 그 밖은 전부 거부다(표 한 줄로 되돌린다)."""
        module = load_checker()
        self.assertEqual(
            module.ACCEPT_TRANSITIONS,
            (
                ("draft", "accepted"),
                ("draft", "rejected"),
                ("draft", "superseded"),
                ("accepted", "superseded"),
            ),
        )
        for before, after in module.ACCEPT_TRANSITIONS:
            self.assertIn(before, module.STATUS_VALUES)
            self.assertIn(after, module.STATUS_VALUES)

    # --- 판정 함수 자체 — 두 바이트열을 견준다 ----------------------------

    def test_classify_accept_transition_compares_bytes_not_diff_text(self):
        module = load_checker()
        base = b"---\nid: 0001-x\nstatus: draft\n---\n# Intent: x\nbody\n"
        same = module.classify_accept_transition(base, base)
        self.assertEqual(same[0], "identical")
        stamp = module.classify_accept_transition(
            base, base.replace(b"status: draft", b"status: accepted")
        )
        self.assertEqual((stamp[0], stamp[1], stamp[2]), ("stamp", "draft", "accepted"))
        body = module.classify_accept_transition(
            base, base.replace(b"status: draft", b"status: accepted").replace(b"body", b"other body")
        )
        self.assertEqual(body[0], "content")
        key = module.classify_accept_transition(
            base, base.replace(b"status: draft", b"status: accepted").replace(b"id: 0001-x", b"id: 0002-y")
        )
        self.assertEqual(key[0], "content")
        comment = module.classify_accept_transition(
            base, base.replace(b"status: draft", b"status: accepted  # PO")
        )
        self.assertEqual(comment[0], "content")
        born = module.classify_accept_transition(b"", base.replace(b"draft", b"accepted"))
        self.assertEqual(born[0], "content")


# --------------------------------------------------------------------------
# E4 — CI 의 detached HEAD 에서도 검사가 **실제로 돈다**
# --------------------------------------------------------------------------
class BranchResolutionFromEnv(unittest.TestCase):
    """「안 돌았다」는 「통과」가 아니다.

    CI 는 detached HEAD 로 체크아웃하므로 `git symbolic-ref` 가 브랜치를 못 낸다.
    그때 브랜치·기본 브랜치를 env 로 받아 검사를 돌린다. 여기서 재는 것은 두 방향이다
    — 위반을 심으면 실제로 빨개지는가(양성 대조) · 진짜 도장은 여전히 통과하는가.
    """

    PATH = "intent/0001-bootstrap-repo/intent.md"

    def _detached_repo(self, accepted_text):
        """main=draft · 브랜치=accepted 를 만들고 CI 모양(detached · 로컬 브랜치 0개)으로 둔다."""
        tmp = tempfile.mkdtemp(prefix="d16env-")
        self.addCleanup(shutil.rmtree, tmp, True)
        git(tmp, "init", "-q", "-b", "main")
        git(tmp, "config", "user.name", "t")
        git(tmp, "config", "user.email", "t@example.invalid")
        path = os.path.join(tmp, self.PATH)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(intent_text("draft"))
        git(tmp, "add", "-A")
        git(tmp, "commit", "-q", "-m", "draft on main")
        git(tmp, "checkout", "-q", "-b", "chore/accept-0001")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(accepted_text)
        git(tmp, "add", "-A")
        git(tmp, "commit", "-q", "-m", "accept")
        # actions/checkout 재현: 원격 참조만 남기고 로컬 브랜치를 지운 detached HEAD
        git(tmp, "update-ref", "refs/remotes/origin/main", "refs/heads/main")
        git(tmp, "checkout", "-q", "--detach", "HEAD")
        git(tmp, "branch", "-q", "-D", "main")
        git(tmp, "branch", "-q", "-D", "chore/accept-0001")
        return tmp

    def _check(self, tmp, env):
        rc, out, err = run_cli(["--format", "json", self.PATH], cwd=tmp, env=env)
        payload = json.loads(out)
        codes = [f["code"] for e in payload["files"] for f in e["findings"]]
        return rc, codes, out + err

    def test_detached_head_without_env_is_a_note(self):
        """env 도 없으면 지금처럼 note 다 — 조용한 통과가 아니라 「못 쟀다」."""
        tmp = self._detached_repo(intent_text("accepted", count="9999"))
        rc, codes, raw = self._check(tmp, scrubbed_env())
        self.assertIn("ACCEPTED_BRANCH_CHECK_SKIPPED", codes, raw)
        self.assertEqual(rc, 0, raw)

    def test_detached_head_with_env_runs_the_check_and_catches_a_violation(self):
        """양성 대조 — env 로 브랜치를 알려주면 검사가 **실제로 돌아** 위반을 잡는다."""
        tmp = self._detached_repo(intent_text("accepted", count="9999"))
        env = scrubbed_env(
            INTENT_CHECK_BRANCH="chore/accept-0001", INTENT_CHECK_DEFAULT_BRANCH="main"
        )
        rc, codes, raw = self._check(tmp, env)
        self.assertNotIn("ACCEPTED_BRANCH_CHECK_SKIPPED", codes, raw)
        self.assertIn("ACCEPTED_ON_BRANCH", codes, raw)
        self.assertEqual(rc, 1, raw)

    def test_detached_head_with_env_still_allows_a_real_stamp(self):
        """거짓 양성 없음 — 같은 배선에서 진짜 도장은 통과한다."""
        tmp = self._detached_repo(intent_text("accepted"))
        env = scrubbed_env(
            INTENT_CHECK_BRANCH="chore/accept-0001", INTENT_CHECK_DEFAULT_BRANCH="main"
        )
        rc, codes, raw = self._check(tmp, env)
        self.assertNotIn("ACCEPTED_BRANCH_CHECK_SKIPPED", codes, raw)
        self.assertNotIn("ACCEPTED_ON_BRANCH", codes, raw)
        self.assertEqual(rc, 0, raw)

    def test_workflow_hands_the_branch_names_to_make_check(self):
        """배선 — 워크플로가 그 env 를 실제로 넘긴다(넘기지 않으면 CI 집행력이 0 이다)."""
        with open(os.path.join(REPO, ".github", "workflows", "check.yml"), encoding="utf-8") as fh:
            workflow = fh.read()
        self.assertIn("INTENT_CHECK_BRANCH: ${{ github.head_ref || github.ref_name }}", workflow)
        self.assertIn("INTENT_CHECK_DEFAULT_BRANCH: ${{ github.base_ref || 'main' }}", workflow)


# --------------------------------------------------------------------------
# E5 — 안 돈 것을 셀 수 있어야 한다
# --------------------------------------------------------------------------
class GateForwardsSkipNotes(unittest.TestCase):
    """게이트가 rc=0 이어도 note 는 로그로 흘러야 한다.

    `run_gate` 는 PASS 일 때 함수 출력을 통째로 버린다 — 그래서 「검사가 안 돌았다」는
    note 가 CI 로그에서 한 줄도 안 남았다. 「코드가 하나라서 셀 수 있다」는 지면의 주장은
    출력이 실제로 흘러야만 참이 된다.
    """

    def setUp(self):
        # 게이트 안에서 다시 게이트를 돌리면 무한 재귀다(check10 이 이 시험을 부른다).
        # 아래 _gate 가 이 표시를 켜고 부르므로, 안쪽 회차의 이 세 시험은 스스로 빠진다.
        if os.environ.get("INTENT_CHECK_GATE_PROBE"):
            self.skipTest("게이트 안의 회차 — 재귀 방지")

    def _gate(self, **extra):
        # 여기서 재는 것은 「지금 이 환경에서 그 검사가 실제로 도는가」다 —
        # 그러니 환경을 지우지 않는다. CI 는 브랜치를 env 로 알려주고, 그것을
        # 걷어내면 CI 회차가 자기 배선을 못 본 채 「안 돈다」고 말한다.
        extra.setdefault("INTENT_CHECK_GATE_PROBE", "1")
        env = os.environ.copy()
        env.update(extra)
        proc = subprocess.run(
            ["bash", "scripts/check_all.sh", "check11_intent_chain"],
            cwd=REPO,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        return proc.returncode, proc.stdout.decode("utf-8", "replace")

    def test_the_chain_has_an_accepted_artifact(self):
        """전제(양성 대조) — 사슬에 accepted 가 하나도 없으면 이 시험들은 아무것도 못 잰다."""
        found = []
        root = os.path.join(REPO, "intent")
        for dirpath, _dirs, files in os.walk(root):
            for name in files:
                if not name.endswith(".md"):
                    continue
                with open(os.path.join(dirpath, name), encoding="utf-8") as fh:
                    if "\nstatus: accepted\n" in fh.read():
                        found.append(os.path.join(dirpath, name))
        self.assertTrue(found, "intent/ 에 status: accepted 인 아티팩트가 없다")

    def test_skip_note_reaches_the_gate_output(self):
        """기본 브랜치를 못 찾게 만들면 게이트 출력에 그 토큰이 뜬다 — 셀 수 있다."""
        rc, out = self._gate(INTENT_CHECK_DEFAULT_BRANCH="__no_such_branch__")
        self.assertEqual(rc, 0, out)
        self.assertIn("PASS", out)
        self.assertGreaterEqual(out.count("ACCEPTED_BRANCH_CHECK_SKIPPED"), 1, out)

    def test_a_healthy_run_prints_no_skip_note(self):
        """이 레포에서 지금 그 검사는 **실제로 돈다** — 토큰이 0 이어야 한다."""
        rc, out = self._gate()
        self.assertEqual(rc, 0, out)
        self.assertEqual(out.count("ACCEPTED_BRANCH_CHECK_SKIPPED"), 0, out)


if __name__ == "__main__":
    unittest.main()
