#!/usr/bin/env python3
"""scripts/metrics.py — 플레이북 Stage 1·2 지표 계산기 (stdlib 전용).

플레이북이 정의한 지표 중 **이 저장소가 실제로 잴 수 있는 것만** 잰다.
계산 불가는 빈칸이나 0 이 아니라 `unavailable` + `reason` 으로 낸다 — 조용한 0 은
「결함 없음」과 「못 쟀음」을 뒤섞는다. 무엇을 계산하지 않는지는 docs/METRICS.md 가
정본이다(플레이 14쌍 전수표).

재는 것(사슬 = `intent/<NNNN-slug>/`):

  l1           레슨 2 leading  — frontmatter `created`(발의자 **신고값**) → intent.md 최초 커밋
  l1_accepted  레슨 2 leading  — `created`(신고값) → frontmatter `status` 를 accepted 로
               바꾼 커밋(본문 코드 펜스·인라인 스팬 안의 예시는 승인이 아니다 — 후보를
               `git show <sha>:<path>` 로 꺼내 교차 확인한다)
  l2           레슨 3 leading  — intent.md 최초 커밋 → spec.md 최초 커밋(두 git 타임스탬프)
  l3           레슨 2 lagging  — spec.md 최초 커밋 **이후** intent.md 를 바꾼 커밋 수
  l4           레슨 3 lagging  — plan.md 최초 커밋 **이후** spec.md 를 바꾼 커밋 수
  l5           레슨 2 lagging  — survival rate: intent.md 를 담은 PR 의 merged/(merged+closed)

지표마다 **어떤 명령으로 무엇을 셌는지**(`method`)를 값과 함께 낸다. 계기 자체가
검증 가능해야 하기 때문이다 — 값만 있는 지표는 아무도 반증할 수 없다.

rc: 0 계산 성공(일부 unavailable 이어도 0) · 1 인자·저장소 오류 · 2 판정 불가.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

# 코드 펜스·인라인 코드 스팬 제거와 frontmatter 파싱은 **정본을 재사용한다**.
# 같은 규칙을 두 번 구현하면 두 판정이 갈라지고, 갈라진 쪽이 조용히 이긴다.
# check_artifacts.py 는 실행부가 전부 `if __name__ == "__main__"` 아래라 import
# 부작용이 없다(실측: import 중 stdout·stderr 둘 다 빈 문자열).
_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)
from check_artifacts import extract_frontmatter, strip_code_spans  # noqa: E402

SCHEMA_VERSION = "1.0"

RC_OK = 0
RC_ARG = 1          # 인자·저장소 경로 오류
RC_UNDECIDABLE = 2  # 판정 불가(git 이 없다 · 대상이 git 저장소가 아니다)

INTENT_HOME = "intent"
GH_PR_LIMIT = 200
GH_TIMEOUT_SEC = 30

# survival rate 의 모수: intent 홈 안의 intent.md 를 건드린 PR 만 센다.
INTENT_FILE_RE = re.compile(r"^intent/[^/]+/intent\.md$")

# `created` 는 자기 신고 필드다(§4 「git 이 모르는 유일한 값」). 오프셋을 강제한다 —
# 오프셋 없는 시각은 읽는 기계의 시간대에 따라 값이 달라지므로 지표가 못 된다.
ISO8601_WITH_OFFSET = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})[T ](?P<time>\d{2}:\d{2}:\d{2})"
    r"(?P<frac>\.\d+)?(?P<off>Z|[+-]\d{2}:?\d{2})$"
)

METRIC_LABELS = {
    "l1": "레슨 2 leading — created(신고값) → intent.md 최초 커밋",
    "l1_accepted": "레슨 2 leading — created(신고값) → intent 가 accepted 로 바뀐 커밋",
    "l2": "레슨 3 leading — intent.md 최초 커밋 → spec.md 최초 커밋",
    "l3": "레슨 2 lagging — spec.md 최초 커밋 이후 intent.md 변경 커밋 수",
    "l4": "레슨 3 lagging — plan.md 최초 커밋 이후 spec.md 변경 커밋 수",
    "l5": "레슨 2 lagging — survival rate(intent PR 의 merged/(merged+closed))",
}


# --------------------------------------------------------------------------- git

def run(cmd, cwd=None, timeout=None, env=None):
    """(rc, stdout, stderr). 예외를 rc 로 접어 넣는다 — 계기가 죽는 자리를 값으로 본다."""
    try:
        p = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=env
        )
        return p.returncode, p.stdout, p.stderr
    except FileNotFoundError as exc:
        return 127, "", str(exc)
    except subprocess.TimeoutExpired:
        return 124, "", "timeout: %ds" % (timeout or 0)


def git(repo, *args):
    return run(["git", "-C", repo] + list(args))


def git_first_commit(repo, path):
    """파일이 추가된 가장 오래된 커밋 (sha, author date ISO). 없으면 None.

    `git log --diff-filter=A` 는 새로 → 오래된 순이므로 마지막 줄이 최초 커밋이다.
    삭제 후 재추가된 파일은 A 가 여러 줄 나오는데, 그때도 가장 오래된 것을 쓴다.
    """
    rc, out, _ = git(
        repo, "log", "--diff-filter=A", "--format=%H%x09%aI", "--", path
    )
    if rc != 0:
        return None
    lines = [ln for ln in out.splitlines() if ln.strip()]
    if not lines:
        return None
    sha, iso = lines[-1].split("\t", 1)
    return sha, iso


ACCEPTED_NONE = "none"              # 후보가 아예 없다 → not_applicable
ACCEPTED_CONFIRMED = "confirmed"    # 그 시점 frontmatter 가 실제로 accepted 였다
ACCEPTED_UNCONFIRMED = "unconfirmed"  # 후보는 있는데 하나도 확인되지 않았다 → unavailable


def frontmatter_status_at(repo, sha, path):
    """`<sha>` 시점의 `<path>` frontmatter `status`. (status, None) 또는 (None, 사유).

    코드 스팬을 **먼저** 벗기고(`strip_code_spans`) frontmatter 를 읽는다
    (`extract_frontmatter`) — 둘 다 scripts/check_artifacts.py 의 정본이다.
    """
    rc, out, err = git(repo, "show", "%s:%s" % (sha, path))
    if rc != 0:
        return None, "git show %s:%s 가 rc=%d (%s)" % (
            sha[:8], path, rc, (err or "").strip().splitlines()[:1],
        )
    data = extract_frontmatter(strip_code_spans(out))[0]
    if data is None:
        return None, "%s 시점 파일에 frontmatter 블록이 없다" % sha[:8]
    if "status" not in data:
        return None, "%s 시점 frontmatter 에 `status` 키가 없다" % sha[:8]
    return data["status"], None


def git_accepted_commit(repo, path):
    """`status: accepted` 로 실제로 바꾼 **가장 오래된** 커밋을 교차 확인해서 고른다.

    돌려주는 것: (kind, sha, iso, candidates, reason)
      kind == ACCEPTED_NONE          후보가 없다(draft/rejected 로만 살았다)
      kind == ACCEPTED_CONFIRMED     sha/iso 가 승인 커밋이다
      kind == ACCEPTED_UNCONFIRMED   후보는 있는데 전부 걸러졌다 — reason 이 사유다

    설계 §4: `accepted_at` 필드를 두지 않는다 — git 이 안다. 자기 신고 필드를
    하나라도 줄이는 쪽이 지표에 유리하다.

    🔴 픽스액스(`git log -S`)는 **문자열 등장 횟수**가 바뀐 커밋을 낸다. 본문의
    인라인 코드 스팬(`` `status: accepted` ``)이나 코드 펜스 안의 예시도 똑같이
    센다 — 그래서 가장 오래된 줄을 교차 확인 없이 쓰면 **draft 로 태어난 커밋**이
    승인 커밋이 된다(실물 사고: PR #12 intent/0001-bootstrap-repo/intent.md L17
    인라인 스팬이 4accbd1 을 승인 커밋으로 만들었고 l1_accepted 가 l1 과 같은
    값으로 붕괴했다). 그래서 후보마다 `git show <sha>:<path>` 로 그 시점의 파일을
    꺼내 코드 스팬을 벗긴 뒤 frontmatter 를 실제로 파싱해 확인한다.

    🔴 알려진 한계: 같은 커밋에서 본문의 예시를 지우면서 frontmatter 를 accepted 로
    바꾸면 `status: accepted` 등장 횟수가 1→1 이라 `-S` 가 그 커밋을 **후보로 아예
    내지 않는다** — 교차 확인은 후보를 거를 뿐 후보를 만들지 못하므로 이 갈래는
    여전히 보이지 않는다(그때는 후보가 0건이라 not_applicable 로 나온다).
    """
    rc, out, err = git(
        repo, "log", "-Sstatus: accepted", "--format=%H%x09%aI", "--", path
    )
    if rc != 0:
        return (
            ACCEPTED_UNCONFIRMED, None, None, [],
            "git log -S 가 rc=%d 로 실패했다 — 후보를 열거하지 못했다 (%s)"
            % (rc, (err or "").strip().splitlines()[:1]),
        )
    lines = [ln for ln in out.splitlines() if ln.strip()]
    if not lines:
        return ACCEPTED_NONE, None, None, [], None
    # `git log` 는 새로 → 오래된 순이므로 뒤에서부터 본다(가장 오래된 승인이 답이다).
    rows = []
    for ln in reversed(lines):
        sha, _, iso = ln.partition("\t")
        rows.append((sha, iso))
    candidates = [sha for sha, _ in rows]
    rejected = []
    for sha, iso in rows:
        status, why = frontmatter_status_at(repo, sha, path)
        if status == "accepted":
            return ACCEPTED_CONFIRMED, sha, iso, candidates, None
        rejected.append("%s(%s)" % (sha[:8], why or "status=%r" % status))
    return (
        ACCEPTED_UNCONFIRMED, None, None, candidates,
        "픽스액스 후보 %d건이 전부 교차 확인에서 걸러졌다 — 그 시점 파일의 "
        "frontmatter `status` 가 accepted 가 아니었다(본문 코드 스팬·펜스 안의 "
        "예시를 센 것이다): %s" % (len(rows), ", ".join(rejected)),
    )


def git_count_commits_after(repo, base_sha, path):
    """`base_sha` **이후**에 `path` 를 바꾼 커밋 수. 실패하면 None.

    🔴 시계(`git log --since=<시각>`)를 쓰지 않는다. `--since` 는 경계값을 **포함**하므로,
    base 커밋과 같은 초에 들어온 그 이전 커밋까지 세어 버린다(실제로 일어난다 —
    intent 를 고치고 곧바로 spec 을 커밋하면 두 커밋이 같은 초다). 커밋 그래프의
    **위상**은 그런 경계가 없다: `base..HEAD` 는 base 의 조상을 정의상 제외한다.
    같은 이유로 커밋 시각의 시간대·재작성(rebase)에도 흔들리지 않는다.
    """
    rc, out, _ = git(repo, "rev-list", "--count", "%s..HEAD" % base_sha, "--", path)
    if rc != 0:
        return None
    try:
        return int(out.strip())
    except ValueError:
        return None


# --------------------------------------------------- frontmatter · 시각 파싱

def parse_frontmatter(text):
    """맨 앞 `---` 블록의 `key: value` 만 읽는다(YAML 파서 없이 stdlib)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fields = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = re.sub(r"\s+#.*$", "", value).strip()  # 줄 끝 주석 제거
        fields[key.strip()] = value
    return fields


