# Plan: 공유 요청 저장소와 로컬 API·CSV (from intent 0001-shared-requests)
Upstream: spec.md 및 design/contracts.md, design/storage.md, design/openapi.json@e9d52f8ad20fb09c912df2138ca4d939d621fad7. Status: draft.

[spec](spec.md)의 전체 Design 정본을 기준으로 초기 가져오기 → 조회·CSV → 버전 변경 순서의 3개 구현 PR을
계획한다. [D2](decisions.md)에서 PO가 설계 집합을 수락했다. 현재 상위 내용은 수락 판과 동일하며
계약 개정은 없다. intent·프로젝트 정책 수락은 D1이다. draft·제안·대기라는 원문의 표기는 수락 기록을 취소하지 않는다.
이 plan은 엔지니어 검토용이며 아직 plan의 수락 SHA나 제품 구현 허가는 기록되지 않았다.

## Files that change

아래 new 경로는 구현할 때 만든다. 이번 제출에는 plan·결정·검증 기록만 포함한다.

| 경로 | 변경 역할 | spec/AC |
|---|---|---|
| service.py, request_service/__init__.py (new) | 별도 진입점·부수 효과 없는 패키지 | R1/R6 |
| request_service/config.py, model.py, service.py (new) | flag, DTO·엄격 검증·고정 오류, 업무 guard와 저장소 연결 | AC2–7,11,14,16 |
| request_service/storage.py (new) | 스키마 확인·초기 가져오기·읽기·원자적 버전 변경 | AC2–9,13,16 |
| request_service/cli.py (new) | 세 명령·인자·UTF-8 출력·종료 코드·서버 실행 | AC1–3,10–13 |
| request_service/http.py (new) | health·게이트·GET·PATCH·파싱·동시 연결·오류 | AC5–8,11–14 |
| request_service/csv_export.py (new) | DTO 목록의 UTF-8 표준 CSV 직렬화 | AC10 |
| tests/__init__.py, tests/support.py (new) | unittest 모듈 실행, 임시 파일·서버 수명·독립 SQL snapshot·동시 시험 동기화 | 전체 |
| tests/test_config_model.py, test_import_storage.py, test_import_race.py, test_cli.py, test_http_base.py (new) | PR1 검증 및 뒤 PR에서 인접 회귀 보강 | AC1–3,9,11,13,14 |
| tests/test_query_csv.py, test_http_read.py (new) | PR2 조회·CSV·인코딩·read-only | AC4,5,10,13,14 |
| tests/test_update_storage.py, test_http_write.py, test_http_protocol.py, test_http_race.py, test_release.py (new) | PR3 변경·실제 HTTP 경합·최종 공개 단위 | AC6–8,12–16 |
| tests/test_tracker.py (기존, 보존) | 기존 세 테스트 그대로 재사용. 추가 flag 독립성은 test_cli.py에서 검사 | AC1 |
| README.md, CLAUDE.md, PROJECT-POLICY.md (기존) | 실제 구현한 명령·시험·부분 완료 범위·사용법과 기록 위치 갱신 | AC1,11,12,15 |
| intent/README.md (기존) | 첫 변경과 정본 링크 갱신 | 문서 인계 |
| intent/0001-shared-requests/execution.md, decisions.md | 실행·수락·통합·공개 기록. execution은 이번 제출에서 new | AC8,9,15 |
| spec.md와 design/*, plan.md (필요 시) | 영향받은 계약/계획만 이유와 함께 관련 구현 커밋에서 갱신 | 피드백 절차 |

tracker.py와 requests.json은 변경하지 않는다. 시험은 원본의 복사본이나 독립 합성 입력만 사용한다.
별도 프레임워크·패키지 설치·빌드·CI·운영 로그 기능을 도입하지 않는다. 현재 python3는 3.9.6,
SQLite는 3.43.2다. 구현과 시험은 이 환경에서 실행되도록 작성하고, 다른 버전에서의 성공을 추정하지 않는다.
예를 들어 Python 3.12 전용 sqlite3 인자를 사용하지 않는다. 추가 지원 버전 약속은 하지 않는다.

## Order of work

### 새 구현 세션의 시작과 권한

이 문서와 저장소만 인계받은 구현자는 다음 순서로 시작한다.

1. AGENTS.md, CLAUDE.md, PROJECT-POLICY.md, REVIEW.md와 채택한 sdlc-feedback을 읽는다.
   intent.md, spec.md와 선언된 네 파일 전체, 이 plan, decisions.md, execution.md를 읽는다.
   D1/D2 실제 SHA의 파일과 현재 문서를 대조한다. plan 수락 SHA·엔지니어 결정도 decisions.md에 있는지 확인한다.
2. plan 수락이 아직 없으면 수락을 발명하거나 구현을 시작하지 않는다. 사용자가 실제 SHA와 수락 결정을
   전달하면 기록한다. 기록 저장용 후속 커밋과 수락 대상 원본 SHA를 구분한다. 수락 뒤에는 같은 결정을 재요청하지 않는다.
3. `git status --short`, `git rev-parse HEAD`, `git rev-parse main`으로 현재 상태를 확인한다.
   제출 시 HEAD는 e9d52f8ad20fb09c912df2138ca4d939d621fad7, 브랜치는 codex/0033-design,
   main은 dcc6663a266cda8c342d609a5f715bda84507c5a였다. 이는 관측값이며 새 세션의 시작점을 고정하지 않는다.
   지금 main에는 수락 문서가 아직 통합되지 않았으므로 사용자가 문서·plan·수락 기록을 main에 먼저 통합해야 한다.
4. 사용자가 최신 로컬 main에서 첫 작업 브랜치 `codex/shared-requests-import`를 준비한다.
   이후 브랜치는 `codex/shared-requests-read`, `codex/shared-requests-update`다. 사용자 작업 트리를 초기화하거나
   이력을 재작성하지 않는다. 기존 작업이 있으면 diff와 범위를 확인하고 보존한다.
5. 아래 baseline과 PR별 검증 순서로 진행한다. 제품 작업의 stage/commit/merge와 브랜치·통합 준비는
   사용자가 대행한다. 에이전트는 파일 작성·읽기·시험·검토와 Git read-only 검사를 맡는다.
   원격 push·실제 배포는 하지 않는다. loopback 실행이 제한되면 아래 사람 실행 절차로 근거를 받는다.

이 plan을 수락하면 아래 3개 PR의 계획 범위가 구현 기준이다. 회사 인증·감사·실데이터 도입은 허용하지 않는다.
새 업무·계약 결정이 필요하면 PO에게 영향과 대안을 제시하고 의존 작업 전에 spec/plan을 현재화한다.
허용된 내부 분할·검증 방식 조정은 이유를 plan에 남긴다. 중간 대화만으로 문서 갱신을 대신하지 않는다.

### 검증 방식 선택

혼합을 선택한다. TDD는 원자성·입력 거부·버전 불변성처럼 정확한 실패를 먼저 관찰할 이점이 큰
model/guard/가져오기/변경 저장소 동작에 적용한다. `.agents/skills/tdd/SKILL.md`를 읽고 적용한다.
HTTP·CLI·조회·CSV 연결과 전체 동시 실행은 한 동작 구현 → 해당 자동 시험 추가·실행 → 수정·회귀 후
다음 동작으로 진행한다. 기존 tracker 세 테스트는 재사용하되 flag 독립성과 전체 출력 보호는 보강한다.

TDD 범위에서는 한 동작의 시험·의도한 실패 → 최소 구현 → 같은 기대의 통과 순서를 기록한다.
없는 import 경로·문법 오류만으로 RED를 주장하지 않는다. 처음 경계가 없으면 import 가능한 최소 뼈대를
만든 뒤 기능이 없다는 동작 assertion의 실패를 확인한다. 이미 통과하는 보존/경계 사례는 회귀 근거로 남기며
RED를 만들려고 코드를 망가뜨리지 않는다. 구현 뒤 작성한 시험을 TDD로 소급하지 않는다.

| 구현 PR | 선행·독립성 | 머지 후 main의 시험 ON / 일반 OFF | 남은 범위 |
|---|---|---|---|
| PR1 초기 가져오기와 공개 경계 | 문서·plan 수락 및 main 통합 후 | import-json과 serve의 /health, 업무 OFF 차단 실행 가능. 기존 CLI 정상 | ON 조회·CSV·PATCH |
| PR2 공통 조회와 CSV | PR1 main 통합·검증 후 | GET 목록·단건과 CSV 실행 가능. 같은 flag, 일반 OFF | 버전 변경·최종 공개 검증 |
| PR3 버전 변경과 공개 단위 완성 | PR2 main 통합·검증 후 | PATCH와 실제 경합까지 전체 시험 가능. 최종 공개 수락 전 일반 OFF | 사람의 코드 통합·최종 공개 결정 |

부분 PR에서 아직 구현하지 않은 ON 명령/라우트는 help에 노출하지 않고 미지원 명령/라우트로 거부한다.
그 부분을 최종 계약 완료로 보고하지 않는다. OFF의 export-csv 직접 호출은 PR1부터 인자 구문을 인식하고
feature_disabled로 막는다. HTTP OFF는 미지원 경로/메서드도 수락한 우선순위로 차단한다.
이것은 개발 중 부분 상태이며 최종 PR에서 세 명령과 모든 경로의 수락 계약을 완성한다.
부분 상태만을 검사한 임시 assertion은 해당 기능 도입 시 제거 이유를 기록하고 최종 기대 시험으로 교체한다.

세 PR은 storage/service/cli/http와 시험 지원 코드를 공유하고 저장소 계약에도 의존하므로 동시에 구현하지 않는다.
CSV serializer 같은 작은 순수 함수는 분리할 수 있으나 PR2의 조회 연결과 통합 시험이 필요해 별도 병렬 PR의
이득이 작다. 구현 서브에이전트는 기본으로 사용하지 않는다. 완료 전 독립 검토는 채택한 스킬에 따라 별도로 수행한다.

### PR1 — 초기 가져오기와 기본 OFF

**Files:** service.py, request_service의 __init__/config/model/service/storage/cli/http,
tests의 __init__/support/test_config_model/test_import_storage/test_import_race/test_cli/test_http_base,
README·CLAUDE·PROJECT-POLICY·intent/README·execution·decisions.
**Strategy:** config/model/업무 guard/가져오기 저장소는 TDD, CLI·health·실제 가져오기 경합은 동작별 구현 후 테스트.
독립 기대는 storage.md의 스키마·가져오기 순서와 AC2/3/9/11/13이다.

1. **Baseline:** `python3 -m unittest discover -s tests -v`로 현재 기존 세 테스트를 확인한다.
   이번 plan 작성에서 3개 통과를 관측했으나 구현 시작 판에서도 확인한다. tests/support.py는 기대를
   계산하는 제품 함수 없이 임시 폴더·명시 열 SQL snapshot·원본 바이트를 제공한다.
2. **TDD:** flag 정확히 1만 ON, 잘못된 JSON·타입·중복·빈 배열 거부, 전체 검증 전 DB 미접근,
   성공한 전체 삽입·초기 version 1, 기존 행 존재 거부 순서로 작은 시험과 구현을 반복한다.
   읽지 말아야 할 입력/DB 경계에 호출 감지 spy를 써도 되지만 원자성 시험은 실제 SQLite를 사용한다.
   schema 생성과 모든 삽입을 같은 BEGIN IMMEDIATE/COMMIT에 넣는다. 생성·삽입·커밋 예외를
   연결 wrapper로 주입하고 실제 DB의 롤백 결과를 검사한다. 가짜 repository 성공으로 원자성을 증명하지 않는다.
3. **연결:** import-json CLI의 인자·중복 옵션·고정 오류·stdout JSON/종료 코드부터 구현·시험한다.
   이어 serve와 /health, HTTP OFF guard·Origin 거부·기본 오류 응답·로그 억제를 구현하고 test_http_base로
   실제 loopback 및 CLI 서버 시작/종료를 확인한다. 서버 시작/모듈 import에는 DB를 열지 않는다.
4. **경합:** test_import_race에서 독립 프로세스 두 개가 같은 빈 DB에 가져오기를 시도하게 한다.
   시작 barrier와 완료 전 겹친 실행 근거, 각 imported 결과/오류, 최종 명시 열과 원본 바이트를 남긴다.
   정상 조건에서 하나 성공·하나 store_not_empty. 별도 쓰기 잠금 유지 시험은 5초 후 store_busy를 기대한다.
5. **회귀:** 기존 CLI의 전체 탭 출력·종료 코드·파일 순서·대상만 변경·반복 완료를 직접 정한 기대와 대조한다.
   flag 미설정/0/1에서 기존 CLI가 같은 결과인지 test_cli에 추가한다. help는 OFF·DB 없음에서도 성공한다.
6. **Done:** PR1 명령군과 기존 회귀 통과, OFF에서 입력/DB 미접근, ON에서 가져오기 확인을 기록한다.
   README는 현재 시험 가능한 부분과 남은 범위를 구분한다. 실제 생긴 명령·성공 기준만 CLAUDE/정책에 반영한다.
   아래 공통 검토·통합 절차 후 PR2로 간다. 일반 공개는 하지 않는다.

### PR2 — 같은 조회 결과의 API와 CSV

**Files:** model/service/storage/cli/http 확장, csv_export.py new,
test_query_csv/test_http_read new, support/test_cli 보강, 사용·실행 기록.
**Strategy:** 동작별 구현 후 테스트. 필터·정렬·읽기 경계·CSV 출력 연결을 작은 단위로 완결한다.
PR1의 TDD 대상 model/guard/초기 가져오기 동작을 고치게 되면 해당 범위는 TDD를 유지한다.

1. **Baseline:** PR1이 main에 통합된 실제 판에서 PR1 명령군과 기존 회귀를 확인한다.
2. **조회:** read-only 연결·스키마 검사·명시 열 SELECT와 DTO 목록/단건을 구현한 뒤 test_query_csv에서
   AC4의 고정 ID 목록을 확인한다. owner/status AND·대소문자·null·미지원 스키마·없는 DB·예약문자 경로를
   검사하고 실패·조회 전후 모든 행이 같음을 확인한다. 이 검증을 마친 뒤 HTTP GET을 연결한다.
3. **HTTP:** 한 번 percent decode하는 ID·쿼리·오류 우선순위와 GET 응답을 구현하고 test_http_read에서
   실제 연결로 검사한다. ID의 slash/percent/plus, Unicode 정규화가 다른 두 ID, 중복·빈·미지원 필터,
   헤더·고정 오류·출력 데이터 비노출을 확인한다. health/OFF 회귀도 실행한다.
4. **CSV:** 직렬화 후 stdout 연결 순서로 구현·시험한다. csv.reader를 독립 소비자로 사용해 AC10의 헤더·열·
   값·줄바꿈을 확인한다. UTF-8 바이트/BOM 없음/CRLF와 빈 결과 헤더를 직접 검사한다. 전체 조회 결과를
   확보하기 전 출력하지 않는지, 조회·출력 실패의 stdout/stderr/종료 코드를 검사한다.
5. **일치:** 쓰기를 멈춘 같은 DB의 HTTP 응답과 CSV를 각각 AC4의 독립 기대와 대조한다.
   둘이 서로 같다는 것만으로 정답을 판정하지 않는다. 읽기 전후 DB의 업무 행과 JSON 원본은 불변이다.
6. **Done:** PR2 명령군·PR1/기존 회귀와 OFF 직접 차단을 검증하고 공통 통합 절차를 마친다.
   README에 GET·CSV 사용법을 추가하되 변경 기능과 최종 공개는 미완료라고 기록한다.

### PR3 — 버전 변경과 최종 공개 검증

**Files:** model/service/storage/http/cli 완성, test_update_storage/test_http_write/test_http_protocol/
test_http_race/test_release new, support·기존 새 시험 보강, 사용·실행·결정 기록.
**Strategy:** PATCH model과 저장소 변경은 TDD. HTTP 전달·프로토콜·동시 HTTP·전체 흐름은 동작별 구현 후 테스트.
명확한 버전·전이 실패 기대는 구현 전에 확인하고 실제 네트워크 경계는 연결한 동작마다 검증한다.

1. **Baseline:** 최신 PR2 통합 main에서 기존 명령군을 확인한다.
2. **TDD:** version 필수·bool/실수·추가 필드·빈 변경 거부, v1→v2 담당자+상태 한 번 변경,
   null 해제·완료 후 담당자 변경, 현재값 no-op, 낡은 버전 같은 값 충돌, done→open 거부와 우선순위,
   최대 버전 no-op/변경 거부 순서로 시험·실패·구현·통과를 남긴다. 한 트랜잭션의 버전 검사와
   owner/status/version 한 UPDATE를 사용한다. 최대 버전 fixture는 시험 전용 독립 SQL로 준비한다.
3. **HTTP:** PATCH 연결·오류 매핑을 구현하고 test_http_write에서 실제 결과·전체 행 불변성을 검사한다.
   test_http_protocol은 raw socket으로 중복 Content-Length/Transfer-Encoding/조기 EOF/timeout,
   MIME·크기 경계·중복 JSON 키·비정수 버전·미지원 메서드·Origin·OFF 우선순위를 검사한다.
   Python 파서 자체 제한의 4xx 예외와 HEAD 본문 없음 등 contracts의 예외도 구분한다.
4. **경합:** test_http_race에서 실제 ThreadingHTTPServer와 독립 연결 두 개, 같은 v1에서 서로 다른 owner를
   보내는 barrier를 사용한다. 송신 시작·응답 시점을 기록해 두 작업 구간이 겹쳤는지 확인한다.
   필요하면 시험 harness에서만 두 handler가 서비스에 진입한 뒤 함께 진행시키는 barrier를 둔다.
   저장소·버전 검사·트랜잭션은 대체하지 않는다. 겹침 근거 없이 순차 결과만 있으면 AC8 미검증이다.
   정상 조건은 정확히 한 200/한 409와 최종 v2·승자 값. 별도로 no-op 경합과 잠금 timeout을 검사한다.
5. **전체 흐름:** test_release에서 같은 임시 DB로 OFF 시작·health → ON 가져오기 → GET → 변경 → GET/CSV →
   프로세스 종료·OFF 재시작을 검증한다. OFF에서도 기존 CLI와 health는 정상이고 요청은 보존돼야 한다.
   200행/5개 담당자 이내의 결정적 합성 입력도 한 번 사용해 전체 왕복을 확인하되 처리량/SLA를 주장하지 않는다.
6. **Done:** 아래 전체 명령·Proof의 모든 AC와 명시된 실패 분기 통과, 최신 diff 독립 검토 후 사용자에게
   로컬 코드 통합을 제출한다. 머지된 실제 main에서 재확인한 뒤 공개 판단 자료를 제출한다.
   사용자의 최종 공개 수락 전까지 기본 OFF를 유지하며 플래그를 삭제하거나 기본값을 바꾸지 않는다.

### 공통 검토·로컬 통합

각 PR은 구현·시험·관련 사용법·변경 이유와 execution 기록을 묶는다. 사용자가 읽을 제출물에는 기준 main SHA,
현재 HEAD와 uncommitted/untracked 파일 목록, 포함 범위·남은 AC, 실제 명령·결과·미실행 사유를 적는다.
아직 원격 PR이 없으므로 원격 PR 번호나 URL을 만들지 않는다. PR1–3은 로컬에서 검토할 변경 묶음 이름이다.

구현 완료 보고 전에는 sdlc-feedback의 fresh-context 검증을 수행하고 결과를 기다린다. 새 검증자는
`.codex/agents/sdlc-verifier.toml`의 developer_instructions를 읽게 한다. named agent 선택을 지원하지 않는
런타임이면 fresh child에 최소 인계만 주고 gpt-5.6-sol/high를 명시한다. 기대 근거를 먼저 주고 D1/D2/plan 수락,
정본 집합·현재 PR 범위·diff 기준·미추적 파일·실행 결과·loopback 한계를 전달한다. 검증자는 읽기·시험만 하며
수정·Git 변경·승인을 하지 않는다. 결과는 execution에 보존하고 지원하는 close 동작이 있으면 닫는다.
도구가 없으면 한계를 기록하고 독립 검토 완료로 표시하지 않는다. 이번 문서 작성에는 구현 완료 검토를 실행하지 않는다.

사용자가 stage/commit하고 SHA·코드 검토 결정을 알려 주면 기록한다. 사용자에게 최신 main과 결합한 작업 트리를
준비받아 해당 PR까지의 전체 회귀·ON/OFF를 확인한다. main이 움직이지 않아 그 내용이 이미 시험한 트리와 같다면
동일성 근거를 기록해 불필요한 중복 실행을 피한다. 충돌 해결·main 변경으로 내용이 바뀌면 관련 시험과 검토를 갱신한다.
사용자가 merge commit으로 main에 통합한 뒤 실제 머지 SHA·부모·내용을 확인하고 누락된 결합 검증을 수행한다.
이미 검증한 결합 내용과 동일하면 그 근거를 남겨 재사용한다. 이전 브랜치 통과만으로 통합 성공을 추정하지 않는다.
다음 PR은 확인한 최신 main에서 시작한다. 선행 PR 미통합 상태의 의존 구현은 이번 계획에서 하지 않는다.

## Risks

| 위험 | 발견 방법 | 대응·중지 조건 |
|---|---|---|
| OFF 우회·서버 시작의 DB 생성 | AC11, 파일 접근 spy + 실제 부재 경로/기존 DB 비교 | 모든 제품 진입점과 실제 효과 경계의 같은 guard를 수정. 일반 ON 금지 |
| 일부 가져오기·경합 중 덮어쓰기 | 실제 SQLite·두 프로세스·독립 SQL snapshot·예외 주입 | 검사/쓰기를 같은 잠금에 유지. 행 불변성이 깨지면 다음 PR로 인계하지 않음 |
| no-op/낡은 버전 순서 오해 | 명시 v1/v2 기대·역전이 우선순위·실제 두 연결 | 버전 검사를 값 비교보다 먼저. 기대값을 코드에 맞춰 바꾸지 않음 |
| SQLite 스키마 검사·URI 경로·잠금 | 합성 비호환 DDL, %/?/# 경로, 보유 잠금 | 수락 스키마 밖은 거부. 자동 migration 추가 금지 |
| OpenAPI와 엄격 parser 차이 | wire 1.0·중복 키 등 구속 계약 사례와 스키마 필드 대조 | 스키마 자체가 모든 lexical 규칙을 표현한다고 주장하지 않음 |
| HTTP 실행 제한 | bind/socket 실제 오류·환경·명령 기록 | 저장소 시험은 계속, HTTP는 사용자 실행 결과 대기. skip을 통과로 표시하지 않음 |
| CSV/API의 공통 오류 | 독립 고정 행 목록·csv.reader·바이트 검사 | 상호 일치만으로 성공 판정 금지 |
| 출력 실패의 오해 | commit 후 응답 단절·stdout 실패 사례 | 쓰기 성공 여부는 다시 조회. 응답 실패를 자동 롤백 약속으로 바꾸지 않음 |
| 대화 없이 인계·오래된 main | D1/D2/plan 수락·diff·실행 기록·실제 main 대조 | 수락 기록 없으면 해당 단계 확인. 기존 수락을 다시 승인받지는 않음 |

## Proof

모든 새 시험 경로·명령은 아래 PR에서 만들 예정이며 아직 실행 가능한 제품 검증으로 보고하지 않는다.
기존 test_tracker만 이미 존재한다. 테스트는 unittest·tempfile·sqlite3·http.client/socket·csv·subprocess 등
표준 라이브러리를 쓴다. fixture 기대를 제품 model/storage/parser로 계산하지 않는다.

| 근거 | 시험 정본·PR | 독립 기대·완료 기준 |
|---|---|---|
| P1 / AC1 | test_tracker, test_cli / 전 PR | 기존 파일의 순서 R-203,R-201,R-205,R-202,R-204; 출력 열·종료 코드·단일 대상 변경·반복 완료·flag 독립성 |
| P2 / AC2,3 | test_config_model, test_import_storage, test_cli / PR1 | requests.json 5행 원문 + version 1. 빈/추가/누락/중복/부적합 입력은 전체 거부·원본 바이트 불변 |
| P3 / AC9,13 | test_import_race, test_import_storage / PR1 | 두 작업 하나 성공. 0바이트/빈 SQLite/빈 유효 스키마 허용, 불일치·손상·DB 접근·삽입/커밋 실패 및 잠금 거부 |
| P4 / AC4,5 | test_query_csv, test_http_read / PR2 | spec AC4의 각 ID 목록, R-202 null, 특수 ID의 원문·한 번 decode·404/400 |
| P5 / AC10 | test_query_csv, test_cli, test_http_read / PR2 | 표준 reader 왕복·5열·헤더·CRLF·BOM 없음·독립 기대와 API/CSV 일치 |
| P6 / AC6,7,16 | test_update_storage, test_http_write / PR3 | 현재 v1 → 실제 변경 v2 → 동일 값 v2 → 낡은 v1 충돌. done 역전이 금지·최대 정수 경계 |
| P7 / AC8 | test_http_race / PR3 | 실제 독립 HTTP 연결 두 쓰기의 겹침·한 200/한 409·최종 v2. 순차 호출/모의 repository는 불충분 |
| P8 / AC11 | test_config_model, test_cli, test_http_base / 전 PR | 정확히 1만 ON, OFF는 입력/DB 미접근, health·기존 CLI·help 보존 |
| P9 / AC13,14 | test_import_storage, test_query_csv, test_update_storage, test_http_protocol / 해당 PR | 오류/충돌/읽기 전후 명시 열 전체 불변. 오류 메시지의 입력/경로/예외 비노출. raw protocol 부정 사례 |
| P10 / AC12,15 | test_release + execution/decisions / PR3 및 통합 | 같은 코드에서 ON 검증·OFF 복귀·health·기존 CLI, 실제 머지/공개는 사람의 별도 결정 |

독립 문자열 fixture에는 `" x "`, `"X"`, `"x"`, `"가"`, 조합형 문자열, `"a/b%+?"`, `"null"`,
쉼표·큰따옴표·CR/LF를 담은 제목을 포함한다. Python 문자열/UTF-8 원문과 명시 기대를 직접 준비한다.
불변성 snapshot은 시험 코드의 명시 SELECT로 전체 5열을 읽고 비교한다. 원본 JSON은 바이트 비교한다.
stdout/네트워크 단절·주입 실패 시험이 운영 디스크 고장·무손실을 증명하지는 않는다.

### 예정 명령

아래 명령은 저장소 루트에서 실행한다. PR1에서 tests/__init__.py를 추가한 뒤 모듈별 명령을 사용할 수 있다.
각 시험은 필요한 ON/OFF 환경을 스스로 분리하고 부모 환경 값에 성공이 좌우되지 않게 한다.

```sh
# 현재 존재하는 baseline
python3 -m unittest discover -s tests -p 'test_tracker.py' -v
# PR1: loopback 불필요
python3 -m unittest -v tests.test_config_model tests.test_import_storage tests.test_import_race tests.test_cli
# PR1: loopback 필요
python3 -m unittest -v tests.test_http_base
# PR2 추가: loopback 불필요 / 필요
python3 -m unittest -v tests.test_query_csv
python3 -m unittest -v tests.test_http_read
# PR3 추가: loopback 불필요 / 필요
python3 -m unittest -v tests.test_update_storage
python3 -m unittest -v tests.test_http_write tests.test_http_protocol tests.test_http_race tests.test_release
# 각 PR 통합: 그때 존재하는 전체 시험
python3 -m unittest discover -s tests -v
# 제품 패키지가 생긴 뒤 문법·diff 확인
python3 -m compileall -q service.py request_service tests
git diff --check
```

test_cli는 서버 시작 시험을 넣지 않아 loopback 없이 실행 가능하게 유지한다. 실제 CLI serve 시작·종료·포트 충돌·
기본 127.0.0.1 bind는 test_http_base에서, 최종 재시작 흐름은 test_release에서 검사한다.
별도 linter/OpenAPI validator/CI는 설치하지 않는다. OpenAPI JSON 파싱·내부 참조와 응답 필드 대조는
test_http_read/write의 계약 확인에 포함하되 전용 validator 통과라고 부르지 않는다.

### 사람이 대행하는 loopback 검증

에이전트 환경에서 한 번 실행해 bind 제한 등 이유를 확인하면 같은 제한을 반복 우회하지 않는다.
비네트워크 명령군을 완료하고 사용자에게 **시험할 정확한 커밋 SHA 또는 미커밋 파일 목록·diff**, 작업 디렉터리,
Python/SQLite 버전, 위 해당 PR의 loopback 명령과 기대를 함께 제출한다. 시험 코드는 먼저 구현·검토해서
사람이 명령을 그대로 실행할 수 있게 한다. 없는 시험 파일을 지금 실행하라고 요청하지 않는다.

사용자는 로컬에서 같은 코드로 명령을 실행하고 다음을 돌려준다: `git rev-parse HEAD`, `git status --short`,
실행 명령·종료 코드·unittest 전체 요약/실패 출력. AC8/9 시험은 두 작업의 UTC 시작·종료와 monotonic 겹침,
각 응답 코드·최종 명시 행을 합성 시험 결과로 출력한다. 제품 운영 로그는 만들지 않는다.
테스트가 자신의 임시 DB·동적 포트·프로세스를 생성하고 종료하므로 실데이터 경로를 받지 않는다.

PR1은 test_http_base, PR2는 여기에 test_http_read, PR3는 모든 loopback 모듈을 실행한다.
가능하면 사용자는 해당 판의 전체 unittest 명령도 실행한다. 결과가 없으면 해당 AC는 미검증으로 남겨
통합 완료/최종 공개 준비 완료를 보고하지 않는다. stub·skip·서비스 직접 호출로 HTTP 근거를 대신하지 않는다.
실패하면 에이전트가 원인과 영향 범위를 수정하고 바뀐 판의 필요한 명령만 다시 인계한다.

### 기록·공개·중단

execution.md에 PR/AC별 실제 코드판·diff 범위·명령·기대·실제 결과·실패 원인·TDD 여부·환경 한계·독립 검토 결과를
남긴다. 매 시험별 새 파일/커밋을 만들 필요는 없다. 사람 실행 근거는 사용자 제공임을 표시한다.
수락·코드 통합·공개·중단은 decisions.md에 대상 SHA·결정자 역할·결정·근거를 기록한다.

최종 공개는 같은 수락 코드에서 사용자가 시험할 프로세스의 `REQUEST_SERVICE_ENABLED=1`을 설정하는 것이다.
기본값이나 코드를 바꾸지 않는다. 승인 범위는 동일 기기의 합성 데이터이며 사내망/실데이터 사용이 아니다.
중단은 사용자 서버 종료 후 flag 제거/0으로 재시작, health·직접 차단·기존 저장 행 확인 순서다.
이미 커밋한 변경은 유지되며 DB 삭제·자동 복구는 하지 않는다. 플래그 제거는 별도 변경이다.
