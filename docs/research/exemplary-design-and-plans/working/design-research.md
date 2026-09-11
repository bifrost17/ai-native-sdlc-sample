# 실무 시스템 설계문서 조사 기록

조사일: 2026-09-11

범위: 공개 원문을 직접 읽을 수 있고, 사전 설계와 구현 또는 운영 흔적을 연결할 수 있는 웹 애플리케이션/중요 기능 설계. 교육용 사후 해설은 제외했다.

## 우선 추천 1: GitLab Cells — HTTP Routing Service

- 정확한 제목: **Cells: HTTP Routing Service**
- 성격: GitLab.com을 여러 Cell로 수평 분할하면서도 단일 `gitlab.com` 도메인을 유지하기 위한 엣지 라우터의 사전·진화형 설계문서.
- 공식 원문: https://handbook.gitlab.com/handbook/engineering/architecture/design-documents/cells/http_routing_service/
- 고정 소스: https://gitlab.com/gitlab-com/content-sites/handbook/-/blob/b23f6a4e/content/handbook/engineering/architecture/design-documents/cells/http_routing_service.md
- 계보: 현재 페이지는 저자/최초 작성일 front matter를 노출하지 않는다. Cells 상위 설계는 2022-09-07 시작되었고, Kamil Trzciński가 2024-06-12에 라우팅 규칙과 워크플로를 확장한 커밋 `8dbee2bf`를 남겼다. 현재 페이지 최종 표시는 2026-02-24, `b23f6a4e`이다. 원저자를 한 사람으로 단정하지 않는 편이 정확하다.
- 검토/결정 기록: 상위 Cells 결정 로그의 ADR-001(Cloudflare Workers), ADR-010(정적 규칙과 HTTP 캐시), 관련 분석 이슈 `#432934`; 구현 저장소 README가 이 설계와 ADR-010을 규범 문서로 직접 링크한다.
- 구현 원문: https://gitlab.com/gitlab-org/cells/http-router
- 운영 원문: https://runbooks.gitlab.com/http-router/http-router-survival-guide/

### 특히 좋은 절

1. **Goals + Requirements + Low Latency**: 단일 도메인, 혼합 버전, 무상태, 보안, 점진 배포를 우선순위 표로 고정하고, 기존 web/API/Git SLI의 p50–p99 headroom에서 50ms 지연 한도를 도출한다. 추상적인 “빨라야 한다”보다 구현 선택을 제한하는 수치가 있다.
2. **Routing rules + Classification**: 경로 claim, 토큰 fallback, Topology Service 조회, 양·음성 캐시, `Cache-Tag` 무효화를 실제 JSON과 두 개의 sequence diagram으로 설명한다. GraphQL처럼 shard key가 URL 깊숙이 있거나 없는 요청도 처음부터 문제로 드러낸다.
3. **Deployment + Rolling Out Rule Sets + Alternatives**: pass-through부터 다중 Cell까지 단계화하고 5→25→50→75→100% 배포, baking time, SLO 확인 절차를 명시한다. 요청 버퍼링 및 동적 route learning을 메모리 비용, Cell 가용성 의존, 혼합 버전 호환성, 캐시 폭증 때문에 거절한다.

### 구현·현재 상태 증거

- 별도 `gitlab-org/cells/http-router` 저장소가 2024-02-15 생성되어 Cloudflare Workers 구현, routing rule, 배포, 보안, 관측, Playwright E2E 문서를 운영 중이다.
- 현재 저장소에는 `session_prefix`, `session_token`, `firstcell`, `passthrough` 규칙과 Topology Service timeout이 실제 설정으로 존재한다.
- 운영 survival guide는 실제 서비스가 Cells를 위해 `gitlab.com` 단일 도메인 앞에서 동작하며, path/header/cached classification으로 대상 Cell을 고른다고 설명한다.
- 2024-12-03 병합된 MR !369는 routable token fallback을 구현했고 파이프라인 통과 및 squash commit `af0e18b6`가 확인된다: https://gitlab.com/gitlab-org/cells/http-router/-/merge_requests/369

### 한계

