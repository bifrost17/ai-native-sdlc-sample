#!/usr/bin/env python3
"""scripts/check_artifacts.py — intent / spec / plan 아티팩트 검증기 (표준 라이브러리만).

무엇을 재는가
--------------
사슬(intent → spec → plan)이 **기계가 확인할 수 있는 형태로** 이어져 있는지만 잰다.
축마다 어휘의 소유자가 누구인지가 이 도구의 설계 기준이다(설계안 §5):

  우리 규약이 어휘를 소유  frontmatter 키 집합 · status enum · id/kind · 절 이름과 순서
  우리 템플릿이 소유       자리표시자 토큰 ‹ ›
  마크다운 문법 하나       코드 펜스 · 인라인 코드 (판정 **전에** 제거한다)
  git 이 소유 · 단일 통로  upstream <파일>@<sha> 해석 · 브랜치 위 자기 승인
  우리 ID 규약이 소유      C# / Q# 이어받기 · AC# ↔ R# · Proof 가 덮는 AC#

**하지 않는 것** (README·설계안 §5 에 같은 문장이 있다 — 안 보는 것을 보는 척하지 않는다)
  - 제목이 해법인지 대상인지 보지 않는다.
  - 산문의 품질(문장이 좋은지, 설명이 충분한지)을 보지 않는다.
  - 요구가 문제를 실제로 푸는지 보지 않는다.
  이 셋은 사람과 리뷰의 몫이다. 이 도구가 그린이라고 해서 아티팩트가 좋다는 뜻이 아니다.

계약
----
  rc 0  통과
  rc 1  결함(아티팩트가 규약을 어겼다)
  rc 2  판정 불가(파일이 없다 · git 이 sha 를 못 연다 · 형이 안 정해진다)
        — rc 2 는 통과가 아니다. 못 잰 것은 통과가 아니다.
  여러 파일을 한 번에 주면 rc 는 2 > 1 > 0 순으로 이긴다.

  `--format json` 은 schema_version 과 항목마다 안정된 `code` 를 낸다.
  소비자는 메시지 문자열이 아니라 `code` 로 분기해야 한다 — 메시지는 바뀔 수 있다.
"""

import argparse
import json
import os
import re
import subprocess
import sys

SCHEMA_VERSION = 1

STATUS_VALUES = ("draft", "accepted", "rejected", "superseded")

# 자리표시자 토큰. U+2039/U+203A 는 한국어·영어 산문에 자연 등장하지 않아
# 정상 문서의 대괄호([Art. 4])·인용부호(「」『』【】)와 절대 겹치지 않는다.
PLACEHOLDER_CHARS = ("‹", "›")

SEV_ERROR = "error"
SEV_UNDECIDABLE = "undecidable"
SEV_NOTE = "note"

ID_RE = re.compile(r"^\d{4}-[a-z0-9]+(?:-[a-z0-9]+)*$")
CREATED_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)
UPSTREAM_RE = re.compile(r"^(?P<file>[A-Za-z0-9][A-Za-z0-9_.-]*\.md)@(?P<sha>[0-9a-fA-F]{7,40})$")
HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.*?)\s*$")
TRAILING_PAREN_RE = re.compile(r"^(.*?)\s*\([^()]*\)\s*$")
FENCE_RE = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})")
LIST_ITEM_RE = re.compile(r"^\s*[-*]\s+([A-Z]+\d+)\b(.*)$")

SCHEMA = {
    "intent": {
        "keys": ["id", "kind", "status", "author", "created", "record", "supersedes"],
        "sections": [
            "Problem",
            "Proposed outcome",
            "Affected users and systems",
            "Constraints",
            "Open questions",
        ],
        "title": "Intent",
    },
    "spec": {
        "keys": ["id", "kind", "status", "upstream", "skills_applied"],
        "sections": [
            "Requirements",
            "Design",
            "Constraints inherited",
            "Constraints discovered",
            "Open questions from intent",
            "Flagged concerns",
            "Out of scope",
            "Acceptance criteria",
        ],
        "title": "Spec",
        "upstream_file": "intent.md",
    },
    "plan": {
        "keys": ["id", "kind", "status", "upstream"],
        "sections": [
            "Files that change",
            "Order of work",
            "Risks",
            "Proof",
            "Options not taken",
            "Parallelisable",
        ],
        "title": "Plan",
        "upstream_file": "spec.md",
    },
}

# 파일명 → 형. 변형 템플릿(결함·인시던트)도 결국 intent 다.
STEM_TO_TYPE = {
    "intent": "intent",
    "intent-defect": "intent",
    "intent-incident": "intent",
    "spec": "spec",
    "plan": "plan",
}

# spec 의 이 두 절은 intent 를 **다시 적으라고** 있는 자리다 — 복사 검사에서 뺀다.
COPY_EXEMPT_SPEC_SECTIONS = ("Constraints inherited", "Open questions from intent")
COPY_MIN_CHARS = 40


# --------------------------------------------------------------------------
# 코드 펜스 · 인라인 코드 제거 — 모든 판정보다 **먼저** 돈다.
# 펜스 안의 `status: accepted` 나 ‹자리표시자› 는 문서의 주장이 아니라 예시다.
# 줄 수를 보존해야 진단의 줄 번호가 원본과 맞는다.
# --------------------------------------------------------------------------
def strip_inline_code(line):
    out = []
    i = 0
    n = len(line)
    while i < n:
        if line[i] == "`":
            j = i
            while j < n and line[j] == "`":
                j += 1
            marker = "`" * (j - i)
            close = line.find(marker, j)
            if close == -1:
                out.append(line[i:])
                i = n
            else:
                out.append(" ")
                i = close + len(marker)
        else:
            out.append(line[i])
            i += 1
    return "".join(out)


def strip_code_spans(text):
    """펜스 블록과 인라인 코드를 지운 사본을 돌려준다(줄 수 보존)."""
    lines = text.split("\n")
    out = []
    fence = None
    for line in lines:
        match = FENCE_RE.match(line)
        if fence is None:
            if match:
                fence = match.group(1)
                out.append("")
                continue
            out.append(strip_inline_code(line))
        else:
            out.append("")
            if match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence):
                fence = None
    return "\n".join(out)


