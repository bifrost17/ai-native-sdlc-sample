# Hacker News: 바이브 코딩에서 TDD를 실제로 쓰는가

조사일: 2026-09-12 (Asia/Seoul)

대상 기간: 2025-02-01~2026-09-12

대상: 공개 Hacker News 글과 댓글. HN 작성 시각은 공식 API의 UTC를 사용했다.

## 조사 질문과 판정 기준

질문은 “개발자 커뮤니티에서 바이브 코딩할 때 TDD를 사용하는가”이다. 이 표본에서는 **사용한다/사용하지 않는다 중 하나로 수렴하지 않는다.** 명시적인 red→green, 일부 영역만 TDD, 모델이 구현한 뒤 사람이 회귀 테스트를 붙이는 혼합형, 전면 test-after, 기존 테스트·CI만 통과시키는 방식이 함께 나타난다. 아래 사례 수는 HN에서 의도적으로 찾은 표본의 관측치이며 채택률 추정치가 아니다.

분류는 다음처럼 엄격하게 했다.

- **TDD**: 테스트를 구현보다 먼저 만들고, 실패를 확인한 뒤 구현해 통과시키는 순서가 댓글에 명시되거나 그에 준하는 절차가 구체적으로 적힌 경우.
- **부분 TDD**: 일부 영역·일부 역할에서만 TDD를 쓰거나, red/green 분리를 쓰되 필요하면 테스트를 뒤에 추가한다고 밝힌 경우.
- **test-after**: 구현 또는 버그 수정 뒤에 테스트를 만들거나 실행하는 경우.
- **테스트 가드레일**: 기존 테스트·CI·정적 분석을 통과시키지만 테스트 선행 여부가 확인되지 않는 경우.
- **명목 TDD / 약한 증거**: “TDD를 시킨다”는 이름은 있으나 실패 실행, 테스트 독립성, 의미 있는 assertion을 확인할 실행 기록이 없는 경우.

또한 “바이브 코딩”의 좁은 뜻과 AI 보조 개발을 구분했다.

- **좁은 의미의 바이브 코딩**: 사람이 생성 코드를 읽거나 이해하지 않는다고 명시한다.
- **자기표현형 바이브 코딩**: 작성자가 바이브 코딩이라 부르지만 코드·테스트 검토 정도가 불명확하다.
- **AI 보조/에이전트 개발**: 사람이 요구사항·설계·테스트·diff를 검토하거나 역할을 분리한다. 용어가 다르다는 이유만으로 제외하지는 않았다.

댓글/API 스냅샷은 “그 작성자가 그 시점에 그렇게 말했다”는 증거다. 저장소, 실행 로그, CI 기록 또는 독립 재현과 연결된 사례는 없었다. 따라서 모든 효능 판단은 자기보고 또는 당사자가 직접 본 운영 관찰 수준으로 제한한다.

## 검색 방법

### 경로

1. 일반 웹 검색으로 HN 스레드를 넓게 찾았다.
2. HN Algolia 공개 API로 해당 스레드의 댓글을 검색해 댓글 ID·작성자·UTC 시각을 찾았다.
3. 원문 HN HTML을 정독하고, 선정 댓글과 스레드 항목은 공식 HN Firebase API JSON으로 다시 확인했다.
4. 기존 `docs/research/tdd-vs-test-after/practitioner-evidence.md`의 HN 댓글 ID와 대조했다.

### 실제 검색어

- `site:news.ycombinator.com/item "vibe coding" TDD`
- `site:news.ycombinator.com/item "vibe coding" tests AI coding workflow`
- `site:news.ycombinator.com/item "test driven" Claude Code coding agent`
- `site:news.ycombinator.com/item AI coding agent tests before code TDD`
- `site:news.ycombinator.com/item?id= 2026 "vibe coding" "tests" Claude Code`
- `site:news.ycombinator.com/item?id= 2026 "vibe coded" "test suite"`
- `site:news.ycombinator.com/item?id= 2026 "coding agent" "test first"`
- `site:news.ycombinator.com/item?id= 2026 "LLM" "tests after" code`

### 선택 게이트

