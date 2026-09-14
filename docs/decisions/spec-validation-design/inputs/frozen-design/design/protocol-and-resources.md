# S8 — 내부 전송·자원과 원본 기능 접점

상태: 003 설계 결정. 원본 browser wire2/Cap'n Web을 유지하고 B↔X에만 별도 내부 protocol1을 둔다.
[S5](execution-channel-contract.md)의 단발 effect와 [S7](authority-and-data.md)의 데이터 권위를 구체화한다.
아래 수치는 새 성능 목표가 아니라 기존 한도 안의 전송/예약 설계다. 구현·부하 PASS는 미실행이다.

## 1. 대안과 선택

| 결정 | A | B | C | 선택·이유·비용·번복 조건 |
|---|---|---|---|---|
| D8.1 내부 framing | NDJSON + binary base64 | 고정 binary prefix + JSON header + raw fragment | Protobuf/gRPC typed streams | B. engine JSON을 보존하고 파일 재인코딩을 줄인다. parser/fragment validation을 소유하는 비용이 있다. C가 실제 CPU/상호운용 필요를 충족하면 schema 비용과 재비교한다. |
| D8.2 제어/일반 전송 | 한 TLS FIFO | 한 TLS의 우선순위 multiplex | 두 TLS: 제어 전용과 일반 multiplex | C. 같은 kernel send FIFO의 bulk가 승인/중단을 가로막는 경로를 분리한다. 연결·인증·원자적 binding 교체가 복잡해진다. 단일 연결이 기존 control deadline과 포화 시나리오를 증명하면 B를 재비교한다. |
| D8.3 번호 체계 | 연결 전체 번호 하나 | lane 전송번호 + effect dispatch번호 + engine event번호 | 요청 UUID map + 별도 이벤트 cursor | B. frame 조립·단발 effect·사건 공백을 구별한다. C는 UUID 보관/회수와 replay fence를 더 소유해야 한다. 완성된 framework가 같은 불변식을 단순화하면 재비교한다. |
| D8.4 사건 복구 | 단절 뒤 snapshot만 재조회 | same-live X/B의 bounded event/result replay | durable X journal + 재구독 | B. 현재 소유자가 보유한 사건을 잇고 별도 durable 실행 원장을 만들지 않는다. 보관 창 밖의 과거 사실은 복원하지 못한다. 무손실 live takeover가 요구되면 C와 S5/R7을 함께 재설계한다. |
| D8.5 전체 자원 집행 | B/X 고정 partition | 매 allocation마다 B의 동기 permit | B 전체 ledger + X의 사전 할당 credit | C. 합계를 지키면서 decode/복사의 순간 위치 변화와 B 부재 때의 bounded control을 지원한다. credit 회수/재관찰이 비용이다. 안전한 고정 partition의 충분성이 실측되면 A로 단순화한다. |
| D8.6 host capability 경계 | 원본 Cap'n Web을 X까지 연장 | B에서 종단하고 유한 port로 X 연결 | 공통 IDL로 B/X host adapter 생성 | B. 원본 capability/callback 수명을 VM 호환 책임에 남긴다. C는 다수 원본/실행 기술을 실제 지원할 때 codegen 유지 비용과 비교한다. 원본 UI를 재작성하는 안은 고정 요구 위반이므로 대안 수에 포함하지 않는다. |

## 2. 연결과 frame

두 mTLS 연결은 하나의 `{allocationId,dataId,B,X,engine,protocol,build,bindingFamily,bindingId}`에 속한다.
제어 C와 일반 D가 모두 인증·S6 grant/복구 증명 대조를 마친 뒤 X가 pair를 원자적으로 activate한다.
한쪽만 교체하거나 인증한 다른 pair와 섞지 않는다. 연결 하나를 잃으면 두 transport의 새 admission을
fence하고 둘을 정리한다. 같은 B/X만 새 pair로 복구할 수 있고 old binding의 queued effect도 최종 guard에서 막는다.
활성 pair 하나와 인증 중 후보 pair 하나만 허용하며 후보가 완성되지 않으면 기존 예산/10초 준비 기한 안에 정리한다.
M 관리 socket은 이 pair와 별도다. browser의 원래 두 WS도 별도 수명이며 내부 연결을 browser WS 수에 중복 집계하지 않는다.

