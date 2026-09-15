# F03: 두 PR, 한 공개 단위

고정 개발 데이터: F02의 네 합성 요청과 baseline list/show/complete를 재사용한다. F03에서는 담당자
목록과 all/open/done 집계를 한 공개 단위로 지정한다. 기존 F02의 두 독립 기능과 다른 요구이며 그
실험 결과를 수정하지 않는다. 작은 Python 표준 라이브러리 CLI로 실행 시간과 의존성을 제한한다.

HUMAN 페르소나: Codex root, 사내 요청 업무의 제품 책임자이자 검토·로컬 통합·모의 공개 결정자.
원하는 업무 결과와 제약을 제공하고, AGENT의 실제 답을 읽어 수락·피드백한다. 구현 코드는 AGENT가
작성한다. 과잉 설계보다 기존 동작·근거·합의한 공개 단위를 중시한다. 사전 고정된 다회차 대본은 없다.

AGENT: 실제 Claude Code CLI Sonnet/medium. 선택형 spec/plan 예시를 명시적으로 읽게 한다.
`--safe-mode` 실행이므로 플러그인 자동 발견이나 native Skill 호출을 측정한 실험은 아니다.
도구는 Read/Glob/Grep/Write/Edit/Bash, 작업 폴더 안의 로컬 문서·구현·시험만 허용한다.
대화 파일은 비공개 추론을 제거하고 도구 입출력·최종 답을 보존한 CLI export다.

## 초기 판과 재현 경로

- maker 정책 후보: 88b367b; 사용판 codex/use-template-0023@f89a92a, 부모 82d7ad2.
- 초기 제품: codex/exp-0023-base@f35b19e. 사용판에 34f41ee의 tracker.py, tests/test_tracker.py,
  requests.json, USAGE.md 네 파일과 새 EXPERIMENT.md·intent만 추가했다. baseline 3시험 PASS.
- 실험 초기 worktree: /Users/jake/Projects/ai-native-sdlc-exp-0023-base.
- 실제 제품 저장소: /Users/jake/Projects/ai-native-sdlc-exp-0023-product. 별도 clone 후 원격 제거,
  main을 초기 판에 만들었다. 작업은 이 main에서 파생한다. maker의 main을 통합 대상으로 쓰지 않는다.
- 첫 문서 작업: exp/f03-plan, /Users/jake/Projects/ai-native-sdlc-exp-0023-plan.

정확한 초기 요구와 역할은 위 초기 판의 EXPERIMENT.md와 intent/f03-owner-insights/intent.md에
있다. 실제 사람 요청은 turn-*.md와 cli/*-prompt.txt에 보존한다. 후속 요청은 바로 앞 결과를 읽고 쓴다.
실행 결과와 판정은 [result.md](result.md)에 기록했다. 계획한 상태와 실제 성공을 구별한다.

## 관측 범위

Plan/Build/로컬 순차 통합/모의 공개와 중단/제어 제거의 부분 프로세스 실험이다. 서버의 인증된 대상
판별, 네트워크 API 우회, 백그라운드 작업, DB 이행, hosted PR/CI, 실제 운영 배포·관측 기간은
시험하지 않는다. 로컬 환경 변수는 프로세스 운영자의 선택이지 CLI 사용자에 대한 보안 장벽이 아니다.
코드 판은 고정한 채 환경 설정을 바꾸는 관측을 공개 이벤트에 대응시킨다.
