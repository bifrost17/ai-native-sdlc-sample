# Spec: 동시 완료 보존과 SQLite 이행
Upstream: intent.md@4a74823. Status: draft.
Skills applied: none（root가 고정 연구자료를 바탕으로 작성한 합성 예시）.
작성 권한: 사용자가 설계 패키지 작성을 허가했다. Upstream은 제작 입력이며 제품 수락을 뜻하지 않는다.

[입력](context.md). 기존 API를 보존하면서 저장소를 전환하고 보고서를 API 소비자로 바꾼다.
이 spec은 아래 문서 집합이 정본이다. 구현/리뷰 전에 모두 읽으며 plan도 같은 판을 참조한다.

| 설계 정본 | 소유하는 결정 |
|---|---|
| 이 파일 | 요구·AC·범위·질문·중요 우려 |
| [design/architecture.md](design/architecture.md) | 구성·배포 경계, 호출/권한/오류, 저장 인터페이스 |
| [design/storage.md](design/storage.md) | 데이터 스키마·원자성·동시성·import/export 계약 |
| [design/operations.md](design/operations.md) | 중지·전환·복구·재개 조건 |

중요 결정을 요약과 상세에 중복 정의하지 않는다. 예를 들어 저장 필드 제약의 정본은 storage.md다.
어느 문서만 바뀌어도 spec 집합 변경이며 관련 구현과 같은 커밋에서 영향받는 문서와 plan을 갱신한다.

## Requirements
| ID | 변경·보존 계약 | 근거 |
|---|---|---|
| R1 | 서로 다른 요청의 겹친 완료 결과 모두 보존, 반복 완료 멱등 | intent 문제 |
| R2 | API 정상/오류·권한, ID/필드/null/순서·기존 데이터 보존 | intent/현재 계약 |
| R3 | 중지 상태 전체 검증·원자 이행. 실패·중단은 원본 보존하고 재시도 가능 | Q2 |
| R4 | 전환 후 최신 쓰기를 포함해 복구, 안전한 쓰기 경로에서만 재개 | Q2 후속 답 |
| R5 | 기존 5초 경합 대기 상한·503 의미 유지, 내부 저장 오류 노출 금지 | 현재 계약 |
| R6 | 야간 보고서를 기존 읽기 계정/GET API로 전환, 옛 JSON fallback 없음 | Q1 후속 답 |

## Acceptance criteria
| ID → 요구 | 조건·행동 | 기대/불변식 |
|---|---|---|
| AC1 → R1 | 서로 다른 연결이 서로 다른 open ID를 실제 겹쳐 완료; 같은 ID 재시도 | 두 행 모두 done, 타 필드/순서 불변; 반복 결과 동일 |
| AC2 → R2 | 기존 목록·완료·인증·권한·없는 ID | 기존 200/401/403/404 계약, 거부 쓰기 없음. GET 200 {requests:[...]}·완료 200 해당 행 |
| AC3 → R3 | 정상/중복 ID/잘못된 타입·status·필드·버전/중단 입력 import | 정상은 모든 값·순서 동일. 오류는 실패·원본 불변·전환 없음; 새 출력으로 재실행 가능 |
| AC4 → R4 | 새 완료 뒤 또는 쓰기 여부 불명 상태에서 복구 export | 최신 값·순서를 가진 새 JSON; 기존 출력 덮어쓰기 없음. 안전 경로 미확인 시 중지 |
| AC5 → R5 | 잠금 경합·I/O 실패·저장 사용 불가 | 대기 상한 설정 5초 적용, 503 {error:temporarily_unavailable}; 부분 완료/내부 오류 노출 없음 |
| AC6 → R6 | JSON 기본/SQLite 선택 모두에서 API→보고서, API 실패 | 같은 데이터의 보고서 결과 유지, 실패를 오류로 보고하고 옛 JSON을 사용하지 않음 |
| AC7 → R3,R4 | 사본 전환/중단/복구 리허설 | 운영 정본의 단계별 중지 조건 준수, 최신 쓰기 대조 후에만 안전 경로 재개 |

## Design
[architecture](design/architecture.md)·[storage](design/storage.md)·[operations](design/operations.md)의
선택이 설계 본문이다. SQLite는 기존 단일 호스트에 들어오며 외부 서비스를 늘리지 않는다.
JSON 전체 쓰기를 잠금으로 보강하는 대안은 보고서 소비자와 이행/복구까지 다시 다뤄야 하므로
이번에는 트랜잭션 저장소를 택한다. 운영 중지와 이행 도구를 유지하는 비용을 감수한다.

## Constraints and scope
외부 서비스·계정·새 API·무중단/다중 호스트·추정 성능 목표 없음. 지원 status/필드의 정본은 storage다.
실제 운영 명령은 현재 미확인이다. 코드 설계 인계는 가능하지만 전환 전 해소해야 한다.

## Open questions
- Q1 answered: 보고서 1개, 다른 직접 writer 없음. 운영 담당의 합성 후속 답을 R6/구성도에 반영.
- Q2 answered: 중지·원본 보존·최신 쓰기 포함·안전한 경로에서만 재개. operations에 반영.
- Q3 answered: 단일 호스트 SQLite, 운영 담당 책임. 정확한 관리 명령은 Q4로 분리.
- Q4 carried forward: 실제 데이터 경로·권한·중지/재개/상태 확인 명령. 운영 담당이 PR-C의
  운영 문서 확정과 실제 전환 전에 확인. 저장/호환 설계를 바꾸지 않는 운영 입력이며 그 전에는 전환 금지.

## Flagged concerns
가장 큰 우려는 코드 revert로 옛 JSON writer를 재개해 다시 결과를 잃는 것이다.
operations의 중지 조건으로 다뤘다. 운영 담당이 Q4와 리허설 근거를 확인하기 전 운영 준비 완료를 주장하지 않는다.
