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
GATE50 = REPO_ROOT / "scripts" / "gates" / "50-metrics.sh"
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
        # PATH 셰임 — 「gh 가 안 보이고 git 은 보이는」 상태를 기계마다 다시 만든다.
        # 시스템 경로를 손으로 박지 않는다: GitHub 호스티드 러너는 `gh` 와 `git` 이
        # **같은 디렉터리**(/usr/bin)에 있고 /bin 이 그리로 가는 심링크라, 경로를
        # 하드코딩하면 개발자 기계에서만 성립하는 셰임이 된다. 그래서
        #   ① 진짜 git 을 셰임 디렉터리에 심링크로 들여놓고
        #   ② PATH 에서 `gh` 를 담고 있는 디렉터리를 전부 뺀다.
        # git 의 하위 명령은 PATH 가 아니라 GIT_EXEC_PATH 에서 오므로 이래도 돈다.
        real_git = shutil.which("git")
        if real_git:
            link = self.shim / "git"
            if not link.exists():
                link.symlink_to(real_git)
        kept = [
            d
            for d in (os.environ.get("PATH") or "").split(os.pathsep)
            if d and shutil.which("gh", path=d) is None
        ]
        self.path_env = os.pathsep.join([str(self.shim)] + kept)
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
        # 가짜 gh 는 **외부 명령을 하나도 쓰지 않는다.** 셰임 PATH 는 gh 를 담은
        # 디렉터리를 전부 빼는데, 러너에서는 그게 /usr/bin(그리고 그리로 가는
        # 심링크 /bin)이라 `cat`·`bash` 까지 함께 사라진다. 셰방을 이 파이썬의
        # 절대 경로로 박고 표준 라이브러리만 쓰면 PATH 탐색이 아예 일어나지 않는다.
        gh.write_text(
            "#!%s\nimport sys\nsys.stdout.write(%r)\n"
            % (sys.executable, json.dumps(payload)),
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


class TestCase12CodeSpanIsNotAcceptance(MetricsTestBase):
    """본문의 코드 스팬 안 `status: accepted` 는 승인이 아니다 — 승인 커밋을 오판하면
    l1_accepted 가 l1 과 같은 값으로 붕괴한다(실물 사고: PR #12 intent.md L17 인라인 스팬).

    픽스액스(`git log -S`)는 **문자열 등장 횟수**만 보므로 draft 로 태어난 커밋도
    후보로 낸다. 후보마다 그 시점 파일의 frontmatter 를 실제로 파싱해야 갈린다.
    """

    def test_draft_born_with_code_span_is_not_the_accepted_commit(self):
        repo = self.new_repo()
        c1 = repo.commit(
            intent_path(), fixture("intent-draft-code-span.md"),
            T_INTENT_CREATE, "feat: intent 발의(draft · 본문에 예시 status: accepted)",
        )
        c2 = repo.commit(
            intent_path(), fixture("intent-accepted-code-span.md"),
            T_INTENT_ACCEPT, "chore: intent 승인(frontmatter status 한 줄)",
        )
        # 양성 대조: 두 커밋이 **둘 다** 픽스액스 후보여야 이 시험이 뜻을 갖는다.
        cand = repo.git(
            "log", "-Sstatus: accepted", "--format=%H", "--", intent_path()
        ).stdout.split()
        self.assertEqual(sorted(cand), sorted([c1, c2]), "픽스액스 후보가 둘이 아니다 — 계기 고장")

        _, doc = self.json_metrics(repo)
        m = self.chain_of(doc)["metrics"]
        l1a = m["l1_accepted"]
        self.assertEqual(l1a["status"], "ok", l1a)
        self.assertEqual(
            l1a["inputs"]["accepted_commit"], c2,
            "승인 커밋을 %s 로 골랐다 — draft 로 태어난 커밋(%s)이면 코드 스팬 오판이다" % (
                l1a["inputs"]["accepted_commit"], c1,
            ),
        )
        # created(10:12) → 승인 커밋(13:00) = 2시간 48분.
        self.assertEqual(l1a["value"], (2 * 60 + 48) * 60, l1a)
        # l1 과 같은 값으로 붕괴하지 않는다.
        self.assertNotEqual(l1a["value"], m["l1"]["value"], "l1 과 l1_accepted 가 붕괴했다")


class TestCase13ExampleOnlyIsUnavailable(MetricsTestBase):
    """후보는 있는데 전부 예시였다면 `unavailable` + 사유다 — 0 도, 임의값도, 조용한
    not_applicable 도 아니다. 「승인이 아직 없다」와 「후보를 못 골랐다」는 다른 일이다."""

    def test_all_candidates_filtered_is_unavailable_with_reason(self):
        repo = self.new_repo()
        c1 = repo.commit(
            intent_path(), fixture("intent-draft-code-span.md"),
            T_INTENT_CREATE, "feat: intent 발의(draft · 예시만 있다)",
        )
        _, doc = self.json_metrics(repo)
        l1a = self.chain_of(doc)["metrics"]["l1_accepted"]
        self.assertEqual(l1a["status"], "unavailable", l1a)
        self.assertIsNone(l1a["value"], l1a)
        self.assertTrue(l1a.get("reason"), "unavailable 인데 사유가 없다")
        self.assertIsNone(l1a["inputs"]["accepted_commit"], l1a)
        self.assertEqual(
            l1a["inputs"]["accepted_candidates"], [c1],
            "걸러진 후보 커밋이 출력에 남지 않았다 — 반증할 수 없는 값이 된다",
        )


class TestCase14NoCandidateStaysNotApplicable(MetricsTestBase):
    """예시조차 없는 순수 draft 는 기존대로 `not_applicable` 이다(두 갈래를 뭉개지 않는다)."""

    def test_plain_draft_is_not_applicable(self):
        repo = self.new_repo()
        repo.commit(
            intent_path(), fixture("intent-draft.md"), T_INTENT_CREATE, "feat: intent 발의"
        )
        _, doc = self.json_metrics(repo)
        l1a = self.chain_of(doc)["metrics"]["l1_accepted"]
        self.assertEqual(l1a["status"], "not_applicable", l1a)
        self.assertEqual(l1a["inputs"]["accepted_candidates"], [], l1a)


class TestCase15Gate50StandaloneSkipContract(MetricsTestBase):
    """50-metrics.sh 의 **단독 실행 대역**도 정본(check_all.sh 의 run_gate)과 같은
    3분법이어야 한다: rc 0 = PASS · 3 = SKIP · 그 밖 = FAIL.

    비침습으로 잰다 — 실파일을 임시 트리의 `scripts/gates/` 로 복사하면 GATE50_ROOT
    가 그 임시 트리가 되므로, PATH 앞의 python3 셰임만으로 rc 를 태울 수 있다.
    대역을 한 줄도 고치지 않고 계약만 관측한다.
    """

    def _run_with_python3_shim(self, shim_rc):
        root = self.tmp / ("gate50-rc%d" % shim_rc)
        (root / "scripts" / "gates").mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(GATE50), str(root / "scripts" / "gates" / "50-metrics.sh"))
        shim = root / "shim"
        shim.mkdir(exist_ok=True)
        fake = shim / "python3"
        fake.write_text("#!/bin/sh\nexit %d\n" % shim_rc, encoding="utf-8")
        fake.chmod(0o755)
        env = dict(os.environ)
        env["PATH"] = os.pathsep.join([str(shim), env.get("PATH", "")])
        # 양성 대조: 셰임이 실제로 앞에 서지 않으면 이 측정은 아무것도 재지 않는다.
        self.assertEqual(
            shutil.which("python3", path=env["PATH"]), str(fake),
            "python3 셰임이 PATH 앞에 서지 않았다 — 계기 고장",
        )
        return subprocess.run(
            ["bash", str(root / "scripts" / "gates" / "50-metrics.sh")],
            env=env, capture_output=True, text=True,
        )

    def test_positive_control_rc0_is_two_passes(self):
        p = self._run_with_python3_shim(0)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("2 passed, 0 failed", p.stdout, p.stdout + p.stderr)

    def test_rc3_is_skip_not_fail(self):
        p = self._run_with_python3_shim(3)
        out = p.stdout + p.stderr
        self.assertIn("SKIP", p.stdout, "rc=3 인데 SKIP 줄이 없다\n" + out)
        self.assertIn("0 passed, 1 failed, 1 skipped", p.stdout, out)


