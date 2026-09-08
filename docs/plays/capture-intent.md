# 의도 채록 (capture-intent)

> 플레이북에서: 사슬의 첫 칸은 해법이 아니라 「무엇이 안 되는가」와 「끝났을 때
> 무엇이 달라지는가」를 담은 intent.md 한 장이다. 해법·기술 선택은 이 단계의
> 산출이 아니다. 출처: 레슨 2.

## 이 레포에서 무엇이 강제되나
- 절 집합·순서·frontmatter 7키·플레이스홀더(`‹…›`) 잔존 여부는
  `scripts/check_artifacts.py` 가 판정한다(코드 펜스 제거 후, rc 0/1/2).
- `scripts/check_all.sh` 검사7(templates 는 반드시 rc=1)·검사8(green rc=0)·
  검사9(red 는 지정 code 로 rc=1)이 검증기 자체의 무동작을 잡는 상주 대조다.
- 위 셋은 전부 `feat/0001-artifact-validator`(PR #7, 대기)에만 있다 — main 엔
  아직 `scripts/check_artifacts.py` 도 `templates/intent.md` 도 없다.
- `.claude/skills/capture-intent/SKILL.md`(PR #5, 대기)의 질문 순서·하드룰
  (status 는 항상 draft·플레이스홀더 금지·`created` 자기 신고)은 모델이
  읽어야 작동하는 규율이다 — 어겨도 막는 기계는 없다(강제 없음 — 규율뿐).
- GitHub ruleset `protect-main`(active, 실측: `gh api
  repos/.../rulesets/22537123`)이 main 직접 push·force-push·삭제를 막고
  `check` 상태 체크를 필수로 건다. 단 `required_approving_review_count: 0`
  · `require_code_owner_review: false` — 사람 리뷰 승인은 강제되지 않는다.

## 증거는 무엇인가
- `python3 scripts/check_artifacts.py <경로>` 의 rc·`--format json` 의 `code`.
- `tests/test_check_artifacts.py` · `tests/run_fixtures.py`(green/red 픽스처).
- `scripts/check_all.sh` 실행 원문의 `PASS/FAIL` 줄.

## 어디에 기록되나
- git 커밋(사슬은 커밋 순서로 읽는다) · PR 본문 · 각 PR 자체의 `check` CI 런
  (`gh pr checks 7` 등 실측: pass).

## 누가 승인하나
- 사람 — 발의자가 되읽고 정정, product owner 가 **PR 머지**로 승인하거나
  **PR close** 로 반려한다(설계안 D6). `.github/CODEOWNERS`(PR #3, 대기)의
  `intent/**` 규칙은 파일은 있으나 ruleset 이 `require_code_owner_review:
  false` 라 지금은 아무것도 강제하지 않는다.

## 지금 상태
| 조각 | 상태 | 어디 |
|---|---|---|
| `scripts/check_artifacts.py` | 대기(PR #7) | `scripts/check_artifacts.py` |
| `templates/intent.md` | 대기(PR #7) | `templates/intent.md` |
| `.claude/skills/capture-intent/SKILL.md` | 대기(PR #5) | `.claude/skills/capture-intent/SKILL.md` |
| `.github/CODEOWNERS`(intent/** 규칙) | 대기(PR #3) | `.github/CODEOWNERS` |
| `.github/ISSUE_TEMPLATE/intent.yml` | 대기(PR #3) | `.github/ISSUE_TEMPLATE/intent.yml` |
| ruleset `protect-main` | 착지(레포 설정) | GitHub rulesets API |
| `intent/0002-claims-status/intent.md` 등 실제 사슬 | 없음 | — |

## 이 플레이에서 우리가 하지 않는 것
- 이슈 폼 → intent PR 자동 생성, claude.ai 커넥터 연동은 안 한다 —
  `docs/PHASES.md`(PR #3): 폼 발의 실적이 0건이라 자동화할 반복 패턴이
  없음, 승격 조건은 「폼 발의 3건 이상」.
- 스킬이 실제로 트리거됐는지 재는 시험은 없다(모델 발화라 결정론 장치가 없다).
