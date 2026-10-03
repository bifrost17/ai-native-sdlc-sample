"""SP08 (FR09/AC08): check the hook against disposable Git repositories."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


EXAMPLE = (Path(__file__).resolve().parents[1] / "tdd-optional" / "org-skills"
           / "examples" / "document-sync-hook")
SCRIPT = EXAMPLE / "document_sync.py"


class DocumentSyncHookTests(unittest.TestCase):
    def setUp(self):
        self.git_env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        self.git_env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1",
                            SDLC_PYTHON=sys.executable)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.run_git("init", "-q", "-b", "main")
        self.run_git("config", "user.name", "Fixture")
        self.run_git("config", "user.email", "fixture@example.invalid")
        hooks = self.repo / ".git" / "hooks"
        shutil.copy2(EXAMPLE / "pre-commit", hooks / "pre-commit")
        shutil.copy2(SCRIPT, hooks / "document_sync.py")
        (hooks / "pre-commit").chmod(0o755)

    def run_git(self, *args, env=None, ok=True):
        result = subprocess.run(["git", *args], cwd=self.repo, env=env or self.git_env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if ok and result.returncode:
            self.fail("git " + " ".join(args) + ": " + result.stderr)
        return result

    def write(self, name, content):
        target = self.repo / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def snapshot(self, env=None):
        result = subprocess.run([sys.executable, str(SCRIPT), "snapshot"], cwd=self.repo,
                                env=env or self.git_env, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def signal(self, documents=(), snapshot=None, env=None):
        values = dict(self.git_env if env is None else env)
        values["SDLC_DOC_SYNC"] = json.dumps({"snapshot": snapshot or self.snapshot(env),
                                                "documents": list(documents)}, ensure_ascii=False)
        return values

    def commit(self, env=None, *args):
        return self.run_git("commit", "-qm", "fixture", *args, env=env, ok=False)

    def initial(self):
        self.write("code.py", "before\n")
        self.run_git("add", "code.py")
        self.assertEqual(self.commit(self.signal()).returncode, 0)

    def test_first_commit_requires_signal_and_accepts_valid_empty_declaration(self):
        self.write("첫 문서/설계 노트.md", "one\n")
        self.run_git("add", "첫 문서/설계 노트.md")
        self.assertNotEqual(self.commit().returncode, 0)
        self.assertEqual(self.commit(self.signal(["첫 문서/설계 노트.md"])).returncode, 0)
        self.assertEqual(self.run_git("rev-list", "--count", "HEAD").stdout.strip(), "1")

    def test_bad_signals_and_required_path(self):
        self.initial()
        self.write("code.py", "after\n")
        self.run_git("add", "code.py")
        valid = self.signal()
        for raw in ("{", "[]", '{"snapshot":"x","documents":[]}',
                    '{"snapshot":"x","snapshot":"y","documents":[]}',
                    json.dumps({"snapshot": self.snapshot(), "documents": [], "extra": 1}),
                    json.dumps({"snapshot": self.snapshot(), "documents": ["../plan.md"]}),
                    json.dumps({"snapshot": self.snapshot(), "documents": ["plan.md", "plan.md"]}),
                    json.dumps({"snapshot": self.snapshot(), "documents": ["*.md"]})):
            env = dict(valid, SDLC_DOC_SYNC=raw)
            self.assertNotEqual(self.commit(env).returncode, 0, raw)
        missing = self.commit(self.signal(["plan.md"]))
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("plan.md", missing.stderr)
        self.assertEqual(self.commit(valid).returncode, 0)

    def test_stale_head_and_index_fail(self):
        self.initial()
        stale_head = self.snapshot()
        self.write("code.py", "second\n")
        self.run_git("add", "code.py")
        self.assertNotEqual(self.commit(self.signal(snapshot=stale_head)).returncode, 0)
        current = self.signal()
        self.write("code.py", "third\n")
        self.run_git("add", "code.py")
        self.assertNotEqual(self.commit(current).returncode, 0)
        self.assertEqual(self.commit(self.signal()).returncode, 0)
        # Same tree but a different HEAD is a different reviewed scope.
        self.write("other", "content\n")
        self.run_git("add", "other")
        before_amend = self.signal()
        self.assertEqual(self.commit(self.signal(), "--amend").returncode, 0)
        self.assertNotEqual(self.commit(before_amend).returncode, 0)

    def test_partial_stage_and_unrelated_worktree_changes(self):
        self.initial()
        self.write("plan.md", "first\n")
        self.run_git("add", "plan.md")
        self.write("plan.md", "first\nunstaged\n")
        self.write("other.py", "untracked\n")
        self.assertEqual(self.commit(self.signal(["plan.md"])).returncode, 0)
        self.assertEqual(self.run_git("show", "HEAD:plan.md").stdout, "first\n")
        self.assertEqual((self.repo / "plan.md").read_text(), "first\nunstaged\n")
        self.assertTrue((self.repo / "other.py").exists())

    def test_unstaged_required_path_does_not_count(self):
        self.initial()
        self.write("plan.md", "only in worktree\n")
        self.write("code.py", "change\n")
        self.run_git("add", "code.py")
        self.assertNotEqual(self.commit(self.signal(["plan.md"])).returncode, 0)
        self.assertEqual(self.commit(self.signal()).returncode, 0)

    def test_binary_diff_ignores_display_and_external_diff_configuration(self):
        self.initial()
        (self.repo / "image.bin").write_bytes(b"\x00\xff\x10\x00")
        self.run_git("add", "image.bin")
        baseline = self.snapshot()
        self.run_git("config", "color.ui", "always")
        self.run_git("config", "diff.external", "/usr/bin/false")
        self.run_git("config", "diff.renames", "true")
        self.run_git("config", "core.quotePath", "false")
        self.assertEqual(self.snapshot(), baseline)
        self.assertEqual(self.commit(self.signal(["image.bin"])).returncode, 0)

    def test_snapshot_survives_hunk_order_and_git_diff_environment_changes(self):
        self.write("a.md", "".join("line %02d\n" % number for number in range(50)))
        self.write("z.md", "original\n")
        self.run_git("add", "a.md", "z.md")
        self.assertEqual(self.commit(self.signal(["a.md", "z.md"])).returncode, 0)
        lines = (self.repo / "a.md").read_text().splitlines(keepends=True)
        lines[4] = "changed near top\n"
        lines[24] = "changed later\n"
        self.write("a.md", "".join(lines))
        self.write("z.md", "changed\n")
        self.run_git("add", "a.md", "z.md")
        reviewed = self.signal(["a.md", "z.md"])
        order = self.repo / "display-order"
        order.write_text("z.md\na.md\n", encoding="utf-8")
        self.run_git("config", "diff.interHunkContext", "30")
        self.run_git("config", "diff.orderFile", str(order))
        changed_env = dict(reviewed, GIT_DIFF_OPTS="--unified=0")
        self.assertEqual(self.snapshot(changed_env), json.loads(reviewed["SDLC_DOC_SYNC"])["snapshot"])
        self.assertEqual(self.commit(changed_env).returncode, 0)

    def test_unstaged_attributes_do_not_change_reviewed_index_snapshot(self):
        self.write("plan.md", "before\n")
        self.run_git("add", "plan.md")
        self.assertEqual(self.commit(self.signal(["plan.md"])).returncode, 0)
        self.write("plan.md", "after\n")
        self.run_git("add", "plan.md")
        reviewed = self.signal(["plan.md"])
        self.write(".gitattributes", "*.md binary\n")
        self.assertEqual(self.snapshot(), json.loads(reviewed["SDLC_DOC_SYNC"])["snapshot"])
        self.assertEqual(self.commit(reviewed).returncode, 0)
        self.assertEqual(self.run_git("show", "HEAD:plan.md").stdout, "after\n")
        self.assertTrue((self.repo / ".gitattributes").exists())

    def test_fixture_ignores_inherited_global_hooks_signing_and_branch(self):
        global_config = self.repo / "host-gitconfig"
        global_config.write_text("[core]\n  hooksPath = /does/not/exist\n"
                                 "[commit]\n  gpgsign = true\n"
                                 "[init]\n  defaultBranch = trunk\n", encoding="utf-8")
        polluted = dict(os.environ, GIT_CONFIG_GLOBAL=str(global_config),
                        GIT_INDEX_FILE=str(self.repo / "stray-index"))
        selected = [
            "tests.test_document_sync_hook.DocumentSyncHookTests.test_first_commit_requires_signal_and_accepts_valid_empty_declaration",
            "tests.test_document_sync_hook.DocumentSyncHookTests.test_unresolved_index_fails_snapshot",
        ]
        result = subprocess.run([sys.executable, "-m", "unittest", *selected],
                                cwd=EXAMPLE.parents[3], env=polluted,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_intent_to_add_empty_file_changes_when_actually_staged(self):
        self.initial()
        self.write("empty.md", "")
        self.run_git("add", "-N", "empty.md")
        reviewed = self.signal()
        self.assertNotIn("empty.md", self.run_git("diff", "--cached", "--name-only").stdout)
        self.run_git("add", "empty.md")
        self.assertIn("empty.md", self.run_git("diff", "--cached", "--name-only").stdout)
        self.assertNotEqual(self.snapshot(), json.loads(reviewed["SDLC_DOC_SYNC"])["snapshot"])
        self.assertNotEqual(self.commit(reviewed).returncode, 0)
        self.assertEqual(self.commit(self.signal(["empty.md"])).returncode, 0)

    def test_deletion_and_rename_accept_actual_staged_old_and_new_paths(self):
        self.write("old.md", "a\n")
        self.run_git("add", "old.md")
        self.assertEqual(self.commit(self.signal(["old.md"])).returncode, 0)
        self.run_git("mv", "old.md", "새 문서.md")
        self.assertEqual(self.commit(self.signal(["old.md", "새 문서.md"])).returncode, 0)
        self.run_git("rm", "새 문서.md")
        self.assertEqual(self.commit(self.signal(["새 문서.md"])).returncode, 0)

    def test_alternate_index_and_path_limited_commit(self):
        self.initial()
        self.write("code.py", "main index change\n")
        self.run_git("add", "code.py")
        self.write("other.md", "alternate\n")
        alternate = self.repo / "alternate-index"
        shutil.copy2(self.repo / ".git" / "index", alternate)
        alt_env = dict(self.git_env, GIT_INDEX_FILE=str(alternate))
        self.run_git("add", "other.md", env=alt_env)
        alt_signal = self.signal(["other.md"], env=alt_env)
        ordinary_env = dict(alt_signal)
        ordinary_env.pop("GIT_INDEX_FILE")
        self.assertNotEqual(self.commit(ordinary_env).returncode, 0)
        self.assertEqual(self.commit(alt_signal).returncode, 0)
        self.assertEqual(self.run_git("show", "HEAD:other.md").stdout, "alternate\n")

        self.write("code.py", "path only\n")
        self.write("other.md", "left aside\n")
        self.run_git("add", "code.py", "other.md")
        wrong_scope = self.signal(["other.md"])
        self.assertNotEqual(self.run_git("commit", "-qm", "path", "--", "code.py", env=wrong_scope,
                                        ok=False).returncode, 0)
        # The failed commit must leave the ordinary index intact.
        self.assertEqual(self.run_git("diff", "--cached", "--name-only").stdout.splitlines(),
                         ["code.py", "other.md"])
        path_index = self.repo / "path-index"
        path_env = dict(self.git_env, GIT_INDEX_FILE=str(path_index))
        self.run_git("read-tree", "HEAD", env=path_env)
        self.run_git("add", "code.py", env=path_env)
        path_signal = self.signal(env=path_env)
        path_signal.pop("GIT_INDEX_FILE")
        self.assertEqual(self.run_git("commit", "-qm", "path", "--", "code.py", env=path_signal,
                                      ok=False).returncode, 0)
        self.assertEqual(self.run_git("show", "HEAD:code.py").stdout, "path only\n")
        self.assertEqual(self.run_git("show", "HEAD:other.md").stdout, "alternate\n")

    def test_unresolved_index_fails_snapshot(self):
        self.initial()
        self.run_git("checkout", "-qb", "other")
        self.write("code.py", "other\n")
        self.run_git("add", "code.py")
        self.assertEqual(self.commit(self.signal()).returncode, 0)
        self.run_git("checkout", "-q", "main")
        self.write("code.py", "main\n")
        self.run_git("add", "code.py")
        self.assertEqual(self.commit(self.signal()).returncode, 0)
        self.assertNotEqual(self.run_git("merge", "other", ok=False).returncode, 0)
        result = subprocess.run([sys.executable, str(SCRIPT), "snapshot"], cwd=self.repo,
                                env=self.git_env, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("index", result.stderr)


if __name__ == "__main__":
    unittest.main()
