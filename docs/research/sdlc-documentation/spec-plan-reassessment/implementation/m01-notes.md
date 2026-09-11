# M01 candidate implementation notes

2026-09-11. 설계 패키지 안의 합성 M01 예시만 개정했다. 제품 구현·활성 양식·설치·운영 전환은 수행하지 않았다.

## Changes

- [spec](../../spec-plan-design/candidate/examples/M01/spec.md): 현재 JSON 덮어쓰기 문제 → 단일 호스트·중지 허용 제약 →
  SQLite 선택과 JSON 잠금 대안의 실제 유지 비용 → 보고서 API 전환 → 대표 흐름·상세 정본 순으로 설명했다.
  기존 Upstream을 유지하고 같은 변경의 개정을 가리키는 Current change를 추가했다.
- [architecture](../../spec-plan-design/candidate/examples/M01/design/architecture.md): 기존 HTTP 계약과 미제공 범위를 직접
  연결하고, 완료 요청의 권한 검사부터 저장·응답·재조회·보고서까지 대표 흐름을 추가했다.
  첫 Mermaid에서 현재·전환 중·목표 및 단일 활성 저장소를 구별했다. 클래스의 논리 인터페이스와 배포 그림도 유지했다.
- [현재 입력 계약](../../spec-plan-design/candidate/examples/M01/inputs/current-contract.md) (new):
  `efa7339:.claude/skills/design-spec/examples/migration/context.md`의 관련 네 문단 묶음을 그대로 발췌했다.
  출처·합성 한계·미제공 오류 본문을 명시했다. [context](../../spec-plan-design/candidate/examples/M01/context.md)는
  직접 입력 경로와 제공된 가상 배치/명령을 설명하며 과거 입력은 출처 확인용으로 남겼다.
- [plan](../../spec-plan-design/candidate/examples/M01/plan.md): PR 인도 지도를 추가하고 A/B1/B2/B3/C1 작업마다
  목적·설계·파일·첫 행동 시험·명령·예상 실패·최소 변경·완료 증명을 모았다. C2의 실제 운영 입력은 Q4로 남기며
  문서 작성에 인위적 행동 RED를 요구하지 않는다. Proof는 전체 명령과 AC 증거 색인이다.

## Verification and preserved contracts

문서만 대상으로 일회성 읽기 점검을 실행했다. 새 검사기 파일은 추가하지 않았다.

```text
spec roles: 6; plan roles: 4
R1-R6 and AC1-AC8: unchanged from HEAD
design/storage.md, design/operations.md, intent.md: byte-unchanged from HEAD
verbatim input blocks against efa7339: 4
M01 local links and anchors: 41 resolved
git diff --check -- .../candidate/examples/M01: no errors
```

SQLite 스키마·연결·BEGIN IMMEDIATE·timeout=5 설정/HTTP 시간 구별·rollback·재시도 상한·내구성,
import/export·기존 출력 거부·source 보존은 storage 정본을 변경하지 않아 유지했다. 운영 정본도 변경하지 않아
최신 쓰기/불명 상태의 보존, 구 JSON writer 재개 금지, 실패 시 중지 유지가 남아 있다.
plan의 A/B 별도 branch/worktree와 경로 소유, 공유 문서 순차 조정, 계약 변경 재평가,
PR마다 최신 main 결합 및 머지 후 통합 확인도 유지했다. 모든 제품 Status는 draft다.

M01 런타임 시험은 실행하지 않았다. 이 제품은 존재하지 않으며 파일·명령·시험 이름은 공급된 합성 가정과 제안이다.
401/403/404 본문 바이트도 여전히 제공되지 않아 만들어 넣지 않았다. Q4와 운영 사본 리허설은 실제 적용 전 조건으로 남는다.

Mermaid 원본은 Markdown에 보존했다. PATH에 `mmdc`가 없어 이번 담당 범위에서 새 그림을 렌더링하지 않았다.
기존 `spec-plan-design/validation/diagrams/M01-*` 파생 이미지는 수정하지 않았으므로 새 첫 구성도의 검증 증거가 아니다.
상위 작업자가 필요하면 설계 패키지의 검증 산출물을 별도로 갱신한다.
