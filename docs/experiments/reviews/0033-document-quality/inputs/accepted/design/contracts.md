# 인터페이스 계약

이 문서는 spec.md와 같은 판으로 읽는 설계 정본이다. 명령·이름·오류·기술 한도는 PO 수락 전 제안이다.

## CLI

새 진입점은 저장소 루트의 `service.py`다. 모든 경로는 호출자의 현재 디렉터리 기준이며 DB 경로를
명시하게 해 잘못된 저장소 사용을 줄인다. 부모 디렉터리는 자동 생성하지 않는다.

```text
python3 service.py --db PATH import-json JSON_PATH
python3 service.py --db PATH serve [--port PORT]
python3 service.py --db PATH export-csv [--owner OWNER] [--status open|done]
```

DB 인자는 하위 명령 앞에 둔다. --port 기본값은 8765, 허용 범위는 1–65535의 십진 정수다.
바인드 주소는 항상 127.0.0.1이며 --host는 제공하지 않는다. 테스트 내부에서 서버 생성자에 포트 0을
전달해 임시 포트를 쓸 수 있으나 공개 CLI 계약은 아니다. 중복 옵션·알 수 없는 옵션·여분 인자는 거부한다.
`--help`는 루트/하위 명령 모두 flag·DB 존재 여부에 관계없이 stdout, 종료 0이다.

`REQUEST_SERVICE_ENABLED=1`만 ON이다. CLI는 인자 구문 검사 후 gate를 확인하고, OFF면 JSON/DB를
읽거나 생성하지 않는다. serve는 OFF에서도 시작한다. ON serve도 DB는 요청 때 열며, 없는 DB를
만들거나 초기화하지 않는다. import-json 성공 시 stdout은 `{"imported":5}` 같은 한 줄 JSON과 LF,
export-csv 성공 시 stdout은 CSV만, serve는 시작 성공 후 `127.0.0.1:8765에서 요청을 받습니다.`를
stderr에 한 줄 출력한다. 주소는 실제 선택 포트다. 운영 요청별 로그는 출력하지 않는다.

| 종료 코드 | 의미 |
|---|---|
| 0 | help, 가져오기/CSV 성공, 정상 서버 종료 |
| 2 | invalid_input(인자·입력 JSON), 포트 범위 오류 |
| 3 | feature_disabled |
| 4 | store_not_empty |
| 5 | store_unavailable, store_busy, input_unavailable, output_unavailable, 서버 bind 실패 |

Ctrl-C는 서버 종료를 요청하고 진행 중 요청을 정리한 뒤 정상 종료한다. bind 실패는 server_unavailable로
종료 5다. CLI 오류는 stderr에 `코드: 고정 문구\n`, stdout은 비어 있다. 단, stdout 출력 도중 OS 오류는
일부 CSV/JSON 바이트가 이미 전송되었을 수 있으며 output_unavailable로 종료 5다. DB 쓰기를 되돌리지 않는다.
오류 메시지에 파일 경로·입력값·원본 예외를 붙이지 않는다. argparse 기본 오류 대신 이 계약에 맞춰 처리한다.

## HTTP

서버는 HTTP/1.0 응답과 요청당 연결 종료를 사용한다. 병렬 연결은 별도 스레드로 처리한다.
모든 응답은 UTF-8 JSON, `Content-Type: application/json; charset=utf-8`, 바이트 기준 Content-Length,
`Connection: close`, `Cache-Control: no-store`를 포함한다. JSON 키 순서·공백은 계약이 아니다.
기본 HTML 오류와 Python 버전 노출은 사용하지 않는다. access log와 traceback 출력도 억제한다.

| 메서드·경로 | 입력 | 성공 |
|---|---|---|
| GET /health | 쿼리·본문 없음 | 200 `{"status":"ok"}`. DB와 flag에 무관한 생존 확인 |
| GET /requests | 선택 owner/status 쿼리 | 200 `{"requests":[Request,...]}`. 빈 결과는 빈 배열 |
| GET /requests/{id} | URL 인코딩한 ID 한 경로 조각 | 200 `{"request":Request}` 또는 404 not_found |
| PATCH /requests/{id} | `{"version":1,"owner":null,"status":"done"}`의 부분 변경 | 200 `{"request":Request}`. owner/status 중 하나 이상 필수 |