frame prefix는 network byte order 16바이트다: magic `CDX8`(4), version u16=1, type u8, flags u8,
headerBytes u32, bodyBytes u32. header는 UTF-8 JSON, 최대64KiB, body fragment는 최대256KiB.
unknown version/type/flags/encoding·중복 key·비정상 길이·depth64/token100000 초과는 allocation 전에 거절한다.
application body는 기존32MiB, 파일은20MiB다. 더 큰 내부 envelope를 핑계로 원본 payload를
조용히 잘라내지 않는다. 원본 최대 payload를 싣기 위한 transport header는 logical-message overhead로
별도 예약하되 원본 payload32MiB 상한을 낮추지 않는다. 즉 application body32MiB와 transport header 상한은 구별한다.

header 공통 필드는 lane, bindingId, messageId, frameSeq, fragmentIndex/count, totalBodyBytes,
bodyEncoding(json/raw), operationId, dispatchSeq, methodCode, contentSha256다. generation identity는
handshake에 고정하고 메시지의 bindingId로 대조한다. 숫자는 safe integer 또는 canonical uint64 문자열로
고정하며 wrap/reuse를 허용하지 않는다. 동일 message/fragment 번호의 다른 bytes는 protocol failure다.
본문 길이·hash·마지막 fragment까지 검증하기 전 업무 effect에 진입하지 않는다. blob staging write는 별도
transfer operation의 효과이며 최종 engine 공개와 구별한다.

type 값은 HELLO=1, BIND=2, CALL=3, RESULT=4, EVENT=5, ACK=6, CREDIT=7, CANCEL=8,
CLOSE=9, FRAGMENT=10으로 고정한다. protocol1 flags는0만 허용한다. HELLO/BIND 전에는 CALL/자원 할당을
받지 않으며 실패한 pair의 나머지 연결도 닫는다. methodCode/operationId/dispatchSeq는 effect CALL에 필수,
original operationId/evidence kind는 RESULT에 필수, engine generation/eventSeq는 EVENT에 필수다.
FRAGMENT는 이미 예약된 message/transfer만 참조하고 새 method/lane을 지정할 수 없다. 선택 필드는 type별
schema에만 허용한다. unknown field를 권한 값으로 보존/전달하는 permissive passthrough는 없다.
각 ID는 server-issued opaque 값으로 길이를 제한하며 path/큰 JSON은 body에만 둔다. 인증 중 연결의 parser와
TLS 자원도 C0 reservation/실제 RSS에 계수하고 미인증 후보 수와 준비 기한을 제한한다.

분할은 무제한 조립을 허용하지 않는다. 먼저 전체 길이/예약을 검증하고 fragment를 정해진 순서로 처리한다.
raw file은 bounded streaming하며 JSON은 decode 예상 메모리까지 확보한 뒤 조립·parse한다. prototype key/
__proto__ 등을 일반 객체 권한 속성으로 섞지 않으며 exact schema의 plain data로만 사용한다.

## 3. lane·번호·deadline

C0는 제어 C socket: binding/fence, credit, ACK, 결과 조회, 승인 응답, interrupt/cancel, unwatch/close다.
대기 control record는 기존16개/64KiB application payload 합계, mandatory drain은5초다. C0 header는
최대4KiB로 별도 예약하며 method body를 header로 이동해 한도를 우회하지 않는다. 승인 **요청 본문**은 C1이고 최대4MiB,
전체 retained approval body16MiB를 유지한다. 승인 응답은 기존 stdin-writer가 실제 제한하는 encoded
control aggregate64KiB 안에 들어야 한다. 요청 body를 응답 control 한도로 잘라 거절하지 않는다.
응답 preflight/예약은 B 소비 전에 하되 이미 소비한 writer 실패는 unknown으로 남기고 pending으로 돌리지 않는다.

