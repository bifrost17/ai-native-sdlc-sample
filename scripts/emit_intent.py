#!/usr/bin/env python3
"""scripts/emit_intent.py — 검출 결과 → Stage 1 형식 intent 초안 (레슨 13).

레슨 13 의 지시: 에이전트는 진단을 **Stage 1: Plan 형식의 intent.md** 로 쓰고,
거기에 이상과 그 증거 · 제안하는 결과 · 영향 시스템 · 미결 물음을 담는다.
여기서는 그 중 「형식과 증거」만 기계가 채운다 — 원인·처방은 채우지 않는다.
검출기가 재지 않은 것을 초안이 아는 척하면 그 초안은 증거가 아니라 추측이다.

입력   scripts/detect_bands.py 의 stdout JSON (파이프 또는 --input)
출력   <--out>/<--id>/intent.md  (docs/DESIGN.md §3.1 스키마 그대로)

tier 규칙
    none · 1sigma  → 초안을 만들지 않고 rc=0 으로 조용히 끝낸다(설정상 행동이
                     log 이거나 없다 — 판정마다 파일을 만들면 사슬이 소음이 된다).
    2sigma · 3sigma → intent.md 초안을 쓴다. status 는 언제나 draft 이고,
                     accepted 로 바꾸는 것은 사람이다.

rc 계약 (검출기와 같은 이유로 tier 를 겸하지 않는다)
    0 = 정상 종료(초안을 썼든 건너뛰었든) · 1 = 입력 오류 · 2 = 쓰기 실패

플레이스홀더를 남기지 않는다
    docs/DESIGN.md §3.1 의 템플릿은 사람이 채울 자리를 ‹…› 로 표시하지만,
    **초안에는 그것을 그대로 두지 않는다**. 검증기가 플레이스홀더 잔존을 red 로
    잡기도 하고, 무엇보다 「사람이 채워야 한다」는 사실 자체를 명시 문장으로
    적는 편이 다음 사람에게 정확하다.
"""

import argparse
import json
import os
import re
import sys

REQUIRED_FIELDS = ["schema_version", "metric", "tier", "action", "rule",
                   "rules_fired", "z", "mean", "sigma", "n", "observed",
                   "evidence", "detected_at"]
SUPPORTED_SCHEMA = 1
WRITE_TIERS = ("2sigma", "3sigma")
ID_PATTERN = re.compile(r"^\d{4}-[a-z0-9]+(-[a-z0-9]+)*$")

RULE_NOTE = {
    "rule1_one_point_beyond_3sigma":
        "규칙1 은 최신 1점만 본다. 그 앞의 점들이 정상이었는지는 이 판정이 말하지 않는다.",
    "rule2_nine_points_one_side":
        "규칙2 는 최신 9점만 본다. 느린 이동이 언제 시작됐는지는 이 판정이 재지 않는다 — "
        "시작 시점은 표본 전체를 다시 훑어야 답한다.",
    "rule3_two_of_three_beyond_2sigma":
        "규칙3 은 최신 3점만 본다. 같은 이탈이 그 앞에서도 있었는지는 이 판정이 재지 않는다.",
}


class InputError(Exception):
    """입력 오류 — rc=1."""


def load_detection(path):
    if path:
        try:
            with open(path, "r", encoding="utf-8") as fh:
                text = fh.read()
        except OSError as exc:
            raise InputError("검출 결과를 읽을 수 없다: %s (%s)" % (path, exc))
    else:
        text = sys.stdin.read()
    if not text.strip():
        raise InputError("검출 결과가 비었다 — 파이프로 넣었는가?")
    try:
        data = json.loads(text)
    except ValueError as exc:
        raise InputError("검출 결과가 JSON 이 아니다 — %s" % exc)
    if not isinstance(data, dict):
        raise InputError("검출 결과가 객체가 아니다.")
    missing = [k for k in REQUIRED_FIELDS if k not in data]
    if missing:
        raise InputError(
            "detect_bands.py 의 출력이 아니다 — 필수 필드 누락 %s. "
            "빈 초안을 쓰느니 멈춘다." % missing)
    if data["schema_version"] != SUPPORTED_SCHEMA:
        raise InputError("모르는 schema_version %r — 아는 것은 %d 뿐이다."
                         % (data["schema_version"], SUPPORTED_SCHEMA))
    if data["tier"] not in ("none", "1sigma", "2sigma", "3sigma"):
        raise InputError("모르는 tier %r" % data["tier"])
    return data


