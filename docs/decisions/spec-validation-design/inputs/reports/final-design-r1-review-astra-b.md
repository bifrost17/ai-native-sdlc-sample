# 003 final-design-r1 독립 최종 설계 리뷰 B

판정: **PASS — 동결된 최종 설계 문서의 통합 계약 범위에 한정.**

중대한 actionable finding은 발견하지 못했다. 제품 구현, 실행 적합성, 컨테이너 격리, AC, Q5, 운영 전환 또는 특정 SHA의 사람 수락을 PASS로 판정한 것이 아니다. 다른 검토자의 판정을 수신하지 않은 상태에서 최초 보고서를 고정한다.

## 검토자와 독립성

- 검토자: `/root/policy_removal_review/runtime_independent`.
- 생성한 parent의 2026-09-14 확인: 실제 spawn 도구 인자는 `model=gpt-6-astra`, `reasoning_effort=high`, `fork_turns=none`이며 생성에 성공했다. 별도 runtime model telemetry는 제공되지 않았다. 도구 지정 사실을 runtime telemetry 검증으로 표현하지 않는다.
- 이 설계의 작성·설계 조언에 참여하지 않았다. 동결 통보 전에는 설계를 읽지 않았고, 동결 통보 후 최종 전체 범위로 독립 검토했다. peer 최초 판정·발견·보고서는 읽지 않았다.
- 제품 명령, Git/Node, 서비스, 컨테이너, 브라우저, 외부 모델/CLI, 추가 하위 에이전트는 실행하지 않았다. Mac에서 파일 읽기·SHA-256/바이트 확인과 이 보고서 쓰기만 수행했다.

## 동결 입력과 무결성

- 입력: `references/final-design-r1/inputs.json`.
- manifest SHA-256: `d36ca8a1d3b2a098a58afb704ac10bfd69271c9004c1bbca3395436bfaac6e8b`.
- 시작 시: manifest 해시 일치, `files/`의 210개 파일을 전부 읽어 SHA-256/바이트 수 대조, 불일치 0.
- 종료 전: 2026-09-14 06:46:38.988862 UTC에 manifest 재확인, 210개 고정 사본 SHA-256/바이트 재대조, 불일치 0. 현재 worktree의 15개 authoritative 파일도 동결 사본과 대조하여 불일치 0.
- 의미 검토: `authoritativePaths`의 15개 문서를 전부 읽었다. 아래 네 정책과 세 팀 스킬, 관련 원본 계약·자원 상수·선별 source를 대조했다. 210개 모두에 대한 무결성 확인을 210개 모두의 전면 source audit로 표현하지 않는다.
- 정책: `AGENTS.md`, `CLAUDE.md`, `PROJECT-POLICY.md`, `REVIEW.md`, `docs/policies/PROGRESS_AND_DIAGNOSIS.md`.
- 팀 스킬: `.agents/skills/design-spec/SKILL.md`, `.agents/skills/spec-policy-pass/SKILL.md`, `.agents/skills/sdlc-feedback/SKILL.md`. 스킬이 참조하는 별도 verifier 설정은 이 동결 packet에 없어 그 설정 전체를 적용했다고 주장하지 않는다. 현재 명시된 독립 문서 리뷰 범위와 프로젝트 정책을 기준으로 검토했다.

## 통합 대조와 판단 근거

경로는 `intent/0003-redesign-compatibility-gateway/` 기준이다. 아래는 발견 목록이 아니라 검토한 주요 반례와 그 반례를 다루는 계약 위치다.

