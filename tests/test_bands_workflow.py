"""R4/R5 — bands 등급별 실행, 읽기 전용 모델 경계, 실패 전파를 검증한다."""
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parent.parent
RUNNER = ROOT / "scripts" / "run_bands.py"


def detection(tier):
    actions = {"none": None, "1sigma": "log", "2sigma": "diagnose", "3sigma": "propose"}
    rules = {"none": None, "1sigma": None, "2sigma": "rule2_nine_points_one_side",
             "3sigma": "rule1_one_point_beyond_3sigma"}
    data = {
        "schema_version": 1,
        "metric": "ci_test_failure_rate",
        "detected_at": "2026-09-10T05:00:00+00:00",
        "tier": tier,
        "action": actions[tier],
        "rule": rules[tier],
        "rules_fired": [rules[tier]] if rules[tier] else [],
        "reason": None,
        "z": 4.2 if tier == "3sigma" else 1.5,
        "mean": 0.05,
        "sigma": 0.004,
        "n": 24,
        "observed": {"ts": "2026-09-10T00:00:00Z", "value": 0.075},
        "evidence": {"window": [], "evaluated": [], "rules_enabled": []},
    }
    if tier == "2sigma":
        data["tools"] = "Read,Grep"
    if tier == "3sigma":
        data["routes"] = ["pull_request"]
    return data


class BandsWorkflowTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = pathlib.Path(self.tmp.name)
        self.input = self.base / "detection.json"
        self.out = self.base / "out"
        self.args_file = self.base / "claude-args.json"
        self.fake = self.base / "fake-claude"
        self.fake.write_text(
            "#!/usr/bin/env python3\n"
            "import json, os, sys\n"
            "open(os.environ['FAKE_CLAUDE_ARGS'], 'w').write(json.dumps(sys.argv[1:]))\n"
            "sys.stderr.write(os.environ.get('FAKE_CLAUDE_STDERR', ''))\n"
            "if os.environ.get('FAKE_CLAUDE_FAIL'):\n"
            "    sys.exit(int(os.environ['FAKE_CLAUDE_FAIL']))\n"
            "inner = {'evidence': 'repository evidence', "
            "'open_questions': ['which change caused it?']}\n"
            "result = os.environ.get('FAKE_CLAUDE_RESULT', json.dumps(inner))\n"
            "envelope = {'result': result}\n"
            "if os.environ.get('FAKE_CLAUDE_IS_ERROR'):\n"
            "    envelope.update({'is_error': True, 'subtype': 'error_during_execution'})\n"
            "print(os.environ.get('FAKE_CLAUDE_ENVELOPE', json.dumps(envelope)))\n",
            encoding="utf-8",
        )
        self.fake.chmod(0o755)

    def tearDown(self):
        self.tmp.cleanup()

    def run_tier(self, tier, key="test-key", extra=None, env_extra=None):
        self.input.write_text(json.dumps(detection(tier)), encoding="utf-8")
        cmd = [sys.executable, str(RUNNER), "--input", str(self.input),
               "--out", str(self.out), "--id", "9999-band-test",
               "--claude", str(self.fake)]
        if extra:
            cmd.extend(extra)
        env = os.environ.copy()
        env["FAKE_CLAUDE_ARGS"] = str(self.args_file)
        if key is None:
            env.pop("ANTHROPIC_API_KEY", None)
        else:
            env["ANTHROPIC_API_KEY"] = key
        if env_extra:
            env.update(env_extra)
        return subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True)

    def record(self):
        return json.loads((self.out / "run.json").read_text(encoding="utf-8"))

    def intent(self):
        return (self.out / "9999-band-test" / "intent.md").read_text(encoding="utf-8")

    def test_none_and_1sigma_record_without_model_or_draft(self):
        for tier in ("none", "1sigma"):
            with self.subTest(tier=tier):
                p = self.run_tier(tier)
                self.assertEqual(p.returncode, 0, p.stderr)
                self.assertEqual(self.record()["status"], "recorded")
                self.assertEqual(self.record()["tier"], tier)
                self.assertEqual(self.record()["model"], "not_required")
                self.assertFalse(self.args_file.exists())
                self.assertFalse((self.out / "9999-band-test").exists())
                if self.out.exists():
                    for child in self.out.iterdir():
                        if child.name != "run.json" and child.is_file():
                            child.unlink()

    def test_2sigma_diagnoses_without_model_write_tools_or_existing_draft(self):
        p = self.run_tier("2sigma")
        self.assertEqual(p.returncode, 0, p.stderr)
        args = json.loads(self.args_file.read_text(encoding="utf-8"))
        self.assertEqual(args[args.index("--tools") + 1], "Read,Grep")
        self.assertEqual(args[args.index("--allowedTools") + 1], "Read,Grep")
        self.assertFalse(any("Write" in arg or "Edit" in arg for arg in args))
        prompt = args[args.index("-p") + 1]
        self.assertNotIn("intent draft", prompt)
        self.assertIn(str(self.input), prompt)
        text = self.intent()
        self.assertIn("repository evidence", text)
        self.assertIn("which change caused it?", text)
        self.assertEqual(self.record()["status"], "diagnosed")
        self.assertNotIn("routes", self.record())

    def test_3sigma_creates_proposal_with_diagnosis(self):
        p = self.run_tier("3sigma")
        self.assertEqual(p.returncode, 0, p.stderr)
        text = self.intent()
        self.assertIn("repository evidence", text)
        self.assertIn("which change caused it?", text)
        self.assertEqual(self.record()["status"], "proposal_drafted")
        self.assertEqual(self.record()["routes"], ["pull_request"])

    def test_3sigma_without_key_keeps_draft_and_records_skipped_diagnosis(self):
        p = self.run_tier("3sigma", key=None)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertFalse(self.args_file.exists())
        self.assertIn("ANTHROPIC_API_KEY", self.intent())
        self.assertEqual(self.record()["model"], "skipped_no_api_key")
        self.assertEqual(self.record()["status"], "proposal_drafted")

    def test_model_failure_is_nonzero_and_recorded(self):
        p = self.run_tier("2sigma", env_extra={"FAKE_CLAUDE_FAIL": "7",
                                                "FAKE_CLAUDE_STDERR": "model failed"})
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(self.record()["status"], "model_failed")
        self.assertIn("model failed", (self.out / "model-error.txt").read_text(encoding="utf-8"))

    def test_zero_exit_model_error_envelope_is_nonzero_and_recorded(self):
        p = self.run_tier("2sigma", env_extra={"FAKE_CLAUDE_IS_ERROR": "1"})
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(self.record()["status"], "model_failed")
        self.assertEqual(self.record()["model"], "failed")

    def test_model_artifact_write_failure_updates_run_record(self):
        self.out.mkdir()
        (self.out / "model-output.json").mkdir()
        p = self.run_tier("2sigma")
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(self.record()["status"], "model_artifact_write_failed")
        self.assertEqual(self.record()["model"], "failed")

    def test_invalid_diagnosis_is_nonzero_and_preserves_raw_output(self):
        p = self.run_tier("3sigma", env_extra={"FAKE_CLAUDE_RESULT": "not-json"})
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(self.record()["status"], "diagnosis_invalid")
        self.assertTrue((self.out / "model-output.json").exists())

    def test_non_object_model_envelope_is_invalid_and_recorded(self):
        p = self.run_tier("3sigma", env_extra={"FAKE_CLAUDE_ENVELOPE": "[]"})
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(self.record()["status"], "diagnosis_invalid")
        self.assertEqual(self.record()["model"], "invalid_output")

    def test_draft_failure_is_nonzero_and_recorded(self):
        broken = self.base / "broken-emitter.py"
        broken.write_text("import sys\nsys.exit(9)\n", encoding="utf-8")
        p = self.run_tier("3sigma", extra=["--emit-script", str(broken)])
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(self.record()["status"], "draft_failed")

    def test_record_failure_is_nonzero(self):
        self.input.write_text(json.dumps(detection("none")), encoding="utf-8")
        self.out.write_text("not a directory", encoding="utf-8")
        p = subprocess.run(
            [sys.executable, str(RUNNER), "--input", str(self.input), "--out", str(self.out),
             "--id", "9999-band-test", "--claude", str(self.fake)],
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("기록", p.stderr)


if __name__ == "__main__":
    unittest.main()
