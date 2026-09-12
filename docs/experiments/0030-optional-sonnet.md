# 0030 — 최신 선택형의 Claude Sonnet 실험

2026-09-12, 모델 실행 전 고정한 계획. 사용자 요청: 최신 템플릿으로 Claude Sonnet 대상 실행.
북극성은 [플레이북](../verification/north-star-playbook.html)이며 사람이 함께 주요 흐름을 대체로
잘 따르는 수준을 목표로 한다. 모델 오류마다 새 정책·검사기를 추가하지 않는다.

## 고정 조건

- source `4bb463d7ee900e9ec687f400474aabbcb948b839`, `tdd-optional/project`와 팀 패키지0.1.2.
- 순수 사용판에는 활성 스킬/훅/제작 자료가 없다. 별도 seed에 작성 예시3개와 완결된 팀 플러그인을
  선택 배치하고 Claude Code의 `--plugin-dir`로 실행별 로드한다. 전역 설치 갱신 실험은 아니다.
- 개발자와 native 검증자는 Claude Sonnet/medium. 기본 Opus/high verifier의 실험 사본만 모델·effort를
  조정하며 본문은 유지한다. 실제 모델·호출·대기는 공개 실행 증거로 따로 확인한다.
- HUMAN은 [PERSONA](PERSONA.md)의 Codex root. AGENT는 Claude Code. 고정 대본 없이 제출과 질문에 반응한다.
- [0029](0029-optional-opencode.md)와 같은 F04 v6/seed102 및 v1 baseline3시험.
  D1–D6을 초기 업무 설명으로 제공한다. D7 JSON은 PR2 최초 코드·시험을 직접 확인한 뒤 처음 공개한다.
  HUMAN-only oracle/기존 결과는 제품에 넣지 않는다. v6의 일괄 RED 평가는 이번 선택형에 적용하지 않는다.
- 초기 방법은 AGENT가 선택한다. TDD 미선택 자체는 실패가 아니며 명시적 비TDD 별도 실험을 강제하지 않는다.
- 사용판→seed→문서→PR1→통합→PR2→통합 브랜치와 실제 SHA, 원본 입력·대화·공개 사건·판정을 보존한다.
  hosted PR/CI·실제 운영 배포·원격 push는 범위 밖이다.

## 진행과 중단 기준

의도→spec→plan을 실제 검토·수락하고 두 작은 PR로 구현한다. 필요한 질문·수정은 같은 세션에 답한다.
후속 JSON 요청은 파일명·스킬·문서 순서를 상기하지 않는 업무 요청이다. 최신 코드·문서·검토와
독립 동작 검증 후 HUMAN이 통합하고 새 디렉터리에서 같은 소스의 OFF→ON→OFF를 확인한다.

첫 개발 CLI 시작부터 root 호출 **최대8회 또는60분**. 최초 계획은6호출이며2회는 실제 질문·발견 복구에
사용한다. 도구 설정 실패도 기록하며 성공할 때까지 예산을 늘리지 않는다. 모델 사용 불가·시간 초과·
미해결 기능 오류이면 미완료 범위를 남긴다. 필요한 최소 보완과 부분 재시험도 같은 예산 안에서 한다.

## 판단과 비교

고정 설명·원문·양식은 기존 정적 검토와 source 동일성을 재사용한다. 동적 평가는 단계 인계·실제 파일과
PR 의존성·방식 선택/독립 기대/실제 순서·문서 선행 갱신과 같은 커밋·스킬 사용·native 검토와 최신 변경·
전체 회귀/통합/인도를 포함한다. 검토자가 현재 테스트 수로 과거 실행을 재작성하는지도 관측한다.

0029와 같은 데이터라도 CLI·모델·추론·플러그인 전달·문맥이 다르다. 특히 0029 전체 실행은0.1.1,
0030은0.1.2이므로 모델만의 인과 비교나 성공률·우열 판단은 아니다. 0029의0.1.2 부분 사례와도
시작 범위·HUMAN이 명시한 방식이 다르다. 최초 실패와 사람의 복구를 통과 뒤에도 남긴다.

