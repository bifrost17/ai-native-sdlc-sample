# 0035 배포·정적 검토 — Sol/medium

2026-09-14. 비교 base `f41854685213ad368dce035666aaefa8708723fc`, 고정 배포 후보
`41c71101cd69e6757da014f3bdcca930016f925e`. 이 검토자는 변경을 설계하거나 구현하지 않았다.

## 판정

현재 배포·정적 범위에 미해결 finding은 없다. 기본형 0.1.10과 선택형 0.1.6의 문서, package manifest,
edition/root marketplace, OpenCode 색인·설치 안내와 선택형 Codex 안내가 일치한다. 후보 이후 HEAD에 추가된
파일은 실험 기록이며 `tdd-first/`, `tdd-optional/`, root marketplace의 후보 내용은 바뀌지 않았다.

이 판정은 preliminary다. 실제 Muse 응답·평가·HUMAN 후속 대화가 아직 없으므로 AC4/AC5의 행동 효과,
실험 종료 기록, 북극성 주석과 최종 통합은 닫지 않는다.

## 변경 의미와 판 회귀

- 두 `project/REVIEW.md`와 design-spec은 spec 인계 전 전체 선언 정본, 공유 경계의 양쪽 의미,
  중요한 장애·수명 분기의 책임·상태·복구, 의존 작업을 막는 미결과 정당한 내부 이월을 검토하게 한다.
  작은 변경에는 짧은 확인을 허용하고 그림 종류·개수·검토자 수를 합격 조건으로 만들지 않는다.
- 공통 `sdlc-feedback`은 spec 인계·중요 설계 개정을 선택 사건으로 추가하면서 기존 구현 완료 절을
  유지한다. 실제 변경과 완료 주장이 섞이면 design-only라는 이름으로 구현 검토를 생략할 수 없고,
  `A design PASS does not replace the fresh implementation-completion review.`를 양판과 설치 변환본에서 확인했다.
- verifier도 설계 slice/spec handoff/구현/mixed scope를 먼저 구분한다. 설계만의 검토에는 아직 없는 plan,
  구현, 실행 결과를 요구하지 않지만 실제 구현을 포함하면 plan·diff·실행 근거를 적용한다. 이 경계가
  spec-only 예외를 구현 완료 fresh review의 대체 수단으로 만들지 않는다.
- 기본형은 `test-first cycle`, 자동 재현 RED와 기존 예외를 유지한다. 선택형은 구현 planning에 한해
  TDD·동작별 구현 후 시험·기존 시험 활용·혼합 방식과 이유를 기록하고 non-TDD 자체를 finding으로
  보지 않는다. `PROCESS.md`, `REVIEW.md`, feedback과 verifier의 이 판별 차이가 그대로 남아 있다.
- 변경 파일의 기존 7~40자리 Git 참조를 base와 비교한 결과 제거된 역사 참조는 0개다.

## 실행한 검증

`make check`는 exit 0이었다. Python unit test 102개가 실행되어 1개 skip, hook 28/28, eval fixture 8/8,
managed settings 검사가 통과했다. 전체 stdout/stderr는 [make-check.txt](make-check.txt)에 보존했다.

`claude plugin validate --strict`를 다음 다섯 대상에 실행했고 모두 exit 0이었다.

- `tdd-first/org-skills`
- `tdd-optional/org-skills`
- `tdd-first`
- `tdd-optional`
- `.`

새 `/Users/jake/Projects/ai-native-sdlc-experiment-private/0035-spec-validation-muse/validation-install` 아래에
세 제품 복사본을 만들었다. 양 OpenCode 설치는 README의 기본 블록과 선택 authoring 블록을 적용해 각
native skill 11개, 직접 읽는 resource 2개, authoring skill 3개와 verifier를 설치했다. 기본형 authoring
참조 포함 23파일, 선택형은 25파일을 모두 source와 대조했다. 선택형 Codex는 README대로 16개 skill,
verifier TOML과 `AGENTS.md`를 설치했고 authoring reference를 포함한 59 source 파일과 patch 생성
`openai.yaml` 4개를 대조했다.

모든 patch는 exit 0이고 fuzz/offset 출력, `.orig`, `.rej`가 없었다. OpenCode verifier 본문은 각 판의
Claude verifier 본문과 일치한다. Codex TOML의 `developer_instructions`는 선택형 본문에 기존 Codex용
`AGENTS.md` 읽기 한 줄만 더한다. 설치본의 spec handoff 절, 플랫폼별 verifier 경로·모델 책임 표현,
authoring invocation flag 제거와 Codex ux-copy 변환을 직접 확인했다.

OpenCode `debug agent sdlc-verifier`는 두 설치에서 순차 실행해 `mode=subagent`, `steps=20`, edit/task/skill
deny와 해당 판의 prompt를 확인했다. `debug skill` 자체는 exit 0이지만 이 환경에서 출력이 65,536 bytes로
잘려 전체 JSON projection은 exit 5였다. 따라서 전체 inventory는 설치 디렉터리와 파일별 SHA-256으로
증명했다. 이 출력 제한은 package parse 실패로 보지 않는다.

## maker verifier 보조 확인

현재 plan의 배포 구현·정적 검증 slice와 후보 diff 사이에 중요한 파일 범위 불일치는 없었다. Muse 실행,
북극성 주석과 최종 기록은 계획상 후속 작업이다. 이전 `0024-spec-plan-activation/plan.md`를 읽고
`944ce6b^..009b9c5` 누적 diff의 활성 양식·스킬·설치·연구/실험 경로를 대조했다. 별도 역사 제품 실행은
재실행하지 않았다.

인접 hook 확인으로 Makefile Edit JSON을 `.claude/hooks/protect-paths.sh`에 넣었고, frozen path 메시지와
exit 2를 관측했다. 이 hook 실행과 `make check`가 decision log를 추가한 것은 시험이 만든 로컬 기록이다.

## 증거와 한계

명령·exit, version map, patch hash, 세 설치의 모든 source/installed 파일 SHA-256은
[static-install.json](static-install.json)에 있다. manifest를 현재 파일에 다시 해시해 불일치 0을 확인한다.

이번 작업에서 Claude/Codex/OpenCode 추론이나 자연 skill 선택, 실제 verifier 위임, 전역 설치는 실행하지
않았다. 설치와 parsing은 본문 적용이나 행동 통과가 아니다. 원 제품 수정·원격 push·커밋도 수행하지 않았다.
실제 Muse 결과가 들어오면 현재 preliminary maker closing 범위를 새 결과와 plan·실험 기록에 다시 대조해야 한다.
