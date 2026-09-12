#!/usr/bin/env python3
"""L10 727: "runs are logged so results can be compared over time".

Record generator envelopes and both grading results; undecidable cases stay
in the pass-rate denominator. This module never approves an artifact.
"""
import argparse
import json
from pathlib import Path
import sys


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize(args):
    events = [json.loads(line) for line in Path(args.trace).read_text(encoding="utf-8").splitlines()
              if line.strip()]
    if not events or not all(isinstance(event, dict) for event in events):
        raise ValueError("generator trace must contain JSON objects")
    results = [event for event in events if event.get("type") == "result"]
    if len(results) != 1:
        raise ValueError("generator trace must contain exactly one final result")
    result = results[0]
    if result.get("subtype") != "success" or result.get("is_error") is not False:
        raise ValueError("generator returned an unsuccessful result")
    if not isinstance(result.get("result"), str):
        raise ValueError("generator result text is missing")
    case = read_json(args.case)
    write_json(args.out, {"schema_version": 1, "case_id": case["id"],
                          "workspace": args.workspace, "result": result["result"],
                          "claude_raw": result})
    return 0


def status(rc):
    return {0: "pass", 1: "fail", 2: "undecidable"}[rc]


def record_case(args):
    codes = (args.generation_rc, args.deterministic_rc, args.semantic_rc)
    rc = max(code if code in (0, 1, 2) else 2 for code in codes)
    if args.generation_rc != 0:
        rc = 2
    write_json(args.out, {"schema_version": 1, "edition": args.edition,
                          "case_id": args.case_id,
                          "generation_rc": args.generation_rc,
                          "deterministic_rc": args.deterministic_rc,
                          "semantic_rc": args.semantic_rc,
                          "status": status(rc), "rc": rc,
                          "model": "sonnet", "effort": "low"})
    return 0


def summarize(args):
    cases = []
    for path in args.cases:
        cid = read_json(path)["id"]
        try:
            result = read_json(Path(args.out_dir) / (cid + ".status.json"))
            if result.get("case_id") != cid or result.get("edition") != args.edition or \
                    result.get("rc") not in (0, 1, 2):
                raise ValueError("invalid case status")
        except (OSError, ValueError, AttributeError):
            result = {"case_id": cid, "rc": 2, "status": "undecidable",
                      "error": "case status missing or invalid"}
        cases.append(result)
    if not cases:
        raise ValueError("no cases were selected")
    counts = {name: sum(case["rc"] == rc for case in cases)
              for rc, name in enumerate(("pass", "fail", "undecidable"))}
    rc = max(case["rc"] for case in cases)
    summary = {"schema_version": 1, "mode": "semantic", "edition": args.edition,
               "cases": cases,
               "total": len(cases), "counts": counts,
               "pass_rate": counts["pass"] / len(cases),
               "status": status(rc), "rc": rc}
    target = Path(args.out_dir) / "summary.json"
    write_json(target, summary)
    print("evals: %s; %d passed, %d failed, %d undecidable; summary=%s" %
          (status(rc), counts["pass"], counts["fail"], counts["undecidable"], target))
    return rc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("normalize")
    for key in ("case", "workspace", "trace", "out"):
        p.add_argument("--" + key, required=True)
    p.set_defaults(fn=normalize)
    p = sub.add_parser("case")
    p.add_argument("--case-id", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--edition", choices=("tdd-first", "tdd-optional"),
                   default="tdd-first")
    for key in ("generation-rc", "deterministic-rc", "semantic-rc"):
        p.add_argument("--" + key, required=True, type=int)
    p.set_defaults(fn=record_case)
    p = sub.add_parser("summary")
    p.add_argument("--edition", choices=("tdd-first", "tdd-optional"),
                   default="tdd-first")
    p.add_argument("--out-dir", required=True)
    p.add_argument("--cases", required=True, nargs="+")
    p.set_defaults(fn=summarize)
    args = parser.parse_args()
    try:
        return args.fn(args)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("UNDECIDABLE: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
