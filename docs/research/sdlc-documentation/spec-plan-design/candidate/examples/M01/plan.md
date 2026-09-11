# Plan: 보고서 호환과 저장소를 병렬 준비한 뒤 통합
Upstream: spec.md@23845b5. Status: draft.
합성 작성 예시. 사용자 허가 범위는 설계 패키지이며 제품 계획 승인/구현 성공이 아니다.
[spec](spec.md)와 [입력](context.md)을 함께 읽는다. 모든 시험은 예정이며 이름은 추가 계획이다.

[spec의 정본 목록](spec.md)에 있는 design/ 세 문서를 모두 읽는다. 구체 경로는 가상 배치/신규 설계이며
실제 운영 명령은 Q4 미확인이다. 코드 인계와 실제 전환의 준비 상태를 구분한다.

## Files that change
| PR | 경로 | 변경 역할·설계 참조 |
|---|---|---|
| A | reports/nightly.py, tests/test_report.py | 기존 GET API로 전환·오류 노출, architecture/R6 |
| B | service/sqlite_store.py (new), service/storage_errors.py (new), tools/migrate_store.py (new), tests/test_sqlite_store.py (new), tests/test_migrate_store.py (new) | SQLite 클래스·예외, import/export와 시험, architecture/storage |
| C | service/store.py, service/api.py, config/service.toml, tests/test_api.py, tests/test_report.py, tests/test_cutover.py (new), docs/operations.md | 선택/HTTP 예외 연결·통합·실제 전환 절차 |
service/json_store.py는 읽기 기준이다. 기존 함수/오류를 보존하는 연결로 충분하지 않다면 관련 설계/plan을 갱신한다.
문서 정본인 design/architecture.md·storage.md·operations.md와 spec/plan은 영향이 생길 때 해당 구현 커밋에 포함한다.

## Order of work
공유 계약은 [architecture](design/architecture.md)의 facade/SQLiteStore/예외와
[storage](design/storage.md)의 스키마/트랜잭션/도구 CLI다. 이 판을 확인한 뒤 A/B는 같은 최신 main에서
각각 별도 branch/worktree로 진행할 수 있다. A는 reports/기존 report 시험, B는 신규 저장/도구 파일을 소유한다.
코드 경로는 겹치지 않지만 계획/공유 설계 문서가 겹치면 root 역할 엔지니어가 순차 조정한다.
각 담당자는 변경 이유와 문서 수정을 관련 구현 커밋에 포함하고 다른 branch 최신 문서를 덮어쓰지 않는다.

### PR-A — 보고서 API 전환
1. 기준 API/JSON/report 시험을 확인한다. tests/test_report.py에 API 응답을 소비한다는 시험을 먼저
   작성한다. 고정 HTTP 응답을 주고 직접 JSON 읽기를 관찰/차단해 기존 파일 읽기 경로에서 예상 RED 확인.
2. 기존 계정/GET 호출 경로로 최소 연결해 GREEN. API 실패는 오류를 드러내며 stale JSON fallback
   하지 않는 시험을 선행하고 필요한 동작을 구현한다. 같은 데이터의 기존 보고서 결과를 비교한다.
3. 정리/전체·최신 main 결합/통합 main 검증. 이 PR은 독립 공개 가능하며 저장소는 JSON 그대로다. P-A.
B가 미완성이어도 A는 동작한다. 새로운 계정을 만들거나 API 계약을 바꾸지 않는다.

### PR-B — 비활성 저장소·이행·복구
1. tests/test_sqlite_store.py에서 목록/완료 인터페이스 시험을 먼저 작성한다. 신규 모듈 부재는 계획된
   미구현 실패인지 확인하고 모듈 골격 후 행동 assertions로 RED를 확인한다.
   최소 구현 뒤 실제 두 연결을 동기화해 겹친 완료·반복·잠금 상한/오류 시험을 먼저 설계·실행한다.
   thread 실행만 하고 직렬 완료된 결과를 동시성 증거로 쓰지 않는다. P-B1.
2. tests/test_migrate_store.py에서 정상 import CLI 기대 rc0/전체 값/순서 시험 선행 → 최소 도구 구현.
   중복·키·타입·버전·기존 target·중단의 동작을 작은 사례로 먼저 검증하고 구현한다. P-B2.
3. 새 완료 후 export/원본 불변/부분 실패/기존 출력 거부 시험 선행 → 최소 export와 대조. P-B3.
4. 필요한 리팩터링 후 전체·최신 main 결합/통합 검증. main의 기본 JSON을 바꾸지 않는다.
   도구/어댑터/시험은 하나의 의미 있는 PR이며 개별 파일마다 PR로 나누지 않는다.

A/B의 독립성은 고정 계약에 한정된다. 계약 변경은 정본 spec 집합을 먼저 조정하고 관련 plan/작업 범위를 재평가한다.