C1은 일반 D socket의 engine call/result/event, PTY, 작은 metadata다. C2는 같은 D의 bulk/file/diff다.
매 fragment 경계에서 C1/C2를 round-robin하며 대용량 source는 공유2개/40MiB/건20MiB 안이다.
각 lane 큐는 기존 browser WS 큐 상수에서 파생한 새 설계 상한256개/40MiB를 둔다. 이는 기존 WS 큐를
그대로 이식했다는 주장이 아니며 전체 resource reservation 위의 추가 상한이다. 큐마다40MiB를
별도 공짜 pool로 배정하지 않는다. control에는 일반 body를 담지 않고 큰 조회 결과는 예약된 C1 응답으로 받는다.
partial-message10초, send no-progress15초, 원래 request60초를 유지한다. 이 기한은 retry 허가가 아니다.
control 실패는 기존5초 전체 deadline과 owned shutdown 확인을 따르며 여러 hop마다 새5초를 더하지 않는다.

번호는 세 종류다. frameSeq는 physical binding/방향/lane의 연속 전송 번호이며 새 pair에서 초기화할 수 있다.
dispatchSeq는 binding family와 고정 C0/C1/C2 effect lane별 단조 상한선이고 transport 교체로 초기화하지 않는다.
eventSeq는 실제 engine generation의 X→B native response/request/event 순서다. admission 순서와 완료 순서는 다르다.
서로 다른 lane의 정상 reorder를 하나의 high-watermark로 버리지 않는다. 원래 업무 ID의 B 소비 기록도 별도로 검사한다.
methodCode→effect lane은 protocol1 manifest에 고정한다. 같은 method를 다른 lane으로 재분류해 상한선을
우회할 수 없다. 일반 workspace/engine/Git/worktree/PTY 생성·입력은 C1, approval/interrupt/close/cancel은
C0, blob chunk의 제한된 staging write는 C2다. blob begin/commit은 C1이다. bulk body fragment 자체는
원래 C1 operation의 payload일 수 있으나 독립적인 새 file/Git effect가 아니다. 그 operation/transfer에 결합된
완성/순서 조건 뒤에만 원래 effect가 진입한다. chunk가 commit보다 늦게 오면 검증 실패이며 조용히 새 파일로 쓰지 않는다.

**B→X mutation frame은 자동 재송신하지 않는다.** 손실 시 원래 operation/dispatch 번호를 조회한다.
X가 상세 결과를 반환하거나 명확한 미진입을 증명할 수 없으면 unknown/unavailable다. X의 duplicate guard는
결함·중복 입력의 effect를 막는 방어이며 자동 요청 retry를 허가하지 않는다. X→B 사건/결과 replay와
ACK/credit 조회 같은 읽기 제어는 원래 번호로 반복할 수 있지만 업무 effect를 발생시키지 않는다.

## 4. 사건·승인·receipt 수명

X는 native framer/correlation의 원래 순서로 eventSeq를 부여한다. B는 현재 registry에 사실을 정착하고
durable 사건은 DB commit을 확인한 뒤 ACK한다. optional browser callback/표시는 별도이며 늦거나 실패해도
원래 결과를 바꾸지 않는다. ACK 유실로 같은 event가 오면 B의 적용 cursor와 원래 identity로 재적용을 막는다.

live replay는 1024 logical events 또는 encoded40MiB 안이다. count는 기존 engine request tombstone 수,
bytes는 WS 큐 상수를 참고해 정한 **새 replay 설계 할당**이며 기존 이벤트 replay 지원 수치가 아니다.
서로 다른 별도 메모리 예산이 아니며 ACK 뒤 사본을 해제한다. 미ACK 사건은 TTL로 조용히
삭제하지 않고 포화 시 native ingress를 멈춰 현재 buffer/승인을 보존한다. 이후 통신 실패는 새 mutation을
fence하는 것이며 단절 자체로 engine/승인을 종료하지 않는다. 필요한 mandatory engine control의 drain 실패는
기존 owned failure 계약으로 별도 처리한다. X의 승인 본문은 실제 engine pending/resolved 수명으로 보존한다.

