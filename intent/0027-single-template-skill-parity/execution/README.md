# 0027 실행·검증 기록

현재 상태: 구현·임시 설치·기존 회귀·독립 최종 검토 완료. 관련 커밋과 로컬 main 통합이 남았다.

## 입력과 Git 범위
사용자 요청: “tdd 선택형을 유일한 템플릿으로 하고 tdd 강제형은 지워. 그리고 코덱스와 클로드 스킬을 같은 수준으로 맞춰줘.”

기준 코드 `b9af49ac0627183db7607f2efaf6549c7e767c40`, 제작 폴더
`/Users/jake/Projects/ai-native-sdlc-sample`, 브랜치 `codex/single-template-skill-parity`.
intent `2df8d8f`, spec `7866bfa`, plan `79dedb8`를 먼저 기록했다.

## 책임과 모델
- root: 단일 배포 구조·삭제·활성 문서·북극성 안내·통합.
- runtime worker: Sol/high, scripts/evals/tests/CI의 실행 경로와 기존 회귀.
- parity worker: Astra/high, 같은 스킬 의미를 전달하는 도구별 설치·갱신·확인 안내와 임시 설치.
- 최종 검토: Astra/high가 새 문맥에서 구현·실제 근거·북극성 범위를 대조했다.

## 범위
기본형의 추적 배포 파일 133개를 삭제하고, 과거 실험·리뷰의 당시 사실은 보존한다.
`tdd-optional/` 경로와 패키지 이름을 유지하며 0.1.8로 배포한다. 전역 Codex/Claude 설정·설치와
제품 저장소는 바꾸지 않는다. 임시 설치와 정적 검사를 실제 개발·자연 스킬 호출로 세지 않는다.

## 검증
- [제작 도구·전체 회귀](runtime-checks.txt): `make check`, Python 103건 실행·기존 1건 건너뜀,
  hooks 28건·eval shell 8건·managed settings 통과. 폐기 판은 모델 호출이나 기록 쓰기 전에 거부한다.
- [설치·자료 대조 설명](parity-verification.md), [원본 출력·해시](parity-installation.json):
  별도 Claude 프로필에 실제 project 설치·목록 확인; Codex 16개 폴더·네 patch·명시 사용 설정·검토 기준 확인.
  기존 OpenCode 세 patch도 확인했다. 두 도구 모두 재설치 충돌에서 원본을 보존했다.
- 환경·비교 기대를 보정한 초기 시도는 `parity-installation-attempt1.json`,
  `parity-installation-attempt2.json`에 남긴다. 최종 성공으로 실패 기록을 덮지 않는다.
- root의 활성 링크 점검에서 실험 색인에 남은 기본형 링크 1개를 발견해 현재 소스로 정정했다.
  역사적 구조 결정의 기본형 링크는 폐기 안내와 실제 `b9af49a`의 대상 존재로 구분한다.
  [최종 링크 결과](root-link-check.json): 206개 확인, 현행 누락 없음.
- 전체 staged `git diff --cached --check`는 새 `codex/patches/pr-loop.patch`의 빈 context 행 때문에
  rc=2였다. unified diff의 한 칸 공백을 보존했으며 해당 patch를 제외한 검사는 rc=0이다.
  이 patch는 임시 설치에서 실제 적용했다. 앞선 worker의 unstaged 공백 검사 통과는 당시
  미추적 patch를 포함하지 않았으므로 전체 변경의 공백 검사 통과로 확대하지 않는다.
- [독립 최종 보고서](final-review.md): 중요한 발견 없음. 새 `make check` 103건·기존 1 skip,
  세 manifest strict, 240파일 해시 재대조, 별도 Codex 설치·재설치 중단·훅 입력·폐기 판 거부를 확인했다.

## root 판정
FR01–03·NFR01–02와 AC01–04의 요청된 배포·설치 준비 범위를 충족했다. 선택형을 유일한 현재
템플릿으로 찾을 수 있고, Codex·Claude가 같은 스킬과 자료·기준을 도구별 경로로 받는다.
과거 기본형의 실험·사슬을 다시 쓰지 않았고 북극성의 기존 행동 판정도 변경하지 않았다.
현행 템플릿의 양식·제품 정책·공통 스킬 본문은 이 변경에서 그대로 보존했다.

실제 Skill 호출·자연 선택·검증자 위임·PR 작업·전체 개발 실험은 이 설치 검사의 범위 밖이다.
기존 정적 시험의 fake CLI는 실제 모델이 정책을 적용했다는 증거가 아니다.
