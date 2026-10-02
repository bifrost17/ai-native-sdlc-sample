# 설계 탐색·UI 인계·조기 통합·검증 전략 조사

조사 기준일: **2026-10-03 Asia/Seoul**. 사용자 추가 요구를 검토한 자료이며, 템플릿 결함이나 개선 효과를 확정한 보고서는 아니다. 원저자·공식 문서 8개를 검색하고 관련 본문을 읽었다. 최신 열람일과 오래된 방법론의 발행일을 구분한다. 원문 수집 결과·해시·질의·접근 실패는 [로컬 연구 기록](../../../.local/research/openwebagent-template-history/20261003/research-methods/research-log.md)과 같은 폴더의 `manifest.json`에 보존했다.

권고 후보는 **다음 인도에 필요한 공유 계약을 정하고, 가장 위험한 연결을 일찍 실행하며, 그 결과로 설계와 검증을 고치는 것**이다. UI에서는 기존 컴포넌트를 쓰는 상호작용 탐색을, 큰 기능에서는 첫 통합 경로를 우선 검토한다. 모든 상세 설계를 선확정하거나 모든 화면을 제품 수준으로 미리 구현하는 규칙은 지지하지 않는다.

## 북극성과 현재 지침에서 출발

외부 자료는 북극성에 없는 보편 의무를 추가하는 근거로 쓰지 않는다. 아래의 “있음”은 현재 문서에 적혀 있다는 뜻이며, 실제 세션에서 읽혀 작동했다는 뜻은 아니다. 당시판·현재 배포 원본·기존 WIP의 구분은 [baseline.md](baseline.md)를 따른다.

