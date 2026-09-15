# S6 — 고정 할당의 runtime과 외부 수명 소유자

상태: 003 설계 결정. 실행 PASS나 runtime 설치 완료가 아니다. [S4](deployment-alternatives.md)의
VM B + 보호된 컨테이너 X 배치, [S5](execution-channel-contract.md)의 process 상실 후 cold recovery를 구체화한다.
이 문서는 runtime·외부 기동/종료·복구 범위를 소유한다. 업무 제어는 B, native/작업 실행 사실은 X가 소유한다.

## 1. 세 대안씩 비교하고 선택한다

같은 조건은 기존 Ubuntu 한 대 안의 한 할당, 다른 VM 업무 보존, 모든 작업 I/O의 컨테이너 실행,
work UID와 제어 권한 분리, 불명 요청 비재전송, 실제 종료 확인이다. 성능 순위는 실측하지 않았다.

| 결정 | 대안 A | 대안 B | 대안 C | 선택·비용·번복 조건 |
|---|---|---|---|---|
| D6.1 runtime | rootless Podman + VM systemd | rootless Docker + VM systemd | rootless containerd/nerdctl + VM systemd | A. 업무 경로에 runtime CLI를 넣지 않고 관리 daemon 수명을 줄인다. B는 daemon 재시작과 live container를, C는 shim/snapshotter 조합을 추가 관리한다. A의 보호·자원·정리 조건이 성립하지 않고 다른 안이 같은 조건을 증명하면 재비교한다. 공통 namespace/delegation 실패를 이름 교체로 우회하지 않는다. |
| D6.2 X 상실 뒤 명시적 복구 scope | 자원별 외부 cgroup | X 세대 전체의 외부 cgroup subtree | 할당 컨테이너 전체 | C. 이 컨테이너의 모든 실행이 한 할당에 속하고 live stdio 인계가 없는 조건에서 종료 범위를 외부가 열거하기 쉽다. 모든 PTY·Git·백그라운드 작업도 중단되는 가용성 비용을 수용한다. 독립 작업 보존이 요구되면 A/B를 실제 기동 전 귀속·이탈 차단과 함께 재설계한다. |
| D6.3 container init | s6 init/reaper와 X once 기동 | 내부 systemd와 Restart=no X service | 전용 최소 init/reaper 구현 | A. reaping을 검증된 도구에 맡기고 내부 systemd/cgroup 통합이나 자체 signal 구현을 피한다. X 재시작 금지의 실제 집행 검증은 필요하다. A의 once 수명이 유지되지 않으면 B와 비교하며 소형이라는 이유만으로 C를 택하지 않는다. |
| D6.4 M 관리 접점 | runtime socket을 B에 직접 전달 | VM 보호 Unix socket의 고정 명령 M | 일반 원격 관리 서비스와 역할별 API | B. 한 할당의 lifecycle만 노출한다. A는 코드가 작지만 B 결함의 관리 권한 범위가 크고, C는 원격 관리 인증·API 운영 비용이 있다. 할당 서비스가 실제 도입될 때 C를 재평가한다. |

