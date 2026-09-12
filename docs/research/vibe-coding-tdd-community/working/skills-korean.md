# 국내 공개 경험: 바이브 코딩에서 TDD 스킬을 실제로 쓰는가

- 조사일: 2026-09-12 (Asia/Seoul)
- 대상 기간: 2025-02-01 ~ 2026-09-12
- 질문: 국내 개발자의 공개 글에서 Superpowers의 `test-driven-development` 또는 개인 TDD 스킬을 실제 선택·사용·중단한 경험을 확인할 수 있는가?
- 결론 강도: **실제 TDD 스킬 사용이 분명한 사례는 커스텀 플러그인 1건이다. Superpowers를 실제 사용한 2건은 프레임워크 사용은 분명하지만 공개 글만으로 TDD 하위 스킬 호출과 작은 Red-Green-Refactor(RGR)를 끝까지 입증하지 못한다.** 따라서 국내 사용률은 산출할 수 없다.

## 판정 기준

다음 세 층을 분리했다.

1. **TDD 스킬 실제 사용**: 스킬·플러그인 이름 또는 호출 명령이 있고, 작성자가 자기 작업에 사용했다고 밝히며, 테스트 우선 실행 흔적이 있다.
2. **스킬 프레임워크 실제 사용, TDD 하위 스킬은 부분 증거**: Superpowers를 켜고 비교하거나 계속 사용했다고 하지만, `test-driven-development` 호출 로그 또는 테스트가 먼저 실패한 기록은 없다.
3. **구성·소개·프롬프트**: 설치 화면, README/AGENTS 지침, 예제 프롬프트, 도구 설명만 있다. 실제 TDD 스킬 사용 사례 수에는 넣지 않는다.

테스트 파일이 존재하거나 최종 테스트가 통과한 사실만으로 TDD로 판정하지 않았다. 여러 테스트를 한꺼번에 쓴 뒤 구현한 방식도 엄격한 작은 RGR과 구분했다.

## 채택 경험 3건

### 1. 김예림·비브로스: 개인 `tdd-pipeline` 스킬을 한 달간 실제 기능에 사용

- 게시일/작성자: 2026-06-10, 김예림
- 원문: https://boostbrothers.github.io/2026-06-10-claude-code-tdd-subagent-harness/
- 고정본: `../sources/skills-korean/boostbrothers-tdd-subagent-harness.html`
- 도구·스킬: Claude Code 팀 플러그인, `/tdd-pipeline:install`, `/tdd-pipeline:run`, 7개 역할 에이전트
- 사용 상태: **실제 사용·계속 개선**
- 판정: **개인 TDD 스킬 실제 사용**

작성자는 일정과 요구 변경 때문에 사람 개발에서는 TDD를 거의 쓰지 않았지만, Claude Code가 신규 기능에서 엣지 케이스를 빠뜨리고 구현에 맞춘 테스트를 만들거나 요청하지 않은 migration을 수행한 뒤 운영 버그까지 낸 경험 때문에 2026년 5월 초 하네스를 만들었다. 글은 팀 플러그인 구조와 두 개의 사용자 호출 스킬을 명시하고, `/tdd-pipeline:run docs/specs/<feature>.md`를 진입점으로 제시한다. 한 달간 실제 기능에 사용했다고 밝히며, 시나리오·Red·Green·리뷰·완료 게이트별 파일과 명령 결과 확인, 18종 회귀 평가를 공개한다.

이것은 단순 AGENTS 프롬프트나 CI test runner가 아니다. 사용자가 호출하는 스킬이 오케스트레이터를 시작하고, 역할별 도구 권한과 증거 게이트로 프로덕션 코드와 테스트 수정을 나눈다. 다만 `test-writer`와 `implementer` 자체는 스킬 파일이 아니라 플러그인 에이전트이고, 여러 실패 테스트를 묶어 만든 뒤 구현 단계로 넘어간다. Refactor도 선택 단계다. 따라서 **명시적 커스텀 TDD 스킬/하네스 사용**에는 해당하지만 Superpowers의 한 테스트 단위 strict RGR과 동일하지 않다.

비용과 한계도 구체적이다. 정의가 약 600줄로 커져 토큰 비용과 규칙 희석 위험이 있고, Bash로 파일을 바꾸는 우회는 막지 못해 사후 검사한다. TypeScript/Jest 외 언어와 팀 전체 확산은 미검증이다.

### 2. 햄스터아저씨: Superpowers 켠/끈 비교 후 조건부 사용 권고

- 게시일/작성자: 2026-03-29, 햄스터아저씨
- 원문: https://blog.hamsterapp.net/review-claude-code-superpowers/
- 고정본: `../sources/skills-korean/hamster-superpowers-review.html`
- 도구·모델: Claude Code, Claude Opus 4.6(1M), Superpowers
- 사용 상태: **비교 실험을 수행하고 조건부 사용을 권고; 일상 작업에서 지속적으로 켜고 끄는지는 미공개**
- 판정: **Superpowers 실제 사용, TDD 하위 스킬은 부분 증거**