재연결에서 B의 마지막 applied/committed cursor와 X retained 범위를 대조한다. 연속 범위만 replay한다.
gap이나 native correlation 소실은 표시하고 관련 mutation을 fence한다. 현재 thread snapshot은 현재 화면 복원용이며
과거 수락/승인 응답 성공을 메우지 않는다. live registry로도 정합성을 입증할 수 없으면 S6의 명시적 cold recovery를
기다린다. 완료 engine request의 상관 tombstone은 기존1024개/5분 한도를 따른다. 이를 PTY tail이나
새 replay 사건의 보관 TTL로 해석하지 않는다. receipt payload는 consumer/ACK/참조가 끝난 뒤 회수하며
high-watermark와 미해결 approval/attempt를 삭제하는 수단이 아니다. PTY tail은 기존16,000바이트 계약을 유지한다.

## 5. 합계 자원과 credit

정본은 [protocol-policy](../../../src/shared/protocol-policy.mjs)다. B/X를 나눴다고 기존 한도를 두 번 허용하지 않는다.

| 자원 | 실행 단위 합계 | 배분/실효 집행 |
|---|---|---|
| data | 512MiB, small reserve16MiB 포함 | B local+DB process payload+X credit+동시 복사 합산 |
| assembly | 256MiB, 논리 connection당32MiB | B local+X credit 합계. browser8개/각32MiB의 기존 admission 공간을 고정192MiB로 축소하지 않음. 내부 조립도 같은 pool에서 동적 예약 |
| framer | 64MiB | X의 native record framing 전용. 내부 header/fragment는 해당 assembly/data에 청구 |
| control | 8MiB | B7MiB/X1MiB 고정, 일반 I/O가 빌리지 못함. M 관리 process 실제 RSS는 별도 관측하되 이 pool로 위장하지 않음 |
| codec | >1MiB 전체1 slot, factor6 예약 | B ledger의 사전 token. X도 token 없이 큰 JSON decode/encode 금지 |
| large I/O | 2개, source40MiB, 건20MiB, working96MiB/건 | B/X/브라우저 처리 전 구간 permit 유지. ACK만으로 반납하지 않음 |
| 기존 logical counts | RPC256, lease256, 승인64/작업8, PTY16/연결8, 구독256/연결64 | B가 전체 admission; X는 전달받은 exact permit과 실제 자원 수명 검사 |

840MiB는 네 protocol accounting pool의 합계다. Node/SQLite/TLS/runtime/engine/파일 cache 전체 RSS 한도라는 뜻은
아니다. 실제 VM+container RSS/FD/process/CPU와 M/helper 비용은 품질 시나리오에서 별도 측정한다.
kernel socket buffer·DB cache/WAL·thread stack 등을 측정에서 누락하지 않는다.

credit은 allocation/B/X/ledger generation, grantId, pool, bytes/count, outstanding 상태를 갖는다.
B가 credit을 기록하고 합계에서 차감한 뒤 X에 준다. 응답 유실로 새 credit을 중복 발급하지 않고 같은 grantId를 조회한다.
X는 local allocation 전 확보된 credit을 차감하고 실제 해제한 뒤 return receipt를 보낸다. B는 exact grant 반환을
한 번만 반영한다. release ACK 유실은 재조회하며 임의 timeout/lease TTL로 재분배하지 않는다. 양쪽이 동시에
사본을 가지면 둘 다 예약한다. 같은 frame이 재전송되었다고 memory가 두 번 무료로 생기지 않는다.

B/X transport 단절 때 X outstanding은 반납되지 않는다. 같은 X의 inventory reconcile 또는 M의 실제 해당
scope 종료 후에만 reclaim한다. B 자체가 상실되어 합계 ledger를 잃으면 S6 cold recovery 전 새 업무를 열지 않는다.
X는 B 부재 중 자기 pregranted reserve만 쓴다. 일반 credit 부족이 control ACK/cleanup 자체의 교착을 만들지 않도록
fixed control partition으로 credit/refund/stop을 처리한다. early native approval/event를 위한 data credit도 engine 시작 전에
확보하며 없으면 engine admission을 열지 않는다. data small reserve16MiB는 그 credit을 포함한 전체에서 유지한다.
전송자가 전체 assembly를 쥔 채 수신자의 assembly 확보를 기다리는 순환 대기는 금지한다. sender는
완성 body를 data/encode 예약으로 이전하고 사용이 끝난 assembly를 해제한 뒤 receiver credit을 기다린다.
전역 codec1slot/receiver data reservation도 같은 규칙으로 acquire 순서를 정한다. 확보 불가인 새 요청은
effect 전에 busy로 거절하며 정상부하 busy는 여전히 품질 실패다. 포화시험의 거절을 정상부하 PASS와 섞지 않는다.

