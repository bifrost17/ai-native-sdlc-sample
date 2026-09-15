# 0033 계획 실행 가능성·구현 발견 역추적 독립평가

## 평가 범위와 판

- 제품 저장소: `/Users/jake/Projects/ai-native-sdlc-codex-astra-20260913/f05-r01`
- 의도 수락판: `e1e06501e3bc13bfb09d7d6feb4da3fb12b8b953`
- spec·설계 수락판: `e9d52f8ad20fb09c912df2138ca4d939d621fad7`
- 계획 수락 원본: `e797fdcf31e7b5788d30f71dfe8318ae06381334`
- 현재 실행 결과 후보: `3ae564a1e6b8d2d4706d74456de731c76b351e68`
- 공개 HUMAN 근거: `/Users/jake/Projects/ai-native-sdlc-experiment-records/0033-codex-astra-medium/experiment-records/0033/human-decisions.md`
- 비교 기준: `tdd-optional/project/examples/skills/plan/references/execution-depth.md:7-54`, `tdd-optional/project/docs/GIT-WORKFLOW.md`, `tdd-optional/project/docs/PR-SIZE.md`, `tdd-optional/project/docs/RELEASE-CONTROL.md`

평가 대상은 계획 문서의 품질과 그 계획에서 현재 구현을 찾을 수 있는 정도다. 계획 작성 시점에 제품 시험이 실행됐는지와 계획이 시험을 충분히 정의했는지는 분리했다. `e797fdc`의 `plan.md:204-206`은 새 시험이 모두 예정 경로이며 당시에는 실행 가능한 제품 검증이 아니라고 명시한다. 따라서 계획 작성 단계에서 새 시험이 미실행된 사실은 문서 미작성이나 허위 통과로 판정하지 않았다. 현재 후보의 구현·시험 결과와 미완료 항목도 별도로 대조했다.

## 판정

**수락 당시 계획은 대화 없이 구현할 수 있을 만큼 구체적이며, 현재 코드와의 대응도 높다. 중대하거나 구현을 막는 계획 결함은 찾지 못했다.** 실제 경로와 책임, 인터페이스 정본, 직렬 PR의 선행 관계, 작업별 검증 방식과 독립 기대, 최신 main 통합, 기본 OFF 공개 제어가 하나의 인도 지도에 연결돼 있다. PR1과 PR2는 계획한 경계로 통합됐고 PR3는 계획의 미충족 검증 때문에 후보로만 보존됐다. 이는 계획이 실행 상태를 가려낸 사례이며 계획 실패가 아니다.

다만 현재 HEAD의 상태 문서에는 개발 호출 종료 뒤 HUMAN이 추가한 E18 결과가 계획·결정 기록의 마지막 상태 문단에 반영되지 않은 경미한 불일치가 있다. 수락 원본의 실행 가능성에는 영향을 주지 않지만, 재개자가 현재 계획만 읽으면 이미 확보한 네트워크 근거를 다시 기다릴 수 있다.

## 발견 사항

### DQ-PL-01 · 경미 · 현재 계획과 결정 기록이 E18의 HUMAN 네트워크 결과를 아직 “없음”으로 표시한다

**근거.** 현재 `intent/0001-shared-requests/plan.md:347-350`은 실제 HTTP 경합과 200행 OFF→ON→OFF 시험을 작성했지만 HUMAN 결과가 아직 없다고 한다. `intent/0001-shared-requests/decisions.md:138-143`도 실제 네트워크 결과가 남았다고 한다. 그러나 더 늦게 추가된 `intent/0001-shared-requests/execution.md:462-480`은 동일 26개 파일에서 전체 77개, 실제 두 PATCH의 200/409·겹침·최종 version 2, 200행 프로세스 흐름을 확인했고 E16–E17의 네트워크 결과 부재가 해소됐다고 기록한다. `README.md:49-54`와 `intent/README.md:3-6`도 E18을 현재 상태로 연결한다. 위 공개 HUMAN 근거의 `human-decisions.md:35-38`은 E18이 마지막 개발 호출 뒤 HUMAN이 추가한 기록이며 제품 코드·시험은 바뀌지 않았다고 확인한다.

**개발 영향.** 계획의 `plan.md:40-56`은 새 구현자가 plan·decisions·execution을 읽어 현재 판과 남은 일을 식별하도록 한다. 서로 다른 현재 상태가 남아 있으면 재개자가 이미 확보한 실제 HTTP·전체 77개 결과를 다시 요청하거나, 반대로 어떤 문서가 최신인지 별도 조사해야 한다. 실제로 남은 일은 네트워크 실행이 아니라 E18 `:477-480`의 no-op/실제 변경 전용 경합, 변경 저장소 쓰기 잠금 timeout, UPDATE 실패/영향 행 0 주입, 최신 검토와 HUMAN 통합 판단이다.

