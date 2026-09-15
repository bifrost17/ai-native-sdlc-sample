# 에이전트 프로젝트의 테스트 순서 정책과 공개 PR 증거

조사 기준일은 2026-09-12이며, 공개 GitHub 이력만을 사용했다. 프로젝트마다 최근 24개월의 병합 PR에서 기능·버그 수정·리팩터링 각 2건을 먼저 골랐다. 세 프로젝트 모두 최초 6건 중 4건 이상에서 테스트와 구현의 시간 순서를 판별할 수 없어, 규칙에 따라 각 범주를 1건씩 추가해 프로젝트당 9건을 확인했다. 문서, 봇·의존성 갱신, 릴리스 자동화, 생성물만 바꾸는 PR은 제외했다. 전체 후보 검색식과 대표 제외 사례는 [`pr-evidence.json`](../data/agent-projects/pr-evidence.json)에 보존했다.

이 표의 “정책”은 두 층을 분리한다. **프로젝트 개발 정책**은 그 저장소에 기여하는 사람이 따라야 할 테스트·평가 규칙이다. **에이전트 작업 지침**은 그 도구가 사용자의 다른 저장소에서 코드를 고칠 때 따르는 절차다. 한쪽의 TDD 문구를 다른 쪽의 실제 관행으로 간주하지 않았다.

| 프로젝트 | 프로젝트 자체 개발 정책 | 에이전트·워크플로 지침 | 최신 적격 PR 9건의 공개 순서 증거 |
|---|---|---|---|
| OpenHands | 행동 변경에 “TDD tests”를 만들라고 하지만, 테스트를 먼저 작성하거나 실패를 먼저 실행하라는 단계는 명시하지 않는다. lint/test/build가 기본 검증이다. | 조사 대상 저장소는 현재 Agent Canvas 프런트엔드다. 에이전트 런타임·도구는 별도 `software-agent-sdk` 소유이므로 이 저장소의 규칙을 OpenHands 에이전트 전체의 실행 절차로 확대할 수 없다. | 9건 모두 `same_commit_order_unknown`. 그중 1건은 구현 후 base에 테스트만 이식한 retrospective RED replay가 있다. |
| SWE-agent | `pytest` 실행법을 제공하고 가능한 곳에 간단한 단위·통합 테스트를 추가하라고 권한다. test-first 순서는 요구하지 않는다. | 기본 설정은 테스트 파일을 수정하지 말고, 먼저 재현 스크립트를 실행해 오류를 확인한 뒤 코드를 고치고 재실행하라고 한다. 이는 재현 우선 절차이며, 테스트 파일을 먼저 쓰는 TDD와 다르다. | `same_commit_order_unknown` 5, `existing_tests_only` 2, `unknown` 2. |
| obra/superpowers | 스킬 변경에 여러 세션의 적대적 평가와 PR의 전후 결과를 요구한다. 플러그인 테스트와 실제 LLM 행동 eval을 구분하며, 행동 eval은 현재 CI에 포함되지 않는다. | `test-driven-development` 스킬은 기능·버그 수정·리팩터링에서 테스트 작성 → 예상 실패 확인 → 최소 구현 → 통과 확인 → 리팩터링을 강하게 요구한다. | 제한된 범위의 `test_commits_first_failure_author_report` 1, `same_commit_order_unknown` 4, `existing_tests_only` 4. |

정책 원문은 각 저장소의 main HEAD에서 읽었다. Superpowers의 최근 표본 중 #2275는 import/proving-it-works-skill, #2236은 dev, #2287은 stacked branch에 병합됐으므로 main에 이미 반영된 변경이라고 간주하지 않는다.

이 결과는 채택률이나 효과 비교가 아니다. 최근 공개 PR의 커밋 경계와 공개 실행 기록에서 **무엇을 확인할 수 있는지**만 나타낸다. 같은 커밋 안에 테스트와 구현이 함께 있으면 로컬 편집·실행 순서는 Git으로 복원할 수 없다. 최종 CI 통과도 테스트가 먼저 작성됐다는 증거가 아니다.

## OpenHands

