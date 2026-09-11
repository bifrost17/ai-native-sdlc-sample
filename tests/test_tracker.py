"""Dataset v1 baseline contract: existing list/show/complete behavior stays observable."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


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

    def test_summary_counts_all_requests_including_unassigned(self):
        before = self.data.read_bytes()
        result = self.invoke("summary")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), ["open\t3", "done\t1"])
        self.assertEqual(self.data.read_bytes(), before)

    def test_summary_owner_counts_only_that_owner(self):
        result = self.invoke("summary", "--owner", "hana")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), ["open\t1", "done\t1"])

    def test_summary_owner_unknown_is_zero(self):
        result = self.invoke("summary", "--owner", "nobody")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), ["open\t0", "done\t0"])

    def test_summary_owner_reflects_completed_copy(self):
        self.invoke("complete", "R-101")
        result = self.invoke("summary", "--owner", "hana")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), ["open\t0", "done\t2"])

    def test_summary_json_counts_all_requests(self):
        before = self.data.read_bytes()
        result = self.invoke("summary", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"open": 3, "done": 1})
        self.assertEqual(self.data.read_bytes(), before)

    def test_summary_json_owner_counts_only_that_owner(self):
        result = self.invoke("summary", "--owner", "hana", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"open": 1, "done": 1})

    def test_summary_json_owner_unknown_or_mismatched_case_is_zero(self):
        for owner in ("HANA", "nobody"):
            result = self.invoke("summary", "--owner", owner, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout), {"open": 0, "done": 0})

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
