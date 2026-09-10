---
name: plan
description: Explicitly selected workflow example for producing an implementation plan from accepted requirements and design, with real files, risks, and verification evidence.
disable-model-invocation: true
---
# 구현 계획 작성 예시

팀이나 사용자가 이 예시를 선택했을 때 사용한다. 대상 변경의 `intent.md`, `spec.md`와 프로젝트가
정한 승인 기록을 확인한다. 초안에서 진행하도록 허용한 지시가 있다면 그 범위와 이유를 기록한다.
기존 코드와 구성은 읽되 계획을 작성하는 동안 제품 코드를 바꾸지 않는다.

`templates/plan.md`를 사용해 같은 변경 폴더에 `plan.md`를 쓴다.

- **Files that change** — 실제 경로를 확인하고 새 파일은 새 파일이라고 적는다.
- **Order of work** — 결함은 실패를 먼저 재현한다. 그 밖의 작업은 관련 기준 동작을 확인하고
  구현, 연결, 검증의 순서를 정한다.
- **Risks** — 영향받는 기존 동작, 위험한 단계, 문제를 발견할 방법과 선택하지 않은 대안을 적는다.
- **Proof** — 실제로 실행할 검사와 성공 기준, 필요한 관측을 적는다. 제품 도구가 아직 없으면
  정해야 할 도구와 담당자를 밝히고 이미 검증한 것처럼 쓰지 않는다.

엔지니어가 대화를 보지 않고도 구현할 수 있는지 검토하게 한다. 무엇이 깨질 수 있는지, 어느 단계가
위험한지, 그 결과를 어떻게 확인할지를 보완한다. 계획 작성과 사람의 승인, 구현은 구분한다.
이 예시는 제품 코드나 다른 단계의 문서를 작성하거나 계획을 승인하지 않는다.
