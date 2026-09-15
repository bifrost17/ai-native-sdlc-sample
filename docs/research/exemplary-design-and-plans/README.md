# 모범적인 시스템 설계문서와 구현계획

조사일: 2026-09-11. **시스템 설계 4건, 구현계획 3건**을 선정했다. 실제 문서의 구체성, 검토와 구현의 흔적, 다른 프로젝트에 참고할 수 있는 설명 방식을 함께 평가했다. 빈 템플릿이나 계획 작성 가이드는 선정 수에 포함하지 않았다.

지금 만드는 `spec.md`·`plan.md`에 가장 먼저 참고할 조합은 **Symphony 명세 + Openverse 다크 모드 계획 + Superpowers 인증 개선 계획**이다. 각각 구현 계약의 명확성, 여러 단계에 걸친 제품 상태, 에이전트가 실행·검증할 작업 단위를 보기 좋다. 웹앱의 아키텍처 설명 방식은 GitLab과 MediaWiki를 함께 읽으면 보완된다.

선정한 원문 7건 전체와 Superpowers의 짝 설계문서 1건을 이 보고서와 함께 `originals/`에 보관했다. 파일별 출처·고정판·보관 형식은 [로컬 원문 목록](originals/README.md)에서 확인할 수 있으며, 아래 상세 평가에는 각 사례의 로컬 원문 링크와 외부 원문 링크를 함께 남겼다.

## 시스템 설계 4건

