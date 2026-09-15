# Plan: 보고서 호환과 저장소를 병렬 준비한 뒤 통합
Upstream: spec.md@23845b5. Status: draft.
Current change: 같은 변경의 spec·설계 정본 개정과 함께 읽는다. 기존 AC1–8을 유지하며 PR별 실행 정보를 모은 후보 개정이다.
합성 작성 예시. 사용자 허가 범위는 설계 패키지이며 제품 계획 승인/구현 성공이 아니다.
[spec](spec.md) → [현재 입력 계약](inputs/current-contract.md) → spec에 연결된 design/ 세 정본을 읽는다.
보고서와 비활성 SQLite 도구를 병렬 준비하고, 둘을 main에서 합친 뒤 선택·API 연결과 운영 전환을 준비한다.

[context](context.md)의 경로·Python 환경·시험 명령은 제공된 합성 가정이며, 아래 신규 파일과 시험 이름은 계획이다.
이 저장소에 M01 제품 코드가 있거나 명령을 실행해 성공했다는 뜻이 아니다. 실제 제품에 적용할 때 기존 코드·fixture·
실행 명령을 먼저 확인하고 경로가 달라지면 관련 구현 커밋에서 plan을 갱신한다. 미제공 오류 본문은 추측하지 않는다.
실제 운영 명령은 Q4 미확인이므로 코드 인계와 실제 전환의 준비 상태를 구분한다.
현재 인계: 아래는 미실행 합성 계획이다. 첫 인도 후보는 T01의 PR-A이며 T02–T04의 PR-B와 병렬 준비한다.
T05 이후 통합과 Q4·T06/T07 운영 검증은 남는다. SP/T는 같은 변경의 현재 정본을 가리키며 Upstream은 기존 입력 판이다.

## Files that change
| PR | 경로 | 변경 역할·설계 참조 |
|---|---|---|
| A | reports/nightly.py, tests/test_report.py | T01 · SP01 / R6: 기존 GET API로 전환·오류 노출 |
| B | service/sqlite_store.py (new), service/storage_errors.py (new), tools/migrate_store.py (new), tests/test_sqlite_store.py (new), tests/test_migrate_store.py (new) | T02–T04 · SP02/SP04/SP05/SP06: 저장·예외와 이행 도구 |
| C | service/store.py, service/api.py, config/service.toml, tests/test_api.py, tests/test_report.py, tests/test_cutover.py (new), docs/operations.md | T05/T06 · SP01/SP02/SP03/SP07: 선택·HTTP 연결·통합·운영 절차 |
service/json_store.py는 읽기 기준이다. 기존 함수/오류를 보존하는 연결로 충분하지 않다면 관련 설계/plan을 갱신한다.
문서 정본인 design/architecture.md·storage.md·operations.md와 spec/plan은 영향이 생길 때 해당 구현 커밋에 포함한다.

## Order of work
검증 방식: **혼합**. 데이터 유실·이행·복구 위험 때문에 A/B/C의 새 동작은 TDD를 선택한다.
이미 존재하는 JSON/API/인증 계약은 기존 테스트를 활용하고, 운영 문서는 계약 대조와 사본 리허설로 검증한다.
각 작업의 기대는 spec 집합과 보존한 원본 데이터가 정본이며, 새 구현 결과로 기대를 만들지 않는다.
공유 계약은 [architecture](design/architecture.md)의 facade/SQLiteStore/예외와
[storage](design/storage.md)의 스키마/트랜잭션/도구 CLI다. 이 판을 확인한 뒤 A/B는 같은 최신 main에서
각각 별도 branch/worktree로 진행할 수 있다. A는 reports/기존 report 시험, B는 신규 저장/도구 파일을 소유한다.
코드 경로는 겹치지 않지만 계획/공유 설계 문서가 겹치면 root 역할 엔지니어가 순차 조정한다.
각 담당자는 변경 이유와 문서 수정을 관련 구현 커밋에 포함하고 다른 branch 최신 문서를 덮어쓰지 않는다.