**최소 보완.** 과거 인계 문단 `plan.md:339-350`과 `decisions.md:138-143`은 당시 사실로 보존하되, 각각 바로 뒤에 “E18에서 동일 26개 파일의 77개/HUMAN 네트워크 결과가 연결되어 해당 대기는 해소됨; 다음 재개는 남은 세 전용 시험 묶음부터”라는 후속 상태 문단을 한 번 추가한다. PR3를 완료·수락·통합·공개로 바꾸면 안 된다.

## 수락 계획의 실행 가능성

| 항목 | 판정 | 문서와 구현의 구체적 대응 |
|---|---|---|
| 실제 파일과 책임 | 충족 | 수락 원본 `plan.md:9-29`은 `service.py`, `request_service/{config,model,service,storage,cli,http,csv_export}.py`, PR별 시험, 사용 문서와 실행 기록까지 AC에 연결한다. 세 PR diff에는 이 경로들이 실제로 나타난다. 현재 후보의 새 제품 파일과 시험 파일은 계획 목록과 일치한다. |
| 인터페이스 발견 가능성 | 충족 | 계획은 `spec.md`와 `design/{contracts,storage,openapi.json}`의 정확한 수락 SHA를 정본으로 고정한다(`plan.md:1-7`). CLI/HTTP/DTO/저장소 책임은 `design/storage.md:29-55`, wire·오류 계약은 `design/contracts.md:5-136`에 있다. 구현자는 인터페이스를 plan에서 재발명할 필요가 없다. 실제 `request_service/service.py:6-47`, `request_service/http.py:18-172`, `request_service/storage.py:16-157`가 그 경계를 따른다. |
| 작업·의존성 | 충족 | PR 지도 `plan.md:74-88`과 PR 상세 `:90-166`이 초기 가져오기 → GET/CSV → version PATCH를 직렬화하고 공유 파일 때문에 병렬화하지 않는 이유를 준다. 실제 시작점은 PR1 `3d6fcf1`, PR2 `ece1ed0`, PR3 `86cde36`이며 `execution.md:246-260`, `:356-369`가 앞 PR의 통합 tree 동일성을 확인한다. |
| PR 단위 | 충족 | 각 PR은 동작·시험·사용법·실행 기록을 함께 묶고, 머지 후 main에서 가능한 기능과 남은 범위를 구분한다(`plan.md:74-84,168-186`). 실제 PR1 `3f14410`/main `ece1ed0`, PR2 `d80fb87`/main `86cde36`은 각각 독립 수락됐고 PR3 `3ae564a`는 미수락 후보로 분리됐다. |
| 검증 기대 | 충족 | AC별 독립 기대와 시험 정본은 `plan.md:202-224`, 실제 명령은 `:226-270`에 있다. fixture 기대를 제품 코드로 계산하지 않고, 실제 SQLite·loopback·두 프로세스/두 연결·원본 바이트·명시 열 snapshot을 요구한다. 계획이 정한 미실행 처리도 “skip/파일 존재를 통과로 세지 않음”까지 명확하다. |
| 선택형 TDD | 충족 | 원자성·입력 거부·버전 불변성에는 TDD, CLI/HTTP/조회/CSV 연결에는 동작별 구현 후 시험, 기존 CLI에는 기존 시험 재사용을 선택하고 이유를 적었다(`plan.md:62-72,95-116,120-145`). 실제 PR1 RED→GREEN은 `execution.md:46-67`, PR3는 `:371-385`에 동작 assertion 실패와 같은 기대의 GREEN이 남아 있다. 이미 통과한 회귀와 import 오류를 RED로 소급하지 않았다. |
| 통합 | 충족 | 각 PR마다 최신 main 결합, 검토, 사람의 merge, merge tree 확인 후 다음 PR 시작을 요구한다(`plan.md:168-186`). 실제 기록은 PR1/PR2에서 이 순서를 충족했고, PR3는 남은 계획 항목 때문에 통합하지 않았다(`execution.md:444-460,477-480`). |
| 공개 | 대체로 충족 | 같은 `REQUEST_SERVICE_ENABLED=1`, 기본 OFF, PR별 시험 ON/일반 OFF, 사람의 최종 공개 결정, 재시작을 통한 ON/OFF와 데이터 보존이 연결돼 있다(`plan.md:74-84,161-166,273-282`). 최종 공개를 merge와 구분하고 PR3 후보를 공개하지 않았다. 현재 시제품 범위에서는 설정 위치가 프로세스 환경이고 담당자가 HUMAN임도 판독 가능하다. 플래그 제거는 별도 변경이라고 제한했으나(`:282`), 후속 별도 변경을 계획할 때는 `RELEASE-CONTROL.md:50-53`의 안정성 관찰·복구판 확인·제거 결정을 새 plan/spec에 구체화해야 한다. 현 PR3 완료의 선행 조건은 아니다. |