| 판단 문제 | 북극성 본문·주석 | 현재 선택형 지침과 해석 |
|---|---|---|
| 충분한 spec과 발견의 반복 | [V3-09](../../verification/north-star-playbook.html#V3-09): 의도와 대조하고 미결을 해소/이월. [V4-11](../../verification/north-star-playbook.html#V4-11): 구현 중 달라진 계획 갱신 | [design-spec](../../../tdd-optional/project/examples/skills/design-spec/SKILL.md)은 불확실한 UI/기술 선택의 제한 탐색과 채택 시 spec/AC 개정을 이미 허용한다. 미결의 영향·해결자·필요 시점을 확인한다. 문서 길이가 충분성의 기준은 아니다. |
| 설계 단계 UI 탐색과 인계 | [V3-03](../../verification/north-star-playbook.html#V3-03): mock을 반복해 다듬고 build로 인계. 해당 주석의 팀 몫/미검증 범위 유지 | [폐기 가능한 UI 탐색 예시](../../../tdd-optional/project/examples/skills/plan/examples/disposable-ui-exploration.md)는 안정된 컴포넌트 재사용, 키보드·viewport 관찰, 채택/폐기와 제품 검증의 차이를 명시한다. HTML 파일만 허용한다거나 초기 UI 구현을 금지한다고 읽을 수 없다. |
| 전체 경계와 조기 통합 | [V4-06/07/08](../../verification/north-star-playbook.html#V4-06): 파일·순서·증명, 위험·대안, 대화 없는 구현. [V7-05/06](../../verification/north-star-playbook.html#V7-05): 독립 작업과 공유 파일 | [설계 상세](../../../tdd-optional/project/examples/skills/design-spec/references/design-depth.md)는 API·공유 의미·순서·실패·복구를, [실행 상세](../../../tdd-optional/project/examples/skills/plan/references/execution-depth.md)는 첫 인도·공유 계약 판·최신 통합 Proof를 다룬다. 실제 첫 연결 시점이 충분히 빠른지는 별도 조사 대상이다. |
| 설계 중 검증 방식 결정 | [V4-06](../../verification/north-star-playbook.html#V4-06)과 [V8-02](../../verification/north-star-playbook.html#V8-02): 계획에서 증명 수단, 작업 중 피드백 | [검증 전략](../../../tdd-optional/project/docs/TESTING-STRATEGY.md)은 독립 기대, 작업별 전략, 작은 동작의 구현·검증 반복, 탐색의 한계와 제품 Proof를 이미 연결한다. 테스트 코드의 작성 순서와 수락 기준의 선행 결정을 구별한다. |

플레이북의 “계획이 탄탄하면 대개 한 번의 패스”는 재작업 0회나 최초 설계의 영구 동결을 약속하는 수락 기준으로 바꾸지 않는다. 같은 문서의 갱신 원칙과 함께 읽어야 한다. 이 조사도 문서 선행 갱신, 실제 읽기, 조기 통합을 Git 최종판만으로 추정하지 않는다.

## 외부 근거와 적용 범위

### 1. 충분한 선행 설계와 반복 발견은 함께 필요하다

Fowler는 즉흥적인 code-and-fix를 비판하면서, 초기 구조의 큰 방향을 잡고 후속 정보에 따라 수정하는 설계를 설명한다. 특히 변경하기 어려운 결정을 줄이고 위험한 가정을 빨리 시험하는 방법을 제시한다. 이것은 “설계 생략”과 “예상 가능한 모든 상세의 동결” 어느 쪽도 정당화하지 않는다. [S1: Is Design Dead?](https://martinfowler.com/articles/designDead.html)

**팀 적용 추론:** 설계 인계 전에는 다음 구현자가 서로 다르게 해석하면 호환성이 깨질 공유 의미를 정한다. 호출 순서·권한·결과/오류·상태 소유자가 여기에 해당할 수 있다. private helper, 아직 사용하지 않을 확장점, 다음 인도와 무관한 세부 값은 필요 시점까지 남겨둘 수 있다. 미정이 첫 인도의 타당성을 바꾼다면 짧은 실행 탐색을 먼저 배치한다. 이미 정한 계약이 틀렸다는 증거가 나오면 spec과 영향 plan을 갱신한다.

**반론/한계:** 이월 자체를 좋은 설계로 평가하면 결정 비용이 구현자에게 전가된다. 반대로 모든 인터페이스·클래스·메서드를 먼저 채우면 실제 발견 전의 추측과 변경 비용이 늘어난다. “필요 시점”은 작업 의존성과 실패 영향으로 설명해야 하며, 무기한 미정이라는 뜻이 아니다.

### 2. UI의 설계 자료를 실행 가능한 상태·사용 흐름으로 넘긴다

GOV.UK는 목적에 맞는 fidelity를 선택하고, 코드 프로토타입이 현실적인 상호작용 탐색에 유용하다고 안내한다. 동시에 prototype 코드에는 production과 같은 보안·성능 기준이 적용되지 않을 수 있으므로 그대로 제품에 복사하지 말라고 명시한다. [S2: Making prototypes](https://www.gov.uk/service-manual/design/making-prototypes)

공통 컴포넌트 재사용은 이미 검증한 패턴의 이점을 살리고 중복 구현을 줄이는 공식 원칙이다. Storybook의 story는 실제 컴포넌트와 초기 props/context를 렌더하고, 클릭·입력·제출 후 결과를 검증할 수 있다. 이 방식은 실제 컴포넌트를 설계와 검증의 공통 자료로 쓰는 구체적 수단이다. [S4: Common components and patterns](https://www.gov.uk/service-manual/service-standard/point-13-use-common-standards-components-patterns), [S3: Interaction tests](https://storybook.js.org/docs/writing-tests/interaction-testing)

**팀 적용 추론:** 기존 UI가 있는 제품에서 모달·폼·표·탐색 흐름을 설계할 때는 기존 컴포넌트와 스타일/접근성 제약을 먼저 확인한다. 의미 있는 상호작용 불확실성이 있으면 격리된 story, sandbox route 또는 프로젝트가 이미 가진 실행 수단으로 초기 UI를 만들어 관찰한다. Storybook 설치를 의무화할 필요는 없다. 단일 정적 HTML도 정보 구조·배치 비교에 적합하면 계속 사용할 수 있다.

인계는 그림만으로 끝내지 않는다. 채택한 UI의 판·실행 진입점·재사용 컴포넌트, 재현 가능한 데이터/상태, 사용자 행동과 관찰 결과, 확정한 UI/API 의미, 미확인 항목을 기존 spec/plan에 연결한다. 제품으로 편입할 파일과 폐기할 가짜 데이터/adapter를 구별한다. 초기 UI 코드를 제품에 계속 쓸 수도 있지만, 제품 편입 시 코드 품질·실제 연결·회귀 검증을 통과해야 한다.

| 실행 자료 | 이번 자료가 뒷받침할 수 있는 판단 | 별도로 확인할 것 |
|---|---|---|
| 정적 mock/HTML | 배치·정보 구조·표현 비교 | 실제 컴포넌트와의 차이, 이벤트·초점·반응형 동작 |
| 실제 컴포넌트 + 가상 상태 | 해당 판의 렌더링·선택된 상호작용·상태 표시 | 실제 인증/권한·네트워크·저장·제품 CSS/라우팅과 결합 |
| 제품 경로에 연결된 얇은 기능 | 선택한 사용자 경로의 실제 연결과 효과 | 빠진 상태·환경·성능·접근성·회귀 등 합의한 나머지 AC |

**반론/한계:** prototype을 곧바로 production-ready로 부르면 검증 범위가 부풀려진다. 반대로 탐색을 무조건 폐기용 HTML로 제한하면 기존 UI가 갖는 실제 제약을 놓칠 수 있다. 사용 흐름이 이미 명확한 작은 수정에 모든 상태의 고충실도 prototype을 강제하지 않는다. 한 사람이 수행한 브라우저 관찰은 사용자 연구나 접근성 전체 감사가 아니다.

### 3. 전체 연결을 먼저 이해하고, 이른 통합 경로를 작게 만든다

Freeman과 Pryce의 공식 도서 미리보기는 walking skeleton을 통해 초기 환경·빌드·첫 end-to-end 시험을 세우고, 시스템 구조의 큰 방향을 확인한 뒤 학습에 따라 바꾼다고 설명한다. 읽은 범위는 Chapter 10 공개 미리보기이며 전체 장이나 Cockburn 원문을 읽었다고 주장하지 않는다. [S7: The Walking Skeleton](https://www.oreilly.com/library/view/growing-object-oriented-software/9780321574442/ch10.html)

Fowler의 CI는 팀의 변경을 자주 같은 mainline에 합치고 자동 build/test로 확인하는 실천이다. 각자 main을 받아오는 것만으로는 전체 통합이 아니며, 공유된 결과가 함께 검증돼야 한다. TDD는 CI의 필수 조건이 아니지만 통합 전에 검증할 시험은 필요하다. [S5: Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html)

**팀 적용 추론:** 큰 작업의 순서는 `대표 사용자 흐름·참여 경계·공유 의미 파악 → 위험한 연결을 통과하는 최소 실행 경로 → 작은 사용자 동작 확장과 반복 통합`을 기본 후보로 검토한다. 모듈 내부 구현과 병렬 분담은 유지할 수 있다. 첫 통합을 모든 모듈의 내부 완료 뒤로 미루는 선택에는 이유와 조기 대체 검증이 필요하다.

“전체 인터페이스/시퀀스 먼저”의 범위는 이번 인도에 영향을 주는 경계다. 알려진 정상 경로뿐 아니라 결과를 바꾸는 실패·취소·재시도·복구 순서를 다룬다. 모든 클래스에 UML을 추가하거나 미래 인도의 API까지 확정하는 뜻은 아니다. 초기 skeleton이 단순 health check라면 사용자 기능 완료를 주장하지 않고 무엇을 연결했는지 밝힌다. 다음 수직 조각은 사용자 행동에서 실제 결과까지 어떤 범위를 더 닫는지 설명한다.

계약 시험은 mock/double과 실제 제공자의 차이를 탐지하는 수단이다. 외부 서비스 변경 리듬에 맞는 별도 실행이나 제공자 측 검증 등 운영 방식은 경계에 따라 달라진다. [S6: Contract Test](https://martinfowler.com/bliki/ContractTest.html) **팀 적용 추론:** 공유 타입만 일치하는지에 그치지 않고 실제 소비자가 의존하는 입력·결과·오류·상태 의미를 시험한다. 스키마 일치만으로 권한, 부작용, 경합, 최종 사용자 흐름이 증명되지는 않는다.

**반론/한계:** 모든 커밋에 실외부 서비스 전체를 호출하거나 불완전 기능을 일반 사용자에게 공개할 필요는 없다. 큰 선행 인프라가 필요할 수도 있다. 그 경우 최소 경로의 무엇이 아직 가상인지, 언제 실제 경계를 연결하는지, 그때까지 어떤 위험이 남는지 계획한다. 공개 제어와 배포 가능성은 기존 프로젝트 정책을 따른다. 이 자료만으로 특정 PR 개수·기간·LOC 상한을 정하지 않는다.

### 4. 설계할 때 관측할 결과와 검증할 경계를 정한다

Google Testing Blog는 빠르고 신뢰할 수 있으며 실패 위치를 좁히는 피드백을 강조한다. 단위들이 따로 통과해도 함께 동작한다는 증거는 없으므로 좁은 통합 시험을 두고, 시스템 전체를 확인하는 소수의 시험도 남긴다. 본문의 70/20/10은 첫 추정치이며 팀마다 비율이 달라진다고 명시한다. [S8: Just Say No to More End-to-End Tests](https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html)

**팀 적용 추론:** 아래는 설계·계획에 필요한 답을 고르는 질문이다. 새 필수 양식이나 전 항목 의무 목록으로 배포할 제안은 아니다. 이번 변화에 결과를 바꾸는 경계만 선택해 기존 AC/Design/Order/Proof에 둔다.

| 설계에서 결정할 의미 | 계획에서 실행 가능하게 연결할 내용 |
|---|---|
| API의 입력·권한·거부/오류·반환 및 부작용 시점 | 소비자/제공자, 실제/가상 경계, 독립 기대, 계약 시험 또는 좁은 통합 절차 |
| 상태 소유자와 전이, 취소·timeout·재시도·중복 처리의 결과 | 상태별 fixture/사건 순서, 실패를 유도할 지점, 허용/금지 효과와 복구 관측 |
| 사용자의 시작 조건·행동·완료/실패 인지와 다음 행동 | 실제 UI 진입점·계정/권한 전제·데이터, 브라우저 단계와 기대 결과, 필요한 서버 효과 대조 |
| 영향을 받는 초점·키보드·작은 화면·loading/empty/error 표시 | 해당 컴포넌트/제품 경로에서 관찰할 순서, viewport 등 재현 조건, 스크린샷과 동작 근거의 역할 |
| 이번 인도의 끝과 보존할 인접 동작 | 작은 조각의 Done, 관련 회귀, 최신 결합 판에서 통합 Proof, 남은 AC |

테스트를 먼저 쓸지, 작은 구현 뒤 바로 검증할지, 기존 시험을 활용할지, 탐색으로 질문을 좁힐지는 작업별로 정한다. 기대값을 구현 출력에서 그대로 복사하지 않는다. 브라우저에서 버튼 클릭이 성공했다는 관찰과 서버 저장·권한·복구가 옳다는 관찰은 구분한다. 계약 시험과 컴포넌트 시험도 실제 사용자 흐름의 모든 부분을 대신하지 않는다.

**반론/한계:** 설계 단계에서 모든 테스트 본문을 작성하면 아직 불확실한 동작을 고정할 수 있다. 매 조각마다 느린 전체 E2E를 반복하는 정책도 피한다. 선택한 위험을 가장 좁게 판별하는 시험과 대표 실제 흐름을 조합하고, 실패가 나면 영향을 받는 계약·계획·구현을 고친다.

## 이력 조사에 반영할 판별 질문

아래는 후속 사건별 분석에 사용할 가설이다. 실제 접근 가능한 개발건 전수의 당시 입력·판·실행 순서와 대조한 뒤 원인을 분류해야 한다. 외부 권고와 다르다는 이유만으로 제작 프로세스 위반이나 템플릿 결함으로 판정하지 않는다.

| 가설 | 뒷받침/반박할 사건 근거 | 개선 후보를 고를 때의 경계 |
|---|---|---|
| 설계가 다음 구현에 필요한 공유 의미를 남기지 않았다 | 독립 구현자가 다른 의미로 구현한 경계, 뒤늦은 결정, 당시 spec의 관련 문장과 미정 처리 | 새 요구·정상적 학습·기존 지침 미적용·양식 부족을 구분 |
| 화면 모양은 정했지만 실제 UI 동작의 인계가 부족했다 | mock 판, 사용한 컴포넌트, 초기/실패 상태, 브라우저 관찰, 제품 편입 후 불일치 | 실제 컴포넌트 탐색으로 발견할 문제인지 확인. HTML 자체를 원인으로 삼지 않음 |
| 모듈별 완료가 쌓이고 실제 통합이 늦었다 | 최초 실제 경계 연결 시점, 각 PR의 실행 가능 경로, mock 교체 시 발견된 계약 차이, 통합 후 재작업 | 필요한 선행 인프라와 불필요한 통합 지연 구분. 내부 작업 분할 자체는 결함 아님 |
| 검증 방법/수락 의미를 너무 늦게 정했다 | 초기 spec/plan 기대, 시험 작성·실행 시점, 코드 출력을 정답으로 채택했는지, 실패 후 문서/구현 변화 | TDD 미선택과 검증 누락을 혼동하지 않음 |

채택할 만한 차이가 확인되면 **기존 지침의 짧은 보완이나 연결된 예시**부터 검토한다. 우선 후보는 (a) UI 탐색에서 실제 컴포넌트와 가상 경계의 인계, (b) 큰 plan의 첫 실제 통합 경로, (c) 설계의 결과/실패 의미와 검증 방식의 연결이다. 현재 지침으로 이미 설명되는 사건에는 중복 규칙을 추가하지 않는다. 보완 후 개발 재실험에서도 설계 준비도, 구현 결과, 독립 검증, 사람 수락을 각각 보고한다.

## 서지와 확인 범위

모두 2026-10-03 Asia/Seoul에 검색/열람했다. 상대적인 검색엔진 발행일은 사용하지 않았다. 제품 문서는 현재 페이지를 읽었으며 특정 설치 버전과의 API 호환성을 검증하지 않았다. 원문을 재게시하지 않고 요약했으며, 표의 날짜는 페이지가 표시한 발행/개정 정보다.

| ID | 저자·공식 출처와 제목 | 발행/개정 | 읽은 범위·용도 |
|---|---|---|---|
| S1 | Martin Fowler, [Is Design Dead?](https://martinfowler.com/articles/designDead.html) | 2004-05, 최초 2000-07 | Planned/Evolutionary Design, Growing an Architecture, Reversibility. 초기 구조·변경 가능성·탐색의 균형 |
| S2 | GOV.UK Design community, [Making prototypes](https://www.gov.uk/service-manual/design/making-prototypes) | 2016-10-18 | 유형 선택, code prototype, production 차이. prototype이 제품 완료라는 해석 반박 |
| S3 | Storybook, [Interaction tests](https://storybook.js.org/docs/writing-tests/interaction-testing) | 페이지에 발행일 없음, 갱신형 문서 | 실제 컴포넌트의 초기 상태·play·결과 assertion, visual과의 구분·유지 비용. 특정 도구 도입 의무 아님 |
| S4 | GOV.UK Service Standard, [13. Use and contribute to open standards, common components and patterns](https://www.gov.uk/service-manual/service-standard/point-13-use-common-standards-components-patterns) | 2019-05-08, 개정 2022-05-30 | 재사용 이유와 팀 실천. GOV.UK 규범을 이 제품의 의무로 전용하지 않음 |
| S5 | Martin Fowler, [Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html) | 개정 2024-01-18 | Self-Testing, Frequent Mainline Integration, Semi-Integration. 자주 실제 결합·검증, TDD와의 구분 |
| S6 | Martin Fowler, [Contract Test](https://martinfowler.com/bliki/ContractTest.html) | 2011-01-12, 명칭 변경 2018-01-01 | double/provider 일치, 계약 변화 감지와 공급자 협의. 외부 계약 시험 주기를 일률 강제하지 않음 |
| S7 | Steve Freeman·Nat Pryce, Addison-Wesley Professional, [Growing Object-Oriented Software, Guided by Tests, Chapter 10: The Walking Skeleton](https://www.oreilly.com/library/view/growing-object-oriented-software/9780321574442/ch10.html) | 2009-10 | 공식 유통본 공개 미리보기의 서두만. 초기 build/environment/첫 E2E와 큰 구조 검증. 전체 책 방법론의 효과 입증 아님 |
| S8 | Mike Wacker, Google Testing Blog, [Just Say No to More End-to-End Tests](https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html) | 2015-04-22 | 본문의 피드백·좁은 통합·시험 균형. 댓글 제외, 테스트 비율을 정책으로 채택하지 않음 |

Cockburn 원문과 ACCU walking-skeleton PDF는 이번 웹 도구에서 읽지 못해 근거로 채택하지 않았다. 검색 결과의 정의를 원저자의 직접 확인 내용으로 인용하지 않았다. 채택한 자료는 전문가의 원저술·운영 지침·공식 기능 설명이며, openWebAgent에서의 인과 효과나 보편 성공률을 측정한 연구가 아니다. 이 문서에서는 템플릿이나 제품을 변경하지 않았고, 개발 재실험도 실행하지 않았다.