| 인도 단위 | 선행·병렬 | 머지 뒤 동작·공개 상태 | 남은 일 |
|---|---|---|---|
| PR-A 보고서 API 전환 | 고정 공유 계약 아래 B와 병렬 | 보고서는 기존 API 사용, 저장소는 JSON. 독립 공개 가능 | SQLite 선택·전체 전환 |
| PR-B 저장소·이행·복구 | 고정 공유 계약 아래 A와 병렬 | 어댑터·도구를 시험할 수 있고 기본 경로는 JSON | API 선택 연결·A와 통합 |
| PR-C 선택·API·운영 준비 | A/B 모두 main에 머지된 뒤 | JSON 기본의 배포 가능한 main, SQLite 명시 선택 가능 | Q4 해소·사본 리허설·실제 운영 전환 |
| 운영 전환 | 통합 검증, Q4, 사본 리허설 성공 | 운영 담당이 중지·대조 뒤 SQLite 쓰기 경로 재개 | 실패 시 operations의 중지·최신 데이터 보존·복구 |

### PR-A — 보고서 API 전환
<a id="t01"></a>
**T01 — 보고서 API 전환.** 설계: [SP01](design/architecture.md#sp01). 소속: PR-A.
**보고서가 활성 저장소의 값을 API로 읽게 한다.** 입력은 [현재 GET·읽기 계정 계약](inputs/current-contract.md)과
[architecture의 대표 흐름](design/architecture.md#representative-flow), spec R6/AC2/AC6다.
변경 파일은 기존 `reports/nightly.py`, `tests/test_report.py`이며 기준 회귀는
`tests/test_api.py`, `tests/test_json_store.py`를 읽는다. API·계정의 계약은 바꾸지 않는다.

먼저 기존 보고서와 같은 데이터의 고정 GET 성공 응답을 제공하고, 직접 JSON 읽기를 차단하는
`test_report_reads_api_without_json`을 `tests/test_report.py`에 추가한다.
`python3 -m unittest discover -s tests -p test_report.py -v`를 실행한다. 예상 RED는 현재 보고서가
JSON을 직접 읽으려 하거나 API 결과를 소비하지 않아 기대 결과를 내지 못하는 행동 실패다.
fixture·자격 설정·import 오류만으로 이 경로를 확인했다고 하지 않는다.

기존 읽기 계정과 HTTP 호출 경로로 GET 응답을 연결하는 최소 변경 후 같은 보고서 값으로 GREEN을 확인한다.
이어서 API 실패가 보고서 오류로 드러나고 옛 JSON으로 fallback하지 않는 시험을 먼저 추가하고 필요한 실패 처리를
구현한다. 이미 그 계약을 만족한다면 회귀로 기록하고 억지 실패를 만들지 않는다.

완료 증명 P-A는 같은 데이터의 기존 보고서 값 일치, JSON 직접 접근 없음, API 실패 노출과 기존 API/JSON 회귀다.
필요한 정리 후 Proof의 전체 명령을 최신 main과 결합한 판에서 실행하고, 머지 뒤 통합 main에서도 확인한다.
B가 미완성이어도 독립 공개 가능하며 저장소는 JSON 그대로다.

### PR-B — 비활성 저장소·이행·복구
#### B1 — 행 단위 완료와 저장 오류
<a id="t02"></a>
**T02.** 설계: [SP02](design/architecture.md#sp02), [SP04](design/storage.md#sp04), [SP05](design/storage.md#sp05). 소속: PR-B.

[architecture의 인터페이스·예외](design/architecture.md#저장-인터페이스와-오류)와
[storage의 데이터·트랜잭션](design/storage.md)을 사용한다. 새 `service/sqlite_store.py`,
`service/storage_errors.py`, `tests/test_sqlite_store.py`가 작업 범위다.

먼저 정본 스키마로 만든 시험 DB에서 `list_requests()`가 원순서의 dict들을 반환하고
`complete_request(id)`가 해당 status만 바꾸는 `test_complete_preserves_other_fields_and_order`를 작성한다.
`python3 -m unittest discover -s tests -p test_sqlite_store.py -v`로 확인한다. 신규 모듈 부재는 예정된
준비 실패로 구별하고, 최소 골격 후에는 미구현 호출이 행·값·순서 assertion을 만족하지 못하는 RED를 확인한다.
이 첫 행동을 통과시키는 최소 연결·목록·완료·예외 구현을 넣는다.

다음에는 서로 다른 실제 연결의 완료 구간을 동기화해 겹치게 하는 시험, 같은 ID 반복, 없는 ID,
잠금 보유 연결과 대기 상한·저장 실패·rollback 시험을 각각 구현 전에 추가한다.
thread를 시작했다는 사실이나 직렬 완료 결과는 경합 증거가 아니다. timeout=5 설정과 실패 관측을 확인하되
전체 HTTP 응답이 엄밀히 5초 안이라는 새로운 기대를 만들지 않는다. 최소 변경은 정본의 트랜잭션·연결 수명·예외 계약으로 제한한다.

완료 증명 P-B1은 겹친 두 완료 보존, 원래 필드·순서·타입, 반복 결과, 실패 후 부분 완료 없음과 예외 매핑이다.
이 작업의 통과로 API 연결이나 일반 사용이 끝났다고 표시하지 않는다.

#### B2 — 원본을 보존하는 import
<a id="t03"></a>
**T03.** 설계: [SP04](design/storage.md#sp04), [SP06](design/storage.md#sp06). 선행: T02. 소속: PR-B.

[storage의 import/export CLI 계약](design/storage.md#importexport-cli-계약)이 정본이다.
새 `tools/migrate_store.py`, `tests/test_migrate_store.py`에서 작업하며 B1의 스키마·어댑터를 사용한다.
먼저 정상 JSON을 새 target으로 import하는 `test_import_preserves_values_order_and_source`를 작성한다.
`python3 -m unittest discover -s tests -p test_migrate_store.py -v`를 실행한다. 기대는 rc0,
전체 키·값·순서 대조와 source 바이트 불변이다. 도구 부재는 준비 실패로 구별하고 CLI 골격을 마련한 뒤
미구현 import가 이 기대를 만족하지 못하는 RED를 확인한다. 제공되지 않은 stderr 바이트를 예상 출력으로 정하지 않는다.

최소 변경은 전체 검증 → 배타적인 새 target → 단일 트랜잭션 작성 → commit 후 재조회·대조다.
빈 배열, 중복 ID, 누락/unknown 키, 잘못된 status·타입·버전, source/target 동일, 기존 target,
중단 후 다른 새 target 재실행을 작은 사례로 시험 먼저 확장한다. 불리언/숫자 coercion을 허용하지 않는다.

완료 증명 P-B2는 AC3과 위 거부 사례, rc1·작업/오류 분류, 원본 불변과 실패 target의 비사용이다.
파일 존재만으로 성공을 판단하거나 실패 파일 자동 삭제를 전제로 재시도하지 않는다.

#### B3 — 최신 쓰기를 포함한 export
<a id="t04"></a>
**T04.** 설계: [SP04](design/storage.md#sp04), [SP06](design/storage.md#sp06), [SP07](design/operations.md#sp07). 선행: T02/T03, 동일 파일의 수정은 순차 진행. 소속: PR-B.

같은 `tools/migrate_store.py`, `tests/test_migrate_store.py`에 [storage의 export 계약](design/storage.md#importexport-cli-계약)을
연결한다. [operations의 복구 조건](design/operations.md)을 읽고 모든 writer를 멈춘 fixture에서 수행한다.
먼저 B1로 새 완료를 만든 뒤 export하는 `test_export_includes_latest_completion`을 작성한다.
`python3 -m unittest discover -s tests -p test_migrate_store.py -v`로 확인한다. 첫 기대는 새 JSON의
최신 전체 값·원순서와 rc0이며, B2만 있는 판의 미구현 export가 이를 만족하지 못하는 것이 예상 RED다.

최소 변경은 SQLite API의 일관된 읽기 트랜잭션, 버전·행·순서 검증, 새 파일 쓰기와 재대조다.
잘못된 user_version, 부분 실패, source/target 동일, 기존 출력 거부와 다른 새 target 재시도를 시험 먼저 확장한다.
원 JSON·DB·정상 export를 보존하고 구버전 list/complete 호환은 export의 별도 사본에서만 확인한다.

완료 증명 P-B3는 최신 완료를 포함한 값·순서, 실패 출력의 비사용과 정상 원본 보존, 사본의 구버전 호환이다.
JSON 호환 통과를 구 JSON writer의 서비스 재개 허가로 사용하지 않는다.

B 전체에서 필요한 리팩터링 후 Proof의 전체 명령을 최신 main과 결합한 판과 머지 뒤 통합 main에서 확인한다.
main의 기본 JSON을 바꾸지 않는다. 도구·어댑터·시험은 하나의 의미 있는 PR이며 개별 파일마다 PR로 나누지 않는다.

A/B의 독립성은 고정 계약에 한정된다. 계약 변경은 정본 spec 집합을 먼저 조정하고 관련 plan/작업 범위를 재평가한다.

### PR-C — 선택·API 연결과 전환 준비
A/B 둘 다 main에 머지된 뒤 최신 main에서 시작한다.

#### C1 — 시작 시 저장소 선택과 기존 API 연결
<a id="t05"></a>
**T05.** 설계: [SP01](design/architecture.md#sp01), [SP02](design/architecture.md#sp02), [SP03](design/architecture.md#sp03), [SP05](design/storage.md#sp05). 선행: PR-A/B 통합. 소속: PR-C.

[architecture의 배포·오류 계약](design/architecture.md)과 AC2/AC5/AC6/AC8이 기준이다.
기존 `service/store.py`, `service/api.py`, `config/service.toml`, `tests/test_api.py`, `tests/test_report.py`와
새 `tests/test_cutover.py`를 변경한다. `service/json_store.py`는 기존 동작의 읽기 기준이다.

먼저 `tests/test_cutover.py`에 정상 DB의 명시 sqlite 선택과 `test_sqlite_missing_db_refuses_start_without_creation`을
추가하고 `python3 -m unittest discover -s tests -p test_cutover.py -v`를 실행한다.
예상 RED는 A/B 판의 facade가 아직 SQLite 선택·시작 검증에 연결되지 않아 새 기대를 만족하지 못하는 것이다.
알 수 없는 backend·잘못된 스키마/버전·열기 실패도 시험 먼저 추가한 뒤, 최소 backend 선택과 시작 검증을 연결한다.
시작 실패에서 DB 비생성·JSON 자동 fallback 없음도 함께 판정한다.

이어 기존 `tests/test_api.py`의 같은 계약 사례를 두 backend로 실행하도록 확장하고
`python3 -m unittest discover -s tests -p test_api.py -v`로 확인한다. 미연결 SQLite 완료·404/503 경로의
행동 RED를 확인하고 facade/API 예외 매핑만 최소 연결한다. 이미 GREEN인 JSON·인증 회귀는 그대로 보존한다.
401/403/404 본문은 실제 적용 제품에서 확인한 기존 시험이 정본이며 합성 입력에서 새 바이트를 만들지 않는다.

완료 증명 P-C는 양 backend의 기존 정상/오류·권한·거부 무쓰기, 구성 실패의 시작 거부,
SQLite 동시성과 완료 후 API/보고서 일치, A/B의 이행·복구 시험이다.
`python3 -m unittest discover -s tests -p test_report.py -v`로 완료 후 보고서까지 확인하고 전체 명령을 실행한다.
JSON 기본을 유지하며, 같은 최신 main 결합 판과 머지 뒤 통합 main에서 A/B 전체를 다시 확인한다.

#### C2 — 실제 전환 절차의 운영 입력
<a id="t06"></a>
**T06.** 설계: [SP07](design/operations.md#sp07). 입력: SP07과 운영 담당의 Q4 답. 입력 수집·초안은 T05와 병행하고, 문서 확정 시 Q4와 대상 통합 판을 확인한다. 소속: PR-C의 운영 문서.

[operations 정본](design/operations.md)의 조건을 실행할 기존 `docs/operations.md`에 운영 담당과 함께
Q4의 실제 데이터 경로·권한·중지/재개/상태 확인 명령을 채운다. 첫 확인은 운영 담당이 제공한 명령으로
리허설 환경의 대상 프로세스·writer와 중지 상태를 식별하는 것이다. 아직 명령이 없으므로 여기에는 실행 결과나
예상 오류 문자열을 만들지 않는다. 문서 작성에 제품 행동 RED를 강제하지 않는다.

T06 완료 증명은 실제 경로·권한·중지/재개/상태 확인 명령과 사본 리허설 절차가 확인된 문서 인계다.
Q4가 없으면 T06은 미완료다. 리허설 실행과 운영 준비 판정은 T07에 남는다. 코드 PR은 그 미해소 운영 제한을 명시할 수 있다.
이 PR 뒤 main은 JSON 기본으로 배포 가능하고 선택 가능한 SQLite가 준비된다. 머지는 운영 전환이 아니다.

### 운영 전환/복구 — PR 이후 운영 담당 실행
<a id="t07"></a>
**T07.** 설계: [SP03](design/architecture.md#sp03), [SP06](design/storage.md#sp06), [SP07](design/operations.md#sp07). 선행: T05의 통합 검증 판과 T06의 확정 운영 문서. 사본 리허설을 먼저 수행하고 그 성공을 실제 전환의 진입 조건으로 삼는다. PR 이후 운영 인도이며 작업 ID가 PR 번호는 아니다.
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
PR 전체·통합 공통 명령은 `python3 -m unittest discover -s tests -v`다. 작업별 첫 시험·명령·기대는
Order of work의 해당 블록에 있고, 아래는 AC와 완료 증명의 색인이다. 모두 예정이며 실제 수치/성공이 아니다.
| ID·연결 | 기존/추가 대상 | 기대/확인 방법 |
|---|---|---|
| P-A T01 · AC2/6 | 기존 tests/test_report.py 확장 + 기존 API/JSON 시험 | 고정 API 결과와 기존 보고서 값 일치, JSON 접근 안 함, API 실패 노출 |
| P-B1 T02 · AC1/2/5 | 추가 test_sqlite_store.py | 서로 다른 연결의 완료 구간 겹침과 두 완료 보존, 반복/원순서/타입, 잠금 보유 연결과 timeout=5 설정·실패 관측, rollback |
| P-B2 T03 · AC3 | 추가 test_migrate_store.py import 사례 | 모든 키/값/순서, 빈/정상 배열, 중복/누락/unknown/타입/버전/target 기존 거부, 중단·새 target 재시도, source 바이트 불변 |
| P-B3 T04 · AC4 | 같은 파일 export 사례 | 새 완료 이후 최신 값/순서, user_version 오류/부분 실패·target 기존 거부, 복구 JSON 사본에서 구버전 호환 |
| P-C T05 · AC1–6/8 (코드 통합) | 추가 test_cutover.py + API/report 확장, A/B 전체 | 양 backend 기존200/401/403/404/503·거부 무쓰기, SQLite 동시성, 선택/DB 경로·스키마 실패 시 시작 거부·DB 비생성·fallback 없음, 완료 후 API와 보고서 일치 |
| 운영 T07 · AC7 (T06 문서 입력) | 운영/통합 담당의 실제 환경 사본 리허설 기록 | Q4 명령·판·상태·값/순서·새 완료 보존·중지/재개 근거. 미실행/실패면 전환하지 않음 |

PR마다 최신 main 결합과 통합 후 전체 시험을 확인한다. 코드 시험이 운영 상태/권한/중지를 증명하지 않는다.
실제 RED/GREEN과 사용한 판·명령·출력은 PR 기록에, 운영 결과는 기존 운영 기록에 남긴다.
