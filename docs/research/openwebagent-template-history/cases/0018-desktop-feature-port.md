# 0018 desktop-feature-port — 복구 범위, 접점 분리와 통합 검증

조사 상태: **evidence-limited**. 초기 요구·설계·계획과 아래 주요 사건 사슬은 검토했다. 0018 전체 구현을 재실행하거나 모든 리뷰의 원문을 확인하지는 않았다. 제품의 완료 상태와 이 조사 문서의 검토 상태는 별개다.

후속 인계: 아래 pilot 당시의 미검토 표는 보존한다. 이후 [middle](0018-followups-middle.md),
[late](0018-followups-late.md), [authority](0018-followups-authority.md)가 해당 사건 일부를 보완했다.
현재 잔여 범위는 [coverage](../coverage.md)를 따른다. 후속 보고서도 전체 코드·모든 상태·런타임 감사는 아니다.

0018에는 구현 전 접점 설계와 시험 전략이 있었다. 그럼에도 실제 엔진 구독 제약, 사용자별 회수 경합, 공유 알림 DTO와 통합 화면에서 추가 수정이 필요했다. 이 사례는 설계를 생략한 개발로 분류할 수 없다. 설계에서 둔 가정의 검증 범위, 각 레인의 전달 범위와 결합판에서 관측한 범위를 함께 봐야 한다.

## 조사판과 근거 구분

