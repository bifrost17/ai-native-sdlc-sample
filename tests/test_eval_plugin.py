"""0013 R3/AC2/AC3: load this checkout's plugin and exercise policy eval wiring.

The fake CLI verifies runner integration only; it cannot prove model skill use.
"""
import fnmatch
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parent.parent
POLICY_CASE = "04-org-policy-application"
POLICY_OUTPUT = """# Spec: 임직원 작업 상태
brand B3: YYYY-MM-DD, 24시간제, 시간대를 적는다.
완료 시각은 2026-09-10 18:30 KST로 표시한다.
data-compliance C2: 로그 · 오류 메시지 · 감사 이벤트에는 내부 ID 만 남긴다.
employee_email과 employee_phone은 응답 경계에서 제외한다.
data-compliance C3: 누가(역할 + ID) · 무엇을(업무 식별자) · 언제(UTC).
P2의 90일 보존 기간과 즉시 이력 삭제 요구가 충돌하므로 정책 오너가 결정한다.
secure-api-review: every endpoint requires the gateway JWT.
새 엔드포인트에 gateway JWT 인증을 요구한다.
ux-copy Error Messages: What happened + Why + How to fix
오류 문구는 실패한 작업, 확인된 원인, 다시 시도할 행동을 담는다.
"""
FAKE_CLAUDE = r'''#!/usr/bin/env python3
import json
import os
from pathlib import Path
import re
import shutil
import sys

args = sys.argv[1:]
prompt = args[args.index("-p") + 1]
cid = re.search(r"evals/out/([^/]+)/ws", prompt).group(1)
with open(os.environ["FAKE_EVAL_LOG"], "a", encoding="utf-8") as log:
    log.write(json.dumps({"args": args, "cwd": os.getcwd(), "id": cid}) + "\n")
if os.environ.get("FAKE_EVAL_FAIL") == cid:
    print("fake model failed", file=sys.stderr)
    sys.exit(17)
workspace = Path("evals/out") / cid / "ws"
shutil.copytree(Path(os.environ["FAKE_EVAL_OUTPUTS"]) / cid, workspace, dirs_exist_ok=True)
print(json.dumps({"result": "Fake CLI output: runner integration only."}))
'''


class EvalPluginIntegration(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="eval plugin ")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.repo = self.base / "checkout"
        self.repo.mkdir()
        for directory in ("evals", ".claude", "org-skills", "policies", "templates"):
            shutil.copytree(ROOT / directory, self.repo / directory,
                            ignore=shutil.ignore_patterns("out", "__pycache__"))
        shutil.copy2(ROOT / "CLAUDE.md", self.repo / "CLAUDE.md")
        self.outputs = self.base / "outputs"
        for cid, fixture in (
            ("01-intent-placeholder", "01-pass"),
            ("02-no-self-accept", "02-pass"),
            ("03-spec-carries-questions", "03-pass"),
        ):
            shutil.copytree(ROOT / "evals/testdata" / fixture / "ws", self.outputs / cid)
        policy_output = self.outputs / POLICY_CASE
        policy_output.mkdir()
        (policy_output / "spec.md").write_text(POLICY_OUTPUT, encoding="utf-8")
        binary = self.base / "bin"
        binary.mkdir()
        cli = binary / "claude"
        cli.write_text(FAKE_CLAUDE, encoding="utf-8")
        cli.chmod(0o755)
        self.log = self.base / "calls.jsonl"
        self.env = dict(os.environ, PATH=str(binary) + os.pathsep + os.environ["PATH"],
                        ANTHROPIC_API_KEY="fake-key-never-sent",
                        FAKE_EVAL_LOG=str(self.log), FAKE_EVAL_OUTPUTS=str(self.outputs))

    def run_evals(self):
        return subprocess.run(["bash", "evals/run.sh"], cwd=self.repo, env=self.env,
                              text=True, capture_output=True, check=False)

    def test_every_case_loads_current_plugin_and_uses_its_workspace(self):
        result = self.run_evals()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        calls = [json.loads(line) for line in self.log.read_text().splitlines()]
        self.assertEqual([call["id"] for call in calls], [
            "01-intent-placeholder", "02-no-self-accept", "03-spec-carries-questions", POLICY_CASE])
        for call in calls:
            with self.subTest(case=call["id"]):
                args = call["args"]
                self.assertIn("--plugin-dir", args)
                self.assertEqual(args[args.index("--plugin-dir") + 1], str(self.repo / "org-skills"))
                self.assertEqual(Path(call["cwd"]), self.repo)
                self.assertEqual(args[args.index("--output-format") + 1], "json")
                case = json.loads((self.repo / "evals/cases" / (call["id"] + ".json")).read_text())
                self.assertEqual(args[args.index("--allowedTools") + 1], case["allowed_tools"])
                self.assertNotIn("--dangerously-skip-permissions", args)
                self.assertNotIn("bypassPermissions", args)
                workspace = self.repo / "evals/out" / call["id"] / "ws"
                prompt = args[args.index("-p") + 1]
                self.assertIn(str(workspace), prompt)
                self.assertIn("Create or change files only in this workspace", prompt)
                recorded = json.loads((self.repo / "evals/out" / (call["id"] + ".json")).read_text())
                self.assertEqual(recorded["workspace"], call["id"] + "/ws")
                for fixture in case["files"]:
                    self.assertTrue((workspace / Path(fixture).name).is_file())
        policy = json.loads((self.repo / "evals/cases" / (POLICY_CASE + ".json")).read_text())
        self.assertIn("Skill", policy["allowed_tools"].split(","))

    def test_policy_names_without_clause_evidence_fail_existing_grader(self):
        self.assertTrue((self.repo / "evals/cases" / (POLICY_CASE + ".json")).exists())
        (self.outputs / POLICY_CASE / "spec.md").write_text(
            "Skills applied: brand, data-compliance, secure-api-review, ux-copy.\n",
            encoding="utf-8")
        result = self.run_evals()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("FAIL", result.stdout)

    def test_model_failure_is_undecidable_and_later_cases_still_run(self):
        self.env["FAKE_EVAL_FAIL"] = "01-intent-placeholder"
        result = self.run_evals()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("claude rc=17", result.stderr)
        calls = [json.loads(line) for line in self.log.read_text().splitlines()]
        self.assertEqual(calls[-1]["id"], POLICY_CASE)

    def test_missing_plugin_is_undecidable_before_model_call(self):
        shutil.rmtree(self.repo / "org-skills")
        result = self.run_evals()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("UNDECIDABLE", result.stderr)
        self.assertFalse(self.log.exists())


class EvalWorkflowPaths(unittest.TestCase):
    def test_relevant_changes_match_pull_request_paths(self):
        workflow = (ROOT / ".github/workflows/agent-evals.yml").read_text()
        paths = re.findall(r"^      - '([^']+)'$", workflow, re.MULTILINE)
        for changed in (
            "CLAUDE.md", ".claude/skills/design-spec/SKILL.md",
            "org-skills/skills/brand/SKILL.md", "org-skills/.claude-plugin/plugin.json",
            "policies/brand.md", "templates/spec.md", "evals/cases/04-org-policy-application.json",
            ".claude-plugin/marketplace.json", ".github/workflows/agent-evals.yml",
        ):
            with self.subTest(path=changed):
                self.assertTrue(any(fnmatch.fnmatchcase(changed, path) for path in paths))


if __name__ == "__main__":
    unittest.main()
