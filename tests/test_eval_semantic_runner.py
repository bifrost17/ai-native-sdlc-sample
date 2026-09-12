"""0014 R4-R6 / AC3: canonical full evals run both graders and preserve outcomes."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
GENERATOR = r'''#!/usr/bin/env python3
import json, os, pathlib, re, sys
args = sys.argv[1:]
prompt = args[args.index("-p")+1]
ws = pathlib.Path(re.search(r"Evaluation workspace \(absolute\): (.+)", prompt).group(1))
cid = ws.parent.name
with open(os.environ["CALL_LOG"], "a") as f:
 f.write(json.dumps({"role":"generator","id":cid,"args":args})+"\n")
if os.environ.get("GEN_FAIL") == cid: sys.exit(17)
(ws/"output.md").write_text("wrong" if os.environ.get("BAD_OUTPUT")==cid else "completed")
events = [
 {"type":"system","subtype":"init","skills":[],"plugins":[]},
 {"type":"assistant","message":{"content":[{"type":"tool_use","id":"read1","name":"Read","input":{"file_path":str(ws/"input.md")}}]}},
 {"type":"user","message":{"content":[{"type":"tool_result","tool_use_id":"read1","content":"input"}]}},
 {"type":"result","subtype":"success","is_error":False,"result":"completed"}
]
if os.environ.get("BAD_TRACE") == cid: events.pop()
if os.environ.get("ERROR_ENVELOPE") == cid: events[-1]["is_error"]=True
for event in events: print(json.dumps(event))
'''
GRADER = r'''import argparse,json,os,pathlib,sys
p=argparse.ArgumentParser()
for key in ("case","result","trace","out"): p.add_argument("--"+key,required=True)
p.add_argument("--edition", choices=("tdd-first","tdd-optional"), default="tdd-first")
a=p.parse_args()
cid=json.loads(pathlib.Path(a.case).read_text())["id"]
with open(os.environ["CALL_LOG"],"a") as f:
 f.write(json.dumps({"role":"grader","id":cid,"trace":a.trace})+"\n")
rc=1 if os.environ.get("GRADE_FAIL")==cid else 0
pathlib.Path(a.out).write_text(json.dumps({"case_id":cid,"rc":rc}))
sys.exit(rc)
'''


class SemanticRunner(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="semantic runner ")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name).resolve()
        self.evals = self.repo / "evals"
        shutil.copytree(ROOT / "evals", self.evals,
                        ignore=shutil.ignore_patterns("out", "cases", "fixtures", "__pycache__"))
        (self.evals / "cases").mkdir()
        (self.evals / "fixtures").mkdir()
        for cid in ("01-a", "02-b"):
            fixture = self.evals / "fixtures" / cid
            fixture.mkdir()
            (fixture / "input.md").write_text("input")
            case = {"schema_version": 1, "id": cid,
                    "prompt": "Read evals/out/%s/ws/input.md and write output.md." % cid,
                    "files": ["evals/fixtures/%s/input.md" % cid],
                    "expected_output": "completed", "assertions": ["The job is completed"],
                    "allowed_tools": "Read,Write",
                    "checks": [{"kind": "contains", "path": "output.md", "value": "completed"}]}
            (self.evals / "cases" / (cid + ".json")).write_text(json.dumps(case))
        for edition in ("tdd-first", "tdd-optional"):
            project = self.repo / edition / "project"
            project.mkdir(parents=True)
            (project / "CLAUDE.md").write_text("selected product guidance")
            manifest = self.repo / edition / "org-skills/.claude-plugin/plugin.json"
            manifest.parent.mkdir(parents=True)
            manifest.write_text('{"name":"test-plugin","version":"0.0.1"}')
        (self.evals / "grade_assertions.py").write_text(GRADER)
        binary = self.repo / "bin"
        binary.mkdir()
        cli = binary / "claude"
        cli.write_text(GENERATOR)
        cli.chmod(0o755)
        self.log = self.repo / "calls.jsonl"
        self.env = dict(os.environ, PATH=str(binary) + os.pathsep + os.environ["PATH"],
                        CALL_LOG=str(self.log), ANTHROPIC_API_KEY="fake-never-sent")

    def run_suite(self, **extra):
        return subprocess.run(["bash", "evals/run.sh", "--semantic"], cwd=self.repo,
                              env=dict(self.env, **extra), capture_output=True, text=True)

    def summaries(self):
        return sorted((self.evals / "out").glob("*/semantic-*/summary.json"))

    def summary(self):
        paths = self.summaries()
        self.assertEqual(len(paths), 1)
        return json.loads(paths[0].read_text())

    def calls(self):
        return [json.loads(line) for line in self.log.read_text().splitlines()]

    def test_full_mode_calls_both_graders_and_records_every_case(self):
        p = self.run_suite()
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        summary = self.summary()
        self.assertEqual(summary["edition"], "tdd-first")
        self.assertEqual(summary["counts"], {"pass": 2, "fail": 0, "undecidable": 0})
        self.assertEqual(summary["pass_rate"], 1)
        self.assertEqual([(c["role"], c["id"]) for c in self.calls()],
                         [("generator", "01-a"), ("grader", "01-a"),
                          ("generator", "02-b"), ("grader", "02-b")])
        for call in self.calls():
            if call["role"] != "generator":
                continue
            args = call["args"]
            for flag, value in (("--model", "sonnet"), ("--effort", "low"),
                                ("--output-format", "stream-json")):
                self.assertEqual(args[args.index(flag) + 1], value)
            self.assertIn("--no-session-persistence", args)
            self.assertIn("--verbose", args)
            self.assertEqual(args[args.index("--setting-sources") + 1], "")
            self.assertIn("--bare", args, "Maker CLAUDE auto-discovery must be disabled")
            self.assertEqual(args[args.index("--plugin-dir") + 1],
                             str(self.repo / "tdd-first/org-skills"))

    def test_editions_have_separate_output_and_plugin_paths(self):
        for edition in ("tdd-first", "tdd-optional"):
            p = self.run_suite(SDLC_EDITION=edition)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        summaries = self.summaries()
        self.assertEqual({json.loads(path.read_text())["edition"] for path in summaries},
                         {"tdd-first", "tdd-optional"})
        calls = self.calls()
        for edition in ("tdd-first", "tdd-optional"):
            expected = str(self.repo / edition / "org-skills")
            self.assertTrue(any(call["role"] == "generator" and
                                call["args"][call["args"].index("--plugin-dir") + 1] == expected
                                for call in calls))

    def test_semantic_failure_cannot_hide_behind_string_matches(self):
        p = self.run_suite(GRADE_FAIL="01-a")
        self.assertEqual(p.returncode, 1, p.stdout + p.stderr)
        summary = self.summary()
        self.assertEqual(summary["counts"], {"pass": 1, "fail": 1, "undecidable": 0})
        self.assertEqual(summary["pass_rate"], 0.5)
        self.assertEqual(summary["cases"][0]["deterministic_rc"], 0)
        self.assertEqual(summary["cases"][0]["semantic_rc"], 1)

    def test_deterministic_failure_does_not_skip_semantic_grading(self):
        p = self.run_suite(BAD_OUTPUT="01-a")
        self.assertEqual(p.returncode, 1, p.stdout + p.stderr)
        self.assertIn(("grader", "01-a"), [(c["role"], c["id"]) for c in self.calls()])
        self.assertEqual(self.summary()["cases"][0]["semantic_rc"], 0)

    def test_generation_error_is_undecidable_and_next_case_still_runs(self):
        p = self.run_suite(GEN_FAIL="01-a", GRADE_FAIL="02-b")
        self.assertEqual(p.returncode, 2, p.stdout + p.stderr)
        summary = self.summary()
        self.assertEqual(summary["total"], 2)
        self.assertEqual(summary["counts"], {"pass": 0, "fail": 1, "undecidable": 1})
        self.assertEqual(summary["pass_rate"], 0)
        self.assertNotIn(("grader", "01-a"), [(c["role"], c["id"]) for c in self.calls()])

    def test_incomplete_or_error_trace_is_undecidable(self):
        for option in ("BAD_TRACE", "ERROR_ENVELOPE"):
            with self.subTest(option=option):
                p = self.run_suite(**{option: "01-a"})
                self.assertEqual(p.returncode, 2, p.stdout + p.stderr)
                last = json.loads(self.summaries()[-1].read_text())
                self.assertEqual(last["counts"]["undecidable"], 1)

    def test_repeated_runs_keep_separate_records(self):
        for _ in range(2):
            p = self.run_suite()
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertEqual(len(self.summaries()), 2)

    def test_make_evals_selects_semantic_mode(self):
        p = subprocess.run(["make", "-n", "evals"], cwd=ROOT, env=self.env,
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("bash evals/run.sh --semantic", p.stdout)


if __name__ == "__main__":
    unittest.main()
