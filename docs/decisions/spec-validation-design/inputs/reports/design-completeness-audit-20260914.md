# 003 설계 충실도와 UML/도식 재검증

2026-09-14. 요청: “설계문서는 충실히 작성되었나 검증해줘. 어떤 UML등이 포함되었어?”
판정: **설계 보완 필요 — 주요 아키텍처는 충실하나 공통 계약 두 곳이 아직 완결되지 않았다.**

이번 검증은 현재 문서 자체와 채택한 양식/설계 깊이 지침을 대조했다. 과거 Astra PASS와 완료 선언은
이번 판정의 대체 근거로 사용하지 않았다. 이전 리뷰·closure는 당시 판정으로 보존한다. 현재 문서가
검토 이후 변한 탓에 생긴 지적은 아니다. 15개 입력은 final-design-r1의 실제 SHA와 모두 일치했다.
현재는 그 판에서 빠뜨렸던 보완점을 발견한 것이며, 앞선 “최종 설계 완성” 표현을 제한·정정한다.

## 범위와 방법

- root: 현재 spec이 연결한 설계의 역할, template 필수 절, R/AC 연결, 도식 code block 전수 목록,
  새 protocol과 lifecycle의 핵심 계약, 현재 파일 SHA를 직접 대조했다.
- 별도 새 문맥 `/root/design_completeness_audit`: spawn 도구 인자 `gpt-6-astra/high/fork_turns=none`.
  별도 backend telemetry는 제공되지 않았다. intent/spec 전체, 현재 설계 정본11개 전체와 초기 참고2개,
  프로젝트 정책과 관련 검토 기준을 읽고 아래 두 P2 지적을 반환했다. 정본을 작성·수정하지 않았다.
- 기존 [spec 양식](../../../templates/spec.md), [설계 깊이 지침](../../../examples/skills/design-spec/references/design-depth.md),
  [정책 검토 지침](../../../.agents/skills/spec-policy-pass/SKILL.md)을 적용했다. 이 지침은 UML 형식을
  강제하지 않으며 중요한 계약을 구체화하라고 요구한다. 그림 부재 자체를 정책 위반으로 판정하지 않았다.
- [기계적으로 확인한 목록](design-completeness-inventory-20260914.json): 15개 SHA 일치, R11개/AC13개,
  선언된 R→AC 연결 누락0/잘못된 R 참조0. 링크가 있다는 사실을 의미적 완전성으로 확대하지 않았다.
- 이번에 제품/Git/Node 시험·서비스/컨테이너 기동·브라우저·실제 모델을 실행하지 않았다.
  도식은 source/의미를 검토했으며 Mermaid 실제 렌더링·시각 배치·UML 규격 적합성을 검증하지 않았다.

## 충실하게 작성된 부분

| 영역 | 실제 확인한 내용 | 현재 한계 |
|---|---|---|
| 목표·범위·추적 | R1–R11, AC1–AC13, 단일 할당 컨테이너·원본 UI·002 분리, 주요 세 품질 | AC 연결은 의미 검토와 실제 실행을 대신하지 않음 |
| 대안·선택 | 논리/물리/복구/runtime/인증/저장/전송의 23개 주요 선택과 세 대안·비용·번복 조건 | 세 대안의 존재로 아래 누락이 없어지는 것은 아님 |
| 책임·권한 | B 업무 판정, X 실제 실행/상관, M lifecycle, work UID/제어 상태 분리 | 새 경계의 구체 API와 일부 전이는 아래에서 보완 |
| 실패·원자성 | M1–M7, H1–H5, 단발 소비/unknown, writer fence, 실제 종료, TOML CAS, 첨부 publication | 전체 engine-only 전이를 연결하는 계약 누락 |
| 자원·품질 | 합계 메모리/credit, 제어 예약, codec/large-I/O, 기존 부하·지연·메모리·정리 기준 | 실행 적합성/성능은 미검증 |
| 기존 코드 연결 | Files/Git/PTY 외 projectless/account/automation rollout의 목적지와 원본 저장소 경계 | 새 opcode manifest는 아직 정본 계약으로 제시되지 않음 |

## 수정이 필요한 발견

### F1 · P2 · 새 내부 protocol의 공통 인터페이스가 완결되지 않음

