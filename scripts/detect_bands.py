#!/usr/bin/env python3
"""scripts/detect_bands.py — Stage 6 결정론 밴드 검출기 (레슨 14).

L14 1030행: "mean and standard deviation over a rolling window with rules
(Western Electric or similar) ... detection stays entirely deterministic,
with no model involved." L14 1036~1038행: 1sigma→log 2sigma→diagnose
3sigma→propose. 규칙은 최신 점에서 끝나는 구간만 본다; 기준선 창은 그 꼬리를
제외한다(포함하면 이동이 자기 평균을 끌어올린다).

rc: 0=판정 성공(tier 는 stdout JSON 필드로만 — rc 가 tier 를 겸하면 검출기
죽음이 "정상" tier 로 오독된다) 1=입력·설정 오류 2=판정 불가.
"""
import argparse, json, re, statistics, sys
from datetime import datetime

RULES = {"rule1_one_point_beyond_3sigma": ("3sigma", 1),
         "rule2_nine_points_one_side": ("2sigma", 9),
         "rule3_two_of_three_beyond_2sigma": ("2sigma", 3)}
TIER_ORDER = ["none", "1sigma", "2sigma", "3sigma"]


class InputError(Exception):
    """입력·설정 오류 — rc=1."""


def load_config(path):
    """ops/bands.yaml 은 고정 모양이라 PyYAML 대신 그 모양만 정규식으로 읽는다."""
    try:
        text = re.sub(r"#.*", "", open(path, encoding="utf-8").read())
    except OSError as exc:
        raise InputError("설정을 읽을 수 없다: %s (%s)" % (path, exc))
    field = lambda name, cast, dflt: cast(m.group(1)) if (
        m := re.search(r"^%s:\s*(\S+)" % name, text, re.M)) else dflt
    cfg = {"metric": field("metric", str, "unknown"), "window": field("window", int, 0),
           "min_samples": field("min_samples", int, 0), "rules": field("rules", str, ""),
           "min_baseline_rate": field("min_baseline_rate", float, 0.0), "tiers": {}}
    blk = re.search(r"rules_enabled:\n((?:\s+-\s+\S+\n?)+)", text)
    cfg["rules_enabled"] = re.findall(r"-\s+(\S+)", blk.group(1)) if blk else []
    for tier in TIER_ORDER[1:]:
        m = re.search(r"^  %s:\n((?:    .+\n?)+)" % tier, text, re.M)
        if not m:
            continue
        body = m.group(1)
        am, tm, rm = (re.search(p, body) for p in
                      (r"action:\s*(\S+)", r'tools:\s*"([^"]+)"', r"routes:\s*\[([^\]]*)\]"))
        cfg["tiers"][tier] = {k: v for k, v in {
            "action": am and am.group(1), "tools": tm and tm.group(1),
            "routes": rm and [x.strip() for x in rm.group(1).split(",") if x.strip()]}.items()
            if v is not None}
    if cfg["rules"] != "western_electric":
        raise InputError("%s: rules 계열 %r 을 구현하지 않았다 — 아는 것은 'western_electric' 뿐이다."
                         % (path, cfg["rules"]))
    if cfg["window"] < 2 or cfg["min_samples"] < 2:
        raise InputError("%s: window/min_samples 는 2 이상이어야 한다: %r/%r"
                         % (path, cfg["window"], cfg["min_samples"]))
    bad = [x for x in cfg["rules_enabled"] if x not in RULES]
    if bad:
        raise InputError("%s: 구현하지 않은 규칙 %s — 아는 것은 %s 뿐이다."
                         % (path, bad, sorted(RULES)))
    needed = {RULES[x][0] for x in cfg["rules_enabled"]} | {"1sigma"}
    absent = sorted(t for t in needed if "action" not in cfg["tiers"].get(t, {}))
    if absent:
        raise InputError("%s: tier %s 의 행동 정의가 없다." % (path, absent))
    return cfg


