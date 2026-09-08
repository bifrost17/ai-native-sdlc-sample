# 플랜 모드 (plan-mode)

> 플레이북에서: 작업 전에 무엇을 어떤 순서로 건드릴지 계획을 세우라고
> 요구하며, 강제 수단으로 훅을 검토하라고만 말한다 — "Consider using a
> hook". 출처: 레슨 4.

## 이 레포에서 무엇이 강제되나
- `.claude/hooks/plan-sync.sh`(PreToolUse·matcher `Bash`, PR #6 대기)가
  `git commit` 계열 명령을 토큰 단위로 판정해, 브랜치 이름이 `NNNN-`로
  시작하면 그 id 의 `intent/<id>/plan.md` 의 `## Files that change` 목록
  밖의 소스가 스테이징돼 있으면 exit 2 로 막는다. 같은 커밋에 plan.md 자체가
  있으면 통과.
- `scripts/check_artifacts.py`(PR #7, 대기)의 `check_plan_proof()` 가 plan
  의 `Proof` 절이 spec 의 `AC#` 를 최소 하나 덮는지 판정한다.
- `docs/SOURCE-OF-TRUTH.md`(PR #7, 대기)는 레슨 4 가 요구하는 「아티팩트마다
  정본 하나 지명」을 「레포가 정본」으로 **선언**한다 — 이건 선언이지 기계
  검사가 아니다(강제 없음 — 문서 규율).
- main 에는 위 전부가 없다(없음).

## 증거는 무엇인가
- `tests/test_hooks.sh`(PR #6, 대기)의 plan-sync 관련 `expect` 단정(전체
  79건 중 일부) · `tests/test_wiring.sh` 의 배선 판정.
- `python3 scripts/check_artifacts.py intent/<id>/plan.md` 의 rc·code.

## 어디에 기록되나
- plan.md 커밋(소스와 나란히, 목록이 늘면 같은 커밋에서 plan 도 갱신) ·
  PR 본문.

## 누가 승인하나
- 사람 — plan.md 가 든 PR 을 머지하는 product owner. 리뷰 승인 강제는
  없다(ruleset `protect-main` 실측, capture-intent.md 참조).

## 지금 상태
| 조각 | 상태 | 어디 |
|---|---|---|
| `.claude/hooks/plan-sync.sh` | 대기(PR #6) | `.claude/hooks/plan-sync.sh` |
| `.claude/settings.json`(PreToolUse 배선) | 대기(PR #6) | `.claude/settings.json` |
| `tests/test_hooks.sh` · `tests/test_wiring.sh` | 대기(PR #6) | `tests/test_hooks.sh` |
| `templates/plan.md` | 대기(PR #7) | `templates/plan.md` |
| `scripts/check_artifacts.py`(check_plan_proof) | 대기(PR #7) | `scripts/check_artifacts.py` |
| `docs/SOURCE-OF-TRUTH.md` | 대기(PR #7) | `docs/SOURCE-OF-TRUTH.md` |
| `intent/0002-claims-status/plan.md` 실제 산출물 | 없음 | — |

## 이 플레이에서 우리가 하지 않는 것
- auto mode · worktree 병렬 세션은 안 한다 — `docs/PHASES.md`(PR #3, 레슨
  4·7 항목): 1인 레포라 동시 작업자가 없어 병렬 조율 장치가 필요 없음,
  승격 조건은 「동시 작업자 2인 이상」.