원본: `/Users/jake/Projects/ai-native-sdlc-experiment-private/0030-optional-sonnet/`.
제품: `/Users/jake/Projects/ai-native-sdlc-sonnet-optional-20260912/`.
실행 후 소스·설치·모델·결과·refs를 아래에 기록한다.

## 첫 호출: 인증 차단, 모델 실험 미실행

설치 준비와 사전 정적 검토는 완료했다. 순수 사용판 `ab83dcc`는 source의 제품 tree와 동일하며,
입력·정책·선택 설치 seed는 `dd48653`이다. 팀13개와 작성3개 스킬을 완결 폴더로 배치했고 원본
플러그인·실험 플러그인·작성 스킬의 strict validation 및 baseline3시험이 통과했다.

Claude Code2.1.265 첫 호출은 2026-09-12 11:51:50 UTC에 시작해 약1.3초 뒤 rc1로 종료했다.
오류는 `Failed to authenticate: OAuth session expired and could not be refreshed`다.
`claude auth status`도 loggedIn=false를 반환했다. 현재 실행 환경에는 Anthropic/Claude 인증 환경변수가
없고 사용자 설정에 apiKeyHelper도 없었다. 다른 모델이나 인증 수단으로 대체하지 않았다.

init은 `sonnet` 별칭을 `claude-sonnet-5`로 해석하고 inline 플러그인0.1.2, 선택한16개 스킬과
namespaced verifier를 등록했다. 그 밖의 내장/전역 스킬 이름도 목록에 있어 완전 격리로 표현하지 않는다.
**실제 assistant model은 오류용 `<synthetic>`뿐이고 도구 호출은0회다.** 모델 실행·스킬 본문 사용·
의도 작성·검토·제품 구현은 모두 미실행이며 init의 모델명이나 설치 통과를 실행 성공으로 세지 않는다.
제품은 seed에서 변경되지 않았다. 공개 첫 실패는 `raw/01-intent.jsonl`과 meta에 보존했다.

이 시도는 인증 차단으로 종료한다. 재인증 후 기존 실패를 덮지 않는 새 실행 번호·브랜치와 시간 예산을
먼저 기록하고 같은 고정 seed·업무 데이터로 시작한다. 재개 전 실제 auth 상태와 source 변경 여부를
확인한다. 이 단계에서는 북극성의 실행 평가나 통과 주석을 갱신하지 않는다.

제작 저장소에 `codex/use-template-optional-sonnet-0030@ab83dcc`,
`codex/experiment-0030-sonnet-seed@dd48653`,
`codex/experiment-0030-sonnet-auth-blocked@dd48653`를 보존했다. private `refs.json`은 전체 SHA,
두 `.bundle`은 검증한 Git 보관본이다. `README.md`에 입력·설치·로그·인증 상태·재개 절차를 연결했다.
독립 Sol 사전 리뷰는 정적 준비를 확인하고 인증 차단을 재확인했으며, 실행 통과로 판정하지 않았다.

## 사용자 요청에 따른 재시도 r02

사용자는 Claude Code가 정상이라며 재시도를 요청했다. 첫 상태 조회는 false였지만 이어서 PTY와
일반 subprocess 모두 loggedIn=true를 확인했다. CLI는2.1.269다. root가 로그인이나 자격 증명을
변경한 것은 아니며 상태 전환의 원인은 확인하지 못했다. 최초 실패를 현재 상태로 일반화하지 않는다.

첫 모델 실행 전에 새 시도 `r02/`와 새 제품 `f04-r02/`, `codex/sonnet-r02-docs`를 만들었다.
동일 고정 seed `dd48653`에서 시작하며 모델·검증자·업무 조건은 유지한다. 이전 실패와 예산은 그대로
보존하고 사용자 재시도의 예산을 새로8호출/60분으로 고정한다. 이것은 제품 실패를 지우는 재시험이
아니며 첫 시도에는 모델 개발이 없었다. raw와 metadata를 덮지 않는 새 세션으로 시작한다.
