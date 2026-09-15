# 검증·실행 기록

이 파일은 실제 관측을 기록한다. 예정 작업과 명령은 plan.md가 정본이다.

## E1 — plan 작성 중 기존 코드 기준 확인

- 대상 HEAD: `e9d52f8ad20fb09c912df2138ca4d939d621fad7`.
- 기존 제품 파일: tracker.py, requests.json, tests/test_tracker.py. 이번 작업은 plan·decisions·이 기록의 문서 변경뿐이다.
- 환경: python3 3.9.6, sqlite3.sqlite_version 3.43.2. 로컬 main은 `dcc6663a266cda8c342d609a5f715bda84507c5a`,
  작업 브랜치는 `codex/0033-design`이었다. 이후 세션에서는 현재 판을 다시 확인한다.
- 실행: `python3 -m unittest discover -s tests -v`.
- 실제 결과: 종료 0, 기존 3개 테스트 모두 OK. 목록의 파일 순서·읽기 불변, 단건/없는 ID,
  대상만 완료 변경·반복 완료를 검사했다. 실행 중 임시 JSON 복사본을 사용했다.
- 한계: 새 저장소/API/CSV 코드와 새 시험은 아직 없다. 기존 세 테스트 통과는 새 기능·ON/OFF·동시성의 증거가 아니다.
  이번에는 loopback 실행을 시도하지 않았으며 제약이 실제 발생했다고 주장하지 않는다.
- Git stage/commit/merge·제품 구현은 하지 않았다. D1/D2 수락 원문은 유지했다.

## 구현 시 이어 기록할 항목

각 PR의 기준 main/작업 SHA와 미커밋 변경, 수행 AC, 명령·기대 출처·실제 결과를 기록한다.
TDD 선택 범위는 의미 있는 RED 이유와 같은 기대의 GREEN을, 구현 후 테스트 범위는 실제 구현·검증 순서를 남긴다.
환경 실패·미실행·사용자 실행은 구분한다. AC8/9의 겹침 근거와 각 응답·최종 상태를 보존한다.
독립 검토 결과·수정 후 확인·결합 main과 실제 머지 판의 동일성/재검증도 기록한다.
사람의 수락·통합·공개 결정은 decisions.md에 연결한다. 이 절은 기록 양식이며 실행 결과가 아니다.

## E2 — plan 제출 전 문서 확인

- 대상: plan.md, decisions.md, execution.md의 이번 문서 변경.
- `git diff --check` 통과. 새 파일은 별도로 행 끝 공백·양식 자리표시자·상대 링크를 Python으로 확인했다.
- D1의 intent/정책 두 파일과 D2의 spec 정본 네 파일을 각 수락 커밋의 바이트와 대조해 일치함을 확인했다.
  OpenAPI JSON 파싱도 성공했다.
- 작성자가 AC1–16과 Proof/PR별 작업, TDD·구현 후 테스트 경계, 일반 OFF/시험 ON,
  사람의 Git·loopback 대행 및 새 세션의 수락 확인 절차를 대조했다.
- 신규 제품 시험·독립 구현 검토는 실행하지 않았다. E1의 기존 세 테스트 외 제품 동작 통과 주장은 없다.

## E3 — PR1 기준과 구현 중 검증

시작 HEAD와 로컬 main은 모두 `3d6fcf1eb46111ca7ffdb1b68aa2ba13ad6aab34`,
브랜치는 `codex/shared-requests-import`, 작업 트리는 깨끗했다. D1의 intent/정책, D2의 spec·선언된
세 설계 파일, D3의 plan을 해당 수락 SHA와 `git diff`로 대조해 차이 없음을 확인했다.
문서의 과거 draft/대기 표현과 D1–D3의 수락은 구별했다. 현재 구현은 그 main 위 미커밋 변경이다.

`python3 -m unittest discover -s tests -v`로 시작 판의 기존 3개 시험 OK(종료 0)를 확인했다.
tracker.py, requests.json, tests/test_tracker.py는 수정하지 않았다.

### TDD와 동작별 연결

기대는 spec AC1–3/9/11/13과 storage/contracts에서 정했다. `tests/support.py`의 명시 5열 기대·SQL
스키마는 제품 함수에서 계산하지 않는다. 실제 실행한 순서는 다음과 같다.

| 범위·명령 | 관측한 RED | 같은 기대의 GREEN 또는 회귀 |
|---|---|---|
| tests.test_config_model.ConfigTests | import 가능한 flag 뼈대가 정확한 1에도 False여서 assertion 실패 | 환경 판정 추가 후 1개 OK |
| tests.test_config_model.ImportModelTests | 빈 결과 뼈대에서 원문 목록 불일치 및 부적합 입력 미거부, 36 failure | 엄격 JSON/필드 검증 후 2개 OK |
| tests.test_config_model.GuardTests | OFF import가 오류를 내지 않음 | guard 추가 후 해당 1개 OK |
| 같은 GuardTests | 입력 실패·잘못된 전체 JSON을 거부하지 않음, 2 failure | guard→파일→전체 검증→repository 순서 연결 후 3개 OK |
| tests.test_import_storage의 전체 가져오기 | 저장소 뼈대 반환 0, 기대 5 assertion 실패 | 실제 BEGIN IMMEDIATE/전체 삽입/COMMIT 후 1개 OK |
| 같은 모듈의 반복 거부 | store_not_empty 대신 store_unavailable | 잠금 안의 기존 행 확인 후 전체 2개 OK |
| 같은 모듈의 스키마 거부 | 미지원 버전·CHECK/열/객체 등 10개 사례 미거부 | 스키마 검사 추가 후 당시 전체 5개 OK |
| sqlite_prefix_lookalike 시험 | LIKE의 `_` wildcard 때문에 sqliteX_private 테이블을 내부 객체로 오인 | literal 접두어 GLOB 검사로 수정 후 통과 |