# 시각 — 재승인 사슬(draft → accepted → draft → accepted).
T_REACCEPT_1 = "2026-09-09T12:00:00+09:00"   # 1차 승인
T_REACCEPT_REVERT = "2026-09-09T13:00:00+09:00"  # 되돌림(draft)
T_REACCEPT_2 = "2026-09-09T14:00:00+09:00"   # 2차 승인(재승인)


class TestCase16ReacceptanceChainPicksOldest(MetricsTestBase):
    """재승인 사슬에서 **가장 오래된 확인된 승인 커밋**을 고른다.

    이건 가상의 이력이 아니다 — 이 저장소의 #12 spec.md 가 이미
    draft→accepted→draft→accepted 다. 재승인이 있으면 픽스액스 후보가 셋이고,
    그중 **오래된 쪽**이 「승인까지 걸린 시간」의 답이다. 최신 쪽을 고르면 같은
    이력에서 값이 두 배가 된다(합성 픽스처 실측: 7200 vs 14400).

    후보 순회 방향이 계약이므로 `accepted_candidates` 의 **순서**까지 단정한다 —
    값만 보면 순회를 뒤집어도 통과하는 구성이 있다.
    """

    def test_oldest_confirmed_acceptance_wins(self):
        repo = self.new_repo()
        draft = fixture("intent-draft.md")
        accepted = fixture("intent-accepted.md")
        c1 = repo.commit(intent_path(), draft, T_INTENT_CREATE, "feat: intent 발의(draft)")
        c2 = repo.commit(
            intent_path(), accepted, T_REACCEPT_1, "chore: 1차 승인(accepted)"
        )
        c3 = repo.commit(
            intent_path(), draft + "\n<!-- 되돌림 -->\n", T_REACCEPT_REVERT,
            "chore: 승인 철회(draft 로 되돌림)",
        )
        c4 = repo.commit(
            intent_path(), accepted + "\n<!-- 재승인 -->\n", T_REACCEPT_2,
            "chore: 재승인(accepted)",
        )

        # --- 양성 대조: 재승인 사슬이 실제로 후보를 셋 만드는가 ---
        cand = repo.git(
            "log", "-Sstatus: accepted", "--format=%H", "--", intent_path()
        ).stdout.split()
        self.assertEqual(
            sorted(cand), sorted([c2, c3, c4]),
            "픽스액스 후보가 c2·c3·c4 셋이 아니다 — 재승인 경계가 안 만들어졌다: %s" % cand,
        )
        self.assertNotIn(c1, cand, "draft 로 태어난 c1 이 후보다 — 픽스처가 잘못됐다")

        _, doc = self.json_metrics(repo)
        l1a = self.chain_of(doc)["metrics"]["l1_accepted"]
        self.assertEqual(l1a["status"], "ok", l1a)
        self.assertEqual(
            l1a["inputs"]["accepted_commit"], c2,
            "승인 커밋으로 %s 를 골랐다 — 재승인(c4=%s)을 고르면 값이 두 배가 된다"
            % (l1a["inputs"]["accepted_commit"], c4),
        )
        # created(10:12) → 1차 승인(12:00) = 1시간 48분. 재승인(14:00)이면 3시간 48분이다.
        self.assertEqual(l1a["value"], (60 + 48) * 60, l1a)
        self.assertNotEqual(l1a["value"], (3 * 60 + 48) * 60, "재승인 쪽을 골랐다")
        # 후보 목록은 오래된 → 새로운 순이어야 한다(순회 방향이 곧 이 지표의 계약이다).
        self.assertEqual(
            l1a["inputs"]["accepted_candidates"], [c2, c3, c4],
            "후보 목록의 순서가 오래된 → 새로운 순이 아니다",
        )


