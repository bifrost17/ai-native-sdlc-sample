#!/usr/bin/env python3
"""tests/test_metrics.py — scripts/metrics.py(플레이북 Stage 1·2 지표 계기)의 계약 시험.

원칙 두 가지.

1. **모의(mock)를 쓰지 않는다.** 이 계기가 재는 대상이 git 이력 그 자체이므로,
   git 을 대역으로 갈아 끼우면 실물과의 계약을 증언하지 못한다. 그래서 매 케이스가
   `tempfile` 로 진짜 저장소를 만들고 `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE` 를
   고정해 이력을 심는다.

2. **PATH 는 셰임으로 고정한다.** 개발자 기계에 `gh` 가 깔려 있는지 여부로 시험
   결과가 달라지면 그 시험은 계기가 아니다. 모든 케이스가 셰임 디렉터리를 PATH
   앞에 두고, `git` 은 보이고 `gh` 는 보이지 않는 상태를 setUp 에서 **양성 대조로
   확인한 뒤** 측정을 시작한다(계기가 정상 상태에서 기대한 값을 내는지 먼저 잰다).
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "metrics.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures-metrics"

CHAIN_ID = "0002-claims-status"

# 픽스처의 intent frontmatter 가 신고한 `created`.
CREATED_REPORTED = "2026-09-09T10:12:00+09:00"

# H1 이력의 시각들(전부 +09:00).
T_INTENT_CREATE = "2026-09-09T11:00:00+09:00"
T_INTENT_MOD1 = "2026-09-09T12:00:00+09:00"
T_INTENT_ACCEPT = "2026-09-09T13:00:00+09:00"
T_SPEC_CREATE = "2026-09-10T09:00:00+09:00"
T_INTENT_MOD2 = "2026-09-10T10:00:00+09:00"
T_INTENT_MOD3 = "2026-09-10T11:00:00+09:00"
T_PLAN_CREATE = "2026-09-11T09:00:00+09:00"
T_SPEC_MOD1 = "2026-09-11T10:00:00+09:00"


def fixture(name):
    return (FIXTURES / name).read_text(encoding="utf-8").replace("{{ID}}", CHAIN_ID)


class TempRepo:
    """진짜 git 저장소 하나. 커밋 시각을 인자로 고정한다."""

    def __init__(self, root, init=True):
        self.path = Path(root)
        self.path.mkdir(parents=True, exist_ok=True)
        self.home = self.path.parent / "home"
        self.home.mkdir(parents=True, exist_ok=True)
        self.shim = self.path.parent / "shim"
        self.shim.mkdir(parents=True, exist_ok=True)
        # PATH 셰임: 실행에 필요한 시스템 경로만 두고 homebrew(=gh) 는 뺀다.
        self.path_env = os.pathsep.join(
            [str(self.shim), "/usr/bin", "/bin", "/usr/sbin", "/sbin"]
        )
        self.env = dict(os.environ)
        self.env.update(
            {
                "PATH": self.path_env,
                "HOME": str(self.home),
                "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_CONFIG_SYSTEM": os.devnull,
                "GIT_TERMINAL_PROMPT": "0",
                "LC_ALL": "C",
            }
        )
        if init:
            self.git("-c", "init.defaultBranch=main", "init", "-q")

    def git(self, *args, at=None, check=True):
        env = dict(self.env)
        if at is not None:
            env["GIT_AUTHOR_DATE"] = at
            env["GIT_COMMITTER_DATE"] = at
        cmd = [
            "git",
            "-C",
            str(self.path),
            "-c",
            "user.name=fixture",
            "-c",
            "user.email=fixture@example.invalid",
        ] + list(args)
        p = subprocess.run(cmd, env=env, capture_output=True, text=True)
        if check and p.returncode != 0:
            raise AssertionError(
                "git %s -> rc=%d\nstdout=%s\nstderr=%s"
                % (" ".join(args), p.returncode, p.stdout, p.stderr)
            )
        return p

    def write(self, rel, content):
        target = self.path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def commit(self, rel, content, at, msg):
        """파일 하나를 쓰고 그 파일만 이름으로 add 해서 커밋. 커밋 sha 를 돌려준다."""
        self.write(rel, content)
        self.git("add", "--", rel)
        self.git("commit", "-q", "-m", msg, at=at)
        return self.git("rev-parse", "HEAD").stdout.strip()

    def author_date(self, sha):
        return self.git("show", "-s", "--format=%aI", sha).stdout.strip()

    def install_fake_gh(self, payload):
        """셰임 디렉터리에 가짜 `gh` 를 심는다 — 네트워크 없이 gh 있는 경로를 잰다."""
        gh = self.shim / "gh"
        gh.write_text(
            "#!/usr/bin/env bash\ncat <<'JSON'\n%s\nJSON\n" % json.dumps(payload),
            encoding="utf-8",
        )
        gh.chmod(0o755)


def intent_path(chain_id=CHAIN_ID):
    return "intent/%s/intent.md" % chain_id


def spec_path(chain_id=CHAIN_ID):
    return "intent/%s/spec.md" % chain_id


def plan_path(chain_id=CHAIN_ID):
    return "intent/%s/plan.md" % chain_id


def build_h1(repo):
    """H1 — 브리프 ①의 이력.

    intent 생성 → 수정 2(그중 하나가 accepted 전이) → spec 생성 → intent 수정 2
    → plan 생성 → spec 수정 1.  기대: L3=2, L4=1.
    """
    shas = {}
    body = fixture("intent-draft.md")
    shas["c1_intent_create"] = repo.commit(
        intent_path(), body, T_INTENT_CREATE, "feat: intent 발의"
    )
    shas["c2_intent_mod"] = repo.commit(
        intent_path(), body + "\n- Q2 상류 한도는 얼마인가 — 플랫폼팀\n",
        T_INTENT_MOD1, "docs: intent 미결 추가",
    )
    accepted = fixture("intent-accepted.md") + "\n- Q2 상류 한도는 얼마인가 — 플랫폼팀\n"
    shas["c3_intent_accept"] = repo.commit(
        intent_path(), accepted, T_INTENT_ACCEPT, "chore: intent accepted"
    )
    shas["c4_spec_create"] = repo.commit(
        spec_path(), fixture("spec.md"), T_SPEC_CREATE, "feat: spec 작성"
    )
    shas["c5_intent_mod"] = repo.commit(
        intent_path(), accepted + "\n<!-- spec 이후 수정 1 -->\n",
        T_INTENT_MOD2, "docs: intent 수정(spec 이후 1)",
    )
    shas["c6_intent_mod"] = repo.commit(
        intent_path(), accepted + "\n<!-- spec 이후 수정 1 -->\n<!-- spec 이후 수정 2 -->\n",
        T_INTENT_MOD3, "docs: intent 수정(spec 이후 2)",
    )
    shas["c7_plan_create"] = repo.commit(
        plan_path(), fixture("plan.md"), T_PLAN_CREATE, "feat: plan 작성"
    )
    shas["c8_spec_mod"] = repo.commit(
        spec_path(), fixture("spec-v2.md"), T_SPEC_MOD1, "docs: spec 수정(plan 이후 1)"
    )
    return shas


class MetricsTestBase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="metrics-w1f-")
        self.tmp = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def new_repo(self, name="repo", init=True):
        repo = TempRepo(self.tmp / name / "work", init=init)
        # 양성 대조: 셰임 PATH 에서 git 은 보이고 gh 는 보이지 않아야 측정이 성립한다.
        self.assertIsNotNone(
            shutil.which("git", path=repo.path_env), "셰임 PATH 에서 git 이 안 보인다 — 계기 고장"
        )
        self.assertIsNone(
            shutil.which("gh", path=repo.path_env), "셰임 PATH 에 gh 가 남아 있다 — 계기 고장"
        )
        return repo

    def run_metrics(self, repo, *extra, env=None):
        cmd = [sys.executable, str(SCRIPT), "--repo", str(repo.path)] + list(extra)
        p = subprocess.run(
            cmd, env=env if env is not None else repo.env, capture_output=True, text=True
        )
        return p

    def json_metrics(self, repo, *extra, env=None):
        p = self.run_metrics(repo, "--format", "json", *extra, env=env)
        self.assertEqual(
            p.returncode, 0, "rc=%d\nstdout=%s\nstderr=%s" % (p.returncode, p.stdout, p.stderr)
        )
        return p, json.loads(p.stdout)

    def chain_of(self, doc, chain_id=CHAIN_ID):
        for chain in doc["chains"]:
            if chain["id"] == chain_id:
                return chain
        self.fail("사슬 %s 가 출력에 없다: %s" % (chain_id, [c["id"] for c in doc["chains"]]))


class TestCase01LaggingCounts(MetricsTestBase):
    """① intent 2수정 → spec → intent 2수정 → plan → spec 1수정 이력에서 L3=2, L4=1."""

    def test_l3_and_l4_counts(self):
        repo = self.new_repo()
        shas = build_h1(repo)
        _, doc = self.json_metrics(repo)
        chain = self.chain_of(doc)
        self.assertEqual(chain["metrics"]["l3"]["status"], "ok", chain["metrics"]["l3"])
        self.assertEqual(chain["metrics"]["l3"]["value"], 2)
        self.assertEqual(chain["metrics"]["l4"]["status"], "ok", chain["metrics"]["l4"])
        self.assertEqual(chain["metrics"]["l4"]["value"], 1)
        # 계기가 어느 커밋을 기준선으로 잡았는지도 계약이다.
        self.assertEqual(chain["metrics"]["l3"]["inputs"]["base_commit"], shas["c4_spec_create"])
        self.assertEqual(chain["metrics"]["l4"]["inputs"]["base_commit"], shas["c7_plan_create"])

    def test_l1_l2_leading_seconds(self):
        repo = self.new_repo()
        shas = build_h1(repo)
        _, doc = self.json_metrics(repo)
        m = self.chain_of(doc)["metrics"]
        # L1: created(신고 10:12) → intent 최초 커밋(11:00) = 48분.
        self.assertEqual(m["l1"]["status"], "ok", m["l1"])
        self.assertEqual(m["l1"]["value"], 48 * 60)
        self.assertEqual(m["l1"]["unit"], "seconds")
        self.assertIn("신고값", m["l1"]["method"] + json.dumps(m["l1"]["inputs"], ensure_ascii=False))
        # L1b: created → status 가 accepted 로 바뀐 커밋(13:00) = 2시간 48분.
        self.assertEqual(m["l1_accepted"]["status"], "ok", m["l1_accepted"])
        self.assertEqual(m["l1_accepted"]["value"], (2 * 60 + 48) * 60)
        self.assertEqual(m["l1_accepted"]["inputs"]["accepted_commit"], shas["c3_intent_accept"])
        # L2: intent 최초 커밋(09-09 11:00) → spec 최초 커밋(09-10 09:00) = 22시간.
        self.assertEqual(m["l2"]["status"], "ok", m["l2"])
        self.assertEqual(m["l2"]["value"], 22 * 3600)


class TestCase02SameSecondBoundary(MetricsTestBase):
    """② spec 최초 커밋과 **같은 초**에 있는 intent 수정을 위상 계산이 세지 않는가.

    `git log --since=<spec 시각>` 은 같은 초의 커밋을 **포함한다**. 시계 기반 구현이면
    여기서 3 이 나와 red 가 된다. 위상(`git rev-list <sha>..HEAD -- <경로>`)은 그
    커밋이 spec 커밋의 **조상**이므로 세지 않는다.
    """

    def test_same_second_ancestor_is_not_counted(self):
        repo = self.new_repo()
        body = fixture("intent-draft.md")
        c1 = repo.commit(intent_path(), body, "2026-09-09T11:00:00+09:00", "feat: intent")
        c2 = repo.commit(
            intent_path(), body + "\n<!-- m1 -->\n", "2026-09-10T08:59:59+09:00", "docs: m1"
        )
        same_second = "2026-09-10T09:00:00+09:00"
        c3 = repo.commit(
            intent_path(), body + "\n<!-- m1 -->\n<!-- m2 -->\n", same_second, "docs: m2 (같은 초)"
        )
        c4 = repo.commit(spec_path(), fixture("spec.md"), same_second, "feat: spec (같은 초)")
        c5 = repo.commit(
            intent_path(), body + "\n<!-- m1 -->\n<!-- m2 -->\n<!-- m3 -->\n",
            "2026-09-10T10:00:00+09:00", "docs: m3",
        )
        c6 = repo.commit(
            intent_path(), body + "\n<!-- m1 -->\n<!-- m2 -->\n<!-- m3 -->\n<!-- m4 -->\n",
            "2026-09-10T11:00:00+09:00", "docs: m4",
        )

        # --- 양성 대조: 경계가 실제로 존재하는가 (없으면 이 시험은 아무것도 안 잰다) ---
        self.assertEqual(
            repo.author_date(c3)[:19], repo.author_date(c4)[:19],
            "c3 과 c4 가 같은 초가 아니다 — 픽스처가 경계를 안 만들었다",
        )
        self.assertEqual(
            repo.git("merge-base", "--is-ancestor", c3, c4, check=False).returncode, 0,
            "c3 이 c4 의 조상이 아니다 — 위상 판정의 전제가 안 선다",
        )
        # --- 음성 대조: 시계 기반으로 세면 3 이 나온다는 사실을 이 자리에서 못박는다 ---
        clock = repo.git(
            "log", "--since=%s" % repo.author_date(c4), "--format=%H", "--", intent_path()
        ).stdout.split()
        self.assertEqual(
            len(clock), 3,
            "시계(--since) 계산이 3 이 아니다 — 이 시험이 가르려는 두 구현이 이미 같다",
        )
        self.assertIn(c3, clock)

        _, doc = self.json_metrics(repo)
        l3 = self.chain_of(doc)["metrics"]["l3"]
        self.assertEqual(l3["status"], "ok", l3)
        self.assertEqual(l3["value"], 2, "같은 초의 조상 커밋(c3)이 세어졌다 — 시계 기반 구현이다")
        # 기준선이 실제로 spec 최초 커밋인가(값만 맞고 다른 곳을 재는 경우를 가른다).
        self.assertEqual(l3["inputs"]["base_commit"], c4)
        # 계기 서술에 계산 명령이 실려 있는가. `--since` 를 쓰는지 여부는 여기서
        # 문자열로 재지 않는다 — method 산문이 「--since 를 쓰지 않는다」고 설명하므로
        # 문자열 검사는 거짓 양성을 낸다. 시계/위상의 판별은 위의 값 단정이 한다.
        self.assertIn("rev-list", l3["method"])
        del c1, c2, c5, c6


class TestCase03CreatedInFuture(MetricsTestBase):
    """③ `created` 가 최초 커밋보다 미래면 L1 을 음수로 내지 않고 unavailable + reason."""

    def test_future_created_is_unavailable_not_negative(self):
        repo = self.new_repo()
        repo.commit(
            intent_path(), fixture("intent-created-future.md"),
            T_INTENT_CREATE, "feat: intent(미래 created)",
        )
        _, doc = self.json_metrics(repo)
        l1 = self.chain_of(doc)["metrics"]["l1"]
        self.assertEqual(l1["status"], "unavailable", l1)
        self.assertIsNone(l1["value"])
        self.assertTrue(l1.get("reason"), "unavailable 인데 reason 이 없다")


class TestCase04CreatedMalformed(MetricsTestBase):
    """④ `created` 가 없거나 오프셋 없는 ISO8601 이면 unavailable + reason."""

    def test_created_missing(self):
        repo = self.new_repo("missing")
        repo.commit(
            intent_path(), fixture("intent-created-missing.md"),
            T_INTENT_CREATE, "feat: intent(created 없음)",
        )
        _, doc = self.json_metrics(repo)
        l1 = self.chain_of(doc)["metrics"]["l1"]
        self.assertEqual(l1["status"], "unavailable", l1)
        self.assertIsNone(l1["value"])
        self.assertIn("created", l1.get("reason", ""))

    def test_created_without_utc_offset(self):
        repo = self.new_repo("nooffset")
        repo.commit(
            intent_path(), fixture("intent-created-no-offset.md"),
            T_INTENT_CREATE, "feat: intent(오프셋 없는 created)",
        )
        _, doc = self.json_metrics(repo)
        l1 = self.chain_of(doc)["metrics"]["l1"]
        self.assertEqual(
            l1["status"], "unavailable",
            "오프셋 없는 created 를 그대로 계산했다 — 로컬 시간대에 따라 값이 달라진다: %s" % l1,
        )
        self.assertIsNone(l1["value"])
        # 사유가 「오프셋」을 지목해야 한다. status 만 보면 못 가른다: 오프셋 없는 시각을
        # UTC 로 간주하는 느슨한 구현도 시간대에 따라서는 「created 가 미래」 갈래로 빠져
        # 같은 unavailable 을 내고, 그러면 이 시험이 두 구현을 구별하지 못한다.
        # (뮤테이션 M2 가 실제로 이 자리를 통과했다 — 그래서 픽스처 시각을 옮기고
        #  사유까지 단정한다.)
        self.assertIn(
            "오프셋", l1.get("reason", ""),
            "unavailable 사유가 오프셋 문제를 지목하지 않는다: %s" % l1.get("reason"),
        )


class TestCase05NoChains(MetricsTestBase):
    """⑤ 사슬이 하나도 없으면 rc=0 + 명시 메시지."""

    def test_empty_repo_is_rc0_with_explicit_message(self):
        repo = self.new_repo()
        repo.commit("README.md", "# 사슬 없는 저장소\n", T_INTENT_CREATE, "chore: seed")
        p = self.run_metrics(repo, "--format", "text")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("사슬 없음", p.stdout)
        pj = self.run_metrics(repo, "--format", "json")
        self.assertEqual(pj.returncode, 0, pj.stdout + pj.stderr)
        doc = json.loads(pj.stdout)
        self.assertEqual(doc["chains"], [])
        self.assertTrue(any("사슬 없음" in n for n in doc.get("notes", [])), doc.get("notes"))


class TestCase06NotAGitRepo(MetricsTestBase):
    """⑥ git 저장소가 아닌 디렉터리 → rc=2(판정 불가)."""

    def test_non_git_directory_is_rc2(self):
        repo = self.new_repo(init=False)
        (repo.path / "README.md").write_text("not a repo\n", encoding="utf-8")
        p = self.run_metrics(repo, "--format", "json")
        self.assertEqual(p.returncode, 2, "rc=%d stdout=%s stderr=%s" % (p.returncode, p.stdout, p.stderr))


class TestCase07GhMissing(MetricsTestBase):
    """⑦ `gh` 가 PATH 에 없으면 L5 는 unavailable + reason 이고 rc 는 0 이다(조용한 0 금지)."""

    def test_survival_rate_unavailable_without_gh(self):
        repo = self.new_repo()
        build_h1(repo)
        p, doc = self.json_metrics(repo)
        l5 = doc["repo_metrics"]["l5"]
        self.assertEqual(
            l5["status"], "unavailable",
            "gh 가 없는데 status 가 unavailable 이 아니다 — 조용한 0: %s" % l5,
        )
        self.assertIsNone(l5["value"], "gh 없이 survival rate 에 값이 실렸다: %s" % l5)
        self.assertIn("gh", l5.get("reason", ""))
        self.assertEqual(p.returncode, 0)


class TestCase08JsonShape(MetricsTestBase):
    """⑧ `--format json` 에 schema_version 이 있고 모든 지표에 status 가 있다."""

    def test_schema_version_and_status_everywhere(self):
        repo = self.new_repo()
        build_h1(repo)
        _, doc = self.json_metrics(repo)
        self.assertIn("schema_version", doc)
        self.assertTrue(doc["schema_version"])
        allowed = {"ok", "unavailable", "not_applicable"}
        seen = 0
        buckets = [c["metrics"] for c in doc["chains"]] + [doc["repo_metrics"]]
        for metrics in buckets:
            for key, m in metrics.items():
                seen += 1
                for field in ("value", "unit", "method", "inputs", "status"):
                    self.assertIn(field, m, "%s 에 %s 가 없다" % (key, field))
                self.assertIn(m["status"], allowed, "%s status=%r" % (key, m["status"]))
                if m["status"] == "unavailable":
                    self.assertTrue(m.get("reason"), "%s 가 unavailable 인데 reason 이 없다" % key)
        self.assertGreaterEqual(seen, 6, "지표가 %d개뿐 — 계기가 비어 있다" % seen)


class TestCase09TextShowsCommands(MetricsTestBase):
    """텍스트 출력이 「무엇을 어떤 명령으로 셌는가」를 함께 낸다(계기 자체가 검증 가능해야)."""

    def test_text_output_carries_methods(self):
        repo = self.new_repo()
        build_h1(repo)
        p = self.run_metrics(repo, "--format", "text")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("git rev-list", p.stdout)
        self.assertIn("--diff-filter=A", p.stdout)
        self.assertIn("신고값", p.stdout)
        self.assertIn("|", p.stdout, "마크다운 표가 아니다")


class TestCase10ArgErrors(MetricsTestBase):
    """인자·저장소 오류는 rc=1(rc=2 인 「판정 불가」와 다른 자리)."""

    def test_unknown_id_is_rc1(self):
        repo = self.new_repo()
        build_h1(repo)
        p = self.run_metrics(repo, "--id", "9999-nope", "--format", "json")
        self.assertEqual(p.returncode, 1, p.stdout + p.stderr)

    def test_bad_format_is_rc1(self):
        repo = self.new_repo()
        build_h1(repo)
        p = self.run_metrics(repo, "--format", "yaml")
        self.assertEqual(p.returncode, 1, p.stdout + p.stderr)

    def test_missing_repo_path_is_rc1(self):
        repo = self.new_repo()
        p = subprocess.run(
            [sys.executable, str(SCRIPT), "--repo", str(repo.path / "does-not-exist")],
            env=repo.env, capture_output=True, text=True,
        )
        self.assertEqual(p.returncode, 1, p.stdout + p.stderr)


class TestCase11SurvivalWithFakeGh(MetricsTestBase):
    """gh 가 **있는** 경로: 가짜 gh 로 survival rate 산식을 네트워크 없이 잰다.

    intent/**/intent.md 를 담은 PR 만 세고, merged/(merged+closed) 를 낸다.
    OPEN 은 분모에 들어가지 않는다.
    """

    def test_merged_over_merged_plus_closed(self):
        repo = self.new_repo()
        build_h1(repo)
        repo.install_fake_gh(
            [
                {"number": 1, "state": "MERGED", "files": [{"path": "intent/0001-a/intent.md"}]},
                {"number": 2, "state": "CLOSED", "files": [{"path": "intent/0002-b/intent.md"}]},
                {"number": 3, "state": "MERGED", "files": [{"path": "README.md"}]},
                {"number": 4, "state": "OPEN", "files": [{"path": "intent/0003-c/intent.md"}]},
            ]
        )
        self.assertIsNotNone(
            shutil.which("gh", path=repo.path_env), "가짜 gh 가 PATH 에 안 보인다 — 계기 고장"
        )
        _, doc = self.json_metrics(repo)
        l5 = doc["repo_metrics"]["l5"]
        self.assertEqual(l5["status"], "ok", l5)
        self.assertAlmostEqual(l5["value"], 0.5)
        self.assertEqual(l5["inputs"]["merged"], 1)
        self.assertEqual(l5["inputs"]["closed"], 1)
        self.assertEqual(sorted(l5["inputs"]["pr_numbers"]), [1, 2])


if __name__ == "__main__":
    unittest.main()
