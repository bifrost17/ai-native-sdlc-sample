# 모범적인 시스템 설계문서 사례

실무의 사전 설계와 이미 구현된 시스템을 설명하는 교육 자료는 역할이 다르다. 각 사례의 성격과 읽어야 할 부분을 함께 표시한다.

## D1. OpenAI Symphony — Service Specification

**에이전트가 다른 언어로도 구현할 수 있도록 작성한 서비스 전체 명세.**

- [로컬 원문](originals/D1-symphony-spec.md) · [원문](https://github.com/openai/symphony/blob/main/SPEC.md) · [검토한 내용의 고정판](https://github.com/openai/symphony/blob/8001b52e3062495a16e520e4ceaf8f9de868c4d0/SPEC.md)
- 작성 주체: OpenAI Symphony 프로젝트. 공개 이력의 최초 추가 2026-03-04, 확인한 파일 최종 변경 2026-08-12. 상태: `Draft v1`, 언어에 독립적인 서비스 명세.
- 웹앱 자체보다는 코딩 에이전트 작업을 관리하는 서비스이며 웹 대시보드는 선택 확장이다.

### 모범적인 부분

`§1–4`는 제품의 목적과 구성 요소뿐 아니라 책임 경계와 식별자의 의미를 고정한다. `§7–8`은 외부 이슈 상태와 내부 실행 상태를 구분하고, 중복 실행 방지·재시도·진행 중 작업 재확인의 규칙을 연결한다. **용어 정의가 상태 전이와 실제 동작 제약까지 이어지는 점**을 높게 평가한다.[^d1-spec]

`§6.2`, `§14`는 설정 갱신 실패와 프로세스 재시작을 구분한다. 재시작 뒤 무엇을 복원하지 않는지도 명확하다. `§17–18`은 기본 구현, 선택 확장, 외부 서비스 통합 검증을 나누고, 환경 부족으로 생략한 검증을 통과로 처리하지 않도록 한다. 구현자의 추측을 줄이는 명세의 좋은 사례다.[^d1-spec]

### 에이전트 사용과 구현 근거

[공식 README](https://github.com/openai/symphony/blob/main/README.md)는 이 명세를 코딩 에이전트에게 전달해 원하는 언어로 구현하는 사용법을 제시한다. [Elixir 참조 구현 안내](https://github.com/openai/symphony/blob/main/elixir/README.md)도 명세에 기반한 구현임을 명시한다. 따라서 파일명만 보고 에이전트용으로 추정한 사례가 아니다.[^d1-readme]

[변경 PR #102](https://github.com/openai/symphony/pull/102)는 명세와 트래커 경계, 실행 코드, 테스트를 함께 변경했다. 작성자는 여러 언어의 명세 기반 구현 검사와 실제 Linear 연동 결과를 보고했다. PR 병합과 코드·테스트 변경은 확인했지만, 보고된 실행 결과를 독립적으로 재현하지는 않았다. 조회한 PR의 리뷰 제출 목록은 비어 있어 이를 외부 전문가 승인으로 표현하지 않는다.[^d1-pr]

### 한계와 참고 방식

공식 프로젝트는 engineering preview, 참조 구현은 평가용 prototype으로 표시한다. 또한 현재 명세는 구현과 함께 개정되어 온 문서다. 최초 구현 전에 지금의 명세가 모두 존재했다고 볼 수 없다. **에이전트에게 필요한 계약의 명확성**을 참고하되, 이 길이와 모든 운영 항목을 작은 웹앱의 필수 분량으로 가져오지는 않는 것이 좋다.[^d1-readme]

## D2. Django — DEP 0009: Async-capable Django

**기존 사용자를 유지하면서 큰 구조 변경을 설계하는 사례.**

- [로컬 원문](originals/D2-django-dep-0009.rst) · [원문](https://github.com/django/deps/blob/main/accepted/0009-async.rst) · [고정판](https://github.com/django/deps/blob/a83080652411e34e6afa8e1f0a97b675a76358e5/accepted/0009-async.rst)
- 저자: Andrew Godwin. 작성 2019-05-06, 2019-07-21 accepted 디렉터리로 이동한 이력 확인. 웹 프레임워크의 대규모 기능·구조 설계이며 전체 웹앱 설계는 아니다.

### 모범적인 부분

`High-Level Summary`와 `Technical Overview`는 동기 API를 유지하면서 비동기 기능을 도입하는 단계를 설명한다. `Threadlocals`, `Views & HTTP Handling`, `The ORM`에서는 그 원칙이 요청 처리와 데이터 연결의 구체 제약에 어떻게 영향을 주는지 보여준다. **호환성을 비기능 요구 한 줄로 끝내지 않고 구조 선택에 반영하는 방식**이 특히 좋다.[^d2-dep]

`Rationale`과 `Alternatives`는 포크, 별도 모듈, 다른 동시성 방식의 비용을 비교한다. `Sequencing`은 부분 완료만으로도 사용자 가치가 남도록 작업을 나눈다. 성능 손실, 기여자의 지속 가능성, 중단될 가능성까지 다루어 기술적으로 가능한 설계와 실제로 전달할 수 있는 설계를 함께 고민한다.[^d2-dep]

### 인정 근거와 구현 연결

공식 DEP의 상태는 `Accepted`이며 [수락된 경로로 이동한 커밋](https://github.com/django/deps/commit/a7080e6f830815829fcee2f2b061f59bdeed489d)을 확인했다. [Django 3.1 공식 릴리스 노트](https://docs.djangoproject.com/en/3.2/releases/3.1/#asynchronous-views-and-middleware-support)는 비동기 뷰·미들웨어·테스트 제공과 당시 ORM 등의 미지원 범위를 명시한다. 설계 방향의 실제 출시는 확인되지만 DEP의 모든 세부안이 그대로 구현되었다는 뜻은 아니다.[^d2-release]

### 한계와 참고 방식

당시 제안한 API 이름·내부 동작·일정은 역사적 설계안이다. 현재 Django 사용법으로 복사하면 안 된다. 문서 자체도 구현 세부를 발견에 따라 조정할 필요를 인정한다. 따라서 바로 실행할 작은 `plan.md`보다는 **변경의 이유, 호환성 제약, 대안과 단계적 전달을 설명하는 `spec.md`**에 적합하다.[^d2-dep]

## D3. GitLab Cells — HTTP Routing Service

**유명 웹앱의 요청 흐름·성능 제약·배포를 함께 설명하는 사례.**

- [로컬 원문](originals/D3-gitlab-http-routing-service.md) · [원문](https://handbook.gitlab.com/handbook/engineering/architecture/design-documents/cells/http_routing_service/) · [페이지에 연결된 변경 커밋 기준 소스](https://gitlab.com/gitlab-com/content-sites/handbook/-/blob/b23f6a4e/content/handbook/engineering/architecture/design-documents/cells/http_routing_service.md)
- 작성 주체: GitLab Cells 프로젝트. 페이지 최종 변경 표시는 2026-02-24. 단일 저자·최초 작성일은 원문에 없으므로 확정하지 않았다. 사전 제안과 후속 운영 내용이 누적된 설계문서다.

### 모범적인 부분

`Requirements`와 `Low Latency`는 기존 요청의 성능 지표를 근거로 라우터의 추가 지연 목표를 정한다. `Routing rules`와 `Classification`은 경로 기반 분류, 토큰으로의 대체 경로, 조회 실패의 캐시까지 다룬다. 요구사항과 요청 예시·시퀀스 다이어그램이 연결되어 있어 웹앱 설계에 특히 참고하기 좋다.[^d3-design]

`Alternatives`는 요청 버퍼링과 동적 경로 학습을 메모리, 서로 다른 버전의 공존, 다른 Cell의 가용성에 대한 의존으로 비교한다. `Rolling Out Rule Sets`는 일부 트래픽에 적용한 뒤 관찰 시간을 두고 SLO 영향을 확인하는 순서를 설명한다. **구조 선택의 이유가 운영과 배포 방법까지 이어지는 점**을 높게 평가한다.[^d3-design]

### 구현·운영 연결과 한계

[공식 운영 안내](https://runbooks.gitlab.com/http-router/http-router-survival-guide/)는 이 설계문서를 직접 연결하며, 라우팅 역할·장애 증상·복구 방법을 설명한다. 라우터를 끄면 기존 Cell과 신규 Cell 사용자에게 서로 다른 영향이 생기는 점도 명시한다. 실제 운영 책임까지 연결된 문서라는 근거다.[^d3-runbook]

다만 설계의 `Non-Goals`와 FAQ 일부는 미정이고, 현재 문서에는 후속 변경이 섞여 있다. 예시 JSON도 실행용 설정 파일처럼 그대로 복사할 자료가 아니다. 따라서 완벽하게 닫힌 계약의 사례로 보기는 어렵다. **비기능 요구를 근거와 함께 정하고 실제 요청·대안·배포에 연결하는 방법**을 읽는 데 추천한다. 연결된 비공개 운영 대시보드나 실제 프로덕션은 조회하지 않았다.[^d3-design]

## D4. MediaWiki — AOSA Volume 2, MediaWiki

**유명 웹앱의 전체 구조를 설명하는 교육·사후 아키텍처 문서.**

- [도표 포함 로컬 읽기본](originals/D4-mediawiki.html) · [HTML 원본 전체](originals/D4-mediawiki.original.html) · [원문](https://aosabook.org/en/v2/mediawiki.html)
- 저자: Sumana Harihareswara, Guillaume Paumier. 2011년 작성 프로젝트와 AOSA Volume 2에 연결되는 역사 자료.
- [공식 작성 프로젝트 기록](https://www.mediawiki.org/wiki/MediaWiki_architecture_document) · [보관된 2차 초안](https://www.mediawiki.org/wiki/MediaWiki_architecture_document/text/revision_2)

### 모범적인 부분

`12.3 Database and Text Storage`는 스키마를 나열하는 대신, 문서 이름 변경·삭제·편집이 기존 구조에서 왜 비쌌는지 설명하고 저장 구조 변경과 연결한다. `12.4 Requests, Caching and Delivery`는 요청 하나를 따라가며 애플리케이션과 캐시 계층을 연결한다. 정적인 구성도와 실제 동작을 함께 이해할 수 있다는 점에서 추천한다.[^d4-chapter]

권한·국제화·확장 지점도 제품의 성격과 연결하고, 기존 구조의 약점을 숨기지 않는다. **“어떤 구성 요소가 있는가”에서 “제품의 요구 때문에 왜 이렇게 되었는가”로 설명을 이어가는 방식**을 참고하기 좋다.[^d4-chapter]

### 인정 근거와 한계

공식 작성 기록에는 신규 개발자의 이해를 돕기 위한 목적, 전문가 의견 수집, 공동체·편집자·기술 검토 과정이 명시되어 있다. 본문의 감사 절에도 기여·검토한 개발자들이 나열된다. 출처와 검토 맥락이 분명한 사례다.[^d4-process][^d4-chapter]

다만 사전 승인용 `spec.md`는 아니며 현재 MediaWiki의 설계를 나타내지도 않는다. 공식 보관 페이지도 내용이 오래되었다고 표시한다. 트래픽 수치·구현 기술을 현재 권고로 가져오지 말고, **시스템 경계·데이터 흐름·결정 이유를 설명하는 방법**을 읽는 것이 적합하다.[^d4-process]

## 출처

[^d1-spec]: OpenAI. [Symphony SPEC.md 고정판](https://github.com/openai/symphony/blob/8001b52e3062495a16e520e4ceaf8f9de868c4d0/SPEC.md), Draft v1. [최초 추가 커밋](https://github.com/openai/symphony/commit/fa75ec68c23fbf773c43197da618f88684d8d3f6), 2026-03-04. 파일 이력과 본문 확인 2026-09-11.
[^d1-readme]: OpenAI. [Symphony README](https://github.com/openai/symphony/blob/main/README.md), [Elixir README](https://github.com/openai/symphony/blob/main/elixir/README.md). 에이전트 구현 안내 및 실험적 상태의 근거.
[^d1-pr]: OpenAI. [Add generic tracker interface with Linear adapter #102](https://github.com/openai/symphony/pull/102), 2026-07-18 병합. 변경 파일 목록과 작성자의 Test Plan 확인. 실행 결과는 작성자 보고.
[^d2-dep]: Andrew Godwin. [DEP 0009: Async-capable Django](https://github.com/django/deps/blob/a83080652411e34e6afa8e1f0a97b675a76358e5/accepted/0009-async.rst), 2019-05-06. 고정판의 2025-01-07 변경은 Last Modified 메타데이터 제거이며 새 설계 작성일이 아니다.
[^d2-release]: Django. [Django 3.1 release notes](https://docs.djangoproject.com/en/3.2/releases/3.1/#asynchronous-views-and-middleware-support), 2020-08-04. 해당 버전에서 제공된 부분과 당시 남은 부분의 근거.
[^d3-design]: GitLab. [Cells: HTTP Routing Service](https://handbook.gitlab.com/handbook/engineering/architecture/design-documents/cells/http_routing_service/), 페이지 표시 최종 변경 2026-02-24, `b23f6a4e`. 본문·다이어그램 텍스트·하단 이력 확인 2026-09-11.
[^d3-runbook]: GitLab. [HTTP Router: On-Call Survival Guide](https://runbooks.gitlab.com/http-router/http-router-survival-guide/). 설계 링크·역할·장애·복구 절차 확인. 운영 상태 설명과 사전 설계안을 동일한 것으로 간주하지 않음.
[^d4-chapter]: Sumana Harihareswara, Guillaume Paumier. [MediaWiki](https://aosabook.org/en/v2/mediawiki.html), *The Architecture of Open Source Applications*, Volume 2, chapter 12. 확인 2026-09-11.
[^d4-process]: Wikimedia. [MediaWiki architecture document](https://www.mediawiki.org/wiki/MediaWiki_architecture_document), 작성 프로젝트 2011. [고정 기록 oldid=3936397](https://www.mediawiki.org/w/index.php?title=MediaWiki_architecture_document&oldid=3936397). 저술·검토 과정의 근거이며 현재 시스템 설명이 아니다.
