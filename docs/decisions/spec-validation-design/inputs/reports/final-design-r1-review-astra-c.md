# 003 final-design-r1 독립 최종 설계 리뷰 C

- 최초 판정: **PASS — 고정된 문서 설계 범위**.
- 판정 의미: 검토한 고정 입력에서 최종 설계를 변경해야 하는 중대한 모순·미결정·원본 계약 위반을 확인하지 못했다. 제품 구현·환경 적합성·AC 실행·Q5·운영 전환 PASS는 아니다.
- 독립성: 이번 입력의 저술·설계 자문에 참여하지 않은 새 문맥에서 판정했다. 다른 검토자 보고·의견을 읽거나 결과를 요청하지 않았다. 고정 문서 자체의 과거 리뷰 언급은 과거 사실로만 취급했다.
- 모델 증거 수준: **spawn 도구 인자 gpt-6-astra/high; 별도 runtime telemetry 미제공**. root의 보충 메시지가 model/reasoning_effort/fork_turns=none 및 성공한 canonical task_name 확인을 전달했다. 이것을 독립적인 backend telemetry 검증으로 확대하지 않는다.
- 범위: R1–R11, AC1–AC13 및 manifest authoritativePaths의 15개 고정 사본 전체. 현재 제품 runtime 설치·실행·전환 중단과 Muse 필수 정책 제거를 적용했다.
- 사람 수락: draft 설계 검토다. 자율 진행 요청이나 모델 판정을 특정 SHA에 대한 Jake의 최종 수락으로 해석하지 않는다.

## 입력 무결성

`inputs.json`의 실제 SHA-256은 `d36ca8a1d3b2a098a58afb704ac10bfd69271c9004c1bbca3395436bfaac6e8b`로 지정값과 일치했다. manifest에 기재된 **210개 파일 모두** 실제 bytes와 SHA-256을 검증했고 불일치는 0개다. 이 검증을 내용 전체를 읽었다는 주장으로 사용하지 않는다.

아래 경로는 모두 `intent/0003-redesign-compatibility-gateway/references/final-design-r1/files/` 아래 고정 사본이다. 보고서의 설계 파일명과 줄 번호도 이 사본을 기준으로 한다.

| authoritative 고정 입력 | bytes | SHA-256 |
|---|---:|---|
| `intent/0003-redesign-compatibility-gateway/intent.md` | 14771 | `7cb4be6f4f45bd3ae2c7ed259157d8e2beb3799d497a1c27d4b829f8d0a42356` |
| `intent/0003-redesign-compatibility-gateway/spec.md` | 22939 | `b268aa5e46fd570fdc0222f49e6697894d29543d0fdfd3ea2675e9da7734e4b6` |
| `intent/0003-redesign-compatibility-gateway/design/architecture.md` | 16042 | `c1aceea7d14682b746d3419c3cb7e7c1f16c2e066e72423aabbda32e85f360ec` |
| `intent/0003-redesign-compatibility-gateway/design/authority-and-data.md` | 27880 | `14904a906d89d9e076b602fe68bed84de4e5f53ca69854ac74d67702cc5a0a61` |
| `intent/0003-redesign-compatibility-gateway/design/compatibility-coverage.md` | 6411 | `60a23d487e47faf0b71826e93175c57fdcbdc72da719572ed1751b11262d4a41` |
| `intent/0003-redesign-compatibility-gateway/design/current-code-assessment.md` | 7155 | `41546c5d0a876f41d64e48ade77bdbe473b672f3cf3778b1693c864c1f8dca92` |
| `intent/0003-redesign-compatibility-gateway/design/deployment-alternatives.md` | 17149 | `220d7bf6e421a9f362399bcdb740418401f2d7cd4378330b7c575d17d5d605fa` |
| `intent/0003-redesign-compatibility-gateway/design/execution-channel-contract.md` | 16642 | `4772cf71de2a3ea4f70d7640f18f04078d294a86ff8d87ed3e86974c2a9b6578` |
| `intent/0003-redesign-compatibility-gateway/design/foundation.md` | 9370 | `e8858a35f9d6e642c0435a7f266fe2b19c2f3ae27300592c1b275ab587f28b13` |
| `intent/0003-redesign-compatibility-gateway/design/integration-and-verification.md` | 15854 | `82fd5c40aa0b0921c470c19d03ffb77a1727c92097afc1ab7480616c31e5f80c` |
| `intent/0003-redesign-compatibility-gateway/design/message-submission-flow.md` | 15212 | `ca9d0355e0a804e5b139d049e6d669a7c6c66b823182dcd39f190e407fa3548e` |
| `intent/0003-redesign-compatibility-gateway/design/owner-recovery-boundary.md` | 15448 | `693e086e9b85c417c94e2ec20f520dcd1fb30dd3c08d965267740bea3e15422c` |
| `intent/0003-redesign-compatibility-gateway/design/protocol-and-resources.md` | 18656 | `0bb7917acad5591cffe90047002487cdc24bf97ead86b492a285d72a446e7bce` |
| `intent/0003-redesign-compatibility-gateway/design/runtime-lifecycle.md` | 16362 | `92169012c80d55655daef759dcfbb2f64e9e68f93706ad0e791501206b293f59` |
| `intent/0003-redesign-compatibility-gateway/design/skeleton-alternatives.md` | 14984 | `1603850d07468bb1284ce20500da03ed1f35431e357d866722edcf0643075d77` |