def _num(value, digits=6):
    return "미측정" if value is None else ("%.*f" % (digits, value))


def _signed(value, digits=3):
    return "미측정" if value is None else ("%+.*f" % (digits, value))


def _series(points, limit=12):
    values = ["%.6f" % p["value"] for p in points][-limit:]
    return ", ".join(values)


def render_intent(data, intent_id):
    """docs/DESIGN.md §3.1 스키마의 intent.md 본문을 만든다."""
    metric = data["metric"]
    observed = data["observed"]
    evidence = data["evidence"]
    window = evidence["window"]
    cfg = evidence.get("config", {})
    mean, sigma = data["mean"], data["sigma"]
    rule = data["rule"] or "규칙 없음"
    bands = ""
    if mean is not None and sigma is not None:
        bands = " / ".join(_num(mean + k * sigma) for k in (1, 2, 3))
    span = "표본 없음"
    if window:
        span = "%s ~ %s (%d점)" % (window[0]["ts"], window[-1]["ts"], len(window))

    front = [
        "---",
        "id: %s" % intent_id,
        "kind: intent",
        "status: draft",
        "author: detect_bands (자동)",
        "created: %s" % data["detected_at"],
        "record: none",
        "supersedes: none",
        "---",
    ]

    body = []
    body.append("# Intent: %s 밴드 이탈 (%s · %s)"
                % (metric, data["tier"], rule))
    body.append("")
    body.append("## Problem (문제)")
    body.append("")
    body.append(
        "`%s` 의 최신 표본(%s · 값 %s)이 롤링 기준선 밴드를 벗어났다. "
        "기준선은 그 표본 앞의 %d점이고 평균 %s · 표준편차 %s 이며, 최신 표본의 z 는 %s 이다."
        % (metric, observed["ts"], _num(observed["value"]), data["n"],
           _num(mean), _num(sigma), _signed(data["z"])))
    body.append(
        "결정론 검출기 `scripts/detect_bands.py` 가 규칙 `%s` 로 tier `%s` 를 판정했다 — "
        "판정에 모델은 개입하지 않았고, 같은 표본과 같은 설정이면 같은 판정이 다시 나온다."
        % (rule, data["tier"]))
    body.append("")
    body.append("증거:")
    body.append("")
    body.append("| 항목 | 값 |")
    body.append("|---|---|")
    body.append("| 지표 | `%s` |" % metric)
    body.append("| 최신 표본 | %s = %s |" % (observed["ts"], _num(observed["value"])))
    body.append("| 기준선 창 | %s |" % span)
    body.append("| 평균 · 표준편차 | %s · %s |" % (_num(mean), _num(sigma)))
    body.append("| 1σ / 2σ / 3σ 상한 | %s |" % (bands or "미측정"))
    body.append("| z | %s |" % _signed(data["z"]))
    body.append("| 걸린 규칙 | %s |" % ", ".join(data["rules_fired"] or ["없음"]))
    body.append("| 설정 | window %s · min_samples %s · min_baseline_rate %s |"
                % (cfg.get("window", "미기재"), cfg.get("min_samples", "미기재"),
                   cfg.get("min_baseline_rate", "미기재")))
    body.append("| 판정 시각 | %s |" % data["detected_at"])
    body.append("")
    body.append("판정 대상 구간의 값(오래된 것부터): %s"
                % _series(evidence.get("evaluated", [])))
    body.append("")
    body.append("## Proposed outcome (원하는 결과)")
    body.append("")
    body.append(
        "`%s` 가 기준선 밴드 안으로 돌아오고, 그 복귀가 이 사슬의 시험으로 확인된다."
        % metric)
    body.append(
        "검출 시점에 설정이 지정한 행동은 `%s` 였고, 이 초안이 그 행동의 산출이다."
        % data["action"])
    body.append(
        "이 초안이 accepted 되면 spec 이 위 증거를 요구(R#)와 수용 기준(AC#)으로 옮긴다. "
        "rejected 되면 그 판단과 이유가 PR close 로 남는다 — 어느 쪽이든 이탈이 조용히 사라지지는 않는다.")
    body.append("")
    body.append("## Affected users and systems (영향 범위)")
    body.append("")
    body.append(
        "지표 `%s` 를 생산하는 CI 파이프라인, 그리고 그 지표를 신뢰해 머지를 판단하는 사람 전부."
        % metric)
    body.append(
        "검출기는 어떤 시험·어떤 커밋이 실패했는지는 재지 않는다 — 영향 범위의 나머지"
        "(실패한 시험 목록 · 연관 변경 · 사용자 체감)는 diagnose 단계가 1차 자료로 채운다.")
    body.append(
        "표본을 생산하는 경로 자체도 영향 범위에 든다. 표본이 끊기면 이 검출은 "
        "이탈을 못 본 채 조용히 멈춘다.")
    body.append("")
    body.append("## Constraints (제약)")
    body.append("")
    body.append(
        "- C1 이 초안은 검출기가 자동으로 썼고 status 는 draft 다. "
        "사람이 accepted 로 바꾸기 전에는 하류(spec · plan)를 시작하지 않는다.")
    body.append(
        "- C2 검출기는 원인도 처방도 재지 않는다. 원인 추정을 이 초안 본문에 적지 않는다 "
        "— 그것은 diagnose 단계의 산출이고, 초안에 섞으면 증거와 추측이 구별되지 않는다.")
    body.append(
        "- C3 위 수치는 판정 시각 %s 의 표본에서 나온 관측이다. 표본이 갱신되면 새 판정을 "
        "새 초안으로 내고, 이 초안의 수치는 고쳐 쓰지 않는다." % data["detected_at"])
    body.append("")
    body.append("## Open questions (미결)")
    body.append("")
    body.append(
        "- Q1 이 이탈이 코드 변경 때문인지 인프라·상류 변동 때문인지 아직 모른다. "
        "검출기는 원인을 재지 않으므로 diagnose 단계가 1차 자료로 답한다.")
    body.append(
        "- Q2 밴드 설정(window %s · min_samples %s · min_baseline_rate %s)이 이 지표에 "
        "맞는지 아직 모른다. 이탈이 세 번 쌓이기 전에는 설정을 바꾸지 않는다."
        % (cfg.get("window", "미기재"), cfg.get("min_samples", "미기재"),
           cfg.get("min_baseline_rate", "미기재")))
    body.append("- Q3 %s" % RULE_NOTE.get(data["rule"],
                "이 판정은 최신 구간만 본다 — 그 앞 구간의 이력은 이 초안이 말하지 않는다."))
    body.append("")
    return "\n".join(front) + "\n" + "\n".join(body)


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        self.exit(1, "%s: 인자 오류: %s\n" % (self.prog, message))