- 저장소: `bifrost17/openwebagent`. 동결 main **M** = `a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e`.
- 미병합 release 조사판 **R** = `824332017802c7daa98bd4b29b8e7455b92aac12`, `codex/0018-backend-regression-release`, [PR #435](https://github.com/bifrost17/openwebagent/pull/435). 수집 API에서 open이다. R의 성과를 M의 기능으로 합치지 않는다.
- 경로 약어 **I** = `intent/0018-desktop-feature-port/`, **D** = `apps/open-webui/backend/open_webui/routers/openhands/codex_desktop/`, **F** = `apps/open-webui/src/lib/`.
- 표의 `SHA:path:line`은 그 Git 객체의 줄이다. `M:I/tasks/T18.md:28`은 위 동결 M의 해당 경로 28행을 뜻한다. 현재 checkout 줄 번호와 혼용하지 않는다.
- 원자료·추출물: `.local/research/openwebagent-template-history/20261003/analysis/0018/`. `source-manifest.json`에 주요 ref의 전체 SHA, `commit-index.tsv`에 I 경로 이력 545건, `pr-index.json`에 branch/title로 찾은 PR 57건을 보존했다. 545건은 조사자가 모두 심층 검토했다는 수치가 아니다.
- Git 코드·시험·문서와 PR 메타데이터를 읽었다. 아래 PASS/FAIL 수치는 **당시 기록의 주장**이다. 이 조사에서 해당 시험·후보 스택을 재실행하지 않았다. 보존된 시험 코드가 기대를 다루는지 일부 교차 확인했으며, /tmp 로그의 현재 존재·해시까지 전부 확인하지 않았다.
- 수집 `pr-details.json`에서 주요 PR의 `reviews` 배열은 비어 있다. 문서의 “독립 리뷰”를 GitHub review 이벤트로 재분류하지 않는다. 본문에 남은 검토자 기록·수정 커밋·실행 수치는 별도 증거다.

바로 읽을 수 있는 고정판 근거: [최초 plan](https://github.com/bifrost17/openwebagent/blob/666bcad21ee97d3a9974dd516cb8cc3b07a30ac3/intent/0018-desktop-feature-port/plan.md#L51), [구현 전 접점·순서](https://github.com/bifrost17/openwebagent/blob/12790637edc689e351efda598f859310cfe1160d/intent/0018-desktop-feature-port/plan.md#L45), [Q15 탐침](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0018-desktop-feature-port/references/probes-2026-09-29.md#L32), [M1d 실패](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0018-desktop-feature-port/references/m1-observation-2026-09-30-m1d.md#L18), [release 잔여 작업](https://github.com/bifrost17/openwebagent/blob/824332017802c7daa98bd4b29b8e7455b92aac12/intent/0018-desktop-feature-port/plan.md#L3).

## 주요 사건 사슬

| 사건 | 요구·설계·계획의 당시 상태 | 구현·검증·인계에서 확인한 변화 | 근거 |
|---|---|---|---|
| 2026-09-28 최초 intent | 0005 T27 전환 후 안전장치·패널·입력 기능의 공백을 열거. 재사용하지 않는 legacy 코드 제거를 제안 | 직전 0005에서 사용자가 “전환 먼저, 이후 이식”을 골랐다고 기록. 0018의 공백 자체를 무단 기능 삭제라고 단정할 수 없음 | `75d25896644a767ae2c7788538eda30c04d26dee:I/intent.md:6-35`; 선행 [#355](https://github.com/bifrost17/openwebagent/pull/355) |
| 요청자의 범위 교정 | “끊긴 기존 와이어 복구”로 한정. 남은 부품은 재연결 대상이며 모양·동작도 legacy처럼 유지 | 새 기능 추가·일괄 잔재 삭제 해석을 초기 단계에서 수정. 이후 시각 검증의 기대도 이 요구에서 나옴 | `7c65adee2cb2e02a0d7015e8a8fdfe1703a50367:I/intent.md:11-43` |
| 초기 spec → 수락 | `213df9e20`에서 FR01~13·AC01~14·SP01~07, `8852b6b51`에서 실측 Q9·FR14/SP08 보강. SP08 회수, SP09 목표 및 클래스 설계가 반복 리뷰로 확장 | `39324c790`이 요청자 수락 기록. 기록상 spec 10회 리뷰와 Astra/Opus 결과가 있으나 리뷰 전체 대화는 미확인 | `666bcad21ee97d3a9974dd516cb8cc3b07a30ac3:I/plan.md:2-14`; [#364](https://github.com/bifrost17/openwebagent/pull/364) |
| 첫 plan | PR-A 배포 차단 해소 → PR-B 안전 → PR-C 목표 → PR-D/E/F 화면 → PR-G 정리. legacy 시험 이식과 새 수명 경계 TDD를 구분 | 첫 plan은 단위별 Done·명령·후보 관측·최신 main 결합 조건까지 명시. 초기 검증 방법이 없었다는 가설의 반례 | `666bcad21:I/plan.md:51-78,82-108` |
| 구현 전 병렬 재설계 | 2판 `1a26b57f0`, 3판 `12790637e`에서 T00a/b 이음매, B1~B18/F1~F8, 공유파일 순서·소유·병합 조건을 추가. 4~5판 후 최종 `722e4c201` | 7개 큰 PR 방식에서 기능별 레인으로 변경. 공유 접점이 새로 발견되면 부모가 보강 PR을 먼저 통합하고 재개하도록 명시 | `12790637edc689e351efda598f859310cfe1160d:I/plan.md:45-161`; [#364](https://github.com/bifrost17/openwebagent/pull/364), [#369](https://github.com/bifrost17/openwebagent/pull/369) |
| 첫 코드 전달 T02 | 활동 보고·회수 원함을 먼저 연결. 보고 없는 이전 WebUI와 호환한다는 계약 | `a79d271ef` 구현, `810fd341c` 신원·감사 시험, #366 병합. 별도 Claude T02 #368은 merge 없이 닫힘. 중복 작업의 실제 비용은 미확인 | [#366](https://github.com/bifrost17/openwebagent/pull/366), [#368](https://github.com/bifrost17/openwebagent/pull/368); 초기 `plan.md:94-108` |
| 엔진 탐침과 Q15 번복 | 0.155.1 RPC를 먼저 관측하겠다는 계획 | 잘못된 `goalsEnabled` 입력을 폐기. 단일 idle 구독에서는 unsubscribe/resume 후 goals 적용, 두 번째 구독·진행 턴에서는 ACK 성공에도 자동 0턴·도구 미노출. Q15을 미해결로 되돌림 | `M:I/references/probes-2026-09-29.md:26-58`; [#367](https://github.com/bifrost17/openwebagent/pull/367) |
| T00a/b 초기 인도 | 기존 동작 보존과 비활성 확장점 분리를 먼저 전달 | T00a 뒤 `prove` 안전 kind·provider/cwd 문맥 등 누락 접점을 #372로 보강. T00b 리뷰는 composer 등록 API·saved options DTO 불일치를 발견 | `M:I/tasks/T00a.md:57-65`; `M:I/references/t00b-seams/baseline.md:43-61`; [#371](https://github.com/bifrost17/openwebagent/pull/371), [#372](https://github.com/bifrost17/openwebagent/pull/372), [#370](https://github.com/bifrost17/openwebagent/pull/370) |
| T00b 화면 보존 시험 | 실제 CodexDesktopChat를 Vite/Chromium에 mount. HTTP/SSE만 fixture로 통제 | 제품 무수정 harness `0e25c3a9f9` → 추출 `fcf98fec70`. 7장면×2테마 DOM·PNG와 focus/node identity를 비교했다고 기록. hand-written HTML mock으로 분류하면 잘못임 | `M:I/references/t00b-seams/baseline.md:5-32`; [#370](https://github.com/bifrost17/openwebagent/pull/370) |
| T00b 검증 근거 정정 | 전용 candidate 이미지 규칙이 이미 존재 | 운영 이미지 사용분을 정본에서 제외하고 #370 병합판 전용 candidate로 재시험. macOS ConfirmModal 대소문자 충돌·전체 typecheck 실패·진단 SQLite와 Docker 정본을 분리 | `M:I/references/t00b-seams/baseline.md:3,38-41,95-110`; `M:I/tasks/T00b.md:99-101`; [#375](https://github.com/bifrost17/openwebagent/pull/375) |
| T03 수명 연결 | 명령 claim·settlement와 활동·release blockers가 서로 의존 | `5a1d77b15b`에서 필수 hook 순서를 보완. 생산 편집이 실행 가능한 RED보다 앞선 순서 이탈을 기록하고 사후 RED를 구분 | `R:I/plan.md:3704-3708`; [#383](https://github.com/bifrost17/openwebagent/pull/383) |
| T18 알림 통합 결함 | threadId 없는 알림은 같은 owner의 열린 대화에 전달. F7 feature 구독과 공유 reducer를 분리 | `a4ecb0d21f` 뒤 리뷰가 여덟째 warning 누락을 찾음. `bc378f2d6`은 backend allowlist/fanout, F7 DTO, shared reducer shape guard와 시험을 함께 변경. 파일 분리만으로 교차 계약이 완성되지는 않았음 | `M:I/tasks/T18.md:4-30`; `bc378f2d6403224ef43ad8c3c6702176ed2c8c01:D/notices.py:115-140`; [#390](https://github.com/bifrost17/openwebagent/pull/390) |
| T08 첫 결합 관측 | M1은 회수 기반·권한·첨부 통합을 본다. 기능 모듈 시험과 후보 관측은 별도 | 9/29 초기 후보 blocker와 fixture 완료를 각각 기록. 9/30 m1c 재가입 실패도 남김. 이 문서들의 존재·상태를 확인했으나 각각의 모든 원출력은 미검토 | `M:I/references/m1-observation-2026-09-29.md`, `m1-observation-2026-09-30.md`; [#395](https://github.com/bifrost17/openwebagent/pull/395), [#396](https://github.com/bifrost17/openwebagent/pull/396), [#412](https://github.com/bifrost17/openwebagent/pull/412) |
| Q15 gateway 설계 변경 | 단일 구독을 강제할 제품 경계 필요. `23d409bee` 승인 문서 뒤 비활성 launcher, broker core, transport/control, runtime, probe 순서 | `2aaaa1722` → `f6c503d62` → `e939c1c51` → `3a6474bf6`. Linux shutdown에서 1 FAIL 후 보정, pinned runtime의 owner/UDS/FD9 관측을 분리 | `M:I/tasks/T14.md:159-188,424-588`; [#402](https://github.com/bifrost17/openwebagent/pull/402) |
| Q15 소비자·entrypoint 전환 | readiness·PID/bounce·MCP·latency 도구를 포함한 소비자 이전을 선행으로 추가 | `3946af9fa`는 23파일에서 orchestrator, entrypoint, MCP/latency 도구·시험을 함께 바꿈. 이후 candidate stack opt-in `bc406f07c`. gateway만 TCP, engine private UDS 경계이며 기본 OFF를 유지 | `3946af9fa65da8bde7e2fab5ae87d3dbc7e6ae7b:sandbox/codex-entrypoint.sh:7-17,372-390`; `R:I/plan.md:3972-4135`; [#408](https://github.com/bifrost17/openwebagent/pull/408), [#409](https://github.com/bifrost17/openwebagent/pull/409) |
| M1d 실제 실패 | `13af3c3e04` 후보에서 첫 답변·유휴 뒤 이력 재열기는 성공 | 재열기 뒤 첫 전송은 `/ensure 503:not-ready`, 두 번째 submission row 없음. stop 중 ensure가 running을 읽는 순서를 소스 함수 barrier로 재현. 실제 요청 내부 분기는 추론으로 남김 | `M:I/references/m1-observation-2026-09-30-m1d.md:3-31`; [#418](https://github.com/bifrost17/openwebagent/pull/418) |
| 회수 경합 수정·재리뷰 | AC15g의 기존 직렬화 기대 유지 | `274642822` 사용자별 claim → `cc62e5203` 취소 drain·clock 재확인 → `f7a2388d6` 조회 timeout·파괴 pause 처리 → `a9438af04` activity 응답의 누락 조회 보완. host 626 PASS 기록과 Docker daemon 무응답 한계를 함께 인계 | `2746428221e5a6d2f7bc9f39bd9f9efb6586c351:orchestrator/tests/test_ensure_lock_granularity.py:446`; `M:I/tasks/T03.md:50-115`; [#420](https://github.com/bifrost17/openwebagent/pull/420) |
| M1e 재관측 | 미병합 #420의 `6b56c61dee` 후보, 텍스트 mock | 후속 답변 완료 화면은 보존. sandbox 종료 출력·DB 쿼리·요청 로그는 미보존이라 정확히 두 제출·유휴 stop을 독립 재확인 불가. M1 Done을 선언하지 않음 | `M:I/references/m1-observation-2026-09-30-m1e.md:3-26`; [#423](https://github.com/bifrost17/openwebagent/pull/423) |
| 실제 화면과 fixture의 차이 | legacy 모양 복구 요구는 그대로 | M1d Working 행이 부모와 함께 translate되어 158px 추가 이동. 이후 picker 중심이 composer에 가려지는 hit-test 결함과 요약 코너 토큰을 보정. 최신 picker2에서 실제 겹침 클릭·입력을 따로 관측 | `M:I/references/m1-observation-2026-09-30-m1d.md:33-37`; `M:I/references/picker-reference-aside-2026-09-30.md:26-39`; [#410](https://github.com/bifrost17/openwebagent/pull/410), [#417](https://github.com/bifrost17/openwebagent/pull/417), [#428](https://github.com/bifrost17/openwebagent/pull/428) |
| 목표 UI 요구 보완 | 9/30 사용자의 compact bar·편집면 결정을 기존 legacy 모양 요구의 예외로 기록 | 제품 코드 전에 intent/spec/classes/T14 정합을 요구. OFF UI 준비와 실제 목표 저장·Q15/D6를 분리. 최초 spec 수락 SHA를 새 표시 요구의 수락으로 재사용하지 않음 | `R:I/plan.md:3521-3522`; `M:I/tasks/T14.md:197-268`; [#432](https://github.com/bifrost17/openwebagent/pull/432) |
| 10/1 product 연결·handoff | gateway/typed client/GoalWatch/인증 stage 결합과 W59 도구 이전 | `6d1873bb5`, `8315cd4ab`, `8ec5a45bf` 등 주요 변경을 commit index와 R plan에서 추적. 세부 private lifecycle 전체 diff는 미검토. frontend 정리만 #440으로 별도 main 병합 | `R:I/plan.md:2908-3132,4449-4540`; [#435](https://github.com/bifrost17/openwebagent/pull/435), [#440](https://github.com/bifrost17/openwebagent/pull/440) |
| 10/2 결합판 회귀 | D6 OFF 일반 thread에 명시적 false 필요하다는 9/29 탐침 기대 유지 | 실제 OFF 실행에서 목표 도구 노출을 발견. `3bc29ab34` 수정. 정상 SIGTERM/열린 SSE, completion ownership, turn-review routing·locale 등 추가 회귀 수정. focused 통과를 release로 확대하지 않음 | `R:I/plan.md:94-116,149-169`; `R:I/tasks/T26.md:199-249,342-531`; [#435](https://github.com/bifrost17/openwebagent/pull/435) |
| 10/2 최종 검증 도구 보정 | 전체 backend 8599 PASS/2 FAIL 기록을 유지 | 두 실패의 준비 경합을 분리해 fixture `612456beb2` 보정. 새 TurnReviewRouting component가 명시 browser 목록에서 빠져 `6a58679a8` 등록. R에서도 전체 회귀·immutable build·실제 E2E·성능·동시성·release가 남아 있음 | `R:I/plan.md:3-9,13-92`; [#435](https://github.com/bifrost17/openwebagent/pull/435) |

## 여섯 축 판정

| 축 | 판정 | 잘 작동한 부분 | 결함·공백과 귀속 |
|---|---|---|---|
| 의도 보존 | 검토 범위에서 사용자 교정·추가 결정을 추적 가능 | 초기 “부품 삭제” 해석을 즉시 재연결 범위로 바꿈. compact goal UI는 예외와 새 수락 경계를 명시 | 모든 사용자 발언 원문은 없음. 문서의 요청자 귀속은 기록 근거이며 원대화 확인을 대신하지 않음 |
| 설계 충실성 | 선행 설계 있음, 일부 핵심 가정은 미검증 상태 | SP08/SP09·클래스 구조·Q15 미해결 gate·접점 표를 코드보다 먼저 둠 | 단일 subscriber 가정, notification DTO, reclaim async 구간, D6 명시 false의 제품 연결 누락. 우선 제품 설계/agent 구현 문제이며 템플릿 결함 귀속은 비교 후 판단 |
| 계획 실행 가능성 | 초기안보다 리뷰 후 실행 조건이 구체화 | legacy 이식/새 경계 TDD/후보 관측을 구분하고 파일 소유·시작/병합 조건을 둠 | 초기 M1 배포 해제 표현이 후속 M1/M2 분리로 정정. T00a/b 이후에도 접점 보강·등록 누락이 반복. “접점 표가 있다”와 “소비자까지 실행으로 확인했다”를 구별할 필요 |
| PR·병렬 분할 | 일부 독립 전달 성공, 큰 통합 tail 존재 | T02, T18, frontend cleanup 등의 별도 PR과 결합판 확인 | 57 PR 중 #435는 여전히 open. 모듈 경계가 DTO·수명·실제 UI 통합을 대체하지 못함. 단순 PR 개수나 크기로 성공/실패를 판단하지 않음 |
| 변경 피드백 | 정정·실패 보존의 좋은 근거가 다수 | Q15 answered 철회, wrong probe 입력 폐기, callback/등록/fixture 수정의 근거·한계, T03 사후 RED 구분 | 최근 문서의 누적 기록만 읽으면 당시 불완전 인도가 사라질 위험. 각 코드판/인계판을 따로 읽어야 함 |
| 검증·보고 정확성 | 증거 층을 잘 나눈 구간과 실제 누락이 공존 | 실제 component/합성 engine/후보 browser/host regression을 구별. M1e 로그 미보존·CodeRabbit rate limit을 숨기지 않음 | 전용 이미지 규칙 위반 후 재시험, 전체 gate 미등록, 실제 E2E 후발 발견. 작성된 시험·수동 PASS·CI 등록·배포 실행을 같은 완료로 취급할 수 없음 |

## 네 가설 검증

**H1 — 설계 부족 때문에 잦은 설계 변경·계획 이탈이 발생했다: 부분 지지.** notification shape·reclaim await 이후 소유·Q15 준비 경계의 부족은 구체 사건으로 확인된다. 다만 spec 10회·plan 5판, 구현 전 접점 분리와 탐침이 있었고, Q15 변경은 엔진 실측이 초기 가정을 반박한 결과다. 변경 횟수를 곧바로 설계 부족의 크기로 세면 사용자 결정, 정상 탐색, 구현 결함, 검증 환경 보정을 섞게 된다.

**H2 — 실제 UI 모양보다 HTML mock만 봤다: 일반화는 반증, 통합 화면 공백은 지지.** T00b의 HTML은 실제 제품 component 렌더 결과이며 DOM/PNG/focus 비교를 했다. 그 fixture가 이후 summary panel·Working 행·picker 겹침 조합까지 입증한 것은 아니다. M1d와 picker2 사건은 실제 화면 조합과 hit-test를 early vertical slice에 넣을 근거다. “브라우저를 썼다”는 표지만으로 실엔진·실제 로그인·실제 모델 사용까지 뜻하지 않는다.

**H3 — 모듈을 늦게 합쳐 실패했으므로 전체 계약과 순서를 먼저 정의해야 한다: 부분 지지.** 계획 3판의 B/F 접점 표와 공유파일 순서는 이미 해당 처방을 상당 부분 시행했다. T18 warning은 producer DTO→fanout→F7→shared reducer의 끝까지 이어지는 계약이 빠졌고, Q15는 엔진 boundary만 만든 뒤 readiness·PID·도구·entrypoint의 소비자 계약을 추가로 정리해야 했다. 개선 실험은 “문서를 더 상세히”보다 **첫 인도에서 실제 소비자가 통과해야 할 수직 경로를 고르고 검증**하는 방향이어야 한다. 각 모듈 내부 코드를 전부 설계 완료해야 한다는 주장은 이 사례만으로 입증되지 않는다.

**H4 — 초기에 검증 방법을 충분히 고려하지 않았다: 부분 지지.** 첫 plan에 시험 방식·기준선·명령·후보 관측·독립 검토가 있었다. 뒤늦은 test census 등록, fixture 준비 경합, 합성 공급자와 실제 제품 조건 차이는 실행 가능한 검증 준비가 덜 완성된 지점이다. 단위시험을 더 만드는 처방만으로 해결되지 않는다. 첫 runnable 후보의 조건, 어떤 상태를 누가 보존하는지, 새 시험이 정식 명령에서 발견되는지를 초기 전달 기준에 넣는 실험이 적절하다.

## 당시 규칙과 현재 0.1.8·WIP5의 비교 입력

이 사례에서는 현재 템플릿 문장을 새로 만들거나 수정하지 않았다. 당시 0018 plan은 이미 설계 근거, 검증 방법, 실패 보존, 공유파일 소유·병합 순서, 독립 검토를 요구했다. 따라서 다음 항목을 곧바로 “템플릿에 없던 규칙”으로 올리지 않는다.

| 개선 후보 | 사건 근거 | 우선 귀속 | 0.1.8·WIP5 비교에서 확인할 것 |
|---|---|---|---|
| 첫 전달 가능한 수직 경로와 소비자 계약을 정한다 | T18 warning, Q15 gateway 소비자 전환, OFF 목표 도구 노출 | project design/agent, template은 미판정 | 현재 plan guidance가 순서뿐 아니라 첫 실행 결과와 producer→consumer 검증까지 다루는지 |
| 실제 제품 component와 실제 후보 E2E를 구분하고 조합을 고른다 | T00b 보존 성공 후 Working/picker 결함 | verification design/agent | 현재 검증 전략·UI 규칙에 이미 있다면 중복 규칙 추가 없이 예제/평가 사례로 사용 |
| 초기 검증 경로가 실제로 실행 가능한지 확인한다 | test census 누락, 후보 run ID·fixture 준비·OS 문제 | tooling/project-policy/agent | 0.1.8 또는 WIP5가 기존 gate 재사용·검증 방식 선정을 얼마나 구체화했는지 |
| 실패와 사후 증명을 원 실행에서 분리한다 | T03 사후 RED, M1e 미보존 로그, CodeRabbit rate limit | agent/evidence | 이미 해결된 규칙이면 회귀 평가 입력으로만 유지 |

**현재 기준과의 문장별 차이·템플릿 수정 필요 여부는 기준판 담당 조사와 결합 전 미판정이다.** 사건이 있다는 이유로 현재 규칙의 결함을 확정하지 않는다.

## OS·모델과 인과 추정의 한계

| 항목 | 알려진 사실 | 모르는 것 |
|---|---|---|
| 호스트/컨테이너 | T00b macOS의 대소문자 비구분 ConfirmModal 충돌, Node22 경로와 Linux candidate 재시험 기록. M1d/e arm64 image ID. Q15 Linux SO_PEERCRED·/proc·FD9 관측과 호스트 주입 시험 구분 | 전 건의 호스트 OS/아키텍처를 일괄 확정할 자료 없음. Windows 실행 근거를 이 조사에서 찾지 못함 |
| 최초 모델 배정 | plan 3판은 핵심 T00a/b/T03/T14 opus, 나머지 sonnet, 동시 10을 제안 | 계획의 모델명이 실제 실행 모델인지 확인 불가 |
| 실제 모델 기록 | T03은 `Sol high`, T18은 `gpt-6-sol`, T14는 Astra급 프로토콜 검토·Sol high 구현·Luna 도구·Astra max 경합으로 기록. 일부 UI 검토는 `Sol 6.1 High` | 정확한 세션별 model ID·reasoning effort·교체 시점은 모두 확인되지 않음. Git author/branch prefix를 모델 증거로 사용하지 않음 |
| 비용/성능 | 반복 리뷰·후속 PR·실패 사건이 존재 | 모델 선택 때문에 실패했는지, 다른 모델이면 절감됐을 시간·비용은 반사실 자료가 없어 계산 불가 |

모델 기록 출처: `12790637e:I/plan.md:126-161`, `M:I/tasks/T03.md:4`, `M:I/tasks/T18.md:4`, `M:I/tasks/T14.md:6,159`. OS 기록 출처: `M:I/references/t00b-seams/baseline.md:38`, `M:I/tasks/T00b.md:101`, `M:I/tasks/T14.md:443-588`, `R:I/plan.md:25-28`.

## 검토 범위와 남은 입력

| 범위 | 조사 상태 | 남은 작업 |
|---|---|---|
| 최초 intent 교정, 초기 spec/plan, 구현 전 접점·순서 전환 | reviewed | 리뷰 대화 원문이 필요한 경우 아래 질문으로 한정 |
| T00a/b 첫 인도·수정, T18 notification, Q15 탐침→gateway, M1d/e 회수 실패와 #420 | reviewed, 실행 증거는 evidence-limited | 주요 코드/시험과 기록은 대조. 원 런타임 로그·모든 리뷰 원문·현재 재실행은 없음 |
| T14 private product preparation·GoalWatch·typed client·ownership 후속 | evidence-limited | R plan의 주요 사건과 커밋 순서는 확인. 전체 구현 diff와 인증/정리 race 행렬 미검토 |
| T06/07/09/10/11/12/13/15/16/17/19/20/21/22/23/24의 개별 전체 구현·모든 리뷰 | not-reviewed 또는 사건 표의 좁은 부분만 reviewed | 분할 인도 목록은 확보했지만 각 AC→구현→최종 통합 검증 전체 사슬은 아직 필요 |
| T25 frontend cleanup와 W59 전체 도구 이행 | evidence-limited | #440 병합과 R handoff 확인. backend cleanup·모든 도구 runtime은 미검토 |
| T26 최종 regression/성능/동시성/release | evidence-limited | R 자체가 미완료. 최신 전체 회귀·immutable build·동조건 성능과 actual E2E 필요 |

사소한 반복 merge·단순 수치 재기록·포맷 정정은 사건의 기대/구현/증거/상태를 바꾸지 않으면 별도 행으로 반복하지 않았다. 위 `not-reviewed` 범위는 사소해서 제외한 것이 아니다. 중요하지만 이번 pilot에서 다 읽지 못한 범위다.

원대화가 있어야 확정되는 질문은 다음으로 한정한다. 세션 ID는 현재 Git/API 자료에서 확인하지 못했다. 전체 채팅을 읽지 않고 root 조사에서 날짜·주제에 맞는 세션만 찾을 수 있다.

- 2026-09-28: spec 10회/plan 5판에서 요청자가 기대한 “충분한 설계”의 범위와 승인 조건. 문서의 수락 기록 외 원 발언 확인.
- 2026-09-29~30: Q15 단일 subscriber 탐침을 answered로 두었다가 철회한 인계의 실제 설명과 새 gateway 구현 위임 범위.
- 2026-09-30~10-02: 각 레인의 정확한 model ID·추론 수준과 교체 이유. 모델별 결함률·비용 비교를 하기 전에 필요.
- 2026-10-01~02: #435 결합 담당자가 최종 완료를 선언했는지 여부. 현재 R에는 명시적 미완료 목록이 있으므로, 별도 전체 완료 주장을 추정하지 않는다.