- 살아 있는 문서라 초기 제안과 현재 운영 절차가 섞여 있고 FAQ 하나가 아직 TBD다.
- 저자와 최초 작성일이 문서 front matter에 없어 commit history로 편집 계보를 설명해야 한다.
- Cells 1.0/1.5/2.0은 이후 Protocells 방향으로 바뀌었으므로, 상위 제품 로드맵의 성공 사례로 읽기보다 HTTP Router라는 실제 산출물의 설계 품질로 읽어야 한다.

## 우선 추천 2: GitLab Cells — Topology Service Transactional Behavior

- 정확한 제목: **Topology Service Transactional Behavior**
- 저자/날짜/상태: `@ayufan`(Kamil Trzciński), 2025-07-02 생성, 현재 `accepted`.
- 공식 원문: https://handbook.gitlab.com/handbook/engineering/architecture/design-documents/cells/topology_service_transactional_behavior/
- 초기 고정본: https://gitlab.com/gitlab-com/content-sites/handbook/-/blob/e0898a4242322dbb1435bea629d5ce5fd84e0718/content/handbook/engineering/architecture/design-documents/cells/topology_service_transactional_behavior.md
- 현재 표시 커밋 기반 고정 URL: https://gitlab.com/gitlab-com/content-sites/handbook/-/blob/54dc9013/content/handbook/engineering/architecture/design-documents/cells/topology_service_transactional_behavior.md
- 결정 기록: ADR-018 https://handbook.gitlab.com/handbook/engineering/architecture/design-documents/cells/decisions/018_topology_service_transactional_behavior/
- 구현 저장소: https://gitlab.com/gitlab-org/cells/topology-service

### 특히 좋은 절

1. **Essential Concepts + Happy Path Workflow**: 글로벌 username/email/route uniqueness를 lease-first/commit-later, 원자적 batch, 시간 제한 lease, 소유 Cell만 파기 가능이라는 불변식으로 시작한다. Rails DB와 Cloud Spanner 사이의 순서를 sequence diagram과 단계별 이유로 설명한다.
2. **Unhappy Path Workflows + Reconciliation**: lease 획득 충돌, 네트워크 단절, 로컬 DB 롤백, 앱 크래시, commit 누락, cleanup 실패 각각에 대해 감지·재시도·idempotent 복구 경로를 제공한다. 주기적 데이터 검증과 “최근 레코드 보호”까지 있어 실패 처리가 부록 수준이 아니다.
3. **Open Questions + Alternative Approaches**: DB transaction 중 RPC라는 명시적 위험을 hard timeout, feature flag, 동시 300 circuit breaker로 제한한다. 별도 leased table과 2PC를 JOIN/원자성/운영 복잡도/복구 비용으로 비교한다. chaos/load/consistency/integration 테스트의 미결 질문도 숨기지 않는다.

### 구현·현재 상태 증거

- Topology Service Go 저장소에 `BeginUpdate`, `CommitUpdate`, `RollbackUpdate`, `ListLeases` 계열 RPC와 테스트가 존재한다. 2026년 초 MR !430은 `GetRecord`/`BeginUpdate` 테스트를 보강했다.
- GitLab Rails 쪽에는 2025-09-02 생성된 `cells_outstanding_leases` migration 흔적이 있고, 후속 테이블 분류 작업에서도 `Cells::OutstandingLease`가 확인된다.
- 실제 metrics에는 `ListLeases` RPC latency histogram이 노출되며, 2026년 운영 업데이트는 Topology Service claim classification 지원 MR !488과 HTTP Router 연동을 기록한다.

### 한계

- 문서 스스로 protobuf와 스키마가 개념 설명용이며 실제 구현을 그대로 반영하지 않는다고 경고한다. 따라서 “복사 가능한 명세”가 아니라 실패 모델과 설계 논리의 모범으로 추천해야 한다.
- 일부 운영·보안·부하 임계치는 여전히 질문 형태이며, 구현은 진행 중이다.
- HTTP Routing Service와 같은 Cells 계열이므로 최종 목록에서 프로젝트 다양성이 중요하면 둘 중 하나만 넣을 수 있다. 그 경우 웹 요청 흐름과 롤아웃을 중시하면 HTTP Routing Service, 실패 복구·분산 일관성을 중시하면 Transactional Behavior를 선택한다.

## 스크리닝 로그 (15건)

