#!/usr/bin/env python3
"""scripts/detect_bands.py — Stage 6 결정론 밴드 검출기 (레슨 13 · 모델 미개입).

무엇을 하는가
    표본(jsonl)의 롤링 창에서 평균·표준편차를 구하고, Western Electric 규칙 중
    **우리가 구현한 세 가지**로 이탈을 판정해 tier 를 stdout JSON 으로 낸다.
    판정에 모델은 개입하지 않는다 — 같은 입력이면 언제나 같은 tier 가 나온다.

구현한 규칙 (그 외 규칙은 설정에서 요구되면 rc=1 로 죽는다)
    rule1_one_point_beyond_3sigma        최신 1점이 3σ 밖            → tier 3sigma
    rule2_nine_points_one_side           최신 9점이 전부 평균 한쪽    → tier 2sigma
    rule3_two_of_three_beyond_2sigma     최신 3점 중 2점이 같은 쪽 2σ 밖 → tier 2sigma

    세 규칙 모두 **최신 점에서 끝나는 구간**만 본다. 그보다 앞선 점들은 그때의
    실행이 이미 판정했다 — 같은 이탈을 매일 다시 제안하지 않기 위해서다.
    규칙이 하나도 안 걸려도 최신 점의 |z| 가 1 이상이면 tier 1sigma(기록만)다.

    기준선 창은 판정 대상 꼬리(최신 9점)를 **제외**한다. 포함하면 지속적 이동이
    자기 자신을 기준선에 섞어 평균을 끌어올려 규칙2 가 자기 눈을 가린다.

🔴 rc 계약 — rc 는 tier 를 겸하지 않는다
    0 = 판정 성공(tier 가 none 이든 3sigma 든 0)
    1 = 입력·설정 오류(표본·설정 파일을 못 읽거나 문법·값이 우리 규약 밖)
    2 = 판정 불가(위로 분류되지 않은 실패)

    왜 겸용을 금지하는가: 레퍼런스 레포(jsnkle)의 검출기는 rc 로 tier 를 알렸다.
    그러자 검출기가 죽어 rc 가 0 이 아닌 값을 냈을 때 소비자 루프가 그것을
    「tier 1 = 정상」으로 읽고 초록으로 보고했다. 검출기의 죽음이 정상 신호로
    둔갑한 것이다. 그래서 여기서는 **tier 를 stdout JSON 의 필드로만** 낸다.
    소비자는 rc 로 「판정이 있었는가」만 알고, 「무엇이었는가」는 반드시 JSON 을
    읽어야 한다. rc≠0 이면 stdout 은 비어 있다 — 파싱 실패로 즉시 드러난다.

이 검출기가 재지 않는 것
    원인 · 처방 · 어떤 시험/커밋이 실패했는가 · 이탈의 중요도. 전부 사람과
    diagnose 단계의 몫이다. 검출기는 「이 숫자가 밴드 밖이다」까지만 말한다.

사용
    python3 scripts/detect_bands.py --samples <표본.jsonl> [--config ops/bands.yaml]
                                    [--format json|text]
    표본 한 줄 = {"ts": "2026-09-02T00:00:00+09:00", "value": 0.075}
"""

import argparse
import json
import statistics
import sys
from datetime import datetime

SCHEMA_VERSION = 1

# 구현한 규칙 → 그 규칙이 세우는 tier. 이 표가 「우리가 재는 어휘」의 전부다.
IMPLEMENTED_RULES = {
    "rule1_one_point_beyond_3sigma": "3sigma",
    "rule2_nine_points_one_side": "2sigma",
    "rule3_two_of_three_beyond_2sigma": "2sigma",
}
# 규칙이 보는 최신 구간의 길이.
RULE_SPAN = {
    "rule1_one_point_beyond_3sigma": 1,
    "rule2_nine_points_one_side": 9,
    "rule3_two_of_three_beyond_2sigma": 3,
}
RULE_ORDER = [
    "rule1_one_point_beyond_3sigma",
    "rule2_nine_points_one_side",
    "rule3_two_of_three_beyond_2sigma",
]
TIER_ORDER = ["none", "1sigma", "2sigma", "3sigma"]
RULE_FAMILY = "western_electric"

