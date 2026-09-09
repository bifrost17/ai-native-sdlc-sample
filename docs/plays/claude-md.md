# CLAUDE.md (claude-md)

> 플레이북에서: CLAUDE.md 는 Commands·Conventions·Architecture 와 「같은
> 실수를 두 번 하면 등재한다」를 적어 두는, 길이가 관리되는 운영 매뉴얼이다.
> 출처: 레슨 5.

## 이 레포에서 무엇이 강제되나
- `scripts/gates/10-docs.sh`(PR #3, 대기)의 `check_claude_md_length()` 가
  `wc -l CLAUDE.md` ≤ 60 을 판정한다.
- `scripts/check_all.sh`(= `make check` = CI 필수 상태 체크 `check`)의
  `scripts/gates/*.sh` source 확장 지점은 이미 살아 있다(PR #7 이 머지돼
  main 에 있다 — 실측: `bash scripts/check_all.sh` 원문에 「PASS  밴드 검출
  시험」·「PASS  스킬·에이전트·커맨드 frontmatter…」등 `scripts/gates/30-
  bands.sh`·`scripts/gates/40-skills.sh` 산출 줄이 실제로 찍힌다). 단
  `scripts/gates/10-docs.sh` 자체는 아직 `feat/0001-artifact-validator`
  가 아니라 `docs/0001-playbook-map`(PR #3, 대기)에만 있어 main 엔 없다 —
  **그래서 지금 이 60줄 게이트만은 강제 없음** — 손으로 `bash scripts/gates/
  10-docs.sh` 를 돌려야만 잰다. #3 이 머지돼야 `make check` 가 60줄 상한을
  CI 로 강제한다.
- CLAUDE.md 본문의 「같은 실수를 두 번 하면 이 파일에 등재한다」는 사람이
  지키는 문서 규율이고, 기계가 두 번째 실수를 감지해 등재를 강요하지 않는다.

## 증거는 무엇인가
- `wc -l CLAUDE.md` 의 출력 값(실측: 35줄) · `bash scripts/gates/10-docs.sh`
  원문(standalone 실행 시의 `PASS/FAIL` 줄).

## 어디에 기록되나
- CLAUDE.md 자체의 git 이력(등재 문장이 늘어나는 커밋).

## 누가 승인하나
- 사람 — CLAUDE.md 변경이 든 PR 을 머지하는 product owner. CODEOWNERS 는
  `intent/**`·`.claude/skills/**`·CLAUDE.md 를 겨눈다고 설계안에 있으나,
  ruleset 이 `require_code_owner_review: false` 라 지금은 강제하지 않는다
  (capture-intent.md 참조).

## 지금 상태
| 조각 | 상태 | 어디 |
|---|---|---|
| `CLAUDE.md`(35줄) | 대기(PR #3) | `CLAUDE.md` |
| `scripts/gates/10-docs.sh` | 대기(PR #3) | `scripts/gates/10-docs.sh` |
| `scripts/check_all.sh` 의 gates source 확장 지점 | 착지 | `scripts/check_all.sh` |
| 확장 지점과 10-docs.sh 가 함께 main 에 있는 상태 | 없음 | — |

## 이 플레이에서 우리가 하지 않는 것
- `docs/PHASES.md`(PR #3)에 레슨 5 를 직접 겨눈 이월 항목은 없다. 위에서
  실측한 「60줄 게이트가 아직 CI 에 안 물림」은 의도적 미구현 원장의 항목이
  아니라 배선 순서(PR #3 과 #7 이 함께 머지돼야 함) 문제다.
