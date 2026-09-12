# TDD 선택형의 의도한 차이

2026-09-12. [tdd-optional](../../../tdd-optional/README.md)은 검증 방식을 작업별로 선택한다.
새 패키지 이름은 `intent-sdlc-skills-optional`, 버전은 0.1.0이다.

| 영역 | 반영한 차이 |
|---|---|
| PROJECT-POLICY·CLAUDE·PROCESS·REVIEW | TDD·동작별 구현 후 테스트·기존 테스트 활용·혼합을 허용. TDD 미선택 자체에 예외 승인 요구 없음 |
| plan·계획 작성 스킬 | 방식과 이유, 구현에서 독립된 기대, 동작별 구현·검증 순서를 연결 |
| 계획 예시 | F01은 구현 후 테스트, B01·F03은 선택 이유가 있는 TDD, W01은 서버 TDD와 UI 구현 후 테스트, M01은 혼합 |
| TDD 스킬 | 사용자가 요청하거나 plan에서 TDD를 선택한 작업에 적용. 선택한 뒤에는 의미 있는 실패·통과 근거 유지 |
| feedback·Claude/OpenCode 검증자 | 선택한 방식과 실제 증거를 대조. TDD 미사용만으로 결함 판단하지 않음 |
| 평가·패키지 | 기본형과 다른 식별자·로드 경로·출력 폴더. prompt와 채점 자료 모두 선택한 namespace 사용 |

intent/spec 양식은 기본형과 동일하다. 인수 조건·독립 기대·회귀 보호·영향 문서 갱신·사람의 수락 및
병합·운영 권한은 유지한다. 버그의 진단 재현과 영구 회귀 테스트 선작성을 구분하며, 사후 시험의
기준판 재생을 원래 TDD를 수행했다는 증거로 바꾸지 않는다.

별도 제품 사본 두 개에서 구현 후 테스트와 TDD를 각각 명시한 실제 작업을 수행했다.
각 7개 시험과 별도 계산 검증이 통과했다. 구현 후 테스트 작업에서 추가 승인을 요구하지 않았다.
[구현 후 테스트 기록](evidence/optional-after/evidence.md), [TDD 기록](evidence/optional-tdd/evidence.md),
[독립 최종 검증](evidence/verification.json). 후자는 단일 함수에 대한 한 RED→GREEN 주기였으며,
복잡한 작업의 세분화나 자연 선택의 일반적인 정확성을 검증하지 않는다.

선택형이 다른 방식보다 우수하다는 결론이나 기본형의 과거 통과를 승계하지 않는다. 유료 native 평가·
실제 설치·자연어 선택은 미검증이다. [전체 검증 범위와 남은 한계](README.md),
[독립 구현 검토](independent-review.md), [연구 근거와 불확실성](../../research/tdd-vs-test-after/README.md)
