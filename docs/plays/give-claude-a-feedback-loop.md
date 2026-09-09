# Claude 에게 피드백 루프를 준다 (give-claude-a-feedback-loop)

> 플레이북에서: 결함은 실패하는 시험을 먼저 커밋하고, 그 시험을 고칠 수
> 없게 막은 채로 구현해야 시험이 결함을 실제로 증언한다. 출처: 레슨 8.

## 이 레포에서 무엇이 강제되나
- `.claude/hooks/protect-tests.sh`(PreToolUse·matcher `Edit|Write|MultiEdit|
  NotebookEdit`, PR #6 대기)가 현재 브랜치가 `fix/`로 시작하고 대상 경로가
  `tests/` 아래일 때 편집을 exit 2 로 막는다. 브랜치를 못 읽으면
  fail-closed(차단). `fix/*` 가 아니면 사정거리 밖(통과) — 대소문자 무시.
- `CLAUDE.md`(PR #3, 대기) 「Verifying your work」절이 `make check` 를 돌려
  원문을 보고에 붙이라고, 시험이 실패하면 "시험이 아니라 코드를 고친다"고
  지시한다 — 모델이 읽고 따르는 문서 규율이고, protect-tests.sh 는 「시험
  파일 편집 자체」만 막지 「보고 전 검사를 안 돌리는 것」은 막지 않는다.
- `Makefile`(main 착지)에는 `check`·`test` 두 타깃만 있고, `test` 는
  `python3 -m unittest discover -s tests -v` 를 돌린다(더 이상 placeholder
  가 아니다 — 실측: `git show origin/main:Makefile`).
- `make build`·`make lint` 타깃은 어느 열린 PR 에도 없다(없음).

## 증거는 무엇인가
- `bash tests/test_hooks.sh` 의 `expect` 단정(전체 79건 중 protect-tests
  관련 분) · `make check` 원문의 `N passed, N failed` 줄.

## 어디에 기록되나
- 결함 브랜치의 커밋 순서(실패 시험 커밋 → 구현 커밋 → green) · PR 본문.

## 누가 승인하나
- 사람 — `fix/*` PR 을 머지하는 product owner. verifier 서브에이전트
  (`.claude/agents/verifier.md`, main 착지)는 독립적으로 관측만 하고
  통과·반려를 선언하지 않는다 — 선언은 사람의 몫.

## 지금 상태
| 조각 | 상태 | 어디 |
|---|---|---|
| `.claude/hooks/protect-tests.sh` | 대기(PR #6) | `.claude/hooks/protect-tests.sh` |
| `.claude/settings.json`(PreToolUse 배선) | 대기(PR #6) | `.claude/settings.json` |
| `CLAUDE.md`(Verifying your work 절) | 대기(PR #3) | `CLAUDE.md` |
| `Makefile`(check·test) | 착지 | `Makefile` |
| `make build` / `make lint` 타깃 | 없음 | — |
| `intent/0003-status-cache-defect/` 결함 사슬 실물 | 없음 | — |

## 이 플레이에서 우리가 하지 않는 것
- UI 시각 피드백 루프는 해당없음 — 이 샘플에 UI 컴포넌트가 없다
  (`docs/DESIGN.md` §8). `docs/PHASES.md`(PR #3)에 레슨 8 을 직접 겨눈
  이월 항목은 없다.