### PR-C — 선택·API 연결과 전환 준비
A/B 둘 다 main에 머지된 뒤 최신 main에서 시작한다.
1. tests/test_cutover.py에 명시 sqlite 선택·알 수 없는 backend 실패 시험을 먼저 추가한다.
   tests/test_api.py의 같은 계약 시험을 두 backend에 적용하도록 확장하고 예상 미연결 RED 확인.
2. store.py의 backend 선택과 api.py의 404/503 매핑을 연결한다. JSON 기본 유지, 자동 fallback 없음.
   구성/권한/완료 후 보고서·복구 경로 시험 P-C를 확인하고 필요한 정리 뒤 전체 검증.
3. 운영 담당과 Q4의 실제 경로·권한·중지/재개/상태 확인 명령을 docs/operations.md에 채운다.
   이 정보가 없으면 운영 준비 완료라고 표시하지 않는다. 코드 PR은 미해소 운영 제한을 명시할 수 있다.
4. 같은 최신 main 통합 판에서 API/보고서 양 backend와 B의 시험을 모두 확인한다.
   main은 JSON 기본으로 배포 가능, 선택 가능한 SQLite가 준비됨. 머지가 운영 전환은 아니다.

### 운영 전환/복구 — PR 이후 운영 담당 실행
[operations 정본](design/operations.md)의 조건을 실제 운영 문서와 연결한다.
사본 리허설: 실제 중지 명령/상태 확인 → writer 없음 확인 → 원본 보존 → 새 DB import → 전체 값·순서 비교
→ 선택 sqlite → API/권한/완료·재조회·보고서·최신 export/복구 확인 → 안전 쓰기 경로 재개 판단을 기록한다.
합의한 리허설이 성공하고 Q4가 해소된 뒤 실제 중지·보존·import·대조·설정 전환·재개를 운영 담당이 수행한다.
전환 실패는 즉시 중지 유지. 쓰기 이후/불명에는 최신 export를 보존하고 안전한 SQLite 경로를 복구한다.
구 JSON writer 서비스 재개로 돌아가지 않는다. 도구 예:
`python3 tools/migrate_store.py import --source <보존한.json> --target <새.db>`,
`python3 tools/migrate_store.py export --source <현재.db> --target <새복구.json>`.
Q4의 실제 호스트 명령은 여기서 발명하지 않는다.

## Risks
가장 위험한 부분은 C 뒤 전환/복구와 unknown writer다. 잘못된 DB/타입/잠금·부분 target을 정상으로
오인하지 않도록 P-B2/B3/C와 사본 리허설로 확인한다. 실패는 원본/최신 DB 보존·중지로 대응한다.
구버전 호환 시험은 복구 JSON 사본만 변경한다. Git revert는 최신 데이터와 안전한 동시 쓰기를 보장하지 않는다.
영구 이중 쓰기는 경합/복구 복잡성을 늘리므로 택하지 않았다. 순수 리팩터링/이미 만족한 계약에 억지 RED는 만들지 않는다.

## Proof
기본 명령 `python3 -m unittest discover -s tests -v`. 아래는 예정 증명이며 실제 수치/성공이 아니다.
| ID·연결 | 기존/추가 대상 | 기대/확인 방법 |
|---|---|---|
| P-A AC2/6 | 기존 tests/test_report.py 확장 + 기존 API/JSON 시험 | 고정 API 결과와 기존 보고서 값 일치, JSON 접근 안 함, API 실패 노출 |
| P-B1 AC1/2/5 | 추가 test_sqlite_store.py | 서로 다른 연결의 완료 구간 겹침과 두 완료 보존, 반복/원순서/타입, 잠금 보유 연결과 timeout=5 설정·실패 관측, rollback |
| P-B2 AC3 | 추가 test_migrate_store.py import 사례 | 모든 키/값/순서, 빈/정상 배열, 중복/누락/unknown/타입/버전/target 기존 거부, 중단·새 target 재시도, source 바이트 불변 |
| P-B3 AC4 | 같은 파일 export 사례 | 새 완료 이후 최신 값/순서, user_version 오류/부분 실패·target 기존 거부, 복구 JSON 사본에서 구버전 호환 |
| P-C AC1–7 | 추가 test_cutover.py + API/report 확장, A/B 전체 | 양 backend 기존200/401/403/404/503·거부 무쓰기, SQLite 동시성, 선택 실패 자동 fallback 없음, 완료 후 API와 보고서 일치 |
| 운영 AC7 | 운영/통합 담당의 실제 환경 사본 리허설 기록 | Q4 명령·판·상태·값/순서·새 완료 보존·중지/재개 근거. 미실행/실패면 전환하지 않음 |

PR마다 최신 main 결합과 통합 후 전체 시험을 확인한다. 코드 시험이 운영 상태/권한/중지를 증명하지 않는다.
실제 RED/GREEN과 사용한 판·명령·출력은 PR 기록에, 운영 결과는 기존 운영 기록에 남긴다.
