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
        rc, out, _err = run_git(self.root, "symbolic-ref", "--quiet", "--short", "HEAD")
        if rc != 0:
            return None
        return out.decode("utf-8", "replace").strip()

    def default_branch(self):
        for name in ("main", "master"):
            rc, _out, _err = run_git(self.root, "rev-parse", "--verify", "--quiet", "refs/heads/" + name)
            if rc == 0:
                return name
        return None


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


STATUS_LINE_RE = re.compile(r"^status:[ \t]*\S+[ \t]*$")


def classify_accept_diff(diff_text):
    """`git diff` 출력이 무엇을 바꿨는가 — identical | status_only | content.

    D16 의 판정 함수다. 승인은 「이미 검토된 문서에 도장을 찍는 행위」이므로,
    바뀐 줄이 `status:` 하나뿐이면 도장이고 그 밖의 줄이 함께 바뀌었으면
    「고치면서 승인」이다. 파일이 통째로 새로 생긴 경우(+ 줄만 여럿)도 content 다
    — 도장을 찍을 원본이 없기 때문이다.
    """
    added = []
    removed = []
    for line in diff_text.split("\n"):
        if not line or line[0] not in "+-":
            continue
        if line.startswith("+++") or line.startswith("---"):
            continue
        (added if line[0] == "+" else removed).append(line[1:])
    if not added and not removed:
        return "identical"
    if len(added) == 1 and len(removed) == 1:
        if STATUS_LINE_RE.match(added[0]) and STATUS_LINE_RE.match(removed[0]):
            return "status_only"
    return "content"


def run_accept_diff(git_ctx, base, relpath):
    """base 와 작업 트리 사이의 그 파일 diff. 실패하면 (None, 사유) 를 돌려준다.

    실패를 삼키지 않는다 — 삼키면 CI 에서 이 자리가 조용히 빈다(호출자가 note 로
    남긴다). `--no-renames` 는 rename 탐지가 +/- 없는 diff 를 만들어 「안 바뀌었다」로
    읽히는 것을 막는다.
    """
    rc, out, err = run_git(
        git_ctx.root, "diff", "--no-color", "--no-renames", "-U0", base, "--", relpath
    )
    if rc != 0:
        return None, (err.strip() or "rc=%d" % rc)
    return out.decode("utf-8", "replace"), None


def accept_baseline(git_ctx, default, relpath):
    """무엇과 견줄 것인가 — (base, outcome, detail). outcome: ok | skip | reject.

    ① 기본 브랜치에 그 파일이 있으면 기본 브랜치가 기준이다(누적 diff).
    ② 없으면 사슬이 이 브랜치에서 태어난 경우다. 이 브랜치의 커밋 중 그 파일이 **아직
       accepted 가 아니었던 가장 최근 판**을 기준으로 삼는다 — 그것이 도장을 찍을
       원본이다. 「그 파일을 건드린 가장 최근 커밋」으로 잡으면 승인을 커밋하기 직전의
       작업 트리가 red 로 읽혀 승인 커밋을 만들 수조차 없다.
    ③ 커밋된 적이 없거나 모든 판이 이미 accepted 면 도장을 찍을 원본이 없다 — reject.
    """
    rc, _out, _err = git_ctx.show(default, relpath)
    if rc == 0:
        return default, "ok", "기본 브랜치 %s" % default
    rc, out, err = run_git(git_ctx.root, "rev-list", "%s..HEAD" % default, "--", relpath)
    if rc != 0:
        return None, "skip", "git rev-list 가 실패했다: %s" % (err.strip() or "rc=%d" % rc)
    shas = out.decode("utf-8", "replace").split()
    if not shas:
        return (
            None,
            "reject",
            "기본 브랜치 %s 에 그 파일이 없고 이 브랜치에서 커밋된 적도 없다 "
            "— 도장을 찍을 원본이 없다" % default,
        )
    for sha in shas:  # rev-list 는 최신 → 과거 순이다
        data, _error = read_upstream_frontmatter(git_ctx, sha, relpath)
        # 읽을 수 없는 판(그 커밋에서 삭제됐거나 frontmatter 가 없다)은 accepted 가
        # 아니다 — 기준으로 잡으면 diff 가 통째로 남아 red 가 된다(안전한 쪽).
        if data is None or data.get("status") != "accepted":
            return sha, "ok", "승인 전 판 %s" % sha[:12]
    return (
        None,
        "reject",
        "이 브랜치의 모든 판이 이미 accepted 다 — 도장을 찍을 draft 판이 없다",
    )


def check_accepted_on_branch(report, path, data):
    """accepted 는 머지된 PR 로만 들어온다 — 브랜치 위 자기 승인을 막는다.

    D16 예외: 브랜치에서도 `status:` 줄 하나만 바꾼 승인은 통과시킨다. 이 예외가
    없으면 승인 PR 자체가 CI 에서 빨개져 사슬이 전진할 수 없다(설계안 §4 는 승인을
    「PR 안에서 status: 를 고치고 머지」로 정의한다). 예외의 폭은 `status:` 줄
    하나이고, 그 밖의 내용이 함께 바뀌면 여전히 ACCEPTED_ON_BRANCH 다.
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
    default = git_ctx.default_branch()
    branch = git_ctx.current_branch()
    if default is None or branch is None:
        report.add(
            "ACCEPTED_BRANCH_CHECK_SKIPPED",
            "기본 브랜치(%r) 또는 현재 브랜치(%r)를 못 정해 브랜치 자기 승인 검사를 "
            "돌리지 않았다(확인 못 함 — CI 의 detached HEAD 가 대표 사례다)"
            % (default, branch),
            severity=SEV_NOTE,
        )
        return
    if branch == default:
        return
    relpath = os.path.relpath(os.path.abspath(path), git_ctx.root).replace(os.sep, "/")

    # D16 — 「도장만 찍는 승인」은 브랜치에서도 통과시킨다. 무엇과 견줄지부터 정한다.
    baseline, outcome, detail = accept_baseline(git_ctx, default, relpath)
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
    diff_text, error = run_accept_diff(git_ctx, baseline, relpath)
    if diff_text is None:
        report.add(
            "ACCEPTED_BRANCH_CHECK_SKIPPED",
            "브랜치 %r 의 승인 전이를 판정하지 못했다(확인 못 함) — git diff %s 가 "
            "실패했다: %s" % (branch, baseline, error),
            severity=SEV_NOTE,
        )
        return
    if classify_accept_diff(diff_text) == "content":
        report.add(
            "ACCEPTED_ON_BRANCH",
            "브랜치 %r 에서 status: accepted 인데 %s 와 견줘 `status:` 줄 말고도 바뀐 "
            "곳이 있다 — 승인은 이미 검토된 문서에 도장을 찍는 행위이지 고치면서 "
            "승인하는 일이 아니다. 내용을 바꾸려면 draft 로 되돌려 다시 검토받는다"
            % (branch, detail),
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