## 계획에서 현재 구현으로의 역추적

### PR1 — 초기 가져오기와 기본 OFF

- 계획: `plan.md:90-116`; 파일은 `request_service/{config,model,service,storage,cli,http}.py`, `tests/{test_config_model,test_import_storage,test_import_race,test_cli,test_http_base}.py`.
- 구현: 가져오기는 `request_service/storage.py:20-49`의 `BEGIN IMMEDIATE`·schema/행 확인·전체 삽입·COMMIT/ROLLBACK, guard는 `request_service/service.py:11-22`, HTTP OFF/health는 `request_service/http.py:67-120`에서 찾을 수 있다.
- 검증 대응: 실제 SQLite 실패 주입과 5초 잠금은 `tests/test_import_storage.py:68-124`, 두 독립 프로세스 barrier는 `tests/test_import_race.py:12-68`, 실제 loopback/CLI 서버 수명은 `tests/test_http_base.py:20-157`에 있다. `execution.md:36-150`은 계획한 TDD·연결 순서와 처음 bind 제한을 구분한다.
- 결과: 원본 후보가 준수하지 못한 HTTP 계약을 독립 검토가 발견하고 수정·재검증한 뒤 `3f14410`이 수락되어 main `ece1ed0`에 통합됐다(`execution.md:184-205,207-257`).

### PR2 — 공통 조회와 CSV

- 계획: `plan.md:118-138`; 조회 저장소 → GET → CSV, 각각 독립 기대와 비교.
- 구현: read-only 명시 열 조회는 `request_service/storage.py:96-133`, HTTP 목록·단건은 `request_service/http.py:76-114`, CSV serializer/CLI 연결은 `request_service/csv_export.py`와 `request_service/cli.py`에 있다. `tests/test_query_csv.py`, `tests/test_http_read.py`가 계획 경로 그대로 존재한다.
- 실행·통합: `execution.md:260-353`은 조회→GET→CSV의 구현 후 시험 순서, 비네트워크와 실제 TCP 근거의 차이, 미완료 상태를 남긴다. 이후 HUMAN 58개와 독립 관찰을 연결하고 `d80fb87`을 main `86cde36`에 통합했다(`execution.md:356-369`).

### PR3 — 버전 변경과 공개 단위

- 계획: `plan.md:140-166`; patch model/저장소 TDD, HTTP 연결 후 실제 두 연결 경합과 OFF→ON→OFF 전체 흐름.
- 구현: 입력 검증은 `request_service/model.py:106-127`, 원자적 변경과 버전/전이/no-op/상한/영향 행 확인은 `request_service/storage.py:52-94`, HTTP PATCH와 timeout 매핑은 `request_service/http.py:99-144`에 있다. 실제 두 연결 barrier는 `tests/test_http_race.py:12-60`, 200행 CLI 프로세스 흐름은 `tests/test_release.py:15-79`다.
- 계획 갱신: raw framing/MIME/JSON 사례를 `test_http_write`에 모으고 `test_http_protocol`은 지연 본문 timeout만 맡긴 배치 변화는 현재 `plan.md:341-345`에 이유와 함께 반영됐다. 파일명은 모두 유지되고 증명 기준은 삭제되지 않았다.
- 결과: TDD 과정과 구현 후 HTTP 검증을 구분했고(`execution.md:371-401`), 59개 비네트워크 검토와 이후 HUMAN 77개/216개 관찰을 확보했다. 그러나 계획한 세 전용 저장소/경합 시험과 최신 검토·사람 통합 판단이 남아 있어 `3ae564a`는 올바르게 미완료 후보로 보존됐다(`execution.md:444-480`).

## 구현 중 발견과 spec 갱신 필요성

**현재 후보까지 spec·세 설계 정본은 `e9d52f8`과 바이트상 동일하며, 그 상태가 누락을 만들었다고 볼 만한 새 제품 계약 결정은 찾지 못했다.** 다음 발견은 모두 수락 계약을 바꾸지 않는 정당한 구현/시험 재량이다.

