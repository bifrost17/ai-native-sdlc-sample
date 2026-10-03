# TDD 선택형

작업별로 TDD, 동작별 구현 후 테스트, 기존 테스트 활용, 혼합 방식을 선택하는 배포판이다.
선택과 이유를 plan에 담고, 인수 조건·독립 기대·회귀 보호·실제 검증 근거를 유지한다.
TDD를 고르지 않았다는 이유만으로 별도의 예외 승인을 요구하지 않는다.

## 채택

1. [project/README.md](project/README.md)를 읽고 `project/`의 **내용**을 별도 제품 저장소 루트로 복사한다.
2. 제품의 [PROJECT-POLICY.md](project/PROJECT-POLICY.md)에 실제 역할·명령·정책을 채운다.
3. 필요하면 이 판의 [팀 스킬](org-skills/README.md)을 선택 설치한다. 식별자는 `intent-sdlc-skills-optional`이다.

작성 3개·팀 13개 스킬은 [Claude Code 설치 안내](org-skills/claude/README.md)와
[Codex 설치 안내](org-skills/codex/README.md)를 따른다. 같은 스킬 폴더·참고 자료·검토 기준을
도구별로 전달하며, 명시 사용 정책과 실제 검증 범위를 함께 설명한다.

폐기된 기본형 패키지나 기존 사용자 전역의 TDD 지침을 함께 적용하지 않도록 실제 설치·로드 출처를 확인한다.
이 구조 변경은 기존 설치를 자동 갱신·제거하지 않는다. `project/`에는 활성 스킬·훅이 없고
작성 스킬은 `project/examples/skills/`의 선택 예시다.

현재 `intent-sdlc-skills-optional` 0.1.9는 유일한 배포판이다. 제품 채택용
[개발건 색인](project/changes/README.md)과 [PR·커밋 전달 기준](project/docs/CHANGE-DELIVERY.md)을 제공하고,
단계 수락·실제 변경·검증판·남은 일을 구별한다. 문서·소스·검증 지침을 전달하는 패키지 변경이며
새 판의 실제 모델 행동이나 제품 실행 통과를 주장하지 않는다. 0.1.8의 Claude·Codex 설치 안내와
PR 입력 변환, 0.1.7의
[요구·설계·작업 추적](project/docs/sdlc-authoring/traceability.md)과 커밋·인계 기준을 유지한다.

## 방식 선택과 검증

[검증 방식 가이드](project/docs/TESTING-STRATEGY.md)에서 작업 조건별 선택, 기대값의 출처, 탐색·실행·완료 기준을 읽는다.
원하는 동작과 판정 근거를 먼저 정하되 모든 테스트 코드를 먼저 작성할 필요는 없다. 플레이북의 버그
test-first 처방을 팀의 선택 정책으로 조정한 범위도 가이드에 명시한다.

[plan 양식](project/templates/plan.md)은 실행 순서 안에서 선택 이유와 선행 인수 조건·검증 방법을 연결한다.
[F01](project/docs/sdlc-authoring/examples/F01/plan.md)은 동작별 구현 후 테스트,
[B01](project/docs/sdlc-authoring/examples/B01/plan.md)은 TDD,
[W01](project/docs/sdlc-authoring/examples/W01/plan.md)은 서버 TDD와 UI 구현 후 테스트의 혼합을 보여준다.
[기존 테스트로 보호하는 리팩터링](project/examples/skills/plan/examples/refactor-existing-tests.md)과
[폐기 가능한 UI 탐색](project/examples/skills/plan/examples/disposable-ui-exploration.md)은 새 테스트가
필요하지 않은 경우와 학습 결과를 제품에 편입할 때의 조건을 보여주는 계획 예시다. 실제 실행 기록은 아니다.
검증자는 선택한 방식과 실제 근거를 대조한다. 구현 후 만든 시험을 과거의 test-first 증거로 바꾸지 않는다.

기본형의 intent/spec와 사람의 수락·병합·운영 구조를 유지한다. 테스트를 약화해 실패를 감추거나
완료 전 검증을 생략하는 방식은 선택지가 아니다. 기본형의 과거 실행 통과를 이 판의 통과로 승계하지 않는다.