| 검토 축·반례 | 읽은 정본 위치 | 판단 |
|---|---|---|
| 원본 renderer를 유지하면서 모든 workspace 효과를 컨테이너로 옮기는가? 숨은 VM projectless/rollout/account 경로가 남는가? | `spec.md:31-40`, `design/compatibility-coverage.md:6-25`, `design/integration-and-verification.md:31-48` | 원본 호환은 B에서 종단하고 실제 file/Git/worktree/PTY·rollout은 X/work에 둔다. capability 객체를 일반 JSON 서비스로 바꾸거나 VM filesystem fallback을 허용하지 않는다. |
| logical B 선택이 X/M의 별도 업무 권위 복제로 바뀌는가? | `design/foundation.md:19-35`, `design/deployment-alternatives.md:115-121`, `design/execution-channel-contract.md:14-20` | B의 업무 소비/허용, X의 native/effect·자원 사실, M의 고정 lifecycle이 구분된다. X의 최종 guard는 별도 상위 업무 조정자가 아니다. |
| 같은 서비스 credential을 가진 새 B가 살아 있는 실행을 선점하는가? M 재시작이 권위를 복구하는가? | `design/runtime-lifecycle.md:47-65`, `design/authority-and-data.md:55-74` | peer process identity·live pidfd·ephemeral key challenge·M grant·X 일회 소비와 same-live continuity를 함께 요구한다. M 연속성 상실도 cold recovery 전 업무 권위를 자동 복원하지 않는다. |
| M/CLI가 죽은 뒤 지연 start가 old scope로 유입하는가? X 자동 재기동이 종료 증거를 무효화하는가? | `design/runtime-lifecycle.md:69-85`, `design/runtime-lifecycle.md:105-129` | generation/operation의 durable 귀속, pending helper/start 종료 대조, X once, 정확한 container/cgroup 및 helper 정리 확인 후 새 세대를 연다. timeout/stop exit0를 실제 종료로 대체하지 않는다. |
| privileged X가 user cwd/symlink/Git hook을 따라 VM·제어 권한을 행사하는가? | `spec.md:35`, `design/runtime-lifecycle.md:89-101`, `design/protocol-and-resources.md:154-158` | work credential/FD/capability를 먼저 확정한 helper가 경로를 해석한다. 자기 Codex 개인 auth의 same-UID 접근은 별도 한계로 명시하고 B/M/X secret과 혼동하지 않는다. |
| B 장애 뒤 옛 store transaction이 새 writer와 겹치는가? | `design/authority-and-data.md:111-136`, `design/owner-recovery-boundary.md:85-101` | writable process가 flock 자체를 보유하고 BEGIN 직전 B/data/store generation을 검사한다. 이미 진입한 transaction의 불명과 살아 있는 lock을 새 writer로 우회하지 않는다. |
| TOML 파일 교체와 DB claim 사이 crash가 옛 설정 실행·cron 권한 소실을 만드는가? | `design/authority-and-data.md:138-166`, `design/authority-and-data.md:202-210` | immutable object·exact-base pointer CAS·선행 config prepare guard·unbased import conflict를 정했다. 가변 파일/JSON 물리 구현 대체를 명시하면서 TOML 의미와 cron mode/permissions·heartbeat settings·unknown 비재전송은 보존한다. |
| 업로드 확인 뒤 work 코드가 bytes를 바꾸거나 삭제와 hold가 경합하는가? | `design/authority-and-data.md:184-198` | X 보호 publication과 exact receipt, B ready/ref commit을 구분한다. delete intent와 새 참조 확보는 같은 transaction에서 배타적이며 unknown hold를 TTL로 버리지 않는다. |
| 두 TLS 중 하나 교체, late queued effect, dispatch 번호 회수로 중복 진입하는가? | `design/execution-channel-contract.md:43-88`, `design/protocol-and-resources.md:20-24`, `design/protocol-and-resources.md:71-84` | pair 전체의 CAS/fence, 실제 writer 직전 guard, family/lane별 유지되는 단조 소비 번호를 사용한다. 자동 mutation retransmission을 허용하지 않는다. |
| X ACK·thread snapshot·늦은 결과가 과거 turn 또는 승인 성공으로 오인되는가? | `design/message-submission-flow.md:94-114`, `design/execution-channel-contract.md:94-117`, `design/protocol-and-resources.md:86-104` | native 상관/step별 accepted, writer와 resolved, 현재 관찰과 과거 수락을 구별한다. gap/상관 소실은 unknown과 관련 mutation fence로 남는다. |
| 분리 배치에서 buffer/credit을 두 번 허용하거나 ACK 뒤 조기 반환하는가? | `design/protocol-and-resources.md:110-138` 및 고정 `src/shared/protocol-policy.mjs:14-85` | data/assembly/framer/control 합계, 별도 control reserve, codec1·large-I/O2, 사본 중복 예약, exact credit 반환과 process 상실 후 reclaim 조건을 정했다. protocol accounting과 전체 RSS를 구분한다. |
| build/restart가 초안을 지우거나 다른 할당에 browser storage를 노출하는가? | `design/authority-and-data.md:30-47`, `design/authority-and-data.md:212-238`, `design/compatibility-coverage.md:27-44` | stable data identity와 전용 origin의 영구 결합을 사용한다. 식별한 artifact cache만 비영속 경로로 바꾸며 일반 auth/편집 storage를 제거하지 않는다. 동적 service-worker 관측 한계도 명시한다. |
| 추가 hop 비용을 품질 완화·부분 PASS로 숨기는가? | `design/integration-and-verification.md:111-143`, `spec.md:49-70` | Git20만 advisory이고 다른 기존 한계·오류/비교불가·자원 실패를 완화하지 않는다. 새 topology의 집계·측정 위치·동일 후보 지문과 실제 browser/engine 증거를 요구한다. |