| 구현 발견 | 기존 정본 | 실제 반영 | 분류와 문서 처리 |
|---|---|---|---|
| 초기 파싱 오류·HTTP/0.9에서 상태선/필수 헤더가 빠짐 | 모든 HTTP 응답은 HTTP/1.0과 고정 헤더를 포함한다(`design/contracts.md:40-45`); 구문 불가 요청은 400이다(`:72-75`). | `request_service/http.py:25-31,41-62`, `tests/test_http_base.py:106-212`; 발견·수정은 `execution.md:184-220`. | **기존 계약 위반 수정.** 새 외부 동작 결정이 아니므로 spec 갱신 불필요. plan에 영향 경로·검증 변화가 `plan.md:312-317`로 반영됐다. |
| 표준 파서가 `//health`를 `/health`로 정규화 | health만 OFF 예외이며 알 수 없는 경로는 404, OFF 업무 경계는 503이다(`design/contracts.md:72-80`). | 원본 request-target 복원 `request_service/http.py:25-31`; raw 회귀 `tests/test_http_base.py:160-212`. | **기존 경로·우선순위 계약 준수 방법.** spec 변경이 아니라 구현 재량이다. |
| Python 3.9에서 `socket.timeout`과 `TimeoutError` 관계가 기대와 다름 | 5초 미완독은 408 request_timeout이며 DB 미접근(`design/contracts.md:87-88`). | 두 예외 catch `request_service/http.py:138-143`, 영구 매핑 시험 `tests/test_http_write.py:105-117`, 근거 `execution.md:398-401`. | **지원 환경 호환 보완.** 외부 오류 계약·timeout 값은 그대로이므로 spec 갱신 불필요. |
| 실제 동시성의 barrier와 공통 monotonic 관측 | AC8/9는 실제 동시 구간과 최종 행을 요구한다(`spec.md:38-39,48-50`). | 가져오기 `tests/test_import_race.py:12-68`, PATCH `tests/test_http_race.py:12-60`; 계획 보충 `plan.md:295-299`. | **증명 방법 구체화.** repository/SQLite를 대체하지 않는 harness 선택이며 plan 대상이다. 이미 반영됨. |
| PR3 protocol 사례의 시험 파일 배치 변경 | 계획 원본은 protocol 사례를 `test_http_protocol` 중심으로 배치했다(`plan.md@e797fdc:152-155,218,241-243`). | 공통 wire 사례는 `tests/test_http_write.py:22-139`, 실제 지연 본문만 `tests/test_http_protocol.py:9-28`; 현재 plan `:341-345`. | **시험 정본 배치 변경.** 계약은 동일하고 plan에 이유가 반영됐으므로 spec 편집은 불필요. |

중요한 결정이라면 API/출력/오류/스키마·공개 계약을 바꾸므로 spec·설계와 영향 plan을 함께 갱신해야 한다(`execution-depth.md:40-46`). 이번 구현은 공개 명령, JSON/CSV 형식, 오류 코드·우선순위, SQLite schema, 버전 규칙, release flag를 바꾸지 않았다. 반대로 no-op/실제 변경 경합이나 UPDATE 실패 주입을 아직 작성하지 않은 것은 새 계약 결정이 아니라 수락 plan의 미완료 검증이다. 이를 spec 누락으로 바꾸거나, 현재 77/216 결과로 자동 충족시켜서는 안 된다.

## 생성 당시 문서와 현재 후보의 구분

- `e797fdc`는 제품 코드가 없던 시점의 **수락된 실행 계획 원본**이다. `plan.md:204-206`의 “만들 예정·아직 실행 가능하지 않음”은 정확하다. 계획의 구체성을 평가할 때 이후 시험 결과를 소급해 넣지 않았다.
- 현재 plan의 `:284-350`은 PR별 구현 인계와 계획 변화의 후속 기록이다. PR1/PR2의 실제 통합과 PR3 시험 배치 변화를 찾는 데 충분하다.
- `3ae564a`는 **현재 실행 결과 후보**이며 PR3 수락·main 통합·공개판이 아니다. 제품 main은 `86cde36`이고, PR3 후보가 계획한 모든 검증을 마치지 않았다는 상태는 `execution.md:444-480`에서 일관되게 보존된다.
- 의도 문서의 `intent.md:61-65`와 계획 상단 `plan.md:4-7`의 draft·당시 미수락 문구는 단계 생성 당시 상태다. 현재 D1–D3 수락은 `decisions.md:34-73`에 실제 SHA와 범위로 기록되고 plan `:42-46,284-288`이 그 해석·재개 절차를 명시하므로, 이를 무수락 구현으로 판정하지 않았다.

## 최소 후속 조치

1. DQ-PL-01의 후속 상태 문단만 plan·decisions에 추가해 E18과 재개 순서를 연결한다.
2. PR3를 계속할 때 `execution.md:477-480`의 세 전용 시험 묶음을 작성·실행하고, 바뀐 코드/시험 범위를 최신 독립 검토한 뒤 HUMAN이 통합 여부를 판단한다.
3. 그 과정에서 계약이 그대로면 spec 네 파일은 형식적으로 편집하지 않는다. API·오류·스키마·공개 조건이 실제로 달라질 때만 수락 절차와 함께 갱신한다.
