"""tests/test_plays_status.py — docs/plays/*.md 「지금 상태」 표·산문의 계기.

왜 있는가: 이 표와 그 산문은 손으로 적은 원장이고, 형제 PR 이 머지되는 순간
아무 소리 없이 거짓이 된다. 실제로 그렇게 됐다 — 표만 고치고 산문 20줄을
남겨 같은 파일 안에서 표와 산문이 서로 다른 말을 했다(PR #4·#5·#7 은 main 에
착지했는데 산문은 「대기」라고 적고 있었다). 기계가 원장을 고쳐서는 안 되지만,
원장이 틀렸다고 우는 것은 기계의 일이다.

무엇을 재는가 — 넷:
  L(살아 있음) docs/plays/*.md 8장 전부가 「## 지금 상태」 표를 갖고 데이터
              행이 1행 이상이며 60줄 이하다. 파서가 아무것도 못 찾고 조용히
              통과하는 「부재 PASS」를 막는 양성 계약이다.
  T(표↔git)   표 각 행의 라벨을 기준 ref 의 실물과 대조한다.
              「착지…」  → 그 경로가 기준 ref 에 있어야 한다.
              「대기(PR #N)」 → 그 경로가 기준 ref 에 없어야 한다(있으면 그 PR 은
              이미 머지된 것이고 라벨이 거짓이다).
  P(산문↔표)  산문이 「PR #N … 대기」라고 쓸 수 있는 N 은 그 파일 표가 대기로
              적은 PR 번호뿐이다. 표만 고치고 산문을 남기면 여기서 빨개진다.
  R(산문 「없음」) 산문이 어떤 경로를 「(없음)」이라 적었는데 같은 파일 표가 그
              경로를 다른 라벨로 적었으면 자기모순이다.

기준 ref: 라벨 「착지」의 뜻은 「main 에 착지」이므로 origin/main 을 먼저 쓴다
(CI 는 actions/checkout fetch-depth: 0 이라 remote-tracking ref 가 있다).
없으면 main, 그것도 없으면 HEAD 로 내려가고 어느 ref 로 쟀는지 실패 메시지에
찍는다. git 자체가 없으면 통과시키지 않고 skip 한다 — 못 잰 것은 통과가 아니다.

무엇을 재지 않는가: 라벨 「없음」 행(경로 칸이 「—」다) · 「착지(레포 설정)」
행(경로 칸이 레포 경로가 아니라 GitHub rulesets API 다) · 표 밖 산문의 사실성
일반(PR 번호와 「없음」 두 형태만 잡는다) · 그 PR 이 실제로 열려 있는지
(GitHub 조회는 오프라인 계기가 아니다).
"""

import os
import re
import subprocess
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAYS = os.path.join(ROOT, "docs", "plays")
MAX_LINES = 60
EXPECTED_FILES = 8


def _git(*args):
    return subprocess.run(
        ["git"] + list(args), cwd=ROOT, capture_output=True, text=True
    )


def resolve_base_ref():
    """착지/대기 를 판정할 기준 ref. 없으면 None(= git 없음)."""
    if _git("rev-parse", "--git-dir").returncode != 0:
        return None
    for ref in ("origin/main", "main", "HEAD"):
        if _git("rev-parse", "--verify", "--quiet", ref + "^{commit}").returncode == 0:
            return ref
    return None


def exists_at(ref, path):
    return _git("cat-file", "-e", "%s:%s" % (ref, path)).returncode == 0


def play_files():
    return sorted(
        os.path.join(PLAYS, f) for f in os.listdir(PLAYS) if f.endswith(".md")
    )


def parse(path):
    """(표 행 리스트, 산문 줄 리스트) — 표 행은 (줄번호, 라벨, 경로 or None)."""
    rows = []
    prose = []
    with open(path, encoding="utf-8") as f:
        for i, raw in enumerate(f.read().splitlines(), 1):
            line = raw.strip()
            if line.startswith("|"):
                cells = [c.strip() for c in line.strip("|").split("|")]
                if len(cells) < 3:
                    continue
                if cells[1] in ("상태",) or set(cells[1]) <= set("-: "):
                    continue  # 머리글·구분선
                m = re.search(r"`([^`]+)`", cells[2])
                rows.append((i, cells[1], m.group(1) if m else None))
            else:
                prose.append((i, raw))
    return rows, prose


def table_pending_prs(rows):
    out = set()
    for _, label, _ in rows:
        m = re.match(r"대기\(PR #(\d+)\)", label)
        if m:
            out.add(int(m.group(1)))
    return out