def parse_created(raw):
    """(datetime, None) 또는 (None, 사유). 오프셋 없는 시각은 거절한다."""
    if raw is None:
        return None, "intent frontmatter 에 `created` 키가 없다 — 레슨 2 leading 지표의 기점이 없다"
    if not raw:
        return None, "intent frontmatter 의 `created` 가 비어 있다"
    m = ISO8601_WITH_OFFSET.match(raw)
    if not m:
        return None, (
            "`created: %s` 가 오프셋 있는 ISO8601 이 아니다 — 오프셋이 없으면 읽는 "
            "기계의 시간대에 따라 값이 달라져 지표가 못 된다" % raw
        )
    off = m.group("off")
    off = "+00:00" if off == "Z" else (off if ":" in off else off[:3] + ":" + off[3:])
    try:
        dt = datetime.strptime(
            "%sT%s%s" % (m.group("date"), m.group("time"), off.replace(":", "")),
            "%Y-%m-%dT%H:%M:%S%z",
        )
    except ValueError as exc:
        return None, "`created: %s` 를 시각으로 읽지 못했다: %s" % (raw, exc)
    return dt, None


def parse_git_iso(raw):
    """git `%aI`(strict ISO 8601, 오프셋 포함)을 datetime 으로."""
    m = ISO8601_WITH_OFFSET.match(raw.strip())
    if not m:
        return None
    off = m.group("off")
    off = "+00:00" if off == "Z" else (off if ":" in off else off[:3] + ":" + off[3:])
    try:
        return datetime.strptime(
            "%sT%s%s" % (m.group("date"), m.group("time"), off.replace(":", "")),
            "%Y-%m-%dT%H:%M:%S%z",
        )
    except ValueError:
        return None