사용한 명령은 각 행의 `python3 -m unittest -v <모듈/클래스/시험>`이다. TDD의 실패는 문법/import 오류가
아닌 동작 assertion이었다. 롤백 주입·잠금·특수 경로·원문 왕복·입력 후반 오류 등 추가 사례는 처음부터
통과했으므로 RED라고 보고하지 않는다. 생성 뒤 user_version 단계, 세 번째 INSERT, COMMIT 직전에
실제 SQLite 연결 wrapper로 오류를 주입했다. 새/기존 빈 DB 모두 user_version=0·테이블 없음으로 롤백했다.
기존 유효 빈 스키마·0바이트·빈 SQLite 가져오기도 확인했다. 별도 쓰기 잠금을 5초 유지하면 store_busy다.

CLI는 구현 후 test_cli를 작성·실행해 당시 6개 OK를 확인했다. 성공 JSON/LF·오류 stdout 비움·종료 코드,
중복/미지원 인자·포트 범위, OFF 파일 미접근, help, 출력 연결 실패 후 이미 커밋한 행 보존을 확인했다.
기존 CLI는 flag 미설정/0/1에서 독립적으로 정한 전체 탭 출력·파일 순서·null 표기·없는 ID·대상만 완료·반복 완료와 대조했다.
HTTP는 그다음 구현·시험했으며 실제 환경 실패는 E4에 별도로 기록한다. 이후 두 실제 프로세스 가져오기
시험을 연결했다. 모듈 import 부수 효과와 DB 연결 오류 비노출도 회귀로 보강했다.

### 실제 경합 (AC9)

두 자식이 RequestService.import_json에 들어가 입력을 읽고 검증한 뒤 repository 진입 barrier에서 대기했다.
부모가 두 ready를 모두 확인한 뒤 해제했다. SQLite 연결·스키마·검사·삽입·커밋은 실제 구현을 실행했다.
초기 시험의 자식 monotonic 수치 직접 비교는 macOS Python 3.9의 공통 원점을 보장하지 않아 최종 증거로
쓰지 않는다. 부모의 한 시계와 barrier를 사용하도록 시험 기록을 보강한 후 다시 통과했다.

2026-09-13 UTC 관측 예: PID 26859는 04:56:35.179137→04:56:35.181658, imported=5;
PID 26860은 04:56:35.179118→04:56:35.183063, store_not_empty였다.
부모 ready ns는 5535009125/5535047333, 완료 관측 ns는 5541936208/5543349875,
관측 구간 교집합은 6888875ns다. barrier에서 둘 다 완료 전 실행 중임을 확인했으며 이 시간은 SQLite 성능 수치가 아니다.
최종 행은 support.EXPECTED의 R-201…R-205 다섯 행과 version=1이며 원본 JSON 바이트도 불변이었다.
시험은 매 실행 UTC·구간·결과·최종 5열을 stdout에 출력한다. 이는 합성 개발 검증 자료이며 제품 운영 로그가 아니다.

## E4 — PR1 실행 한계와 사용자 loopback 인계

환경은 Python 3.9.6 / SQLite 3.43.2다. `python3 -m unittest -v tests.test_http_base`를 실행했으나
5개 모두 bind 단계의 `PermissionError: [Errno 1] Operation not permitted`로 ERROR, 종료 1이었다.
HTTP 요청 실행 전의 환경 실패다. 재시도·우회·skip으로 통과시키지 않았다. 실제 health·HTTP OFF 우선순위·Origin·
헤더/로그 억제·CLI serve 시작/Ctrl-C/포트 충돌은 사용자 실행 결과를 기다린다. 이 결과를 수신하기 전까지
AC11/14의 HTTP 부분과 PR1 통합 검증은 미완료다. 전체 discover 통과도 주장하지 않는다.

실행 대상은 이 변경 폴더의 `pr1-code.sha256`에 적은 제품·시험·합성 입력 파일 전체다.
기준 HEAD는 위 3d6fcf1이며 미커밋 신규 코드/시험을 포함한다. 문서는 코드 해시 집합과 별도다.
저장소 루트 `/Users/jake/Projects/ai-native-sdlc-codex-astra-20260913/f05-r01`에서 실행한다.

```sh
shasum -a 256 -c intent/0001-shared-requests/pr1-code.sha256
git rev-parse HEAD
git status --short
python3 -m unittest -v tests.test_http_base
# 가능하면 같은 판 전체 확인
python3 -m unittest discover -s tests -v
```

해시 전부 OK와 HTTP 5개 OK가 기대다. 전체 시험 수는 최종 확인 절의 수를 기준으로 한다.
시험은 합성 임시 DB·동적 loopback 포트·프로세스를 직접 준비하고 정리한다. 외부 서비스·실데이터는 사용하지 않는다.
사용자는 HEAD/status, 실제 명령·종료 코드·unittest 요약/실패 출력을 돌려준다. 새 SHA로 커밋해도 파일 해시가 같으면
같은 실행 코드판인지 대조할 수 있다. 사용자 시험·통합·공개 수락 결과는 아직 없다.

## E5 — PR1 최종 비네트워크 확인과 제출 범위

2026-09-13 UTC, E4의 해시 목록 코드판에서 실행했다.

| 실행 | 실제 결과 |
|---|---|
| `python3 -m unittest -v tests.test_config_model tests.test_import_storage tests.test_import_race tests.test_cli tests.test_tracker` | 28개 OK, 종료 0 (7.815초) |
| `python3 -m compileall -q service.py request_service tests` | 종료 0 |
| `shasum -a 256 -c intent/0001-shared-requests/pr1-code.sha256` | 18개 파일 모두 OK, 종료 0 |
| `git diff --check` | 종료 0. 신규 파일은 별도 공백 검사 대상에 포함 |

추가로 임시 메모리 연결 어댑터에서 실제 Handler를 호출해 health 200, OFF 503, Origin 403,
HEAD 405/빈 본문, 중복 길이 400의 다섯 입력과 JSON·입력 비노출을 확인했다. 이는 네트워크 없는
진단이며 영구 loopback 시험이나 HTTP 통합 통과의 대체 증거가 아니다.