| 사례와 원문 | 성격 | 특히 잘한 부분 | 읽을 때의 제한 | 로컬 파일 |
|---|---|---|---|---|
| D1. [OpenAI Symphony SPEC](https://github.com/openai/symphony/blob/main/SPEC.md) | 에이전트 구현을 염두에 둔 서비스 전체 명세 | 책임 경계, 상태 전이, 복구, 검증 매트릭스 | 실험적 프로젝트이며 현재판은 후속 개정 포함 | [로컬 전체](originals/D1-symphony-spec.md) |
| D2. [Django DEP 0009](https://github.com/django/deps/blob/main/accepted/0009-async.rst) | 유명 웹 프레임워크의 대규모 구조 변경안 | 호환성 제약, 대안 비교, 부분 완료에도 가치가 남는 단계 | 2019년 제안이며 현재 API 사용 설명이 아님 | [로컬 전체](originals/D2-django-dep-0009.rst) |
| D3. [GitLab HTTP Routing Service](https://handbook.gitlab.com/handbook/engineering/architecture/design-documents/cells/http_routing_service/) | 실제 웹앱의 라우팅 설계 | 성능 요구의 근거, 요청 흐름, 대안, 점진 배포 | 비목표 등 미정 항목과 후속 운영 내용 공존 | [로컬 전체](originals/D3-gitlab-http-routing-service.md) |
| D4. [MediaWiki — AOSA](https://aosabook.org/en/v2/mediawiki.html) | 유명 웹앱의 교육·사후 아키텍처 해설 | 저장 구조의 이유, 요청·캐시 흐름, 제품 특성과 구조의 연결 | 사전 설계문서도 현재 아키텍처도 아님 | [로컬 읽기본](originals/D4-mediawiki.html) / [HTML 원본](originals/D4-mediawiki.original.html) |

각 문서의 작성자·날짜·고정판·좋은 절·검토와 구현 근거는 [시스템 설계 상세 평가](system-designs.md)에 정리했다.

## 구현계획 3건

| 사례와 원문 | 성격 | 특히 잘한 부분 | 실제 확인 범위 | 로컬 파일 |
|---|---|---|---|---|
| P1. [Openverse Dark Mode](https://docs.openverse.org/projects/proposals/dark_mode/20240325-implementation_plan_dark_mode.html) | 웹앱 기능 구현계획 | 병렬 작업, 단계별 화면 상태, 시각회귀, SSR·캐시, 복구 | 계획 승인 → 구현 PR → 공식 출시 | [로컬 전체](originals/P1-openverse-dark-mode.md) / [그림 포함](originals/P1-openverse-dark-mode.reading.md) |
| P2. [Openverse Ingestion Server Removal](https://docs.openverse.org/projects/proposals/ingestion_server_removal/20240328-implementation_plan_ingestion_server_removal.html) | 운영 시스템 교체 계획 | 기존 경로 유지, 단계별 검증, 전환 후 철거, 계획 개정 | 승인·개정·일부 구현 확인; 전체 미완료, 데이터 복구 상세 부족 | [로컬 전체](originals/P2-openverse-ingestion-server-removal.md) |
| P3. [Superpowers Visual Companion Auth Hardening](https://github.com/obra/superpowers/blob/83b5d3a963ed63d8231ecb3276c8368caf1857a3/docs/superpowers/plans/2026-06-10-visual-companion-auth-hardening.md) | **에이전트용 실제 계획** | 실패 재현 → 구현 → 통과 조건, 회귀·브라우저 검증 | 계획 커밋 → 직접 자식 구현 커밋 → 출시 PR 연결 | [로컬 전체](originals/P3-superpowers-auth-hardening-plan.md) |

세부 평가는 [구현계획 상세 평가](implementation-plans.md)에 있다. Openverse 두 건은 같은 프로젝트지만 기능 출시와 운영 시스템 교체라는 서로 다른 계획 문제를 잘 보여 주어 함께 선정했다. P3는 에이전트용이라는 명시와 사전 계획 이력을 모두 확인한 사례다. 모든 작업의 자동 실행 transcript까지 확보한 것은 아니다.

## 추천하는 읽기 순서

1. **Openverse Dark Mode:** 가장 익숙한 웹앱 기능부터 읽는다. `Expected Outcomes` → 단계별 계획 → `Launch plan` → `Rollback` 순서로 작업과 사용자 경험의 연결을 본다.
2. **Superpowers Auth Hardening:** `File Map` → `Task 2` → `Task 6` → `Task 9–10`을 읽는다. 특히 이미 통과하는 테스트를 실패 재현으로 포장하지 않는 원칙과 브라우저에서 확인할 결과를 살핀다.
3. **Symphony:** `§1–4` → `§7–8` → `§14` → `§17–18`을 읽는다. 도메인 정의와 실행 규칙·복구·완료 판정이 일관되게 이어지는지 본다.
4. **GitLab / Django / MediaWiki:** 요청 흐름과 운영은 GitLab, 큰 변경의 대안·호환성은 Django, 전체 구조를 이해시키는 서술은 MediaWiki에서 보완한다.
5. **Openverse Ingestion:** 데이터 이전·기존 시스템 대체를 계획할 때 읽는다. 구현 완료와 철거 가능 시점을 나누는 부분을 집중해서 본다.

## 템플릿 설계에 가져올 관찰

좋은 문서는 항목의 수보다 **결정 사이의 연결**이 강했다. 제약이 구조를 제한하고, 선택 이유가 대안과 연결되며, 작업의 결과가 검증과 연결된다. 이 연결을 보존하는 것이 여러 문서의 목차를 합치는 것보다 유용하다는 것이 이번 조사의 판단이다.

| 템플릿에서 해결할 문제 | 참고할 실제 문서 |
|---|---|
| 용어·책임·상태를 에이전트가 추측하지 않게 만들기 | Symphony |
| 성능 요구에 근거를 붙이고 요청 하나를 끝까지 설명하기 | GitLab, MediaWiki |
| 기존 사용자·기능을 유지하는 구조 변경을 설명하기 | Django |
| 여러 PR 사이의 제품 상태와 병렬 가능 범위를 설명하기 | Openverse Dark Mode |
| 한 작업의 실패 재현·완료 판정·검증을 연결하기 | Superpowers Auth Hardening |
| 데이터 전환 후 기존 경로를 제거할 조건을 정하기 | Openverse Ingestion |

원문의 긴 코드 블록, 개인 절대 경로, 예시 설정, 당시 성능 수치까지 그대로 양식으로 옮기는 것은 권하지 않는다. 상위 설계가 결정할 것과 구현 중 확인할 것을 구분하고, 문서에 완료라고 적힌 것과 실제 실행 근거도 구분해야 한다.

## 근거와 추가 자료

- [선정 방법·근거 해석·제외 기준](methodology.md)
- [시스템 설계 후보와 제외 사유](working/design-research.md)
- [에이전트 계획 후보·Git 이력 검증](working/agent-plan-research.md)
- [커뮤니티 브라우저 조사 기록](working/community-research.md)
- [Openverse·AOSA 및 추가 탐색 기록](working/root-research.md)
- [최종 비판 검토와 반영 사항](review.md)

이 목록은 모든 독자의 합의나 소프트웨어의 무결함을 주장하는 순위가 아니다. 공개 근거로 추천 이유와 한계를 검토할 수 있는 참고 목록이다. 대상 프로젝트의 전체 빌드·외부 연동을 재실행하지 않았으며, PR 작성자의 테스트 보고와 이번에 확인한 Git·출시 기록을 나누어 표시했다.
