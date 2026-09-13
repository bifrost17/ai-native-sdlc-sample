# 0034 제작 변경·설치 정적 리뷰 — Sol

## 판정

수정 반영 후 미해결 finding은 없다. `fc4c730` 대비 후보는 두 판의 기존 검증 정책 차이를 유지하면서
설계 이해와 후속 근거 인계 안내를 같은 의미로 보완한다. 정적 설치와 patch 적용도 통과했다.

리뷰 중 두 문제를 발견해 재검증했다.

1. 두 OpenCode `team-resources/INDEX.md`가 현행 전달판을 각각 0.1.8과 0.1.4로 표시했다. root가
   0.1.9와 0.1.5로 바로잡았고 manifest·marketplace·현행 README·색인의 판이 일치한다.
2. 새 `sdlc-feedback` 문단이 기존 adapter hunk보다 앞에 5줄 추가되어 Apple `patch 2.0`가 세 설치에서
   offset 적용 뒤 `SKILL.md.orig`를 남겼다. 변환 본문은 바꾸지 않고 선택형 Codex와 두 OpenCode patch의
   hunk 시작행만 현재 source에 맞췄다. 깨끗한 r02 세 곳에서 다시 적용해 `.orig=0`, `.rej=0`,
   fuzz/offset 메시지 없음과 예상 변환을 확인했다.

## 의미 검토

- 기본형과 선택형 모두 M01 컴포넌트·배포·경합 시퀀스와 W01 사용자 흐름으로 바로 연결하고, 작은 F01에
  같은 그림을 의무화하지 않는다. `design-depth.md`의 추가 문장은 여러 경계나 대표 흐름 이해에 도움이 될
  때만 Mermaid를 선택하게 하며 클래스 그림이나 그림 수를 일반 의무로 만들지 않는다.
- 두 `sdlc-feedback`은 후속 시험·검토 결과가 남은 작업을 바꿀 때 현재 plan·인계, 실제 시험 revision,
  기존 근거를 연결하고 과거 기록·작성자와 수락·통합·완료의 구분을 보존한다.
- 기본형은 test-first cycle과 RED 규칙을 유지한다. 선택형은 TDD·동작별 구현 후 시험·기존 시험 활용·혼합
  선택과 그 이유·독립 기대를 유지한다. 공통 추가문이 이 차이를 덮지 않는다.
- 변경 파일의 기존 7~40자리 Git 참조 집합을 base와 비교한 결과 제거된 역사 참조는 0개다.

## 검증

`claude plugin validate --strict`를 두 `org-skills`, 두 edition marketplace, root marketplace에 실행했고
다섯 명령 모두 exit 0이었다. 수정 후 `git diff --check fc4c730`도 exit 0이다.

선택형 `project/`를 새
`/Users/jake/Projects/ai-native-sdlc-experiment-private/0034-document-handoff/validation-install/optional-codex-r02`
에 복사하고 Codex README 설치 블록을 절대 경로로 실행했다. 16개 skill, verifier TOML, `AGENTS.md`가
설치됐고 세 patch는 충돌·reject·backup 없이 적용됐다. 네 explicit-only skill의 invocation flag 제거와
`openai.yaml` 추가, feedback의 Codex verifier 경로·모델 표현, ux-copy의 현재 요청·connector 변환을 확인했다.

별도 `tdd-first-opencode-r02`, `tdd-optional-opencode-r02`에는 각 판의 OpenCode README 두 설치 블록을
실행했다. 각 설치는 native skill 11개, 직접 읽는 team resource 2개, 선택 작성 skill 3개를 포함한다.
각 판의 feedback·ux-copy·authoring patch 세 개가 clean 적용됐고 OpenCode verifier 경로·모델 책임 표현과
작성 skill invocation flag 제거를 확인했다.

명령, exit, 판 map, patch와 설치 파일별 SHA-256은 [static-install.json](static-install.json)에 있다.
root가 별도로 보고한 `make check` 결과는 이 정적 리뷰의 독립 실행 결과로 세지 않았다.

## 한계

이번 확인은 manifest 검증, 파일 복사, patch, hash와 문구 변환의 정적 검증이다. Claude, Codex,
OpenCode의 실제 모델 선택·본문 적용·검증자 위임 행동이나 전역 설치는 실행하지 않았다. 0033 제품 구현,
PR3 수락·통합, D7, 두 판 전체 제품 개발 통과도 이 판정의 범위가 아니다.