def load_samples(path):
    try:
        rows = [l for l in open(path, encoding="utf-8") if l.strip()]
    except OSError as exc:
        raise InputError("표본을 읽을 수 없다: %s (%s)" % (path, exc))
    out = []
    for i, raw in enumerate(rows, 1):
        try:
            row = json.loads(raw)
            ts = row["ts"][:-1] + "+00:00" if row["ts"].endswith("Z") else row["ts"]
            at, value = datetime.fromisoformat(ts), row["value"]
            if at.utcoffset() is None:
                raise ValueError("ts 에 시간대 오프셋이 없다")
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError("value 가 수가 아니다")
        except (ValueError, KeyError, TypeError) as exc:
            raise InputError("%s:%d: %s" % (path, i, exc))
        out.append({"ts": row["ts"], "value": float(value), "_at": at})
    if not out:
        raise InputError("%s: 표본이 한 줄도 없다." % path)
    out.sort(key=lambda s: s["_at"])
    return out


def evaluate(samples, cfg):
    """부작용 없음 · 모델 미개입 — 판정은 순수 함수."""
    enabled = [x for x in RULES if x in cfg["rules_enabled"]]
    span = max(RULES[x][1] for x in enabled)
    baseline, tail, obs = samples[:-span][-cfg["window"]:], samples[-span:], samples[-1]
    pt = lambda s: {"ts": s["ts"], "value": s["value"]}
    r = {"schema_version": 1, "metric": cfg["metric"],
         "detected_at": datetime.now().astimezone().isoformat(timespec="seconds"),
         "tier": "none", "action": None, "rule": None, "rules_fired": [], "reason": None,
         "z": None, "mean": None, "sigma": None, "n": len(baseline), "observed": pt(obs),
         "evidence": {"window": [pt(s) for s in baseline], "evaluated": [pt(s) for s in tail],
                      "rules_enabled": enabled, "config": {k: cfg[k] for k in
                      ("window", "min_samples", "min_baseline_rate")}}}
    if len(baseline) < cfg["min_samples"]:
        r["reason"] = "insufficient_samples"
        return r
    values = [s["value"] for s in baseline]
    mean, sigma = statistics.mean(values), statistics.stdev(values)
    r["mean"], r["sigma"] = mean, sigma
    if sigma == 0:
        r["reason"] = "zero_sigma_baseline"
        return r
    if mean < cfg["min_baseline_rate"]:
        r["reason"] = "baseline_below_min_rate"
        return r
    z = lambda s: (s["value"] - mean) / sigma
    z_last = r["z"] = z(obs)
    fired, last9, last3 = [], tail[-9:], tail[-3:]
    if "rule1_one_point_beyond_3sigma" in enabled and abs(z_last) > 3.0:
        fired.append("rule1_one_point_beyond_3sigma")
    if "rule2_nine_points_one_side" in enabled and len(last9) == 9 and (
            all(s["value"] > mean for s in last9) or all(s["value"] < mean for s in last9)):
        fired.append("rule2_nine_points_one_side")
    if "rule3_two_of_three_beyond_2sigma" in enabled and len(last3) == 3 and (
            sum(1 for s in last3 if z(s) > 2.0) >= 2 or sum(1 for s in last3 if z(s) < -2.0) >= 2):
        fired.append("rule3_two_of_three_beyond_2sigma")
    r["rules_fired"] = fired
    if fired:
        tier = max((RULES[x][0] for x in fired), key=TIER_ORDER.index)
        r["tier"], r["rule"] = tier, next(x for x in fired if RULES[x][0] == tier)
    elif abs(z_last) >= 1.0:
        r["tier"] = "1sigma"
    if r["tier"] != "none":
        spec = cfg["tiers"][r["tier"]]
        r["action"] = spec["action"]
        r.update({k: spec[k] for k in ("tools", "routes") if k in spec})
    return r


def main(argv=None):
    class P(argparse.ArgumentParser):
        def error(self, message):
            self.exit(1, "%s: 인자 오류: %s\n" % (self.prog, message))
    p = P(description="Stage 6 결정론 밴드 검출기(모델 미개입)")
    p.add_argument("--samples", required=True)
    p.add_argument("--config", default="ops/bands.yaml")
    args = p.parse_args(argv)
    try:
        res = evaluate(load_samples(args.samples), load_config(args.config))
    except InputError as exc:
        sys.stderr.write("입력·설정 오류: %s\n" % exc)
        return 1
    except Exception as exc:
        sys.stderr.write("판정 불가: %s: %s\n" % (type(exc).__name__, exc))
        return 2
    sys.stdout.write(json.dumps(res, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
