# 0029 — 표 없는 생성 SQL을 되묻기

판정: **검토 완료, 실행은 기록 한정.** text2sql이 답할 수 없는 질문에 `SELECT 1` 같은 표 없는 상수 SQL을 정상 결과로 내던 결함을 막았다. [PR #471](https://github.com/bifrost17/openwebagent/pull/471)은 뒤따르는 #472(0030)의 기반이었다. 고정 원본 main은 `a08295f`.

| 사건 | 근거·범위 |
|---|---|
| 요청·최초 계약 | [`6078701`](https://github.com/bifrost17/openwebagent/commit/6078701753836630e6669bf82a9a9620033a3f7d) 문서가 intent/spec/plan을 먼저 Git에 남겼다. `spec.md:9-25,33-44`는 한 문장·파싱 가능한 조회의 실제 참조 표가 0개면 재시도 없이 422 `clarification_needed`, face 검사 0회·장부 행 1개·SQL 비노출, 에이전트/콘솔 공통을 정했다. 불가독 SQL은 기존 face로 넘긴다. `intent.md`와 `plan.md:65-71`은 수정 전 `:3080` CLI 6질문 모두 rc0·빈 assumptions, 수정 후 대표 4질문 rc1·정상 질문 rc0을 보고한다. 실행 로그 원본은 이번 수집에 없다. |
| 코드·시험 | [`0791ef8`](https://github.com/bifrost17/openwebagent/commit/0791ef82c7ee6c4a99cce53ade3e4b9df6f0d4ea)은 `sql_tables.py`와 라우트·시험을 추가했다. 처음 판의 CTE 이름 판별은 범위별이 아니었고 CI 매니페스트에 새 시험을 빠뜨렸다. 새 문맥 구현 검토 뒤 `plan.md:31-37,73-75`와 다음 수정 판에서 `traverse_scope`·`DUAL`·CTE 대소문자, 매니페스트를 보완했다. RED는 새 모듈 수집 `ModuleNotFoundError`와 라우트의 실제 200 2건을 구별해 적었다(`plan.md:65-69`). |
| PR 리뷰 | [`727d56e`](https://github.com/bifrost17/openwebagent/commit/727d56eabe8bd062a2035477a18aa39828bba3eb)가 코드 리뷰 6건 중 2건을 반영했다. 조회 아닌 `DELETE`·`DROP`·`SHOW`를 “표 없음”으로 잘못 되묻지 않게 `exp.Query`가 아니면 `None`; 스키마 한정 뒤 `FROM DUAL`/CTE가 실제 표처럼 보이는 것을 막으려 한정 전 SQL로 판정한다. 최종 `sql_tables.py:35-61`, `router.py:962-975`로 직접 확인했다. T04의 새 시험 10개 RED→GREEN과 전체 text2sql 572 passed는 `plan.md:77-81`의 실행 주장이다. |
| 통합·후속 | [`dd15ffb`](https://github.com/bifrost17/openwebagent/commit/dd15ffbd6e36d847552ace17c52e7f8218bdb0ee)로 #471 머지, 뒤이어 [#472](https://github.com/bifrost17/openwebagent/pull/472) 0030이 `referenced_tables`를 재사용해 없는 표 판정을 추가했다. frozen main `a08295f`의 같은 경로에는 0030 후속 코드도 포함된다. `0029 plan.md:4-5`의 “머지는 요청자 결정 대기”는 머지 후 현재 인계 문구로 갱신되지 않았다. |

여섯 축: **의도 보존**은 상수 SQL을 되묻되 봉투·장부 어휘 유지. **설계 충실성**은 실제 표/CTE/DUAL/판정 불가 경계가 검토·리뷰를 거쳐 spec AC와 일치한다. **계획 실행 가능성**은 판정 함수→공통 라우트→실모델 추가 증거로 나누고 시험 매니페스트 등재를 검토에서 보충했다. **PR/병렬 분할**은 0030을 이 PR 위에 쌓고 순서대로 머지했다. **변경 피드백**은 CTE 범위·비조회·스키마 한정 시점의 오판을 코드로 고쳤다. **검증/보고**는 집중 572 passed와 e2e 4질문 단발을 기록하며 전체 백엔드/CI는 미실행이라고 PR이 밝힌다. `docker cp` 반영은 임시이고 실모델 출력은 비결정적이다.

**PR 본문 정확성:** #471 본문의 한계에 “`SHOW TABLES` 같은 표 없는 비-SELECT는 되묻기가 된다”고 남았지만 최종 `727d56e:sql_tables.py:40-43`은 비조회 `None`(판정 불가), `router.py:965-975`는 `[]`만 되묻고 `None`은 face에 넘긴다. 코드 리뷰 수정 뒤 PR 본문·plan 마지막 한계 문장이 낡은 것이다. “SHOW는 실행기 파서가 어차피 거절”은 별개 단계의 예상으로 이 오기된 되묻기 주장을 구제하지 않는다. `6078701` spec FR01의 “한정 뒤 판정”도 최종 코드의 한정 전 판정으로 후속 정정됐는지 현행 문구를 읽어야 한다.

가설: H1 **부분 지지**(최초 설계의 CTE/비조회/한정 시점 구멍을 검토로 고침), H2 **범위 밖**(CLI·서버 중심, 콘솔은 같은 라우트를 쓰지만 화면 실브라우저 없음), H3 **후속 연결 성공**(0030이 함수를 재사용, 이 PR 자체의 통합 충돌은 없음), H4 **부분 지지**(판정·e2e 계획은 있었으나 CI 등재와 반례는 후반 보강). 원인은 제품의 SQL AST 범위 판정과 리뷰 피드백이며 현행 0.1.8/WIP의 검증·문서 갱신 요구 부재로 단정하지 않는다. 표 없는 정당한 조회의 오탐, 모르는 방언에서 검사를 건너뛰는 한계는 남는다. 모델·OS는 문서의 Sonnet 검토 진술 외에 확인되지 않는다.