Request는 명시적으로 `id,title,owner,status,version`만 반환한다. JSON 타입과 문자열 규칙은 storage.md와
openapi.json을 따른다. id/title을 수정할 수 없다. 생성·삭제·가져오기·CSV HTTP endpoint는 없다.
PATCH의 owner/status 생략은 현재 값 유지, owner=null은 배정 해제다. status=null은 잘못된 입력이다.
응답 성공은 트랜잭션 커밋 후에만 전송한다. 응답 손실 시 클라이언트가 다시 조회한다. 자동 쓰기 재시도는 없다.

### 경로와 쿼리 파싱

경로를 먼저 `/`로 나누고 ID 조각을 percent decode 한 번만 한다. slash가 포함된 ID는 `%2F`, percent는
`%25`, 물음표는 `%3F`로 인코딩한다. ID의 `+`는 그대로, 쿼리의 `+`는 공백이다. UTF-8 디코딩은 엄격하며
깨진 percent/UTF-8은 invalid_input이다. 디코딩 후에도 문자열은 trim·casefold·정규화하지 않는다.
빈 ID·공백만 ID는 invalid_input. 끝 slash는 자동 리디렉트하지 않고 route_not_found다.

목록 쿼리는 owner/status만 허용하고 각각 최대 한 번이다. 순서는 무관하고 조합은 AND다.
owner는 비어 있지 않고 공백만이 아닌 문자열을 정확히 비교한다. `owner=null`은 문자열 "null" 담당자다.
null 전용 필터는 이번에 추가하지 않는다. owner 생략은 null 포함 전체다. status는 open/done만 허용한다.
빈 값·중복 키·알 수 없는 키는 invalid_input이다. `GET /requests?`는 필터 없음과 같다.
health·단건·PATCH에는 쿼리를 허용하지 않는다(빈 `?` 제외). 절대 URL request target과 fragment는 거부한다.

### 요청 검증과 오류 우선순위

1. HTTP 구문을 파싱할 수 없으면 400 invalid_input. 파싱 가능한 경우 `/health`를 제외한 모든 요청은
   OFF일 때 503 feature_disabled로 종료하고 본문·DB를 읽지 않는다. `/health`도 GET 외 메서드는 405다.
2. ON 및 health에서 Origin 헤더가 있으면 403 origin_not_allowed. 브라우저 CORS를 제공하지 않는다.
   이는 인증이 아니며 같은 기기의 프로세스가 호출 가능한 전제는 변하지 않는다.
3. 경로 디코딩과 라우트를 확인한다. 알 수 없는 경로는 404 route_not_found, 알려진 경로의 미지원
   메서드(HEAD/OPTIONS 포함)는 405 method_not_allowed와 Allow(GET 또는 GET, PATCH)다.
   HEAD 응답은 동일한 오류 헤더를 주되 HTTP 규칙에 따라 본문을 전송하지 않는다.
4. 쿼리, 본문 framing, MIME, JSON/필드 순으로 검사한다. GET은 본문 없음 또는 Content-Length: 0만
   허용한다. 모든 Transfer-Encoding과 중복/음수/비십진 Content-Length는 400 invalid_input이다.
   PATCH Content-Length 누락은 411 length_required, 0은 400 invalid_input이다.
5. PATCH는 최대 1,048,576바이트다. 초과는 본문 읽기 전에 413 payload_too_large. 이는 로컬 시제품의
   메모리 제한 제안이며 회사 정책 한도가 아니다. MIME은 application/json, 선택 charset=utf-8만 허용하며
   토큰 대소문자는 무시한다. MIME 누락·다른 형식/charset은 415 unsupported_media_type이다.
6. 연결 읽기 timeout은 5초, 시간 안에 명시 길이를 못 읽으면 408 request_timeout 또는 조기 EOF의
   400 invalid_input이며 DB에 접근하지 않는다. 연결 단절로 응답을 전달할 수 없으면 응답 보장은 없다.
7. 본문은 BOM 없는 UTF-8 JSON 객체다. 중복 키, NaN/Infinity, 고립 surrogate, 추가 필드, bool/실수 버전,
   owner/status 없는 변경은 400 invalid_input이다. storage의 필드 규칙도 검사한다.
8. 저장소를 확인하고 트랜잭션에서 ID 존재 → 버전 일치 → 상태 전이 → 실제 차이 순서로 판단한다.
   따라서 오래된 버전의 done→open도 version_conflict다. 현재 버전의 done→open은 invalid_transition이다.

HTTP 파서 자체의 헤더/요청줄 크기 제한은 표준 서버의 제한을 사용한다. 이 범위의 초과 거부는 4xx로
처리하되 세부 코드 동일성은 보장하지 않는다. 요청 데이터에 접근하지 않고 원본 입력을 오류에 넣지 않는다.

