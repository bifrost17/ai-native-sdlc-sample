"""Dataset v1 baseline contract: existing list/show/complete behavior stays observable."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


def _load_tracker_module():
    spec = importlib.util.spec_from_file_location("tracker_under_test", ROOT / "tracker.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExistingTrackerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name) / "requests.json"
        self.data.write_bytes((ROOT / "requests.json").read_bytes())
        self.original = json.loads(self.data.read_text(encoding="utf-8"))

    def invoke(self, *args):
        return subprocess.run([sys.executable, str(ROOT / "tracker.py"), "--data", str(self.data), *args],
                              capture_output=True, text=True, check=False)

    def test_list_preserves_order_and_does_not_write(self):
        before = self.data.read_bytes()
        result = self.invoke("list")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([line.split("\t")[0] for line in result.stdout.splitlines()],
                         [row["id"] for row in self.original["requests"]])
        self.assertEqual(self.data.read_bytes(), before)

    def test_list_owner_filters_and_keeps_order_including_done(self):
        before = self.data.read_bytes()
        result = self.invoke("list", "--owner", "hana")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([line.split("\t")[0] for line in result.stdout.splitlines()], ["R-101", "R-103"])
        self.assertEqual(self.data.read_bytes(), before)

    def test_list_owner_unknown_or_mismatched_case_is_empty(self):
        for owner in ("HANA", "nobody"):
            result = self.invoke("list", "--owner", owner)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")

    def test_summary_all_and_by_owner(self):
        before = self.data.read_bytes()
        result = self.invoke("summary")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "open\t3\ndone\t1\n")
        result = self.invoke("summary", "--owner", "hana")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "open\t1\ndone\t1\n")
        self.assertEqual(self.data.read_bytes(), before)

    def test_summary_owner_unknown_is_zero(self):
        result = self.invoke("summary", "--owner", "nobody")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "open\t0\ndone\t0\n")

    def test_summary_reflects_completed_status_in_copy(self):
        self.invoke("complete", "R-101")
        result = self.invoke("summary", "--owner", "hana")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "open\t0\ndone\t2\n")

    def test_summary_output_writes_file_and_empties_stdout(self):
        before = self.data.read_bytes()
        output_path = Path(self.temp.name) / "summary.txt"
        result = self.invoke("summary", "--output", str(output_path))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(output_path.read_text(encoding="utf-8"), "open\t3\ndone\t1\n")
        self.assertEqual(self.data.read_bytes(), before)

        owner_output_path = Path(self.temp.name) / "summary-hana.txt"
        result = self.invoke("summary", "--owner", "hana", "--output", str(owner_output_path))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(owner_output_path.read_text(encoding="utf-8"), "open\t1\ndone\t1\n")

    def test_summary_output_does_not_overwrite_existing_file(self):
        output_path = Path(self.temp.name) / "summary.txt"
        output_path.write_text("existing content", encoding="utf-8")
        before_data = self.data.read_bytes()
        result = self.invoke("summary", "--output", str(output_path))
        self.assertEqual(result.returncode, 2)
        self.assertIn("already exists", result.stderr)
        self.assertEqual(output_path.read_text(encoding="utf-8"), "existing content")
        self.assertEqual(self.data.read_bytes(), before_data)

    def test_summary_output_preserves_file_created_between_check_and_write(self):
        """Regression for TOCTOU: simulate another process creating --output's path at the
        instant the tracker attempts to open it, and require the existing content survive.
        Uses an in-process call with a patched Path.open (deterministic, not timing-based) so
        this fails against a check-then-write implementation and passes against an atomic one.
        """
        tracker = _load_tracker_module()
        output_path = Path(self.temp.name) / "race-summary.txt"
        sentinel = "existing content from a concurrent writer\n"
        original_open = Path.open
        triggered = {"done": False}

        def racy_open(self_path, *args, **kwargs):
            if not triggered["done"] and self_path == output_path:
                triggered["done"] = True
                with original_open(self_path, "w", encoding="utf-8") as handle:
                    handle.write(sentinel)
            return original_open(self_path, *args, **kwargs)

        stdout, stderr = io.StringIO(), io.StringIO()
        with mock.patch.object(Path, "open", racy_open):
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exit_code = tracker.main(["--data", str(self.data), "summary", "--output", str(output_path)])

        self.assertTrue(triggered["done"], "race simulation never triggered — test is not exercising the write path")
        self.assertEqual(exit_code, 2)
        self.assertIn("already exists", stderr.getvalue())
        self.assertEqual(output_path.read_text(encoding="utf-8"), sentinel)

    def test_summary_output_missing_parent_directory_fails(self):
        output_path = Path(self.temp.name) / "missing-dir" / "summary.txt"
        before_data = self.data.read_bytes()
        result = self.invoke("summary", "--output", str(output_path))
        self.assertEqual(result.returncode, 2)
        self.assertNotEqual(result.stderr, "")
        self.assertFalse(output_path.exists())
        self.assertEqual(self.data.read_bytes(), before_data)

    def test_show_existing_and_missing_id(self):
        row = self.original["requests"][0]
        result = self.invoke("show", row["id"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.split("\t")[0], row["id"])
        missing = self.invoke("show", "R-999")
        self.assertEqual(missing.returncode, 1)
        self.assertIn("Request not found", missing.stderr)

    def test_complete_changes_only_target_status_and_is_repeatable(self):
        target = self.original["requests"][0]["id"]
        result = self.invoke("complete", target)
        self.assertEqual(result.returncode, 0, result.stderr)
        expected = self.original
        expected["requests"][0]["status"] = "done"
        self.assertEqual(json.loads(self.data.read_text(encoding="utf-8")), expected)
        before_repeat = self.data.read_bytes()
        self.assertEqual(self.invoke("complete", target).returncode, 0)
        self.assertEqual(self.data.read_bytes(), before_repeat)


if __name__ == "__main__":
    unittest.main()
