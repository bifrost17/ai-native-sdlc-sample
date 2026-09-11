# 모범적인 구현계획 사례

번호는 식별자다. 모든 사례에서 문서의 품질과 구현 확인 범위를 나누어 읽어야 한다. 계획의 명령은 당시 저장소·환경을 위한 내용이며, 이 자료집에서 실행할 지시가 아니다.

## P1. Openverse — Dark Mode Frontend Implementation Plan

**웹앱 기능을 여러 PR로 구현할 때 가장 먼저 읽을 사례.**

- [로컬 원문 전체](originals/P1-openverse-dark-mode.md) · [색상표 포함 읽기본](originals/P1-openverse-dark-mode.reading.md) · [원문](https://docs.openverse.org/projects/proposals/dark_mode/20240325-implementation_plan_dark_mode.html) · [고정판](https://github.com/WordPress/openverse/blob/c815ba4942a3d53cb687d51121f7d44caec7b7e3/documentation/projects/proposals/dark_mode/20240325-implementation_plan_dark_mode.md)
- 작성: Zack Krida, 문서·PR 시작 2024-03-25. 성격: 사람을 위한 실제 기능 구현계획. 에이전트 실행 근거는 확인하지 못했다.

### 모범적인 부분

`Expected Outcomes`에서 OS 설정과 사용자의 선택을 조합해 기대 동작을 정하고, `Step-by-step implementation plan`에서 색상 체계와 토글을 병렬 작업으로 나눈다. 특히 각 단계 뒤에 화면 변화가 없는지, 테스트 환경에서만 보이는지 설명한다. 작업 목록만 읽어도 통합 중 제품 상태를 예상할 수 있다는 점을 높게 평가한다.[^p1-plan]

시각회귀 스냅샷을 구현 순서 안에 배치하고, SSR에서 선택을 유지할 쿠키와 캐시 예외까지 포함한다. `Rollback`은 토글을 숨기는 데서 끝나지 않고 이전에 저장한 사용자 선택도 무시하도록 한다. **눈에 보이는 기능과 그 기능을 떠받치는 상태·캐시·검증을 함께 계획하는 방식**이 좋은 참고다.[^p1-plan]

### 검토와 구현 연결

[계획 PR #3963](https://github.com/WordPress/openverse/pull/3963)은 두 검토자의 승인 후 2024-05-01 병합되었다. [구현 PR #4810](https://github.com/WordPress/openverse/pull/4810)은 2024-08-30 병합되었으며, UI 상태·쿠키·기능 플래그와 단위 테스트 변경을 확인했다. [공식 출시 공지](https://make.wordpress.org/openverse/2024/12/10/introducing-dark-mode/)는 2024-12-10 다크 모드 제공을 알린다. 계획, 구현, 출시를 각각 다른 근거로 확인할 수 있다.[^p1-review][^p1-code][^p1-release]

### 한계와 참고 방식

세부 색 이름·토글 디자인은 상위 설계 승인이 필요한 부분으로 남아 있다. 따라서 계획 하나만으로 모든 제품 결정을 대체하는 사례는 아니다. 에이전트용으로 참고할 핵심은 **작업별 선행 조건, 병렬 가능 범위, 중간 통합 상태, 검증과 복구**다. 전체 코드와 UI를 재실행한 검증은 수행하지 않았다.

## P2. Openverse — Ingestion Server Removal

**운영 중인 시스템을 단계적으로 교체하고 계획 변경을 기록하는 사례.**

- [로컬 원문](originals/P2-openverse-ingestion-server-removal.md) · [원문](https://docs.openverse.org/projects/proposals/ingestion_server_removal/20240328-implementation_plan_ingestion_server_removal.html) · [고정판](https://github.com/WordPress/openverse/blob/c815ba4942a3d53cb687d51121f7d44caec7b7e3/documentation/projects/proposals/ingestion_server_removal/20240328-implementation_plan_ingestion_server_removal.md)
- 작성: @stacimc, 문서 날짜 2024-03-28, 공개 PR 시작 2024-04-03. 성격: 사람을 위한 실제 서버·데이터 파이프라인 전환 계획.

### 모범적인 부분

`Approach to the Distributed Reindex`는 비용만 비교하지 않고 로컬 개발, 운영 관찰, 배포와 유지보수까지 비교한다. `Step-by-step plan`은 새 데이터 갱신 경로를 기존 경로와 함께 만들고, 단계별로 가능한 실행을 설명한 뒤 검증 이후에 철거하도록 한다. 기존 파일에서 옮길 부분과 새로운 실행 경로도 연결한다.[^p2-plan]

`Run the data refreshes`, `Remove the ingestion server`, `Rollback`을 함께 읽으면 **새 코드의 구현 완료와 기존 시스템의 철거 허가가 다른 시점**임을 알 수 있다. 다만 마지막 `Risks`의 낮은 위험 표현은 데이터 교체의 실제 영향에 비해 낙관적이고, 성공 판정의 정량 기준도 더 명시할 수 있다. 이 약점까지 검토 대상으로 삼아야 한다.[^p2-plan]

### 검토와 구현 연결

[계획 PR #4026](https://github.com/WordPress/openverse/pull/4026)은 2024-04-17 병합되었다. [검토 댓글](https://github.com/WordPress/openverse/pull/4026#pullrequestreview-1981621777)은 계획의 상세함을 평가하면서 확인 질문을 남겼고, 이후 두 검토자가 승인했다. 단순 유명 프로젝트라는 이유보다 강한 외부 근거다.[^p2-review]

이후 [#4615](https://github.com/WordPress/openverse/pull/4615)는 ASG에서 직접 EC2 관리로 계획을 개정했다. [구현 #4684](https://github.com/WordPress/openverse/pull/4684)는 Airflow 제약으로 원래 구상한 multiprocessing 복제 대신 mapped tasks를 사용한 이유와 달라진 동작, 확인 절차를 명시한다. 계획이 실제 발견에 따라 수정되는 자료다.[^p2-revision][^p2-code]

### 한계와 참고 방식

조회한 [프로젝트 #3925](https://github.com/WordPress/openverse/issues/3925)는 아직 열려 있고 미완료 항목이 있다. **전체 전환이 끝난 성공 사례로 소개하지 않는다.** 현재 문서에는 후속 개정이 포함되어 있으므로 처음부터 모든 내용이 존재했다고 해석해서도 안 된다. 참고할 핵심은 **기존 경로 유지 → 단계별 검증 → 전환 → 철거**, 그리고 계획과 달라진 구현의 이유를 추적하는 방식이다.[^p2-status]

복구 부분에는 중요한 빈틈도 있다. 새 인스턴스와 DAG 제거를 통한 실행 경로 원복은 설명하지만, 이미 교체한 운영 테이블·검색 인덱스의 데이터 복원과 기존 서버 철거 이후의 복구 절차는 구체적이지 않다. **전환 순서와 계획 변경 기록의 참고 사례이며, 데이터 마이그레이션 복구계획의 완성형으로 사용하면 안 된다.**[^p2-plan]

## P3. Superpowers — Visual Companion Auth Hardening

**실패 재현부터 브라우저 확인까지 연결한 에이전트용 실제 구현계획.**

- [로컬 원문](originals/P3-superpowers-auth-hardening-plan.md) · [원문](https://github.com/obra/superpowers/blob/main/docs/superpowers/plans/2026-06-10-visual-companion-auth-hardening.md) · [최초 계획 고정판](https://github.com/obra/superpowers/blob/83b5d3a963ed63d8231ecb3276c8368caf1857a3/docs/superpowers/plans/2026-06-10-visual-companion-auth-hardening.md)
- 작성 이력: Drew Ritter, 2026-06-10. 코딩 에이전트 도구에 포함된 로컬 웹 UI 서버의 인증·재연결 개선 계획. 첫 문단에서 agentic workers의 작업별 실행을 명시한다.
- [같이 작성된 설계문서의 로컬 원문](originals/P3-superpowers-auth-hardening-design.md)과 [외부 고정판](https://github.com/obra/superpowers/blob/83b5d3a963ed63d8231ecb3276c8368caf1857a3/docs/superpowers/specs/2026-06-10-visual-companion-auth-hardening-design.md)을 함께 읽으면 spec → plan의 실제 연결도 볼 수 있다. 이 설계문서는 별도 선정 건수에 중복 집계하지 않았다.

### 모범적인 부분

`File Map`은 변경 파일과 대응 테스트를 연결한다. `Task 1–5`는 실패해야 하는 동작, 확인 명령, 최소 구현, 통과 조건 순서로 구성되어 있다. 인증 성공만 확인하지 않고 다른 출처의 WebSocket 연결과 파일 경로 이탈이 차단되는지도 다룬다.[^p3-plan]

특히 `Task 6`은 이미 앞 작업으로 통과한 테스트를 실패 재현 단계라고 부르지 말라고 명시한다. `Task 9–10`은 개별 테스트, 전체 회귀, 반복 실행, 실제 브라우저 동작 순서로 검증을 확장한다. 브라우저 연결 표시뿐 아니라 선택 이벤트가 기록되는 결과까지 확인하도록 한다. **실행 기록을 정직하게 남기면서 실제 효과까지 검증하는 방식**이 가장 참고할 부분이다.[^p3-plan]

### 계획이 구현보다 앞섰다는 근거

[계획 커밋](https://github.com/obra/superpowers/commit/83b5d3a963ed63d8231ecb3276c8368caf1857a3)은 설계와 계획을 추가한다. 그 커밋을 직접 부모로 갖는 [후속 구현 커밋](https://github.com/obra/superpowers/commit/b17d54f839831b2345aa389e2f65f435f3a82867)은 약 44분 뒤 서버·브라우저 helper·시작/정지 스크립트와 네 테스트 파일 등을 변경했다. 주요 패치에서 계획과 대응하는 동작·회귀 테스트를 확인했다. 단순히 날짜가 적힌 파일이 아니라 Git 선후 관계가 확인되는 사례다.[^p3-code]

GitHub의 커밋 연관 PR 조회는 [v6.0.0 출시 PR #1769](https://github.com/obra/superpowers/pull/1769)에 연결되며 2026-06-16 병합 기록이 있다. 다만 출시 PR의 인간 검토·에이전트 사용 설명은 작성자 보고이며, 이 계획의 모든 단계를 특정 모델이 자동 실행한 독립 증거는 아니다.[^p3-release]

### 한계와 참고 방식

개인 체크아웃 절대 경로와 임시 probe 경로가 남아 있어 그대로 다른 환경에 넘길 수 없다. 긴 코드 블록은 당시 작업에는 구체적이지만 구현과 쉽게 어긋날 수 있다. 실제 구현도 브라우저 `sessionStorage` 접근이 차단되는 예외와 추가 검증을 보강했다. 계획의 코드가 최종 코드와 같다고 가정하지 말고 **실패 조건 → 작업 → 관찰 가능한 통과 조건**의 연결을 가져오는 것이 좋다. 이번 조사에서는 테스트를 재실행하지 않았다.[^p3-plan][^p3-code]

## 출처

[^p1-plan]: Zack Krida. [2024-03-25 Implementation Plan: Dark Mode](https://docs.openverse.org/projects/proposals/dark_mode/20240325-implementation_plan_dark_mode.html). Openverse. 확인 2026-09-11.
[^p1-review]: Openverse. [Dark Mode Frontend Implementation Plan #3963](https://github.com/WordPress/openverse/pull/3963), 2024-03-25~2024-05-01. [승인 1](https://github.com/WordPress/openverse/pull/3963#pullrequestreview-2032868182), [승인 2](https://github.com/WordPress/openverse/pull/3963#pullrequestreview-2033715146).
[^p1-code]: Openverse. [Add color mode to ui store #4810](https://github.com/WordPress/openverse/pull/4810), 2024-08-26~2024-08-30. PR 변경 파일과 테스트 지침 확인.
[^p1-release]: Olga Bulat. [Introducing Dark Mode](https://make.wordpress.org/openverse/2024/12/10/introducing-dark-mode/), 2024-12-10. 정식 날짜 경로에서 공지 본문과 게시일 확인.
[^p2-plan]: @stacimc. [2024-03-28 Implementation Plan: Ingestion Server Removal](https://docs.openverse.org/projects/proposals/ingestion_server_removal/20240328-implementation_plan_ingestion_server_removal.html). Openverse. 확인 2026-09-11.
[^p2-review]: Openverse. [Implementation plan: Ingestion server removal #4026](https://github.com/WordPress/openverse/pull/4026), 2024-04-03~2024-04-17. [승인 1](https://github.com/WordPress/openverse/pull/4026#pullrequestreview-1998688566), [승인 2](https://github.com/WordPress/openverse/pull/4026#pullrequestreview-2002490278).
[^p2-revision]: Openverse. [Update ingestion server removal IP with EC2 approach #4615](https://github.com/WordPress/openverse/pull/4615), 2024-07-16~2024-07-19.
[^p2-code]: Openverse. [Add alter data step to the data refresh DAG #4684](https://github.com/WordPress/openverse/pull/4684), 2024-07-31~2024-08-20.
[^p2-status]: Openverse. [Removal of the ingestion server #3925](https://github.com/WordPress/openverse/issues/3925). GitHub REST 조회 2026-09-11: open. 공개 PR의 검증 지침은 독립적인 테스트 재실행 결과가 아니다.
[^p3-plan]: Drew Ritter. [Visual Companion Auth Hardening Implementation Plan](https://github.com/obra/superpowers/blob/83b5d3a963ed63d8231ecb3276c8368caf1857a3/docs/superpowers/plans/2026-06-10-visual-companion-auth-hardening.md), 2026-06-10. 원문 전체와 파일 이력 확인.
[^p3-code]: Superpowers. [Document visual companion auth hardening plan](https://github.com/obra/superpowers/commit/83b5d3a963ed63d8231ecb3276c8368caf1857a3), 2026-06-10 21:14:15 UTC; [Harden brainstorm companion auth regressions](https://github.com/obra/superpowers/commit/b17d54f839831b2345aa389e2f65f435f3a82867), 같은 날 21:58:16 UTC. 부모 커밋과 변경 파일·주요 패치 확인.
[^p3-release]: Superpowers. [Release v6.0.0 #1769](https://github.com/obra/superpowers/pull/1769), 2026-06-16 병합. 커밋 연관 PR 및 출시 설명 확인. 개별 작업의 자동 실행 transcript는 확보하지 않았다.
