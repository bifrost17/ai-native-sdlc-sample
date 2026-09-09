"""tests/test_detect_bands.py — scripts/detect_bands.py 계약 시험 (레슨 14).

L14 1030행: "the bands catch slow drift as well as spikes ... detection
stays entirely deterministic, with no model involved." — 양성 대조(3σ 스파이크가
tier 3 을 낸다) · σ=0 가드 · 미구현 규칙/rules 계열 거부 · rc 계약(0/1/2)을 잰다.
"""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "detect_bands.py"
EMIT = ROOT / "scripts" / "emit_intent.py"
CHECK = ROOT / "scripts" / "check_artifacts.py"
DATA = ROOT / "tests" / "data" / "bands"
CONFIG = ROOT / "ops" / "bands.yaml"


def run(samples, config=None):
    cmd = [sys.executable, str(SCRIPT), "--samples", str(samples),
           "--config", str(config or CONFIG)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    out = json.loads(p.stdout) if p.returncode == 0 else None
    return p.returncode, out, p.stderr


class DetectBandsTest(unittest.TestCase):
    def test_spike_3sigma_is_tier_3sigma_propose(self):
        """양성 대조 — 3σ 를 넘는 값이 반드시 tier 3sigma·action propose 를 낸다."""
        rc, out, err = run(DATA / "spike-3sigma.jsonl")
        self.assertEqual(rc, 0, err)
        self.assertEqual(out["tier"], "3sigma")
        self.assertEqual(out["action"], "propose")
        self.assertEqual(out["rule"], "rule1_one_point_beyond_3sigma")

    def test_normal_is_tier_none(self):
        rc, out, err = run(DATA / "normal.jsonl")
        self.assertEqual(rc, 0, err)
        self.assertEqual(out["tier"], "none")
        self.assertIsNone(out["action"])

    def test_run_of_9_one_side_is_tier_2sigma_diagnose(self):
        rc, out, err = run(DATA / "run-of-9.jsonl")
        self.assertEqual(rc, 0, err)
        self.assertEqual(out["tier"], "2sigma")
        self.assertEqual(out["rule"], "rule2_nine_points_one_side")

    def test_two_of_three_beyond_2sigma_is_tier_2sigma(self):
        rc, out, err = run(DATA / "two-of-three.jsonl")
        self.assertEqual(rc, 0, err)
        self.assertEqual(out["tier"], "2sigma")
        self.assertEqual(out["rule"], "rule3_two_of_three_beyond_2sigma")

    def test_drift_1sigma_logs_only(self):
        rc, out, err = run(DATA / "drift-1sigma.jsonl")
        self.assertEqual(rc, 0, err)
        self.assertEqual(out["tier"], "1sigma")
        self.assertEqual(out["action"], "log")

    def test_zero_sigma_baseline_guards_instead_of_dividing(self):
        """가드 — 기준선 σ=0 이면 3σ 로 튀지 않고 reason 으로 멈춘다."""
        rc, out, err = run(DATA / "zero-sigma-flat.jsonl")
        self.assertEqual(rc, 0, err)
        self.assertEqual(out["tier"], "none")
        self.assertEqual(out["reason"], "zero_sigma_baseline")

    def test_all_zero_baseline_hits_zero_sigma_before_min_rate(self):
        rc, out, err = run(DATA / "all-zero-baseline.jsonl")
        self.assertEqual(rc, 0, err)
        self.assertEqual(out["reason"], "zero_sigma_baseline")

    def test_too_few_samples_is_insufficient(self):
        rc, out, err = run(DATA / "too-few.jsonl")
        self.assertEqual(rc, 0, err)
        self.assertEqual(out["reason"], "insufficient_samples")

    def test_broken_jsonl_is_input_error_rc1(self):
        rc, out, err = run(DATA / "broken.jsonl")
        self.assertEqual(rc, 1)
        self.assertIn("입력·설정 오류", err)

    def test_bad_value_type_is_input_error_rc1(self):
        rc, out, err = run(DATA / "bad-value-type.jsonl")
        self.assertEqual(rc, 1)

    def test_missing_samples_file_is_input_error_rc1(self):
        rc, out, err = run(DATA / "does-not-exist.jsonl")
        self.assertEqual(rc, 1)

    def test_unimplemented_rule_in_config_is_rejected(self):
        """설정이 요구한 규칙을 조용히 건너뛰지 않는다 — rc=1 로 죽는다."""
        rc, out, err = run(DATA / "normal.jsonl",
                           DATA / "config-unimplemented-rule.yaml")
        self.assertEqual(rc, 1)
        self.assertIn("구현하지 않은 규칙", err)

    def test_unknown_rule_family_is_rejected(self):
        rc, out, err = run(DATA / "normal.jsonl", DATA / "config-unknown-family.yaml")
        self.assertEqual(rc, 1)

    def test_unsupported_yaml_syntax_is_rejected(self):
        rc, out, err = run(DATA / "normal.jsonl", DATA / "config-unsupported-syntax.yaml")
        self.assertEqual(rc, 1)

    def test_rc_never_doubles_as_tier(self):
        """rc≠0 이면 stdout 은 파싱 가능한 결과가 아니다 — tier 로 오독될 수 없다."""
        rc, out, err = run(DATA / "broken.jsonl")
        self.assertNotEqual(rc, 0)
        self.assertIsNone(out)

    def test_mutation_flipping_3sigma_comparison_breaks_spike_detection(self):
        """뮤테이션 — abs(z_last) > 3.0 을 뒤집으면(<) 스파이크가 안 잡혀야 한다."""
        src = SCRIPT.read_text(encoding="utf-8")
        mutated = src.replace("abs(z_last) > 3.0", "abs(z_last) < 3.0", 1)
        self.assertNotEqual(src, mutated, "치환 대상 문자열을 못 찾았다")
        tmp = ROOT / "scripts" / "_mutant_detect_bands.py"
        tmp.write_text(mutated, encoding="utf-8")
        try:
            p = subprocess.run([sys.executable, str(tmp), "--samples",
                               str(DATA / "spike-3sigma.jsonl"), "--config", str(CONFIG)],
                              capture_output=True, text=True)
            out = json.loads(p.stdout)
            self.assertNotEqual(out["tier"], "3sigma",
                               "뮤테이션이 살아남았다 — 시험이 이 비교를 못 잰다")
        finally:
            tmp.unlink()


    def test_emit_intent_draft_has_no_placeholders_and_passes_check_artifacts(self):
        """L14 1034행 — 진단을 Stage 1 intent 형식으로 쓴다: 실제로 그 형식을 통과해야 한다."""
        det = subprocess.run([sys.executable, str(SCRIPT), "--samples",
                              str(DATA / "spike-3sigma.jsonl"), "--config", str(CONFIG)],
                             capture_output=True, text=True)
        with tempfile.TemporaryDirectory() as tmp:
            p = subprocess.run([sys.executable, str(EMIT), "--id", "0099-band-test",
                               "--out", tmp], input=det.stdout, capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            path = pathlib.Path(tmp) / "0099-band-test" / "intent.md"
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("‹", text)
            check = subprocess.run([sys.executable, str(CHECK), str(path)],
                                   capture_output=True, text=True)
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

    def test_emit_intent_skips_1sigma(self):
        det = subprocess.run([sys.executable, str(SCRIPT), "--samples",
                              str(DATA / "drift-1sigma.jsonl"), "--config", str(CONFIG)],
                             capture_output=True, text=True)
        with tempfile.TemporaryDirectory() as tmp:
            p = subprocess.run([sys.executable, str(EMIT), "--id", "0098-x", "--out", tmp],
                               input=det.stdout, capture_output=True, text=True)
            self.assertEqual(p.returncode, 0)
            self.assertEqual(json.loads(p.stdout)["status"], "skipped")
            self.assertFalse((pathlib.Path(tmp) / "0098-x").exists())


if __name__ == "__main__":
    unittest.main()