# --------------------------------------------------------------------------
# frontmatter · 절 파싱
# --------------------------------------------------------------------------
def _split_value_comment(value):
    """값 뒤의 ` # 주석` 을 떼어낸다. 값 안의 '#' 은 앞에 공백이 있어야 주석이다."""
    match = re.search(r"\s#(?:\s|$)", value)
    if match:
        return value[: match.start()].strip()
    return value.strip()


def parse_scalar(value):
    value = _split_value_comment(value)
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip("\"'") for item in inner.split(",")]
    return value


def extract_frontmatter(stripped_text):
    """코드 제거본에서 **첫 `---` 블록**을 frontmatter 로 읽는다.

    돌려주는 것: (data, order, start_line, end_line, preceded_by_content, parse_errors)
    data 가 None 이면 frontmatter 가 없다.
    """
    lines = stripped_text.split("\n")
    start = None
    for i, line in enumerate(lines):
        if line.strip() == "---":
            start = i
            break
    if start is None:
        return None, [], None, None, False, []
    end = None
    for j in range(start + 1, len(lines)):
        if lines[j].strip() in ("---", "..."):
            end = j
            break
    if end is None:
        return None, [], None, None, False, []
    preceded = any(lines[k].strip() for k in range(0, start))
    data = {}
    order = []
    errors = []
    for offset in range(start + 1, end):
        raw = lines[offset]
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if ":" not in raw:
            errors.append((offset + 1, "key: value 형식이 아니다: %r" % raw.strip()))
            continue
        key, _, value = raw.partition(":")
        key = key.strip()
        if not key:
            errors.append((offset + 1, "빈 키: %r" % raw.strip()))
            continue
        if key in data:
            errors.append((offset + 1, "키가 두 번 나온다: %s" % key))
            continue
        data[key] = parse_scalar(value)
        order.append(key)
    return data, order, start + 1, end + 1, preceded, errors


class Section(object):
    def __init__(self, token, raw_heading, line, body_lines):
        self.token = token
        self.raw_heading = raw_heading
        self.line = line
        self.body_lines = body_lines

    @property
    def body(self):
        return "\n".join(self.body_lines)

    def is_empty(self):
        return not any(line.strip() for line in self.body_lines)


def section_token(heading_text):
    """`Problem (문제)` → `Problem`. 영문 토큰만 남기고 한국어 병기는 버린다."""
    match = TRAILING_PAREN_RE.match(heading_text)
    if match:
        return match.group(1).strip()
    return heading_text.strip()


def parse_document(stripped_text, body_start_line):
    """제목(#)과 절(##) 을 읽는다. body_start_line 은 frontmatter 다음 줄(1-based)."""
    lines = stripped_text.split("\n")
    title = None
    title_line = None
    sections = []
    current = None
    for idx in range(body_start_line - 1, len(lines)):
        line = lines[idx]
        match = HEADING_RE.match(line)
        if match and len(match.group(1)) == 1:
            if title is None:
                title = match.group(2).strip()
                title_line = idx + 1
            current = None
            continue
        if match and len(match.group(1)) == 2:
            current = Section(section_token(match.group(2)), match.group(2).strip(), idx + 1, [])
            sections.append(current)
            continue
        if current is not None:
            current.body_lines.append(line)
    return title, title_line, sections


def list_ids(section, prefix):
    """절 안의 `- C1 …` 형태 항목에서 ID 를 순서대로 뽑는다."""
    ids = []
    for line in section.body_lines if section else []:
        match = LIST_ITEM_RE.match(line)
        if match and re.match(r"^%s\d+$" % prefix, match.group(1)):
            ids.append(match.group(1))
    return ids


def list_items(section, prefix):
    items = []
    for line in section.body_lines if section else []:
        match = LIST_ITEM_RE.match(line)
        if match and re.match(r"^%s\d+$" % prefix, match.group(1)):
            items.append((match.group(1), match.group(2)))
    return items


def find_section(sections, token):
    for section in sections:
        if section.token == token:
            return section
    return None


def normalize_prose(text):
    return " ".join(text.split()).lower()


