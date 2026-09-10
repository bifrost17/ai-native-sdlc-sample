"""0018 R1-R6 / AC4-AC5: runtime review transport and fail-closed controls."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "team-harness" / "sdlc_claude.py"
INSTALLER = ROOT / "team-harness" / "install.py"

FAKE_CLAUDE = r'''#!/usr/bin/env python3
import json, os, pathlib, sys, time

root = pathlib.Path(os.environ["FAKE_CLAUDE_ROOT"])
counter = root / "counter"
index = int(counter.read_text()) if counter.exists() else 0
counter.write_text(str(index + 1))
script = json.loads((root / "script.json").read_text())
step = script[index]
args = sys.argv[1:]
prompt = sys.stdin.read()
session = args[args.index("--resume") + 1] if "--resume" in args else (
    args[args.index("--session-id") + 1] if "--session-id" in args else "reviewer-session")
def substitute(value):
    if isinstance(value, str): return value.replace("$SESSION", session)
    if isinstance(value, list): return [substitute(item) for item in value]
    if isinstance(value, dict): return {key: substitute(item) for key, item in value.items()}
    return value
step = substitute(step)
with (root / "calls.jsonl").open("a") as stream:
    stream.write(json.dumps({"args": args, "prompt": prompt, "cwd": os.getcwd()}) + "\n")
if step.get("touch"):
    pathlib.Path(step["touch"]).write_text(step.get("contents", "changed during review\n"))
if step.get("sleep"):
    time.sleep(step["sleep"])
if "stdout" in step:
    print(step["stdout"])
else:
    for event in step.get("events", []):
        print(json.dumps(event))
sys.stderr.write(step.get("stderr", ""))
sys.exit(step.get("rc", 0))
'''


def developer(text, session="$SESSION", *, thinking="private chain of thought"):
    return {"events": [
        {"type": "system", "subtype": "init", "session_id": session},
        {"type": "assistant", "message": {"content": [
            {"type": "thinking", "thinking": thinking},
            {"type": "text", "text": text},
            {"type": "tool_use", "id": "tool-1", "name": "Bash",
             "input": {"command": "python3 -m unittest focused_test"}},
        ]}},
        {"type": "user", "message": {"content": [{"type": "tool_result",
         "tool_use_id": "tool-1", "content": "TEST-TOOL-RESULT: success"}]}},
        {"type": "result", "subtype": "success", "is_error": False,
         "session_id": session, "result": text, "total_cost_usd": 0.01},
    ]}


def review(verdict="pass", reason="consistent", feedback=""):
    return {"stdout": json.dumps({
        "type": "result", "subtype": "success", "is_error": False,
        "session_id": "reviewer-session",
        "total_cost_usd": 0.02,
        "structured_output": {"verdict": verdict, "reason": reason, "feedback": feedback},
    })}


class TeamHarnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="team-harness-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.repo = self.base / "project"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Harness Test"], cwd=self.repo, check=True)
        chain = self.repo / "intent/0018-team-harness"
        chain.mkdir(parents=True)
        (chain / "intent.md").write_text("original intent\n")
        (chain / "spec.md").write_text("original spec\n")
        (chain / "plan.md").write_text("original plan\n")
        (self.repo / "tracked.txt").write_text("base\n")
        subprocess.run(["git", "add", "."], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-qm", "base"], cwd=self.repo, check=True)
        self.base_sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=self.repo, text=True).strip()

        (self.repo / "tracked.txt").write_text("committed delta\n")
        subprocess.run(["git", "commit", "-qam", "after base"], cwd=self.repo, check=True)
        (chain / "spec.md").write_text("dirty spec decision\n")
        (self.repo / "untracked.txt").write_text("untracked evidence\n")

        self.fake = self.base / "fake"
        self.fake.mkdir()
        binary = self.fake / "claude"
        binary.write_text(FAKE_CLAUDE)
        binary.chmod(0o755)
        self.state = self.base / "state"
        self.env = dict(os.environ,
                        PATH=str(self.fake) + os.pathsep + os.environ["PATH"],
                        FAKE_CLAUDE_ROOT=str(self.fake),
                        SDLC_HARNESS_STATE_ROOT=str(self.state))

    def invoke(self, prompt="implement the accepted behavior", *, resume=None,
               timeout=2, extra=None):
        command = ["python3", str(HARNESS), "--project", str(self.repo),
                   "--chain", "intent/0018-team-harness", "--base", self.base_sha,
                   "--timeout", str(timeout)]
        if resume:
            command.extend(["--resume", resume])
        if extra:
            command.extend(extra)
        return subprocess.run(command, env=self.env, cwd=self.repo,
                              input=prompt, capture_output=True, text=True, check=False)

    def session_id(self):
        sessions = [path for path in self.state.iterdir() if path.is_dir()]
        self.assertEqual(len(sessions), 1)
        return sessions[0].name

    def scripted(self, *steps):
        (self.fake / "script.json").write_text(json.dumps(steps))
        for name in ("counter", "calls.jsonl"):
            (self.fake / name).unlink(missing_ok=True)

    def calls(self):
        path = self.fake / "calls.jsonl"
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    @staticmethod
    def flag(call, name):
        args = call["args"]
        return args[args.index(name) + 1]

    def assert_sonnet_effort(self, call, effort):
        self.assertEqual(self.flag(call, "--model"), "sonnet")
        self.assertEqual(self.flag(call, "--effort"), effort)

    def test_pass_returns_current_developer_answer_after_independent_toolless_review(self):
        self.scripted(developer("public final answer"), review())
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("public final answer", result.stdout)
        calls = self.calls()
        self.assertEqual(len(calls), 2)
        self.assert_sonnet_effort(calls[0], "low")
        self.assert_sonnet_effort(calls[1], "medium")
        self.assertIn("--session-id", calls[0]["args"])
        self.assertIn("--json-schema", calls[1]["args"])
        self.assertEqual(self.flag(calls[1], "--tools"), "")
        self.assertEqual(self.flag(calls[1], "--setting-sources"), "")
        self.assertIn("--safe-mode", calls[1]["args"])
        self.assertIn("--no-session-persistence", calls[1]["args"])
        self.assertNotIn("--resume", calls[1]["args"])
        session_dir = self.state / self.session_id()
        session_record = json.loads((session_dir / "session.json").read_text())
        summary = json.loads((session_dir / "turn01/summary.json").read_text())
        self.assertEqual((session_record["model"], session_record["effort"]), ("sonnet", "low"))
        self.assertEqual(session_record["reviewer_effort"], "medium")
        self.assertEqual(summary["developer"]["total_cost_usd"], 0.01)
        self.assertTrue(summary["input_digest"])
        self.assertTrue(summary["workspace_digest"])
        self.assertIn("finished_at", summary)

    def test_review_snapshot_contains_public_history_chain_and_all_git_change_classes(self):
        self.scripted(developer("PUBLIC-DEVELOPER-OUTPUT", thinking="HIDDEN-REASONING"), review())
        result = self.invoke("USER-DECISION-AND-ACCEPTANCE")
        self.assertEqual(result.returncode, 0, result.stderr)
        prompt = self.calls()[1]["prompt"]
        for evidence in ("USER-DECISION-AND-ACCEPTANCE", "PUBLIC-DEVELOPER-OUTPUT",
                         "original intent", "dirty spec decision", "original plan",
                         "committed delta", "untracked evidence", "TEST-TOOL-RESULT: success"):
            self.assertIn(evidence, prompt)
        self.assertNotIn("HIDDEN-REASONING", prompt)
        persisted = "\n".join(path.read_text(errors="replace")
                               for path in self.state.rglob("*") if path.is_file())
        self.assertNotIn("HIDDEN-REASONING", persisted)

    def test_revise_resumes_same_developer_session_and_reviews_each_new_final(self):
        self.scripted(
            developer("draft one", session="$SESSION"),
            review("revise", "spec omission", "add the agreed retry limit"),
            developer("draft two", session="$SESSION"), review())
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        calls = self.calls()
        self.assertEqual(len(calls), 4)
        self.assertIn("--resume", calls[2]["args"])
        self.assertEqual(self.flag(calls[2], "--resume"), self.session_id())
        self.assertIn("add the agreed retry limit", calls[2]["prompt"])
        self.assertIn("draft two", result.stdout)
        self.assertIn("draft two", calls[3]["prompt"])

    def test_third_revise_is_unresolved_and_never_reported_as_pass(self):
        self.scripted(
            developer("v1", "$SESSION"), review("revise", feedback="fix one"),
            developer("v2", "$SESSION"), review("revise", feedback="fix two"),
            developer("v3", "$SESSION"), review("revise", feedback="still missing"))
        result = self.invoke()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertEqual(len(self.calls()), 6)
        self.assertNotIn("passed", result.stdout.lower())

    def test_wait_is_a_normal_return_without_automatic_resume(self):
        self.scripted(developer("question for HUMAN"),
                      review("wait", "waiting for acceptance"))
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(len(self.calls()), 2)
        self.assertIn("question for HUMAN", result.stdout)

    def test_unknown_missing_and_unsupported_verdicts_fail_closed(self):
        invalid = [
            review("unknown", "insufficient evidence"),
            {"stdout": json.dumps({"structured_output": {"reason": "no verdict"}})},
            review("approve", "unsupported spelling"),
        ]
        for reviewer in invalid:
            with self.subTest(reviewer=reviewer):
                self.scripted(developer("answer"), reviewer)
                result = self.invoke()
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertNotIn("passed", result.stdout.lower())

    def test_reviewer_non_json_error_and_timeout_fail_closed(self):
        failures = [
            ({"stdout": "not json"}, 2),
            ({"stderr": "backend failed", "rc": 17}, 2),
            ({"sleep": 1.2}, 1),
        ]
        for reviewer, timeout in failures:
            with self.subTest(reviewer=reviewer):
                self.scripted(developer("answer"), reviewer)
                result = self.invoke(timeout=timeout)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertNotIn("passed", result.stdout.lower())

    def test_snapshot_changed_during_review_is_stale_and_fails_closed(self):
        target = self.repo / "tracked.txt"
        self.scripted(developer("answer"), {
            **review(), "touch": str(target), "contents": "changed inside review\n",
        })
        result = self.invoke()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        output = (result.stdout + result.stderr).lower()
        self.assertTrue(any(word in output for word in ("stale", "changed", "변경")), output)

    def test_untracked_symlink_loop_becomes_recorded_unknown_instead_of_traceback(self):
        (self.repo / "loop-a").symlink_to("loop-b")
        (self.repo / "loop-b").symlink_to("loop-a")
        self.scripted(developer("answer before snapshot"))
        result = self.invoke()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(len(self.calls()), 1, "review must not run with unsupported evidence")
        session = self.session_id()
        summary = json.loads((self.state / session / "turn01/summary.json").read_text())
        self.assertEqual(summary["verdict"], "unknown")
        self.assertTrue(any(word in summary["reason"].lower()
                            for word in ("symlink", "loop", "unsupported")), summary)
        recorded = json.loads((self.state / session / "turn01/review-result.json").read_text())
        self.assertIn(summary["reason"], recorded["error"])

    def test_resume_after_developer_error_preserves_failed_turn_and_reviews_recovery(self):
        self.scripted({"stderr": "developer backend failed", "rc": 17})
        first = self.invoke("original human request")
        self.assertEqual(first.returncode, 2, first.stdout + first.stderr)
        session = self.session_id()
        failed_dir = self.state / session / "turn01"
        before = {path.name: path.read_bytes() for path in failed_dir.iterdir() if path.is_file()}
        first_summary = json.loads((failed_dir / "summary.json").read_text())
        self.assertEqual(first_summary["verdict"], "unknown")
        self.assertIn("developer exited 17", first_summary["reason"])

        self.scripted(developer("recovered answer"), review())
        recovered = self.invoke("retry after transport recovery", resume=session)
        self.assertEqual(recovered.returncode, 0, recovered.stdout + recovered.stderr)
        self.assertIn("recovered answer", recovered.stdout)
        after = {path.name: path.read_bytes() for path in failed_dir.iterdir() if path.is_file()}
        self.assertEqual(after, before, "resume rewrote evidence from the failed turn")
        calls = self.calls()
        self.assertEqual(self.flag(calls[0], "--resume"), session)
        review_prompt = calls[1]["prompt"]
        for evidence in ("original human request", "retry after transport recovery",
                         "recovered answer"):
            self.assertIn(evidence, review_prompt)
        packet = json.loads(review_prompt)
        failed_turn = packet["developer_turns"][0]
        self.assertEqual(failed_turn["turn"], 1)
        self.assertTrue(failed_turn["recorded_outcome"]["execution_failed"])
        self.assertEqual(failed_turn["recorded_outcome"]["verdict"], "unknown")
        self.assertIn("source_log", failed_turn)
        session_summary = json.loads((self.state / session / "summary.json").read_text())
        self.assertEqual([turn["verdict"] for turn in session_summary["turns"]],
                         ["unknown", "pass"])

    def test_three_user_turns_resume_one_session_and_retry_budget_resets_each_turn(self):
        # Two revisions are allowed independently in both the first and third user turns.
        first = [developer("1a", "$SESSION"), review("revise", feedback="r1"),
                 developer("1b", "$SESSION"), review("revise", feedback="r2"),
                 developer("1c", "$SESSION"), review()]
        self.scripted(*first)
        self.assertEqual(self.invoke("turn one").returncode, 0)
        session = self.session_id()

        self.scripted(developer("2", "$SESSION"), review("wait", "need user input"))
        self.assertEqual(self.invoke("turn two", resume=session).returncode, 0)

        third = [developer("3a", "$SESSION"), review("revise", feedback="r1"),
                 developer("3b", "$SESSION"), review("revise", feedback="r2"),
                 developer("3c", "$SESSION"), review()]
        self.scripted(*third)
        self.assertEqual(self.invoke("turn three", resume=session).returncode, 0)
        calls = self.calls()
        developer_calls = [call for call in calls if "--json-schema" not in call["args"]]
        self.assertTrue(developer_calls)
        for call in developer_calls:
            self.assertEqual(self.flag(call, "--resume"), session)
        final_review = calls[-1]["prompt"]
        for turn in ("turn one", "turn two", "turn three"):
            self.assertIn(turn, final_review)
        records = [json.loads(path.read_text()) for path in
                   sorted((self.state / session).glob("turn*/input.json"))]
        self.assertEqual([record["kind"] for record in records],
                         ["human", "reviewer_feedback", "reviewer_feedback", "human",
                          "human", "reviewer_feedback", "reviewer_feedback"])
        self.assertEqual([record["automatic_revision_index"] for record in records],
                         [0, 1, 2, 0, 0, 1, 2])

    def test_wait_question_survives_short_human_answer_while_prior_pass_text_is_omitted(self):
        question = "배포 대상을 선택해 주세요: 1) staging 2) production"
        self.scripted(developer(question),
                      review("wait", "a human choice is required", "choose option 1 or 2"))
        first = self.invoke("배포 대상을 물어봐 주세요")
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        session = self.session_id()

        completed = "OPTION-ONE-APPLIED-PASS-FINAL"
        self.scripted(developer(completed), review())
        second = self.invoke("첫 번째요", resume=session)
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        second_packet = json.loads(self.calls()[1]["prompt"])
        self.assertIn({"turn": 2, "prompt": "첫 번째요"},
                      second_packet["human_conversation"])
        prior_wait = second_packet["developer_turns"][0]
        self.assertEqual(prior_wait["recorded_outcome"]["verdict"], "wait")
        self.assertEqual(prior_wait["human_decision_context"], question)

        self.scripted(developer("later unrelated result"), review())
        third = self.invoke("후속 상태를 확인해 주세요", resume=session)
        self.assertEqual(third.returncode, 0, third.stdout + third.stderr)
        third_packet = json.loads(self.calls()[1]["prompt"])
        self.assertEqual(third_packet["developer_turns"][0]["human_decision_context"], question)
        prior_pass = third_packet["developer_turns"][1]
        self.assertEqual(prior_pass["recorded_outcome"]["verdict"], "pass")
        self.assertNotIn("human_decision_context", prior_pass)
        self.assertNotIn(completed, self.calls()[1]["prompt"])
        self.assertEqual(prior_pass["superseded_final_claim_sha256"],
                         hashlib.sha256(completed.encode()).hexdigest())


class TeamHarnessInstallerTests(unittest.TestCase):
    def test_temporary_prefix_round_trip_preserves_existing_files_and_excludes_authoring_templates(self):
        with tempfile.TemporaryDirectory(prefix="harness-install-") as temporary:
            prefix = Path(temporary)
            existing = prefix / "bin/existing-tool"
            existing.parent.mkdir(parents=True)
            existing.write_text("keep me\n")
            config = prefix / "share/existing.conf"
            config.parent.mkdir(parents=True)
            config.write_text("keep config\n")

            install = subprocess.run(
                ["python3", str(INSTALLER), "--prefix", str(prefix)],
                capture_output=True, text=True, check=False)
            self.assertEqual(install.returncode, 0, install.stdout + install.stderr)
            self.assertEqual(existing.read_text(), "keep me\n")
            self.assertEqual(config.read_text(), "keep config\n")
            self.assertTrue((prefix / "bin/sdlc-claude").is_file())
            copied = [p.relative_to(prefix).as_posix() for p in prefix.rglob("*") if p.is_file()]
            self.assertEqual(set(copied), {
                "bin/existing-tool", "bin/sdlc-claude", "share/existing.conf",
                "share/intent-sdlc-harness/reviewer.md",
                "share/intent-sdlc-harness/sdlc_claude.py",
            })

            round_trip = subprocess.run(
                [str(prefix / "bin/sdlc-claude"), "--help"],
                capture_output=True, text=True, check=False)
            self.assertEqual(round_trip.returncode, 0, round_trip.stdout + round_trip.stderr)
            reinstall = subprocess.run(
                ["python3", str(INSTALLER), "--prefix", str(prefix)],
                capture_output=True, text=True, check=False)
            self.assertEqual(reinstall.returncode, 0, reinstall.stdout + reinstall.stderr)
            self.assertEqual(existing.read_text(), "keep me\n")
            self.assertEqual(config.read_text(), "keep config\n")

    def test_installer_refuses_to_replace_an_existing_foreign_entrypoint(self):
        with tempfile.TemporaryDirectory(prefix="harness-install-foreign-") as temporary:
            prefix = Path(temporary)
            destination = prefix / "bin/sdlc-claude"
            destination.parent.mkdir(parents=True)
            destination.write_text("#!/bin/sh\necho personal tool\n")
            result = subprocess.run(
                ["python3", str(INSTALLER), "--prefix", str(prefix)],
                capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertEqual(destination.read_text(), "#!/bin/sh\necho personal tool\n")

    def test_installer_does_not_follow_predictable_temporary_symlinks(self):
        with tempfile.TemporaryDirectory(prefix="harness-install-symlinks-") as temporary:
            prefix = Path(temporary)
            runtime = prefix / "share/intent-sdlc-harness"
            bindir = prefix / "bin"
            runtime.mkdir(parents=True)
            bindir.mkdir()
            sentinel = prefix / "personal-notes.txt"
            sentinel.write_text("private file must remain unchanged\n")
            traps = [runtime / "sdlc_claude.py.tmp", runtime / "reviewer.md.tmp",
                     bindir / "sdlc-claude.tmp"]
            for trap in traps:
                trap.symlink_to(sentinel)

            result = subprocess.run(
                ["python3", str(INSTALLER), "--prefix", str(prefix)],
                capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(sentinel.read_text(), "private file must remain unchanged\n")
            self.assertTrue(all(trap.is_symlink() and trap.resolve() == sentinel.resolve()
                                for trap in traps))
            self.assertIn("Small, stdlib-only Claude Code team harness",
                          (runtime / "sdlc_claude.py").read_text())
            self.assertIn("# Independent SDLC review", (runtime / "reviewer.md").read_text())


if __name__ == "__main__":
    unittest.main()