## 중대한 발견

**없음.** 수정이 필요한 P0/P1/P2 finding이나 해당 반례를 확인하지 못했다. 아래는 설계 판단의 근거와 입증 경계이며, 미실행인 제품 검증을 통과로 바꾼 목록이 아니다.

## 요구·수락 기준 대조

| 검토 영역 | 요구/AC | 판정 근거 |
|---|---|---|
| 원본 UI와 실제 엔진 | R1,R3,R10 / AC1,3,12 | spec 59–71, S9 35–40·52–69·140–143은 원본 serializer·Cap'n Web·두 WS/wire2를 유지하고 실제 컨테이너의 native 응답/bytes를 요구한다. 새 UI·health/mock을 연결 증거로 쓰는 경로가 없다. 원본 host 계약의 capability 수명은 고정 APP_HOST_CONTRACT 13–35와 대조했다. |
| 같은 작업 환경과 기능 목적지 | R2,R5 / AC2,3,4,5,9 | coverage 8–20과 S8 142–158이 Files/Git/worktree/PTY, projectless, folder picker, account, engineHome, automation rollout까지 B 제어와 X/work I/O로 구분한다. container path를 VM fs로 처리하거나 protected X UID로 사용자 cwd를 해석하지 않는 계약이다. opcode의 실제 완성 여부는 구현 범위다. |
| 접근 주체·연결·실행권 | R4,R5 / AC4,5,6 | S7 25–47·55–74의 dedicated origin/세션·mTLS와 S6 47–65의 M-signed grant/B ephemeral key는 각각 browser 인증, 서비스 인증, process 연속성을 구분한다. 새 B가 장기 인증서나 옛 ID만으로 initial/live 제어를 인계받지 못한다. |
| 실행·승인·원래 제출 | R6,R7 / AC6,7,8 | S2 M1–M7, S3 H1–H5, S5 49–105·109–145와 S8 81–104·165–175에서 X 수신, 최종 writer 진입, 원래 native 결과, UI 전달, 실제 종료를 분리한다. unknown/lookup miss/중복 응답은 재실행 근거가 아니다. |
| 정본 데이터·복구 | R7,R8,R10 / AC8,9,11,12 | S7 95–181·186–217은 pre-effect 소비/hold/queue transaction, TOML immutable object+exact pointer CAS, closed namespace, 참조 기반 첨부 정리, stable browser namespace를 정한다. code/build 복귀로 최신 history/auth/원장을 덮지 않는다. |
| 자원·성능 | R9 / AC10 | S8 20–25·54–138은 두 TLS pair/lane, 번호 수명, replay/credit와 실제 동시 사본 계수를 구분한다. S9 113–127은 원래 workload·측정 위치·분산 RSS 합계와 비교 지문을 요구하며 Git20 advisory 외의 한계를 완화하지 않는다. |
| 의존 방향·변경 비용 | R11 / AC13 | S1 foundation 53–70, S9 28–44·117–118이 core의 업무 판단과 DB/TLS/Podman/Cap'n 구현을 분리한다. 원본 method 변경과 runtime 변경을 실제 영향 범위로 평가한다. 추상 계층 수를 품질 증거로 쓰지 않는다. |