class TestCase17StripCodeSpansIsLoadBearing(MetricsTestBase):
    """`strip_code_spans` 를 항등으로 바꾸면 **답이 달라지는** 구성 셋.

    스팬 제거를 지나가는 장식으로 두면 위조가 통한다. 그래서 「제거가 실제로
    답을 바꾸는」 자리만 골라 잰다 — 제거하든 말든 같은 답이 나오는 문서로는
    이 계약을 증언할 수 없다(기존 픽스처 2종이 그랬다).
    """

    def _candidates(self, repo):
        return repo.git(
            "log", "-Sstatus: accepted", "--format=%H", "--", intent_path()
        ).stdout.split()

    def test_fence_before_frontmatter_is_not_acceptance(self):
        """① 예시 펜스가 진짜 frontmatter **앞**에 있다 — 벗기지 않으면 첫 `---`
        블록이 예시 쪽이라 accepted 로 읽힌다."""
        repo = self.new_repo("fence-before")
        c1 = repo.commit(
            intent_path(), fixture("intent-fence-before-frontmatter.md"),
            T_INTENT_CREATE, "feat: intent(예시 펜스가 frontmatter 앞)",
        )
        self.assertEqual(self._candidates(repo), [c1], "후보가 c1 하나가 아니다 — 계기 고장")
        _, doc = self.json_metrics(repo)
        l1a = self.chain_of(doc)["metrics"]["l1_accepted"]
        self.assertEqual(l1a["status"], "unavailable", l1a)
        self.assertIsNone(
            l1a["inputs"]["accepted_commit"],
            "펜스 안 예시를 승인으로 읽었다 — 코드 스팬 제거가 죽어 있다: %s" % l1a,
        )
        self.assertIn(
            "status='draft'", l1a.get("reason", ""),
            "그 시점 status 를 draft 로 읽지 않았다: %s" % l1a.get("reason"),
        )

    def test_span_valued_status_is_not_acceptance(self):
        """② frontmatter 의 **값 자체**가 인라인 스팬이다(`` status: `accepted` ``).
        벗기면 빈 값, 안 벗기면 백틱째 — 사유 문자열이 둘을 가른다."""
        repo = self.new_repo("span-value")
        c1 = repo.commit(
            intent_path(), fixture("intent-span-valued-status.md"),
            T_INTENT_CREATE, "feat: intent(status 값이 인라인 스팬)",
        )
        self.assertEqual(self._candidates(repo), [c1], "후보가 c1 하나가 아니다 — 계기 고장")
        _, doc = self.json_metrics(repo)
        l1a = self.chain_of(doc)["metrics"]["l1_accepted"]
        self.assertEqual(l1a["status"], "unavailable", l1a)
        self.assertIsNone(l1a["inputs"]["accepted_commit"], l1a)
        self.assertIn(
            "status=''", l1a.get("reason", ""),
            "인라인 스팬을 벗긴 빈 값이 아니라 백틱째로 읽었다: %s" % l1a.get("reason"),
        )

    def test_fence_only_without_frontmatter_is_not_acceptance(self):
        """③ frontmatter 가 아예 없고 예시 펜스만 있다 — 벗기지 않으면 그 예시가
        frontmatter 로 승격한다."""
        repo = self.new_repo("fence-only")
        c1 = repo.commit(
            intent_path(), fixture("intent-fence-only-no-frontmatter.md"),
            T_INTENT_CREATE, "feat: intent(frontmatter 없이 예시 펜스만)",
        )
        self.assertEqual(self._candidates(repo), [c1], "후보가 c1 하나가 아니다 — 계기 고장")
        _, doc = self.json_metrics(repo)
        l1a = self.chain_of(doc)["metrics"]["l1_accepted"]
        self.assertEqual(l1a["status"], "unavailable", l1a)
        self.assertIsNone(
            l1a["inputs"]["accepted_commit"],
            "frontmatter 가 없는 문서를 승인으로 읽었다: %s" % l1a,
        )
        self.assertIn(
            "frontmatter 블록이 없다", l1a.get("reason", ""),
            "사유가 frontmatter 부재를 지목하지 않는다: %s" % l1a.get("reason"),
        )