CONFIG_KEYS = ["metric", "baseline", "window", "min_samples",
               "min_baseline_rate", "rules", "rules_enabled", "tiers"]
TIER_KEYS = ["action", "tools", "routes"]


class InputError(Exception):
    """입력·설정 오류 — rc=1."""


# --------------------------------------------------------------------------
# YAML 부분집합 파서
#
# PyYAML 을 쓰지 않는다(stdlib 만). 대신 ops/bands.yaml 이 실제로 쓰는 문법만
# 파싱하고, 그 밖의 문법을 만나면 **에러로 죽는다**. 조용한 폴백을 두지 않는
# 이유: 레퍼런스 레포(honghu)의 검사기는 괄호·들여쓰기만 보는 폴백을 갖고
# 있었고, 그 폴백이 의미상 깨진 설정을 통과시켰다.
#
# 지원: 주석 · key: 스칼라 · key: 로 여는 중첩 매핑 · "- " 스칼라 목록 ·
#       [a, b] 흐름 목록 · 따옴표 문자열 · 정수 · 실수 · true/false · null
# 미지원(전부 에러): 탭 들여쓰기 · 앵커(&) · 별칭(*) · 태그(!) ·
#       블록 스칼라(| >) · 흐름 매핑({}) · 문서 구분자(--- ...) · 키 중복
# --------------------------------------------------------------------------

def _strip_comment(line):
    """따옴표 밖의 주석만 잘라낸다."""
    quote = None
    for i, ch in enumerate(line):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            return line[:i]
    if quote:
        raise InputError("따옴표가 닫히지 않았다: %s" % line.strip())
    return line


def _scalar(text, where):
    text = text.strip()
    if text[:1] in ("&", "*", "!", "|", ">", "{", "?"):
        raise InputError(
            "%s: 지원하지 않는 YAML 문법 %r — 이 파서는 ops/bands.yaml 이 쓰는 "
            "부분집합만 읽는다(앵커·별칭·태그·블록 스칼라·흐름 매핑 미지원)."
            % (where, text[:1]))
    if text.startswith("["):
        if not text.endswith("]"):
            raise InputError("%s: 흐름 목록이 닫히지 않았다: %s" % (where, text))
        inner = text[1:-1].strip()
        if not inner:
            return []
        return [_scalar(item, where) for item in inner.split(",")]
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        return text[1:-1]
    if text in ("null", "~"):
        return None
    if text == "true":
        return True
    if text == "false":
        return False
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        pass
    return text


def _tokenize(text, path):
    tokens = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        where = "%s:%d" % (path, lineno)
        body = _strip_comment(raw)
        if not body.strip():
            continue
        if "\t" in body[:len(body) - len(body.lstrip())]:
            raise InputError("%s: 탭 들여쓰기는 지원하지 않는다." % where)
        stripped = body.rstrip()
        if stripped.strip() in ("---", "..."):
            raise InputError("%s: 여러 문서(--- / ...)는 지원하지 않는다." % where)
        indent = len(stripped) - len(stripped.lstrip(" "))
        tokens.append((indent, stripped.strip(), where))
    return tokens


def _parse_block(tokens, i, indent, path):
    """tokens[i:] 에서 indent 수준의 블록 하나를 읽어 (값, 다음 인덱스)."""
    if tokens[i][1].startswith("- "):
        items = []
        while i < len(tokens) and tokens[i][0] == indent and tokens[i][1].startswith("- "):
            item = tokens[i][1][2:].strip()
            if ":" in item and not item.startswith(("\"", "'")):
                raise InputError(
                    "%s: 목록 항목 안의 매핑은 지원하지 않는다." % tokens[i][2])
            items.append(_scalar(item, tokens[i][2]))
            i += 1
        return items, i
    mapping = {}
    while i < len(tokens) and tokens[i][0] == indent:
        cur_indent, content, where = tokens[i]
        if content.startswith("- "):
            raise InputError("%s: 매핑 블록 안에 목록 항목이 섞였다." % where)
        if ":" not in content:
            raise InputError("%s: 'key: value' 형태가 아니다: %s" % (where, content))
        key, _, rest = content.partition(":")
        key = key.strip()
        if not key or any(c in key for c in " \"'{}[]"):
            raise InputError("%s: 지원하지 않는 키 표기: %s" % (where, content))
        if key in mapping:
            raise InputError("%s: 키가 중복됐다: %s" % (where, key))
        rest = rest.strip()
        i += 1
        if rest:
            mapping[key] = _scalar(rest, where)
            continue
        if i >= len(tokens) or tokens[i][0] <= cur_indent:
            raise InputError("%s: '%s:' 아래에 값도 블록도 없다." % (where, key))
        mapping[key], i = _parse_block(tokens, i, tokens[i][0], path)
    return mapping, i