정책 적용: brand B1–B3/P1의 이름과 contracts의 고정 오류를 유지한다. data-compliance C1/C2에 따라
자격증명·원본 예외 출력 없이 명시 DTO·열을 사용한다. C3 감사는 D1/D2의 시제품 제외 범위로 남긴다.
secure-api-review의 1 인증은 수락한 로그인 제외를 적용하고 충족으로 표시하지 않는다.
2 입력 검증은 PR1의 JSON과 health/OFF 경계에 적용했으며 PATCH는 PR3다.
3 감사는 수락한 제외 범위다. 4 데이터 분류는 회사 PII 분류를 만들지 않고 합성 데이터·고정 오류·로그 억제를 적용했다.
실제 HTTP 오류/로그 동작은 E4의 사용자 시험 대기다. 문서는 stop-slop-ko의 기술 문서 문체를 적용했다.

제출물은 기준 main과 같은 HEAD 위 다음 미커밋 변경이다. Git stage/commit/merge는 수행하지 않았다.

- 수정: CLAUDE.md, PROJECT-POLICY.md, README.md, intent/README.md,
  intent/0001-shared-requests/{plan,decisions,execution}.md.
- 신규: service.py, request_service/{__init__,config,model,service,storage,cli,http}.py,
  tests/{__init__,support,test_config_model,test_import_storage,test_import_race,test_cli,test_http_base}.py,
  intent/0001-shared-requests/pr1-code.sha256.
- 보존: tracker.py, requests.json, tests/test_tracker.py, D1 intent와 D2 전체 설계 정본.
  PROJECT-POLICY의 실행 명령만 현재화했다. 수락한 P1–P3·업무 범위는 바꾸지 않았다.

제품 결과는 초기 가져오기·기본 OFF 경계와 기존 CLI 보존이다. 실행으로 확인한 범위는
AC1–3/9 및 AC11/13의 비네트워크 부분이다. HTTP 시험 5개와 사용자 코드 검토·실제 로컬 통합은 남아 있다.
PR2의 조회·CSV, PR3의 버전 변경·HTTP 경합·전체 공개 단위 검증은 구현하지 않았다.
main은 시작 SHA와 같아 현재 시험은 그 main에 PR1을 더한 내용이다. 미래 merge 결과의 동일성은 사용자의
통합 SHA/부모/내용을 받은 뒤 대조하며, 현재 브랜치 통과로 머지 후 통과를 추정하지 않는다.

## E6 — S2 재개와 HUMAN 실제 실행 결과

직전 호출은 독립 검토 대기 중 회당 900초 제한으로 중단됐다. 재개 후 `collaboration.list_agents`에는
`/root`만 있었으며 기존 `/root/pr1_verifier`는 복원되지 않았다. 해당 검토의 결과를 회수하지 못했으므로
완료·무결함으로 간주하지 않는다. 원래 실행 결과 E3–E5는 보존한다.
채택한 sdlc-feedback 절차와 HUMAN 후속 지시에 따라 새 문맥의 `/root/pr1_verifier_resumed`를
`gpt-5.6-sol/high`로 시작했다. `.codex/agents/sdlc-verifier.toml`의 기준을 읽도록 인계한 fallback이며
named role이 선택됐다는 증거는 아니다. 검토 결과는 E7에 실제 수신 후 기록한다.

HUMAN은 전체 구현·테스트·문서 변경을 직접 읽었고 중요한 결함을 발견하지 않았다고 보고했다.
원본 후보는 HUMAN이 `3822e6686f8ef9b4f4d769b8f963a2373753ebd7`로 보존했다.
재개 시 HEAD가 이 SHA이고 작업 트리가 깨끗함을 확인했다. main은 여전히
`3d6fcf1eb46111ca7ffdb1b68aa2ba13ad6aab34`이며 PR1은 아직 통합 전이다.

다음 결과는 HUMAN이 같은 S2 후속 메시지로 제공한 실제 환경 실행 보고다. 에이전트가 직접 실행한
결과로 바꾸어 적지 않는다. 원본 후보의 선언된 코드/시험 파일 18개 해시가 각 실행 전후 같다는 보고를 포함한다.

| HUMAN 실행 시각 (UTC) | 실제 명령·관측 | 결과 |
|---|---|---|
| 2026-09-13T04:59:51Z | `python3 -m unittest tests.test_http_base -v` | 5개 모두 OK, 2.743초. 실행 전후 18개 해시 동일 |
| 2026-09-13T05:01:32Z | `python3 -m unittest discover -s tests -v` | 33개 모두 OK, 10.543초. pr1-code.sha256 실행 전후 18개 모두 OK. 실제 두 프로세스 가져오기 성공 1/기존 데이터 거부 1 및 HTTP 프로세스 시험 포함 |
| 별도 시각 미제공 | HUMAN 별도 관찰 | 41/41 통과 보고. 기존 CLI, 기본 OFF/health, 원본 바이트 보존, 전체 입력 검증과 DB 미생성, 원자적 가져오기, 실제 100행·2프로세스 가져오기 경합 포함 |

HUMAN의 별도 관찰기 파일·개별 출력은 제공되지 않았으며 제품에 넣지 않는다. 41개 보고를 저장소의
영구 unittest 33개로 합산하거나 각 사례의 독립 재현을 주장하지 않는다. 위 메시지에 숫자 종료 코드는
별도로 제시되지 않았으므로 OK 보고를 그대로 보존한다.

E4/E5의 HTTP 대기는 이 HUMAN 실행 보고로 해소됐다. 에이전트 환경의 bind 실패 사실은 그대로다.
현재 후보의 PR1 HTTP와 전체 시험은 HUMAN 실행 근거를 확보했으며, 이 결과가 PR2/PR3의 미구현 동작이나
미래 main 머지 결과를 증명하지는 않는다. 코드·시험이 바뀌지 않으면 같은 33개 시험을 다시 요구하지 않는다.
독립 검토에서 변경이 필요하면 변경된 범위와 필요한 재검증을 따로 기록한다.

## E7 — 복원 후 새 독립 검토 결과와 수정 범위