# ------------------------------------------------------------------- 지표 그릇

def metric(status, value=None, unit=None, method="", inputs=None, reason=None):
    out = {
        "value": value,
        "unit": unit,
        "method": method,
        "inputs": inputs or {},
        "status": status,
    }
    if status == "unavailable":
        # 계약: unavailable 이면 반드시 사유가 붙는다.
        out["reason"] = reason or "사유 미기재(계기 결함)"
    elif reason:
        out["reason"] = reason
    return out


def unavailable(method, reason, inputs=None):
    return metric("unavailable", None, "seconds", method, inputs, reason)


# ------------------------------------------------------------------- 사슬 계산

def discover_chains(repo, only_id=None):
    home = os.path.join(repo, INTENT_HOME)
    found = []
    if os.path.isdir(home):
        for name in sorted(os.listdir(home)):
            chain_dir = os.path.join(home, name)
            if not os.path.isdir(chain_dir):
                continue
            if not os.path.isfile(os.path.join(chain_dir, "intent.md")):
                continue
            found.append(name)
    if only_id is not None:
        return [c for c in found if c == only_id], found
    return found, found


def compute_chain(repo, chain_id):
    ipath = "%s/%s/intent.md" % (INTENT_HOME, chain_id)
    spath = "%s/%s/spec.md" % (INTENT_HOME, chain_id)
    ppath = "%s/%s/plan.md" % (INTENT_HOME, chain_id)

    m_first = "git log --diff-filter=A --format=%%aI -- %s (가장 오래된 것)"
    method_l1 = (
        "frontmatter `created`(발의자 신고값) → `" + (m_first % ipath) + "` 의 차이"
    )
    method_l1a = (
        "frontmatter `created`(발의자 신고값) → "
        "`git log -Sstatus: accepted --format=%aI -- " + ipath + "` 의 후보 중, "
        "`git show <sha>:" + ipath + "` 로 그 시점 파일을 꺼내 코드 스팬을 벗기고 "
        "frontmatter `status` 가 accepted 임을 교차 확인한 가장 오래된 커밋 "
        "(펜스·인라인 코드 스팬 안의 예시는 승인이 아니다)"
    )
    method_l2 = (
        "`" + (m_first % ipath) + "` → `" + (m_first % spath) + "` (두 git 타임스탬프)"
    )
    method_l3 = (
        "위상: `git rev-list --count <spec 최초 커밋 sha>..HEAD -- " + ipath + "` "
        "(시계 --since 를 쓰지 않는다 — 같은 초 경계를 포함해 버린다)"
    )
    method_l4 = (
        "위상: `git rev-list --count <plan 최초 커밋 sha>..HEAD -- " + spath + "` "
        "(같은 이유로 시계를 쓰지 않는다)"
    )

    intent_text = ""
    try:
        with open(os.path.join(repo, ipath), "r", encoding="utf-8") as fh:
            intent_text = fh.read()
    except OSError as exc:
        intent_text = ""
        read_error = str(exc)
    else:
        read_error = None

    fm = parse_frontmatter(intent_text)
    created_raw = fm.get("created")
    created_dt, created_reason = parse_created(created_raw)
    if read_error:
        created_dt, created_reason = None, "intent.md 를 읽지 못했다: %s" % read_error

    intent_first = git_first_commit(repo, ipath)
    spec_first = git_first_commit(repo, spath)
    plan_first = git_first_commit(repo, ppath)
    acc_kind, acc_sha, acc_iso, acc_candidates, acc_reason = git_accepted_commit(
        repo, ipath
    )

    metrics = {}

    # --- l1 --------------------------------------------------------------
    inputs_l1 = {
        "intent_path": ipath,
        "created_reported": created_raw,
        "created_is_self_reported": True,
        "intent_first_commit": intent_first[0] if intent_first else None,
        "intent_first_commit_at": intent_first[1] if intent_first else None,
    }
    if created_dt is None:
        metrics["l1"] = unavailable(method_l1, created_reason, inputs_l1)
    elif intent_first is None:
        metrics["l1"] = unavailable(
            method_l1, "%s 가 git 이력에 없다(아직 커밋되지 않았다)" % ipath, inputs_l1
        )
    else:
        commit_dt = parse_git_iso(intent_first[1])
        if commit_dt is None:
            metrics["l1"] = unavailable(
                method_l1, "git 이 낸 시각 %r 를 읽지 못했다" % intent_first[1], inputs_l1
            )
        else:
            delta = int((commit_dt - created_dt).total_seconds())
            if delta < 0:
                metrics["l1"] = unavailable(
                    method_l1,
                    "신고된 `created`(%s)가 최초 커밋(%s)보다 미래다 — 음수 소요시간을 "
                    "지어내지 않는다(신고값 오류로 보고 발의자가 고쳐야 한다)"
                    % (created_raw, intent_first[1]),
                    inputs_l1,
                )
            else:
                metrics["l1"] = metric("ok", delta, "seconds", method_l1, inputs_l1)

    # --- l1_accepted ------------------------------------------------------
    inputs_l1a = {
        "intent_path": ipath,
        "created_reported": created_raw,
        "created_is_self_reported": True,
        "accepted_commit": acc_sha,
        "accepted_commit_at": acc_iso,
        # 픽스액스가 낸 후보 전량. 걸러진 것까지 남겨야 이 값을 반증할 수 있다.
        "accepted_candidates": acc_candidates,
        "accepted_cross_checked": True,
    }
    if acc_kind == ACCEPTED_NONE:
        metrics["l1_accepted"] = metric(
            "not_applicable", None, "seconds", method_l1a, inputs_l1a,
            reason="아직 `status: accepted` 로 바꾼 커밋이 없다(draft 또는 rejected)",
        )
    elif acc_kind == ACCEPTED_UNCONFIRMED:
        # 「승인이 아직 없다」가 아니라 「후보를 못 골랐다」다 — 0 이나 임의값을
        # 지어내지 않는다.
        metrics["l1_accepted"] = unavailable(method_l1a, acc_reason, inputs_l1a)
    elif created_dt is None:
        metrics["l1_accepted"] = unavailable(method_l1a, created_reason, inputs_l1a)
    else:
        acc_dt = parse_git_iso(acc_iso)
        if acc_dt is None:
            metrics["l1_accepted"] = unavailable(
                method_l1a, "git 이 낸 시각 %r 를 읽지 못했다" % acc_iso, inputs_l1a
            )
        else:
            delta = int((acc_dt - created_dt).total_seconds())
            if delta < 0:
                metrics["l1_accepted"] = unavailable(
                    method_l1a,
                    "신고된 `created`(%s)가 accepted 커밋(%s)보다 미래다" % (created_raw, acc_iso),
                    inputs_l1a,
                )
            else:
                metrics["l1_accepted"] = metric("ok", delta, "seconds", method_l1a, inputs_l1a)

    # --- l2 ---------------------------------------------------------------
    inputs_l2 = {
        "intent_first_commit": intent_first[0] if intent_first else None,
        "intent_first_commit_at": intent_first[1] if intent_first else None,
        "spec_first_commit": spec_first[0] if spec_first else None,
        "spec_first_commit_at": spec_first[1] if spec_first else None,
    }
    if intent_first is None or spec_first is None:
        missing = ipath if intent_first is None else spath
        metrics["l2"] = metric(
            "not_applicable", None, "seconds", method_l2, inputs_l2,
            reason="%s 가 아직 git 이력에 없다 — 두 타임스탬프 중 하나가 없다" % missing,
        )
    else:
        a, b = parse_git_iso(intent_first[1]), parse_git_iso(spec_first[1])
        if a is None or b is None:
            metrics["l2"] = unavailable(method_l2, "git 이 낸 시각을 읽지 못했다", inputs_l2)
        else:
            delta = int((b - a).total_seconds())
            if delta < 0:
                metrics["l2"] = unavailable(
                    method_l2,
                    "spec 최초 커밋이 intent 최초 커밋보다 이르다 — 사슬 순서가 뒤집혀 "
                    "leading 지표로 읽을 수 없다",
                    inputs_l2,
                )
            else:
                metrics["l2"] = metric("ok", delta, "seconds", method_l2, inputs_l2)

    # --- l3 / l4 ----------------------------------------------------------
    metrics["l3"] = _count_metric(
        repo, base=spec_first, target_path=ipath, method=method_l3,
        na_reason="%s 가 아직 git 이력에 없다 — 기준선이 없다" % spath,
        base_label="spec_first_commit",
    )
    metrics["l4"] = _count_metric(
        repo, base=plan_first, target_path=spath, method=method_l4,
        na_reason="%s 가 아직 git 이력에 없다 — 기준선이 없다" % ppath,
        base_label="plan_first_commit",
    )

    return {
        "id": chain_id,
        "paths": {"intent": ipath, "spec": spath, "plan": ppath},
        "status_field": fm.get("status"),
        "metrics": metrics,
    }