Podman은 [고정 4.9.3 문서](https://github.com/containers/podman/tree/v4.9.3/docs/source/markdown),
비교안은 [Docker rootless](https://docs.docker.com/engine/security/rootless/)와
[nerdctl rootless](https://github.com/containerd/nerdctl/blob/v2.1.0/docs/rootless.md)를 참조했다.
[Podman systemd 통합](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html)의 최신 옵션을
4.9.3 지원 사실로 사용하지 않는다. 정상 데이터 경로의 별도 daemon 부재가 속도 우위의 증거는 아니다.

## 2. M의 권한과 데이터

M은 VM에서 **고정 할당 한 개의 외부 lifecycle**만 관리한다. 전용 runtime Unix 계정으로 실행하며
rootless runtime storage·관리 bus·CLI 권한은 그 계정에만 있다. B 계정과 work UID에는 주지 않는다.
M도 VM root의 임의 관리 권한을 갖지 않는다. 전용 계정·subuid/subgid·systemd delegation을 준비하는
관리 절차는 별도 설치 입력이며 B나 브라우저의 기능으로 만들지 않는다.

관리자가 고정한 manifest는 allocationId, dataId, 허용 image digest, 컨테이너 경로/볼륨 identity,
B 서비스 identity, X 기동 파일 hash, network 정책, resource profile hash를 포함한다. 사용자·renderer가
임의 image·mount·argv·PID·cgroup 경로·container selector를 전달할 수 없다. 이름만 맞는 컨테이너도 대상이 아니다.

M의 durable lifecycle record는 schemaVersion, allocationId/dataId, generation, lifecycleOperationId,
phase(prepared/starting/running/retiring/stopped/uncertain), runtime container ID, generation별 생성 이름,
확인한 init/process/cgroup identity, pending 관리 helper, 종료 관찰을 보존한다. 인증 비밀·업무 메시지·
승인 본문은 넣지 않는다. 단일 M은 Linux flock으로 기록 writer를 소유하고 기존 원자적 파일 저장의
file sync→rename→directory sync를 따른다. flock 획득은 옛 실행 종료 증거가 아니다.

입력 명령은 inspect, prepare-fixed-generation, start-prepared, fence-generation, stop-generation,
inspect-operation으로 닫는다. prepare/start는 외부 운영자가 명시적으로 연 고정 배치에만 사용한다.
B는 inspect와 현재 세대의 fence/stop 요청만 요청할 수 있고, 신규 할당·image 변경·임의 exec는 못 한다.
브라우저 retry는 readiness 재조회이며 컨테이너 복구 명령이 아니다.

M socket은 보호된 VM 경로에 둔다. kernel peer UID/PID와 등록한 B process identity·메모리 capability를
함께 확인한다. 최초 B 등록은 고정 서비스에서 온 살아 있는 한 process만 원자적으로 등록하며 기존
등록자가 살아 있으면 교체하지 않는다. process identity는 boot ID/PID/start identity와 live pidfd를
함께 사용한다. M이 재시작하여 연속성 근거를 잃으면 새 B 권위를 자동 부여하지 않고 §5 복구로 간다.
장기 서비스 credential, 같은 UID, 저장된 B ID는 이전 process의 권위 복원 근거가 아니다.

최초 등록에서 B는 process 메모리에만 둔 ephemeral signing key의 public key를 M에 제출하고
M challenge에 서명한다. M은 peer process와 public key를 durable 등록한 뒤, 고정 allocation/data,
container/X generation, B process identity/public key, build/protocol digest, 일회 grant ID에 서명한
startup grant를 발급한다. M 공개 검증키는 X의 보호된 bootstrap 입력이다. X는 grant의 자기 문맥과
B의 challenge 서명을 확인하고 한 번만 initial binding을 만든다. 서비스 인증서만으로 initial grant를
요청하거나 재사용할 수 없다. grant 재조회는 같은 public key/ID의 같은 문서만 반환하며 새 권위를 만들지 않는다.
M의 서명키는 VM M 계정에서 보호한다. grant는 실행 권위이므로 일반 로그에 싣지 않는다.

B 교체는 등록한 옛 B process가 실제 종료하고 VM control-store flock을 놓은 뒤에만 가능하다.
M이 다른 UID의 B를 임의 kill할 권한을 갖지는 않는다. 필요한 B 중단은 operator가 고정 systemd B unit에
수행하는 복구 단계이며 PID 문자열을 직접 죽이지 않는다. X 상실 뒤 같은 B가 생존한 경우는 B를 교체할
필요가 없다. M 상실 뒤 살아 있는 옛 B는 durable public key에 대한 새 challenge와 실제 process identity를
대조해 관찰자로 재등록할 수 있으나 cold recovery 전 업무 권위를 재개하지 않는다.

## 3. 기동은 effect 전에 귀속한다

1. B/M 제어 저장소와 지정 볼륨이 존재·정합한지 확인한다. 예상 데이터 소실을 신규 초기화로 처리하지 않는다.
2. M은 새 generation과 고유 생성 이름을 durable prepared로 확정한 뒤 runtime 명령을 시작한다.
   시작된 CLI/helper의 고정 systemd 작업 단위와 operation ID도 기록한다. 명령을 잃은 뒤 이름을 새로
   만들어 재시도하지 않는다. 알려진 생성 이름의 기존 대상을 관찰하고 완료/불명으로 분류한다.
3. 새 컨테이너는 network/user/PID/mount namespace를 분리하고 임의 host mount·관리 socket·host network가 없다.
   시작부터 할당된 cgroup 안에 들어가야 한다. work가 cgroup을 이동·확장하거나 privileged namespace를
   만들어 제어 권한을 얻지 못하게 한다. 실효 UID mapping·capability·mount·controller 값을 시작 입력과 대조한다.
4. 보호된 init은 살아 있고 X service는 기본 down이다. M이 고정된 bootstrap 한 번만 허용한다.
   X는 재생성된 supervisor에서도 자동 재기동되지 않는다. X에게 runtime 관리 socket이나 임의 spawn grant를 주지 않는다.
5. X가 M이 지정한 container/generation과 실행 입력을 확인한 뒤 B와 실행 binding을 맺는다.
   engine 실제 생성·initialize·저장/권한/예산 준비까지 확인해야 readiness와 새 업무 admission을 연다.

X/engine을 container PID 1의 수명과 직접 묶지 않는다. PID namespace init이 죽으면 나머지 프로세스도
종료되므로 X 장애를 관찰한 뒤 명시적으로 복구한다는 계약을 보존해야 한다.
[Linux PID namespace](https://man7.org/linux/man-pages/man7/pid_namespaces.7.html),
[s6 once 제어](https://github.com/skarnet/s6/blob/v2.12.0.3/doc/s6-svc.html)를 기초로 구현 후보를 검증한다.
init 자체의 crash·OOM·VM 종료는 전체 실행 상실이다. 이를 승인 보존이나 무중단 실행으로 약속하지 않는다.

## 4. 권한과 spawn 환경

컨테이너 init·X 제어 파일과 secret socket은 work와 다른 UID가 소유한다. X가 work 프로세스를 만들 때는
작업 UID/GID·supplementary group·capabilities·열린 FD·환경을 명시적으로 정한다. 기본은 positive allowlist다.
제어 credential·부모 환경 전체·관리 FD를 상속하지 않는다. 원래 app-server의 환경 denylist만 재사용하면 부족하다.
고정 launcher는 먼저 work credential/FD/capability를 확정한 뒤 사용자 cwd를 해석하고 chdir한다.
Node spawn의 uid 옵션이 있다고 user cwd 접근까지 UID 전환 뒤라고 가정하지 않는다. X가 여는 cwd/root FD는
M이 고정한 mount root에 한정하며 그 아래 사용자 경로 해석은 work helper가 한다. PTY도 같은 순서를 적용한다.
작업용 subprocess가 다른 UID로 engine 내부 도구를 실행할 수 있다고 가정하지 않는다. 실제 Codex와
그 도구·PTY·Git은 work identity다. Codex 개인 인증의 의미는 다음 인증/데이터 계약에서 별도로 정한다.

작업 코드와 Git hook은 신뢰하지 않는다. cwd 검사만으로 보호가 되지 않으며 동일 UID 파일 읽기와
signal 권한·/proc·network 접근까지 negative 사례로 검증한다. 기본 root filesystem은 read-only,
작업·개인 설정·history의 선언한 볼륨만 writable이다. 필요한 X 제어 capability는 고정 launcher에서만
사용하고 일반 작업에는 제거한다. container root를 VM root와 동일시하지도, 자동으로 안전하다고 보지도 않는다.

## 5. 명시적 cold recovery와 실패 의미

B/X transport만 끊겼으면 S5의 same-process binding 복구다. B/X process 또는 M 연속성을 잃으면
새 업무를 fence하고 관찰·이미 소유한 정리를 유지한다. 자동 container 재시작·health restart·auto-update·
systemd restart·X restart를 추가 기동자로 남겨 두지 않는다. 장애 감지만으로 전체 종료하지 않는다.
운영자가 정확한 할당의 cold recovery를 요청할 때 아래 순서를 수행한다. 전체 종료는 정밀 정리 실패의 fallback이 아니다.

1. M이 해당 generation을 durable retiring으로 기록하고 모든 start/exec/grant를 차단한다. 저장 불명은 fence한다.
2. M의 이전 lifecycle helper/systemd job과 pending runtime start를 대조한다. 이미 진입한 지연 create/start도
   끝나거나 취소·종료된 사실을 확인할 때까지 새 세대를 열지 않는다. M process가 사라졌다는 사실만으로
   helper 종료를 가정하지 않는다. 다른 generation의 컨테이너를 해당 불명 작업의 대체물로 만들지 않는다.
3. 살아 있는 X에는 기존 binding fence와 owned cleanup을 요청한다. 불명 응답은 성공이나 미실행이 아니다.
4. 고정된 옛 container ID의 종료를 요청한다. 기본 profile은 기존 engine shutdownGraceMs=5000 안에서
   killEscalationMs=4500에 강제 종료를 요청하고 남은 구간에서 확인한다. 각 하위 단계마다 5초를 새로 주지 않는다.
   이는 종료 보장 시간이 아니라 대기 상한이다. runtime 기본 10초 stop과 중첩하지 않도록 명시 신호/kill을 사용한다.
5. M은 container init 종료, 정확한 cgroup subtree의 populated=0, pending start/exec 부재, 관련 runtime
   monitor/network/helper와 자원 의무의 정리 상태를 확인한다. 단순 Podman stop exit0·unit inactive·저장된 PID는 충분하지 않다.
6. 확인을 durable stopped로 보존하고 B가 S3 저장·불명 시도·현재 정책을 대조한 뒤에만 새 세대를 준비한다.

deadline 초과·scope 대응 불명·helper 미확인·M 저장 실패면 retiring/uncertain으로 남고 readiness/new mutation은
닫힌다. 데이터는 보존한다. 반복 stop은 동일 lifecycle operation의 현황과 아직 살아 있는 소유 scope에만
작용하며 새 PID·임의 경로를 대신 종료하지 않는다. [cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html)의
populated/kill 기능은 실행 범위 관찰 수단이다. 미래 유입 권위와 경로 재사용을 스스로 배제하지 않는다.

작업 프로세스가 종료해도 이미 발생한 파일 변경·원격 효과·kernel writeback을 취소한 것은 아니다.
파일 결과의 성공/원자성은 해당 저장 계약으로 판별하고 unknown을 유지한다. 관측 불가능한 “모든 외부 I/O 소멸”을
새 성공 조건으로 만들지 않는다. 같은 볼륨의 새 writer는 옛 프로세스와 관리 명령의 유입 배제를 확인한 뒤 연다.

## 6. 환경 근거와 구현 전 판별

[기존 preflight](../references/s6-runtime-preflight.md)와 [추가 namespace 관찰](../references/s6-namespace-observation.json)을 읽는다.
2026-09-14 UTC 05:39의 제한된 user/PID namespace는 exit0으로 끝났고 UID 0→host501의 단일 mapping을 확인했다.
이는 복수 UID/subuid·mount/network/cgroup·container 실행 검증은 아니다. 로컬 apt cache에는 Podman
4.9.3+ds1-1ubuntu0.2, crun1.14.1-1, uidmap4.13 계열, s6 2.12.0.3-1build1 후보가 있지만 미설치다.
현재 사용자 systemd manager는 signal9 실패다. 원인·전용 계정 delegation 성공을 추정하지 않는다.

첫 준비 검증은 disposable 전용 scope에서 아래 순서로 한 번의 구별 가능한 판별을 수행한다.
설치·계정/delegation·container 기동은 현재 실행 범위 밖이다. 여기서는 요구와 실패 시 대응을 확정한다.

| 판별 | 필요한 증거 | 실패 시 영향 |
|---|---|---|
| F6.1 mapping·기본 격리 | 두 실제 UID, work의 X/VM sentinel 접근 거절, hostnetwork/mount 비노출 | R5 성립 전 product wiring 금지. 단일 UID/privileged/hostnetwork 우회 금지 |
| F6.1에 포함할 engine 조건 | 고정 engine가 원래 sandbox/approval 모드로 실행하고 필요한 Linux sandbox 기능이 실제 작동 | 편의를 위한 danger-full-access·자동 승인·제어 UID 실행으로 우회하지 않음 |
| F6.2 자원 위임 | 고정 container cgroup의 cpu/memory/pids 실효 제한과 scope 밖 sentinel 보존 | R9 미충족. 전용 계정 준비를 수정하거나 D6.1 대안 재비교 |
| F6.3 init/X 독립 | X crash 뒤 init 생존, 재시작 0회, 유효 남은 실행을 관찰 | D6.3 구현 교정/재비교. live takeover로 요구 변경 금지 |
| F6.4 늦은 spawn·정리 | M crash/stop 응답 유실·setsid child·지연 start 후 이전 scope 종료와 새 유입 0 | D6.2/관리 adapter 수정. 후속 제품 구현 선행 조건 |

이 네 항목은 설계 선택의 실행 적합성 검증이며 미실행 상태다. 최종 문서 설계가 완성되어도 이를
통과하기 전에는 현재 환경에 검증된 runtime이 있다고 인계하거나 제품 구현을 바로 가동하지 않는다.
실제 설치 판·이미지 digest·생성 unit과 hardening은 준비 결과로 고정하고 최신 문서만으로 지원을 주장하지 않는다.