def prose_pending_prs(prose):
    """(줄번호, PR 번호) — 「대기」를 달고 있는 PR #N 언급.

    한 줄 안에서 끝나기도 하고 「PR #6\\n  대기)」 처럼 줄바꿈으로 갈라지기도
    하므로, 그 줄과 바로 다음 줄을 이어 붙인 창에서 본다."""
    out = []
    for idx, (lineno, text) in enumerate(prose):
        nxt = prose[idx + 1][1] if idx + 1 < len(prose) else ""
        window = text + " " + nxt.strip()
        for m in re.finditer(r"PR\s*#(\d+)", text):
            tail = window[m.start() : m.start() + 40]
            if "대기" in tail:
                out.append((lineno, int(m.group(1))))
    return out


def prose_absent_paths(prose):
    """(줄번호, 경로) — 「(없음)」 이라고 적은 줄 및 그 앞 두 줄의 백틱 경로."""
    out = []
    for idx, (lineno, text) in enumerate(prose):
        if "(없음)" not in text:
            continue
        window = " ".join(t for _, t in prose[max(0, idx - 2) : idx + 1])
        for m in re.finditer(r"`([^`]+)`", window):
            out.append((lineno, m.group(1)))
    return out


class PlaysStatusLiveness(unittest.TestCase):
    """L — 파서가 실제로 무언가를 보고 있다는 양성 대조."""

    def test_files_tables_and_length(self):
        files = play_files()
        self.assertEqual(
            len(files), EXPECTED_FILES, "docs/plays/*.md 는 %d장이어야 한다: %s"
            % (EXPECTED_FILES, [os.path.basename(f) for f in files]),
        )
        for path in files:
            name = os.path.basename(path)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            self.assertIn("## 지금 상태", text, "%s 에 「## 지금 상태」 절이 없다" % name)
            n = len(text.splitlines())
            self.assertLessEqual(n, MAX_LINES, "%s 이 %d줄 — %d줄 이하" % (name, n, MAX_LINES))
            rows, _ = parse(path)
            self.assertGreaterEqual(len(rows), 1, "%s 표에서 데이터 행을 못 찾았다" % name)


class PlaysStatusTableMatchesGit(unittest.TestCase):
    """T — 표 라벨 ↔ 기준 ref 의 실물."""

    def test_labels_match_repository(self):
        ref = resolve_base_ref()
        if ref is None:
            self.skipTest("git 저장소가 아니라 착지/대기를 판정할 수 없다 — 못 잰 것은 통과가 아니다")
        bad = []
        checked = 0
        for path in play_files():
            name = os.path.basename(path)
            rows, _ = parse(path)
            for lineno, label, target in rows:
                if target is None:
                    continue  # 경로 칸이 「—」 등 레포 경로가 아닌 행
                if not (label.startswith("착지") or label.startswith("대기")):
                    continue
                if label.startswith("착지") and "(" in label:
                    continue  # 「착지(레포 설정)」 — 레포 경로가 아니다
                checked += 1
                here = exists_at(ref, target)
                if label.startswith("착지") and not here:
                    bad.append("%s:%d 「착지」인데 %s 에 %s 가 없다" % (name, lineno, ref, target))
                if label.startswith("대기") and here:
                    bad.append(
                        "%s:%d 「%s」인데 %s 에 %s 가 이미 있다 — 그 PR 은 머지됐고 표가 낡았다"
                        % (name, lineno, label, ref, target)
                    )
        self.assertGreater(checked, 0, "대조한 행이 0 — 파서가 표를 못 읽었다(계기 고장)")
        self.assertEqual(bad, [], "기준 ref=%s\n" % ref + "\n".join(bad))


class PlaysStatusProseMatchesTable(unittest.TestCase):
    """P·R — 같은 파일 안에서 산문과 표가 같은 말을 하는가."""

    def test_prose_pending_pr_is_in_table(self):
        bad = []
        seen = 0
        for path in play_files():
            name = os.path.basename(path)
            rows, prose = parse(path)
            pending = table_pending_prs(rows)
            for lineno, num in prose_pending_prs(prose):
                seen += 1
                if num not in pending:
                    bad.append(
                        "%s:%d 산문이 PR #%d 를 「대기」라 적는데 이 파일 표의 대기 목록은 %s"
                        % (name, lineno, num, sorted(pending) or "비어 있다")
                    )
        self.assertGreater(seen, 0, "산문에서 「대기 PR」 언급을 0건 찾았다(계기 고장)")
        self.assertEqual(bad, [], "\n".join(bad))

    def test_prose_absent_claim_matches_table(self):
        bad = []
        for path in play_files():
            name = os.path.basename(path)
            rows, prose = parse(path)
            labels = {}
            for _, label, target in rows:
                if target:
                    labels[target] = label
            for lineno, target in prose_absent_paths(prose):
                label = labels.get(target)
                if label is not None and not label.startswith("없음"):
                    bad.append(
                        "%s:%d 산문은 %s 를 「(없음)」이라 적는데 표는 「%s」라 적는다"
                        % (name, lineno, target, label)
                    )
        self.assertEqual(bad, [], "\n".join(bad))


if __name__ == "__main__":
    unittest.main()