현재 [`AGENTS.md`](../originals/projects-agent/openhands-AGENTS@de5a79b4.md)는 이 저장소를 Agent Canvas 프런트엔드로 한정하고, 에이전트·도구·서버 로직은 `OpenHands/software-agent-sdk` 소유라고 구분한다(24–32행). 같은 문서는 `npm run lint`, `npm test`, `npm run build`, `npm run build:lib`를 기본 검증으로 제시하고(19–20행), 행동 변경에는 “Create TDD tests”라고 한다(327–346행). 다만 RED를 구현 전에 실행하라는 순차 규칙은 없다. 따라서 **TDD라는 명칭이 있는 테스트 작성 정책**으로 기록하되, 엄격한 red-first 정책으로 분류하지 않았다. [`DEVELOPMENT.md`](../originals/projects-agent/openhands-DEVELOPMENT@de5a79b4.md)와 [`TESTING_MATRIX.md`](../originals/projects-agent/openhands-TESTING_MATRIX@de5a79b4.md)는 실행 명령·mutation testing·릴리스 검증 범위를 보완하지만 작성 순서를 추가하지 않는다.

| 범주 | PR | 병합 시각 (UTC) | 분류 | 공개 근거 |
|---|---:|---|---|---|
| 기능 | [#17164](https://github.com/OpenHands/OpenHands/pull/17164) | 2026-09-12 03:22 | same commit, 순서 불명 | 여러 커밋에서 구현과 테스트가 함께 바뀜. 마지막 Ubuntu/Windows test-and-build 성공. |
| 기능 | [#17289](https://github.com/OpenHands/OpenHands/pull/17289) | 2026-09-11 22:50 | same commit, 순서 불명 | 최초 기능 커밋에 구현과 테스트 4개가 함께 있음. 최종 test-and-build 성공. |
| 기능 | [#16685](https://github.com/OpenHands/OpenHands/pull/16685) | 2026-09-10 16:38 | same commit, 순서 불명 | 최초 기능 스냅샷에 구현·테스트가 함께 있음. 이후 test-only 보정은 최초 순서를 밝히지 못함. |
| 버그 | [#17228](https://github.com/OpenHands/OpenHands/pull/17228) | 2026-09-11 16:03 | same commit, 순서 불명 | 최초 수정 커밋에 구현과 테스트가 함께 있음. 최종 test-and-build 성공. |
| 버그 | [#17264](https://github.com/OpenHands/OpenHands/pull/17264) | 2026-09-11 10:41 | same commit, 순서 불명 | 최초 스냅샷에 수정·테스트가 함께 있고 이후 테스트 인프라 변경이 이어짐. |
| 버그 | [#17253](https://github.com/OpenHands/OpenHands/pull/17253) | 2026-09-10 15:05 | same commit, 순서 불명 + retrospective replay | 코드와 테스트 3개가 함께 커밋됨. PR 본문은 완성 뒤 테스트만 clean main에 이식해 예상 실패 3개를 재현하고 브랜치에서 38개 통과했다고 기록함. 테스트 유효성 근거지만 원래의 test-first 시간 증거는 아님. |
| 리팩터링 | [#16982](https://github.com/OpenHands/OpenHands/pull/16982) | 2026-09-09 17:55 | same commit, 순서 불명 | 리팩터링과 테스트 갱신이 한 커밋에 처음 나타남. 최종 test-and-build 성공. |
| 리팩터링 | [#16955](https://github.com/OpenHands/OpenHands/pull/16955) | 2026-09-09 05:12 | same commit, 순서 불명 | 워크플로·스크립트 리팩터링과 테스트가 함께 처음 나타남. 전용 테스트와 최종 CI 성공. |
| 리팩터링 | [#17064](https://github.com/OpenHands/OpenHands/pull/17064) | 2026-09-08 14:37 | same commit, 순서 불명 | 최초 rename 커밋에 단위 테스트 변경이 함께 있음. 최종 unit/build와 mock-LLM E2E 성공. |

## SWE-agent

프로젝트 기여 문서 [`docs/dev/contribute.md`](../originals/projects-agent/swe-agent-dev-contribute@3ea751c.md)는 `pytest` 실행 방법을 제공하고(43–62행), 에이전트 행동 변경에는 성공률 개선의 징후를 요구하며 가능한 곳에 간단한 단위·통합 테스트를 추가하라고 한다(108–118행). 테스트를 구현보다 먼저 쓰거나 실패부터 실행하라는 요구는 없다.

반면 사용자 저장소를 고치는 기본 에이전트 프롬프트 [`config/default.yaml`](../originals/projects-agent/swe-agent-default@3ea751c.yaml)은 테스트 변경을 이미 처리된 것으로 간주해 테스트를 수정하지 말라고 하고(18–20행), 오류 재현 스크립트를 먼저 만들어 실행한 뒤 구현을 수정하고 다시 실행하라고 한다(21–26행). 제출 검토도 수정된 테스트 파일을 되돌리라고 한다(49–57행). 따라서 SWE-agent의 기본 작업 흐름은 **실패 재현 우선**이지만 **테스트 작성 우선**은 아니다.

| 범주 | PR | 병합 시각 (UTC) | 분류 | 공개 근거 |
|---|---:|---|---|---|
| 기능 | [#1346](https://github.com/SWE-agent/SWE-agent/pull/1346) | 2026-02-23 18:43 | same commit, 순서 불명 | User-Agent 동작과 테스트 83줄이 한 커밋. Python 3.11/3.12 CI 성공. |
| 기능 | [#1343](https://github.com/SWE-agent/SWE-agent/pull/1343) | 2026-02-23 15:45 | same commit, 순서 불명 | private-repo 지원과 테스트가 최초 커밋에 함께 있음. 최종 rollup에는 pre-commit만 보임. |
| 기능 | [#1239](https://github.com/SWE-agent/SWE-agent/pull/1239) | 2025-08-04 19:34 | 기존 테스트만 | 테스트 파일 변경 없음. Python CI 성공, markdown-link 검사는 실패. |
| 버그 | [#1458](https://github.com/SWE-agent/SWE-agent/pull/1458) | 2026-07-16 15:21 | same commit, 순서 불명 | mapping 수정과 회귀 테스트가 한 커밋. 최종 테스트는 인접 의존성 문제로 10개 실패·118개 통과해 병합된 수정 자체의 독립 성공 증거가 되지 못함. |
| 버그 | [#1463](https://github.com/SWE-agent/SWE-agent/pull/1463) | 2026-07-16 15:20 | same commit, 순서 불명 | URL parser 수정과 테스트 갱신이 최초 커밋에 함께 있음. Python CI 성공. |
| 버그 | [#1446](https://github.com/SWE-agent/SWE-agent/pull/1446) | 2026-07-07 14:34 | same commit, 순서 불명 | Content-Type 수정과 테스트 17줄이 한 커밋. Python CI 성공. |
| 리팩터링 | [#1266](https://github.com/SWE-agent/SWE-agent/pull/1266) | 2025-08-04 20:03 | 기존 테스트만 | 테스트 파일 변경 없음. Python CI 성공. |
| 리팩터링 | [#1224](https://github.com/SWE-agent/SWE-agent/pull/1224) | 2025-06-26 22:13 | 불명 | tokenizer 수정 뒤 단순화. 테스트 변경과 PR check rollup이 없음. |
| 리팩터링 | [#1201](https://github.com/SWE-agent/SWE-agent/pull/1201) | 2025-06-12 20:34 | 불명 | production-only 단일 커밋, 테스트 변경과 PR check rollup 없음. |

## obra/superpowers

프로젝트 자체의 기여 규칙 [`CLAUDE.md`](../originals/projects-agent/superpowers-CLAUDE@b36e082.md)는 스킬을 에이전트 행동을 바꾸는 코드로 취급한다. 스킬을 바꿀 때 writing-skills 절차, 여러 세션의 적대적 압력 테스트, PR의 before/after eval 결과를 요구하며(93–100행), 최소 한 harness에서 테스트하고 결과를 보고하라고 한다(110–115행). [`docs/testing.md`](../originals/projects-agent/superpowers-testing@b36e082.md)는 플러그인 비-LLM 테스트와 실제 LLM 세션 행동 eval을 분리하고, 행동 eval은 현재 CI에 없다고 명시한다(1–6, 24–35행). 이는 프로젝트 자체의 개발·평가 정책이다.

사용자에게 적용되는 [`test-driven-development` 스킬](../originals/projects-agent/superpowers-TDD-skill@b36e082.md)은 별도로 매우 엄격하다. 기능·버그 수정·리팩터링에 항상 적용하고(16–29행), production code 전에 실패 테스트가 있어야 하며(31–45행), RED 실행과 예상 실패 확인(71–128행), 최소 GREEN 구현과 전체 통과 확인(130–183행), green 이후 리팩터링을 지시한다. 이 강한 워크플로 규칙이 실제 저장소의 모든 병합 PR에서 지켜졌다고 전제하지 않고 공개 이력을 따로 조사했다.

| 범주 | PR | 병합 시각 (UTC) | 분류 | 공개 근거 |
|---|---:|---|---|---|
| 기능 | [#2275](https://github.com/obra/superpowers/pull/2275) | 2026-09-12 00:16 | 테스트 커밋 선행 + 실패 작성자 보고 | 공개 테스트 커밋들이 production 수정 전에 있음. 커밋 `49bc293`의 [Task 1 보고서](../originals/projects-agent/superpowers-pr-2275-task1-report@49bc293.md)는 recorder 구현 전에 `KeyError: 'shells'`, `KeyError: 'native_success'`를 관찰했다고 작성자가 요약함. 원문은 상세 run artifact가 Git-ignored라고 명시함. 중간 커밋 GitHub check는 0개이며, 이 기록은 명명된 feasibility/probe 사이클의 작성자 보고이며, 실패 실행의 독립 확인이나 뒤의 모든 변경을 입증하지 않는다. |
| 기능 | [#2236](https://github.com/obra/superpowers/pull/2236) | 2026-09-11 22:21 | same commit, 순서 불명 | 최초 기능 커밋에 스킬·구조 테스트·계획·명세가 함께 있음. 외부 eval 주장에 저장소 내 artifact·GitHub check 없음. |
| 기능 | [#1995](https://github.com/obra/superpowers/pull/1995) | 2026-08-07 20:42 | same commit, 순서 불명 | manifest/support 수정과 CI-safe 테스트가 최초 커밋에 함께 있음. 본문 transcript는 변경 후 acceptance 결과. |
| 버그 | [#2287](https://github.com/obra/superpowers/pull/2287) | 2026-09-11 22:21 | same commit, 순서 불명 | evidence-preservation 수정과 구조 테스트 1줄 갱신이 함께 처음 나타남. stacked PR이며 #2236과 merge commit 공유. |
| 버그 | [#2258](https://github.com/obra/superpowers/pull/2258) | 2026-09-08 18:17 | 기존 평가만 | 스킬 문구만 변경. 본문의 행동 eval은 artifact와 GitHub check가 없어 순서 불명. |
| 버그 | [#2100](https://github.com/obra/superpowers/pull/2100) | 2026-08-06 23:21 | same commit, 순서 불명 | 설계·계획은 구현 전에 공개됐으나 스크립트 수정과 focused test는 구현 커밋에 함께 있음. 본문은 red/green을 주장하지만 transcript/check 없음. |
| 리팩터링 | [#1934](https://github.com/obra/superpowers/pull/1934) | 2026-07-14 22:02 | 기존 평가만 | 본문 before/after 행동 eval로 TDD 문구를 재수정했다고 하나 artifact·GitHub check는 없음. 평가 기반 반복의 근거이며 코드 TDD 순서 근거는 아님. |
| 리팩터링 | [#1935](https://github.com/obra/superpowers/pull/1935) | 2026-07-13 21:25 | 기존 평가만 | 스킬 문구만 변경. 두 after-change sanity check를 보고하고 전체 before/after eval은 pending이라고 명시. |
| 리팩터링 | [#1933](https://github.com/obra/superpowers/pull/1933) | 2026-07-13 21:25 | 기존 평가만 | 스킬 문구만 변경. change wave 뒤 dry-run을 보고하고 전체 before/after eval은 pending이라고 명시. |

## 계획 `83b5d3…` → 구현 `b17d54…` 재검증

이 사례는 원래 커밋 그래프에서 계획 커밋 `83b5d3a963ed63d8231ecb3276c8368caf1857a3`의 직계 다음 커밋이 구현 `b17d54f839831b2345aa389e2f65f435f3a82867`임을 확인했다. 작성자 시각 차이는 44분이다. [보존된 계획 원문](../../exemplary-design-and-plans/originals/P3-superpowers-auth-hardening-plan.md)은 [고정 커밋의 원본](https://raw.githubusercontent.com/obra/superpowers/83b5d3a963ed63d8231ecb3276c8368caf1857a3/docs/superpowers/plans/2026-06-10-visual-companion-auth-hardening.md)과 대응한다. 원본은 source PR [#1720](https://github.com/obra/superpowers/pull/1720)에서 각각 `f656a28e…`, `7b757c6d…`로 rebase되어 병합됐다.

확실히 보이는 사실은 **공개 커밋 그래프에서 계획이 구현에 선행한다**는 것이다. 그러나 구현 커밋은 production 파일과 테스트 파일 4개를 함께 바꿨다. 구현 커밋과 source PR 모두 GitHub check run이 0개다. [보존한 PR 본문](../originals/projects-agent/superpowers-pr-1720-body.md)은 focused regression을 RED에서 GREEN으로 실행했다고 주장하고 결과를 요약하지만, 원래 4회 eval artifact가 PR diff와 현재 worktree에 없다고도 적는다. 공개 transcript나 CI가 실패 실행의 구현 선행 시각을 독립적으로 보여주지 않는다.

따라서 이 사례의 분류는 `same_commit_order_unknown`이다. **plan-before-code는 입증되지만 red-before-green 실행은 작성자 보고**다. 계획 파일 존재만으로 엄격한 TDD 실행까지 입증하는 사례로 인용하면 증거 범위를 넘는다.

## 판정 기준과 한계

- `test_commits_first_failure_author_report`: 관련 테스트가 production 변경보다 앞선 공개 커밋에 있고, 예상 실패 실행에 대한 작성자 요약 artifact가 있다. 원 실행 로그와 독립 CI는 확보하지 못했다. PR 전체가 같은 방식이었다는 뜻은 아니다.
- `same_commit_order_unknown`: 테스트와 production 변경이 동일한 공개 커밋에 처음 나타난다. 커밋 내부 편집·실행 순서는 판정하지 않는다.
- `existing_tests_only`: 관련 신규 테스트는 없고 최종 CI 또는 작성자 보고의 기존 테스트·eval만 있다.
- `unknown`: 관련 테스트 변경과 신뢰할 공개 실행 근거를 찾지 못했다.
- `retrospective_red_replay`: 완성된 브랜치의 테스트를 base 코드에 나중에 재생해 실패를 확인했다. 테스트의 민감도는 뒷받침하지만 원래 작업 순서는 뒷받침하지 않는다.

PR 본문과 커밋 보고서는 작성자 제공 증거로 표시했다. GitHub check가 없는 경우 로컬 실행 주장을 실패로 간주하지도, 독립 검증으로 승격하지도 않았다. squash/rebase는 공개 커밋 이력을 압축할 수 있으므로 `unknown`은 TDD가 없었다는 뜻이 아니다. 반대로 최종 CI 성공, 높은 테스트 수, TDD 정책 문구도 test-first 시간 순서를 단독으로 입증하지 않는다.

원문은 고정 commit raw URL, SHA-256, 바이트 수와 함께 [`source-manifest.json`](../originals/projects-agent/source-manifest.json)에 보존했다. 구조화된 PR·커밋·CI 판정과 검색·제외 기록은 [`pr-evidence.json`](../data/agent-projects/pr-evidence.json), 데이터 디렉터리의 출처 색인은 [`source-manifest.json`](../data/agent-projects/source-manifest.json)에 있다. 핵심 사례 #2275, #17253, #1720의 수정하지 않은 GitHub REST PR·commit·file·check 응답은 [`raw/manifest.json`](../data/agent-projects/raw/manifest.json)에 endpoint와 SHA-256을 함께 기록했다.