근거: [S8 34행](../design/protocol-and-resources.md#2-연결과-frame)의 header 필드·부분 필수조건과
[유한 port](../design/protocol-and-resources.md#6-유한-port와-경로), [coverage](../design/compatibility-coverage.md)의
새 opcode manifest 요구. 해당 파일의 34–48/140–158행은 “type별 schema”와 “build artifact”를 선언하지만
HELLO/BIND/ACK/CREDIT/CANCEL 등의 정확한 요청·응답, 필드별 타입/허용값/누락 의미, 상태별 허용과 오류가 없다.

반례: B와 X를 따로 구현하는 담당자가 HELLO→BIND 교환, 결과 조회, credit 반환의 body와 오류,
worktree/watch/PTY의 operation identity·event mapping을 서로 다르게 정해도 현재 설명 일부를 각각 만족할 수 있다.
원본 allowlist/wire2는 새 protocol1의 실제 타입 정의를 대신하지 않는다. 등록 없는 기능을 거절한다는 원칙만으로
지원 목록을 확정할 수 없다. 이 차이는 호환·identity·단발 effect·복구에 영향을 준다.

필요 보완:

1. type별 요청/응답 schema, 필수/선택·허용값·숫자/ID 표현과 크기, 허용 상태·오류/연결 종료 결과.
2. handshake/recovery, effect/result/query, credit, watch/PTY/blob의 유한 method 목록.
3. 원본 producer/consumer→B adapter→X method/event의 대응. 생성 artifact가 참조할 정본을 먼저 정의.

이것은 모든 내부 클래스·SQL DDL·파일명까지 지금 정하라는 요구가 아니다. 양쪽 구현이 공유할 중요한
인터페이스를 구현 과정에서 다시 설계하지 않도록 하자는 지적이다.

### F2 · P2 · engine 단독 종료/재시작의 전체 전이가 연결되지 않음

근거: [spec AC8](../spec.md#acceptance-criteria) 66행은 engine/container/gateway 각각 재시작을 요구한다.
[S9 장애표](../design/integration-and-verification.md#3-장애-결과-표) 73–83행에는 engine 단독 종료 행이 없다.
[S6 cold recovery](../design/runtime-lifecycle.md#5-명시적-cold-recovery와-실패-의미) 105–108행은 B/X process
또는 M 연속성 상실을 대상으로 한다. S8 20/35–36행은 engine generation을 pair/handshake에 고정한다.

반례: B/X/M은 살아 있고 독립 PTY가 실행 중인 상태에서 Codex app-server만 종료된다. 이전 engine의 실제
종료 확인, 과거 approval 무효화, unknown 보존 원칙은 이미 있다. 그러나 누가 어떤 명시적 요청으로 다음
engine을 기동하는지, pair/binding family/event cursor/credit을 어떻게 바꾸는지, 독립 PTY를 유지하는지 또는
전체 cold recovery를 요구하는지가 하나의 전이로 연결되어 있지 않다. 기존 로컬 종료 코드의 재사용만으로
새 원격 binding 전환을 결정할 수 없다.

필요 보완: engine-only 장애와 재시작의 상태/전이 계약을 추가한다. 기동 권위·종료 범위·새 generation/pair,
승인/미확정 요청/PTY/credit 처리, readiness 재개 조건과 금지 전이를 확정하고 AC8에 연결한다.
설계 선택이 필요한 경우 기존 사용자 지시대로 실질적인 세 대안을 비교한다. 이는 새 요구가 아니라 AC8의 상세화다.

## 실제 포함된 UML/도식

현재 정본의 Mermaid는 **4개: flowchart3개, sequenceDiagram1개**다. 초기 참고 architecture의 flowchart1개를
포함하면 전체5개다. intent에는 두 줄의 텍스트 구조 그림이 추가로 있다.

| 역할 | 파일/시작 줄 | 실제 표기 | 판독 |
|---|---|---|---|
| 논리 책임·의존 방향 | [foundation.md](../design/foundation.md#4-의존-방향), 55행 | flowchart LR | 컴포넌트/의존 뷰. 엄밀한 UML component 표기라고 부르지 않음 |
| 선택한 P1 배치·권한 경계 | [deployment-alternatives.md](../design/deployment-alternatives.md#4-p1-작업안의-배치와-금지되는-지름길), 75행 | flowchart LR + subgraph | 배치 뷰. UML deployment의 정식 node/artifact 표기 세트는 아님 |
| 최종 B/store/M/X/work 구성 | [integration-and-verification.md](../design/integration-and-verification.md#1-목표-topology와-의존-방향), 8행 | flowchart LR + subgraph | 최종 통합/실행 배치 뷰 |
| 메시지 수락 후 browser 응답 유실·조회 | [message-submission-flow.md](../design/message-submission-flow.md#3-정상-수락-뒤-브라우저-응답이-유실되는-순서), 43행 | sequenceDiagram | UML 계열 상호작용 시퀀스. 특정 한 시나리오이며 전체 장애 시퀀스는 아님 |
| 초기 배치 참고안 | [architecture.md](../design/architecture.md#2-배치와-권한), 26행 | flowchart LR + subgraph | 참고1개. 현재 정본 도식 수에 합치지 않음 |

`stateDiagram-v2`, `classDiagram`, `erDiagram`, 정식 UML activity/use-case/package 도식은 없다.
상태명·전이 규칙·데이터 관계 설명 자체가 모두 없다는 뜻은 아니다. 그 내용은 주로 문장과 표에 있다.
분류는 [Mermaid flowchart](https://mermaid.js.org/syntax/flowchart.html),
[sequence](https://mermaid.js.org/syntax/sequenceDiagram.html), [state](https://mermaid.js.org/syntax/stateDiagram.html)의
공식 표기와 현재 code block을 대조했다. Mermaid 사용과 UML 규격 적합성은 같은 판정이 아니다.

## 권장 보완 순서

1. **F2의 engine-only 전이와 상태표/상태도**: M/B/X/engine의 독립 수명과 새 실행 허용 조건을 명확히 한다.
2. **F1의 공통 interface/schema 목록**: 그림의 화살표가 가리키는 실제 계약을 닫는다.
3. **핵심 시퀀스 확장**: 최초 기동/grant, same-live pair 복구, 승인 응답 유실, cold recovery,
   TOML/첨부 publication의 성공·충돌·불명 분기를 표현한다. 이미 충분한 산문을 그림 때문에 재설계하지 않는다.
4. **논리 데이터 관계·주요 port 관계**: attempt/approval/queue/attachment/automation의 identity·관계·유일성,
   B/store/M/X의 제공/요구 interface를 표 또는 ER/컴포넌트 뷰로 연결한다. 내부 클래스 전수 그림은 우선순위가 낮다.

새로운 UML 의무·수치 점수·추가 제품 출시 기준을 만들지 않았다. 정본 설계·제품 코드를 이번에 수정하지 않았고,
검증 목록/이 보고/현재 실행 기록의 판정만 남긴다. 두 P2를 보완·재검토하기 전 현재 판을 완결된 상세 설계로
인계하지 않는다. runtime 설치·실제 격리·성능 시험의 미실행은 이 문서 보완과 별도의 확인 항목이다.
