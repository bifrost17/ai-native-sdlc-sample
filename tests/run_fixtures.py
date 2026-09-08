#!/usr/bin/env python3
"""tests/run_fixtures.py — 픽스처 묶음을 돌려 PASS/FAIL 한 줄씩 찍는다.

게이트(`scripts/check_all.sh`)와 사람이 같은 명령을 쓴다:
    python3 tests/run_fixtures.py --set red
    python3 tests/run_fixtures.py --set green
    python3 tests/run_fixtures.py --set all --fixture fence-forged-status

red 는 EXPECT 의 code 다중집합과 **정확히** 같아야 통과다 — 「red 이기만 하면 됨」은
통과가 아니다(엉뚱한 이유로 빨간 픽스처는 그 축을 재지 못한다).
green 은 error·undecidable 이 0건이어야 통과다.
rc: 0 전부 통과 / 1 하나라도 어긋남 / 2 픽스처 자체가 고장(계기 고장).
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fixture_harness import FixtureError, format_detail, run_fixture  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, "fixtures")


def discover(which):
    sets = ["red", "green"] if which == "all" else [which]
    found = []
    for name in sets:
        base = os.path.join(FIXTURES, name)
        if not os.path.isdir(base):
            continue
        for entry in sorted(os.listdir(base)):
            path = os.path.join(base, entry)
            if os.path.isdir(path):
                found.append((name, entry, path))
    return found


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--set", dest="which", choices=["red", "green", "all"], default="all")
    parser.add_argument("--fixture", help="이름 하나만 돌린다")
    args = parser.parse_args(argv)

    fixtures = discover(args.which)
    if args.fixture:
        fixtures = [f for f in fixtures if f[1] == args.fixture]
    if not fixtures:
        print("픽스처를 하나도 찾지 못했다 — 계기 고장이다", file=sys.stderr)
        return 2

    passed = failed = 0
    broken = 0
    for kind, name, path in fixtures:
        try:
            ok, detail = run_fixture(path)
        except FixtureError as exc:
            print("BROKEN %s/%s" % (kind, name))
            print("  %s" % exc)
            broken += 1
            continue
        if ok:
            print("PASS   %s/%s  (%s)" % (kind, name, ", ".join(detail["codes"]) or "code 없음"))
            passed += 1
        else:
            print("FAIL   %s/%s" % (kind, name))
            print(format_detail(name, detail))
            failed += 1

    print("")
    print("%d passed, %d failed, %d broken" % (passed, failed, broken))
    if broken:
        return 2
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
