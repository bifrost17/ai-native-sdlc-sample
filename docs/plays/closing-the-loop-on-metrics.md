# 지표로 루프를 닫는다 (closing-the-loop-on-metrics)

> 플레이북에서: 에이전트는 이상 진단을 Stage 1 형식의 intent.md 로 쓰고
> 이상과 그 증거·제안 결과·영향 시스템·미결 물음을 담는다. 원인·처방은
> 사람의 몫이다. 출처: 레슨 13.

## 이 레포에서 무엇이 강제되나
- `scripts/detect_bands.py`(PR #4, 대기) — Western Electric 규칙 3종(1점
  3σ 이탈·9점 한쪽·3점 중 2점 2σ 이탈)만 구현하고, `ops/bands.yaml` 이
  요구하는 규칙 이름이 그 세 개 밖이면 rc=1 로 죽는다(모델 미개입·결정론).
  tier 는 rc 가 아니라 stdout JSON 필드로만 낸다(rc·tier 겸용 금지).
- `scripts/emit_intent.py`(PR #4, 대기) — tier `2sigma`/`3sigma` 일 때만
  `intent.md` 초안을 쓰고 `status` 는 항상 `draft`. `none`/`1sigma` 는
  파일을 만들지 않는다(rc=0 으로 조용히 종료).
- `scripts/gates/30-bands.sh`(PR #4, 대기)는 `tests.test_detect_bands`
  (28건, 실측: `grep -c "def test_"`)를 등록한다. **단독 실행이 안 된다** —
  다른 세 게이트(10/20/40)와 달리 `run_gate` 가 없으면 즉시 실패 메시지를
  내고 `python3 -m unittest tests.test_detect_bands` 를 직접 돌리라고
  지시한다. 이 게이트는 이제 `check_all.sh` 가 source 한다(claude-md.md
  참조 — 실측: `bash scripts/check_all.sh` 원문에 「PASS  밴드 검출 시험
  (tests/test_detect_bands.py)」 줄).
- main 에는 위 전부가 없다(없음).

## 증거는 무엇인가
- `python3 -m unittest tests.test_detect_bands` 원문(28 test, `tests/data/
  bands/*.jsonl` 12종 픽스처 대조) · `detect_bands.py` stdout JSON 의
  `tier` 필드.

## 어디에 기록되나
- `emit_intent.py` 가 쓰는 `intent/<id>/intent.md` 초안 커밋(사람이 triage
  한 뒤 PR로) — 사슬 실물은 아직 없음(아래 표).

## 누가 승인하나
- 사람 — 초안을 triage 해 accepted 로 바꾸는 것은 언제나 사람(PR 머지).
  검출기·초안 생성기 어느 쪽도 `status:` 를 accepted 로 바꾸지 않는다.

## 지금 상태
| 조각 | 상태 | 어디 |
|---|---|---|
| `ops/bands.yaml` | 착지 | `ops/bands.yaml` |
| `scripts/detect_bands.py` | 착지 | `scripts/detect_bands.py` |
| `scripts/emit_intent.py` | 착지 | `scripts/emit_intent.py` |
| `scripts/gates/30-bands.sh` | 착지 | `scripts/gates/30-bands.sh` |
| `tests/test_detect_bands.py`(28 test) | 착지 | `tests/test_detect_bands.py` |
| `docs/METRICS.md`(플레이북 14쌍 표) | 대기(PR #3) | `docs/METRICS.md` |
| 라이브 스케줄 실행(cron 등) | 없음 | — |

## 이 플레이에서 우리가 하지 않는 것
- 라이브 스케줄 밴드 감시 · Claude Tag 온콜 · 사전 승인 runbook 은 안
  한다 — `docs/PHASES.md`(PR #3): 30일 이상 쌓인 실측 기준선이 없어 밴드
  (1σ/2σ/3σ) 값을 신뢰 있게 못 정함, 승격 조건은 「30일 기준선이 쌓일 때」.
