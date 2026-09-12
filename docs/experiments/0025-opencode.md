# 0025 — OpenCode 준비 실험과 전체 개발 실험

2026-09-12. 사용자가 실행을 승인했다. **준비 실험을 마쳤고 전체 F04 개발을 시작한다. 전체 제품 판정은 아직 없다.**
설계 정본은 [OpenCode 실험 설계](../research/opencode-compatibility/experiment/README.md)다.

## 실행 방법

먼저 작은 공개 label helper로 스킬 읽기, 제품 질문과 같은 session 재개, 선행 시험/수정,
독립 검증자 전달·대기, 공개 사건 수집을 확인한다. 이것은 부분 준비 실험이다.
F04와 별도의 코드·질문을 쓰며 전체 intent/spec/plan 사슬 생략을 HUMAN이 명시한다.
명시적 tdd/verifier 호출은 기술 경로 검증이며 자연 선택 성공으로 계산하지 않는다.

준비에서 드러난 설치·권한·모드·출력 수집 문제를 수정하고 결과를 남긴 뒤 새 F04 clone/session을 시작한다.
F04는 사용판 d4d2153, 데이터 v6.0.0/seed102, 팀 스킬 원본 0.1.5에 고정한다.
native 14개와 파일 2개를 제공하며 적용할 것은 AGENT가 선택한다.
Codex는 HUMAN, OpenCode는 개발 AGENT다. 고정 대본이나 자동 후속 판단은 없다.
최초 문서 작성/수락 뒤 새 구현 세션, 두 PR의 로컬 통합, 첫 요약 구현 뒤 JSON 요구 추가,
독립 검토·전체 회귀·같은 소스 OFF→ON→OFF와 인도를 관측한다.

## 시작 조건

- 시작: 2026-09-12 01:51:18 UTC. 준비/복구 포함 제안 상한 03:21:18 UTC 또는 HUMAN 16턴.
- OpenCode 1.18.30. 연결된 OpenCode Go를 사용한다. 실제 확인한 모델 목록에서
  `opencode-go/gpt-5.6-luna`가 tool call과 medium/high reasoning을 제공한다.
- 준비 개발 medium, 교차 자료 검토 high. 실제 모델·옵션·결과는 각 turn metadata와 대조한다.
- 개인 영구 설치는 변경하지 않는다. 외부 프로젝트 경로/네트워크와 push/merge는 AGENT에 허용하지 않는다.
  로컬 통합은 HUMAN이 판단해 수행한다. 경로·권한 설정을 OS 격리로 표현하지 않는다.
- 제품 작업 루트: `/Users/jake/Projects/ai-native-sdlc-opencode-20260912/`.
- 진행 중 운영/공개 출력: `/Users/jake/Projects/ai-native-sdlc-experiment-private/0025-opencode/`.
  공개 자료는 마감 때 실험 refs에 보존한다. 비공개 HUMAN 입력은 제품에 넣지 않는다.

[run-opencode.py](../research/opencode-compatibility/experiment/run-opencode.py)는 한 HUMAN 요청을
전달하고 공개 text/tool/result 사건만 보존한다. 다음 응답 선택·검토·수정·채점을 하지 않는다.
reasoning/signature는 쓰기 전 제외한다. 출력 수집 검사는 이 부분을 확인하는 기술 검사다.

## 결과

### 준비 실험과 방법 보완

1. pilot-01은 subprocess cwd만 지정했고 inherited PWD는 maker였다. 실제 도구가 maker를 읽어
   환경 오염으로 판정했다. 중단을 시도할 때는 이미 rc0으로 종료돼 있었다(34.467초).
   원인을 PWD 사용으로 추정하되 내부 구현까지 확인한 것은 아니다. 전달기에 `run --dir` 명시와
   cwd/PWD 일치를 추가하고 새 session에서 재시험했다. rc0만으로 올바른 작업 공간을 판단하지 않는다.
2. 설치 중 ux-copy 초안 patch의 hunk count 오류가 발견됐다. 수정된 patch를 완성된 staging 원본에
   먼저 적용해 검증하고 복사하는 방식으로 보완했다. SKILL과 PROVENANCE를 함께 바꾸는 patch를
   단일 target 파일로 적용하지 않는다. 제작 중인 patch를 동시에 읽었던 준비 문제도 남긴다.
3. pilot-01b는 `ses_f6ca9800fffeEfqaU0HB9HXbaL`에서 실제 native tdd와 올바른 pilot 파일을 읽고
   대소문자 결정을 질문했다(10.947초). pilot-02는 같은 session에서 HUMAN 답을 받고 실제 시험
   1통과/2실패→최소 구현→3통과를 수행했다(91.773초).
4. native task가 `ses_f6ca6bd56ffeODWTH7vgpyPd5f`를 생성해 현재 파일·diff·시험을 확인했고
   부모는 결과를 기다린 뒤 보고했다. 검증자도 과거 test-first 순서는 최종 tree만으로 증명할 수 없다고
   구분했다. HUMAN은 실제 공개 도구 순서와 3시험 재실행을 대조해 이 준비 범위를 통과로 판단했다.
   pilot seed `8c31f97`, HUMAN 수락·보존 커밋 `93852aa`. 모델은 실제 task metadata의 Luna와 일치한다.
5. 큰 session export를 PIPE로 받으면 UTF-8 byte65535에서 잘리는 문제가 재발했다. 원문을 디스크에
   쓰지 않고 PTY에서 메모리로 받아 reasoning/signature를 제거한 공개 JSON만 저장했다.
   child 174290 bytes·parent 117815 bytes를 완전한 JSON으로 받았다. API/프롬프트 실패로 분류하지 않는다.

이 과정은 명시 호출·부분 작업이므로 자연 스킬 선택이나 전체 사슬 통과로 계산하지 않는다.
준비 결과와 수집 오류를 보존하고 F04는 별도 깨끗한 clone·새 session에서 시작한다.
배포 자료는 [org-skills/opencode](../../org-skills/opencode/README.md)에 포함했다.
