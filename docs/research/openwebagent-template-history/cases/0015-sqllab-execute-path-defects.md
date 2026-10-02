# 0015 — SQL Lab 실행 잠금과 시간 초과 취소

판정: **이력 검토 완료, 원시 실행 재현은 미검증.** PR-1은 SQLite 쓰기 잠금 때 루프에서 동기 commit이 기다리다 500을 내는 결함 A와 워커 메타데이터 덮어쓰기 E를, PR-2는 대상 DB 쿼리 취소 미배선 C와 `timed_out` 화면을 다뤘다. 두 PR의 경계와 요청자 화면 결정은 문서·Git에서 확인된다.

## 사건 사슬

고정 자료는 `.local/research/openwebagent-template-history/20261003/collection/` inventory·API·bare Git, 초기 main `a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e`다. [PR #343](https://github.com/bifrost17/openwebagent/pull/343)과 [PR #344](https://github.com/bifrost17/openwebagent/pull/344)의 본문은 당시 주장으로 읽는다.

| 순서 | 근거·판정 |
|---|---|
| 최초 요구·문서 | [`4c391fd`](https://github.com/bifrost17/openwebagent/commit/4c391fdcbb5)가 intent·spec·plan을 제품 변경 전에 추가했다. intent `:15-108`은 A의 라이브 500·별도 프로세스 재현과 C의 408 뒤 쿼리 존속을 분리한다. spec `:93-172`는 rollback 뒤 작업 재적용·루프 밖 메타 DB 작업·최신 행 조회, `:184-342`는 취소 함수·원자적 상태 기록·화면을 규정한다. 당시 원시 `p2-a-app`·운영 로그는 이 수집에 없다. |
| 인계·PR-1 | [`c2f42b4`](https://github.com/bifrost17/openwebagent/commit/c2f42b4777f)가 착수 전 계획 리뷰 F1·F2·F7·F8·F10을 반영. [`e2b717e`](https://github.com/bifrost17/openwebagent/commit/e2b717eea23) T01, [`bd700a4`](https://github.com/bifrost17/openwebagent/commit/bd700a4e684) T02·03, [`918c32e`](https://github.com/bifrost17/openwebagent/commit/918c32ea4d7) T04 diff가 헬퍼·실파일 SQLite 경합 시험·라우트·워커 수정을 담는다. `c664cfc`·`27bb97c`·`894813b`가 실행·V3·V4 기록을 후속 문서 커밋으로 남겼다. [`b675b58`](https://github.com/bifrost17/openwebagent/commit/b675b5820)가 #343 머지. |
| PR-2 설계 변화 | 머지 후 [`ec80b92`](https://github.com/bifrost17/openwebagent/commit/ec80b92f31d)에서 요청자 D5 “화면도 함께”를 intent·spec·plan에 반영하고 [`3f86b3d`](https://github.com/bifrost17/openwebagent/commit/3f86b3ddcd0)가 계획 인계 재검토를 반영했다. 이는 최초 설계의 임의 이탈이 아니라 **추가 결정**이다. spec SP05 `:224-290`은 취소 스레드와 실행 스레드의 늦은 쓰기 경합을 계약화한다. |
| PR-2 구현·검토 | [`e32dc16`](https://github.com/bifrost17/openwebagent/commit/e32dc164004) T05 취소 배선, [`9e0cc35`](https://github.com/bifrost17/openwebagent/commit/9e0cc35c4c9) T06 원자적 `timed_out`, [`19c32dc`](https://github.com/bifrost17/openwebagent/commit/19c32dc1adb) 실DB 시험, [`b34d60d`](https://github.com/bifrost17/openwebagent/commit/b34d60d4a17) 0003 SP06-102 정정, [`35506a6`](https://github.com/bifrost17/openwebagent/commit/35506a6ef0e) T09 결과 창·상태 막대 diff를 확인했다. [`17b33c2`](https://github.com/bifrost17/openwebagent/commit/17b33c246ec)가 리뷰 F1·F3의 타이머 정지·바깥 `SoftTimeLimitExceeded` 시험을 추가했다. [`df9c6eb`](https://github.com/bifrost17/openwebagent/commit/df9c6ebd3)가 #344 머지. |
| 검증·후속 | plan `:302-324,568-591,900-940`과 PR 본문은 실파일 잠금 시험, 프런트 시험, 게이트, 리뷰 보완을 보고한다. PR-1의 `StaticPool` fixture는 연결 간 경합을 만들 수 없어 실제 파일·별도 프로세스 시험으로 바꿨다. PR-2 plan 머리 `:10-24`는 **현재 main에도 “검증 대기·사람 plan 수락·V5-C 미실행”**을 남겼다. 완료·배포를 증명하는 현재 정본으로 쓰면 안 된다. 원문 실행 출력과 머지 뒤 V5-C는 확보하지 못했다. |

## 여섯 축

| 축 | 판정 |
|---|---|
| 의도 보존 | **충족.** A의 500과 C의 취소 누락을 다른 PR로 다루되 둘 다 기록했고, D5의 화면 표시를 spec SP07·T09로 연결했다. |
| 설계 충실성 | **정적 확인.** 잠금 재시도 때 rollback·재적용, 루프 밖 동기 DB, 최신 행 판정, 취소·`timed_out` 원자 갱신과 프런트 오류 상태가 각 diff에 있다. 실제 DB 방언별 취소 효과는 확인하지 못했다. 0003 SP06-102의 오래된 순서를 T08에서 정정했으므로 그 과거 문서만 현재 계약으로 쓰면 오판한다. |
| 계획 실행성 | **구체적.** plan `:92-117,139-324,334-568`은 PR 선후·TDD 입력/RED/GREEN·실파일 경합과 화면 기대를 지정했다. 문서 후속 커밋은 갱신 사실을 보이나 실제 RED→GREEN 시간 순서의 독립 로그는 아니다. |
| PR·병렬 분할 | **의존성 명확.** #343 머지 뒤 #344 설계를 보완하고 시작했다. 공유 실행 경로의 A/E를 먼저 안정화해 C를 붙였다. 별도 에이전트 핸드오프 원문은 없다. |
| 변경 피드백 | **반영.** 리뷰에 따른 문서·시험 수정과 요청자 D5가 커밋으로 남았다. 기존 가짜 세션 시험의 변경 이유는 plan T01에 명시돼 시험 약화 여부 판단 자료를 준다. |
| 검증·보고 | **방법은 강하나 결과 증거는 제한적.** 실파일·별도 프로세스 경합은 SQLite 잠금 오류를 직접 겨냥한다. PR 본문의 성공 수치, 실제 취소/게이트 출력은 독립 수집되지 않았고 V5-C는 미실행이다. |

H1: C 화면 범위 증가는 요청자의 후속 결정이며 초기 설계 결함으로 셀 수 없다. A의 루프·세션 경계는 이전 0003 이식의 누락이다. H2: 화면 표시의 상태·배지 계약은 있으나 실제 UI 심미성 판단 자료가 없어 근거 부족. H3: 동기 DB/이벤트 루프·워커/취소/상태의 공유 순서가 핵심이었고 spec SP02·SP05에서 사전에 설계한 뒤 구현했다. H4: 최초 plan의 실파일 경쟁 시험은 가짜 fixture 사각을 명시적으로 보완해 가설의 긍정적 대조다. 다만 머지 뒤 실DB 취소와 화면 통합을 완료로 주장할 수 없다.

당시 실제 스킬 설치·호출은 미확인이다. 현행 0.1.8은 공유 계약·구현 방법·독립 기대·미실행 기록을 이미 요구하며 기존 WIP는 정책 진입점의 계획 구체성 문구만 보강한다([기준](../baseline.md)). 이 사례는 현행 지침 적용·검증 범위를 먼저 확인할 근거이지 곧바로 새 규칙을 만들 근거는 아니다.
