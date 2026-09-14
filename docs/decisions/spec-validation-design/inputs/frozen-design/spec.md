# Spec: 할당 컨테이너를 사용하는 Codex 호환 실행 단위
Upstream: [intent.md](intent.md)@sha256:7cb4be6f4f45bd3ae2c7ed259157d8e2beb3799d497a1c27d4b829f8d0a42356. Status: draft.
Skills applied: 프로젝트의 `design-spec`, `spec-policy-pass`, `sdlc-feedback`; 실제 경로·확인 판·적용 범위는 [설계 입력 기록](references/design-inputs.md#적용한-작성-지침).

Jake의 최신 요청에 따라 **최종 설계 완성**을 목표로 골격부터 점진적으로 구체화했다.
ISO/IEC 25010 기준의 성능 효율성·유지보수성·신뢰성을 주요 판단 축으로 삼는다.
S1–S5의 논리 책임·메시지/소유권·물리 배치·실행 의미에 이어 [S6 runtime](design/runtime-lifecycle.md),
[S7 인증/데이터](design/authority-and-data.md), [S8 전송/자원](design/protocol-and-resources.md),
[S9 통합/검증 경계](design/integration-and-verification.md)를 정했다. 중요한 결정마다 세 대안을 비교하고
하나를 선택했으며 비용과 번복 조건을 남겼다. 선택안은 **VM의 보호된 B/control store, 고정 M,
rootless Podman의 한 할당 컨테이너 안의 보호 X와 work UID 실행**이다.
Jake는 “이대로 계속 해. 내승인 요청하지 말고 자율진행으로 시작.”이라고 후속 설계 진행을 허용했다.
합의 범위의 설계 결정을 재승인 대기로 멈추지 않으며 특정 SHA의 사람 수락이나 제품 실행 재개와 구별한다.
최신 요청·정책 개정은 [개정 기록](references/review-policy-amendment.md), 실제 진행·검토·확인한 한계는
[execution](execution.md)에 둔다. 과거 추가 모델 리뷰의 실패가 현행 진행 조건으로 남지 않으며 성공으로 바꾸지도 않는다.

현재 VM의 로컬 파일·프로세스를 사용하는 화면을 할당된 컨테이너의 작업 환경으로 연결한다.
설계는 요구·원본 계약에서 출발한다. 기존 코드 보존율이나 전면 재작성을 성공 기준으로 두지 않는다.
초기 VM gateway 후보는 강한 컨테이너 내부 권한 분리안과 비교했다. S4에서 제어 기록의 수명·노출 경로와
원격 전송 비용을 대조해 P1을 선택했으며, 기존 초기 자료 자체를 채택 근거로 삼지 않았다.

이 문서는 최종 설계 검토용 draft다. 기술 선택/계약과 실제 실행 적합성은 구분한다.
현재 runtime은 미설치이며 S6 F6.1–F6.4를 통과하기 전 dependent 제품 wiring을 시작할 수 있다고
인계하지 않는다. 그 준비 판별은 선택한 계약과 실패 시 재설계 범위가 정해져 있다. 현재 컨테이너 동작이나
회귀 PASS를 주장하지 않는다. 계획 양식에 설계를 옮겨 미결을 감추지 않는다.

## Requirements

| ID | 바뀔 동작 또는 유지할 계약 | 근거 |
|---|---|---|
| R1 | 기존 Codex Desktop renderer로 명시적으로 할당한 컨테이너 하나의 실제 Codex를 사용한다. | intent Proposed outcome, 사용자 단일 컨테이너 결정 |
| R2 | 대화·Files·Review·Git·worktree·PTY가 같은 컨테이너 작업 공간을 대상으로 하며 VM 업무 경로로 대체 실행하지 않는다. | intent Problem/Proposed outcome |
| R3 | 원본 bridge/host capability와 준비 renderer의 계약을 유지한다. 컨테이너 연결 실패를 빈 성공·mock 응답으로 숨기지 않는다. | [APP_HOST_CONTRACT](../../docs/APP_HOST_CONTRACT.md#bootstrap-and-capn-web), intent Constraints |
| R4 | 사용자·할당 대상·실행 세대·브라우저 연결·제어권을 구분한다. 브라우저가 보낸 경로나 ID 자체로 대상 선택 권한을 부여하지 않는다. | intent 소유권·접근 제한 |
| R5 | 사용자 코드·Git·PTY가 gateway/M/X의 제어 상태·접근 인증·renderer와 VM/컨테이너 관리 권한에 접근하지 못하게 한다. Codex 개인 인증은 자기 work UID가 소비하며 같은 UID shell에서 은닉한다고 약속하지 않는다. | intent VM/컨테이너 경계, S6 권한 분리·S7 D7.4, [TERMINAL](../../docs/TERMINAL.md)의 cwd 검증 한계 |
| R6 | 브라우저 단절과 실행 프로세스 종료를 구분한다. 유효한 승인·실행은 기존 수명대로 보존하고 중복 승인·불명 요청의 재전송을 막는다. | [실행 수명 계약](../../docs/diagnosis/execution-lifecycle-contract.md), intent 실패·복구 |
| R7 | 컨테이너·엔진·gateway 재시작에서 영속 상태와 실행 중 상태를 구분하고, 이전 실행의 종료를 확인하기 전 새 실행권을 부여하지 않는다. | intent 수명·복구, 기존 EngineSession의 실제 종료 경계 |
| R8 | 설정·history·작업 데이터·첨부·기존 자동화 상태의 소유자와 저장 위치를 정하며, 기존 업무 데이터는 보존한다. | intent 상태 보존, [자동화 설정 계약](../../docs/diagnosis/automation-settings-contract.md) |
| R9 | 컨테이너 연결의 응답성·처리 능력·자원 사용을 지정한 사용 조건에서 평가할 수 있게 하고 기존 전송·파일·프로세스·메모리 한도와 종료 책임을 유지한다. 자원/측정 실패를 목표 미달로 낮추지 않는다. | intent 성능 효율성, [프로젝트 정책](../../PROJECT-POLICY.md#검증과-운영), [protocol-policy](../../src/shared/protocol-policy.mjs) |
| R10 | 동일 후보의 준비·기동·종료·복구를 재현하고 원본 화면의 결과와 실제 컨테이너의 결과를 대조할 수 있다. | intent 완료의 의미 |
| R11 | 책임과 의존성을 파악하고 원본 frontend 또는 실행 환경의 변화에 필요한 부분을 수정·검증할 수 있게 한다. 구현 기술 변경이 핵심 정책으로 확산되지 않도록 계약 경계를 둔다. | intent 유지보수성 |

세 품질의 현재 연결은 성능 효율성 R9, 유지보수성 R11, 신뢰성 R6–R8이다. 구체 품질 시나리오와
판정 기준은 [S9 §5](design/integration-and-verification.md#5-세-품질의-관측과-판정)에 연결한다. S1의 [검토 질문](design/foundation.md#5-세-품질-목표로-골격을-검토한다)을
[공통 작업·장애·변경 시나리오](design/skeleton-alternatives.md#3-같은-시나리오로-비교)에 적용했다. 실행 결과나 수치 기준은 아니다.

## Acceptance criteria

아래는 기대 결과다. 실행 결과가 아니며 세부 입력 fixture와 시험 ID·순서는 후속 plan에서 연결한다.
관측 가능한 계약을 먼저 고정하고 구현 출력에서 기대값을 역산하지 않는다.
AC6/AC7 중 기존 idle thread의 `turn/start` 한 건은 [S2의 M1–M7](design/message-submission-flow.md#4-손실-지점별-결과와-금지할-추론)로
구체화했다. 해당 사례는 브라우저 손실·native 상관의 경계를 다루며 승인·재시작 전체 AC의 완료를 뜻하지 않는다.
AC8/AC11/AC12의 보존·재시작 조건은 [S3](design/owner-recovery-boundary.md)의 H1–H5와 복구 허용 조건에 연결한다.
S4의 배치와 S5의 fence 경쟁·중복/회수·네 장애는 AC6–AC8/AC10의 입력이다. S6–S8이 실제 집행 수단의
설계를, S9가 기능·품질별 조건을 정한다. 아래 AC는 전부 구현 후 실행할 기대이며 현재 PASS 수는 0이다.

| ID → 요구 | 조건·입력·행동 | 관찰할 기대 결과·불변식 |
|---|---|---|
| AC1 → R1,R3,R10 | 고정 renderer/build와 할당 설정으로 첫 화면을 열고 실제 Luna/low 작업을 시작한다. | 두 기존 WS가 같은 build/할당 실행 단위에 연결되고 실제 컨테이너 엔진의 응답이 스트리밍된다. 엔진 부재 시 readiness 실패이며 가짜 대화는 없다. |
| AC2 → R2,R5 | 새 전용 작업 공간에 고유 표식을 만들고 Files·Review·Git·PTY에서 읽고 변경한다. VM에는 별도 검증 표식을 둔다. | UI의 파일·hash·diff와 컨테이너 결과가 일치한다. VM의 검증 표식·기존 업무 경로는 변경되지 않는다. 초기 cwd 확인만으로 이 결과를 대체하지 않는다. |
| AC3 → R2,R3 | 같은 파일을 순차로 두 번 변경하고 작업·worktree를 재열기한다. | 각 변경의 UI generation·hash·Git diff가 대응한다. worktree와 Codex cwd는 같은 컨테이너 경로다. |
| AC4 → R4,R5 | 할당 대상·경로·host ID·generation을 바꾸거나 잘못된 인증으로 HTTP/각 WS/다운로드를 요청한다. | 할당 변경이나 VM 작업 실행 없이 거절한다. engine가 제시한 경로도 VM 파일 접근 권한이 되지 않는다. |
| AC5 → R5 | 컨테이너의 shell에서 호스트 업무 경로·제어 상태·관리 소켓·gateway 인증 정보에 접근을 시도한다. | 경로·마운트·권한·네트워크 정책에 따라 접근이 차단된다. 허용된 자기 작업 파일은 사용할 수 있다. 결과는 단일 호스트/컨테이너 경계 증거로 한정한다. |
| AC6 → R6 | 스트리밍·승인 대기 중 브라우저의 각 WS를 따로 끊고 새 문서로 복구한다. | 실제 살아 있는 실행/승인만 다시 관찰한다. 살아 있는 다른 탭의 제어권을 자동 선점하지 않는다. 메시지·승인 자동 재전송은 없다. PTY는 기존 연결 종료 정책을 따른다. |
| AC7 → R6,R7 | gateway↔adapter 전달 전·후에 응답을 유실시키고 승인 응답을 중복 제출한다. | authoritative 미전송과 결과 불명을 구분한다. socket close/전송 ACK를 프로세스 종료·승인 완료로 처리하지 않는다. engine 전달 중복은 없다. |
| AC8 → R7,R8 | engine·컨테이너·gateway를 각각 재시작하고 이전 generation의 응답·승인을 재현한다. | 이전 실행권은 현재 세대에 적용되지 않는다. workspace/history/확정 설정은 보존되고 불명 작업은 자동 재실행되지 않는다. 종료 미확인 상태는 격리되어 readiness/새 mutation을 막는다. |
| AC9 → R8 | 지원 중인 첨부를 제출하고 작업을 재열며, 기존 자동화 설정·불명 실행 원장을 재시작한다. | 엔진이 읽는 첨부 bytes가 일치한다. 확정된 자동화 설정을 임의 초기화하지 않고 현재 정책을 재검증한다. 불명 회차는 재전송하지 않는다. 기능 전체 출시 완료를 이 AC로 주장하지 않는다. |
| AC10 → R9 | 파일 크기·large-I/O·PTY·전송 한계와 취소·자연 종료·adapter 장애를 재현한다. | 기존 유효 한계의 초과를 거절하고 제어 자원을 보존한다. VM와 컨테이너 양쪽의 실제 메모리·자식 프로세스·FD 정리가 확인된다. VM의 다른 업무는 보존한다. |
| AC11 → R4,R8 | 같은 할당 환경에서 reload/build 변경 후 초안·history/settings를 복원한다. | 안정된 데이터 identity를 사용하며 runtime generation 때문에 데이터를 버리지 않는다. 다른 할당의 저장소와 혼합하지 않는다. 불명 초안은 자동 제출하지 않는다. |
| AC12 → R8,R10 | 준비·기동·종료를 반복하고 실패 복귀 절차를 실행한다. | source/build/image/config/데이터 identity를 대조할 수 있다. code/build 복귀가 사용자 데이터 snapshot 복원으로 변질되지 않는다. 과거 후보 PASS를 현재 결과로 승계하지 않는다. |
| AC13 → R11 | 원본 host method의 인자/응답 한 개 변경 및 mTLS endpoint/runtime 교체 시나리오를 검토한다. | S9 §1/§5의 영향 범위에 대응하며 불필요한 Podman/DB 업무 판단 또는 원본 renderer/approval·queue 의미 변경을 요구하지 않는다. 실제 공통 권한·수명 계약이 바뀌면 그 영향을 숨기지 않는다. |

## Design

### Approach

기존 `createGateway()`는 로컬 엔진·경로·업무 상태를 한 process에서 조립한다. 그 코드를 그대로
컨테이너에 넣으면 빠르게 시작할 수 있지만, 같은 사용자 권한의 PTY가 gateway 상태와 코드에
접근할 수 있다. 반대로 engine endpoint만 원격화하면 Files/Git/PTY는 VM에 남는다.

현재 결정 범위는 원본 호환, 작업 조정·정책, 할당 환경의 실행·작업, 제어 상태 보존의 논리 책임이다.
세 대안을 비교해 B의 할당 실행 단위 수명 소유자 안에서 최종 제어 판단과 실행 수명을 연결하는 안을
선택했다. 내부 기능의 수명과 실행·저장 계약은 분리한다. S4의 P1에서는 B와 제어 기록을
VM에, 보호된 native/process 실행 책임과 모든 작업 I/O를 컨테이너에 둔다. P2와 추가 P3의 강한 형태를
비교했으며 권한을 합친 P0 진단 기준선을 세 유효 대안의 하나로 세지 않았다.
기존 코드의 재사용은 이 책임·계약에 맞는지 확인한 뒤 판단한다.

### Behavior and contracts

S1은 [foundation](design/foundation.md)의 책임·사실 소유자·의존 방향과
[대안 비교](design/skeleton-alternatives.md)의 선택 근거·반증 조건을 함께 읽는다.
S2는 [메시지 제출 흐름](design/message-submission-flow.md)의 수락 근거·손실 지점·재관찰 의미와 A 대조를 읽는다.
S3는 [소유자 재시작 경계](design/owner-recovery-boundary.md)의 identity·보존 사실·crash 구간·차단 범위를 읽는다.
기록 조회와 현재 실행권을 분리하며 근거 없는 재실행·새 세대 기동을 허용하지 않는다.
S4는 [물리 배치 비교](design/deployment-alternatives.md)의 P1/P2 tradeoff·실행 사실 제공 책임·번복 조건을 읽는다.
S5는 [실행 연결 계약](design/execution-channel-contract.md)의 binding·최종 effect 가드·단발 소비·조회와
네 장애의 복구 범위를 읽는다. 같은 B/X의 transport 복구와 새 process의 제어권 인계를 구분한다.
현재는 process 상실 후 live engine 제어 인계를 지원안으로 채택하지 않고 R7의 종료 후 새 세대를 따른다.
S6은 rootless Podman·외부 M의 고정 grant/기동/종료, s6 once/init, 명시적 컨테이너 전체 cold recovery를 정한다.
S7은 HTTPS 세션·mTLS/continuity·VM SQLite 단일 writer·불변 TOML/첨부·stable data namespace를 정한다.
S8은 두 내부 TLS·raw framing·단발 effect·사건 replay·credit 합계와 유한 work port를 정한다.
S9의 정상 흐름/장애표/품질·준비 판별이 위 계약을 연결한다. 모든 단계의 문서를 아래 범위로 함께 읽는다.

| 문서 | 현재 역할·필수 읽기 범위 |
|---|---|
| [design/foundation.md](design/foundation.md) | 현재 S1 구조 정본. 논리 책임·상태 소유·의존 방향·품질 검토 질문 |
| [design/skeleton-alternatives.md](design/skeleton-alternatives.md) | S1 논리 대안·공통 시나리오·추천 이유·선택을 바꿀 조건의 정본 |
| [design/message-submission-flow.md](design/message-submission-flow.md) | S2 기존 thread 한 건의 전달·수락·재관찰 의미, 손실 반례와 A 대조의 정본 |
| [design/owner-recovery-boundary.md](design/owner-recovery-boundary.md) | S3 보존할 사실·새 소유자의 허용 조건·차단 범위·두 복구 경로의 요구 근거 정본 |
| [design/deployment-alternatives.md](design/deployment-alternatives.md) | S4 물리 대안·P1 선택·실행 근거의 보호·번복 조건 정본 |
| [design/execution-channel-contract.md](design/execution-channel-contract.md) | S5 B↔X binding·단발 전달·결과 조회·소유권 상실 시 지원 복구 범위 정본 |
| [design/runtime-lifecycle.md](design/runtime-lifecycle.md) | S6 runtime/M/grant/init/실제 종료·F6.1–F6.4 정본 |
| [design/authority-and-data.md](design/authority-and-data.md) | S7 browser/service 인증·writer/transaction·TOML/첨부·보관/이행 정본 |
| [design/protocol-and-resources.md](design/protocol-and-resources.md) | S8 frame/pair/lane/sequence·receipt/credit·work port·method별 결과 정본 |
| [design/integration-and-verification.md](design/integration-and-verification.md) | S9 통합 책임·대표 정상/장애 흐름·기능/품질·설계와 실행 완료 경계 정본 |
| [design/compatibility-coverage.md](design/compatibility-coverage.md) | 기존 source family의 VM/container 이동·원본 browser 저장소 대조와 보존 정본 |
| [design/architecture.md](design/architecture.md) | 초기 배치·상태 후보와 DQ 목록. 현재 배치 결정은 S4를 따르며 이 자료의 세부 제안은 자동 채택하지 않음 |
| [design/current-code-assessment.md](design/current-code-assessment.md) | 기존 계약·코드·검증 자산 대조 입력. 물리 배치를 선결정하지 않음 |

기존 계약은 위 R에서 연결한 문서의 명시된 부분을 보존 대상으로 삼는다. [기존 설계 입력 기록](references/design-inputs.md)과
[당시 입력 해시](references/design-source-inputs.json), [첫 S1 기록](references/s1-quality-record.md)은 이전 관측 판이다.
대안 선택 당시의 입력·리뷰는 [S1 대안 기록](references/s1-alternatives-record.md), 메시지 흐름은
[S2 기록](references/s2-message-flow-record.md), 보존·재시작은 [S3 기록](references/s3-owner-recovery-record.md), 배치 비교는
[S4 기록](references/s4-deployment-record.md), 실행 연결은 [S5 기록](references/s5-execution-channel-record.md)에 둔다. 과거 비교·리뷰는
현재 수정판에 대한 검토나 실행 증거가 아니다. 과거 단계의 “아직 미정/다음 단계”는 당시 단계 범위이며,
구체 결정은 현재 정본 S6–S9를 따른다. 내부 runtime protocol은 원본 제품 wire/API와 별도다.

S7의 control DB·불변 TOML object는 기존 JSON ledger/가변 TOML 물리 구현을 명시적으로 대체한다.
원본 UI/API·definition 의미·cron mode/permissions·heartbeat settings·unknown 비재전송은 유지한다.
002의 제품 작업을 재개하거나 그 전체 출시 기준을 003 완료 조건으로 끌어오지 않는다.

## Constraints and scope

- 세 품질을 주요 판단 축으로 삼고 개발 시간·자원 절약을 설계 타협 이유로 쓰지 않는다. 단계마다
  작은 논점만 구체화하며 제품 자원 한도·기능/권한/데이터 조건은 유지한다.
- intent의 단일 사용자·단일 컨테이너, 기존 원본 frontend/engine, 기존 VM·운영/WIP 보존 범위를 따른다.
- gateway·adapter의 정확한 배치 구현과 재사용은 설계 판단이다. 기존 코드 구조 유지·전면 재작성을 선결정하지 않는다.
- 자동 할당·계정 관리·오케스트레이션·다중 사용자 플랫폼·두 사용자 동시 검증·전체 기능 출시를 추가하지 않는다.
- 다른 개발건의 요구나 종료 조건을 가져오지 않는다. 이 설계에서 직접 바꾸는 계약과 영향받는 회귀를 검증한다.
- Git·Node·시험은 Ubuntu `codex-re-poc` / Node `22.23.2`, 무거운 검증은 직렬이다. 현재 제품 명령은 미실행이다.
- Git20 advisory와 기존 assessment/browser 정책 ID를 유지한다. 새 실행 topology의 성능 비교 가능성은 별도로 확인한다.
- TDD는 선택형이다. 구현/검증 순서는 plan에서 정하며 이 spec에 미래 RED/PASS 기록을 만들지 않는다.

## Open questions

intent에 Q ID가 없으므로 현재 다섯 질문을 순서대로 Q1–Q5로 대응한다.

| ID | answered / carried forward | 답과 근거 또는 미정의 영향·해결 주체·필요 시점 |
|---|---|---|
| Q1 gateway 배치·연결 | answered | S4 P1, S6 grant/외부 M, S7 mTLS+browser session, S8 내부 두 TLS/framing/유한 port를 선택했다. 고정 요구와 세 대안·비용·번복 조건을 각 정본에 기록했다. |
| Q2 runtime·이미지·볼륨·인증·자원 | answered (설계), 실행 판별 별도 | S6 rootless Podman/s6, S7 immutable image+volumes/SQLite/TOML/private Codex auth, S8 credit 합계를 정했다. FC1의 준비 적합성은 미실행이며 F6.1–F6.4 전에 dependent product wiring으로 인계하지 않는다. 실제 image digest/credential revision/resource profile 값은 operator 준비 입력이다. |
| Q3 흐름·실패·보존 | answered | S5 D5.1의 명시적 cold recovery, S6 actual scope·pending start 배제, S7 durable 소비/상태, S8 ACK와 effect 분리, S9 정상·장애·기능표로 구체화했다. |
| Q4 통합·운영 | carried forward | 이번은 설계다. 현재 운영 교체·remote/PR 통합 결정은 Jake가 해당 단계 전에 정한다. 설계 초안 작성은 막지 않는다. |
| Q5 세 품질의 평가·상충 | answered | S8 합계/credit, S9 원래 dataset/측정 위치/부하·지연/메모리·변경 영향 시나리오를 정했다. Git20만 advisory이며 비교불가/오류/다른 한계는 완화하지 않는다. 미측정 배치의 성능 우위를 주장하지 않는다. |

## Flagged concerns

| ID | 근거·영향 | 결정·확인 주체와 필요한 시점 |
|---|---|---|
| FC1 컨테이너 실행 적합성 미확인 | 제한 user/PID namespace 생성은 exit0. 복수 UID/subuid·mount/network/cgroup·실제 runtime/protected X는 미검증이고 필요한 packages/user delegation이 미준비다. 선택이 실행 가능하다고 주장하지 않는다. | S6 F6.1–F6.4를 준비 담당 Codex/operator가 제품 wiring 전에 판별한다. 실패 시 해당 D6 결정을 다시 열며 운영 전역 설정/기존 서비스를 임의 변경하지 않는다. |
| FC2 실행 경계 설계와 검증 구별 | S6/S7의 M-signed grant·B key/continuity·pair fence·X native 상관·실제 scope 종료를 정했다. 별도 M/runtime/init/인증 준비·검증 비용과 cold recovery 가용성 손실을 수용한다. | 설계 검토에서 중대 지적을 종결한 뒤 동일 contract의 실제 정상·거절·장애 관측은 구현 후보에서 수행한다. |
| FC3 저장 이행·자원 집행 비용 | SQLite worker/process/락과 TOML revisions가 기존 파일 구현을 대체한다. schema/import/rollback·자원credit·object정리 검증이 필요하다. 개인 Codex 인증은 자기 shell로부터 숨기지 않는다. | S7/S8/S9의 이행·합계·privacy 경계를 구현 전에 확인한다. DB/이미지/볼륨이 있다는 이유로 원자성·격리를 PASS 처리하지 않는다. |
| FC4 증거 범위 | 소스 분석·문서 리뷰는 새 topology의 runtime/격리/브라우저 PASS가 아니다. 참조 계약의 historical PASS도 승계 불가다. | 설계 단계는 이 한계를 기록하고, 구현 후보에 실제 AC와 회귀를 수행한다. |

기존 정책의 sandbox 유예는 intent에 기록된 Jake의 단일 컨테이너 예외를 따른다. 정책 검토는
범위·권한·데이터 보존·원본 계약·품질·증거 구분을 다뤘으며 새로운 승인 체계나 제품 실행 권한을 만들지 않았다.
