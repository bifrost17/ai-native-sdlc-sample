# 저장소와 실행 경계

## 데이터 계약

입력 파일은 BOM 없는 UTF-8 JSON으로 최상위 키가 정확히 `requests` 하나인 객체다.
requests는 비어 있지 않은 배열이다. 빈 배열은 invalid_input으로 거부해 성공한 초기 가져오기의 의미를
분명히 한다. 각 행은 정확히 id/title/owner/status 네 키를 가진 객체다. 모든 깊이의 중복 JSON 키,
NaN/Infinity, 잘못된 UTF-8·고립 surrogate를 거부한다. JSON 공백과 키 순서는 자유다.
추가/누락 필드는 거부한다. version을 JSON 입력에 추가해도 거부한다.

id/title은 Python 문자열이면서 `value.strip()`이 빈 값이 아니어야 한다. owner는 이 조건의 문자열 또는
null이다. strip은 검사에만 쓰며 저장값은 원문이다. UTF-8로 표현 가능한 Unicode scalar 문자열만 받는다.
문자열의 길이·ID 접두어·문자 집합·담당자 목록 제한은 추가하지 않는다. status는 정확히 open/done이다.
중복 ID는 원문 문자열의 정확 일치로 판단한다. 공백·대소문자·Unicode 정규화 형태가 다르면 별도 값이다.

반환용 Request는 다음 다섯 필드만 가진 불변 DTO다. SQL은 이 열만 명시 조회하며 엔티티 전체 반환·SELECT *를 쓰지 않는다.

| 필드 | 타입·제약 | 변경 |
|---|---|---|
| id | 문자열, 위 규칙, 고유·BINARY 비교 | 초기 가져오기 후 불변 |
| title | 문자열, 위 규칙 | 초기 가져오기 후 불변 |
| owner | 문자열 또는 null | PATCH로 교체·해제 |
| status | open 또는 done | open→done, 동일 값 가능 |
| version | bool을 제외한 정수 1–9223372036854775807 | 초기 1, 실제 값 변경 시 정확히 +1 |

현재 버전·현재 값의 no-op는 최대 버전에서도 성공한다. 최대 버전에서 실제 변경은 version_exhausted이며
모든 값이 불변이다. 음수·0·상한 초과·bool·JSON 실수 버전은 invalid_input이다.

## 구조와 내부 계약

| 경계·제안 파일 | 책임·계약 |
|---|---|
| service.py, request_service/cli.py | 인자·환경 읽기, import-json/serve/export-csv, stdout/stderr·종료 코드 |
| request_service/config.py | 환경 값 정확히 1 여부만 판정. 평가 실패는 False. import 시 파일/DB 부수 효과 없음 |
| request_service/model.py | Request/RequestPatch/RequestFilter, 엄격 JSON 파싱과 타입 검증, ServiceError(code) |
| request_service/service.py | RequestService(db_path, enabled), 업무 guard와 저장소 호출 |
| request_service/storage.py | 연결·스키마 확인·명시 SQL·트랜잭션. transport·출력과 독립 |
| request_service/http.py | 병렬 HTTP 연결별 parsing·DTO JSON·오류 매핑·고정 loopback bind |
| request_service/csv_export.py | 조회 DTO 목록을 UTF-8 CSV 바이트로 직렬화. DB 쓰기 없음 |

이 이름들은 구현자가 경계를 추측하지 않도록 정한 제안이다. 함수 내부 보조 분할은 plan에서 정할 수 있으나
계약·경계를 바꾸면 spec도 갱신한다. 패키지 내부 repository는 외부 공개 명령이 아니며 모든 제품 진입점은
RequestService를 거친다. 외부에서 DB 파일을 직접 수정하는 것은 이 시제품 API 계약 밖이다.

