#!/usr/bin/env python3
"""scripts/emit_intent.py — 검출 결과 → Stage 1 intent 초안 (레슨 14).

L14 1036행: "The agent writes its diagnosis as intent.md in the Stage 1:
Plan format, covering the anomaly and its evidence, a proposed outcome,
the affected systems, and any open questions."

templates/intent.md(레인 B 소유)을 읽어 frontmatter 키·섹션 제목 순서를
가져온다 — 하드코딩하면 템플릿이 바뀔 때 조용히 어긋난다. tier none/1sigma 는
초안을 만들지 않는다(행동이 log 뿐). status 는 언제나 draft.
"""
import argparse, json, os, re, sys

WRITE_TIERS = ("2sigma", "3sigma")
TEMPLATE = os.path.join(os.path.dirname(__file__), "..", "templates", "intent.md")


class InputError(Exception):
    """입력 오류 — rc=1."""


def load_template():
    text = open(TEMPLATE, encoding="utf-8").read()
    return (re.findall(r"^([a-z_]+):", text.split("---")[1], re.M),
            re.findall(r"^## (.+)$", text, re.M))


def load_detection(path):
    text = open(path, encoding="utf-8").read() if path else sys.stdin.read()
    try:
        data = json.loads(text)
    except ValueError as exc:
        raise InputError("검출 결과가 JSON 이 아니다 — %s" % exc)
    if data.get("tier") not in ("none", "1sigma", "2sigma", "3sigma"):
        raise InputError("detect_bands.py 의 출력이 아니다(tier 필드 없음/모름).")
    return data


def render(d, intent_id, keys, heads):
    vals = {"id": intent_id, "kind": "intent", "status": "draft",
            "author": "detect_bands (자동)", "created": d["detected_at"],
            "record": "none", "supersedes": "none"}
    front = ["---"] + ["%s: %s" % (k, vals.get(k, "none")) for k in keys] + ["---"]
    body = {
        heads[0]: "`%s` 최신 표본 %s=%s 이 규칙 `%s` 로 tier `%s` 를 냈다 (n=%s mean=%s sigma=%s z=%s)."
                  % (d["metric"], d["observed"]["ts"], d["observed"]["value"], d["rule"],
                     d["tier"], d["n"], d["mean"], d["sigma"], d["z"]),
        heads[1]: "`%s` 가 기준선 안으로 돌아오고, 행동 `%s` 가 이 초안으로 이행됐다."
                  % (d["metric"], d["action"]),
        heads[2]: "지표 `%s` 를 생산하는 CI 와 그 지표로 머지를 판단하는 사람 전부." % d["metric"],
        heads[3]: "- C1 status 는 draft — accepted 전엔 하류(spec·plan)를 시작하지 않는다.\n"
                  "- C2 원인·처방은 여기 없다 — diagnose 단계의 몫이다.",
        heads[4]: "- Q1 이탈이 코드 변경 때문인지 인프라 변동 때문인지 diagnose 단계가 답한다.",
    }
    out = front + ["# Intent: %s 밴드 이탈 (%s · %s)" % (d["metric"], d["tier"], d["rule"]), ""]
    for h in heads:
        out += ["## " + h, "", body.get(h, "‹자동 미채움 — 사람이 채운다›"), ""]
    return "\n".join(out)


def main(argv=None):
    class P(argparse.ArgumentParser):
        def error(self, message):
            self.exit(1, "%s: 인자 오류: %s\n" % (self.prog, message))
    p = P(description="검출 결과 → Stage 1 intent 초안")
    p.add_argument("--input", default=None)
    p.add_argument("--id", required=True, dest="intent_id")
    p.add_argument("--out", required=True)
    args = p.parse_args(argv)
    try:
        data = load_detection(args.input)
    except InputError as exc:
        sys.stderr.write("입력 오류: %s\n" % exc)
        return 1
    if data["tier"] not in WRITE_TIERS:
        print(json.dumps({"status": "skipped", "tier": data["tier"]}))
        return 0
    keys, heads = load_template()
    target = os.path.join(args.out, args.intent_id, "intent.md")
    try:
        os.makedirs(os.path.dirname(target), exist_ok=True)
        open(target, "w", encoding="utf-8").write(render(data, args.intent_id, keys, heads))
    except OSError as exc:
        sys.stderr.write("초안을 쓸 수 없다: %s (%s)\n" % (target, exc))
        return 2
    print(json.dumps({"status": "written", "written": target, "tier": data["tier"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
