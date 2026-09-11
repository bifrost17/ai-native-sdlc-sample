# Spec Kitty 조사

## 조사 판과 범위

이 폴더는 이전 홈이 아니라 이동된 공식 저장소 [`spec-kitty/spec-kitty`](https://github.com/spec-kitty/spec-kitty)의 기본 브랜치 `main`을 커밋 [`d96d0209b82318a641234812aff0817afbf09681`](https://github.com/spec-kitty/spec-kitty/tree/d96d0209b82318a641234812aff0817afbf09681)에 고정해 조사한 개발 스냅샷이다. 커밋 시각은 2026-09-10T18:13:29Z이다. 조사 당시 최신 릴리스 `v3.2.7` 태그는 다른 커밋을 가리켰으므로, 여기 보관한 20개 파일은 릴리스 자료를 섞지 않고 모두 고정한 `main`에서 받았다. 상세 출처와 해시는 [`sources.json`](sources.json)에 있다.

## 확인된 산출물과 상태 모델

소프트웨어 개발 mission은 intent를 단순 문서 연쇄보다 더 큰 실행 상태로 바꾼다. 공식 개요의 흐름은 `spec → plan → tasks → next → review → accept → merge`이고, [`mission-system.md`](evidence/docs/mission-system.md)는 discovery → specify → plan → tasks outline/packages/finalize → implement → review → accept를 구분한다.

| 산출물 | 역할 | 필수성·연결 |
|---|---|---|
| [`spec.md`](templates/spec-template.md) | 우선순위 사용자 시나리오, 수용 시나리오, FR/NFR/constraint, 성공 기준 | 사용자 시나리오·요구사항·성공 기준이 필수다. FR/NFR/C에 안정 ID와 상태를 둔다. |
| [`plan.md`](templates/plan-template.md) | 기술 맥락, charter gate, 실제 저장소 구조, 복잡성 예외, 선택적 implementation concern map | spec 다음에 만들며, 미해결 계획 질문을 먼저 해소한다. concern은 WP가 아니며 tasks 단계에서 실행 단위로 번역된다. |
| [`tasks.md`](templates/tasks-template.md) | WP 목록, 의존 그래프, 요구 커버리지 표, subtask 색인 | WP마다 독립 전달·검증 가능해야 한다. subtask 완료는 Markdown checkbox가 아니라 event-log 기반 명령 상태가 권위다. |
| [`tasks/WP*.md`](templates/task-prompt-template.md) | WP별 소유 파일, 생성 의도, 역할·에이전트, 상세 실행·테스트·수용·리뷰 맥락 | 코드 변경 WP와 계획 산출물 WP의 소유 경계를 선언하며 각 WP의 구현·리뷰 입력이 된다. |

[`expected-artifacts.yaml`](evidence/expected-artifacts.yaml)은 단계별 blocking 파일을 별도로 선언한다. specify에는 `spec.md`, plan에는 `plan.md`, tasks outline에는 `tasks.md`, package/finalize에는 `tasks/WP*.md`가 필요하다. research, gap analysis, quickstart, data model은 optional이다. implement와 review 단계에는 이 manifest만으로 강제되는 파일이 없고 WP 상태나 런타임 gate가 별도로 판단한다. bulk edit의 occurrence map도 런타임에서만 검사된다고 명시한다. 즉 파일 존재 검사와 실행 상태 검사는 같은 것이 아니다.

[`mission.yaml`](evidence/mission.yaml)은 `spec.md`, `plan.md`, `tasks.md`를 필수 산출물로 두고, WP가 모두 approved/done이어야 하며 review 승인 gate가 있어야 다음으로 진행하는 조건을 선언한다. WP는 `planned → claimed → in_progress → for_review → in_review → approved → done` 같은 lane 상태를 갖고, 구현은 WP별 격리된 Git worktree에서 수행된다. `tasks` 지침은 의존 DAG의 cycle, requirement/plan 참조 누락, 과도한 WP 크기를 오류로 다루고 각 WP의 소유 파일을 분리한다.

## 사람·에이전트 검토와 구현

[`implement`](evidence/actions/implement.md) 지침은 CLI가 지정한 worktree 밖, 특히 main checkout에 산출물을 쓰지 못하게 하고, 모든 구현을 커밋한 뒤 `for_review`로 옮기게 한다. [`review`](evidence/actions/review.md)는 WP 의존성이 main에 병합됐는지, 실제 코드 결합과 선언이 맞는지, 수용 기준과 테스트 커버리지를 확인한다. 승인하면 `approved`, 거절하면 구조화한 피드백을 남기고 `planned`로 되돌린다. 리뷰어는 직접 수정하지 않고 구현자에게 실행 가능한 피드백을 돌려준다. [`review-work-package.md`](evidence/docs/review-work-package.md)는 수용 기준을 1차 판정 기준으로 삼고 한 리뷰에 승인 또는 거절 하나만 내리도록 한다.

모든 WP가 approved/done이면 [`accept-and-merge.md`](evidence/docs/accept-and-merge.md)의 mission acceptance가 메타데이터, 활동 로그, 미해결 clarification을 확인한다. merge도 독립 preflight를 수행하며, 이후 mission review로 spec-to-code fidelity와 FR coverage를 다시 본다. 일부 post-consolidation 조건은 accept 시점에 판단할 수 없어 지연될 수 있고, 저장소가 별도 CI 검사를 갖추지 않으면 실제로 검증되지 않는다고 원문이 명시한다. 그러므로 accept 기록이나 요구 커버리지 표 자체를 종단간 검증 보증으로 해석하면 안 된다.

사람 역할은 선택 사항으로 사라지지 않는다. upstream README는 사람이 intent·architecture·acceptance criteria를 정하고 reviewer가 accept/reject/merge 결정을 내리는 기본 모델을 설명한다. 다중 에이전트 예시는 lead가 spec/plan을 조정하고 에이전트가 서로 다른 WP를 맡으며 human reviewer가 `for_review`를 처리한다. 같은 사람이 self-review할 수도 있지만 독립성의 정도는 팀 선택이다.

## 변경 기록, 규모, 기존 시스템

[`mission-workflow.md`](evidence/docs/mission-workflow.md)는 spec·plan·tasks뿐 아니라 planning/status/review/orchestration commit, 병합 전 dry-run, 병합 뒤 mission review와 retrospective까지 남기는 아홉 단계 흐름을 제시한다. 원문은 core artifacts를 `kitty-specs/`와 Git에 유지하고, runtime state와 리뷰 결과도 저장한다고 설명한다. 다만 완료 mission을 별도 archive로 옮기는 OpenSpec식 모델이나 living spec 재생성 규칙은 이번 소프트웨어 개발 자료에서 확인되지 않았다. 새 요구나 구현 발견이 생겼을 때 어떤 기존 문서를 먼저 수정하고 history를 어떻게 보존할지는 팀 규칙을 추가로 정해야 한다.

[`solo-developer-workflow.md`](evidence/docs/solo-developer-workflow.md)는 작은 기능도 동일 흐름을 쓰는 예시를 주지만 tiny change에는 과하다고 직접 말한다. dashboard는 선택이고 worktree도 fallback은 가능하다고 설명한다. [`multi-agent-workflow.md`](evidence/docs/multi-agent-workflow.md)는 큰 기능에서 WP별 소유 경계와 worktree가 병렬 충돌을 줄이는 용도를 보여 준다. bug·refactor도 software-dev mission을 더 작은 범위로 쓰라는 설명은 있으나, 기존 시스템 전체를 어떻게 점진 명세화하는지에 관한 별도 brownfield 전략은 선택 원문에서 확인되지 않았다.

[해석] Spec Kitty의 강점은 FR ID → WP requirement refs → owned files → lane/review/merge 기록을 한 저장소에서 이어 볼 수 있다는 점이다. 그러나 이 연결은 선언된 추적 구조이며, 모든 FR이 실제 코드·테스트·PR과 완전하게 연결된다는 보장은 아니다. 특히 expected-artifacts manifest 밖의 runtime gate와 외부 CI가 존재해, 템플릿만 복사하면 같은 통제가 생기지 않는다. 또한 spec·plan·tasks 외에 WP prompt, event log, worktree, lane, charter, gate, acceptance matrix, retrospective가 붙어 운영 비용이 가장 크다.

[권고] 여러 에이전트가 병렬로 작업하거나 소유 파일 충돌과 독립 리뷰가 실제 문제인 큰 변경에 WP 단위 모델을 선택적으로 참고한다. 사내 기본 양식에는 requirement ID, WP 의존성, 소유 파일, 수용 기준, 승인/거절 상태만 얇게 가져오고 dashboard·orchestrator·retrospective·복잡한 gate는 필요가 입증된 팀에만 둔다. tiny change에는 간단한 작업 기록을 허용하고, brownfield에서는 기존 구조와 호환성 경계를 먼저 읽는 별도 규칙을 보완한다. 명세 변경 순서와 완료 문서 보존 정책도 명시해야 한다.

## 의존성, 불일치, 이용 조건

도구는 Python 3.11 이상, `spec-kitty-cli`, Git과 worktree, 지원 AI 에이전트 통합에 의존한다. hosted tracker와 sync는 선택이지만 로컬 CLI와 repo 상태 모델은 핵심이다. 고정 스냅샷 안에서도 [`mission.yaml`](evidence/mission.yaml)의 legacy agent context는 test-first를 non-negotiable로 서술하는 반면 [`tasks-template.md`](templates/tasks-template.md)는 이해관계자가 요청할 때만 명시적 테스트 작업을 넣으라고 한다. 이는 개발 브랜치 자료를 그대로 조직 정책으로 채택하기 전에 현재 릴리스와 charter 해석을 재확인해야 할 이유다.

원문은 [`MIT License`](licenses/LICENSE)이며 저작권 표기는 `Copyright (c) 2026 Spec Kitty, Inc.`이다. 이번 조사는 정적 문서 분석이며 CLI, worktree, gate, 병렬 실행, 테스트나 성능을 실행 검증하지 않았다. 공식 예시의 “충돌 없음” 같은 결과도 제품 일반 성능 주장으로 사용하지 않았다.
