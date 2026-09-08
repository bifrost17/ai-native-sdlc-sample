# 스킬 = 조직 지식 (skills-as-institutional-knowledge)

> 플레이북에서: 반복되는 절차·정책을 스킬로 굳혀 다음 세션에 다시 설명하지
> 않게 한다. 스킬은 모델이 읽어야 작동하는 조언적 통제다. 출처: 레슨 6.

## 이 레포에서 무엇이 강제되나
- `.claude/skills/capture-intent/SKILL.md` · `.claude/skills/secure-api-
  review/SKILL.md`(둘 다 PR #5, 대기) 자체는 강제가 아니다 — 모델이 읽고
  따르는 규율이다. `secure-api-review` 문서 본문도 스스로 「이것은 조언적
  통제다. 읽히면 작동하고 안 읽히면 작동하지 않는다」라고 명시한다.
- 그 뒤에 둔 기계는 `scripts/check_endpoints.sh`(PR #5, 대기) — 파이썬
  AST 로 단일 응답 통로(`build_response`)·단일 허용 목록(`RESPONSE_FIELDS`)
  ·단일 라우트 파일을 판정한다(R1~R6, rc 0/1/2, `tests/test_check_
  endpoints.sh` 가 red 4종·green 1종으로 상주 대조).
- 이 백스톱조차 지금은 자동으로 돌지 않는다 — `scripts/gates/40-skills.sh`
  가 이 시험을 등록하지만 `scripts/check_all.sh`(= `make check` = CI 필수
  체크 `check`)가 `scripts/gates/*.sh` 를 아직 source 하지 않는다
  (claude-md.md 와 같은 사정). 지금은 `bash scripts/check_endpoints.sh`
  (또는 `gates/40-skills.sh`)를 손으로 돌려야 잰다.
- main 에는 스킬·백스톱 전부 없다(없음).

## 증거는 무엇인가
- `bash scripts/check_endpoints.sh [디렉터리]` 의 rc·`E-*` code.
- `bash tests/test_check_endpoints.sh` 원문(픽스처별 기대 code 대조).

## 어디에 기록되나
- `.claude/skills/**` 변경 커밋 · PR 본문(적용한 스킬은 spec 의
  `skills_applied` 필드에도 남는다 — requirements-and-design.md 참조).

## 누가 승인하나
- 사람 — `.claude/skills/**` 변경 PR 을 머지하는 product owner. 설계안은
  CODEOWNERS 를 「정책 소유자」로 부르지만, ruleset 이 코드오너 리뷰를
  요구하지 않아(실측, capture-intent.md) 지금은 그 승인 경로가 강제되지
  않는다.

## 지금 상태
| 조각 | 상태 | 어디 |
|---|---|---|
| `.claude/skills/capture-intent/SKILL.md` | 대기(PR #5) | `.claude/skills/capture-intent/SKILL.md` |
| `.claude/skills/secure-api-review/SKILL.md` | 대기(PR #5) | `.claude/skills/secure-api-review/SKILL.md` |
| `scripts/check_endpoints.sh` | 대기(PR #5) | `scripts/check_endpoints.sh` |
| `tests/test_check_endpoints.sh` + `tests/fixtures-endpoints/{green,red}` | 대기(PR #5) | `tests/test_check_endpoints.sh` |
| `scripts/gates/40-skills.sh` | 대기(PR #5) | `scripts/gates/40-skills.sh` |
| CI 가 위 시험을 자동으로 돌리는 상태 | 없음 | — |

## 이 플레이에서 우리가 하지 않는 것
- 스킬이 실제로 호출됐는지 재는 시험은 안 한다 — `docs/PHASES.md`(PR #3):
  모델이 스킬을 실제로 호출했는지는 결정론 스크립트로 못 재고 반복 측정할
  evals 예산(키)이 없음, 승격 조건은 「evals 가 키를 얻을 때」.
