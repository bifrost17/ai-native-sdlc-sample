# tests/data/bands — `scripts/detect_bands.py` 표본·설정 픽스처

전부 손으로 만든 결정론 데이터다. 값은 `ci_test_failure_rate`(0~1 비율), `ts` 는 하루 1점.

## 공통 기준선
`*.jsonl` 의 앞 24점(2026-08-01 ~ 2026-08-24)은 다음 8값 주기를 3회 반복한 것이다:

    0.048 0.052 0.046 0.054 0.050 0.056 0.044 0.051

그 24점의 통계(표본 표준편차 n-1, `statistics` 모듈로 독립 계산):

| 값 | 수치 |
|---|---|
| mean | 0.050125 |
| sigma | 0.003837 |
| 2σ 상한 | 0.057799 |
| 3σ 상한 | 0.061636 |

뒤 9점(2026-08-25 ~ 2026-09-02)이 판정 대상 꼬리다. 검출기는 기준선 창에서 꼬리를 **제외**한다
— 그래서 지속적 이동(규칙2)이 자기 자신을 기준선에 섞어 희석시키지 않는다.

## 파일

| 파일 | 꼬리에 넣은 것 | 기대 |
|---|---|---|
| `normal.jsonl` | 주기 그대로 | `tier: none` · 규칙 0건 · z(last) = -0.554 |
| `drift-1sigma.jsonl` | 마지막 0.056 | `tier: 1sigma`(규칙 0건 · z = +1.531) |
| `spike-3sigma.jsonl` | 마지막 0.075 | 규칙1 · `tier: 3sigma` · z = +6.483 |
| `run-of-9.jsonl` | 9점 전부 평균 위(0.052~0.056, 2σ 안) | 규칙2 · `tier: 2sigma` · z = +1.271 |
| `two-of-three.jsonl` | 마지막 3점 중 2점(0.0595 · 0.059)이 2σ 밖, 3σ 안 | 규칙3 · `tier: 2sigma` · z = +2.313 |
| `zero-sigma-flat.jsonl` | 기준선 24점 전부 0.050(σ=0) + 마지막 0.500 | 가드 — `tier: none` · `reason: zero_sigma_baseline` |
| `all-zero-baseline.jsonl` | 기준선 전부 0.0 + 마지막 0.040 | 가드 — `tier: none` · `reason: zero_sigma_baseline` (σ=0 가드가 `min_baseline_rate` 가드보다 먼저다) |
| `too-few.jsonl` | 12점뿐(기준선 3점) | `tier: none` · `reason: insufficient_samples` |
| `broken.jsonl` | 4번째 줄이 중간에서 끊긴 JSON | rc=1 |
| `bad-value-type.jsonl` | `value` 가 문자열 | rc=1 |
| `config-unimplemented-rule.yaml` | 미구현 규칙 요구 | rc=1 |
| `config-unsupported-syntax.yaml` | 앵커·별칭 | rc=1 (조용한 폴백 금지) |
| `config-unknown-family.yaml` | `rules: nelson` | rc=1 |

`zero-sigma-flat.jsonl` 와 `all-zero-baseline.jsonl` 둘 다 두는 이유: 앞의 것은 평균이
`min_baseline_rate` 위라 **σ=0 가드만** 잡고, 뒤의 것은 두 가드가 모두 참이라 **순서**를 잰다.
σ=0 가드를 지우면 앞은 판정이 바뀌고(또는 0으로 나눠 죽고) 뒤는 `reason` 이 바뀐다 — 뮤테이션이 반드시 red 를 낸다.
