# spec·plan 작성 예시

이 패키지는 [`templates/spec.md`](../../templates/spec.md)와 [`templates/plan.md`](../../templates/plan.md)를
실제 변경에 채우는 방법을 보여주는 교육 자료다. 먼저 해당 사례의 `context.md`와 `intent.md`, 이어서
`spec.md`와 `plan.md`를 읽는다. M01만 `spec.md`가 선언한 현재 계약과 세 설계 문서까지 같은 spec 집합으로 읽는다.

| 필요 | 사례 | 보여주는 범위 |
|---|---|---|
| 작은 기능 | [F01](examples/F01/context.md) | 동작별 구현 후 테스트, 정확한 작은 계약, 한 PR |
| 버그 수정 | [B01](examples/B01/context.md) | TDD 선택, 제어문자 재현·고정 시험으로 수정 전후 대조 |
| 두 PR·한 공개 단위 | [F03](examples/F03/context.md) | TDD 선택, 일반/시험 상태, 공개·중단·제어 제거 |
| 저장소 이행 | [M01](examples/M01/context.md) | TDD·기존 시험·운영 관측의 혼합, 다문서 spec과 복구 인계 |
| 웹 UI와 API | [W01](examples/W01/context.md) | 서버 TDD·화면 구현 후 테스트의 혼합, 전체 기능 공개 |
| 구현 중 발견 | [변경 walkthrough](change-walkthrough.md) | 영향받는 spec 집합·plan·시험을 함께 갱신하는 범위 |

완성된 intent/spec 합성 예시를 되풀이하지 않고 plan 판단만 볼 때는 간결한 plan-only 예시인
[기존 시험을 활용한 리팩터링](../../examples/skills/plan/examples/refactor-existing-tests.md)과
[폐기할 UI 탐색](../../examples/skills/plan/examples/disposable-ui-exploration.md)을 참고한다.
전자는 보존 계약과 기존 검증 범위를, 후자는 탐색 질문·직접 관찰·폐기 또는 제품 편입 경계를 보여준다.
둘 다 실제 실행이나 제품 수락 기록이 아니다.

작성 깊이는 [설계 지침](../../examples/skills/design-spec/references/design-depth.md)과
[실행 지침](../../examples/skills/plan/references/execution-depth.md)을 따른다. 공개와 PR 판단에는
[Git 흐름](../GIT-WORKFLOW.md), [PR 크기](../PR-SIZE.md), [공개 제어](../RELEASE-CONTROL.md)를 적용한다.
검증 순서와 탐색·제품 편입 판단은 [검증 방식 가이드](../TESTING-STRATEGY.md)를 필요한 범위에서 읽는다.
각 context가 연결한 [교육 입력](inputs/README.md)은 이 패키지 안에 있다. 이 경로들과 프로젝트 루트의
양식·정책 문서만으로 예시의 필수 읽기가 닫힌다.

구성과 실행 위치는 [M01 컴포넌트·배포 뷰](examples/M01/design/architecture.md),
변경 순서는 [M01 경합 시퀀스](examples/M01/design/storage.md),
화면에서 시작하는 흐름은 [W01 사용자 흐름](examples/W01/spec.md)에서 바로 볼 수 있다.
계약의 상세와 함께 읽되 작은 F01 같은 변경에 같은 그림을 모두 요구하지 않는다.

## 출처와 한계

현행 선택형 plan은 원본에서 검증 방식·이유·순서를 개정한 교육 사본이다. intent/spec의 제품 계약은 유지한다.
모든 방식에서 독립 기대·AC·회귀 검증을 유지하며, 선택형 예시를 원본 실행 결과로 간주하지 않는다.

다섯 예시와 walkthrough의 직접 원본은
`docs/research/sdlc-documentation/spec-plan-design/candidate/`의 source commit `2d3f2dc`다.
교육 입력은 같은 commit의 `docs/research/sdlc-documentation/spec-plan-design/inputs/`에서 복제했다.
각 예시의 `Upstream` SHA는 원래 합성 자료가 있던 당시 배치의 제작 이력이다. 새
`docs/sdlc-authoring/` 경로가 그 과거 commit에 있었다거나 제품 오너가 수락했다는 뜻이 아니다.

F03의 역사 spec `f1ba82e`와 역사 plan `5fc8bdc`, M01의 선행 합성 입력 `efa7339`는 선택적
provenance다. 연구 자료나 maker의 과거 Git 객체가 없는 채택 저장소에서도 현행 예시를 읽을 수 있도록
필수 계약을 이 패키지에 두었고, F03의 전체 역사 실행 자료는 복제하지 않았다. 모든 사례는 합성 draft이며
예정 시험·명령은 제품 구현, 실행 성공, 운영 승인 기록이 아니다. 실제 적용 때에는 경로·명령·정책과
수락 SHA를 해당 제품에서 다시 확인한다.