def _count_metric(repo, base, target_path, method, na_reason, base_label):
    inputs = {
        "base_commit": base[0] if base else None,
        "base_commit_at": base[1] if base else None,
        "base_commit_role": base_label,
        "counted_path": target_path,
    }
    if base is None:
        return metric("not_applicable", None, "commits", method, inputs, reason=na_reason)
    count = git_count_commits_after(repo, base[0], target_path)
    if count is None:
        return metric(
            "unavailable", None, "commits", method, inputs,
            reason="git rev-list 가 실패했다 — 세지 못했다",
        )
    return metric("ok", count, "commits", method, inputs)


# ------------------------------------------------------------ survival rate

def compute_survival(repo):
    gh_cmd = [
        "gh", "pr", "list", "--state", "all",
        "--limit", str(GH_PR_LIMIT), "--json", "number,state,files",
    ]
    method = (
        "`" + " ".join(gh_cmd) + "` 로 PR 을 받아 `intent/<사슬>/intent.md` 를 담은 PR 만 "
        "고르고 merged/(merged+closed) 를 낸다(OPEN 은 분모에서 제외 — 아직 판정되지 않았다)"
    )
    inputs = {"command": " ".join(gh_cmd), "intent_file_pattern": INTENT_FILE_RE.pattern}

    if shutil.which("gh") is None:
        return metric(
            "unavailable", None, "ratio", method, inputs,
            reason="`gh` 가 PATH 에 없다 — PR 의 merge/close 판정은 git 이력에 없고 "
                   "GitHub 만 안다. 계산하지 않는다(0 을 내면 「전부 닫혔다」로 읽힌다)",
        )

    rc, out, err = run(gh_cmd, cwd=repo, timeout=GH_TIMEOUT_SEC)
    if rc != 0:
        head = (err or out).strip().splitlines()
        head = head[0] if head else "(출력 없음)"
        return metric(
            "unavailable", None, "ratio", method, inputs,
            reason="`gh pr list` 가 rc=%d 로 실패했다(네트워크·인증·리모트 미설정): %s" % (rc, head),
        )
    try:
        prs = json.loads(out)
    except ValueError as exc:
        return metric(
            "unavailable", None, "ratio", method, inputs,
            reason="`gh pr list` 출력이 JSON 이 아니다: %s" % exc,
        )

    merged, closed, numbers = 0, 0, []
    for pr in prs:
        files = pr.get("files") or []
        paths = [f.get("path", "") for f in files if isinstance(f, dict)]
        if not any(INTENT_FILE_RE.match(p) for p in paths):
            continue
        state = str(pr.get("state", "")).upper()
        if state == "MERGED":
            merged += 1
        elif state == "CLOSED":
            closed += 1
        else:
            continue  # OPEN — 아직 product owner 가 판정하지 않았다
        numbers.append(pr.get("number"))

    inputs.update({"merged": merged, "closed": closed, "pr_numbers": numbers})
    denom = merged + closed
    if denom == 0:
        return metric(
            "not_applicable", None, "ratio", method, inputs,
            reason="intent.md 를 담은 채 merge/close 된 PR 이 아직 없다 — 분모가 0 이다",
        )
    return metric("ok", merged / denom, "ratio", method, inputs)