# --------------------------------------------------------------------------
# git — 단일 통로
# --------------------------------------------------------------------------
def run_git(cwd, *args):
    try:
        proc = subprocess.run(
            ["git"] + list(args),
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        return 127, b"", str(exc)
    return proc.returncode, proc.stdout, proc.stderr.decode("utf-8", "replace")


class GitContext(object):
    """파일 하나가 속한 저장소. 없으면 root 가 None 이고 상류 검사는 판정 불가다."""

    _cache = {}

    def __init__(self, directory):
        self.directory = directory
        rc, out, _err = run_git(directory, "rev-parse", "--show-toplevel")
        self.root = out.decode("utf-8", "replace").strip() if rc == 0 else None

    @classmethod
    def for_dir(cls, directory):
        key = os.path.abspath(directory)
        if key not in cls._cache:
            cls._cache[key] = cls(key)
        return cls._cache[key]

    def show(self, rev, relpath):
        rc, out, err = run_git(self.root, "show", "%s:%s" % (rev, relpath))
        return rc, out, err

    def current_branch(self):
        """지금 브랜치 이름. detached HEAD 면 `INTENT_CHECK_BRANCH` 를 쓴다.

        CI 는 PR 을 detached HEAD 로 체크아웃한다 — 그러면 `symbolic-ref` 가 답을
        못 내고 브랜치 검사가 통째로 빠졌다(집행력 0). 그 자리를 **우리가 소유하는
        env 이름**으로 메운다. env 도 없으면 None 이고, 호출자가 note 로 남긴다.
        """
        rc, out, _err = run_git(self.root, "symbolic-ref", "--quiet", "--short", "HEAD")
        if rc == 0:
            name = out.decode("utf-8", "replace").strip()
            if name:
                return name
        return os.environ.get("INTENT_CHECK_BRANCH", "").strip() or None

    def resolve_default(self):
        """(기본 브랜치 이름, git 이 풀 수 있는 ref). 못 정하면 (None, None).

        이름과 ref 를 나눠 돌려준다 — 비교(`branch == default`)는 이름으로 하고
        조회(`git show`/`ls-tree`)는 ref 로 해야 한다. 얕지 않은 CI 클론에는
        `refs/heads/main` 이 없고 `refs/remotes/origin/main` 만 있다.
        """
        env = os.environ.get("INTENT_CHECK_DEFAULT_BRANCH", "").strip()
        names = [env] if env else ["main", "master"]
        for name in names:
            for ref in ("refs/heads/" + name, "refs/remotes/origin/" + name):
                rc, _out, _err = run_git(self.root, "rev-parse", "--verify", "--quiet", ref)
                if rc == 0:
                    return name, ref
        return None, None


# --------------------------------------------------------------------------
# 검사 본체
# --------------------------------------------------------------------------
class Report(object):
    def __init__(self, path, artifact_type):
        self.path = path
        self.type = artifact_type
        self.findings = []

    def add(self, code, message, line=None, severity=SEV_ERROR):
        self.findings.append(
            {"code": code, "severity": severity, "line": line, "message": message}
        )

    @property
    def rc(self):
        if any(f["severity"] == SEV_UNDECIDABLE for f in self.findings):
            return 2
        if any(f["severity"] == SEV_ERROR for f in self.findings):
            return 1
        return 0

    def as_dict(self):
        return {
            "path": self.path,
            "type": self.type,
            "rc": self.rc,
            "findings": self.findings,
        }


def has_placeholder(text):
    return any(char in text for char in PLACEHOLDER_CHARS)


def resolve_type(path, forced):
    if forced:
        return forced
    stem = os.path.basename(path)
    if stem.endswith(".md"):
        stem = stem[:-3]
    return STEM_TO_TYPE.get(stem)


def read_upstream_frontmatter(git_ctx, sha, relpath):
    """상류 파일을 실제로 열어 frontmatter 만 읽는다(코드 제거 후)."""
    rc, out, err = git_ctx.show(sha, relpath)
    if rc != 0:
        return None, err.strip() or "git show 실패"
    text = out.decode("utf-8", "replace")
    data, _order, _s, _e, _pre, _errs = extract_frontmatter(strip_code_spans(text))
    if data is None:
        return None, "상류 파일에 frontmatter 가 없다"
    return data, None


def check_frontmatter(report, artifact_type, path, data, order, parse_errors, preceded):
    schema = SCHEMA[artifact_type]
    if preceded:
        report.add(
            "FRONTMATTER_NOT_AT_TOP",
            "frontmatter 앞에 내용이 있다 — 파일 맨 위여야 한다",
            line=1,
        )
    for line, message in parse_errors:
        code = "FRONTMATTER_DUPLICATE_KEY" if "두 번" in message else "FRONTMATTER_UNPARSABLE"
        report.add(code, message, line=line)

    expected = schema["keys"]
    for key in expected:
        if key not in data:
            report.add("FRONTMATTER_MISSING_KEY", "필수 키가 없다: %s" % key, line=1)
    for key in order:
        if key not in expected:
            report.add(
                "FRONTMATTER_UNKNOWN_KEY",
                "스키마에 없는 키: %s (읽지 않는 필드는 두지 않는다 — 기대 키: %s)"
                % (key, ", ".join(expected)),
                line=1,
            )
    for key in order:
        value = data.get(key)
        if isinstance(value, str) and not value.strip():
            report.add("FRONTMATTER_EMPTY_VALUE", "값이 비었다: %s" % key, line=1)

    status = data.get("status")
    if isinstance(status, str) and status.strip():
        if status not in STATUS_VALUES:
            report.add(
                "STATUS_INVALID",
                "status 가 %r — 허용값은 %s" % (status, " | ".join(STATUS_VALUES)),
                line=1,
            )

    kind = data.get("kind")
    if isinstance(kind, str) and kind.strip() and kind != artifact_type:
        report.add(
            "KIND_MISMATCH",
            "kind 가 %r 인데 파일이 %s 다" % (kind, artifact_type),
            line=1,
        )

    artifact_id = data.get("id")
    if isinstance(artifact_id, str) and artifact_id.strip():
        if not ID_RE.match(artifact_id):
            report.add(
                "ID_MALFORMED",
                "id 가 %r — NNNN-slug 형식이어야 한다" % artifact_id,
                line=1,
            )
        dirname = os.path.basename(os.path.dirname(os.path.abspath(path)))
        if artifact_id != dirname:
            report.add(
                "ID_DIRNAME_MISMATCH",
                "id 가 %r 인데 디렉터리는 %r 이다" % (artifact_id, dirname),
                line=1,
            )

    if artifact_type == "intent":
        created = data.get("created")
        if isinstance(created, str) and created.strip() and not CREATED_RE.match(created):
            report.add(
                "CREATED_INVALID",
                "created 가 %r — 오프셋을 포함한 ISO8601(예 2026-09-09T10:12:00+09:00)이어야 한다"
                % created,
                line=1,
            )
        supersedes = data.get("supersedes")
        if isinstance(supersedes, str) and supersedes.strip():
            if supersedes != "none" and not ID_RE.match(supersedes):
                report.add(
                    "SUPERSEDES_INVALID",
                    "supersedes 가 %r — none 또는 NNNN-slug 여야 한다" % supersedes,
                    line=1,
                )

    if artifact_type == "spec":
        skills = data.get("skills_applied")
        if skills is not None and not isinstance(skills, list):
            report.add(
                "SKILLS_APPLIED_INVALID",
                "skills_applied 가 목록이 아니다: %r ([] 또는 [a, b])" % skills,
                line=1,
            )


def check_title(report, artifact_type, title, title_line, data):
    schema = SCHEMA[artifact_type]
    if title is None:
        report.add("TITLE_MISSING", "`# %s: …` 제목 줄이 없다" % schema["title"])
        return
    prefix = "%s:" % schema["title"]
    if not title.startswith(prefix) or not title[len(prefix) :].strip():
        report.add(
            "TITLE_MALFORMED",
            "제목이 %r — `# %s: <내용>` 이어야 한다" % (title, schema["title"]),
            line=title_line,
        )
        return
    if artifact_type in ("spec", "plan"):
        artifact_id = data.get("id") or ""
        number = artifact_id.split("-")[0] if isinstance(artifact_id, str) else ""
        if not re.search(r"\(from intent \S+\)", title):
            report.add(
                "TITLE_MISSING_SOURCE",
                "제목에 `(from intent NNNN)` 이 없다: %r" % title,
                line=title_line,
            )
        elif number and ("(from intent %s)" % number) not in title:
            report.add(
                "TITLE_MISSING_SOURCE",
                "제목의 출처 번호가 id 와 다르다: %r (id=%s)" % (title, artifact_id),
                line=title_line,
            )


def check_sections(report, artifact_type, sections):
    expected = SCHEMA[artifact_type]["sections"]
    seen = []
    for section in sections:
        if section.token in seen:
            report.add(
                "SECTION_DUPLICATE",
                "절이 두 번 나온다: %s" % section.token,
                line=section.line,
            )
        seen.append(section.token)
        if section.token not in expected:
            report.add(
                "SECTION_UNKNOWN",
                "스키마에 없는 절: %r (기대: %s)" % (section.raw_heading, ", ".join(expected)),
                line=section.line,
            )
        elif section.is_empty():
            report.add(
                "EMPTY_SECTION",
                "절이 비었다: %s — 해당 없으면 「해당 없음 — 이유」를 쓴다" % section.token,
                line=section.line,
            )
    for token in expected:
        if token not in seen:
            report.add("SECTION_MISSING", "절이 없다: %s" % token)
    ordered = [token for token in seen if token in expected]
    deduped = []
    for token in ordered:
        if token not in deduped:
            deduped.append(token)
    filtered_expected = [token for token in expected if token in deduped]
    if deduped != filtered_expected:
        report.add(
            "SECTION_ORDER",
            "절 순서가 스키마와 다르다: %s (기대 %s)"
            % (" → ".join(deduped), " → ".join(filtered_expected)),
        )


def check_placeholders(report, stripped_text):
    lines = stripped_text.split("\n")
    hits = [i + 1 for i, line in enumerate(lines) if has_placeholder(line)]
    if hits:
        shown = ", ".join(str(n) for n in hits[:5])
        more = "" if len(hits) <= 5 else " 외 %d줄" % (len(hits) - 5)
        report.add(
            "PLACEHOLDER_LEFT",
            "자리표시자 ‹…› 가 %d줄에 남아 있다 (줄 %s%s)" % (len(hits), shown, more),
            line=hits[0],
        )


def check_upstream(report, artifact_type, path, data):
    """upstream: <파일>@<sha> — git 을 단일 통로로 실제로 연다."""
    schema = SCHEMA[artifact_type]
    expected_file = schema.get("upstream_file")
    if not expected_file:
        return None
    raw = data.get("upstream")
    if not isinstance(raw, str) or not raw.strip():
        return None
    if has_placeholder(raw):
        report.add(
            "UPSTREAM_CHECK_SKIPPED_PLACEHOLDER",
            "upstream 이 아직 자리표시자다 — 상류 해석은 돌리지 않았다(확인 못 함)",
            line=1,
            severity=SEV_NOTE,
        )
        return None
    match = UPSTREAM_RE.match(raw.strip())
    if not match:
        report.add(
            "UPSTREAM_MALFORMED",
            "upstream 이 %r — `<파일>@<sha>` 형식이어야 한다" % raw,
            line=1,
        )
        return None
    if match.group("file") != expected_file:
        report.add(
            "UPSTREAM_WRONG_FILE",
            "upstream 파일이 %r 인데 %s 는 %s 를 상류로 가진다"
            % (match.group("file"), artifact_type, expected_file),
            line=1,
        )
        return None
    directory = os.path.dirname(os.path.abspath(path))
    git_ctx = GitContext.for_dir(directory)
    if not git_ctx.root:
        report.add(
            "NOT_A_GIT_REPO",
            "git 저장소가 아니라 상류를 열 수 없다: %s" % directory,
            line=1,
            severity=SEV_UNDECIDABLE,
        )
        return None
    relpath = os.path.relpath(os.path.join(directory, expected_file), git_ctx.root)
    relpath = relpath.replace(os.sep, "/")
    upstream_data, error = read_upstream_frontmatter(git_ctx, match.group("sha"), relpath)
    if upstream_data is None:
        report.add(
            "UPSTREAM_UNRESOLVABLE",
            "git show %s:%s 를 열 수 없다 — %s" % (match.group("sha"), relpath, error),
            line=1,
            severity=SEV_UNDECIDABLE,
        )
        return None
    if upstream_data.get("status") != "accepted":
        report.add(
            "UPSTREAM_NOT_ACCEPTED",
            "상류 %s@%s 의 status 가 %r — accepted 여야 한다"
            % (expected_file, match.group("sha")[:12], upstream_data.get("status")),
            line=1,
        )
    if upstream_data.get("id") != data.get("id"):
        report.add(
            "UPSTREAM_ID_MISMATCH",
            "상류 %s@%s 의 id 가 %r 인데 이 파일은 %r 이다"
            % (
                expected_file,
                match.group("sha")[:12],
                upstream_data.get("id"),
                data.get("id"),
            ),
            line=1,
        )
    return upstream_data


# --------------------------------------------------------------------------
# D16 — 승인 전이. 이 판정의 어휘는 git 이 아니라 우리가 소유한다.
#
# 옛 축은 `git diff` 출력의 **텍스트 모양**을 읽었다. 그 어휘(무엇을 binary 로 볼지 ·
# `.gitattributes` 의 diff 드라이버 · `+++`/`---` 접두 · rename 탐지)의 소유자는 git 이라,
# git 이 형식을 바꾸거나 사용자가 속성을 거는 순간 축이 죽었다 — 실제로 8종이 뚫렸다.
# 지금 축은 **두 blob 의 바이트**를 직접 견준다: frontmatter 키 집합과 상태 enum 은
# 이미 이 레포가 SCHEMA 로 소유하는 닫힌 어휘다.
# --------------------------------------------------------------------------

# 어떤 상태 변화가 「도장」으로 허용되는가. **한 곳에 데이터로** 두고, 표에 없는 전이는
# 전부 거부한다 — 승인 게이트의 안전한 기본값은 deny-by-default 이고, 되돌리려면
# 이 표에 한 줄을 더하면 된다.
#
# 부모 세션 잠정 결정 · product owner 확인 대기(spec 의 F2). `rejected` → `accepted`
# 와 `superseded` → `accepted` 는 「되살리기」라 거부한다 — 되살리려면 새 아티팩트를
# 만들고 `supersedes:` 로 옛 것을 가리킨다.
ACCEPT_TRANSITIONS = (
    ("draft", "accepted"),
    ("draft", "rejected"),
    ("draft", "superseded"),
    ("accepted", "superseded"),
)

# 「도장 한 줄」의 형태. 값 뒤에 주석·인용부호가 붙으면 도장이 아니다 — 승인 커밋에
# 함께 들어온 산문은 아무도 검토하지 않았다. 끝의 공백·CR 만 눈감아 준다.
STAMP_LINE_RE = re.compile(rb"^status:[ \t]*([A-Za-z][A-Za-z0-9_-]*)[ \t\r]*$")


def split_frontmatter_bytes(raw):
    """바이트 원문 → (frontmatter 줄 목록, 그 뒤 본문 바이트). 못 가르면 (None, None).

    `strip_code_spans` 를 타지 않는다 — 여기서 묻는 것은 「무엇을 뜻하는가」가 아니라
    「무엇이 바뀌었는가」이고, 그 답은 바이트로만 낸다. 문서가 `---` 로 **시작**해야
    한다(그렇지 않은 문서는 frontmatter 검사가 이미 결함으로 잡는다).
    """
    lines = raw.split(b"\n")
    if not lines or lines[0].strip() != b"---":
        return None, None
    for j in range(1, len(lines)):
        if lines[j].strip() in (b"---", b"..."):
            return lines[1:j], b"\n".join(lines[j + 1 :])
    return None, None


def frontmatter_entries(fm_lines):
    """frontmatter 줄을 (키, 줄 원문) 으로. 키를 못 읽는 줄(빈 줄·주석)은 키가 None."""
    entries = []
    for line in fm_lines:
        stripped = line.strip()
        if not stripped or stripped.startswith(b"#") or b":" not in line:
            entries.append((None, line))
            continue
        entries.append((line.split(b":", 1)[0].strip(), line))
    return entries


def classify_accept_transition(base_raw, current_raw):
    """두 판(바이트)을 견줘 (판정, 이전 status, 지금 status).

    판정
      identical  두 바이트열이 실제로 같다.
      stamp      frontmatter 의 `status` 값 하나만 바뀌었고 나머지는 전부 바이트가 같다.
      content    그 밖 전부(본문 한 바이트 · 다른 키 · 키 순서 · 형식이 이상한 status 줄).

    「identical」은 두 바이트열이 같을 때만이다 — git 이 diff 를 못 냈다는 것은
    「안 바뀌었다」가 아니다.
    """
    if base_raw == current_raw:
        return "identical", None, None
    base_fm, base_body = split_frontmatter_bytes(base_raw)
    cur_fm, cur_body = split_frontmatter_bytes(current_raw)
    if base_fm is None or cur_fm is None:
        return "content", None, None
    if base_body != cur_body:
        return "content", None, None
    base_entries = frontmatter_entries(base_fm)
    cur_entries = frontmatter_entries(cur_fm)
    if len(base_entries) != len(cur_entries):
        return "content", None, None
    before = after = None
    for (base_key, base_line), (cur_key, cur_line) in zip(base_entries, cur_entries):
        if base_key != cur_key:
            return "content", None, None
        if base_key == b"status":
            if before is not None:  # status 가 두 번 — 도장이 아니다
                return "content", None, None
            base_match = STAMP_LINE_RE.match(base_line)
            cur_match = STAMP_LINE_RE.match(cur_line)
            if not base_match or not cur_match:
                return "content", None, None
            before = base_match.group(1).decode("ascii")
            after = cur_match.group(1).decode("ascii")
            continue
        if base_line != cur_line:
            return "content", None, None
    if before is None or before == after:
        # status 값은 그대로인데 바이트가 다르다(파일 끝 개행 따위) — 도장이 아니다.
        return "content", None, None
    return "stamp", before, after


def tree_files(git_ctx, rev, scope):
    """그 판의 트리에 있는 파일 경로 전량(scope 아래로만). 실패하면 (None, 사유)."""
    args = ["ls-tree", "-r", "--name-only", "-z", rev]
    if scope:
        args += ["--", scope]
    rc, out, err = run_git(git_ctx.root, *args)
    if rc != 0:
        return None, (err.strip() or "rc=%d" % rc)
    return [name for name in out.decode("utf-8", "replace").split("\0") if name], None


def artifacts_in_tree(git_ctx, rev, scope, artifact_type):
    """그 판의 트리에서 같은 형인 아티팩트를 (경로, frontmatter) 로 훑는다."""
    names, error = tree_files(git_ctx, rev, scope)
    if names is None:
        return None, error
    found = []
    for name in names:
        if resolve_type(name, None) != artifact_type:
            continue
        data, _error = read_upstream_frontmatter(git_ctx, rev, name)
        if data is not None:
            found.append((name, data))
    return found, None


def vanished_accepted_ids(git_ctx, default_rev, scope, artifact_type):
    """기본 브랜치에서 `accepted` 였는데 이 브랜치 트리에서 **사슬 id 째로 사라진** 것들.

    승인된 아티팩트를 지우고 새 id 로 갈아타 그 자리에서 자기 승인하면, 파일 하나만
    보는 검사는 「이 브랜치에서 태어난 새 사슬」로 읽어 통과시킨다(⑥c). 경로는 git 이
    움직일 수 있지만 사슬 id 는 우리 어휘라, 그 사라짐은 셀 수 있다.
    """
    base_found, error = artifacts_in_tree(git_ctx, default_rev, scope, artifact_type)
    if base_found is None:
        return None, error
    head_found, error = artifacts_in_tree(git_ctx, "HEAD", scope, artifact_type)
    if head_found is None:
        return None, error
    head_ids = set(data.get("id") for _name, data in head_found)
    gone = []
    for name, data in base_found:
        if data.get("status") != "accepted":
            continue
        if data.get("id") not in head_ids:
            gone.append((data.get("id"), name))
    return gone, None


def accept_baseline(git_ctx, default_rev, relpath, artifact_type, chain_id):
    """무엇과 견줄 것인가 — (rev, path, outcome, detail). outcome: ok | skip | reject.

    ① 기본 브랜치에 **같은 사슬 id 의 같은 형** 아티팩트가 있으면 그것이 기준점이다.
       경로가 아니라 id 로 찾는다 — 경로로 찾으면 디렉터리·파일 개명 한 번에 기준점이
       브랜치 자기 커밋으로 후퇴해, 브랜치가 심은 draft 위에 도장을 찍을 수 있다.
    ② 없으면 사슬이 이 브랜치에서 태어난 경우다. 이 브랜치의 커밋 중 그 파일이 **아직
       accepted 가 아니었던 가장 최근 판**을 기준으로 삼는다 — 그것이 도장을 찍을
       원본이다. 「그 파일을 건드린 가장 최근 커밋」으로 잡으면 승인을 커밋하기 직전의
       작업 트리가 red 로 읽혀 승인 커밋을 만들 수조차 없다.
    ③ 커밋된 적이 없거나 모든 판이 이미 accepted 면 도장을 찍을 원본이 없다 — reject.
    """
    scope = relpath.split("/")[0] if "/" in relpath else None
    if chain_id:
        found, error = artifacts_in_tree(git_ctx, default_rev, scope, artifact_type)
        if found is None:
            return None, None, "skip", "git ls-tree 가 실패했다: %s" % error
        hits = [name for name, data in found if data.get("id") == chain_id]
        if len(hits) > 1:
            return (
                None,
                None,
                "reject",
                "기본 브랜치에 사슬 id %r 인 %s 가 여럿이다(%s) — 기준점을 하나로 정할 수 없다"
                % (chain_id, artifact_type, ", ".join(sorted(hits))),
            )
        if hits:
            return default_rev, hits[0], "ok", "기본 브랜치의 %s" % hits[0]
    rc, _out, _err = git_ctx.show(default_rev, relpath)
    if rc == 0:
        return default_rev, relpath, "ok", "기본 브랜치의 %s" % relpath
    rc, out, err = run_git(git_ctx.root, "rev-list", "%s..HEAD" % default_rev, "--", relpath)
    if rc != 0:
        return None, None, "skip", "git rev-list 가 실패했다: %s" % (err.strip() or "rc=%d" % rc)
    shas = out.decode("utf-8", "replace").split()
    if not shas:
        return (
            None,
            None,
            "reject",
            "기본 브랜치에 그 사슬의 %s 가 없고 이 브랜치에서 커밋된 적도 없다 "
            "— 도장을 찍을 원본이 없다" % artifact_type,
        )
    for sha in shas:  # rev-list 는 최신 → 과거 순이다
        data, _error = read_upstream_frontmatter(git_ctx, sha, relpath)
        # 읽을 수 없는 판(그 커밋에서 삭제됐거나 frontmatter 가 없다)은 accepted 가
        # 아니다 — 기준으로 잡으면 blob 이 안 열려 red 가 된다(안전한 쪽).
        if data is None or data.get("status") != "accepted":
            return sha, relpath, "ok", "승인 전 판 %s" % sha[:12]
    return (
        None,
        None,
        "reject",
        "이 브랜치의 모든 판이 이미 accepted 다 — 도장을 찍을 draft 판이 없다",
    )


def check_accepted_on_branch(report, path, data):
    """accepted 는 머지된 PR 로만 들어온다 — 브랜치 위 자기 승인을 막는다.

    D16 예외: 브랜치에서도 **frontmatter 의 `status` 값 하나만 바뀐** 승인은 통과시킨다.
    이 예외가 없으면 승인 PR 자체가 CI 에서 빨개져 사슬이 전진할 수 없다(설계안 §4 는
    승인을 「PR 안에서 status: 를 고치고 머지」로 정의한다). 예외의 폭은 그 한 값이고,
    본문이 한 바이트라도 다르거나 다른 키가 함께 바뀌면 여전히 ACCEPTED_ON_BRANCH 다.
    전이 자체도 ACCEPT_TRANSITIONS 안에 있어야 한다.
    """
    if data.get("status") != "accepted":
        return
    directory = os.path.dirname(os.path.abspath(path))
    git_ctx = GitContext.for_dir(directory)
    if not git_ctx.root:
        report.add(
            "ACCEPTED_BRANCH_CHECK_SKIPPED",
            "git 저장소가 아니라 브랜치 자기 승인 검사를 돌리지 않았다(확인 못 함)",
            severity=SEV_NOTE,
        )
        return
    default_name, default_rev = git_ctx.resolve_default()
    branch = git_ctx.current_branch()
    if default_name is None or branch is None:
        report.add(
            "ACCEPTED_BRANCH_CHECK_SKIPPED",
            "기본 브랜치(%r) 또는 현재 브랜치(%r)를 못 정해 브랜치 자기 승인 검사를 "
            "돌리지 않았다(확인 못 함 — CI 의 detached HEAD 가 대표 사례다. "
            "INTENT_CHECK_BRANCH · INTENT_CHECK_DEFAULT_BRANCH 로 알려줄 수 있다)"
            % (default_name, branch),
            severity=SEV_NOTE,
        )
        return
    if branch == default_name:
        return
    relpath = os.path.relpath(os.path.abspath(path), git_ctx.root).replace(os.sep, "/")
    artifact_type = report.type
    chain_id = data.get("id")
    if not isinstance(chain_id, str) or not chain_id:
        chain_id = None
    scope = relpath.split("/")[0] if "/" in relpath else None

    # 기준점을 지우고 새 id 로 갈아타는 우회를 먼저 본다.
    gone, error = vanished_accepted_ids(git_ctx, default_rev, scope, artifact_type)
    if gone is None:
        report.add(
            "ACCEPTED_BRANCH_CHECK_SKIPPED",
            "브랜치 %r 의 승인 전이를 판정하지 못했다(확인 못 함) — %s" % (branch, error),
            severity=SEV_NOTE,
        )
        return
    if gone:
        report.add(
            "ACCEPTED_ARTIFACT_VANISHED",
            "브랜치 %r 에서 status: accepted 인데, 기본 브랜치 %s 의 accepted %s 가 "
            "이 브랜치에서 사슬 id 째로 사라졌다(%s) — 승인 기록을 지우고 새 id 로 "
            "갈아타는 것은 승인이 아니다. 대체하려면 옛 것을 superseded 로 남긴다"
            % (
                branch,
                default_name,
                artifact_type,
                ", ".join("%s(%s)" % (cid, name) for cid, name in sorted(gone)),
            ),
            line=1,
        )
        return

    baseline_rev, baseline_path, outcome, detail = accept_baseline(
        git_ctx, default_rev, relpath, artifact_type, chain_id
    )
    if outcome == "skip":
        report.add(
            "ACCEPTED_BRANCH_CHECK_SKIPPED",
            "브랜치 %r 의 승인 전이를 판정하지 못했다(확인 못 함) — %s" % (branch, detail),
            severity=SEV_NOTE,
        )
        return
    if outcome == "reject":
        report.add(
            "ACCEPTED_ON_BRANCH",
            "브랜치 %r 에서 status: accepted 인데 %s — 승인은 이미 검토된 문서에 "
            "도장을 찍는 행위다" % (branch, detail),
            line=1,
        )
        return

    # 기준점 blob 과 지금 파일을 **바이트로** 꺼낸다. 실패를 삼키지 않는다.
    rc, base_raw, error = git_ctx.show(baseline_rev, baseline_path)
    if rc != 0:
        report.add(
            "ACCEPTED_ON_BRANCH",
            "브랜치 %r 에서 status: accepted 인데 기준점(%s)을 열지 못했다 — %s"
            % (branch, detail, error.strip() or "rc=%d" % rc),
            line=1,
        )
        return
    try:
        with open(path, "rb") as handle:
            current_raw = handle.read()
    except OSError as exc:
        report.add(
            "ACCEPTED_BRANCH_CHECK_SKIPPED",
            "브랜치 %r 의 승인 전이를 판정하지 못했다(확인 못 함) — 파일을 바이트로 "
            "읽지 못했다: %s" % (branch, exc),
            severity=SEV_NOTE,
        )
        return

    verdict, before, after = classify_accept_transition(base_raw, current_raw)
    if verdict == "identical":
        return
    if verdict == "content":
        report.add(
            "ACCEPTED_ON_BRANCH",
            "브랜치 %r 에서 status: accepted 인데 %s 와 견줘 frontmatter 의 `status` "
            "값 말고도 바뀐 곳이 있다 — 승인은 이미 검토된 문서에 도장을 찍는 행위이지 "
            "고치면서 승인하는 일이 아니다. 내용을 바꾸려면 draft 로 되돌려 다시 "
            "검토받는다" % (branch, detail),
            line=1,
        )
        return
    if (before, after) not in ACCEPT_TRANSITIONS:
        report.add(
            "ACCEPT_TRANSITION_NOT_ALLOWED",
            "브랜치 %r 에서 status 가 %r → %r 인데 허용 전이가 아니다(%s 기준) — "
            "허용: %s. 되살리려면 새 아티팩트를 만들고 supersedes: 로 옛 것을 가리킨다"
            % (
                branch,
                before,
                after,
                detail,
                " · ".join("%s→%s" % pair for pair in ACCEPT_TRANSITIONS),
            ),
            line=1,
        )


def load_sibling(path, filename):
    sibling = os.path.join(os.path.dirname(os.path.abspath(path)), filename)
    if not os.path.exists(sibling):
        return None, None
    with open(sibling, encoding="utf-8", errors="replace") as handle:
        text = handle.read()
    stripped = strip_code_spans(text)
    data, _order, _s, end, _pre, _errs = extract_frontmatter(stripped)
    body_start = (end + 1) if end else 1
    _title, _tline, sections = parse_document(stripped, body_start)
    return data, sections


def check_spec_inheritance(report, path, sections):
    intent_data, intent_sections = load_sibling(path, "intent.md")
    if intent_sections is None:
        report.add(
            "SIBLING_INTENT_MISSING",
            "같은 디렉터리에 intent.md 가 없어 이어받기를 판정할 수 없다",
            severity=SEV_UNDECIDABLE,
        )
        return
    constraints = find_section(intent_sections, "Constraints")
    questions = find_section(intent_sections, "Open questions")
    inherited = find_section(sections, "Constraints inherited")
    carried = find_section(sections, "Open questions from intent")

    inherited_body = inherited.body if inherited else ""
    for cid in list_ids(constraints, "C"):
        if not re.search(r"\b%s\b" % cid, inherited_body):
            report.add(
                "CONSTRAINT_NOT_INHERITED",
                "intent 의 %s 가 「Constraints inherited」에 없다" % cid,
                line=inherited.line if inherited else None,
            )

    carried_lines = carried.body_lines if carried else []
    for qid in list_ids(questions, "Q"):
        hits = [line for line in carried_lines if re.search(r"\b%s\b" % qid, line)]
        if not hits:
            report.add(
                "QUESTION_NOT_CARRIED",
                "intent 의 %s 가 「Open questions from intent」에 없다 — 답했거나 "
                "넘겼거나 둘 중 하나여야 한다" % qid,
                line=carried.line if carried else None,
            )
            continue
        if not any(("answered:" in line or "carried:" in line) for line in hits):
            report.add(
                "QUESTION_NOT_RESOLVED",
                "%s 가 적혀 있지만 `answered:` 도 `carried:` 도 없다" % qid,
                line=carried.line if carried else None,
            )

    # spec 이 intent 를 옮겨 적었는가 — 절 단위 축자 복사.
    for section in sections:
        if section.token in COPY_EXEMPT_SPEC_SECTIONS:
            continue
        normalized = normalize_prose(section.body)
        if len(normalized) < COPY_MIN_CHARS:
            continue
        for intent_section in intent_sections:
            if normalize_prose(intent_section.body) == normalized:
                report.add(
                    "SPEC_COPIES_INTENT",
                    "spec 의 「%s」 절이 intent 의 「%s」 절과 글자 그대로 같다 — "
                    "spec 은 intent 를 옮겨 적는 자리가 아니다"
                    % (section.token, intent_section.token),
                    line=section.line,
                )
                break


def check_spec_acceptance(report, sections):
    requirements = find_section(sections, "Requirements")
    acceptance = find_section(sections, "Acceptance criteria")
    r_ids = list_ids(requirements, "R")
    covered = set()
    for ac_id, rest in list_items(acceptance, "AC"):
        refs = re.findall(r"\bR\d+\b", rest)
        if not refs:
            report.add(
                "AC_NO_REQUIREMENT",
                "%s 가 어떤 R# 도 가리키지 않는다 (`- AC1 → R1 …`)" % ac_id,
                line=acceptance.line if acceptance else None,
            )
            continue
        for ref in refs:
            if ref not in r_ids:
                report.add(
                    "AC_UNKNOWN_REQUIREMENT",
                    "%s 가 없는 요구 %s 를 가리킨다" % (ac_id, ref),
                    line=acceptance.line if acceptance else None,
                )
            else:
                covered.add(ref)
    for r_id in r_ids:
        if r_id not in covered:
            report.add(
                "REQUIREMENT_UNCOVERED",
                "요구 %s 를 덮는 AC# 가 없다" % r_id,
                line=requirements.line if requirements else None,
            )


def check_plan_proof(report, path, sections):
    spec_data, spec_sections = load_sibling(path, "spec.md")
    if spec_sections is None:
        report.add(
            "SIBLING_SPEC_MISSING",
            "같은 디렉터리에 spec.md 가 없어 Proof 가 무엇을 덮는지 판정할 수 없다",
            severity=SEV_UNDECIDABLE,
        )
        return
    acceptance = find_section(spec_sections, "Acceptance criteria")
    ac_ids = list_ids(acceptance, "AC")
    proof = find_section(sections, "Proof")
    refs = re.findall(r"\bAC\d+\b", proof.body) if proof else []
    if not refs:
        report.add(
            "PROOF_COVERS_NO_AC",
            "plan 의 Proof 가 AC# 를 하나도 가리키지 않는다 — 「전체 시험을 돌린다」는 "
            "증명이 아니다",
            line=proof.line if proof else None,
        )
        return
    for ref in refs:
        if ref not in ac_ids:
            report.add(
                "PROOF_UNKNOWN_AC",
                "Proof 가 spec 에 없는 %s 를 가리킨다" % ref,
                line=proof.line if proof else None,
            )


def check_file(path, forced_type=None):
    artifact_type = resolve_type(path, forced_type)
    report = Report(path, artifact_type)
    if not os.path.exists(path):
        report.add("FILE_MISSING", "파일이 없다", severity=SEV_UNDECIDABLE)
        return report
    if artifact_type not in SCHEMA:
        report.add(
            "TYPE_UNKNOWN",
            "파일명에서 형(intent|spec|plan)을 정할 수 없다 — --type 으로 지정하라",
            severity=SEV_UNDECIDABLE,
        )
        return report
    try:
        with open(path, encoding="utf-8", errors="strict") as handle:
            text = handle.read()
    except (OSError, UnicodeDecodeError) as exc:
        report.add("FILE_UNREADABLE", "파일을 읽을 수 없다: %s" % exc, severity=SEV_UNDECIDABLE)
        return report

    stripped = strip_code_spans(text)
    check_placeholders(report, stripped)

    data, order, _start, end, preceded, parse_errors = extract_frontmatter(stripped)
    if data is None:
        report.add("FRONTMATTER_MISSING", "`---` 로 감싼 frontmatter 가 없다", line=1)
        return report

    check_frontmatter(report, artifact_type, path, data, order, parse_errors, preceded)
    title, title_line, sections = parse_document(stripped, (end + 1) if end else 1)
    check_title(report, artifact_type, title, title_line, data)
    check_sections(report, artifact_type, sections)
    check_upstream(report, artifact_type, path, data)
    check_accepted_on_branch(report, path, data)
    if artifact_type == "spec":
        check_spec_inheritance(report, path, sections)
        check_spec_acceptance(report, sections)
    if artifact_type == "plan":
        check_plan_proof(report, path, sections)
    return report


# --------------------------------------------------------------------------
# 출력
# --------------------------------------------------------------------------
def render_text(reports, stream):
    errors = undecidable = notes = 0
    for report in reports:
        for finding in report.findings:
            if finding["severity"] == SEV_ERROR:
                errors += 1
            elif finding["severity"] == SEV_UNDECIDABLE:
                undecidable += 1
            else:
                notes += 1
    for report in reports:
        label = {0: "OK  ", 1: "FAIL", 2: "????"}[report.rc]
        stream.write("%s %s (%s)\n" % (label, report.path, report.type or "형 미정"))
        for finding in report.findings:
            stream.write(
                "     %-12s %-30s %s%s\n"
                % (
                    finding["severity"],
                    finding["code"],
                    ("line %s: " % finding["line"]) if finding["line"] else "",
                    finding["message"],
                )
            )
    stream.write(
        "\n%d file(s) checked — %d error, %d undecidable, %d note\n"
        % (len(reports), errors, undecidable, notes)
    )


def render_json(reports, stream):
    errors = sum(1 for r in reports for f in r.findings if f["severity"] == SEV_ERROR)
    undecidable = sum(
        1 for r in reports for f in r.findings if f["severity"] == SEV_UNDECIDABLE
    )
    notes = sum(1 for r in reports for f in r.findings if f["severity"] == SEV_NOTE)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "tool": "check_artifacts.py",
        "rc": max([r.rc for r in reports] + [0]) if reports else 0,
        "summary": {"errors": errors, "undecidable": undecidable, "notes": notes},
        "files": [r.as_dict() for r in reports],
    }
    if undecidable:
        payload["rc"] = 2
    elif errors:
        payload["rc"] = 1
    else:
        payload["rc"] = 0
    json.dump(payload, stream, ensure_ascii=False, indent=2)
    stream.write("\n")


EPILOG = """\
재지 않는 것 (안 보는 것을 보는 척하지 않는다)
  · 제목이 해법인지 변경 대상인지
  · 산문의 품질 — 문장이 좋은지, 설명이 충분한지
  · 요구가 문제를 실제로 푸는지
  이 셋은 사람과 리뷰의 몫이다. 그린은 「규약을 지켰다」일 뿐 「좋다」가 아니다.

rc: 0 통과 · 1 결함 · 2 판정 불가(rc 2 는 통과가 아니다).
--format json 의 소비자는 메시지가 아니라 code 로 분기하라.
"""


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="check_artifacts.py",
        description="intent / spec / plan 아티팩트가 사슬 규약을 지키는지 검사한다.",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("paths", nargs="+", help="검사할 .md 파일")
    parser.add_argument(
        "--type",
        choices=sorted(SCHEMA),
        help="형을 강제한다(기본은 파일명에서 유도)",
    )
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)

    reports = [check_file(path, args.type) for path in args.paths]
    if args.format == "json":
        render_json(reports, sys.stdout)
    else:
        render_text(reports, sys.stdout)
    codes = [r.rc for r in reports]
    if 2 in codes:
        return 2
    if 1 in codes:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
