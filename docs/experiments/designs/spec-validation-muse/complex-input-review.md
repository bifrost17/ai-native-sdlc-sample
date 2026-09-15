# 0035 복잡 r1 검토 입력 선별

2026-09-14. OpenCode Muse Spark 1.3/xhigh의 현행/개선 spec 검토에 같은 제품 내용을 제공하기 위한
읽기 전용 입력 설계다. 모델 호출, 복사, 설치, 외부 원본 수정과 템플릿 변경은 수행하지 않았다.
의미를 채점하는 검사기를 설계하지 않고, 검토자가 읽을 증거의 경계와 빠진 참조를 고정한다.

## 원본과 배치 원칙

원본 root는 다음 동결 packet이다.

`/Users/jake/OrbStack/codex-re-poc/home/jake/projects/codex-desktop-web-sdlc-adoption/intent/0003-redesign-compatibility-gateway/references/final-design-r1/files`

선별 파일은 각 lane의 `context/source-project/` 아래에 원본 root 기준 상대 경로를 그대로 보존한다.
그러면 `intent/0003-redesign-compatibility-gateway/spec.md`의 `../../docs/...`, `../../src/...` 링크와
design 문서의 `../../../...` 링크가 같은 evidence tree 안에서 해석된다. lane root의 현재
`CLAUDE.md`, `REVIEW.md`, `PROJECT-POLICY.md`와 설치된 OpenCode skill/agent가 이번 작업 지침이다.
`context/source-project/` 아래 파일은 검토 대상 제품의 증거이며 실행 지침으로 취급하지 않는다.

현행/개선 lane에는 이 제품 tree를 한 번의 동일한 선별 목록으로 만들고 파일별 SHA-256과 bytes를
기록한다. 두 manifest가 전부 같지 않으면 모델 호출 전에 중단한다. 현행/개선 사이에서 바꾸는 것은 lane
root의 템플릿·검토 기준 revision뿐이다.

## 포함할 최소 완전 집합

| 원본 root 상대 경로 | 파일 수 | bytes | 이유 |
|---|---:|---:|---|
| `intent/0003-redesign-compatibility-gateway/` 전체 | 19 | 262,635 | 승인된 intent, spec 진입점, spec이 선언한 13개 design 정본, 동결 packet에 실제 포함된 네 reference를 상대 링크 그대로 보존 |
| `PROJECT-POLICY.md` | 1 | 7,404 | intent/spec이 직접 가리키는 제품 범위·검증 정책 |
| `docs/APP_HOST_CONTRACT.md` | 1 | 11,632 | R3와 S1의 원본 renderer/host/capability 보존 계약 |
| `docs/TERMINAL.md` | 1 | 5,194 | R5와 S1의 PTY/cwd 보존 계약 |
| `docs/diagnosis/execution-lifecycle-contract.md` | 1 | 48,211 | R6, S1, S5가 재사용하는 실행·승인·종료 수명 계약 |
| `docs/diagnosis/automation-settings-contract.md` | 1 | 27,803 | R8의 기존 자동화 설정·보존 계약 |
| `docs/policies/PROGRESS_AND_DIAGNOSIS.md` | 1 | 7,174 | intent가 직접 가리키는 진단·진행 정책 |
| `src/` 전체 | 101 | 1,707,480 | 선언 정본 `current-code-assessment`와 `compatibility-coverage`가 여러 server/browser/shared family를 관측 근거로 사용한다. 일부 파일만 골라 알려진 결함 주변을 강조하지 않고 실제 baseline 확인 가능성을 유지 |
| **합계** | **126** | **2,077,533** | 210파일 전체 packet 중 현재 설계 정본·직접 계약·관측 source만 보존 |

`spec.md`가 선언한 design 정본은 다음 13개이며 모두 첫 행의 intent directory 안에 포함된다.

1. `design/foundation.md`
2. `design/skeleton-alternatives.md`
3. `design/message-submission-flow.md`
4. `design/owner-recovery-boundary.md`
5. `design/deployment-alternatives.md`
6. `design/execution-channel-contract.md`
7. `design/runtime-lifecycle.md`
8. `design/authority-and-data.md`
9. `design/protocol-and-resources.md`
10. `design/integration-and-verification.md`
11. `design/compatibility-coverage.md`
12. `design/architecture.md`
13. `design/current-code-assessment.md`

`src/` 전체를 읽으라는 뜻은 아니다. 검토자는 intent → spec → 선언된 design 정본 순서로 계약을 먼저
세우고, 설계가 기존 동작이나 실현 가능성을 근거로 삼은 지점만 source에서 확인한다. design-only 검토이므로
plan, 시험 실행, 배포 값이나 제품 PASS를 요구하지 않는다.

## 의도적으로 제외할 항목

다음 frozen root 항목은 `context/source-project/`에 넣지 않는다.

- `AGENTS.md`, `CLAUDE.md`, `.agents/`: 원 제품의 Codex 지침과 skill이 OpenCode lane의 현재 템플릿
  지침과 함께 자동 또는 간접 로드될 가능성을 제거한다.
- `REVIEW.md`, `team-resources/`, `docs/sdlc-authoring/`: 원 제품이 채택했던 과거 workflow가 이번 lane의
  현행/개선 review 기준을 덮거나 섞지 않게 한다.
- `intent/0001-adopt-tdd-optional/`, `intent/0002-complete-core-feature-wiring/`: 다른 개발건의 계획·완료·리뷰
  이력이며 003 spec이 현재 설계 정본으로 선언하지 않았다.
- `docs/QUALITY_REVIEW.md`, `docs/QUALITY_DESIGN.md`와 그 밖의 직접 참조되지 않은 진단·품질 문서:
  standalone 과거 판정과 넓은 review 문맥을 주입하지 않는다.