# ---------------------------------------------------------------------- 출력

def fmt_value(m):
    if m["value"] is None:
        return "—"
    if m["unit"] == "ratio":
        return "%.3f" % m["value"]
    if m["unit"] == "seconds":
        return "%d (%s)" % (m["value"], human_seconds(m["value"]))
    return str(m["value"])


def human_seconds(sec):
    sec = int(sec)
    d, rem = divmod(sec, 86400)
    h, rem = divmod(rem, 3600)
    mi, s = divmod(rem, 60)
    parts = []
    if d:
        parts.append("%d일" % d)
    if h:
        parts.append("%d시간" % h)
    if mi:
        parts.append("%d분" % mi)
    if s or not parts:
        parts.append("%d초" % s)
    return " ".join(parts)


def cell(text):
    return str(text if text not in (None, "") else "—").replace("|", "\\|").replace("\n", " ")


def render_text(doc):
    out = []
    out.append("# 플레이북 Stage 1·2 지표 — %s" % doc["repo"])
    out.append("")
    out.append("- 계산 시각(UTC): %s" % doc["generated_at"])
    out.append("- HEAD: %s" % (doc.get("head") or "—"))
    out.append("- schema_version: %s" % doc["schema_version"])
    out.append("")
    for note in doc.get("notes", []):
        out.append("> %s" % note)
    if doc.get("notes"):
        out.append("")

    out.append("## 사슬별")
    out.append("")
    out.append("| 사슬 | 지표 | 값 | 단위 | 상태 | 사유 |")
    out.append("|---|---|---|---|---|---|")
    if not doc["chains"]:
        out.append("| — | — | — | — | — | 사슬 없음(W2 에서 들어온다) |")
    for chain in doc["chains"]:
        for key in ("l1", "l1_accepted", "l2", "l3", "l4"):
            m = chain["metrics"][key]
            out.append(
                "| %s | %s | %s | %s | %s | %s |"
                % (cell(chain["id"]), cell(key), cell(fmt_value(m)), cell(m["unit"]),
                   cell(m["status"]), cell(m.get("reason")))
            )
    out.append("")

    out.append("## 저장소 전체")
    out.append("")
    out.append("| 지표 | 값 | 단위 | 상태 | 사유 |")
    out.append("|---|---|---|---|---|")
    for key, m in doc["repo_metrics"].items():
        out.append(
            "| %s | %s | %s | %s | %s |"
            % (cell(key), cell(fmt_value(m)), cell(m["unit"]), cell(m["status"]),
               cell(m.get("reason")))
        )
    out.append("")

    out.append("## 계기 — 무엇을 어떤 명령으로 셌는가")
    out.append("")
    out.append("| 지표 | 무엇을 세는가 | 계산 |")
    out.append("|---|---|---|")
    seen = []
    for chain in doc["chains"]:
        for key in ("l1", "l1_accepted", "l2", "l3", "l4"):
            if key in seen:
                continue
            seen.append(key)
            out.append(
                "| %s | %s | %s |"
                % (cell(key), cell(METRIC_LABELS[key]), cell(chain["metrics"][key]["method"]))
            )
    for key, m in doc["repo_metrics"].items():
        out.append("| %s | %s | %s |" % (cell(key), cell(METRIC_LABELS.get(key, "")), cell(m["method"])))
    out.append("")
    out.append(
        "`created` 는 발의자 **신고값**이다 — git 이 모르는 유일한 값이므로 l1·l1_accepted 는 "
        "그 신고를 믿는 만큼만 믿을 수 있다. 나머지는 전부 git/GitHub 이 아는 사실이다."
    )
    if not doc["chains"]:
        out.append("")
        out.append("사슬 없음(W2 에서 들어온다) — 잰 것이 없다.")
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------- 진입점