def parse_yaml_subset(text, path):
    tokens = _tokenize(text, path)
    if not tokens:
        raise InputError("%s: 설정이 비었다." % path)
    if tokens[0][0] != 0:
        raise InputError("%s: 첫 줄이 들여쓰기돼 있다." % tokens[0][2])
    value, i = _parse_block(tokens, 0, 0, path)
    if i != len(tokens):
        raise InputError("%s: 들여쓰기 수준이 맞지 않는다." % tokens[i][2])
    return value


# --------------------------------------------------------------------------
# 설정
# --------------------------------------------------------------------------

def load_config(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        raise InputError("설정 파일을 읽을 수 없다: %s (%s)" % (path, exc))
    cfg = parse_yaml_subset(text, path)
    if not isinstance(cfg, dict):
        raise InputError("%s: 최상위가 매핑이 아니다." % path)

    unknown = [k for k in cfg if k not in CONFIG_KEYS]
    if unknown:
        raise InputError(
            "%s: 우리가 읽지 않는 설정 키 %s — 허용 키는 %s 뿐이다. "
            "읽지 않는 키를 두면 설정한 사람이 그것이 효력을 갖는 줄 안다."
            % (path, unknown, CONFIG_KEYS))
    missing = [k for k in CONFIG_KEYS if k not in cfg]
    if missing:
        raise InputError("%s: 필수 설정 키 누락 %s" % (path, missing))

    if not isinstance(cfg["metric"], str) or not cfg["metric"]:
        raise InputError("%s: metric 이 비어 있다." % path)
    for key in ("window", "min_samples"):
        if not isinstance(cfg[key], int) or isinstance(cfg[key], bool) or cfg[key] < 2:
            raise InputError("%s: %s 는 2 이상의 정수여야 한다: %r"
                             % (path, key, cfg[key]))
    rate = cfg["min_baseline_rate"]
    if isinstance(rate, bool) or not isinstance(rate, (int, float)) or rate < 0:
        raise InputError("%s: min_baseline_rate 는 0 이상의 수여야 한다: %r"
                         % (path, rate))
    baseline = cfg["baseline"]
    if not (isinstance(baseline, str) and baseline.startswith("rolling_")
            and baseline.endswith("d") and baseline[8:-1].isdigit()):
        raise InputError("%s: baseline 은 'rolling_<일수>d' 여야 한다: %r"
                         % (path, baseline))
    if int(baseline[8:-1]) != cfg["window"]:
        raise InputError(
            "%s: baseline %s 와 window %d 가 어긋난다 — 둘 중 하나는 거짓말이다."
            % (path, baseline, cfg["window"]))
    if cfg["rules"] != RULE_FAMILY:
        raise InputError(
            "%s: rules 계열 %r 을 구현하지 않았다 — 아는 것은 %r 뿐이다."
            % (path, cfg["rules"], RULE_FAMILY))
    enabled = cfg["rules_enabled"]
    if not isinstance(enabled, list) or not enabled:
        raise InputError("%s: rules_enabled 가 비었다." % path)
    unimplemented = [r for r in enabled if r not in IMPLEMENTED_RULES]
    if unimplemented:
        raise InputError(
            "%s: 구현하지 않은 규칙을 요구했다 %s — 구현한 것은 %s 뿐이다. "
            "조용히 건너뛰면 설정이 약속한 검출이 없는 채로 초록이 된다."
            % (path, unimplemented, sorted(IMPLEMENTED_RULES)))
    tiers = cfg["tiers"]
    if not isinstance(tiers, dict) or not tiers:
        raise InputError("%s: tiers 가 비었다." % path)
    for name, spec in tiers.items():
        if name not in TIER_ORDER[1:]:
            raise InputError("%s: 모르는 tier 이름 %r — %s 뿐이다."
                             % (path, name, TIER_ORDER[1:]))
        if not isinstance(spec, dict) or "action" not in spec:
            raise InputError("%s: tier %s 에 action 이 없다." % (path, name))
        extra = [k for k in spec if k not in TIER_KEYS]
        if extra:
            raise InputError("%s: tier %s 의 모르는 키 %s — 허용 키는 %s."
                             % (path, name, extra, TIER_KEYS))
    needed = set(IMPLEMENTED_RULES[r] for r in enabled) | {"1sigma"}
    absent = sorted(t for t in needed if t not in tiers)
    if absent:
        raise InputError(
            "%s: 활성 규칙이 세울 수 있는 tier %s 의 정의가 없다 — "
            "판정은 나는데 행동이 없는 자리가 생긴다." % (path, absent))
    return cfg


# --------------------------------------------------------------------------
# 표본
# --------------------------------------------------------------------------

def _parse_ts(text, where):
    if not isinstance(text, str):
        raise InputError("%s: ts 가 문자열이 아니다: %r" % (where, text))
    raw = text[:-1] + "+00:00" if text.endswith("Z") else text
    try:
        stamp = datetime.fromisoformat(raw)
    except ValueError:
        raise InputError("%s: ts 가 ISO8601 이 아니다: %r" % (where, text))
    if stamp.utcoffset() is None:
        raise InputError("%s: ts 에 시간대 오프셋이 없다: %r — "
                         "오프셋 없는 시각은 다른 기계에서 다른 뜻이 된다."
                         % (where, text))
    return stamp


def load_samples(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except OSError as exc:
        raise InputError("표본 파일을 읽을 수 없다: %s (%s)" % (path, exc))
    samples = []
    for lineno, raw in enumerate(lines, 1):
        if not raw.strip():
            continue
        where = "%s:%d (%d번째 줄)" % (path, lineno, lineno)
        try:
            row = json.loads(raw)
        except ValueError as exc:
            raise InputError("%s: JSON 이 아니다 — %s" % (where, exc))
        if not isinstance(row, dict):
            raise InputError("%s: 객체가 아니다." % where)
        for key in ("ts", "value"):
            if key not in row:
                raise InputError("%s: 필수 필드 %r 이 없다." % (where, key))
        value = row["value"]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise InputError("%s: value 가 수가 아니다: %r" % (where, value))
        samples.append({"ts": row["ts"], "value": float(value),
                        "_at": _parse_ts(row["ts"], where)})
    if not samples:
        raise InputError("%s: 표본이 한 줄도 없다." % path)
    samples.sort(key=lambda s: s["_at"])
    return samples


# --------------------------------------------------------------------------
# 판정
# --------------------------------------------------------------------------

def _point(sample):
    return {"ts": sample["ts"], "value": sample["value"]}


def evaluate(samples, cfg):
    """설정과 표본으로 판정 결과 딕셔너리를 만든다(부작용 없음 · 모델 미개입)."""
    enabled = [r for r in RULE_ORDER if r in cfg["rules_enabled"]]
    span = max(RULE_SPAN[r] for r in enabled)
    baseline = samples[:-span][-cfg["window"]:]
    tail = samples[-span:]
    values = [s["value"] for s in baseline]
    observed = samples[-1]

    result = {
        "schema_version": SCHEMA_VERSION,
        "metric": cfg["metric"],
        "detected_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "tier": "none",
        "action": None,
        "rule": None,
        "rules_fired": [],
        "reason": None,
        "z": None,
        "mean": None,
        "sigma": None,
        "n": len(baseline),
        "observed": _point(observed),
        "evidence": {
            "window_size": len(baseline),
            "window": [_point(s) for s in baseline],
            "evaluated": [_point(s) for s in tail],
            "rules_enabled": enabled,
            "config": {
                "window": cfg["window"],
                "min_samples": cfg["min_samples"],
                "min_baseline_rate": cfg["min_baseline_rate"],
            },
        },
    }

    # 가드 1 — 기준선이 부족하면 판정하지 않는다.
    if len(baseline) < cfg["min_samples"]:
        result["reason"] = "insufficient_samples"
        if len(values) >= 2:
            result["mean"] = statistics.mean(values)
            result["sigma"] = statistics.stdev(values)
        return result

    mean = statistics.mean(values)
    sigma = statistics.stdev(values)   # 표본 표준편차(n-1)
    result["mean"] = mean
    result["sigma"] = sigma

    # 가드 2 — σ=0 (기준선이 전부 같은 값). 이 가드가 없으면 값 하나만 달라도
    # z 가 무한대가 돼 즉시 3σ 로 튄다(레퍼런스 레포 imsungbin 의 모서리).
    # 순서가 중요하다: 아래 min_baseline_rate 가드보다 **먼저** 판정한다 —
    # 전부 0 인 기준선은 두 가드에 다 걸리는데, 그때 reason 이 무엇이냐로
    # 「σ=0 가드가 살아 있는가」를 시험이 잰다.
    if sigma == 0:
        result["reason"] = "zero_sigma_baseline"
        return result

    # 가드 3 — 기준선 자체가 너무 낮아 밴드가 의미를 잃는 구간.
    if mean < cfg["min_baseline_rate"]:
        result["reason"] = "baseline_below_min_rate"
        return result

    def z_of(sample):
        return (sample["value"] - mean) / sigma

    z_last = z_of(observed)
    result["z"] = z_last

    fired = []
    if "rule1_one_point_beyond_3sigma" in enabled:
        if abs(z_last) > 3.0:
            fired.append("rule1_one_point_beyond_3sigma")
    if "rule2_nine_points_one_side" in enabled:
        last9 = tail[-9:]
        if len(last9) == 9 and (all(s["value"] > mean for s in last9)
                                or all(s["value"] < mean for s in last9)):
            fired.append("rule2_nine_points_one_side")
    if "rule3_two_of_three_beyond_2sigma" in enabled:
        last3 = tail[-3:]
        if len(last3) == 3:
            above = sum(1 for s in last3 if z_of(s) > 2.0)
            below = sum(1 for s in last3 if z_of(s) < -2.0)
            if above >= 2 or below >= 2:
                fired.append("rule3_two_of_three_beyond_2sigma")

    result["rules_fired"] = fired
    if fired:
        tier = max((IMPLEMENTED_RULES[r] for r in fired), key=TIER_ORDER.index)
        result["tier"] = tier
        result["rule"] = next(r for r in fired if IMPLEMENTED_RULES[r] == tier)
    elif abs(z_last) >= 1.0:
        result["tier"] = "1sigma"

    if result["tier"] != "none":
        spec = cfg["tiers"][result["tier"]]
        result["action"] = spec["action"]
        for key in ("tools", "routes"):
            if key in spec:
                result[key] = spec[key]
    return result


def render_text(result):
    return (
        "metric=%s tier=%s action=%s rule=%s z=%s n=%d mean=%s sigma=%s reason=%s\n"
        % (result["metric"], result["tier"], result["action"],
           result["rule"], _fmt(result["z"]), result["n"],
           _fmt(result["mean"]), _fmt(result["sigma"]), result["reason"]))


def _fmt(value):
    return "none" if value is None else "%.6f" % value


class _Parser(argparse.ArgumentParser):
    """argparse 의 사용법 오류도 rc=1(입력 오류)로 낸다 — rc=2 와 섞지 않는다."""

    def error(self, message):
        self.exit(1, "%s: 인자 오류: %s\n" % (self.prog, message))


def main(argv=None):
    parser = _Parser(description="Stage 6 결정론 밴드 검출기(모델 미개입)")
    parser.add_argument("--samples", required=True, help="표본 jsonl 경로")
    parser.add_argument("--config", default="ops/bands.yaml", help="밴드 설정 경로")
    parser.add_argument("--format", default="json", choices=["json", "text"])
    args = parser.parse_args(argv)

    try:
        cfg = load_config(args.config)
        samples = load_samples(args.samples)
        result = evaluate(samples, cfg)
    except InputError as exc:
        sys.stderr.write("입력·설정 오류: %s\n" % exc)
        return 1
    except Exception as exc:                       # 분류하지 못한 실패
        sys.stderr.write("판정 불가: %s: %s\n" % (type(exc).__name__, exc))
        return 2

    if args.format == "json":
        sys.stdout.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    else:
        sys.stdout.write(render_text(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
