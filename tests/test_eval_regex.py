"""0014 R1/AC1: grep match, miss, and execution errors remain distinct verdicts."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "evals/check.sh"


class EvalRegexTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="eval-regex-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.workspace = self.base / "ws"
        self.workspace.mkdir()
        self.target = self.workspace / "output.txt"
        self.target.write_text("alpha 42\n-TOKEN42\n", encoding="utf-8")
        self.case = self.base / "case.json"
        self.result = self.base / "result.json"
        self.result.write_text(json.dumps({"workspace": "ws"}), encoding="utf-8")

    def check(self, kind, value="alpha", *, environment=None, checks=None):
        if checks is None:
            field = "pattern" if kind.startswith("regex_") else "value"
            checks = [{"kind": kind, "path": "output.txt", field: value}]
        self.case.write_text(json.dumps({"id": "regex-contract", "checks": checks}), encoding="utf-8")
        return subprocess.run(
            ["/bin/bash", str(CHECKER), str(self.case), str(self.result)],
            capture_output=True, text=True, env=environment, check=False,
        )

    def assert_undecidable(self, result):
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("UNDECIDABLE", result.stderr)
        self.assertNotIn("  PASS", result.stdout)

    def test_invalid_regex_is_undecidable_for_both_kinds(self):
        for kind in ("regex_present", "regex_absent"):
            for pattern in ("[", "("):
                with self.subTest(kind=kind, pattern=pattern):
                    self.assert_undecidable(self.check(kind, pattern))

    def test_valid_ere_match_and_miss_keep_original_verdicts(self):
        for kind, match_rc, miss_rc in (("regex_present", 0, 1), ("regex_absent", 1, 0)):
            with self.subTest(kind=kind, matching=True):
                result = self.check(kind, r"^alpha [[:digit:]]{2}$|^never$")
                self.assertEqual(result.returncode, match_rc, result.stdout + result.stderr)
            with self.subTest(kind=kind, matching=False):
                result = self.check(kind, r"^beta [[:digit:]]+$")
                self.assertEqual(result.returncode, miss_rc, result.stdout + result.stderr)

    def test_leading_hyphen_regex_is_a_pattern_not_an_option(self):
        for kind, match_rc, miss_rc in (("regex_present", 0, 1), ("regex_absent", 1, 0)):
            for pattern, expected in (("-TOKEN[[:digit:]]{2}", match_rc), ("-MISSING", miss_rc)):
                with self.subTest(kind=kind, pattern=pattern):
                    result = self.check(kind, pattern)
                    self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_fixed_string_match_and_miss_keep_original_verdicts(self):
        for kind, match_rc, miss_rc in (("contains", 0, 1), ("not_contains", 1, 0)):
            for value, expected in (("-TOKEN42", match_rc), ("[missing]", miss_rc)):
                with self.subTest(kind=kind, value=value):
                    result = self.check(kind, value)
                    self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_grep_execution_errors_are_undecidable_for_all_search_kinds(self):
        binary = self.base / "bin"
        binary.mkdir()
        fake = binary / "grep"
        environment = dict(os.environ, PATH=str(binary) + os.pathsep + os.environ["PATH"])
        for code in (2, 7):
            fake.write_text("#!/bin/bash\nprintf 'simulated read failure\\n' >&2\nexit %d\n" % code)
            fake.chmod(0o755)
            for kind in ("regex_present", "regex_absent", "contains", "not_contains"):
                with self.subTest(kind=kind, grep_rc=code):
                    self.assert_undecidable(self.check(kind, environment=environment))

    def test_missing_grep_is_undecidable(self):
        binary = self.base / "bin"
        binary.mkdir()
        (binary / "jq").symlink_to(shutil.which("jq"))
        environment = dict(os.environ, PATH=str(binary))
        for kind in ("regex_present", "regex_absent", "contains", "not_contains"):
            with self.subTest(kind=kind):
                self.assert_undecidable(self.check(kind, environment=environment))

    def test_unreadable_regular_file_is_undecidable(self):
        self.target.chmod(0)
        self.addCleanup(self.target.chmod, 0o600)
        if os.access(self.target, os.R_OK):
            self.skipTest("current user can read files despite mode 000")
        for kind in ("regex_present", "regex_absent", "contains", "not_contains"):
            with self.subTest(kind=kind):
                self.assert_undecidable(self.check(kind))

    def test_error_takes_precedence_over_an_earlier_failed_check(self):
        result = self.check("regex_absent", checks=[
            {"kind": "regex_present", "path": "output.txt", "pattern": "missing"},
            {"kind": "regex_absent", "path": "output.txt", "pattern": "["},
        ])
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("  FAIL  [0]", result.stdout)
        self.assertIn("UNDECIDABLE", result.stderr)

    def test_missing_target_and_file_exists_contract_stays_unchanged(self):
        self.target.unlink()
        for kind in ("file_exists", "regex_present", "regex_absent", "contains", "not_contains"):
            with self.subTest(kind=kind):
                result = self.check(kind)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