`/root/pr1_verifier_resumed`의 실제 최종 결과를 수신했다. 후보 `3822e66`과 문서 후속 diff에 대해
다음 중요 결함 2건을 보고했다. 이전 `/root/pr1_verifier`의 결과를 대신 복원했다고 주장하지 않는다.

1. 초기 요청줄 오류와 HTTP/0.9 요청에서 `request_version == HTTP/0.9`인 채 표준 헤더 작성 함수를
   사용해 상태선·필수 헤더 없이 JSON 본문만 보낸다. 예: `GET /health INVALID`와 version 없는 GET.
   contracts의 모든 HTTP/1.0 응답·파싱 오류 400 계약 위반이며 기존 raw 시험의 본문 검사만으로는 놓친다.
2. 표준 파서가 raw `//health`를 `/health`로 정규화해 OFF guard 예외 및 라우트 판정에 들어간다.
   실제 Handler 진단에서 200을 관찰했다. 수락한 경로 계약상 OFF는 503 feature_disabled,
   ON은 미지원 경로의 404 route_not_found로 처리해야 한다.

검증자는 기대·수락 계보·전체 PR1 diff와 현재 문서를 읽었고, 별도 `git diff --check`·18개 해시 확인·
실제 Handler의 비네트워크 raw 진단을 수행했다. 전체 unittest·loopback은 반복하지 않았다.
그 밖에 검토 범위의 추가 중요 불일치는 찾지 못했다고 보고했다. E3의 TDD 순서는 작성자 기록이며
독립적으로 실행 역사를 재구성하지 못한 한계를 명시했다. 두 결함 해결·관련 회귀 전에는 통합 가능으로
판단할 수 없다는 결론이다. 이 결과는 HUMAN의 원본 후보 시험·검토 보고를 지우지 않는다.

수정은 기존 계약을 충족하도록 HTTP 응답 작성과 raw target 보존에 한정한다. 표준 파서가 받는
HTTP/0.9 GET은 기존대로 처리하되 응답은 항상 수락한 HTTP/1.0 상태선·헤더를 갖게 한다.
새 업무/API 계약은 추가하지 않는다. HTTP는 계획의 구현 후 검증 범위이며, 위 진단을 바탕으로
영구 회귀를 보강한다. 이 수정 때문에 원본 후보의 33개 통과를 수정본 전체 통과로 옮겨 적지 않는다.

## E8 — HTTP 두 결함 수정과 관련 재검증

원본 후보 `3822e66`은 그대로 보존하고 그 위 미커밋 수정으로 처리했다.
`request_service/http.py`는 표준 구문 파싱 뒤 원래 request-target을 복원하고, HTTP/0.9의 응답 헤더
생략 분기를 피하도록 응답 작성 시 HTTP/1.0 헤더를 강제한다. raw `//health`와 `///health`는 OFF에서
503 feature_disabled, ON에서 404 route_not_found다. 정상 health·Origin·업무 guard의 순서는 유지한다.

`tests/test_http_base.py`의 raw 시험은 본문 문자열만 보던 검사를 HTTP/1.0 상태선, Content-Type,
바이트 Content-Length, Connection, Cache-Control, Server 비노출, JSON payload 검사로 보강했다.
동일 입력·기대를 영구 `HTTPParserTests`와 실제 loopback 시험에서 공유한다. ON/OFF 각 6개 raw 입력이다.

- 수정 전 `python3 -m unittest -v tests.test_http_base.HTTPParserTests`: 1개 시험, subtest 10개 assertion 실패.
  헤더 없는 응답과 //health의 200을 재현했다. 나머지 중복 길이 2개 사례는 이미 통과했다.
- 수정 후 같은 명령: 1개 OK, 0.003초, 종료 0. 입력·기대는 유지했다.
- 임시 실제 Handler 진단 4개: HTTP/1.0 및 1.1 정상 health, ON Origin 거부, OFF PATCH의
  Origin·본문 전 guard를 확인해 모두 OK. 소켓 없는 진단이며 loopback 통과를 뜻하지 않는다.
- `python3 -m compileall -q request_service/http.py tests/test_http_base.py`, `git diff --check`: 종료 0.
- 갱신한 `pr1-code.sha256`의 18개 파일 모두 OK. 원본 대비 제품/시험 해시 변화는 위 두 파일뿐이다.

실제 바뀐 raw loopback 시험 1개의 HUMAN 실행과 최신 수정 검토를 요청했다.
명령은 `python3 -m unittest -v tests.test_http_base.HTTPBaseTests.test_raw_duplicate_length_and_malformed_request`다.
전체 33개 반복은 요청하지 않았다. 원본의 33개와 수정본의 추가 파서 1개 결과는 서로 다른 코드판의 근거다.
수정본 전체 34개가 실행됐다고 주장하지 않는다. 후속 실행·검토 결과는 실제 수신 후 덧붙인다.

## E9 — 최신 수정 독립 재검토

같은 새 검증자 `/root/pr1_verifier_resumed`에게 이전 검토 이후 바뀐 HTTP·시험·해시·문서를 다시 인계하고
실제 최종 결과를 수신했다. 두 결함은 현재 수정으로 해소됐으며 추가 중요 결함을 찾지 못했다고 보고했다.
HTTP/0.9 fallback·초기 파싱 오류의 HTTP/1.0 응답과 raw target 보존에 따른 OFF 503/ON 404를 확인했다.

검증자가 직접 실행한 `python3 -m unittest -v tests.test_http_base.HTTPParserTests`는 1개 시험의
12개 입력 모두 통과했다. `git diff --check`와 갱신된 코드 해시 18개도 통과했다.
실제 loopback은 재실행하지 않았다. 원본 `3822e66`의 33개 통과를 수정본 전체 통과로 쓸 수 없으며,
수정된 raw loopback 시험의 HUMAN 통과 결과가 있어야 최신 PR1 통합 근거가 완성된다는 결론이다.

현재 남은 사항은 E8의 HUMAN focused loopback 실행 결과와 HUMAN의 후속 커밋·로컬 통합 판단이다.
이 기록은 독립 재검토의 실제 반환 결과이며 코드 승인·머지·공개 수락이 아니다.
PR2는 착수하지 않았고 Git 변경 명령은 수행하지 않았다. 검증자 이력은 삭제하지 않았다.