| RequestService 메서드 | 입력·출력·오류 |
|---|---|
| import_json(path) | gate → 파일 읽기·전체 검증 → 저장소 초기 가져오기. 반환 imported 정수, 실패는 ServiceError |
| list_requests(owner=None, status=None) | gate → 필터 검증 → 명시 열 조회. None은 필터 생략. 반환 ID 정렬 Request 목록 |
| get_request(id) | gate → ID 검증 → 조회. 반환 Request, 없으면 not_found |
| update_request(id, patch) | gate → 입력 검증 → 원자적 변경. patch는 version 필수와 owner/status의 누락을 구분. 반환 커밋한 Request |

model 검증은 HTTP뿐 아니라 service에서 호출해 CLI/내부 시험이 잘못된 값을 저장하지 못하게 한다.
HTTP는 framing·경로·쿼리의 transport 검증을 추가한다. repository는 ServiceError에 대응하는 저장소 오류만
외부에 전달한다. 원본 예외를 str로 붙이지 않는다. 예상하지 못한 예외는 HTTP internal_error, CLI는
internal_error와 종료 5로 처리한다. 업무 guard에서 OFF이면 저장소 생성자도 파일 접근을 하지 않아야 한다.

## SQLite 스키마와 파일 수명

스키마 버전은 `PRAGMA user_version=1`이다. SQLite 일반 파일 한 개에 아래 테이블만 둔다.
사용자 입력은 항상 SQL 바인딩 파라미터로 전달하며 필터 SQL 조각은 고정된 owner/status 조건만 조합한다.

```sql
CREATE TABLE requests (
  id TEXT NOT NULL COLLATE BINARY PRIMARY KEY,
  title TEXT NOT NULL,
  owner TEXT,
  status TEXT NOT NULL CHECK(status IN ('open', 'done')),
  version INTEGER NOT NULL CHECK(typeof(version) = 'integer' AND version >= 1)
);
```

문자열 상세 검증은 model이 담당한다. SQLite의 암묵적 변환에 입력 검증을 맡기지 않는다.
스키마 확인은 user_version, 요청 테이블의 열 이름·선언 타입·NOT NULL·PK, status/version CHECK,
사용자 테이블·view·trigger 구성을 확인한다. 이 설계의 스키마와 다르거나 무관한 사용자 객체가 있으면
store_unavailable로 거부한다. SQLite가 생성한 내부 인덱스는 허용한다. 자동 migration은 없다.

가져오기만 DB를 생성한다. 대상이 없거나 0바이트 파일, 또는 user_version=0이고 사용자 객체가 전혀 없는
유효한 SQLite이면 트랜잭션 안에서 스키마를 만든다. 버전 1의 일치 스키마이면서 요청이 0행이면 가져올 수 있다.
그 외 스키마·깨진 DB·부모 경로 없음·접근 실패는 store_unavailable다. 기존 요청이 있으면 store_not_empty다.
빈 DB에 임의의 성공 마커를 따로 저장하지 않는다. 제품에 삭제 기능이 없어 성공 뒤에는 항상 요청이 남는다.

조회/CSV는 기존 파일에 read-only 연결, 변경은 기존 파일에 read-write(생성 금지) 연결을 사용한다.
새 DB 연결은 SQLite URI의 예약 문자를 안전하게 인코딩한다. 파일 경로로 SQL/URI 옵션을 삽입할 수 없어야 한다.
read-only 조회는 스키마를 바꾸지 않는다. 연결마다 user_version·구조를 확인하며, 서버 시작에는 연결하지 않는다.
커넥션을 스레드 간 공유하지 않고 요청 또는 CLI 작업 종료 시 닫는다.

journal_mode는 DELETE, synchronous는 FULL을 사용한다. 쓰기 연결에서 WAL로 전환하지 않는다.
잠금 대기 한도는 연결별 5초다. 이는 회사 정책/성능 SLA가 아닌 구현 제안이다. 잠금/커밋에 따른 DB 저널은
SQLite 복구용 기술 파일이며 운영 감사 로그 기능이 아니다. 예상 저장소 손상·전원/디스크 고장까지 무손실을 보장하지 않는다.

## 가져오기 원자성

1. gate를 확인한 뒤 파일 전체를 읽고 JSON/행/중복 ID 검증을 끝낸다. 이 시점까지 DB를 열지 않는다.
   입력 읽기 오류는 input_unavailable, 형식 오류는 invalid_input이다.