def main(argv=None):
    parser = _Parser(description="검출 결과 → Stage 1 형식 intent 초안")
    parser.add_argument("--input", default=None,
                        help="detect_bands.py 의 JSON 파일(생략하면 표준입력)")
    parser.add_argument("--id", required=True, dest="intent_id",
                        help="intent ID (NNNN-slug)")
    parser.add_argument("--out", required=True, help="intent 홈 디렉터리")
    args = parser.parse_args(argv)

    try:
        if not ID_PATTERN.match(args.intent_id):
            raise InputError("--id 가 NNNN-slug 형태가 아니다: %r" % args.intent_id)
        data = load_detection(args.input)
    except InputError as exc:
        sys.stderr.write("입력 오류: %s\n" % exc)
        return 1

    if data["tier"] not in WRITE_TIERS:
        sys.stdout.write(json.dumps(
            {"status": "skipped", "written": None, "tier": data["tier"],
             "reason": data.get("reason"),
             "note": "tier 가 %s 라 초안을 만들지 않는다(2sigma 이상만 초안)."
                     % data["tier"]},
            ensure_ascii=False) + "\n")
        return 0

    target_dir = os.path.join(args.out, args.intent_id)
    target = os.path.join(target_dir, "intent.md")
    try:
        os.makedirs(target_dir, exist_ok=True)
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(render_intent(data, args.intent_id))
    except OSError as exc:
        sys.stderr.write("초안을 쓸 수 없다: %s (%s)\n" % (target, exc))
        return 2

    sys.stdout.write(json.dumps(
        {"status": "written", "written": target, "tier": data["tier"],
         "rule": data["rule"], "action": data["action"]},
        ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