## E10 — PR1 수정본 HUMAN 실행·통합과 PR2 시작

HUMAN은 2026-09-13T05:17:00Z부터 수정본에서 `python3 -m unittest discover -s tests -v`를
새로 실행했다. raw HTTP 보강 시험을 포함한 전체 34개 OK, 11.636초, 종료 0이며 실행 전후 18개 해시가
같고 manifest도 모두 OK라고 보고했다. 이는 E6 원본의 33개 재사용이 아닌 수정본의 실제 실행이다.
E8/E9의 focused loopback 대기는 이 결과로 해소됐다. D4의 직접 수락 기록을 확인했다.

PR1 최종 커밋은 `3f14410409550594e1f76b436edc00cef0de8d6e`, main merge는
`ece1ed0824a60cc965ba34f124554f905ac330dc`다. PR2 시작 시 HEAD/main이 해당 merge이고,
브랜치가 `codex/shared-requests-read`, 작업 트리가 깨끗함을 확인했다. merge 부모는 이전 main
`3d6fcf1`과 PR1 `3f14410`이다. `git diff --exit-code 3f14410409550594e1f76b436edc00cef0de8d6e ece1ed0824a60cc965ba34f124554f905ac330dc`
종료 0으로 두 전체 트리 동일성을 직접 확인했다. 따라서 이 main의 PR1 baseline은 HUMAN 34개 통과를
동일성 근거로 재사용하며 시작 전 같은 시험을 불필요하게 반복하지 않는다.

PR2는 D3 plan의 조회 저장소→GET→CSV 연결 순서를 따른다. 새 조회/CSV는 동작별 구현 후 테스트,
기존 PR1 TDD 영역을 바꾸면 해당 전략을 유지한다. 기대는 AC4/5/10/13/14, contracts/storage와
support.EXPECTED의 고정 5행이다. 기존 bind 제한은 재시도하지 않고 새 실제 HTTP 시험·코드판을 HUMAN에게 인계한다.

## E11 — PR2 구현과 비네트워크 결과

코드 기준은 E10의 main `ece1ed0` 위 현재 PR2 미커밋 변경이다. 수락한 spec/설계 계약을 개정하지 않았다.
조회 저장소·service를 구현한 뒤 `tests.test_query_csv`의 조회 7개를 실행했다. 6개 OK, 1개는 시험 wrapper의
인자 이름 uri가 sqlite3.connect의 URI 옵션과 충돌한 TypeError였다. wrapper 인자를 database로 고치고
해당 원문·예약 경로 시험을 다시 실행해 OK를 확인했다. 제품 결함이나 TDD RED로 보고하지 않는다.

그 다음 GET을 연결하고 메모리 실제 Handler의 HTTPReadTests 계약을 실행했다. 필터·단건/null·오류·
percent 한 번 decode·plus/Unicode 원문·순서·OFF·미지원 메서드·응답 필드·OpenAPI 내부 참조를 확인했다.
이 단계의 6개 및 PR1 파서 1개가 OK였다. 이어 CSV serializer를 작성·표준 csv.reader 시험 1개 OK를 확인하고
CLI 출력에 연결했다. CSV/CLI·HTTP와 CSV의 독립 기대 비교를 보강한 당시 연결 16개는 모두 OK였다.

2026-09-13 UTC 최종 비네트워크 명령은 다음과 같다.

```sh
python3 -m unittest -v tests.test_config_model tests.test_import_storage tests.test_import_race tests.test_cli tests.test_tracker tests.test_query_csv tests.test_http_read.MemoryHTTPReadTests tests.test_http_base.HTTPParserTests
python3 -m compileall -q service.py request_service tests
git diff --check
```

46개 OK, 13.841초, 종료 0을 관측했다. compileall·diff 검사도 종료 0이다. PR1 baseline 34개를
시작 전에 반복한 것이 아니라 공통 경계 변경 후 영향받은 회귀를 포함한 실행이다. 기존 tracker/import/guard,
조회 read-only·5초 exclusive 잠금·없는/빈/잘못된 DB·고정 오류·입력 바이트·전체 행 불변을 검사했다.
CSV는 고정 5열/CRLF/UTF-8/BOM 없음·null 빈 셀·쉼표/따옴표/한글/CR/LF·빈 헤더·수식 원문 유지,
필터·stdout 인코딩 독립·조회/직렬화 실패 시 출력 없음·출력 실패 후 행 불변을 확인했다.

같은 실행의 실제 두 프로세스 import 회귀는 PID 37936 imported=5와 PID 37937 store_not_empty였다.
UTC 실행 구간은 각각 05:27:18.031632→05:27:18.034575, 05:27:18.031635→05:27:18.035418이다.
부모 공통 시계의 ready 5558367666/5558445083, 완료 관측 5565439458/5565962125,
관측 구간 교집합 6994375ns였다. 최종 R-201…R-205 5열은 EXPECTED와 같고 원본 바이트도 불변이었다.
이 기록은 E3처럼 barrier 겹침 근거이며 성능 수치가 아니다.

## E12 — PR2 실제 HTTP 인계·남은 범위

새 실제 HTTP는 아직 에이전트 환경에서 실행하지 않았다. 이미 확인한 bind 제한을 재시도·우회하지 않았다.
메모리 Handler 시험을 TCP 시험으로 보고하지 않는다. HUMAN에게 현재 코드판으로 다음 실행을 요청했다.

```sh
shasum -a 256 -c intent/0001-shared-requests/pr2-code.sha256
python3 -m unittest -v tests.test_http_base tests.test_http_read.HTTPReadTests
# 전체를 선택하는 경우
python3 -m unittest discover -s tests -v
```