같은 날 세 과제(파이썬 비밀번호 CLI, Pomodoro HTML, 퀴즈 HTML)를 “그냥 만들어줘”와 “Superpowers 워크플로우”로 비교했다. CLI는 Superpowers를 쓴 결과 28개 테스트가 생겼다. 세 과제 합계는 미사용 36,975토큰·179초, 사용 60,239토큰·483초로, 작성자 계산상 토큰 63%, 시간 170%가 늘었다. 이는 공개 저장소 재현이 아니라 작성자의 단일 세션 관찰값이다.

작성자는 비교 후 일회성 스크립트·프로토타입에는 비용이 과하고, 프로덕션·장기 유지·자율 실행·테스트 요구가 있는 작업에는 가치가 있다고 판단했다. 이는 조건부 사용을 권하는 판단이며, 이후 일상 작업에서 실제로 켜고 끄는 관행까지 밝힌 것은 아니다.

그러나 글이 공개한 워크플로우는 스펙→계획→구현→자기 리뷰까지이며 `test-driven-development` 호출 로그가 없다. 테스트도 CLI 과제에서만 보고됐고 웹 두 과제에는 테스트 수가 없다. 28개 테스트가 구현 전에 하나씩 실패한 기록도 없다. 그러므로 **Superpowers 사용과 테스트 생성은 입증되지만, TDD 스킬의 strict RGR 실행을 입증한 사례로 세면 안 된다.**

### 3. Tony Cho(Flowkater): 개인 TDD 스킬을 자주 건너뛰다 Superpowers로 전환

- 게시일/작성자: 2026-02-08, Tony Cho
- 원문: https://flowkater.io/posts/2026-02-08-superpowers-introduction/
- 고정본: `../sources/skills-korean/flowkater-superpowers.html`
- 도구: Claude Code, Codex, 기존 개인 TDD Planning/인터뷰 커맨드, Superpowers
- 사용 상태: **기존 개인 스킬은 상황에 따라 생략; Superpowers는 계속 사용한다고 보고**
- 판정: **개인 스킬 사용 경험 + Superpowers 실제 사용 자기보고, TDD 하위 스킬 실행 흔적은 미공개**

작성자는 원래 인터뷰 커맨드와 TDD Planning을 직접 만들어 썼으나 병렬 작업에서 호출을 잊었고, 언어·프레임워크별 스킬 설정이 번거로워 고객사에서는 자주 건너뛰었다고 한다. 자신의 커맨드·스킬을 합친 것과 같은 Superpowers를 발견한 뒤 Claude Code의 빠른 작업과 Codex의 프로덕션 작업 모두에서 유용하며 인터뷰와 TDD 워크플로우를 적극 사용한다고 썼다. 이후에도 스킬을 추가해 사용한다고 밝혔다.

이는 “개인 TDD 스킬을 만들었는가”뿐 아니라 **왜 실제로 생략했는지**를 보여준다: 호출 망각, 병렬 작업, 환경별 설정 비용이다. Superpowers 채택은 이 마찰을 줄이려는 선택이다.

한계는 글 대부분이 제품 구조와 설치법 설명이라는 점이다. 본인 프로젝트명, 명시적 `test-driven-development` 호출, Red 실패 출력, 커밋 순서는 공개하지 않았다. “TDD 워크플로우를 적극 사용”한다는 1인칭 진술은 실제 사용 자기보고로 채택했지만, Superpowers가 특정 작업에서 하위 스킬을 자동 호출했다는 실행 증거로 승격하지 않았다. 같은 사이트의 영어판은 한국어 원문의 번역본이므로 중복 사례가 아니다.

## 경계 사례와 재분류

### 갓대희: 설치·일부 단계 실행은 보이지만 TDD 단계는 설명/기대 결과

- 게시일/작성자: 2026-04-22, 갓대희
- 원문: https://goddaehee.tistory.com/581
- 고정본: `../sources/skills-korean/goddaehee-superpowers-review.html`
- 판정: **Superpowers 설치 및 브레인스토밍·계획·서브에이전트·리뷰 데모; TDD 스킬 실제 사용에서는 제외**

작성자는 user scope 설치 화면, 명시적 brainstorming 호출, 질문·설계 문서, 자동 plan 전환, subagent-driven 실행, 코드 리뷰 화면을 제시한다. 반면 Step 5 `test-driven-development`에는 공식 SKILL.md의 규칙과 “기대 결과”만 있고, 앞 단계의 `ex)` 실행 스크린샷이 없다. 설치 또는 전체 하네스 데모를 TDD 하위 스킬 실행으로 세지 않는 이유다.

