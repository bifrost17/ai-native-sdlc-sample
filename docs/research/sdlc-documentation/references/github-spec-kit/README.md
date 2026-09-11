# GitHub Spec Kit 조사

## 조사 판과 범위

이 폴더는 공식 저장소 [`github/spec-kit`](https://github.com/github/spec-kit)의 기본 브랜치 `main`을 커밋 [`c173bf19a6654e3b05386ec3599349a55282b897`](https://github.com/github/spec-kit/tree/c173bf19a6654e3b05386ec3599349a55282b897)에 고정해 조사한 개발 스냅샷이다. 커밋 시각은 2026-09-10T18:16:20Z이다. 조사 당시 최신 릴리스는 `v1.0.6`이었으나 그 태그는 다른 커밋을 가리켰다. 따라서 여기 보관한 17개 원문은 릴리스 자료와 섞지 않고 모두 이 `main` 커밋에서 받았다. 파일별 원본 URL·해시·조회 시각은 [`sources.json`](sources.json)에 있다.

## 확인된 산출물과 역할

다음은 원문이 직접 규정한 사실이다.

| 산출물 | 역할 | 필수성·관계 |
|---|---|---|
| [`constitution.md`](templates/constitution-template.md) | 프로젝트 원칙, 개발 제약, 거버넌스와 개정 규칙 | 기능별 산출물이 아니라 프로젝트 공통 기준이다. 이후 계획의 Constitution Check와 분석의 최상위 제약으로 쓰인다. |
| [`spec.md`](templates/spec-template.md) | 구현 방법을 배제한 사용자 시나리오, 기능 요구사항, 성공 기준, 가정 | 사용자 시나리오·요구사항·성공 기준이 필수다. 데이터가 있을 때만 엔터티 절이 필요하다. |
| [`plan.md`](templates/plan-template.md) | 기술 맥락, 설계 방향, 프로젝트 구조, 복잡성 예외 | `spec.md`를 입력으로 삼고 constitution gate를 전후로 확인한다. `tasks.md`는 이 단계가 만들지 않는다. |
| [`tasks.md`](templates/tasks-template.md) | 사용자 스토리별 구현 작업, 의존 순서, 병렬 가능성, MVP 범위 | `plan.md`와 `spec.md`가 필수 입력이다. research/data model/contracts는 있을 때 참고한다. 테스트 작업은 명세나 사용자가 명시했을 때만 포함한다. |

기본 흐름은 [`specify`](evidence/commands/specify.md) → 선택적 [`clarify`](evidence/commands/clarify.md) → [`plan`](evidence/commands/plan.md) → [`tasks`](evidence/commands/tasks.md) → 읽기 전용 [`analyze`](evidence/commands/analyze.md) → [`implement`](evidence/commands/implement.md)이다. `specify`는 자연어 의도를 기능 명세로 바꾸고 품질 체크리스트를 반복 점검한다. 모호성이 남으면 최대 세 개의 중요한 질문을 사람에게 묻는다. `clarify`는 계획 전에 명세의 불확실성을 줄이는 선택 명령이며 답을 `spec.md`에 반영한다. `analyze`는 세 핵심 산출물의 중복·누락·모순과 constitution 위반을 보고하지만 파일을 고치지 않는다. 수정은 사람이 승인한 뒤 별도 작업으로 해야 한다. `implement`는 체크리스트와 계획 자료를 읽고 작업을 수행하며 완료 표식을 갱신한다.

이 구조는 intent와 implementation을 분리한다. `spec.md`는 무엇과 왜를, `plan.md`는 기술적 어떻게를, `tasks.md`는 실행 단위를 기록한다. 사용자 스토리와 작업의 `[USn]` 표시는 요구에서 작업으로 이어지는 명시적 연결점이다. 다만 표식이 있다고 코드가 요구사항을 충족했다는 보장은 없다. `analyze` 역시 정적 문서 검토이며 실제 테스트 성공이나 운영 품질의 증거가 아니다. 구현 뒤에는 코드와 산출물 diff를 사람이 함께 검토하라는 지침이 있다.

## 변경과 기록의 수명

Spec Kit은 한 가지 유지 정책을 강제하지 않는다. [`spec-persistence.md`](evidence/docs/spec-persistence.md)는 세 모델을 나눈다. flow-forward는 완료 폴더를 역사로 남기고 후속 요구를 새 기능 폴더로 만든다. living spec은 `spec.md`를 계약으로 갱신한 뒤 `plan.md`와 `tasks.md`를 다시 생성하거나 고친다. flow-back은 구현·작업·계획 어디서든 발견을 기록한 다음 전체 산출물을 수동으로 다시 맞춘다. 어느 모델도 기본값이나 CLI 설정이 아니며 팀 규칙이다.

[`evolving-specs.md`](evidence/docs/evolving-specs.md)는 living spec에서 `spec` → `plan` → `tasks` 순으로 반영하고 `analyze` 후 구현을 재개하라고 한다. flow-back도 어떤 문서가 바뀌었는지 판별한 뒤 불일치를 해소해야 한다. 재생성 전 중요한 구현 근거를 옮기지 않으면 잃을 수 있다. 도구 자체의 프로젝트 파일 갱신과 기능 산출물의 진화를 별도 루프로 다루며, 강제 초기화는 커스텀 constitution·template·script를 덮어쓸 수 있다고 경고한다.

## 규모와 기존 시스템에 대한 판단

공식 [`existing-projects.md`](evidence/docs/existing-projects.md)는 기존 시스템 전체를 역으로 명세하지 말고, 깨끗하고 검토 가능한 기준점에서 다음의 작은 변경 하나를 잡으라고 한다. 기존 README·ADR·CI에서 실제 규칙을 constitution으로 옮기고, 호환성 경계를 명세한 뒤 현재 구조와 의존성을 재사용하는 계획인지 검토한다. 이는 brownfield에 적합한 점진 도입 방식이다. 사용자 스토리 단위 독립 테스트와 MVP 우선 작업 구조는 작은 기능을 잘게 자르는 데 유용하고, constitution과 여러 설계 산출물은 큰 기능이나 조직 규칙에 더 가치가 있다.

[해석] 작은 수정에도 constitution, 품질 체크리스트, spec, plan, tasks를 모두 강제하면 문서 비용이 변경 가치보다 커질 수 있다. 반대로 API 호환성, 데이터 마이그레이션, 여러 팀 경계가 있는 변경에서는 같은 구조가 중요한 결정을 먼저 드러낸다. 확장 hook은 조직 자동화를 붙일 수 있지만 명령 프롬프트가 길고, 필수 hook 실행 의미까지 이해해야 하므로 단순 템플릿보다 운영 표면이 넓다. Spec Kit은 `specify` CLI와 지원 에이전트 통합에 의존하며, 문서만 복사하면 생성·검사 흐름이 그대로 재현되지는 않는다.

[권고] 사내 기본 양식에는 사용자 시나리오, 검증 가능한 요구, 성공 기준, 기술 결정, 작업-요구 연결만 얇게 차용한다. constitution은 프로젝트 공통 규칙이 실제로 있을 때만 두고, 작은 변경은 간단한 spec과 작업 목록으로 축약한다. 완료 문서의 수명 정책은 도구에 맡기지 말고 flow-forward/living/flow-back 중 하나를 팀 규칙으로 선언한다. `analyze` 결과와 체크박스를 테스트·코드리뷰 증거로 취급하지 않는다.

## 이용 조건과 한계

원문은 [`MIT License`](licenses/LICENSE)이며 저작권 표기는 `Copyright GitHub, Inc.`이다. 재사용 시 라이선스 고지와 저작권 고지를 유지해야 한다. 이번 조사는 템플릿과 지침을 정적으로 읽은 결과이며 CLI 설치, 명령 실행, 생성물 품질 또는 성능 벤치마크를 검증하지 않았다. `main` 개발 스냅샷은 이후 변경될 수 있으므로 운영 채택 전 안정 릴리스에서 다시 확인해야 한다.