class TestCase18CandidateEnumerationFailure(MetricsTestBase):
    """`git log -S` 가 rc≠0 인 갈래 — 후보를 **열거하지 못한** 것은 「승인이 없다」가
    아니다. unavailable + 사유이고, 사유는 git 이 실제로 한 말을 **문장으로** 싣는다.

    실물로 태운다: 커밋이 하나도 없는 저장소에서 `git log` 는 rc=128 이다(모의 없음).
    """

    def test_pickaxe_failure_is_unavailable_with_plain_reason(self):
        repo = self.new_repo("no-commits")
        # 커밋하지 않는다 — 워크트리에만 둔다(사슬 탐색은 파일 존재로 한다).
        repo.write(intent_path(), fixture("intent-accepted.md"))

        # --- 양성 대조: 이 상태에서 픽스액스가 실제로 실패하는가 ---
        probe = repo.git(
            "log", "-Sstatus: accepted", "--format=%H", "--", intent_path(), check=False
        )
        self.assertNotEqual(
            probe.returncode, 0,
            "커밋 없는 저장소에서 git log -S 가 rc=0 이다 — 이 시험이 재려는 갈래가 없다",
        )

        p, doc = self.json_metrics(repo)
        self.assertEqual(p.returncode, 0, "열거 실패가 계기 전체를 죽였다")
        l1a = self.chain_of(doc)["metrics"]["l1_accepted"]
        self.assertEqual(
            l1a["status"], "unavailable",
            "후보를 열거하지 못했는데 unavailable 이 아니다 — 「승인 없음」과 뭉갰다: %s" % l1a,
        )
        self.assertIsNone(l1a["value"], l1a)
        reason = l1a.get("reason", "")
        self.assertTrue(reason, "unavailable 인데 사유가 없다")
        self.assertIn("rc=%d" % probe.returncode, reason, reason)
        # F-REVA-6: 사유가 파이썬 리스트를 그대로 찍으면 사람이 읽는 문장이 아니다.
        self.assertNotIn("['", reason, "사유가 리스트 리터럴로 렌더된다: %s" % reason)
        self.assertNotIn('["', reason, "사유가 리스트 리터럴로 렌더된다: %s" % reason)
        # 사유는 git 이 실제로 한 말을 담아야 한다(빈 괄호로 삼키지 않는다).
        self.assertIn(
            "does not have any commits yet", reason,
            "git 이 낸 진단이 사유에 실리지 않았다: %s" % reason,
        )