2. DB 연결 후 `BEGIN IMMEDIATE`로 쓰기 잠금을 얻는다. 잠금 안에서 스키마 적합성과 요청이 없음을 확인한다.
   검사와 삽입을 별도 트랜잭션으로 나누지 않는다. 입력 오류와 기존 데이터가 함께 있으면 입력 오류가 우선이다.
3. 필요 시 스키마와 user_version을 만들고 모든 행을 version=1로 삽입한다. 전부 성공하면 COMMIT한다.
4. 예외·삽입/커밋 실패 시 ROLLBACK하고 연결을 닫는다. 기존 요청을 변경하지 않는다. 이번 실행으로 새 파일이
   생겼다면 빈 SQLite/0바이트 파일은 남을 수 있으나 일부 요청·부분 스키마는 남기지 않는다. 실패 시 파일을
   자동 삭제하면 다른 프로세스의 성공 DB를 지울 수 있어 삭제하지 않는다.

동시 가져오기 두 작업은 같은 DB 잠금을 사용한다. 첫 성공 뒤 두 번째는 잠금을 얻고 요청 존재를 다시 검사해
store_not_empty다. 한쪽이 5초 넘게 잠금을 잡으면 다른 쪽은 store_busy일 수 있다. 정상 단기 경합 시험에서는
정확히 하나 성공·하나 store_not_empty를 요구하고 별도 잠금 유지 시험에서 timeout을 확인한다.

## 변경·조회 원자성

변경은 BEGIN IMMEDIATE → ID 조회 → 전달 버전 비교 → 상태 전이 확인 → 값 비교 순서다.
ID가 없으면 not_found, 버전이 다르면 같은 값도 version_conflict, 현재 done에서 open이면 invalid_transition이다.
아무 값도 달라지지 않으면 쓰지 않고 트랜잭션을 끝내 현재 Request를 반환한다.
실제 값이 하나라도 다르면 version+1로 owner/status를 한 UPDATE에서 바꾼다. WHERE에는 id와 읽은 version을
함께 지정하고 영향 행 수가 1인지 확인한다. 0이면 version_conflict로 롤백한다. 성공 반환값은 트랜잭션 안의
변경 결과를 DTO로 보관하고 COMMIT한 뒤 반환한다. 그 직후 다른 쓰기가 있어도 반환은 이 변경의 결과다.

같은 버전으로 서로 다른 실제 변경이 경합하면 쓰기 잠금으로 한쪽을 먼저 처리하고 다른 쪽은 최신 버전을 읽어
충돌한다. no-op가 먼저 성공하면 버전을 올리지 않으므로 뒤의 실제 변경도 성공할 수 있다. 이는 두 실제 변경이
동일 버전을 덮어쓰는 경우와 다르다. no-op와 실제 변경의 경합에서는 최종 데이터와 반환 버전으로 판정한다.

조회는 명시 열과 `ORDER BY id COLLATE BINARY ASC`를 사용한다. BINARY는 대소문자·원문을 구분하며
자연수 정렬이 아니다(R-10이 R-2보다 앞설 수 있음). 필터는 BINARY 정확 일치, 조합은 AND다.
목록 한 SELECT를 끝까지 읽어 하나의 일관된 snapshot을 얻고 연결을 닫는다. API와 CSV는 같은 함수를 호출한다.
업무 데이터/버전을 갱신하는 읽기 부수 효과는 없다. 숨은 access/updated_at 컬럼도 없다.

잠금 만료는 store_busy, 나머지 접근·스키마·SQLite 실패는 store_unavailable다. 서비스는 자동 재시도하지 않는다.
COMMIT 뒤 네트워크·stdout 실패는 이미 확정한 데이터를 되돌리지 않는다. 클라이언트가 다시 읽어 현재 상태를
판단한다. 쓰기 재전송에 오래된 version을 그대로 사용하면 충돌하며 자동으로 최신 버전을 대입하지 않는다.