## 대안과 실행 전 판별

S1의 A/B/C, S4의 P1/P2/P3, S5 D5.1, S6 D6.1–D6.4, S7 D7.1–D7.10, S8 D8.1–D8.6을 읽었다. 주요 배치·소유·복구·저장·전송 결정에는 서로 다른 실질 대안, 선택안, 유지 비용과 번복 조건이 있다. P0 같은 권한 결합의 기각 기준선을 유효한 세 물리 대안에 포함하지 않는다. 문서에 없는 성능 순위를 검토자가 추가하지 않았다.

F6.1–F6.4의 미실행과 현재 runtime/전용계정/delegation 미준비는 분명한 실행 한계다. 이를 곧바로 문서 설계 결함으로 판정하지 않았다. 선택된 runtime·scope·init·grant·writer·transport 계약이 이미 구체화되어 있고, 준비 판별 실패의 영향과 재설계할 결정이 지정되어 있기 때문이다. 이번 검토에서 중요한 선택이 비어 있거나 상충하는데 F6로 미뤄 감춘 사례는 확인하지 못했다. 이 판단은 해당 선택의 실제 성공 가능성이나 현 VM에서의 설치 성공을 입증하지 않는다.

## Findings와 관측 한계

- P0/P1/P2의 중대한 actionable finding: 없음. 설계 정합성 범위에서 REVISE를 요구할 구체적인 반례를 확인하지 못했다.
- 전체 003 제품 PASS는 아니다. 15개 최종 정본의 문서 검토 PASS만 반환한다. 실제 AC 통과 수는 이 검토에서 증가하지 않았다.
- 원본 renderer 전체 bundle의 독립 역분석, 모든 210개 입력의 줄별 source audit, 외부 기술 문서의 실시간 검증, runtime 설치·namespace/UID/cgroup/Node SQLite API 실행, 저장 내구성/성능, native/브라우저/실제 모델/Q5는 수행하지 않았다.
- opcode별 구현 manifest, 실제 image/credential/resource profile 값, parser 및 race 집행은 후속 준비·구현 입력/검증 대상이다. 이 보고서가 그 값이나 동작을 대신 확정하지 않는다.
- 동결 사본에 대한 검토다. 이후 변경은 이 PASS의 자동 승계 대상이 아니다.