### 권한·기동·cold recovery

S6 53–70에서 startup grant는 M의 고정 할당·generation·B public key·build/protocol 문맥에 묶인다. X의 최초 binding은 grant와 B challenge 서명으로, 같은 B/X의 transport 복구는 S7 63–66의 memory continuity+expected binding CAS로 분리된다. pair 전체의 활성/폐기는 S8 20–24가 소유한다. 서비스 인증서 보유만으로 process 상실을 복구하는 예외를 발견하지 못했다.

S6 103–129는 단순 scope-empty 관측 외에 retiring의 durable 확정, 기존 lifecycle helper와 지연 start/exec의 해소, 고정 옛 container/init/cgroup 관찰을 요구한다. 새 세대는 그 뒤에만 열린다. X once/reaper 독립과 자동 재시작 금지도 명시되어 있다. stop exit0·M의 죽음·PID 숫자·새 UUID를 종료 증거로 대체하지 않는다. 따라서 no-late-spawn을 F6의 시험 이름만 남겨 둔 설계로 보지 않았다.

F6.1–F6.4는 현재 미설치된 runtime의 실제 성립을 판별할 후속 준비 검증이다. mapping/격리, 원본 engine sandbox, 자원 delegation, init/X 독립, 지연 기동·정리의 계약과 실패 시 재검토할 D6 결정이 이미 정해져 있다. 실제 이미지·UID 수치·cgroup identity가 미기입인 사실만으로 아키텍처 미결정이라고 판정하지 않았다. 이번 검토에서는 선택을 무효화하는 구체적인 불가능성이나 모순을 찾아내지 못했다. 현재 Ubuntu에서 해당 선택이 실행 가능하다는 주장은 하지 않는다.

### store writer·TOML·queue

S7 119–132의 store process가 직접 flock FD를 보유하고 writable DB를 열며, B와의 연결을 잃은 뒤 새 BEGIN을 금지한다. 이미 시작한 transaction의 정착과 DB close/process 종료까지 lock을 유지하고 old B/store scope 종료 전 새 writer를 금지한다. lock helper만 사라져 old writer가 뒤늦게 commit하는 경로를 허용하는 계약은 아니다.

TOML 게시의 config prepare guard는 object 저장보다 먼저 확정되고, object fsync/rename/directory sync 뒤 DB pointer CAS가 온다(S7 144–166). 일반 외부 editor의 base 없는 변경은 자동 현행판으로 채택하지 않고 staging/import conflict로 처리한다. 현재 코드의 pendingConfigs 차단·cron permissions/collaborationMode 보존·heartbeat settings 분리·단일 주기 claim과 비교했을 때, 물리 저장 대체가 이 의미를 제거하는 것으로 읽히지 않았다. queue는 동일 B transaction의 exact claim/bind/disposition으로 연결되고 consumed 작업을 DB outbox에서 재전송하지 않는다.

### 승인 본문 사본·보관과 실제 표시 소비자

현재 source는 `engine-ownership.mjs:308–327`에서 `measureRetainedBytes`로 승인 건별/합계 한도를 집행하고, `343–354`에서 응답 소비 시 pending 본문을 제거한다. `file-approval-items.mjs:72–84,100–110`의 선행 file item payload는 pending approval과 같은 합계 한도를 사용하며 반환용으로 무계수 diff clone을 만들지 않는다. `native-file-approval.mjs:18–23,51–74`에서는 그 exact file item과 request가 원본 표시의 실제 입력이다. 단순 request ID나 history의 유사 diff는 대체할 수 없다.

설계는 S7 103–104의 기존 승인 보관 한도, S8 58–61의 큰 요청 본문과 작은 응답 control 구분, 94–104의 replay/승인/receipt별 수명, 126–134의 동시 사본 예약을 함께 적용한다. `ACK 뒤 replay 사본 해제`를 아직 유효한 승인 본문 전체의 해제로 읽지 않았다. 반대로 X에 보관된 본문을 B의 소비된 응답 재인가 근거로 읽지 않았다. 실제 구현은 B/X의 물리 사본과 원본 file-item prerequisite를 함께 계수해야 한다. 이번 검토는 그 복사/회수 구현이 이미 존재하거나 16MiB의 실제 계수가 통과했다고 판정한 것이 아니다.

