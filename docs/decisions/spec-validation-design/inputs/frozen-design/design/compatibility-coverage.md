# 원본 호출 패밀리의 목적지와 이행 경계

현재 source를 Sol/high가 읽기 전용 대조하고 root가 S6–S9 정본에 연결했다. 제품 실행 결과가 아니다.
기존 [초기 코드 평가](current-code-assessment.md)의 미결 호출 지도에 대한 후속이다. 개별 코드 삭제 목록은 plan에서 정한다.

| 호출 패밀리 | 현재 source 진입점 (`src/` 기준) | 목표 소유자·금지할 fallback |
|---|---|---|
| 시작/Cap'n Web/두 WS | server/gateway, app-host, prepared-build, static-assets; browser-bridge/index | B 호환/인증 종단과 browser. capability/callback은 X로 넘기지 않음 |
| native engine·thread 수명 | server/engine-requests, engine-session, engine-ownership, stdin-writer, app-server, thread-lifecycle | native/process는 X, 업무 소비/판정은 B, 원본 projection은 호환 adapter |
| host/global/settings/account | server/host-fetch, settings-fetch | B 설정/registry. account는 X의 allowlisted account projection 또는 고정 CODEX_HOME reader가 비밀 없는 결과만 반환 |
| workspace files | server/app-host, file-read, file-metadata, file-watches, request-policy, turn-steer-policy | X work helper의 fd/path 검사. B나 protected X에서 사용자 path를 realpath/open/stat하지 않음 |
| 프로젝트/폴더 선택 | server/projects, folder-picker, gateway의 fixturesRoot 처리 | B 이름/순서/root mapping; 실제 열거/검증은 X work. VM fixturesRoot로 대체하지 않음 |
| projectless | server/projectless-workspace, gateway의 stateDir/projectless | X work의 container projectless/outputs/work 생성. B에는 logical thread/cwd mapping만 보존 |
| Git/Review | server/git-worker, git-query-scheduler, git-snapshots, git-working-hashes, git-invalidation, host-fetch | 실제 Git/query/snapshot capture/hash는 X work. B는 요청 조정·global budget·원본 반환. 로컬 VM Git fallback 없음 |
| worktree/pending | server/worktrees, pending-worktrees | X work의 FS/Git effect, B의 registry/pending/owner relation. `.git/codex-thread.json`은 남아도 비권위 projection |
| PTY | server/terminal, owned-pty | X work UID의 실제 PTY/자식/cwd. VM bash·/proc를 사용자 PTY로 사용하지 않음 |
| attachment/save/download | server/attachment-store, app-host; browser 저장 adapter | B ready/ref/hold, X exact 보호 object, browser 실제 저장 outcome. 개인 CODEX_HOME에 제어 ledger를 두지 않음 |
| automation/inbox | server/automation-store, automation-service, automation-scheduler, automation-execution, automation-targets, automation-inbox | B 설정/claim/run/inbox, X native/workspace/rollout 관찰. thread.path를 VM에서 읽지 않음 |
| queue/submission/control store | server/settings-service, thread-projects, native-queue 계열, native-submission-bindings, state-store | B canonical DB/transaction. X의 request guard는 업무 원장 복제 아님 |
| engineHome·visualizations·shell environment | gateway/host-fetch/automation/request-policy의 engineHome 사용 | user auth/config/history/rollout·visualization mkdir·Git shell-env는 X work 또는 고정 전용 reader. B가 HOME 문자열을 로컬 권한으로 쓰지 않음 |

표의 source명은 실제 `.mjs` 파일/계열이다. 그 함수의 현재 구현이 이미 target을 따른다는 뜻이 아니다.
새 opcode manifest는 모든 실제 producer/consumer를 이 family에 연결해야 한다. 미분류 host method는
범용 exec/fs fallback으로 처리하지 않고 effect 전에 거절한다. 신규 003 후보의 지원 목록·미지원 이유는 원본
준비 build에 고정하며 알려진 미지원 기능을 성공처럼 표시하지 않는다.

## 브라우저 데이터의 전체 경계

현재 bridge의 sessionStorage key는 `poc-draft-checkpoint-v1`, `poc-draft-tab-v2`, `poc-draft-alternate-v1`,
`poc-execution-capabilities-v1`, `poc-consumed-approvals-v1`, `poc-viewed-thread-v1`, `poc-recovery-reloads-v1`이다.
IndexedDB는 `codex-browser-drafts/checkpoints`, `codex-browser-draft-lifecycle/lifecycles`다.
bridge의 직접 localStorage 쓰기는 소스 감사에서 없었고 draft identity는 현재 appVersion에 의존한다.

S7의 server-issued stable namespace를 모든 envelope/key/IDB record에 적용한다. 공개 health에 data identity를
노출하지 않고 인증된 bootstrap/readiness에서 namespace를 대조한다. build ID나 engine generation을 dataId로 쓰지 않는다.
원본 renderer의 자체 localStorage/IndexedDB/Cache/ServiceWorker는 src 목록만으로 포괄했다고 주장하지 않는다.
별도 [원본 저장소 감사](../references/original-storage-inventory.json)는 고정 snapshot에서 저장소 사용이 검색된
vendor 21개 파일의 현재 bytes/SHA가 extraction manifest와 일치함을 확인했다. 동적 persisted atom·인증·편집기
IndexedDB·telemetry queue·Mapbox 저장 등 17개 family를 기록했으며 동적 key 전체를 열거했다고 주장하지 않는다.
직접 serviceWorker 등록 일치는 0개다. 간접 호출까지 없다는 증거는 아니다. `.NET/artifact`의 path별 CacheStorage는
S7 D7.10에서 명시적으로 비영속 artifact fetch 경로를 선택한다. 일반 사용자 저장까지 지우는 cache 정리는 하지 않는다.
S7의 dedicated origin↔principal/allocation/data 영구 결합을 전체 browser storage에 적용한다. 새 할당은 새 origin이고
기존 origin의 내용을 초기화하거나 다른 주체로 import하지 않는다. 같은 data의 build 변경에는 원래 build 검증과
prepared immutable asset/loader 계약을 적용한다. 오래된 문서/서비스 참조와 새 WS를 섞지 않는다.

## 이행 수락의 유한 관찰

1. 위 source family 각각에서 B의 사용자 FS/Git/PTY 실행이 없는지 dependency/실제 call trace를 대조한다.
2. worktree owner file·browser path·engine path·auth projection이 관리 권한이 되는 우회를 거절한다.
3. 동일 input과 attachment bytes가 실제 container engine에 전달되고 Files/Review/PTY 결과가 같은 공간에 대응하는지 본다.
4. 모든 bridge key와 원본 browser 저장에 대해 same-data reload/build 변경과 다른-data origin을 구별한다.

이는 설계 입력과 구현 후 검증 목록이다. 현재 운영 source를 수정하거나 새 runtime/브라우저에서 실행하지 않았다.
