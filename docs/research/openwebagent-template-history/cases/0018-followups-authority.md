# 0018 후속: T14 권한·준비 수명과 T26 최종 인도

조사 상태: **중요 사건 reviewed, 실행 증거 evidence-limited, 일부 하위 경계 not-reviewed**. [기본 사례](0018-desktop-feature-port.md)를 보완한다. 제품 T14/T26의 완료를 뜻하지 않는다. 원 제품·템플릿을 변경하거나 시험을 다시 실행하지 않았다.

T14는 단순 목표 배너 복원에서 시작했지만 최종 인도에는 제품 DB의 binding/writer, native client의 원 RID·연결, gateway의 공유 준비 작업, 실제 엔진 설정, 정상 종료를 연결하는 작업이 필요했다. 분리 시험 통과 후 반복 결함은 확인된다. 다만 초기 설계와 혼합 검증 계획이 있었고, 뒤의 실패를 숨기지 않은 기록도 많다. “설계가 없어서 실패했다” 또는 “문서를 더 쓰면 해결된다”는 결론은 근거보다 넓다.

## 출처와 읽는 법

- `I` = `intent/0018-desktop-feature-port`; `D` = `apps/open-webui/backend/open_webui/routers/openhands/codex_desktop`; `B` = `apps/open-webui/backend/open_webui/routers/openhands`.
- `R` = 미통합 release head `824332017802c7daa98bd4b29b8e7455b92aac12`; `M` = frozen main `a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e`. `R:I/tasks/T14.md:129-164`는 그 Git blob의 1-based 줄이다.
- [PR #435](https://github.com/bifrost17/openwebagent/pull/435)는 수집 API에서 **open, merged_at=null**. 본문은 `2528f598c9f70511d71b56ab7268222c6e20bf60` 대상이며 API head R과 다르다. 본문의 Draft·미완료 표시, 과거 이미지의 source SHA를 그대로 보존한다. 최신 head의 full PASS로 읽지 않는다.
- 원문·초기 task·선택 code/test diff·PR JSON은 private `analysis/0018-authority/`에 보존했다. 본문에 인용한 `/tmp` 실행 로그는 Git 문서의 위치/hash 기록을 확인한 것이며 이번 조사에서 해당 원로그를 모두 확보·재실행한 것은 아니다.

## 초기 계약에서 첫 실행까지

| 사건 | 확인한 원문·실행·변경 | 판정과 근거 |
|---|---|---|
| 초기 SP09 | 최초 설계는 RuntimeSession이 thread별 GoalWatch를 소유하고, 엔진 자동 계속과 WS 종료 이후 동작은 0.155.1 탐침으로 재확인하도록 했다. P1~P6가 독립 질문이었다. | 설계·검증을 전혀 고려하지 않았다는 H1/H4의 반증. `f9a70505314e1644e2b62695af163b7d2dd4f5b9:I/design/runtime-guard.md:116-176` |
| 첫 task 분할 | T14는 M1·T09/10·T13·T18 및 Q15 결정 이후 시작. pure state는 TDD, 연결/화면은 복원 후 시험, 강제 종료/재시작은 후보 관측. T26는 T25가 머지된 main을 받아 SQLite/PG·실사용5/10·성능을 보는 **코드 PR 없는 관측 레인**이었다. | 후속 T26의 대규모 수정은 최초 계획과 다른 실행이다. 실패를 해당 T로 반환한다는 계획도 있었다. `12790637edc689e351efda598f859310cfe1160d:I/tasks/T14.md:4-23`, `tasks/T26.md:1-8` |
| 첫 제품 준비 문맥 | `f0a52991534afbac386892714877f20aed565de0`는 service/runtime과 기존3시험에서 immutable binding·writer·provider·cause를 첫 hook await 전에 전달. durable command가 accepted인데 hook binding=None인1 FAIL→GREEN. 추가 recovery/cause 시험은 코드 후라 사전 RED로 부르지 않았다. | 첫 인도의 범위는 실행권이 아닌 문맥 전달. `R:I/tasks/T14.md:4058-4088,4110-4128`. 바로 다음 `bd3236f62f14aefd574cbe5668cb4c624767d2f7`는 **문서5파일 commit**이다. task4132가 이를 “코드판”이라 부르지만 Git diff는 문서 기록판임을 확인했다. |
| 집중86과 전체253 실패 | 독립 host86 PASS 뒤 Docker 전체6945 PASS/253 FAIL. 첫 draft deletion만 단독 선택하면 기준/현재 둘 다 PASS라 선행 상태가 중요했다. 전체 원출력544948 tokens가 잘렸고 전량 파일을 보존하지 못했음을 명시했다. | host 집중 통과→전체 실패는 실제 통합 사건. 253개를 같은 결함/환경으로 단정하지 않는다. `R:I/tasks/T14.md:4130-4149` |
| 실제 결함·fixture 결함 분리 | `aa911dcf460c21bee6bfed62091c06895002425c`는 live session 중 draft binding=None을 참조한 activity2줄과 영구39줄 시험을 수정. 이후 fixture tombstone가 patch purge를 생략해 close/fence가 막히는 별개 문제는 실제 same-session purge로 보정했다. | 제품 RED1과 fixture의 후속20개 선행 실패를 구분. 수정 후 원86 PASS가 전체 무결함은 아니다. `R:I/tasks/T14.md:4151-4181,2985-3040`; 위 commit code/test diff 확인. |

## T14 권한·취소·전달·정리 사건 사슬

| 사건 | 실제 수정 또는 시험 경계 | 결과·제한과 근거 |
|---|---|---|
| authenticated bridge 첫 인도 | `0e0c7d90340c199e0caf27e08554a24a385f1f84`: gateway138줄·barrier시험288줄 변경. 준비를 별도 bounded worker로 돌려 같은 소켓 Stop을 읽고, worker 실행 전 barrier와 deadline을 예약. | method_not_allowed RED1, 지연 worker가8 RPC를 쓰던 RED1→0 I/O. 실제 인증 WS지만 upstream은 fixture. `R:I/tasks/T14.md:2524-2567` |
| RID 조기 응답 충돌 | `02964880437ffb1cc42597d6160414ae7ce3c785`: 모든 early response 앞 duplicate-only 검사. capacity와 분리해 새 ID의 안전 동작은 유지. | 영구11 assertion FAIL→5시험 PASS. 첫 GREEN의 ConnectionReset cleanup ERROR3은 따로 보존. `R:I/tasks/T14.md:2451-2469`; R gateway802-819 |
| engine ACK≠downstream 전달 | `2cd3e1bbaac77cef59093d68862522f60f5e4fb8`: pending을 actual send 완료까지 유지, 중복 engine ACK 억제, early response도 bounded 전달 집합에 포함. | actual WS를 포함한8 assertion FAIL. 현재 시험은 held delivery 중 same-ID initialize 거절과 release 후 재사용을 단언. `R:I/tasks/T14.md:2380-2397`; `R:scripts/tests/verification/test_codex_gateway_thread_barrier.py:2110-2144`; `R:sandbox/codex_exclusive_gateway.py:1341-1369` |
| proof 송신 불확실성 | `8eb6412d67080e5eca5b747dd3f652e5994c95aa`: 실제 writer.write 직전 guard 통과를 표시하고 이후 drain 오류/timeout/cancel은 owner fence. 같은 ID fallback 오류를 다시 보내지 않음. | 실제 write 후3 RED→GREEN, loopback proof1건 뒤 EOF. guard 자체 거절(미송신 확인)은 별도. `R:I/tasks/T14.md:2278-2310`; R barrier2498-2511. 이 생산 diff28줄과 시험209줄을 대조했다. |
| scoped cancel·shared flight | 선행계약 `85e54494cc1c397eaac5a88ef56028dcd5523bbc` 뒤 `cc8c04b32c8426fdfbc2fa6889db7c8d6d0b92ca`: 원 RID type/value·thread·binding·requestKey 일치, 같은 flight proof만 폐기. identity tombstone는 owner drain까지4096에 포함. | 첫6 RED는 새 wire 부재여서 심층 경합6개 모두를 재현한 것은 아님. 첫5PASS/1FAIL은 다른 RID 응답 순서의 과도한 fixture 기대를 교정. `R:I/tasks/T14.md:2188-2225` |
| typed client | `0cb14c97c58e4b258429867437cc71f557abd17d`: factory→wait/cancel, 첫 send await 전 원 RID/소켓/receiver/lock 캡처.30초 원기한, usable ACK timeout/명시 취소만 최대1회5초 cleanup. | factory 부재·send entry 오류·bool RID·cleanup once 등 영구 RED를 구분. malformed proof는 자동 송신하지 않는 계약으로 시험을 생산 변경 전에 교정. `R:I/tasks/T14.md:1854-1893`; R client2142 이후 |
| close/reconnect 후 권한 오염 | 독립 public close/connect에서 old typed send가 gen1 fence를 복원해 다음 close가 successor receiver를 취소함. stale generic waiter도 gen2를 fence. `655f2e11bfe71de67cf3176463005e5cc2bd7ad1`은 captured tuple이 current일 때만 전역 오류를 바꿈. `d16b78badcb0e05cb7e12ecfed2773f074f366ff`는 이미 진입한 generic late error도 같은 guard로 좁힘. | 최초9FAIL/1PASS→중간9PASS/1FAIL→10PASS, 인접 entered-generic2FAIL도 후속수정. 기존480/648 통과는 이 경합의 증거가 아니었다. `R:I/tasks/T14.md:1500-1560,1604-1625`; R client1918,1965. 두 생산 diff26/12줄과 시험187/79줄 대조. |
| 진짜 auth 결합과 실행권한 제한 | 실제 CodexClient connect/initialize/sole receiver와 GatewayWebSocketServer를 연결한8시험 추가. wrong bearer401/upstream0, wrong provider 추가 repair 없음, peer socket close 뒤 proof 폐기·claim0을 검사. | author8 setup FAIL(bind EPERM), Git index.lock 거절로 미커밋 인계. root가 working/staged 차이와 hash 대조 후 실제 socket8 PASS 및 `f53ad0851b` commit. **조율자 agent의 복구이며 사람 직접 실행으로 확인되지 않음.** `R:I/tasks/T14.md:1627-1721`; R `B/adapters/codex/tests/test_codex_thread_preparation_bridge.py:504-539` |
| product binder·최종 권한 | `_prepare`는 feature OFF no-I/O, current binding/writer/provider를 확인하고 preparation에 commandId/action을 시작부터 결합. `ProductPreparation.revalidate`는 DB 검증 뒤 local identity를 다시 확인. | 뒤늦게 commandId를 붙이면 다른 명령의 proof를 소비할 수 있던 공백을 보완. typed ACK 자체가 DB authority는 아니다. `R:I/tasks/T14.md:1297-1347`; `R:D/goal_watch.py:302-407` |
| 소비 handler/config P2 | 좁은691/리뷰17 PASS 후 actual framing에서는 queued execution await가 같은 소켓 Stop 읽기를 막고 false proof가 flat/nested goals=true를 통과시켰다. bounded owner-local task와 공통 config guard로 보정. | 실제 native queued Stop ACK·zero writer RED. 이후 native14는 canned upstream이고 실제 엔진 자동 턴 증명은 아님. `R:I/tasks/T14.md:1139-1185`; R barrier1159-1251/native bridge173-326 |
| expiry와 task 은퇴 | pending0/worker0인데 control59 응답이 남은 시점에 expiry가 core를 삭제해 다음 공개 write0. control/pending/execution ownership과 response-settled를 함께 확인. | 준비된 core 수명과 task.done()를 동일시한 결함. public API 영구 RED 후 수정. author703PASS/32FAIL→root 동일 source735PASS; Docker1128PASS/2FAIL은 별도 fixture/취소 의미 재검토. `R:I/tasks/T14.md:1009-1073,4183-4216` |
| Python cancel 의미 차이 | 원 deadline와 external cancel이 같은 순간 도착할 때 Python3.9에서는 cancelledFalse/holder 미폐기,3.12에서는 cancelledTrue였다. public Task.cancel 계수로 자체 deadline만 timeout으로 바꿈. | writer0만으로 충분하지 않았다. externalCancelled·revoke·응답0·pendingworker0 회귀를 추가. private CPython state/global task factory는 쓰지 않음. `R:I/tasks/T14.md:356-402`; R barrier843 이후 |
| GoalWatch와 실제 제품 연결 | pure state934 PASS와 public91PASS/16FAIL을 분리. 실제 input RID 등록·sole receiver 순서·effect owner·clock·late receipt·Stop version을 연결. coalesced command=None이 watch owner를 덮거나 pause 실패가 running interrupt를 생략하는 결함을 보완. | 현재 pure state는5번째 계속 **완료**에 착지,12 completion에 detach, 확인 pause 실패는 retry 유지. `R:I/tasks/T14.md:203-252,773-817`; `R:D/goal_watch_state.py:547-642`. 실제 socket entry에서 Stop/terminal/writer 변경 시 activate0·holder revoked 시험은 `R:B/tests/test_codex_desktop_goal_product.py:430-498`. |
| mandatory cleanup 경합 | 첫 await 전 local revoke→active-use drain→captured client 확인 pause/cancel→transport→preparation retirement→epoch commit→owner fence/lock 해제. transport settled와 preparation retired를 분리. | 취소 호출 자체를 퇴역 확인으로 세지 않음. hook 부재·before-await revoke·cleanup cancel-ignore sender·pause interface의 RED와 setup cascade를 구분. `R:I/tasks/T14.md:872-922`; `R:D/goal_watch.py:496-541` |
| GoalControl 권한·receipt | 실제 send lock 안에서 user/chat admission·same session·binding/writer 재검증. goal edit은 objective만 변경, expected mismatch412. 원 RPC response receipt로 unknown과 미송신을 구분. | engine에 get→set CAS가 없다는 한계를 코드가 명시. malformed result8FAIL과 OpenAPI requestBody 누락1FAIL 수정, 최소 receipt/retained authority 후속은 별도. `R:I/tasks/T14.md:647-696,109-125`; `R:D/goal_control.py:181-244,271-307` |
| merge와 원 실패 인계 | unfinished HEAD17b09522e/MERGE_HEAD313257a의5충돌을 양쪽 이력 보존으로 해결. root merge `ea34be8498`; precommit canonical114PASS와 host104PASS/10FAIL은 다른 실행. | ours/theirs 일괄 선택 없이19파일 결합. provider1+attachment9 실패를 전부 환경 탓으로 지우지 않음. `R:I/tasks/T14.md:1421-1488`; `R:I/tasks/T26.md:676-690` |
| 실제 OFF가 OFF가 아니었음 | actual immutable OFF plain 입력에 get/create/update_goal3개 노출. engine0.155.1 기본값ON인데 false를 생략. 선행 method `1c90123916`→실제 service/client cold/new3FAIL→`f938d299665afe43cdd3399a99d7251a8e028afe` hook 보정→7PASS. |1143PASS/3PGSKIP는 인접 source시험. 새 실제 ON/OFF 광고 검증은 여전히 미완료. 늦은 실제 관측의 구체적 비용. `R:I/tasks/T14.md:3-63` |
| UI/lateACK fixture 보완 | goal entry synthetic component44, landing actual compiled11 PASS. lateACK 시험의0.2초가 stage 진입 전에 끝나던 문제는 원30초 안의 실제 socket entry에서만 단축. | 합성 화면을 actual D6/Aside로 부르지 않음. lateACK SQLite/PG76씩 통과도 실제 엔진 증명 아님. `R:I/tasks/T14.md:66-107` |

## T26: 관측 레인이 수정 레인으로 바뀐 과정

| 사건 | 관측·수정 | 판정·출처 |
|---|---|---|
| firstsend 하네스 자체 오판 | 합성18PASS인데 foreign turn도 completed5로 세고 자동 completion GET에 no-wake가 없었다. exact top-level turnId와 GET header를 고쳐21PASS. | 실제 candidate5/10 미실행. 테스트 하네스도 독립 오라클 검토 대상이었다. `R:I/tasks/T26.md:594-638` |
| paired 측정 실패 | before/after 각 fixture warm5/cold3 실행은 완료됐지만 after warm 수락 중앙값.282~.346s vs before.121~.141s, 완료약5초, API목표 미통과. 첫 slow warm6.6~9.4초를 버리지 않음. | 동일 fixture ID만으로 준비 상태 동등성이 성립하지 않았다. baseline project folder 누락400·transport0 및 hundred loaded rows100vs5를 정상 API/UI 준비로 보정했으나 재측정 미완료. `R:I/tasks/T26.md:199-221,535-592` |
| completion controller 수정·재리뷰 | native terminal 뒤 exact turn의 non-live engine item만 완료 근거로 사용. unknown 대기 중 중복 history, stale chat 응답이 현재 wait를 덮음, child/goal_resume가 parent wait를 소유하는 오류를 차례로 발견. |144→148→155 focused PASS를 최신 실제 성능 PASS로 확대하지 않음. `R:I/tasks/T26.md:342-416` |
| 정상 종료·Undo 실패 | 실제 wrapper recreate 후 sealed Undo 소실. Uvicorn HTTP drain이 lifespan보다 먼저인데 열린 SSE가 끝나지 않음. `1b8071ad2932993daf547126a9088d417cc61122`는 실제 기존 signal handler를 감싸 begin_shutdown을 앞당김. | h11/httptools SIGTERM2FAIL, lost wake/late attach2FAIL→7PASS. SIGKILL open epoch 거부는 유지. `R:I/tasks/T26.md:417-445,519-529`; `R:D/shutdown_signals.py:16-43`; `R:B/tests/test_codex_desktop_server_shutdown.py:90-149,206-219` |
| 종료 수정의 역회귀 | eager drain이 ready/accepted completion을 거부. 이후 shared retain_session gate가 이미 수락한 fork unknown 정산 hook을 건너뜀. `f8337d4aa84d0cc4204aacba2d8de61ddecd2349`는 shared guard를 제거하고 새 직접 control 입구에서만 closing을 검사. | fork RED OwnerUnavailable→같은 settlement GREEN,14파일425PASS. 실제 재시작 후 파일 bytes는 별도 미완료. `R:I/tasks/T26.md:447-517`; 해당 control/routes_terminals/runtime code-test diff 대조. |
| 합친 UI locale 회귀 | isolated570PASS 전후와 달리 전체720파일에서 toast2줄·ratchet54vs53 발생. `767b2793e2`는 공통 결과 handler로 좁히고 기존 gate를 변경하지 않음. | full10684PASS/2FAIL→후속10686PASS/1SKIP. 분리 리뷰는 결합 리뷰를 대체하지 않음. `R:I/tasks/T26.md:207-248` |
| 최종 backend2실패 | clean ec890706dc 전체8599PASS/2FAIL/14SKIP/1XFAIL. 하나는 signal 전20초 bootstrap 준비, 하나는 accepted 직후 async patch source 등록을 즉시 읽음. 두 nodeid만 다시 돌리면 이미2PASS여서 시점 제어가 필요했다. | `612456beb2`는 제품 변화 없이 fixture-ready60초와 actual server-ready20초 분리, accepted 뒤 원2초 terminal barrier.6파일148PASS. 원 full 실패의 정확한 cold import 시간은 미입증. `R:I/tasks/T26.md:25-93`; 현재 server 시험112-149 대조. |
| 시험 census와 최종 상태 | actual component test가 unit 제외+browser 명시 목록 누락. `6a58679a85` 등록 후 census PASS지만 실제 browser/build/CI PASS는 아님. | 현재 plan은 full·build·Goal/rich20 E2E·Undo/restart bytes·paired·5/10·release/CI/main/배포를 남김. `R:I/tasks/T26.md:3-23`; `R:I/plan.md:3-9`; PR435 본문/API. |

## 여섯 축·네 가설·귀속

| 축 | 판단 |
|---|---|
| 의도 보존 | legacy 복원·기능 공개OFF·기존 AC를 유지하려고 구체적인 권한/종료 계약을 추가했다. 일반 Goal OFF 노출과 정상 Undo 소실은 그 의도에 대한 실제 실패다. |
| 설계 충실성 | 초기 SP09·T14 의존·mixed strategy는 있었다. 이후 RID/ACK 전달·one-shot·captured lifetime·retirement의 연결 계약은 실제 결함을 보고 확장했다. H1은 **부분 지지**이며 모든 수정이 요구변경은 아니다. |
| 계획 실행 가능성 | 코드 없는 T26가 성능 controller·signal·fixture·census 수정까지 맡게 됐다. 실제 환경/계측 준비를 마지막 관측으로 미룬 부담은 H4 지지. 초기 검증방법 부재라는 주장은 반증된다. |
| PR/병렬 분할 | client/gateway/pure state/product/정리 lane의 집중 통과 뒤 실제 조합에서 새 결함. H3을 구체적으로 지지한다. 먼저 authenticated prepare→claim→write→ACK→Stop→retire의 작은 실제 경로를 인도하는 개선 실험이 타당하다. 모든 내부 구현 전에 모든 문서를 완성하라는 처방까지 입증하지 않는다. |
| 변경 피드백 | 방법 선행→행동 RED→수정→바로 다음 영향문서가 여러 commit에 남고, 처음부터GREEN·setup 오류·잘못된 fixture·실제 실패를 구별한다. auth/Git 권한 실패는 root 조율자에게 넘겨 동일 source로 복구했다. 이는 좋은 반례다. |
| 검증/보고 정확성 | 원 실패/과거 source/현재 source를 분리하고 fake upstream·synthetic DOM·host·Docker·PG·실엔진을 구분한 기록은 좋다. 거대 원출력 미보존, commit을 코드판으로 부른 한 곳, PR 본문 대상SHA와 현재 head 차이는 추가 한계. H2의 “HTML mock만”은 지지되지 않으나 실제 통합 UX 관측 부족은 남는다. |

제품/프로젝트 구현 원인은 captured lifetime·응답 전달·feature 기본값·서버 종료 순서에 구체적으로 연결된다. 도구/환경 원인은 bind EPERM·Git lock·Python 취소 의미·Docker bootstrap에 따로 연결된다. 이 구분 없이 모두 템플릿 결함으로 귀속할 수 없다. 현재 배포0.1.8/WIP5 문장별 gap은 부모의 기준판 대조 결과와 결합해야 하며 여기서는 새 필수규칙을 확정하지 않는다.

## 검토 범위와 아직 부족한 것

| 범위 | 조사 상태 | 이유 |
|---|---|---|
| 초기 T14/T26·SP09, 첫 binder, auth/typed client/RID/전달/cancel/retirement, 실제 OFF/종료/최종 실패 | reviewed / 실행 evidence-limited | 사건 원문과 핵심 생산·시험 diff/현재 단언 확인. 원로그 대부분은 문서의 hash/결과 기록으로만 확인. |
| pure GoalWatch의 모든 상태표 조합·GoalControl retained authority32의 모든 도달 경로·DTO schema portability 전수 | not-reviewed | 주요 의도·통합 실패와 대표 코드만 읽었다. 수백 개 테스트의 전수 의미 분석이나 모든 세부 commit은 하지 않았다. |
| PG migration/order 전량, 실제 ON D6·Goal 편집 경합·rich20·restart bytes·재paired·동시5/10·배포 | 제품 미완료 또는 evidence-limited | 최신 plan/PR가 미완료라고 명시. 사건의 미완료 상태는 읽었으므로 이 항목을 단순 조사 누락으로 처리하지 않는다. 후속 실행 성공을 추정하지 않음. |
| 원 사용자 판단·실제 모델 교체 | evidence-limited | 초기 계획은 T14 opus/T26 sonnet. 실제 첫 product context/review는 Sol6.1 Ultra, 후기 High/Medium 표기가 있지만 모델명을 전부 특정할 수 없다. 계획 모델과 실제 모델을 혼동하지 않음. Mac host3.9/3.12와 Docker3.11 차이는 확인, Windows 실행은 확인하지 못함. |

원대화가 꼭 필요하면 root가 찾은 Mac 세션 `01a0e862-9c36-79a1-ae48-2460649a0474`에서 **9/30 첫 product context 위임,10/1 auth socket/Git 권한 인계·미완료 merge 복구,10/2 final-off1의 Goal/Undo 실패와 release 보류** 구간의 metadata를 먼저 좁혀야 한다. 453MB 원문 전체는 읽지 않았다. 이 보고서의 “root 복구”는 기록상 조율자 실행이고 사람의 손수 복구로 판정하지 않는다.
