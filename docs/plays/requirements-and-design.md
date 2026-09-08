# 요구와 설계 (requirements-and-design)

> 플레이북에서: spec 은 flagged concerns 를 요구하고, intent 의 미결마다
> `answered:`/`carried:` 를 달고, 적용한 스킬 버전을 남긴다 — "skill versions
> in force are logged". 출처: 레슨 3.

## 이 레포에서 무엇이 강제되나
- `scripts/check_artifacts.py`(PR #7, 대기)의 `check_upstream()` 이 spec 의
  `upstream: intent.md@<sha>` 가 가리키는 커밋에서 그 파일의 `status` 가
  `accepted` 인지 판정한다(아니면 red). `check_spec_inheritance()` 는 intent
  의 `C#`/`Q#` 가 spec 의 「상속한 제약」·「Open questions from intent」에
  전부 이어받아졌는지 판정한다.
- `.claude/commands/spec.md`(PR #5, 대기)는 `/spec` 실행 전 intent 의
  `status:` 가 `accepted` 인지 확인하라고 **지시**한다 — 모델이 지시를 읽고
  따르는 규율이고, 실제로 어기면 위 검증기가 뒤에서 잡는 게 강제다.
- `secure-api-review` 스킬(PR #5, 대기) 자체는 조언적 통제다. 대신
  `scripts/check_endpoints.sh`(같은 PR)가 응답 허용 목록·단일 통로를
  파이썬 AST 로 판정한다(R1~R6, rc 0/1/2) — 이 플레이의 유일한 기계 백스톱.
- main 에는 위 전부가 없다(없음) — `docs/DESIGN.md` 만 있다.

## 증거는 무엇인가
- `python3 scripts/check_artifacts.py intent/<id>/spec.md` 의 rc·code.
- `bash scripts/check_endpoints.sh` 의 rc·`E-*` code(`tests/test_check_
  endpoints.sh` 가 red 4종·green 1종 픽스처로 상주 대조).
- `.claude/agents/verifier.md`(PR #5, 대기)가 plan 의 `Proof` ↔ 실행된
  시험 이름을 대조한 보고.

## 어디에 기록되나
- spec.md 커밋(intent 와 나란히) · PR 본문 · `check` CI 런(PR #5/#7 각자
  pass, 실측: `gh pr checks`).

## 누가 승인하나
- 사람 — product owner 가 spec 커밋이 든 PR 을 머지해야 다음 단계(plan)가
  그 sha 를 상류로 잡을 수 있다. 리뷰 승인 강제는 capture-intent.md 와
  같은 이유로 없다(ruleset `protect-main` 실측).

## 지금 상태
| 조각 | 상태 | 어디 |
|---|---|---|
| `scripts/check_artifacts.py`(check_upstream·check_spec_inheritance) | 대기(PR #7) | `scripts/check_artifacts.py` |
| `templates/spec.md` | 대기(PR #7) | `templates/spec.md` |
| `.claude/commands/spec.md` | 대기(PR #5) | `.claude/commands/spec.md` |
| `.claude/skills/secure-api-review/SKILL.md` | 대기(PR #5) | `.claude/skills/secure-api-review/SKILL.md` |
| `scripts/check_endpoints.sh` + `tests/test_check_endpoints.sh` | 대기(PR #5) | `scripts/check_endpoints.sh` |
| `.claude/agents/verifier.md` | 대기(PR #5) | `.claude/agents/verifier.md` |
| `intent/0002-claims-status/spec.md` 실제 산출물 | 없음 | — |

## 이 플레이에서 우리가 하지 않는 것
- intent merge → spec PR 자동 생성 job 은 안 한다 — `docs/PHASES.md`
  (PR #3): 손으로 반복되는 패턴이 3회 미만이라 자동화 비용을 정당화 못
  함, 승격 조건은 「손으로 3회 반복될 때」.
- Claude Design 목업 → Code 핸드오프도 안 한다 — 같은 원장: 이 샘플에 UI
  컴포넌트가 없어 핸드오프할 대상이 없음, 승격 조건은 「UI 있는 예제가 생길 때」.