### D7.10 cache

S7 219–239는 세 대안 중 artifact/.NET의 영속 CacheStorage를 사용하지 않는 경로를 선택한다. 일반 local/sessionStorage·IndexedDB를 지우지 않고, 새 할당은 새 hostname, 같은 data의 build 변경은 stable origin이라는 설계다. cache 저장 성공을 흉내 내는 shim을 금지하고 fetch·취소·오류·동일 bytes/hash·동시 load를 준비 build에서 확인하도록 했다.

고정 `original-storage-inventory.json`의 조사 범위·storage families·cacheCleanup·limitations를 읽었다. 원본 vendor loader 자체는 이 210개 packet의 고정 source 사본에 없으므로 직접 읽거나 해당 anchor/지원 옵션을 새로 검증하지 않았다. inventory의 기존 정적 관찰을 이번 reviewer의 renderer 직접 실행/원본 21개 파일 해시 검증으로 쓰지 않는다. 선택된 비영속 fetch 계약의 실제 원본 호환성은 명시된 준비 patch 검증 대상이다.

### 대안·비용

논리 소유권 A/B/C, 물리 P1/P2/P3, D5.1, D6.1–D6.4, D7.1–D7.10, D8.1–D8.6을 읽었다. P0의 같은 UID 결함을 세 유효 배치 대안의 하나로 세지 않았고, workload/권한/복구 조건이 같은 대안의 실제 이점·비용·번복 조건을 기록했다. 선택한 P1의 원격 전송/복사, M 및 store process, 인증서 배포, explicit cold recovery의 가용성 손실을 실측 성능 우위로 포장하지 않는다. 고정 요구를 위반하는 retry/exactly-once 또는 대체 UI를 형식적인 대안으로 세지 않는 것도 타당하다.

## 실제 읽은 추가 범위와 실행 한계

authoritative 15개는 전체를 읽었다. 그 외 다음 고정 사본을 업무상 선택해 읽거나 명시 범위에서 검색했다.

- 정책 전체: `AGENTS.md`, `CLAUDE.md`, `PROJECT-POLICY.md`, `REVIEW.md`, `.agents/skills/sdlc-feedback/SKILL.md`. 구현 완료용 재귀 리뷰·서비스 실행·추가 subagent를 수행하지 않았다.
- source 전체: `src/shared/protocol-policy.mjs`, `src/server/engine-approval-ids.mjs`, `src/server/file-approval-items.mjs`, `src/browser-bridge/native-file-approval.mjs`, `src/server/stdin-writer.mjs`, `src/server/retained-size.mjs`.
- source 발췌/검색: `engine-ownership.mjs`의 승인/제어권/파일 item 처리와 180–211·230–356, `engine-session.mjs`의 request/dispatch/receive/timeout/send/fail/close, `engine-requests.mjs`의 권한/준비/최종 native 호출·정착, `automation-store.mjs`의 230–350·500–578 및 TOML/claim 관련 검색. `host-fetch.mjs`와 `app-host.mjs`는 automation/readFile 관련 검색 결과를 확인했다. 이 파일들 전체를 읽었다고 주장하지 않는다.
- 참조 계약 발췌: `docs/diagnosis/execution-lifecycle-contract.md`의 120–208 및 승인/제어 검색, `docs/APP_HOST_CONTRACT.md`의 bootstrap/capability·host services·settings 부분.
- 저장소 감사: `references/original-storage-inventory.json` 1–240의 정적 감사 범위/가족/한계. 나머지 원본 vendor/외부 문서/과거 리뷰를 직접 조사하지 않았다.

Mac에서 Python의 파일 읽기·bytes/SHA-256 계산과 읽기 전용 source 검색을 수행했다. 제품 Git/Node/시험/브라우저/서비스/설치/외부 모델 CLI/Muse/추가 agent는 실행하지 않았다. 고정 packet과 제품/정본 파일을 수정하지 않았고, 이 보고서 한 개만 새로 썼다. 일부 source 도구 출력은 길이 제한으로 잘렸으므로 전체 읽기 주장에 포함하지 않았다.

이 보고서는 위 입력의 **최초 판정**으로 고정한다. 이후 입력 변경에 대한 판단은 별도 검토이며 이 파일의 PASS를 승계할 수 없다.
