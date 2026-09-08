"""scripts/detect_bands.py · scripts/emit_intent.py 단위 시험 (stdlib · unittest).

두 스크립트를 **서브프로세스로** 돌린다. 이유는 두 가지다:
  1. rc 계약(0/1/2)은 프로세스 종료 코드로만 잴 수 있다. import 해서 함수를 부르면
     계약이 아니라 구현을 재게 된다.
  2. 뮤테이션(파일을 일부러 깨서 red 를 확인)이 정말 대상 파일을 읽는지 보장된다
     — in-process import 는 캐시된 모듈을 읽어 변조본을 못 볼 수 있다.

표본·설정 픽스처는 tests/data/bands/ 에 있고, 그 디렉터리의 README.md 에
기준선 통계(mean 0.050125 · sigma 0.003837)를 `statistics` 모듈로 독립 계산해 적어 뒀다.
여기 단정에 쓰는 기대값은 그 독립 계산에서 왔지 검출기 출력에서 오지 않았다.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DETECT = ROOT / "scripts" / "detect_bands.py"
EMIT = ROOT / "scripts" / "emit_intent.py"
CONFIG = ROOT / "ops" / "bands.yaml"
DATA = ROOT / "tests" / "data" / "bands"

# tests/data/bands/README.md 의 독립 계산값
BASELINE_MEAN = 0.050125
BASELINE_SIGMA = 0.003837


def run_detect(samples, config=None, fmt="json", extra=None):
    """검출기를 돌리고 (rc, stdout, stderr) 를 준다."""
    cmd = [sys.executable, str(DETECT), "--samples", str(samples),
           "--config", str(config or CONFIG), "--format", fmt]
    if extra:
        cmd += list(extra)
    p = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def detect_json(samples, config=None):
    """rc=0 을 단정하고 stdout JSON 을 준다."""
    rc, out, err = run_detect(samples, config=config)
    assert rc == 0, "rc=%d 기대 0 · stderr=%s" % (rc, err)
    return json.loads(out)


def run_emit(argv, stdin_text=None):
    cmd = [sys.executable, str(EMIT)] + list(argv)
    p = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True,
                       input=stdin_text)
    return p.returncode, p.stdout, p.stderr


class DetectorJudgementTest(unittest.TestCase):
    """① ~ ⑥ · 규칙별 판정과 가드."""

    def test_01_normal_series_is_tier_none(self):
        """정상 변동은 tier none — 규칙 0건, reason 없음."""
        r = detect_json(DATA / "normal.jsonl")
        self.assertEqual(r["tier"], "none")
        self.assertEqual(r["rules_fired"], [])
        self.assertIsNone(r["rule"])
        self.assertIsNone(r["reason"])
        self.assertAlmostEqual(r["mean"], BASELINE_MEAN, places=6)
        self.assertAlmostEqual(r["sigma"], BASELINE_SIGMA, places=6)
        self.assertAlmostEqual(r["z"], -0.554, places=3)

    def test_02_one_point_beyond_3sigma_is_rule1_and_3sigma(self):
        """1점이 3σ 밖 → 규칙1 · tier 3sigma · action 은 설정의 propose."""
        r = detect_json(DATA / "spike-3sigma.jsonl")
        self.assertEqual(r["tier"], "3sigma")
        self.assertEqual(r["rule"], "rule1_one_point_beyond_3sigma")
        self.assertIn("rule1_one_point_beyond_3sigma", r["rules_fired"])
        self.assertEqual(r["action"], "propose")
        self.assertEqual(r["routes"], ["pull_request"])
        self.assertAlmostEqual(r["z"], 6.483, places=3)

    def test_03_nine_points_one_side_is_rule2(self):
        """연속 9점이 한쪽 → 규칙2. 1점 3σ 도 2σ 2/3 도 아닌데 잡혀야 한다(느린 드리프트)."""
        r = detect_json(DATA / "run-of-9.jsonl")
        self.assertEqual(r["rules_fired"], ["rule2_nine_points_one_side"])
        self.assertEqual(r["rule"], "rule2_nine_points_one_side")
        self.assertEqual(r["tier"], "2sigma")
        self.assertEqual(r["action"], "diagnose")
        self.assertLess(abs(r["z"]), 3.0)

    def test_04_two_of_three_beyond_2sigma_is_rule3(self):
        """최근 3점 중 2점이 같은 쪽 2σ 밖 → 규칙3 · tier 2sigma."""
        r = detect_json(DATA / "two-of-three.jsonl")
        self.assertEqual(r["rules_fired"], ["rule3_two_of_three_beyond_2sigma"])
        self.assertEqual(r["rule"], "rule3_two_of_three_beyond_2sigma")
        self.assertEqual(r["tier"], "2sigma")
        self.assertLess(abs(r["z"]), 3.0)

    def test_05_zero_sigma_flat_baseline_is_guarded(self):
        """기준선이 전부 같아 σ=0 이면 즉시 3σ 로 튀지 않는다(imsungbin 의 모서리).

        평균 0.050 은 min_baseline_rate(0.02) 위라 **σ=0 가드만** 이 케이스를 잡는다.
        """
        r = detect_json(DATA / "zero-sigma-flat.jsonl")
        self.assertEqual(r["tier"], "none")
        self.assertEqual(r["reason"], "zero_sigma_baseline")
        self.assertNotEqual(r["tier"], "3sigma")
        self.assertIsNone(r["z"])
        self.assertEqual(r["sigma"], 0.0)

    def test_06_all_zero_baseline_with_one_failure_is_guarded(self):
        """전부 0 인 기준선 + 1건 실패 → 3sigma 가 아니라 가드 + reason.

        두 가드가 모두 참인 입력이라 **순서**를 잰다 — σ=0 가드가 먼저다.
        """
        r = detect_json(DATA / "all-zero-baseline.jsonl")
        self.assertNotEqual(r["tier"], "3sigma")
        self.assertEqual(r["tier"], "none")
        self.assertEqual(r["reason"], "zero_sigma_baseline")

    def test_07_insufficient_samples_is_none_with_reason(self):
        """표본 부족 → tier none + reason insufficient_samples."""
        r = detect_json(DATA / "too-few.jsonl")
        self.assertEqual(r["tier"], "none")
        self.assertEqual(r["reason"], "insufficient_samples")
        self.assertLess(r["n"], 20)

    def test_08_one_sigma_drift_is_logged_not_proposed(self):
        """규칙은 안 걸리고 |z|≥1 이면 tier 1sigma(action log)."""
        r = detect_json(DATA / "drift-1sigma.jsonl")
        self.assertEqual(r["tier"], "1sigma")
        self.assertEqual(r["rules_fired"], [])
        self.assertEqual(r["action"], "log")
        self.assertAlmostEqual(r["z"], 1.531, places=3)

    def test_09_baseline_window_is_truncated_to_window(self):
        """기준선은 창 크기(30)로 잘린다 — 그보다 오래된 표본은 안 본다."""
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "long.jsonl"
            cycle = [0.048, 0.052, 0.046, 0.054, 0.050, 0.056, 0.044, 0.051]
            values = (cycle * 7)[:50] + cycle[:8] + [0.048]
            lines = []
            for i, v in enumerate(values):
                lines.append(json.dumps(
                    {"ts": "2026-06-%02dT00:00:00+09:00" % (i % 28 + 1), "value": v}))
            p.write_text("\n".join(lines) + "\n")
            r = detect_json(p)
        self.assertEqual(r["n"], 30)
        self.assertEqual(len(r["evidence"]["window"]), 30)


class DetectorContractTest(unittest.TestCase):
    """⑦ ⑧ ⑨ · rc 계약과 출력 스키마."""

    def test_10_unimplemented_rule_in_config_exits_1(self):
        """설정이 미구현 규칙을 요구하면 rc=1 로 죽는다 — 조용히 건너뛰지 않는다."""
        rc, out, err = run_detect(DATA / "normal.jsonl",
                                  config=DATA / "config-unimplemented-rule.yaml")
        self.assertEqual(rc, 1)
        self.assertIn("rule4_four_of_five_beyond_1sigma", err)

    def test_11_unsupported_yaml_syntax_exits_1(self):
        """파싱 못 하는 YAML 문법은 폴백이 아니라 rc=1 이다(honghu 실사고)."""
        rc, out, err = run_detect(DATA / "normal.jsonl",
                                  config=DATA / "config-unsupported-syntax.yaml")
        self.assertEqual(rc, 1)
        self.assertEqual(out, "")

    def test_12_unknown_rule_family_exits_1(self):
        rc, out, err = run_detect(DATA / "normal.jsonl",
                                  config=DATA / "config-unknown-family.yaml")
        self.assertEqual(rc, 1)
        self.assertIn("nelson", err)

    def test_13_broken_jsonl_exits_1(self):
        rc, out, err = run_detect(DATA / "broken.jsonl")
        self.assertEqual(rc, 1)
        self.assertEqual(out, "")
        self.assertIn("4", err)  # 몇 번째 줄인지 말한다

    def test_14_bad_value_type_exits_1(self):
        rc, out, err = run_detect(DATA / "bad-value-type.jsonl")
        self.assertEqual(rc, 1)

    def test_15_missing_samples_file_exits_1(self):
        rc, out, err = run_detect(DATA / "does-not-exist.jsonl")
        self.assertEqual(rc, 1)

    def test_16_rc_is_independent_of_tier(self):
        """⑨ rc 는 tier 를 겸하지 않는다 — 3σ 여도 rc=0.

        jsnkle 의 실사고: 검출기가 rc 로 tier 를 알리자, 검출기가 죽었을 때(rc≠0)
        소비자가 그것을 「tier 1 정상」으로 읽고 초록으로 보고했다.
        """
        rc_hi, out_hi, _ = run_detect(DATA / "spike-3sigma.jsonl")
        rc_lo, out_lo, _ = run_detect(DATA / "normal.jsonl")
        self.assertEqual(rc_hi, 0)
        self.assertEqual(rc_lo, 0)
        self.assertEqual(json.loads(out_hi)["tier"], "3sigma")
        self.assertEqual(json.loads(out_lo)["tier"], "none")
        # tier 가 달라도 rc 는 같다 — tier 는 stdout 의 필드에서만 읽힌다
        self.assertEqual(rc_hi, rc_lo)

    def test_17_output_has_all_schema_fields(self):
        r = detect_json(DATA / "spike-3sigma.jsonl")
        for key in ("schema_version", "metric", "tier", "rule", "z", "mean",
                    "sigma", "n", "action", "evidence", "detected_at",
                    "rules_fired", "reason", "observed"):
            self.assertIn(key, r)
        self.assertEqual(r["metric"], "ci_test_failure_rate")
        self.assertEqual(r["evidence"]["window_size"], 24)
        self.assertEqual(len(r["evidence"]["window"]), 24)
        self.assertEqual(len(r["evidence"]["evaluated"]), 9)
        for point in r["evidence"]["window"] + r["evidence"]["evaluated"]:
            self.assertIn("ts", point)
            self.assertIn("value", point)
        self.assertEqual(r["observed"]["ts"], "2026-09-02T00:00:00+09:00")

    def test_18_text_format_is_one_line_summary(self):
        rc, out, err = run_detect(DATA / "spike-3sigma.jsonl", fmt="text")
        self.assertEqual(rc, 0)
        self.assertIn("3sigma", out)
        self.assertIn("rule1_one_point_beyond_3sigma", out)

    def test_19_no_model_is_involved(self):
        """모델 미개입 — 검출기는 네트워크·모델 라이브러리를 쓰지 않는다."""
        src = DETECT.read_text()
        for banned in ("import requests", "urllib.request", "http.client",
                       "anthropic", "openai", "socket"):
            self.assertNotIn(banned, src)


class EmitIntentTest(unittest.TestCase):
    """⑩ · 검출 결과 → Stage 1 형식 intent 초안."""

    SECTIONS = [
        "## Problem (문제)",
        "## Proposed outcome (원하는 결과)",
        "## Affected users and systems (영향 범위)",
        "## Constraints (제약)",
        "## Open questions (미결)",
    ]
    KEYS = ["id", "kind", "status", "author", "created", "record", "supersedes"]

    def _emit_from(self, fixture, intent_id="0003-status-cache-defect"):
        payload = json.dumps(detect_json(DATA / fixture))
        d = tempfile.mkdtemp()
        rc, out, err = run_emit(["--id", intent_id, "--out", d], stdin_text=payload)
        return rc, out, err, Path(d) / intent_id / "intent.md"

    def test_20_writes_intent_for_3sigma(self):
        rc, out, err, path = self._emit_from("spike-3sigma.jsonl")
        self.assertEqual(rc, 0, err)
        self.assertTrue(path.is_file(), "intent.md 가 없다: %s" % path)
        text = path.read_text()
        head, _, body = text.partition("\n---\n")
        self.assertTrue(text.startswith("---\n"))
        for key in self.KEYS:
            self.assertIn("\n%s:" % key, head + "\n")
        self.assertIn("status: draft", head)
        self.assertIn("id: 0003-status-cache-defect", head)
        self.assertIn("kind: intent", head)
        self.assertIn("# Intent:", body)
        for section in self.SECTIONS:
            self.assertIn(section, body)
        # 절 순서
        positions = [body.index(s) for s in self.SECTIONS]
        self.assertEqual(positions, sorted(positions))

    def test_21_no_placeholder_survives(self):
        """‹…› 플레이스홀더를 남기지 않는다 — 사람이 채울 자리도 명시 문장으로."""
        rc, out, err, path = self._emit_from("spike-3sigma.jsonl")
        text = path.read_text()
        self.assertNotIn("‹", text)
        self.assertNotIn("›", text)
        self.assertNotIn("TODO", text)

    def test_22_no_section_is_empty(self):
        """빈 절 금지 — 절마다 본문 1줄 이상."""
        rc, out, err, path = self._emit_from("spike-3sigma.jsonl")
        body = path.read_text().split("\n---\n", 1)[1]
        for i, section in enumerate(self.SECTIONS):
            start = body.index(section) + len(section)
            end = body.index(self.SECTIONS[i + 1]) if i + 1 < len(self.SECTIONS) else len(body)
            chunk = [ln for ln in body[start:end].splitlines() if ln.strip()]
            self.assertTrue(chunk, "빈 절: %s" % section)

    def test_23_evidence_is_carried_into_problem(self):
        """Problem 절에 이상과 증거(지표·z·규칙·시각)가 들어간다."""
        r = detect_json(DATA / "spike-3sigma.jsonl")
        rc, out, err, path = self._emit_from("spike-3sigma.jsonl")
        text = path.read_text()
        self.assertIn(r["metric"], text)
        self.assertIn("rule1_one_point_beyond_3sigma", text)
        self.assertIn("2026-09-02T00:00:00+09:00", text)
        self.assertIn("6.48", text)

    def test_24_writes_for_2sigma(self):
        rc, out, err, path = self._emit_from("run-of-9.jsonl")
        self.assertEqual(rc, 0, err)
        self.assertTrue(path.is_file())
        self.assertIn("rule2_nine_points_one_side", path.read_text())

    def test_25_skips_tier_none_and_1sigma(self):
        """none·1sigma 는 초안을 만들지 않고 rc=0 으로 조용히 끝낸다."""
        for fixture in ("normal.jsonl", "drift-1sigma.jsonl"):
            rc, out, err, path = self._emit_from(fixture)
            self.assertEqual(rc, 0, err)
            self.assertFalse(path.exists(), "%s 에서 초안이 생겼다: %s" % (fixture, path))
            self.assertIn("skipped", out)

    def test_26_input_flag_equals_stdin(self):
        """--input 파일과 파이프가 같은 결과를 낸다."""
        payload = json.dumps(detect_json(DATA / "spike-3sigma.jsonl"))
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / "detect.json"
            src.write_text(payload)
            out_dir = Path(d) / "intent"
            rc, out, err = run_emit(["--input", str(src), "--id", "0003-x",
                                     "--out", str(out_dir)])
        self.assertEqual(rc, 0, err)

    def test_27_broken_input_exits_1(self):
        with tempfile.TemporaryDirectory() as d:
            rc, out, err = run_emit(["--id", "0003-x", "--out", d],
                                    stdin_text="{not json")
            self.assertEqual(rc, 1)

    def test_28_missing_tier_field_exits_1(self):
        """검출기 JSON 이 아닌 것을 먹이면 rc=1 — 조용히 빈 초안을 쓰지 않는다."""
        with tempfile.TemporaryDirectory() as d:
            rc, out, err = run_emit(["--id", "0003-x", "--out", d],
                                    stdin_text='{"hello": 1}')
            self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main()