class TestCase19OneToOneRewriteIsUnavailableNotApplicable(MetricsTestBase):
    """등재한 한계의 **결과값**을 못박는다.

    같은 커밋에서 본문 예시를 지우면서 frontmatter 를 accepted 로 바꾸면
    `status: accepted` 등장 횟수가 1→1 이라 픽스액스가 그 커밋을 후보로 내지
    않는다. 그때 나오는 값은 **후보 0건의 not_applicable 이 아니라**, 예시를
    들고 태어난 옛 커밋 1건이 교차 확인에서 걸러진 `unavailable` 이다.
    (문서가 not_applicable 이라고 적으면 「조용한 해당없음」을 기대하게 만든다 —
    실제로는 사유가 붙은 시끄러운 unavailable 이고, 그 편이 더 안전하다.)
    """

    def test_1to1_rewrite_yields_unavailable_with_one_candidate(self):
        repo = self.new_repo("one-to-one")
        c1 = repo.commit(
            intent_path(), fixture("intent-draft-one-example.md"),
            T_INTENT_CREATE, "feat: intent 발의(draft · 본문에 예시 1회)",
        )
        c2 = repo.commit(
            intent_path(), fixture("intent-accepted.md"),
            T_INTENT_ACCEPT, "chore: 예시를 지우면서 frontmatter 를 accepted 로(1→1)",
        )

        # --- 양성 대조: 등장 횟수가 정말 1→1 이어야 이 갈래가 성립한다 ---
        n1 = repo.git("show", "%s:%s" % (c1, intent_path())).stdout.count("status: accepted")
        n2 = repo.git("show", "%s:%s" % (c2, intent_path())).stdout.count("status: accepted")
        self.assertEqual((n1, n2), (1, 1), "등장 횟수가 1→1 이 아니다 — 픽스처가 갈래를 안 만들었다")
        cand = repo.git(
            "log", "-Sstatus: accepted", "--format=%H", "--", intent_path()
        ).stdout.split()
        self.assertEqual(cand, [c1], "진짜 승인 커밋 c2 가 후보에 있다 — 갈래가 안 선다: %s" % cand)

        _, doc = self.json_metrics(repo)
        l1a = self.chain_of(doc)["metrics"]["l1_accepted"]
        self.assertEqual(
            l1a["status"], "unavailable",
            "1→1 재작성 갈래가 not_applicable 로 나왔다 — 등재한 한계의 결과값이 다르다: %s" % l1a,
        )
        self.assertIsNone(l1a["value"], l1a)
        self.assertTrue(l1a.get("reason"), "unavailable 인데 사유가 없다")
        self.assertEqual(
            l1a["inputs"]["accepted_candidates"], [c1],
            "후보가 0건이 아니라 1건이어야 한다(예시를 들고 태어난 옛 커밋)",
        )
        self.assertIsNone(l1a["inputs"]["accepted_commit"], l1a)


if __name__ == "__main__":
    unittest.main()