1. **GitLab HTTP Routing Service** — 최상급. 수치 제약, 요청 흐름, 대안, 단계 배포, 실제 운영 서비스까지 연결.
2. **GitLab Topology Service Transactional Behavior** — 최상급. happy/unhappy path, 재조정, 대안, 구현 흔적이 매우 강함.
3. **GitLab Topology Service** — 상급 예비 후보. goals/requirements/non-goals, sequence/claim/classify, Spanner 선택, 성능, DR, 대안이 풍부하나 범위가 넓고 하위 Transactional Behavior가 더 날카롭다.
4. **GitLab Cells (상위 blueprint)** — 탈락. 영향 범위와 decision log는 좋지만 WIP가 크고 기존 Cells 1.x가 Protocells로 대체되어 단일 모범 문서로는 불안정.
5. **GitLab Cells 1.0** — 탈락. 단계·exit criteria·pros/cons가 좋지만 현재 on hold이고 후속 방향이 변경됨.
6. **GitLab Cells Routable Tokens** — 예비. 중요한 웹/API 인증 라우팅 문제이나 HTTP Router 문서에 비해 독립된 전체 설계의 설명력이 좁음.
7. **GitLab Cells Infrastructure** — 예비. 배포 토폴로지와 책임 경계가 좋지만 사용자 요청 흐름과 선택 대안은 약함.
8. **GitLab Feature Gates** — 예비. 분산 control plane 설계는 흥미롭지만 새 문서라 장기 구현·운영 증거가 상대적으로 부족.
9. **Sentry RFC 0005 Symbolicator caching** — 탈락. 캐시 coalescing 흐름과 현재 결함은 명확하지만 `informational` 현재 구조 기록이며 사전 선택·대안·구현 계획이 약함.
10. **Sentry RFC 0016 Automatic code mappings** — 탈락. 데이터와 API rate-limit 검토는 좋지만 “Drawbacks: None”이고 미결 질문이 많아 모범 설계로 부족.
11. **Sentry RFC 0141 Linking Traces** — 보류/탈락. use case, envelope 계약, 대안, MVP 순서는 매우 좋지만 현재 `draft`이고 구현 완료 연결이 부족.
12. **Discourse: Exploring ServiceWorkers for Discourse** — 탈락. 캐시 무효화, message bus race, long-lived tab 업데이트 문제를 솔직히 다루지만 2015 탐색 글이며 결론이 shelved, 구현 문서가 아님.
13. **Discourse: Community Editing** — 탈락. 제품 권한·신뢰 trade-off 토론이 있으나 커뮤니티 아이디어 스레드이며 설계 구조와 검증 기준이 없음.
14. **Zulip architecture/subsystem docs 및 기술 제안 이슈** — 탈락. 현행 구조 문서는 우수하나 검색에서 문제→대안→구현으로 연결되는 단일 사전 설계 원문을 확보하지 못함.
15. **Chromium Multi-process / Site Isolation / Design archive** — 탈락(이번 목적). 역사적으로 훌륭한 구조 설명이지만 여러 시대의 살아 있는 문서 묶음이고, 정확한 최초 리뷰·단일 구현 PR 연결이 어렵다. 실무 사전설계보다 교육/현재구조 참고자료에 가깝다.

## 검색 경로와 판단 메모

- GitLab Handbook의 design-documents/cells 인덱스 → 개별 blueprint → ADR decision log → 별도 구현 저장소 → MR/운영 runbook 순서로 역추적했다.
- Sentry는 공식 `getsentry/rfcs` index에서 feature/informational 문서를 읽고 RFC PR 및 실제 component repository 존재 여부를 확인했다.
- Discourse Meta와 Zulip GitHub 이슈는 공식 프로젝트 내부 토론만 후보로 삼았으나, 모범 사전설계의 구조와 구현 추적 기준을 충족하지 못했다.
- Chromium 공식 Design Documents index와 Multi-process/Site Isolation 원문을 확인했으나 이번 “실무 사전설계 + 검토/구현 계보” 기준에서는 제외했다.
- 최종 두 건은 같은 GitLab Cells 계열이라는 편향이 있다. 이는 명성 때문이 아니라 공개 원문, ADR, 구현 저장소, 운영 runbook, 현재 변경 이력이 한 사슬로 연결되는 공개성이 다른 후보보다 월등했기 때문이다.