## 6. 유한 port와 경로

Cap'n Web의 callback/export/capability는 B 호환 adapter에서만 소유한다. X로 capability 객체·임의 함수·
JS 소스·범용 host fetch를 보내지 않는다. 아래는 method family의 닫힌 역할이다. 정확한 opcode 목록은
기존 allowlist/host 소비자에 대응하는 build artifact이며 등록 없는 기능은 effect 전에 METHOD_UNSUPPORTED다.

| port | 역할/효과와 권한 |
|---|---|
| binding/flow | authenticate/recover/observe/fence, credit/ACK/result lookup/cancel. 새 할당·임의 exec 없음 |
| engine | 고정 initialize, allowlisted native call, 원래 native approval response, ordered record, owned shutdown. `thread/queue/*` mutation 금지 유지 |
| workspace/git/worktree | stat/list/read/watch, 허용 write/metadata/Git opcode/worktree lifecycle. root handle과 relative path를 work UID에서 검증 |
| pty | create/write/resize/close/attach/getCwd/snapshot 등 기존 계약. 실제 session/owner/generation 대조, reconnect 명령 재실행 없음 |
| blob | exact transfer begin/chunk/commit/read/delete와 영수증 조회. X 보호 object namespace에만 작용 |

VM B는 임의 container path를 로컬 fs/Git/PTY 함수에 넘기지 않는다. X control process도 사용자 path를
자기 UID로 realpath/open하거나 Git hook을 실행하지 않는다. 고정 work UID helper가 rootHandle+
relative path를 자기 namespace의 fd/symlink/root 검사로 해석하고 효과를 수행한다. parent dir swap/../absolute
VM path·symlink·Git option 주입을 거절한다. 권한 있는 root handle은 server가 발행하며 browser path가 권한이 아니다.
Git은 opcode별 argv를 고정 조립하고 일반 shell fallback이 없다. PTY의 사용자 shell은 허용된 작업 UID/scope에서만 실행한다.

## 7. method별 결과와 취소

effect 결과는 not-sent/rejected/accepted/unknown/unavailable와 별도 완료/정리 fact로 표현한다.
accepted를 모든 기능의 완료로 일반화하지 않는다. 원본 adapter는 기존 응답 형태에 정확한 의미만 투영한다.

| 기능 | 권위 있는 관찰 | 자동으로 추론하지 않을 것 |
|---|---|---|
| thread/start, turn/start/steer | 원래 native correlation의 valid thread/turn ID와 error | X ACK, history snapshot이 수락을 증명하지 않음 |
| approval answer | B 단일 소비 + X의 원래 writer 성공; resolved는 후속 engine 사건 | writer 실패 뒤 pending 부활/자동 재응답 없음 |
| file/Git/worktree mutation | work helper의 exact operation 결과·파일/hash/diff·partial/conflict | socket close가 rollback/미실행 증거가 아님 |
| PTY create/write/close | 소유 session 생성, 실제 input write, 실제 process/descendant 종료 각각 | close ACK가 모든 자원 반환 또는 명령 취소 증거가 아님 |
| attachment | S7 publication receipt + B ready/reference commit | upload socket 전달이 engine 읽기나 제출 성공이 아님 |

cancel은 원 작업과 다른 operation이다. effect 진입 전 권위 있게 취소되었을 때만 그 step을 not-sent로
분류한다. 이미 진입한 native/spawn/fs effect를 cancel 성공으로 미실행 처리하지 않는다. 재관찰 read는 현재
권한으로 새 요청할 수 있으나 과거 업무의 성공/미실행을 추측하지 않는다. 미지원 method를 빈 성공으로 감추지 않는다.
