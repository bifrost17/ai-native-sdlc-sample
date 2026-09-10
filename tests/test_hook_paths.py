"""0013 R1 / AC1: guards resolve aliases, links, new destinations and invalid paths."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parents[1]


class HookPathTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="hook-paths-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.root = self.base / "checkout"
        self.hooks = self.root / ".claude" / "hooks"
        shutil.copytree(SOURCE / ".claude" / "hooks", self.hooks)
        for directory in ("src", "tests", ".github/workflows"):
            (self.root / directory).mkdir(parents=True)
        self.outside = self.base / "outside"
        self.outside.mkdir()
        (self.root / "src/ok.py").write_text("value = 1\n")
        (self.root / "src/bad.py").write_text("def broken(:\n")
        (self.outside / "bad.py").write_text("def broken(:\n")

    def invoke(self, hook, path=None, *, cwd=None, fix=False, payload=None,
               process_cwd=None, field="file_path"):
        if payload is None:
            payload = {
                "tool_name": "NotebookEdit" if field == "notebook_path" else "Write",
                "tool_input": {field: str(path)},
                "cwd": str(self.root if cwd is None else cwd),
            }
        environment = os.environ.copy()
        environment.pop("INTENT_TASK", None)
        if fix:
            environment["INTENT_TASK"] = "fix"
        return subprocess.run(
            ["/bin/bash", str(self.hooks / hook)],
            input=json.dumps(payload), text=True, capture_output=True,
            cwd=self.outside if process_cwd is None else process_cwd,
            env=environment, check=False,
        )

    def verdict(self, expected, hook, path=None, **kwargs):
        result = self.invoke(hook, path, **kwargs)
        self.assertEqual(result.returncode, expected, result.stderr)
        if expected == 2:
            self.assertIn("Route:", result.stderr)
        return result

    def test_protected_absolute_relative_and_dot_paths(self):
        for path in (
            "./.github/workflows/new.yml",
            "src/../Makefile",
            str(self.root / "src/../.claude/hooks/new.sh"),
            "./.claude/./settings.json",
            ".github/new/../new/deep/workflow.yml",
        ):
            with self.subTest(path=path):
                self.verdict(2, "protect-paths.sh", path)

    def test_payload_cwd_controls_relative_paths(self):
        self.verdict(2, "protect-paths.sh", "../Makefile", cwd=self.root / "src")
        self.verdict(2, "protect-tests.sh", "test_new.py", cwd=self.root / "tests", fix=True)
        self.verdict(0, "protect-paths.sh", "ok.py", cwd=self.root / "src")

    def test_fix_task_dot_paths_and_notebook_paths(self):
        for path in ("./tests/new.py", "src/../tests/deep/new.py",
                     str(self.root / "src/../tests/new.py")):
            with self.subTest(path=path):
                self.verdict(2, "protect-tests.sh", path, fix=True)
        self.verdict(2, "protect-tests.sh", "./tests/new.ipynb", fix=True,
                     field="notebook_path")

    def test_links_into_protected_directories_and_missing_destinations(self):
        (self.root / "src/ci").symlink_to("../.github", target_is_directory=True)
        (self.root / "src/test-alias").symlink_to("../tests", target_is_directory=True)
        (self.root / "src/future").symlink_to("../.github/not-yet-created", target_is_directory=True)
        self.verdict(2, "protect-paths.sh", "src/ci/workflows/new.yml")
        self.verdict(2, "protect-paths.sh", "src/future/deep/new.yml")
        self.verdict(2, "protect-tests.sh", "src/test-alias/new.py", fix=True)

    def test_file_link_and_symlink_before_parent_component(self):
        (self.root / "src/build").symlink_to("../Makefile")
        (self.root / "src/jump").symlink_to("../.github/workflows", target_is_directory=True)
        self.verdict(2, "protect-paths.sh", "src/build")
        self.verdict(2, "protect-paths.sh", "src/jump/../new.yml")

    def test_protected_lexical_paths_stay_protected_when_links_point_out(self):
        (self.root / ".claude/settings.json").symlink_to(self.outside / "settings.json")
        (self.root / "tests/escape").symlink_to(self.outside, target_is_directory=True)
        self.verdict(2, "protect-paths.sh", ".claude/settings.json")
        self.verdict(2, "protect-tests.sh", "tests/escape/new.py", fix=True)

    def test_checkout_alias_preserves_protected_lexical_path(self):
        alias = self.base / "checkout-alias"
        alias.symlink_to(self.root, target_is_directory=True)
        (self.root / ".claude/settings.json").symlink_to(self.outside / "settings.json")
        (self.root / "tests/escape").symlink_to(self.outside, target_is_directory=True)
        self.verdict(2, "protect-paths.sh", alias / ".claude/settings.json")
        self.verdict(2, "protect-tests.sh", alias / "tests/escape/new.py", fix=True)
        self.verdict(2, "protect-tests.sh", "new.py", cwd=alias / "tests/escape", fix=True)
        self.verdict(0, "protect-paths.sh", alias / "src/ok.py")

    def test_unprotected_new_paths_and_parent_components_pass(self):
        for path in ("src/new/deep/file.py", "tests/../src/new.py", "src/with space.py",
                     str(self.outside / "new.py"), ".github-other/new.py"):
            with self.subTest(path=path):
                self.verdict(0, "protect-paths.sh", path)
                self.verdict(0, "protect-tests.sh", path, fix=True)
        self.verdict(0, "protect-tests.sh", "tests/new.py")

    def test_unprotected_links_and_dangling_links_pass(self):
        (self.root / "src/alias").symlink_to(self.outside, target_is_directory=True)
        (self.root / "src/future").symlink_to("new-parent/new.py")
        self.verdict(0, "protect-paths.sh", "src/alias/new.py")
        self.verdict(0, "protect-paths.sh", "src/future")

    def test_symlink_loop_and_non_directory_ancestor_fail_closed(self):
        (self.root / "src/loop-a").symlink_to("loop-b")
        (self.root / "src/loop-b").symlink_to("loop-a")
        for path in ("src/loop-a/new.py", "src/ok.py/new.py"):
            with self.subTest(path=path):
                self.verdict(2, "protect-paths.sh", path)
                self.verdict(2, "protect-tests.sh", path, fix=True)

    def test_malformed_paths_fail_closed(self):
        for path in (None, False, 42, [], {}, "", "src/new\n.py", "src/new\x00.py", "src/\ud800.py"):
            payload = {"tool_name": "Write", "tool_input": {"file_path": path}, "cwd": str(self.root)}
            with self.subTest(path=repr(path)):
                self.verdict(2, "protect-paths.sh", payload=payload)
                self.verdict(2, "protect-tests.sh", payload=payload, fix=True)

    def test_missing_edit_target_and_malformed_payload_fail_closed(self):
        for payload in ([], "Write", {"tool_name": "Write", "tool_input": {}},
                        {"tool_name": "Edit", "tool_input": "Makefile"}):
            with self.subTest(payload=payload):
                self.verdict(2, "protect-paths.sh", payload=payload)

    def test_malformed_or_unresolvable_cwd_fails_closed(self):
        (self.root / "src/loop").symlink_to("loop")
        for cwd in (None, 12, [], "src", "", str(self.root / "missing"),
                    str(self.root / "src/ok.py"), str(self.root / "src/loop")):
            payload = {"tool_name": "Write", "tool_input": {"file_path": "new.py"}, "cwd": cwd}
            with self.subTest(cwd=cwd):
                self.verdict(2, "protect-paths.sh", payload=payload)

    def test_absent_cwd_uses_hook_working_directory(self):
        payload = {"tool_name": "Write", "tool_input": {"file_path": "../Makefile"}}
        self.verdict(2, "protect-paths.sh", payload=payload, process_cwd=self.root / "src")

    def test_format_lint_checks_actual_relative_and_external_file(self):
        self.verdict(2, "format-lint.sh", "bad.py", cwd=self.root / "src")
        self.verdict(2, "format-lint.sh", self.outside / "bad.py")
        (self.root / "src/alias.txt").symlink_to("bad.py")
        self.verdict(2, "format-lint.sh", "src/alias.txt")
        self.verdict(0, "format-lint.sh", "ok.py", cwd=self.root / "src")

    def test_bash_without_file_target_keeps_existing_behavior(self):
        self.verdict(0, "production-gate.sh", payload={
            "tool_name": "Bash", "tool_input": {"command": "git status"}, "cwd": str(self.root),
        })

    def require_case_insensitive_filesystem(self):
        alternate = self.root / ".GITHUB"
        if not alternate.exists() or not alternate.samefile(self.root / ".github"):
            self.skipTest("this filesystem does not alias differently-cased names")

    def test_filesystem_case_aliases_protect_future_paths(self):
        self.require_case_insensitive_filesystem()
        (self.root / "Makefile").write_text("all:\n\ttrue\n")
        for path in (".GITHUB/workflows/new.yml", ".GITHUB/future/deep/new.yml",
                     ".CLAUDE/HOOKS/new.sh", "MAKEFILE"):
            with self.subTest(path=path):
                self.verdict(2, "protect-paths.sh", path)
        self.verdict(2, "protect-tests.sh", "TESTS/future/new.py", fix=True)
        self.verdict(2, "protect-tests.sh", "new.py", cwd=self.root / "TESTS", fix=True)
        self.verdict(0, "protect-paths.sh", "SRC/future/new.py")

    def test_filesystem_case_aliases_preserve_outgoing_protected_links(self):
        self.require_case_insensitive_filesystem()
        (self.root / ".claude/settings.json").symlink_to(self.outside / "future.json")
        (self.root / "tests/escape").symlink_to(self.outside, target_is_directory=True)
        self.verdict(2, "protect-paths.sh", ".CLAUDE/SETTINGS.JSON")
        self.verdict(2, "protect-tests.sh", "TESTS/ESCAPE/new.py", fix=True)
        self.verdict(2, "protect-paths.sh", self.root.with_name("CHECKOUT") / ".CLAUDE/SETTINGS.JSON")

    def test_format_lint_checks_filesystem_case_alias_extension(self):
        self.require_case_insensitive_filesystem()
        self.verdict(2, "format-lint.sh", "SRC/BAD.PY")
        self.verdict(0, "format-lint.sh", "SRC/OK.PY")

    def test_case_sensitive_distinct_directories_remain_unprotected(self):
        if (self.root / ".GITHUB").exists():
            self.skipTest("this filesystem aliases differently-cased directories")
        for directory in (".GITHUB", "TESTS", ".CLAUDE/HOOKS"):
            (self.root / directory).mkdir(parents=True)
        self.verdict(0, "protect-paths.sh", ".GITHUB/future/new.yml")
        self.verdict(0, "protect-paths.sh", ".CLAUDE/HOOKS/future.sh")
        self.verdict(0, "protect-tests.sh", "TESTS/future/new.py", fix=True)


if __name__ == "__main__":
    unittest.main()