class Parser(argparse.ArgumentParser):
    """argparse 기본 rc 는 2 지만, 이 스크립트에서 2 는 「판정 불가」다.

    인자 오류는 rc=1 로 낸다(출력 계약).
    """

    def error(self, message):
        sys.stderr.write("인자 오류: %s\n" % message)
        sys.exit(RC_ARG)


def main(argv=None):
    parser = Parser(
        prog="metrics.py",
        description="플레이북 Stage 1·2 지표 계산기 — 재는 것만 재고, 못 재는 것은 unavailable + 사유로 낸다.",
    )
    parser.add_argument("--repo", default=".", help="대상 저장소 경로(기본: 현재 디렉터리)")
    parser.add_argument("--format", dest="fmt", default="text", choices=["text", "json"])
    parser.add_argument("--id", dest="chain_id", default=None, help="사슬 하나만(예: 0001-bootstrap-repo)")
    args = parser.parse_args(argv)

    if shutil.which("git") is None:
        sys.stderr.write("판정 불가: `git` 이 PATH 에 없다 — 이 지표는 전부 git 이력에서 나온다\n")
        return RC_UNDECIDABLE

    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        sys.stderr.write("인자 오류: --repo 경로가 디렉터리가 아니다: %s\n" % repo)
        return RC_ARG

    rc, out, err = git(repo, "rev-parse", "--show-toplevel")
    if rc != 0:
        sys.stderr.write(
            "판정 불가: %s 는 git 저장소가 아니다 — 이 지표는 커밋 이력에서만 나온다 (%s)\n"
            % (repo, (err or out).strip().splitlines()[:1])
        )
        return RC_UNDECIDABLE
    repo = out.strip() or repo

    selected, all_chains = discover_chains(repo, args.chain_id)
    if args.chain_id is not None and not selected:
        sys.stderr.write(
            "인자 오류: --id %s 에 해당하는 사슬이 없다. 있는 사슬: %s\n"
            % (args.chain_id, ", ".join(all_chains) or "(없음)")
        )
        return RC_ARG

    rc_head, head_out, _ = git(repo, "rev-parse", "HEAD")
    head = head_out.strip() if rc_head == 0 else None

    notes = []
    if not selected:
        notes.append("사슬 없음(W2 에서 들어온다) — %s/ 밑에 intent.md 가 하나도 없다" % INTENT_HOME)

    doc = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repo": repo,
        "head": head,
        "chains": [compute_chain(repo, cid) for cid in selected],
        "repo_metrics": {"l5": compute_survival(repo)},
        "notes": notes,
    }

    if args.fmt == "json":
        sys.stdout.write(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
    else:
        sys.stdout.write(render_text(doc))
    return RC_OK


if __name__ == "__main__":
    sys.exit(main())