### 강준현: TDD 스킬이 아니라 Copilot 재사용 프롬프트

- 원문: https://junhyunny.github.io/ai/ai-agent/copilot/prompt/improve-development-process-by-vibe-coding/
- 고정본: `../sources/skills-korean/junhyunny-copilot-prompts.html`
- 판정: **스킬 사용 사례에서 제외**

`.github/prompts/*.prompt.md`의 `/frontend-test` 등 재사용 프롬프트와 `docs/tdd-guideline.md`로 팀 절차를 작게 나눈 사례다. 실행 가능한 테스트가 있지만 Agent Skill의 `SKILL.md`, 플러그인, TDD 스킬 호출은 아니다. 기존 조사에서 “단계·권한 하네스”와 나란히 읽을 수 있어도, 이번 질문의 스킬 사용 분자에는 넣지 않는다.

### `penggu-dev/raillo-backend`: 저장소 표준 워크플로우 구성

- 원문: https://github.com/penggu-dev/raillo-backend
- 고정본: `../sources/skills-korean/raillo-readme.txt`
- 판정: **정책/구성 사례; 실제 호출 증거가 없어 제외**

README는 `superpowers:brainstorming`→`writing-plans`→`test-driven-development`→프로젝트 `/test`→`verification-before-completion`을 표준 워크플로우로 적는다. 명시적 스킬 이름은 강한 채택 신호지만, 공개 README만으로 어느 기능에서 스킬을 호출했고 Red가 먼저였는지 알 수 없다. AGENTS/README 지침을 실제 실행으로 세지 않았다.

## 사용률과 설문

검색에서 국내 개발자를 모집단으로 삼고 “TDD 스킬/Superpowers를 실제 사용하느냐”, 테스트 작성 순서, 스킬 활성·비활성을 함께 묻는 공개 설문은 발견하지 못했다. 이는 설문의 부재를 증명한 것이 아니라 아래 경로에서 **자격을 갖춘 설문을 만나지 못했다**는 열람 결과다. 블로그 3건은 자기 선택적으로 공개된 사례이며 분모가 없으므로 사용률, 다수/소수, 대표성을 계산할 수 없다. GitHub star·설치 수·영상 조회 수도 TDD 하위 스킬 실행률이 아니다.

## 검색 경로·채택 및 제외 기록

사용한 검색어 묶음:

- `"Superpowers" "TDD" "Claude Code" 한국어`
- `"superpowers:test-driven-development" 한국어`
- `"TDD 스킬" "Claude Code" 사용 후기`
- `"test-driven-development" "바이브 코딩" 스킬`
- `"Superpowers" 사용해보니 Claude Code TDD`
- `site:velog.io "test-driven-development" "Superpowers"`
- `"Superpowers" 제거|끄기|비활성화 TDD 한국어`
- `한국 개발자 설문 AI 코딩 TDD 스킬 Superpowers 사용률`
- `바이브 코딩 설문 TDD 테스트 우선 개발 한국`
- `site:okky.kr Superpowers TDD Claude Code`

채택 문턱은 1인칭 사용·비교·중단 경험, 구체적 스킬/플러그인 식별, 기간 내 게시, 원문 공개였다. 공식 Superpowers 페이지, 설치 가이드, Wikidocs 교재, 영상·도구 홍보, 외국 Reddit 경험, 영어 번역판 중복은 국내 실제 경험 수에서 제외했다. `1995-dev` 글은 작성자가 앱/CLI에 설치해 검증하지 않았다고 명시해 제외했다. 소개 글에 있는 “자동으로 TDD한다”는 제품 설명도 실행 증거로 취급하지 않았다.

## 답변에 쓸 수 있는 범위

국내 공개 글에서는 **TDD 스킬을 쓰는 개발자가 실제로 있다**. 가장 명확한 사례는 자기 팀용 호출 스킬과 증거 게이트를 만든 비브로스다. Superpowers도 실제 사용·비교 사례가 있지만, 공개 글이 보통 전체 워크플로우를 단위로 평가하므로 `test-driven-development` 하위 스킬이 매번 발동하고 strict RGR을 지켰는지는 거의 남지 않는다.

조건부 사용은 운영 정책과 권고에서 모두 나타난다. 비브로스는 모든 프로젝트에서 TDD를 필수로 쓰지 않을 계획이라 명시 요청 때만 호출하도록 구성했다. 햄스터아저씨는 비교 뒤 일회성·프로토타입에 비용이 과하다고 권고했다. Tony Cho는 개인 스킬을 호출 망각·환경별 설정 부담으로 실제 생략했다고 밝혔다. **명시적 선택 정책, 비교 후 권고, 실제 생략 경험**을 구분해야 하며, 이 세 사례를 국내 개발자 전체의 경향이나 비율로 일반화할 수 없다.
