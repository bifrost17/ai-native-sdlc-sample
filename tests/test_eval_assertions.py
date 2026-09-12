"""0014 R2/R3: semantic assertion grader의 격리·근거·rc 계약을 검증한다."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parent.parent
GRADER = ROOT / "evals" / "grade_assertions.py"
FAKE = r'''#!/usr/bin/env python3
import json, os, sys
packet = json.load(sys.stdin)
log = {"args": sys.argv[1:], "cwd": os.getcwd(), "packet": packet}
open(os.environ["FAKE_LOG"], "w", encoding="utf-8").write(json.dumps(log))
mode = os.environ.get("FAKE_MODE", "pass")
if mode == "cli-error": sys.exit(19)
if mode == "malformed": print("not json"); sys.exit(0)
sources = packet["sources"]
source = sorted(sources)[0]
excerpt = sources[source][:12]
items = []
for i, assertion in enumerate(packet["assertions"]):
    result = "fail" if mode == "fail" else "undecidable" if mode == "undecidable" else "pass"
    items.append({"index": i, "result": result, "reason": "fake judgment",
                  "evidence": [{"source": source, "excerpt": excerpt}]})
if mode == "duplicate": items.append(dict(items[0]))
if mode == "missing": items = items[:-1]
if mode == "bad-evidence": items[0]["evidence"][0]["excerpt"] = "not in any source"
envelope = {"type": "result", "subtype": "success", "is_error": False,
            "session_id": "grader-session", "structured_output": {"assertions": items}}
if mode == "error-envelope": envelope.update({"subtype": "error", "is_error": True})
if mode == "same-session": envelope["session_id"] = "generator-session"
print(json.dumps(envelope))
'''


class AssertionGraderTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="assertion grader ")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.workspace = self.base / "out" / "case" / "ws"
        self.workspace.mkdir(parents=True)
        self.artifact = self.workspace / "spec.md"
        self.artifact.write_text("gateway JWT is named, but this sentence grants no authentication.\n",
                                 encoding="utf-8")
        self.case = self.base / "case.json"
        self.case.write_text(json.dumps({
            "schema_version": 1, "id": "case", "prompt": "write a spec",
            "expected_output": "authenticated endpoint", "files": [],
            "assertions": ["The endpoint actually requires authentication",
                           "The selected stage skill was read and applied, not merely named"],
            "checks": [{"kind": "file_exists", "path": "spec.md"}],
            "grading_context": [],
        }), encoding="utf-8")
        self.result = self.base / "out" / "case.json"
        self.result.write_text(json.dumps({
            "schema_version": 1, "case_id": "case", "workspace": "case/ws",
            "result": "generation complete",
            "claude_raw": {"type": "result", "subtype": "success", "is_error": False,
                           "session_id": "generator-session", "result": "generation complete"},
        }), encoding="utf-8")
        self.trace = self.base / "out" / "case.claude.jsonl"
        events = [
            {"type": "system", "subtype": "init", "session_id": "generator-session",
             "skills": ["design-spec", "plugin:policy-pass"],
             "plugins": [{"name": "plugin", "path": "/installed/plugin",
                          "source": "plugin@inline", "version": "1.2.3"}],
             "account": {"email": "must-not-leak@example.com"},
             "mcp_servers": [{"name": "must-not-leak"}]},
            {"type": "assistant", "session_id": "generator-session", "message": {
                "role": "assistant", "content": [{"type": "tool_use", "id": "tool-1",
                "name": "Read", "input": {"file_path": str(self.artifact)}}]}},
            {"type": "user", "session_id": "generator-session", "message": {
                "role": "user", "content": [{"type": "tool_result", "tool_use_id": "tool-1",
                "content": self.artifact.read_text(), "is_error": False}]}},
            {"type": "result", "subtype": "success", "is_error": False,
             "session_id": "generator-session", "result": "generation complete"},
        ]
        self.trace.write_text("".join(json.dumps(x) + "\n" for x in events), encoding="utf-8")
        self.output = self.base / "grade.json"
        self.fake = self.base / "claude"
        self.fake.write_text(FAKE, encoding="utf-8")
        self.fake.chmod(0o755)
        self.log = self.base / "call.json"

    def run_grader(self, mode="pass", edition="tdd-first"):
        env = dict(os.environ, FAKE_LOG=str(self.log), FAKE_MODE=mode)
        return subprocess.run([
            sys.executable, str(GRADER), "--case", str(self.case), "--result", str(self.result),
            "--trace", str(self.trace), "--out", str(self.output), "--claude", str(self.fake),
            "--edition", edition,
        ], cwd=ROOT, env=env, text=True, capture_output=True)

    def grade(self):
        return json.loads(self.output.read_text(encoding="utf-8"))

    def digest_inputs(self):
        return {str(path): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in (self.case, self.result, self.trace, self.artifact)}

    def test_pass_is_rc0_and_grader_has_no_tools_or_repo_settings(self):
        before = self.digest_inputs()
        p = self.run_grader()
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(self.digest_inputs(), before)
        grade = self.grade()
        self.assertEqual(grade["result"], "pass")
        self.assertEqual(grade["rc"], 0)
        self.assertEqual([x["index"] for x in grade["assertions"]], [0, 1])
        call = json.loads(self.log.read_text(encoding="utf-8"))
        args = call["args"]
        self.assertEqual(args[args.index("--model") + 1], "sonnet")
        self.assertEqual(args[args.index("--effort") + 1], "low")
        self.assertEqual(args[args.index("--tools") + 1], "")
        self.assertIn("--strict-mcp-config", args)
        self.assertIn("--disable-slash-commands", args)
        self.assertIn("--bare", args)
        self.assertEqual(args[args.index("--setting-sources") + 1], "")
        system_prompt = args[args.index("--system-prompt") + 1]
        self.assertIn("Do not require every catalog skill", system_prompt)
        self.assertIn("applicable skill", system_prompt)
        self.assertNotEqual(Path(call["cwd"]), ROOT)
        self.assertNotEqual(Path(call["cwd"]), self.workspace)
        self.assertIn("trace:tool:tool-1", call["packet"]["sources"])
        catalog = call["packet"]["sources"]["trace:catalog"]
        self.assertIn("skill: design-spec\n", catalog)
        self.assertIn("skill: plugin:policy-pass\n", catalog)
        self.assertIn("version=1.2.3", catalog)
        self.assertNotIn("account", catalog)
        self.assertNotIn("mcp_servers", catalog)
        self.assertTrue((self.base / "grade.packet.json").is_file())
        self.assertTrue((self.base / "grade.raw.json").is_file())

    def test_policy_prompt_and_grading_sources_use_the_selected_edition(self):
        policy = json.loads((ROOT / "evals/cases/04-org-policy-application.json").read_text())
        case = json.loads(self.case.read_text())
        case["prompt"] = policy["prompt"]
        case["grading_context"] = policy["grading_context"]
        self.case.write_text(json.dumps(case))
        for edition in ("tdd-first", "tdd-optional"):
            with self.subTest(edition=edition):
                p = self.run_grader(edition=edition)
                self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
                packet = json.loads(self.log.read_text())["packet"]
                manifest = json.loads((ROOT / edition /
                                       "org-skills/.claude-plugin/plugin.json").read_text())
                self.assertEqual(packet["edition"], edition)
                self.assertIn(manifest["name"] + ":spec-policy-pass", packet["task_prompt"])
                self.assertNotIn("SDLC_", packet["task_prompt"])
                source = edition + "/org-skills/skills/spec-policy-pass/SKILL.md"
                text = (ROOT / source).read_text()
                self.assertIn(text, packet["sources"].values())
                key = next(key for key, value in packet["sources"].items() if value == text)
                self.assertEqual(packet["source_sha256"][key],
                                 hashlib.sha256(text.encode()).hexdigest())

    def test_semantic_failure_is_rc1_even_when_keyword_is_present(self):
        p = self.run_grader("fail")
        self.assertEqual(p.returncode, 1, p.stderr)
        self.assertEqual(self.grade()["result"], "fail")
        self.assertEqual(self.grade()["counts"], {"pass": 0, "fail": 2, "undecidable": 0})

    def test_assertion_undecidable_has_rc2_precedence(self):
        p = self.run_grader("undecidable")
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertEqual(self.grade()["result"], "undecidable")

    def test_malformed_judgments_are_rc2_and_persisted(self):
        for mode in ("duplicate", "missing", "bad-evidence", "error-envelope",
                     "same-session", "malformed", "cli-error"):
            with self.subTest(mode=mode):
                p = self.run_grader(mode)
                self.assertEqual(p.returncode, 2, p.stdout + p.stderr)
                self.assertEqual(self.grade()["result"], "undecidable")

    def test_incomplete_trace_is_rc2_without_calling_grader(self):
        events = [json.loads(line) for line in self.trace.read_text().splitlines()]
        events.pop(2)  # tool_result
        self.trace.write_text("".join(json.dumps(x) + "\n" for x in events), encoding="utf-8")
        p = self.run_grader()
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertFalse(self.log.exists())
        grade = self.grade()
        self.assertEqual(grade["result"], "undecidable")
        self.assertEqual(grade["case_id"], "case")
        self.assertEqual(grade["counts"]["undecidable"], 2)

    def test_malformed_trace_is_rc2_without_calling_grader(self):
        self.trace.write_text("{broken\n", encoding="utf-8")
        p = self.run_grader()
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertFalse(self.log.exists())

    def test_missing_init_catalog_is_rc2_without_calling_grader(self):
        events = [json.loads(line) for line in self.trace.read_text().splitlines()]
        events.pop(0)
        self.trace.write_text("".join(json.dumps(x) + "\n" for x in events), encoding="utf-8")
        p = self.run_grader()
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertFalse(self.log.exists())

    def test_unsafe_successful_read_path_is_rc2(self):
        events = [json.loads(line) for line in self.trace.read_text().splitlines()]
        events[1]["message"]["content"][0]["input"]["file_path"] = "/etc/passwd"
        self.trace.write_text("".join(json.dumps(x) + "\n" for x in events), encoding="utf-8")
        p = self.run_grader()
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertFalse(self.log.exists())

    def test_mixed_generator_sessions_are_undecidable(self):
        events = [json.loads(line) for line in self.trace.read_text().splitlines()]
        events[1]["session_id"] = "another-session"
        self.trace.write_text("".join(json.dumps(x) + "\n" for x in events), encoding="utf-8")
        p = self.run_grader()
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertFalse(self.log.exists())

    def test_empty_assertions_are_undecidable(self):
        data = json.loads(self.case.read_text())
        data["assertions"] = []
        self.case.write_text(json.dumps(data), encoding="utf-8")
        p = self.run_grader()
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertFalse(self.log.exists())


if __name__ == "__main__":
    unittest.main()