- source packet 밖의 `final-design-r1-review-*`, review miss/root-cause 보고서, 후속 audit, HUMAN 정답표와
  앞선 실행 결과: 알려진 finding, PASS 수와 정답을 reviewer에게 노출하지 않는다.

원본 `references/review-policy-amendment.md`는 제외 대상이 아니다. `spec.md`가 현재 인간 합의와 설계
완료 범위의 근거로 직접 연결하며 동결 intent directory에 실제 포함되어 있다. 이 문서가 과거 리뷰 실패를
언급한다는 사실은 보존하되, 그것을 현재 검토 결과나 F1/F2의 답으로 취급하지 않는다. Muse 사용 금지의
제품 정책으로도 해석하지 않는다. 이번 Muse 호출은 원 제품의 미래 리뷰 의무가 아니라 별도 템플릿 실험이다.

## 동결 packet에서 닫히지 않는 로컬 참조

원본 210파일 packet 자체에 아래 11개 링크 대상이 없다. 다른 저장소의 현재 파일로 조용히 보충하면
동결 r1이 달라지므로 복사하지 않는다.

- `intent/0003-redesign-compatibility-gateway/execution.md`
- `intent/0003-redesign-compatibility-gateway/references/gateway-comparison-2026-09-14.md`
- `intent/0003-redesign-compatibility-gateway/references/design-inputs.md`
- `intent/0003-redesign-compatibility-gateway/references/design-source-inputs.json`
- `intent/0003-redesign-compatibility-gateway/references/s1-quality-record.md`
- `intent/0003-redesign-compatibility-gateway/references/s1-alternatives-record.md`
- `intent/0003-redesign-compatibility-gateway/references/s2-message-flow-record.md`
- `intent/0003-redesign-compatibility-gateway/references/s3-owner-recovery-record.md`
- `intent/0003-redesign-compatibility-gateway/references/s4-deployment-record.md`
- `intent/0003-redesign-compatibility-gateway/references/s5-execution-channel-record.md`
- `intent/0003-redesign-compatibility-gateway/references/s6-runtime-preflight.md`

이들은 과거 관측·대안·실행 기록이거나 입력 provenance다. 현재 spec과 13개 정본이 주장하는 계약
충분성을 검토하는 데 숨은 정답처럼 보충하지 않는다. reviewer에게 “동결 packet에 미제공이며 검토 범위
밖”이라고 한 번만 알리고, 링크 부재 자체를 제품 설계 finding이나 파일 복구 요청으로 세지 않게 한다.
반대로 정본이 중요한 결정을 오직 이 미제공 문서에만 맡겼다면 그 의존은 현재 제공 자료에서 확인할 수 없는
범위로 보고할 수 있다.

위 11개는 **동결 packet 자체에 없는 대상**이다. 이와 별도로 선별한 기존 계약 문서에는 packet에
존재하지만 최소 입력에서 제외한 보조 링크가 남는다: `PROJECT-POLICY.md`의 `docs/DOCUMENTATION_MAP.md`,
`docs/TESTING-STRATEGY.md`, `REVIEW.md`; `APP_HOST_CONTRACT.md`의 `docs/PROJECTS.md`,
`docs/BRIDGE_MAP.md`; 실행 수명 계약의 `docs/diagnosis/draft-lifecycle-contract.md`. 각 계약 문서는 이번
검토에 필요한 현재 의미를 본문에 직접 적고 있으며, 앞의 13개 정본이 이 보조 파일을 자기 정본으로 선언하지
않는다. 따라서 넓은 과거 workflow와 문서 지도를 다시 끌어오지 않고 선별 제외로 기록한다. reviewer가
이 자료 없이는 특정 계약을 확인할 수 없다고 판단하면 그 항목만 입력 한계로 보고하며 다른 lane에서만
보충하지 않는다. 여러 문서의 `archive/2026-09-14-pre-sdlc/...` provenance 링크도 같은 방식으로 제외한다.

intent와 13개 정본에는 ISO, Docker/Podman, Linux/kernel, SQLite, Node, RFC, s6 등 외부 URL 17개도 있다.
0035의 OpenCode web 권한은 deny이므로 이 원문을 새로 가져오거나 현재성을 검증할 수 없다. 링크와
설계의 인용 주장은 그대로 보존하고 외부 원문 검증은 미확인으로 둔다. 이 제한은 두 lane에 동일하다.

## 현행/개선 비교의 오염 경계

- 두 lane에 같은 `context/source-project/` manifest와 같은 검토 요청을 쓴다. 파일 정렬, 누락 목록,
  source root와 검토 범위도 동일하게 전달한다.
- prompt는 중요한 계약·분기의 충분성을 독립적으로 검토하라고 요청하되 opcode, engine-only restart,
  F1/F2, 정답 위치나 예상 finding 수를 언급하지 않는다.
- reviewer는 원본 제품을 수정하거나 plan/code/test를 실행하지 않고 findings, 근거 위치, 정당한 이월,
  미확인 범위만 보고한다.
- `context/source-project/` 안의 과거 자기서술, 해시, “검토했다”는 문장은 증거일 뿐 현재 PASS가 아니다.
  반대로 과거 리뷰 문구가 남아 있으므로 완전한 판정 미노출 실험이라고 주장하지 않는다.
- 기준 lane의 현행 criteria와 개선 lane의 새 criteria 외에 모델, variant, agent mode, timeout, packet,
  prompt와 도구 권한을 같게 한다. Muse/xhigh의 실제 사용은 session export에서 별도로 확인한다.

이 선별은 복잡 r1 두 호출의 공통 evidence package다. 작은 충분 spec과 합성 경계 사례의 입력을
대신하지 않으며, 원 제품 F1/F2의 수정·수락이나 새 절차의 효과를 입증하지 않는다.