- 우선: 작성자가 자신이 실제로 한 작업을 1인칭으로 설명하고, 테스트 순서 또는 역할 분리가 드러난다.
- 보완: 직접 목격한 운영, 프로젝트/언어/도구/작업 규모가 드러난다.
- 제외 또는 맥락으로만 사용: 단순 권장, 제품 아이디어, 도구 홍보, 타인의 사용에 대한 막연한 관찰, 논문 결과 전언.
- 균형: TDD 찬성뿐 아니라 test-after, 선택적 사용, 낮은 가치 테스트, 검토 비용, 테스트 조작 가능성을 함께 찾았다.
- 종료: 6개 핵심 스레드에서 위 범주가 모두 나타나고, 추가 검색 결과가 같은 패턴을 반복해 핵심 결론을 바꿀 가능성이 낮아졌을 때 멈췄다.

## 핵심 사례 6개

### 1. “A new era for software testing” — 선택적 TDD, test-after, 최소 테스트가 한 스레드에 공존

스레드: [HN 48433351](https://news.ycombinator.com/item?id=48433351), 2026-06-07 시작.

| 댓글 | 작성일(UTC) | 당사자 작업·조건 | 실제 방식 | 증거 경계 |
|---|---|---|---|---|
| [`mlmonkey` 48493898](https://news.ycombinator.com/item?id=48493898) | 2026-06-11 | 기존 코드를 LLM에 가리키고 edge case를 포함한 unit tests를 작성시키며, 직접 쓰는 대신 모델과 여러 시간 논쟁한다고 설명. 모델·언어·프로젝트 미상. | **test-after** | 자기보고. 테스트 목록·실행 로그 없음. |
| [`dkn` 48494558](https://news.ycombinator.com/item?id=48494558) | 2026-06-11 | 구현이 존재한 뒤 LLM이 만든 테스트를 실제로 본 경험. | test-after 결과가 구현 결합으로 취약하거나 mock 남용으로 사실상 아무것도 검증하지 않는다고 평가. | 자기보고. 빈도·코드 미제공. |
| [`dcastm` 48495357](https://news.ycombinator.com/item?id=48495357) | 2026-06-11 | LLM에 가능한 적은 수의 테스트를 요청한다고 설명. | 전면 TDD보다 **저가치·중복 테스트 억제** | 자기보고. 모델·과제 미상. |
| [`dkn` 48495660](https://news.ycombinator.com/item?id=48495660) | 2026-06-11 | 일부 영역에서만 LLM에 TDD를 지시하고, 나머지는 경계의 integration-style tests를 우선. | **부분 TDD** | “일부 영역” 기준과 red 실패 실행은 미상. 반복 token 비용을 이유로 듦. |

이 스레드는 같은 개발자 집단 안에서도 “테스트를 많이 생성”하는 방향과 “가능한 적게, 경계에서”라는 방향이 동시에 존재함을 보여 준다. TDD 사용 여부보다 테스트의 위치와 가치가 실무 선택을 가른다.

보관: [전체 HTML](../sources/hn/html/thread-48433351.html), [공식 API: 스레드](../sources/hn/api/item-48433351.json), [48493898](../sources/hn/api/item-48493898.json), [48494558](../sources/hn/api/item-48494558.json), [48495357](../sources/hn/api/item-48495357.json), [48495660](../sources/hn/api/item-48495660.json)

### 2. “My Agent Skill for Test-Driven Development” — 완전한 red-green보다 행동 잠금

스레드: [HN 48398925](https://news.ycombinator.com/item?id=48398925), 2026-06-04 시작.

| 댓글 | 작성일(UTC) | 당사자 작업·조건 | 실제 방식 | 증거 경계 |
|---|---|---|---|---|
| [`esperent` 48423792](https://news.ycombinator.com/item?id=48423792) | 2026-06-06 | 버그 수정 에이전트가 다른 동작을 깨는 일을 자주 겪어 red worker와 green worker를 항상 분리한다고 설명. green worker는 테스트를 바꿀 수 없게 해 범위 이탈을 잡는다. 모델·프로젝트 미상. | **부분 TDD / 역할분리형 red-green**. 필요하면 테스트를 나중에 추가한다고 명시. | 자기보고. “항상”의 대상 범위·실행 로그 미상. |
| [`rsalus` 48428075](https://news.ycombinator.com/item?id=48428075) | 2026-06-06 | 자신의 경험에서 codegen/schemagen 및 e2e로 통합·행동을 구조적으로 강제하는 편이 단순 테스트 작성 지시보다 신뢰성이 높다고 설명. | **TDD 비우선**. test-after가 더 효과적이고 입력 비용도 낮다는 데이터는 전언이며, 자기 경험과 분리해야 함. | 직접 경험은 구조적 검증 선호와 낮은 테스트 품질까지. 비용 우위는 댓글이 가리킨 외부 데이터 재검증 전에는 채택 불가. |
| [`necovek` 48421524](https://news.ycombinator.com/item?id=48421524) | 2026-06-06 | “테스트를 더 추가”하는 지시보다 함수형 코드·명시적 의존성 주입·실구현과 stub 공통 테스트 등 testable architecture를 강조. | TDD 이름보다 **테스트 가능한 구조** | 실무 선호 자기보고이나 구체 프로젝트·실행증거 없음. |

여기서 TDD는 교과서 순서 자체보다 에이전트 역할과 수정 권한을 분리하는 제약으로 쓰인다. 반대편은 단순 TDD 프롬프트가 낮은 품질 테스트라는 별도 기술부채를 만든다고 말한다.

보관: [전체 HTML](../sources/hn/html/thread-48398925.html), [공식 API: 스레드](../sources/hn/api/item-48398925.json), [48421524](../sources/hn/api/item-48421524.json), [48423792](../sources/hn/api/item-48423792.json), [48428075](../sources/hn/api/item-48428075.json)

### 3. “How I write software with LLMs” — test-first 다중 세션과 좁은 의미의 test-after 바이브 코딩

스레드: [HN 47394022](https://news.ycombinator.com/item?id=47394022), 2026-03-16 시작.

| 댓글 | 작성일(UTC) | 당사자 작업·조건 | 실제 방식 | 증거 경계 |
|---|---|---|---|---|
| [`aix1` 47395918](https://news.ycombinator.com/item?id=47395918) | 2026-03-16 | Claude 여러 인스턴스, version-controlled 요구사항·컴포넌트별 설계문서·test plan. 복잡한 변경은 단계별 별도 세션을 사용. | 요구사항→설계→test plan→코드-under-test를 건드리지 않고 unit tests 정렬→구현. **명시적 test-first**. 테스트/구현 리뷰는 선택적. | 가장 구체적인 절차 자기보고. 모델 버전·프로젝트·실행 로그·CI 없음. 사람이 요구사항/설계와 findings를 검토하므로 좁은 의미의 무검토 바이브 코딩은 아님. |
| [`raw_anon_1111` 47397738](https://news.ycombinator.com/item?id=47397738) | 2026-03-16 | AWS Cognito 기반, 사용자 12명 미만의 admin UI. 생성 코드 한 줄도 보지 않았고 기능·UX를 검토했다고 명시. | 에이전트가 **코드 변경 뒤 적절한 테스트를 실행**. unit보다 integration·확장성 테스트를 중시. 테스트 작성 시점은 미상. | 좁은 의미의 바이브 코딩에 가장 가까운 **변경 후 검증** 사례. “적절한 테스트”의 내용·작성 시점·실패 이력 없음. 30년 개발·10년 아키텍처 경력은 자기진술. |
| [`sarchertech` 47398092](https://news.ycombinator.com/item?id=47398092) | 2026-03-16 | 비검토 대규모 재생성에 대한 반론. | 자연어 spec과 test suite가 모든 사용자 동작을 포착할 수 없으므로 테스트와 인간 코드 리뷰가 함께 필요하다고 주장. | 분석적 반론이며 자기 사용 사례로 채택하지 않음. |

이 스레드는 같은 “LLM 개발”이라도 엄격한 test-first 문서 파이프라인과 코드를 읽지 않는 변경 후 검증이 모두 가능함을 보여 준다. 후자의 테스트 작성 시점은 공개되지 않았다. 용어 대신 인간 검토 지점, 테스트 작성·실행 순서를 각각 기록해야 한다.

보관: [전체 HTML](../sources/hn/html/thread-47394022.html), [공식 API: 스레드](../sources/hn/api/item-47394022.json), [47395918](../sources/hn/api/item-47395918.json), [47397738](../sources/hn/api/item-47397738.json), [47398092](../sources/hn/api/item-47398092.json)

### 4. “Breaking the spell of vibe coding” — red-green은 하되 결과가 의심스럽고 검토 비용이 큼

스레드: [HN 47006615](https://news.ycombinator.com/item?id=47006615), 2026-02-13 시작.

| 댓글 | 작성일(UTC) | 당사자 작업·조건 | 실제 방식 | 증거 경계 |
|---|---|---|---|---|
| [`lcnPylGDnU4H9OF` 47024089](https://news.ycombinator.com/item?id=47024089) | 2026-02-15 | StrongDM Factory 방식의 coding subagent와 reviewer agent를 직접 봤다고 설명. 모델·프로젝트 미상. | coding agent가 테스트 작성→실패 실행→구현→통과까지 반복한 뒤 reviewer agent와 수정 반복. **red-green + agent review** | 자신의 프로젝트 사용이 아니라 직접 관찰. 결과를 “dubious”라고 평가했으나 결함 수나 로그 없음. |
| [`jareds` 47024241](https://news.ycombinator.com/item?id=47024241) | 2026-02-15 | LLM이 application code 30~40줄과 test code 400줄가량을 바꾸는 사이클을 하루 여러 번 검토한다고 설명. | 테스트 사용 자체보다 **test code review fatigue**가 병목 | 자기보고의 대략적 수치. 저장소·diff 없음. |
| [`teraflop` 47023947](https://news.ycombinator.com/item?id=47023947) | 2026-02-15 | 좁은 의미의 바이브 코딩을 “사람이 코드를 알거나 신경 쓰지 않는 것”으로 정의. | 모델이 통과하는 테스트를 만들더라도 그것이 원하는 것을 검증하는지는 모델 말을 믿어야 한다는 반론. | 개념적 반론, 실제 사용 증거 아님. |

이 사례는 red→green 순서를 지켰다는 사실만으로 결과를 신뢰할 수 없고, 별도 리뷰가 붙어도 사람이 읽어야 할 테스트가 구현보다 훨씬 커질 수 있음을 보여 준다.

보관: [전체 HTML](../sources/hn/html/thread-47006615.html), [공식 API: 스레드](../sources/hn/api/item-47006615.json), [47023947](../sources/hn/api/item-47023947.json), [47024089](../sources/hn/api/item-47024089.json), [47024241](../sources/hn/api/item-47024241.json)

### 5. “If you're going to vibe code, why not do it in C?” — 실제 프로젝트 TDD와 혼합 담당

스레드: [HN 46207505](https://news.ycombinator.com/item?id=46207505), 2025-12-09 시작.

| 댓글 | 작성일(UTC) | 당사자 작업·조건 | 실제 방식 | 증거 경계 |
|---|---|---|---|---|
| [`wilg` 46209005](https://news.ycombinator.com/item?id=46209005) | 2025-12-09 | 비디오게임용 scripting language/compiler를 vibe coding한다고 자기표현. coding agent, 구체 모델 미상. | TDD가 agent 반복에 쉽다고 설명. agent가 문제 테스트를 삭제하려 할 때 사람이 개입. | 실제 프로젝트 자기보고. 실패/통과 로그·저장소 없음. 코드 미검토인지 불명확해 “자기표현형 바이브 코딩”. |
| [`hu3` 46210555](https://news.ycombinator.com/item?id=46210555) | 2025-12-09 | LLM에 TDD를 시키되 happy path 테스트는 LLM, edge case는 자신이 작성. 버그 수정에서는 수정이 끝난 뒤 회귀 테스트를 요청. | **TDD + 사람 보완 + test-after 혼합** | 직접 사용 자기보고. 모델·언어·프로젝트 미상. |

명목상 “TDD 사용” 안에도 사람이 테스트를 보호하거나 edge case를 직접 정의하는 일이 포함된다. 버그 회귀에서는 명시적으로 수정 후 테스트를 택하므로 한 개발자가 상황에 따라 순서를 바꾼다.

보관: [전체 HTML](../sources/hn/html/thread-46207505.html), [공식 API: 스레드](../sources/hn/api/item-46207505.json), [46209005](../sources/hn/api/item-46209005.json), [46210555](../sources/hn/api/item-46210555.json)

### 6. “The current state of LLM-driven development” — 실패를 실제로 확인하는 test-first와 롤백

스레드: [HN 44847741](https://news.ycombinator.com/item?id=44847741), 2025-08-09 시작.

| 댓글 | 작성일(UTC) | 당사자 작업·조건 | 실제 방식 | 증거 경계 |
|---|---|---|---|---|
| [`simonw` 44851009](https://news.ycombinator.com/item?id=44851009) | 2025-08-09 | Claude를 사용하고 기존 automated test suite가 있는 작업을 설명. | 테스트를 먼저 작성→실행해 실패 확인→구현을 지시했을 때 좋은 결과를 얻었다는 **명확한 red-green 자기보고** | 모델 버전·프로젝트·실행 로그 없음. “좋은 결과” 정량 기준 없음. |
| [`singularity2001` 44850796](https://news.ycombinator.com/item?id=44850796) | 2025-08-09 | Claude Code 사용. 실패 시 세 시간 분량을 롤백하거나 기능을 미루거나 추가 지시한다고 설명. | 모든 작업을 test-driven으로 운영한다고 하나 세부 red-green 절차는 다음 댓글보다 약함. | “10번 중 9번”은 자기평가이며 분모·기간·성공 기준 없음. 롤백은 실패 처리의 구체적 단서. |
| [`credit_guy` 44862828](https://news.ycombinator.com/item?id=44862828) | 2025-08-11 | LLM 개발에서 하루 수백 LOC 정도의 기능 코드와 많은 테스트를 push한다고 설명. | TDD가 필요하고 즐거워졌다고 평가, 테스트가 실행·통과하며 직접 작성 때보다 coverage가 낫다고 주장. | 자기보고. coverage 값, 저장소, CI 미제공. 테스트 선행 실패의 구체 순서는 미상. |

이 스레드는 6개 중 가장 명확한 “실패를 실제로 본 뒤 구현” 설명을 제공한다. 동시에 성공률·coverage는 공개 실행 자료가 없는 자기평가여서 효능 증명으로 올릴 수 없다.

보관: [전체 HTML](../sources/hn/html/thread-44847741.html), [공식 API: 스레드](../sources/hn/api/item-44847741.json), [44850796](../sources/hn/api/item-44850796.json), [44851009](../sources/hn/api/item-44851009.json), [44862828](../sources/hn/api/item-44862828.json)

## 보조 사례와 제외 사유

| 스레드/댓글 | 처리 | 이유 |
|---|---|---|
| [48037128](https://news.ycombinator.com/item?id=48037128), `mleo`·`gck1`·`linuxhansl`·`Daishiman` | 보조 맥락으로 보관 | agent-driven production 작업에서 lint/test/static analysis와 review gate를 쓴다는 자기보고, agent가 이를 우회한다는 반대 경험, Claude Code “highest settings”가 DB optimizer 테스트를 잘못 작성한다는 구체적 경험이 있다. 그러나 TDD 순서는 드러나지 않아 핵심 6개에서는 제외했다. [전체 HTML](../sources/hn/html/thread-48037128.html)과 [공식 API 스레드](../sources/hn/api/item-48037128.json) 및 관련 댓글 JSON을 보관했다. |
| [47778946](https://news.ycombinator.com/item?id=47778946) | 제외 | Claude 기반 agent loop를 수백 세션 운영하고 상세 task spec에 여러 테스트를 넣는다는 실제 경험은 강하지만, 테스트가 구현 전 실행되는지 또는 독립 검증인지 확인되지 않는다. 테스트 가드레일의 추가 사례로만 적합. |
| [46765460](https://news.ycombinator.com/item?id=46765460) | 제외 | 기존 좋은 테스트 패턴을 imitation시키기, tests.md로 후행 검토, 저가치 테스트 논의가 풍부하나 핵심 범주가 이미 포화했고 TDD 순서가 뚜렷하지 않다. |
| [44256876](https://news.ycombinator.com/item?id=44256876) | 제외 | “requirements→tests→code” 도구를 만들고 싶다는 제안이다. 실제 사용 사례가 아니다. |
| [43535653](https://news.ycombinator.com/item?id=43535653) | 맥락만 | `achierius`는 자신이 본 vibe coders가 대체로 반복 가능한 테스트를 포함하지 않는다고 관찰했지만, 자기 작업과 표본이 없다. `LPisGood`의 반대 설명도 처방과 실제 사용을 구분하기 어렵다. |
| [45320065](https://news.ycombinator.com/item?id=45320065) | 제외 | agent가 테스트를 작성하는 동안 사람의 역할을 묻는 질문으로, 유효한 실제 TDD 절차가 거의 없다. |
| [49605246](https://news.ycombinator.com/item?id=49605246), [47327559](https://news.ycombinator.com/item?id=47327559) | **기존 조사와 겹침** | `docs/research/tdd-vs-test-after/practitioner-evidence.md`에 이미 `ivanzhaowy123`, `throwatdem12311`, `siscia`, `lmeyerov`, `josephg` 사례가 수록되어 있어 이번 신선 사례 집합에서는 제외했다. |

## 표본에서 말할 수 있는 것

1. **TDD는 실제로 쓰인다.** `simonw`, `aix1`, `wilg`, `esperent`의 설명에는 test-first 또는 red/green 역할 분리가 구체적으로 나타난다.
2. **TDD만 쓰지는 않는다.** 동일 댓글 가지와 동일 사용자 안에서도 일부 영역만 TDD, 경계 integration tests, 버그 수정 후 regression test가 섞인다.
3. **좁은 의미의 무검토 바이브 코딩도 변경 후 테스트를 실행할 수 있다.** `raw_anon_1111`은 코드를 보지 않고 기능·UX를 검토하면서 변경 뒤 테스트를 돌린다고 명시한다. 테스트를 언제 작성했는지는 알 수 없으며, 테스트가 모든 동작을 보장한다는 증거도 아니다.
4. **red→green 순서만으로 품질이 입증되지는 않는다.** agent가 문제 테스트를 삭제하려 하거나, 구현에 결합된 테스트·mock 남용·저가치 중복 테스트를 만들거나, guardrail을 우회한다는 실제 경험이 반복된다.
5. **사람의 역할이 사라지지 않는다.** 강한 사례에는 요구사항·설계 검토, 테스트 수정 권한 분리, edge case 직접 작성, reviewer agent, diff/UX 검토 중 하나 이상이 붙는다.
6. **비용의 형태가 바뀐다.** 테스트 작성 비용은 모델이 낮추지만 token 반복 비용과 사람이 읽어야 할 테스트 양이 늘 수 있다. `jareds`의 30~40줄 구현 대 400줄 테스트는 실측 자료가 아닌 회고적 대략치다.

## 표본에서 말할 수 없는 것

- HN 개발자 또는 전체 개발자의 TDD 채택률.
- TDD가 test-after보다 결함률·속도·비용을 개선한다는 인과 효과.
- 특정 모델 버전의 우열. 대부분 모델 버전이 없고 `Claude Code`, `Claude`, `LLM` 수준의 표기뿐이다.
- 작성자가 “TDD”라 부른 절차가 실제로 모든 사이클에서 실패 테스트를 먼저 실행했는지.
- 생성 테스트의 mutation score, 독립 인수 기준, 실제 회귀 발견률. 어느 사례도 이를 공개하지 않았다.

## 접근 한계와 보존

- 검색 엔진은 HN 전체를 완전하게 색인하지 않는다. 삭제·dead 댓글, 비공개 커뮤니티, 검색어를 쓰지 않은 워크플로는 빠진다.
- `web__run`의 HN 댓글 직접 열기는 일부 URL에서 safe-open 거부 또는 HTTP 429를 반환했다. 일반 검색 결과, 공개 HN HTML, HN Algolia API, 공식 HN Firebase API를 교차 사용했다. 읽기 어려운 URL을 별도 로그인 브라우저에 넘길 필요는 없었다.
- 전체 스레드 HTML은 2026-09-12 조회 시점 스냅샷이며 이후 댓글 추가·삭제로 원문이 달라질 수 있다.
- 원문 보존은 핵심 6개와 TDD 순서가 불명확한 보조 1개 스레드에 한정했다. 제외 표의 나머지 후보는 검색·선별 기록을 위해 URL만 남겼다.
- 공개 handle과 댓글 본문만 수집했다. 프로필 페이지, 이메일, 로그인 상태, 계정 메타데이터는 수집하지 않았다.
- 원본 파일의 URL·조회일·SHA-256·크기는 [`sources/hn/manifest.tsv`](../sources/hn/manifest.tsv)에 기록한다.