저장소 루트에서 실행한다. `pr2-code.sha256`은 service.py, request_service/*.py, tests/*.py,
tracker.py, requests.json 전체 21개 파일의 SHA-256이다. 기준 HEAD는 `ece1ed0`이며 미커밋 PR2 파일을 포함한다.
첫 HTTP 명령은 13개(기존 실제 HTTP 5개·파서 1개·새 실제 GET/CSV 연계 7개), 전체는 58개 OK가 기대다.
HUMAN의 실행 시각·종료 코드·요약 및 실행 전후 해시 동일 결과를 실제 수신하면 이어 기록한다.

제품 구현 범위는 R3/R5의 조회·CSV와 PR2의 OFF/오류 불변성이다. 실제 TCP 연결 및 사용자 통합 판단은
아직 남아 있다. PR3 PATCH·실제 두 변경 경합·최종 공개 단위 검증은 구현하지 않았다.
정책은 기존 P1–P3·D1/D2 범위로 적용한다. 응답은 명시 5필드, SQL은 명시 열·바인딩 값이며
고정 오류/로그 억제를 유지한다. 인증·감사 제외를 해당 팀 스킬 충족으로 바꾸지 않는다.

PR2 추가 정책 확인은 secure-api-review의 네 항목을 구분했다. 1 인증은 D1/D2가 수락한 로그인 제외를
유지하며 인증 충족으로 표시하지 않는다. 2 입력 검증은 GET의 허용/중복 필터, 엄격 percent/UTF-8,
원문 ID·GET framing, service 재검증과 OpenAPI 명시 응답 필드를 대조했다. 3 감사는 수락한 이력 제외를
유지하며 새 GET/CSV에 업무 쓰기를 넣지 않는다. 4 데이터 취급은 명시 5필드·SQL 바인딩·고정 오류·
로그 억제로 확인했다. 회사 PII 분류·보존 기간은 새로 만들지 않았다. brand의 이름·고정 오류와
stop-slop-ko의 기술 문서 문체를 적용했다.

## E13 — PR2 독립 완료 검토와 제출 상태

새 문맥의 `/root/pr2_verifier`를 `gpt-5.6-sol/high`로 시작해 `.codex/agents/sdlc-verifier.toml`의
기준을 읽도록 인계했다. named role selector 없는 런타임의 file-read fallback이며 이전 PR1 검토를
현재 PR2 검토로 대신하지 않았다. 실제 최종 결과를 수신했다.

검증자는 `ece1ed0`부터 현재 작업 트리의 추적 변경 14개·미추적 4개 전체, D1–D3와 최신 D4/실행 기록,
intent/spec/plan·선언된 전체 설계·구현·시험·문서를 대조했다. PR2 범위의 중요한 Bugs/Security/Policy-scope
발견은 없다는 결론이다. 정확 필터·정렬·URI/쿼리 처리·오류 우선순위·OFF, read-only SQLite, 명시 5필드,
CSV 인코딩·실패 동작이 계약과 맞고 PATCH 미구현은 PR3 범위임을 확인했다.

검증자가 직접 실행한 명령은
`python3 -m unittest -v tests.test_query_csv tests.test_http_read.MemoryHTTPReadTests tests.test_http_base.HTTPParserTests`이며
16개 OK, 5.526초였다. 실행 전후 `pr2-code.sha256` 21개 모두 OK, `git diff --check` 종료 0을 확인했다.
D2 정본은 승인 판 이후 변경 없음을 대조했다. 알려진 bind 제한은 재시도하지 않았다.
메모리 Handler 시험은 실제 TCP 증거가 아니며 HUMAN의 E12 명령 결과 전에는 PR2 통합 검증 완료로
판단할 수 없다는 한계를 명시했다. 사람의 코드 승인·통합도 별도다.

PR2 제출 시 HEAD/main은 `ece1ed0824a60cc965ba34f124554f905ac330dc`다. 현재 미커밋 파일은 다음과 같다.

- 수정 제품: request_service/{cli,http,model,service,storage}.py.
- 신규 제품: request_service/csv_export.py.
- 수정 시험: tests/test_cli.py, tests/test_http_base.py. 신규 시험: tests/test_query_csv.py, tests/test_http_read.py.
- 문서/판: CLAUDE.md, PROJECT-POLICY.md, README.md, intent/README.md,
  intent/0001-shared-requests/{plan,decisions,execution}.md 및 신규 pr2-code.sha256.

tracker.py·requests.json·기존 tracker 시험·PR1 config/model/import 회귀 시험과 D2 설계 정본은 보존했다.
제품 결과는 공통 GET 조회·현재 CSV 추출이며 비네트워크 46개와 독립 집중 16개가 실행 근거다.
PR2 실제 TCP·HUMAN 코드 수락·로컬 merge와 PR3 변경/경합/최종 공개는 아직 완료가 아니다.
Git stage/commit/merge·원격 push·배포는 수행하지 않았다. PR2를 이 상태로 제출하고 PR3는 착수하지 않는다.

## E14 — PR2 HUMAN 실행·통합과 PR3 시작

HUMAN은 PR2 전체 diff·독립 검토 결과를 읽고 D5로 수락했다. 실제 전체 실행은
2026-09-13T05:28:06Z 시작, 58개 OK/21.545초/종료 0이며 실제 HTTP 13개를 포함한다.
21개 코드/시험 해시는 전후 동일하고, 같은 파일을 고정한 HUMAN 관찰용 복제본도 112/112 통과했다는
보고다. 관찰기는 제품에 포함하지 않으며 개별 관찰을 에이전트 직접 실행으로 바꾸지 않는다.
HUMAN이 현재 파일과 두 실행판의 동일성도 확인했다. E12/E13의 HTTP 대기는 이 결과로 해소됐다.

PR2 최종 `d80fb872c87533e40e0cd765252362f1bf4ecfe6`과 main merge
`86cde3641ae02a32fa35037d9eb24bac00cede3b`를 `git diff --exit-code`로 직접 대조해 종료 0을 확인했다.
PR3 시작 브랜치는 `codex/shared-requests-update`, HEAD/main은 이 merge이고 작업 트리는 깨끗했다.
동일 baseline의 58개는 재사용한다. 일반 공개·push·배포는 수락되지 않았고 Git은 HUMAN 담당이다.
PR3는 수락한 TDD model/저장소 → HTTP 연결 → 실제 경합/전체 공개 단위 시험 순서를 따른다.
마감 05:49:42Z 안에 미실행·미검토 부분이 남으면 해당 부분을 완료로 표시하지 않는다.

## E15 — PR3 TDD 및 연결 실행 (진행 중)

기준 HEAD/main은 E14의 86cde36이며 현재 미커밋 변경이다. 수락한 계약은 바꾸지 않았다.
다음은 실제 관측한 TDD 순서다. 명령은 `python3 -m unittest -v tests.test_update_storage` 또는
해당 새 클래스/시험의 집중 실행이었다. 없는 모듈·문법 오류를 RED로 세지 않았다.

- validate_patch의 통과 뼈대: 부적합 입력 22개 미거부 failure. 엄격 필드/정수 version/owner/status 검증 뒤 2개 OK.
- 저장소 변경 뼈대는 현재 행만 반환: 기대한 담당자·done·v2와 달라 실패. 실제 BEGIN IMMEDIATE·한 UPDATE·COMMIT 뒤 통과.
- 동일 값 변경에서 v2를 반환해 v1 기대 실패. no-op를 넣은 뒤 낡은 version 미거부로 다시 실패했고
  값 비교 전에 version 검사를 넣어 같은 기대를 통과했다.
- done→open 미거부 failure, 최대 version 실제 변경은 SQLite 정수 OverflowError. 전이·상한 검사 뒤 당시 6개 OK.
- 잘못된 patch의 validation보다 Repository 생성이 먼저 평가되는 spy assertion 실패. validated 값을 먼저 만든 뒤
  생성하도록 바꿔 당시 8개 OK. 커밋 실패 주입의 실제 행 롤백은 처음부터 통과한 회귀다.
- parse_patch의 중복 키 미거부 failure 및 깨진 UTF-8/BOM/JSON의 원본 오류 3개를 관측했다.
  공통 엄격 object_pairs_hook/parse_constant와 고정 오류 매핑 후 model·저장소 9개 OK.

HTTP는 구현 뒤 test_http_write의 상태변경/동일값/경합오류/전이/해제, raw framing·MIME·JSON 오류,
최대 1,048,576바이트와 MIME 대소문자를 메모리 Handler로 확인했다. 당시 집중 20개(쓰기 3개와
model/저장소 9개·조회 7개·기존 파서 1개) 모두 OK였다. actual TCP 시험으로 바꾸어 적지 않는다.

공통 경계 변경 뒤 비네트워크 전체 명령을 한 번 실행했다:
`python3 -m unittest -v tests.test_config_model tests.test_import_storage tests.test_import_race tests.test_cli tests.test_tracker tests.test_query_csv tests.test_http_read.MemoryHTTPReadTests tests.test_http_base.HTTPParserTests tests.test_update_storage tests.test_http_write.MemoryHTTPWriteTests`.
결과는 58개 OK/13.511초/종료 0이다. 이 숫자는 PR2 HUMAN 전체 58개와 다른 시험 집합·코드판이다.
이 실행 시점에는 새 timeout 회귀가 아직 없었다. 실제 가져오기 회귀는 PID 43614 store_not_empty,
43615 imported=5였고 UTC 구간은 05:43:15.180278→05:43:15.184246 및
05:43:15.180388→05:43:15.182970이었다. 부모 관측 구간 교집합 8212292ns, 최종 5행/원본 바이트 불변이었다.

Python 3.9에서 `issubclass(socket.timeout, TimeoutError)`가 False임을 직접 확인해 HTTP timeout
catch를 두 예외로 보완했다. 이 HTTP 영역은 구현 후 검증 방식이다. 영구 timeout 매핑 시험을 보강한
`tests.test_http_write.MemoryHTTPWriteTests` 4개는 0.019초에 OK였다. 마지막 보완 뒤 전체 59개를
실행했다고 소급하지 않는다. 나머지 기존 비네트워크 근거는 해당 변경 영향 밖에서 재사용한다.

## E16 — PR3 현재 코드판·실제 실행 및 검토 대기

새 실제 파일 tests/test_http_write.py, test_http_protocol.py, test_http_race.py, test_release.py를 작성했다.
경합은 독립 HTTP 연결 두 개와 handler→실제 service 진입 barrier로 동시 구간을 만들고 한 200·한
409 version_conflict·최종 v2/승자·전체 행·UTC/monotonic 구간을 출력하도록 작성했다. 저장소는 대체하지 않는다.
전체 흐름은 실제 CLI serve 프로세스를 OFF→ON→OFF로 종료·재시작하며 200행/5명 합성 입력의
가져오기→GET→PATCH→GET/CSV→OFF 보존을 검사한다. 아직 이 환경에서 TCP 실행하지 않았다.

HUMAN에게 `pr3-code.sha256`의 26개 코드/시험 파일과 다음 명령을 인계했다.

```sh
shasum -a 256 -c intent/0001-shared-requests/pr3-code.sha256
python3 -m unittest -v tests.test_http_base tests.test_http_read.HTTPReadTests tests.test_http_write.HTTPWriteTests tests.test_http_protocol tests.test_http_race tests.test_release
# 전체를 선택하면 현재 수집 수 77개
python3 -m unittest discover -s tests -v
```

집중 HTTP 명령은 현재 19개가 기대다. 이 명령·예상 수는 실행 통과가 아니다.
기준 HEAD는 86cde3641ae02a32fa35037d9eb24bac00cede3b + 현재 미커밋 PR3 변경이다.
기존 pr1/pr2 manifest는 과거 판으로 보존하고 현재 판에는 pr3 manifest를 사용한다.

새 문맥 `/root/pr3_verifier`를 gpt-5.6-sol/high로 시작해 verifier TOML 기준을 읽도록 인계했다.
named role 선택이 아닌 file-read fallback이다. 현재 실제 반환 결과는 대기 중이며 마감에 복원되지 않거나
미완료면 검토 완료를 추정하지 않는다. PR3 전체 완료·통합·일반 공개를 선언하지 않았다.

남은 증거는 HUMAN 네트워크 결과, no-op/실제 변경 전용 경합, 변경 저장소의 쓰기 잠금·UPDATE/영향 행 0
실패 시험, 최종 AC 전체 대조와 독립 검토다. 이 목록을 이유 없이 삭제하거나 기존 통과로 대체하지 않는다.
재개 시 pr3 해시와 미커밋 diff를 먼저 대조하고 실제 리뷰 결과·이 미실행 항목부터 이어간다.

## E17 — PR3 독립 검토 결과 및 미완료 인계

05:47Z 검증자 `/root/pr3_verifier`의 실제 최종 결과를 수신했다. 검토 자체의 결과는 회수했으며
진행 중 검토를 완료로 추정한 것이 아니다. 검증자는 현재 코드에서 중요한 Bugs/Security/계약 불일치를
찾지 못했다. strict patch, guard·검증 후 Repository, HTTP framing/MIME/우선순위, 트랜잭션의
존재→version→전이→no-op→상한→한 UPDATE/영향 행 확인→COMMIT/롤백을 계약과 대조했다.

검증자가 현재 timeout 보완까지 포함한 비네트워크 59개를 직접 실행해 13.875초 모두 OK를 확인했다.
compileall·git diff --check는 종료 0, manifest 26개 모두 OK였다. D2 정본이 승인 판과 같고
PR2 최종 커밋과 merge 트리도 같음을 별도로 확인했다. E15의 RED→GREEN 순서는 작성자 기록으로
보존되며, 검증자는 현재 시험/GREEN은 확인했지만 과거 실행 순서를 독립 재구성한 것은 아니다.

검토 결론은 **PR3 완료 불가**다. 코드 결함을 발견하지 못했다는 사실과 완료 여부를 구분한다.
수락한 plan이 요구한 no-op/실제 변경 전용 경합, 변경 저장소 쓰기 잠금 timeout, UPDATE 오류 및
영향 행 0 주입 시험이 아직 없다. E16의 미실행 목록이 이 공백을 정확히 드러내지만 완료 조건을 충족하지는 않는다.
또한 HUMAN의 실제 HTTP 19개/전체 77개 결과가 아직 없어 PATCH transport·408·AC8 동시 변경·
200행 프로세스 OFF→ON→OFF 흐름은 실행 근거가 없다. 새 실제 네트워크 시험 파일 작성만으로 이를 완료로 세지 않는다.

현재 제출은 main/HEAD `86cde3641ae02a32fa35037d9eb24bac00cede3b` 위 미커밋 PR3다.
제품 수정은 request_service/{model,service,storage,http}.py, 기존 시험 수정은 tests/test_http_read.py,
신규 시험은 tests/{test_update_storage,test_http_write,test_http_protocol,test_http_race,test_release}.py다.
문서 수정은 CLAUDE/PROJECT-POLICY/README, intent/README와 변경 폴더의 plan/decisions/execution이며
새 pr3-code.sha256으로 전체 실행 파일 26개를 고정했다. 기존 원본·시험 실패·수락·이전 manifest는 보존했다.
Git stage/commit/merge·일반 공개·push·배포는 수행하지 않았다.

재개 순서는 현재 pr3 해시 및 diff 대조 → HUMAN의 실제 실행 결과를 코드판과 연결 → 위 누락된 전용
시험 보강·실행 → 실패가 있으면 선택한 TDD/연결 검증 순서로 수정 → 최신 범위 독립 재검토 →
HUMAN 통합 판단이다. 최종 공개는 별도 사용자 수락 전까지 기본 OFF를 유지한다.
마감 때문에 중요한 검증 기준을 낮추거나 예정 명령을 통과로 바꾸지 않았으며, PR3를 미완료로 인계한다.

## E18 — HUMAN 실행 결과 연결과 미완료 판 보존

2026-09-13, HUMAN/root가 개발 호출 종료 뒤 추가한 기록이다. 개발 에이전트가 이 결과를 전달받아
재검토한 것으로 표시하지 않는다. 전체 실행은 원래90분 한도 내8회 호출, 마지막 종료05:48:59Z였다.

- HUMAN은 실제 PR3 소스와 모든 새·변경 시험을 읽었다. 05:44:21Z의 실제 지연 본문 진단은408과
  request_timeout을 반환하고 DB를 만들지 않았다. 당시 HTTP 해시가 전후 동일했다. 에이전트가 이미
  socket.timeout 보완을 적용한 판의 성공 관찰이며, HUMAN이 최초 실패를 재현하거나 수정한 사례가 아니다.
- 05:45:03Z부터 현재26개 파일에서 전체 unittest를 실제 실행했다. 77개 OK,29.107초,종료0이었다.
  실제 두 PATCH는200/409,최종version2와 승자 값,양쪽 실행 구간 겹침을 확인했다. 200행의 실제 CLI
  프로세스 OFF→ON→OFF와 조회/CSV도 포함한다.26개 코드/시험 해시는 전후 동일했다.
- 같은26개 파일을 고정한 HUMAN 관찰용 복제본에서도 초기 계약216/216 확인을 통과했다.
  명령32·HTTP52·SQLite17 기록이며 읽기/변경/충돌/원자성·같은 소스의 OFF/ON/OFF·재시작을 포함한다.
  관찰기는 제품에 넣지 않는다. 현재파일과 관찰판의 코드 동일성을 확인했다.

따라서 E16–E17의 실제 HTTP 결과 부재는 이 HUMAN 근거로 해소됐다. 그러나 계획의 no-op/실제 변경
전용 경합,쓰기 잠금 timeout,UPDATE 실패/영향 행0 시험은 남는다. PR3의 최종 수락·통합·공개는 하지 않는다.
HUMAN은 구현과 관련 문서가 담긴 현재 판을 미완료 커밋으로 보존한다. 통합 main은 D5의PR2까지다.
재개 시 이26개 해시와 보존판을 대조하고 남은 시험·최신 검토·HUMAN 통합 판단부터 이어간다.
