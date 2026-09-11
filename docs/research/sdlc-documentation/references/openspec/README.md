# OpenSpec 조사

## 조사 판과 범위

이 폴더는 공식 저장소 [`Fission-AI/OpenSpec`](https://github.com/Fission-AI/OpenSpec)의 기본 브랜치 `main`을 커밋 [`9d4e5974e5c0d9a09b9c6c1e1eb0975e80ec4461`](https://github.com/Fission-AI/OpenSpec/tree/9d4e5974e5c0d9a09b9c6c1e1eb0975e80ec4461)에 고정해 조사했다. 커밋 시각은 2026-09-09T20:59:22Z이고, 조사 당시 최신 릴리스 `v1.13.0` 태그도 같은 커밋을 가리켰다. 보관한 19개 원문은 모두 이 단일 스냅샷이다. 파일별 출처와 SHA-256은 [`sources.json`](sources.json)에 있다.

## 확인된 산출물과 그래프

기본 `spec-driven` 스키마의 산출물 관계는 [`schema.yaml`](evidence/schema.yaml)이 가장 정확히 보여 준다.

| 산출물 | 역할 | 의존 관계·선택성 |
|---|---|---|
| [`proposal.md`](templates/proposal.md) | 변경 이유, 구체적 범위, 새로 만들거나 수정할 capability, 영향 | 그래프의 시작점이다. 구현 상세는 넣지 않는다. 행동 변화가 없는 리팩터링·도구·문서 변경은 `.openspec.yaml`의 `skip_specs: true`로 spec delta를 생략할 수 있다. |
| [`specs/**/spec.md`](templates/spec.md) | capability별 행동 계약의 ADDED/MODIFIED/REMOVED/RENAMED delta | proposal을 요구한다. 요구마다 시나리오가 필요하며, 기존 요구 수정은 전체 블록을 복사해 바꿔야 한다. |
| [`design.md`](templates/design.md) | 기술 맥락, 결정과 대안, 위험, migration, 열린 질문 | proposal을 요구한다. 지침상 여러 모듈, 새 의존성, 보안·성능·migration 복잡성이 있을 때 만든다. |
| [`tasks.md`](templates/tasks.md) | 순서 있는 구현 체크리스트와 각 작업의 검증 방법 | 스키마상 specs와 design을 모두 요구한다. 각 작업은 파서가 인식하는 체크박스 형식을 써야 한다. |

이 관계는 단순한 일직선 단계가 아니다. proposal 다음에 specs와 design이 서로 독립적으로 준비될 수 있고, 둘이 완료되어야 tasks가 열린다. [`workflows.md`](evidence/docs/workflows.md)는 이를 “actions, not phases”로 설명하며 구현 중에도 [`update`](evidence/skills/update-change.md)로 기존 산출물을 어느 방향으로든 다시 맞출 수 있다고 한다. 다만 기본 스키마의 tasks 의존성은 실제 제약이고, design 지침의 “큰 변경에만 작성”과 어떻게 skip 상태로 결합되는지는 이번에 보관한 원문만으로 완전히 확인하지 못했다. 따라서 “항상 자유 순서”나 “design은 언제나 생략 가능”이라고 단정하면 안 된다.

[`new-change`](evidence/skills/new-change.md)는 폴더와 첫 산출물 지침만 준비한다. [`continue-change`](evidence/skills/continue-change.md)는 status가 `ready`인 첫 산출물 하나를 만들고, 완료된 의존 자료를 디스크에서 다시 읽는다. 기본 설치의 빠른 경로는 `propose`가 계획 산출물을 한 번에 만들 수 있으며, 세분화된 new/continue/verify는 expanded profile에서 제공된다. explore와 verify는 선택 동작이다. 즉 원본 양식 네 개가 곧 모든 사용자에게 동일한 필수 대화 횟수를 뜻하지는 않는다.

## 사람·에이전트 검토와 구현

[`reviewing-changes.md`](evidence/docs/reviewing-changes.md)는 사람이 두 번 검토하도록 제시한다. 구현 전에는 proposal의 의도·범위, delta spec의 완료 정의, design의 결정, tasks의 실행 가능성을 읽고, 구현 뒤에는 선택적 [`verify`](evidence/skills/verify-change.md)로 코드와 계획을 비교한다. `verify`는 task 완료, 요구·시나리오 대응, design 준수를 completeness/correctness/coherence로 나누지만 키워드 검색과 추론도 사용한다. 따라서 보고서의 “covered”는 테스트 실행이나 형식 검증의 보증이 아니며, 불확실하면 낮은 심각도로 분류하라는 휴리스틱이다.

[`apply`](evidence/skills/apply-change.md)는 CLI가 반환한 context files를 읽고 미완료 task를 구현하며 체크박스를 즉시 갱신한다. 모호하거나 명세 밖 작업, 설계 문제, 오류가 나오면 멈추고 사용자에게 알리도록 되어 있다. 구현 발견으로 계획이 달라지면 update로 돌아간다. update는 이미 존재하는 계획 파일만 수정하고 코드나 아직 생성되지 않은 산출물은 만들지 않으며, 산출물별 변경을 사람에게 확인받는다. 이는 에이전트가 작성하고 사람이 의도·변경 방향을 승인하는 경계를 명시한다.

## 현재 명세 동기화와 이력

OpenSpec의 핵심 구분은 진행 중 변경의 delta와 현재 상태의 main spec이다. [`sync-specs`](evidence/skills/sync-specs.md)는 delta를 `openspec/specs/<capability>/spec.md`에 지능적으로 병합한다. 수정 시 delta에 없는 기존 시나리오는 보존하고, 새 capability는 Purpose와 Requirements 형태로 만든다. sync 뒤에는 `openspec validate --specs`를 실행하도록 지시한다. 이 검증은 문서 형식과 스펙 상태에 대한 검사이지 구현 검증은 아니다.

[`archive-change`](evidence/skills/archive-change.md)는 산출물과 task의 미완료 상태를 확인하되 경고 뒤 사람이 진행을 승인할 수 있게 한다. delta가 있으면 적용 내용을 먼저 보여 주고 “지금 sync” 또는 “sync 없이 archive”를 명시적으로 선택하게 한다. sync를 선택하면 main spec과 다시 비교해 남은 차이가 없어야 변경 폴더를 날짜가 붙은 archive 경로로 옮긴다. 따라서 archive는 history 보존이고 sync는 현재 명세 갱신이며 서로 다른 동작이다. sync 없이 archive하는 모드가 실제로 있으므로 “archive가 항상 현재 명세를 갱신한다”고 쓰면 틀리다. 별도로 `skip_specs: true`는 행동 변화가 없어 delta 자체를 만들지 않는 선택이다. 이 둘도 혼동하면 안 된다.

## 규모·brownfield·운영 비용에 대한 판단

[`existing-projects.md`](evidence/docs/existing-projects.md)는 기존 코드 전체를 사전 문서화하지 않고 다음의 작은 실제 변경만 delta로 남기라고 한다. archive 때 main spec이 조금씩 축적되는 구조라 brownfield에 직접 맞는다. 작은·중간 기능은 빠른 경로, 요구가 불명확하거나 아키텍처 결정이 큰 일은 explore와 산출물별 continue, 여러 저장소는 beta stores를 제시한다. [`team-workflow.md`](evidence/docs/team-workflow.md)는 `openspec/`을 코드와 함께 Git에 커밋해 PR에서 검토하는 방식을 설명한다.

[해석] proposal과 behavior delta를 분리하고, 완료 뒤 현재 명세와 변경 이력을 모두 남기는 구조는 변화가 잦은 기존 서비스에 특히 유용하다. 반면 capability 분류, 엄격한 heading/checkbox 형식, CLI status·instructions, agent skill, 선택 profile, beta store까지 채택하면 단순 문서 양식 이상의 운영 체계가 된다. Node.js 20.19 이상과 OpenSpec CLI, 에이전트 통합이 필요하고, agent-driven semantic merge는 사람의 검토 없이 완전한 자동 정합성을 보장하지 않는다.

[권고] 사내 얇은 흐름에는 `proposal → testable delta → optional design → verifiable tasks`와 “sync와 archive 분리” 원칙을 우선 차용한다. 행동이 안 바뀌는 변경은 명세 생략 사유를 짧게 남긴다. 큰 변경이나 여러 팀이 소유한 capability에만 전체 그래프와 별도 main spec을 적용하고, 작은 수정에는 빠른 경로를 쓴다. verify 결과, 체크된 task, `validate --specs`를 실제 테스트·코드리뷰 통과와 별도로 기록한다.

## 이용 조건과 한계

원문은 [`MIT License`](licenses/LICENSE)이며 저작권 표기는 `Copyright (c) 2024 OpenSpec Contributors`이다. 이 조사는 저장소 문서와 스킬을 정적으로 분석했으며 CLI를 설치하거나 archive/sync 동작, 테스트, 성능을 실행 검증하지 않았다. stores는 원문에서 beta로 표시되어 있고, 설계 생략의 구체적인 상태 전이는 추가 실행 검증이 필요하다.