### 오류 응답과 문구

HTTP 오류 본문은 `{"error":{"code":"version_conflict","message":"다른 변경이 반영됐습니다. 다시 조회한 버전으로 변경해 주세요."}}` 형태다.
아래 표 외 임의 필드·현재 요청값·SQL·파일 경로·원본 예외를 넣지 않는다. CLI도 같은 코드·문구를 쓴다.

| 코드 | HTTP | 고정 message |
|---|---|---|
| feature_disabled | 503 | 새 요청 기능이 꺼져 있습니다. 시험 설정을 확인해 주세요. |
| invalid_input | 400 | 입력 형식이 맞지 않습니다. 필드와 값을 확인해 주세요. |
| not_found | 404 | 요청을 찾을 수 없습니다. ID를 확인해 주세요. |
| route_not_found | 404 | 지원하지 않는 경로입니다. API 경로를 확인해 주세요. |
| method_not_allowed | 405 | 지원하지 않는 메서드입니다. 허용된 메서드를 사용해 주세요. |
| origin_not_allowed | 403 | 브라우저 출처가 있는 요청은 받지 않습니다. 로컬 HTTP 클라이언트를 사용해 주세요. |
| version_conflict | 409 | 다른 변경이 반영됐습니다. 다시 조회한 버전으로 변경해 주세요. |
| invalid_transition | 409 | 완료된 요청은 미완료로 되돌릴 수 없습니다. |
| length_required | 411 | 본문 길이가 필요합니다. Content-Length를 지정해 주세요. |
| payload_too_large | 413 | 요청 본문이 허용 크기를 넘었습니다. 본문을 줄여 주세요. |
| unsupported_media_type | 415 | UTF-8 JSON 본문이 필요합니다. Content-Type을 확인해 주세요. |
| request_timeout | 408 | 본문을 제시간에 받지 못했습니다. 연결을 확인해 주세요. |
| store_unavailable | 503 | 저장소를 사용할 수 없습니다. 경로와 초기 가져오기 상태를 확인해 주세요. |
| store_busy | 503 | 저장소가 사용 중입니다. 잠시 뒤 다시 조회해 주세요. |
| version_exhausted | 409 | 버전을 더 늘릴 수 없습니다. 담당 엔지니어에게 알려 주세요. |
| internal_error | 500 | 요청을 처리하지 못했습니다. 담당 엔지니어에게 알려 주세요. |
| store_not_empty | CLI 전용 | 요청이 이미 있어 가져올 수 없습니다. 빈 저장소를 지정해 주세요. |
| input_unavailable | CLI 전용 | 입력 파일을 읽을 수 없습니다. 파일과 접근 권한을 확인해 주세요. |
| output_unavailable | CLI 전용 | 출력을 전달하지 못했습니다. 출력 연결을 확인해 주세요. |
| server_unavailable | CLI 전용 | 서버를 시작할 수 없습니다. 포트 사용 상태를 확인해 주세요. |

## CSV

export-csv는 HTTP를 호출하지 않고 같은 RequestService.list_requests와 같은 DB 경로를 사용한다.
API와 함께 쓸 때 호출자가 같은 --db를 지정한다. 필터 규칙은 HTTP와 같고 옵션 생략도 같은 의미다.
조회 한 번의 일관된 결과를 메모리에 받아 CSV 전체를 구성한 뒤 출력한다. 조회/직렬화 실패 시 stdout은 빈 값이다.
Python csv의 excel dialect에 해당하는 쉼표 구분·큰따옴표 quote·내부 quote 두 번·필요 시 quote·CRLF 행 끝을 쓴다.
UTF-8, BOM 없음이며 stdout의 로케일 인코딩과 무관하게 이 바이트를 출력한다.

헤더는 `id,title,owner,status,version`이다. null은 빈 셀, version은 십진 문자열이다. 빈 결과는 헤더와 CRLF만
출력한다. 필드 안의 CR/LF·쉼표·따옴표·한글을 보존한다. 수식 같은 문자열도 원문 그대로이며 접두어를 붙이지 않는다.
CSV 파일 출력 옵션·집계·완료 시각은 없다. 비교 검증 중 다른 쓰기를 멈추면 API와 CSV의 동일 행을 대조할 수 있다.
서로 다른 시점에 조회하면 각각의 일관된 현재 상태를 반환하며 두 호출 사이 snapshot 고정은 제공하지 않는다.
