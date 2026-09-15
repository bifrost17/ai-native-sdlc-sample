# Spec: 사내 요청 대장의 SQLite 저장소·로컬 HTTP API·CSV
Upstream: intent.md 및 PROJECT-POLICY.md@e1e06501e3bc13bfb09d7d6feb4da3fb12b8b953. Status: draft.
Skills applied: 아래 적용 근거 표 참조.

담당자는 같은 기기의 SQLite 요청 상태를 조회·변경하고 현재 상태를 CSV로 추출한다.
기존 JSON CLI와 새 저장소는 독립적으로 유지한다. 상위 문서는 [D1](decisions.md)로 수락됐다.
현재 사용한 상위 내용은 수락 판 전체이며 후속 업무 변경은 없다. 이 spec의 구체적 계약은 PO 검토용 제안이다.
JWT·감사 이력에 관한 팀 스킬과 시제품 범위의 차이는 Flagged concerns에 기록했다. 회사 정책은 미제공이다.

## Requirements

| ID | 바뀔 동작 또는 유지할 계약 | 근거 |
|---|---|---|
| R1 | 기존 tracker.py의 list/show/complete, JSON 사용과 출력·종료 코드·순서를 유지하고 자동 동기화하지 않는다 | intent Constraints, 기존 코드·tests/test_tracker.py |
| R2 | 비어 있는 새 저장소에 검증한 JSON 전체를 한 번 가져온다. 반복·병합·덮어쓰기와 일부 성공을 거부한다 | intent Proposed outcome |
| R3 | 목록·단건 조회, owner/status 정확 필터와 ID 오름차순을 제공하며 업무 데이터를 변경하지 않는다 | intent Proposed outcome |
| R4 | 읽은 버전으로 담당자·상태를 원자적으로 변경한다. 오래된 버전은 같은 값도 충돌이며 유효한 동일 값은 버전 불변이다 | intent Proposed outcome |
| R5 | 같은 저장소·필터·정렬의 현재 상태를 UTF-8 CSV stdout으로 추출한다 | intent Proposed outcome |
| R6 | 새 HTTP·관리 CLI·CSV를 한 공개 단위로 기본 OFF, 시험 ON, 수락 후 같은 코드에서 공개한다. /health와 기존 CLI는 OFF에서도 작동한다 | intent Constraints |
| R7 | 127.0.0.1·합성 데이터에 한정한다. OFF·잘못된 요청·충돌·가져오기 실패로 요청 데이터를 바꾸지 않는다 | intent Constraints, 정책 P2/P3 |
| R8 | 실제 동시 변경과 기존 동작 회귀를 검증하고 실행 근거·수락을 저장소 문서로 보존한다 | intent, 정책 검증과 운영 |

## Acceptance criteria

아래 기대는 상위 합의와 이 설계에서 정한 계약에서 도출한다. 기존 합성 입력의 ID 순서는
`R-201,R-202,R-203,R-204,R-205`가 새 조회의 기대이며 기존 CLI는 원본 파일 순서를 유지한다.
version은 모두 1로 가져온다. 구현 출력을 기대값으로 복사하지 않는다.

| ID → 요구 | 조건·입력·행동 | 관찰할 기대 결과·불변식 |
|---|---|---|
| AC1 → R1 | 기존 세 테스트 및 ON/OFF에서 기존 CLI 실행 | 기존 출력·종료 코드·JSON 변경 범위 보존, 새 DB와 무관. 새 기능으로 원본 JSON 바이트 불변 |
| AC2 → R2 | 제공 합성 5행을 새 DB에 가져오기 | 5행과 version=1, 원문 문자열·null 보존. 같은 입력 또는 다른 입력으로 반복하면 store_not_empty, 기존 행 불변 |
| AC3 → R2,R7 | 빈 배열, 추가/누락 필드, 잘못된 타입·상태·공백 문자열·중복 ID·중복 JSON 키·깨진 UTF-8/JSON | invalid_input. 새 요청 일부가 남지 않음. 기존 DB/원본 JSON 불변. 전체 입력 검증 후 쓰기 시작 |
| AC4 → R3 | 필터 없음·owner=hana·status=done·둘의 AND·불일치·대소문자 차이 | 각각 5행, R-203/R-205, R-204/R-205, hana+done은 R-205, 빈 목록, Hana는 빈 목록. null은 owner 생략 때 포함 |
| AC5 → R3,R7 | 단건 R-202, 없는 ID, 특수문자를 가진 합성 ID의 URL 인코딩, 잘못된/중복 쿼리 | 단건 owner=null, 없는 ID는 404, 인코딩 왕복, 쿼리 거부. 조회·오류 전후 업무 행 불변 |
| AC6 → R4 | R-201 v1의 owner와 status를 한 요청에서 다른 담당자 및 done으로 변경 | 둘 다 반영, v2. R-201 외 행은 불변. null 배정 해제와 완료 후 담당자 변경도 같은 규칙 |
| AC7 → R4 | 현재 버전으로 같은 값; 오래된 버전으로 같은 값/다른 값; done→open; id/title/빈 변경 | 동일 값은 200과 버전 불변. 오래된 버전은 409 version_conflict. 역전이는 409 invalid_transition. 나머지는 400 invalid_input. 실패 시 불변 |
| AC8 → R4,R8 | 독립 HTTP 연결 2개가 같은 v1에 서로 다른 owner 변경을 실제 동시 전송 | 정상 저장소 조건에서 정확히 한 200과 한 409 version_conflict, 최종 v2와 승자 값. 순차 호출로 대체하지 않음 |
| AC9 → R2,R8 | 빈 DB에 초기 가져오기 2개를 동시 실행 | 정상 조건에서 하나만 성공, 다른 하나는 store_not_empty. 전체 행 집합 한 벌만 존재 |
| AC10 → R5 | 전체·필터·빈 결과 CSV를 표준 reader로 읽기 | 정확한 헤더/열 순서, API와 같은 행·정렬, null 빈 셀, version 십진수. 쉼표·따옴표·한글·줄바꿈 원문 복원. BOM 없음 |
| AC11 → R6,R7 | flag 미설정·0·true·공백 등 잘못된 값에서 직접 HTTP/가져오기/CSV 호출 | 새 업무 경계는 feature_disabled, DB 생성·열기·초기화 및 입력 파일 읽기 없음. /health는 200, 기존 CLI·help 정상 |
| AC12 → R6 | 같은 코드의 flag=1 시험과 최종 수락 후 실행, 다시 OFF로 재시작 | ON에서 전체 기능, OFF에서 차단과 /health 유지. OFF 전환이 이미 커밋된 요청을 되돌리지 않음 |
| AC13 → R7 | DB 없음·미지원 스키마·잠금 유지·읽기/쓰기 실패 | 설계의 store_unavailable/store_busy. 읽기·서버 시작은 DB를 만들지 않음. 쓰기 커밋 전 실패는 롤백 |
| AC14 → R7 | body 추가/중복 키, bool/실수 버전, 잘못된 MIME·길이·UTF-8, Origin 포함 요청 | 명시한 HTTP 오류, 요청 데이터 불변, 입력 값·경로·예외·헤더가 오류/운영 로그로 노출되지 않음 |
| AC15 → R6,R8 | 각 부분 PR과 최종 공개 단위 검증 | 부분 ON 결과는 그 부분만 증명. 최종 전체 AC와 OFF 복귀 검증 후 사용자 공개 결정 기록 |
| AC16 → R4 | 최대 버전의 동일 값·실제 변경, 원문 공백·대소문자 보존 | 동일 값은 성공·버전 불변, 실제 변경은 version_exhausted. 유효 문자열은 입력 그대로 저장·조회 |

AC8/9는 barrier로 두 작업을 출발시켜 실행 구간이 겹친 근거와 각 응답·최종 행을 남긴다.
잠금 실패 시험은 별도 연결이 쓰기 잠금을 유지해 수행한다. 요청 불변성은 전후 명시 열의 전체 행 비교,
원본 JSON 불변성은 바이트 비교로 확인한다. DB 파일 바이트 동일성은 SQLite 저널·메타데이터와 구분한다.
실제 명령·개발 검증 순서·PR별 증거는 plan에서 정한다. 이 문서 제출에서 제품 시험을 실행한 것은 아니다.

## Design

### Approach

새 진입점 `service.py`와 `request_service/` 패키지를 제안한다. 기존 tracker.py에는 새 저장소와 flag를
연결하지 않는다. HTTP와 CSV가 같은 저장소 조회 함수를 쓰게 해 필터·정렬의 차이를 막는다.
행 변경은 SQLite 트랜잭션 안에서 버전을 확인한다. JSON 전체 덮어쓰기를 재사용하면 경합에 의한
유실을 막기 어렵고 기존 CLI와 동기화하지 않는 제약도 있으므로 채택하지 않는다.

HTTP는 표준 라이브러리 ThreadingHTTPServer, CSV는 csv, 저장소는 sqlite3를 사용한다.
스레드마다 별도 DB 연결을 열고 짧은 쓰기를 직렬화한다. 이는 예상 규모에 맞춘 제안이며 처리량 보장은 아니다.
추가 서버 프레임워크·인증·외부 서비스·ORM·마이그레이션 도구는 도입하지 않는다.

| 설계 정본 | 소유하는 결정·필수 읽기 범위 |
|---|---|
| [spec.md](spec.md) 전체 | 요구·AC·공개 단위·범위·정책 판단 |
| [design/contracts.md](design/contracts.md) 전체 | CLI/HTTP/CSV 입력·출력·오류·flag와 오류 문구 |
| [design/storage.md](design/storage.md) 전체 | 데이터 타입·스키마·내부 경계·트랜잭션·실패·동시성 |
| [design/openapi.json](design/openapi.json) 전체 | OpenAPI 3.1 API 경로·JSON 필드 스키마·응답 상태 |

이 네 파일을 같은 실제 커밋의 spec 문서 집합으로 수락한다. OpenAPI는 JSON 모양과 라우트,
contracts는 파싱·오류 우선순위와 실행 계약, storage는 원자성·데이터 계약을 소유한다.
겹치는 내용이 불일치하면 구현자가 한쪽을 선택하지 말고 spec을 고친 뒤 진행한다.

### 공개 제어

`REQUEST_SERVICE_ENABLED` 환경 변수가 정확히 `1`일 때만 새 업무 기능을 켠다. 미설정·잘못된 값·평가
실패는 OFF다. 서버는 시작 시 한 번 읽으며 바꾸려면 재시작한다. CLI는 실행마다 읽는다.
HTTP와 관리 CLI 모두 같은 설정 판정과 업무 서비스 guard를 사용한다. 쿼리·헤더·요청 본문으로 켤 수 없다.
프로세스 환경을 설정할 수 있는 동일 기기 사용자를 시험 주체로 전제하며 flag를 인증으로 취급하지 않는다.

서버 OFF 시작은 허용하되 DB를 열지 않는다. /health는 DB 상태와 무관한 생존 확인이다.
가져오기·CSV·HTTP의 업무 경계에서 guard 후에만 파일/DB에 접근한다. 모듈 import나 서버 시작에
DB 생성·migration·업무 쓰기를 하지 않는다. 기존 CLI와 새 CLI help는 공개 단위 밖이다.

개발 중 일반 설정은 OFF, 명시한 시험 프로세스만 ON이다. 작은 PR마다 OFF에서 시작·기존 CLI·직접
차단을 확인하고 ON에서 완성된 부분을 시험한다. 최종 전체 AC와 동일 코드의 ON/OFF 전환을 검증한 뒤
사용자가 코드 SHA·대상(동일 기기 합성 데이터)·설정·근거를 decisions.md에 남겨 공개한다.
구체적인 PR 순서와 검증 방식 선택은 plan의 일이다.

중단은 사용자가 실행 중 프로세스를 종료하고 flag를 제거하거나 0으로 바꿔 재시작한다. 이미 진행 중인
쓰기는 커밋되었을 수 있으므로 OFF가 데이터 복구를 의미하지 않는다. 재시작 후 차단·health와 저장된
행을 확인한다. DB를 자동 삭제·복원하지 않는다. 플래그 제거는 이번 범위 밖이며 별도 변경·수락이 필요하다.

## Constraints and scope

D1의 intent Constraints 및 정책 P1–P3 전체를 이어받는다. 로그인·사내망·실데이터·실제 배포·원격 push,
웹 화면·완료 취소·id/title 변경·수식 방어·완료 시각/이력·운영 로그·감사는 제외한다.
CSV 파일 출력 옵션은 제공하지 않는다. 새 관리 CLI는 import-json/serve/export-csv만 제공하며
별도 로컬 변경 명령은 추가하지 않는다. 쓰기는 HTTP PATCH로 수행한다.
약 200개 요청·5명 담당자는 예상 시험 규모다. 입력 수 상한이나 담당자 등록 제한으로 바꾸지 않는다.
기술적 요청 크기·잠금 대기는 contracts/storage의 제안 값이며 회사 정책 수치가 아니다.

## Open questions

| ID | answered / carried forward | 답과 근거 또는 제안의 검토 시점 |
|---|---|---|
| Q1 업무·공유·데이터 | answered | 사용자 답변과 D1으로 확정. 127.0.0.1·합성 데이터·동시 변경 시험 |
| Q2 입력·API·CLI·저장소 | carried forward | 이 설계의 구체적 제안 전체를 PO가 실제 SHA로 검토·수락. 추가 업무 답변 없이 작성 가능하도록 명시 |
| Q3 공개 flag | carried forward | 환경 변수·기본 OFF·재시작·중단 계약을 제안. PO spec 수락에서 결정 |
| Q4 PR·검증 순서 | carried forward | spec 수락 뒤 plan에서 3~4개 PR 및 독립성·검증 전략 결정. 구현 전 엔지니어 검토 |
| Q5 실제 회사 기준 | carried forward | 이번 시제품 밖. 실제 도입 전 회사 정책 결정자 확인. 사용자에게 회사 기준 승인을 재요청하지 않음 |

## Flagged concerns

| 항목·근거 | 영향·판단·결정자·필요 시점 |
|---|---|
| secure-api-review 1의 gateway JWT와 D1 로그인 제외 | JWT/session을 도입하지 않는다. 127.0.0.1도 인증이 아님을 명시한다. 사용자 승인 범위를 적용하며 회사 기준 충족으로 표시하지 않는다. 실제 도입 전 재검토 |
| secure-api-review 3 및 data-compliance C3 감사 요구와 D1 이력 제외 | 운영 접근/변경 로그와 행위자 식별 저장을 추가하지 않는다. D1의 시제품 범위 판단을 적용한다. 실제 도입 시 해당 회사 기준·책임자를 확인 |
| secure-api-review 2 입력 검증 | OpenAPI 스키마와 추가 엄격 파싱 계약에 따라 알려진 필드만 받는다. Python 표준 라이브러리로 명시 검증하며 스키마 검증 외부 패키지는 넣지 않는다. 구현 시 스키마·검증기 일치를 시험 |
| secure-api-review 4, data-compliance C1/C2 | 회사 PII 분류는 미제공. 합성 데이터만 사용하며 오류는 고정 문구, DTO는 명시 5필드. 본문/헤더/쿼리/원본 예외를 로그로 출력하지 않는다. 회사 분류를 발명하지 않음 |

위 차이는 이미 수락된 범위의 적용이며 추가 허가 요청이 아니다. PO가 이번 문서 집합의 구체적 제안을
수락하기 전에는 plan 인계 완료로 표시하지 않는다.

### Skills applied 근거

namespace는 로컬 프로젝트 `.agents/skills`다. 아래 각 파일을 실제 읽었고 경로별 최근 변경 SHA는 모두
`dcc6663a266cda8c342d609a5f715bda84507c5a`다. 제출 준비 시 해당 파일에 로컬 변경은 없었다.
정책 본문으로 실제 확인한 출처는 아래 파일과 D1의 PROJECT-POLICY.md다. 스킬 주석의 별도
policies/brand.md·policies/compliance.md는 이 저장소에서 제공 여부를 별도로 확인하지 않았으므로 읽었다고 주장하지 않는다.

| 스킬·출처(저장소 루트 기준) | 적용 |
|---|---|
| spec-policy-pass — .agents/skills/spec-policy-pass/SKILL.md | 정책 적용·차이·전체 문서 집합 검토 |
| brand — .agents/skills/brand/SKILL.md | B1–B3, 한국어 고정 오류·일관 용어, P1과 새 제안 구분 |
| data-compliance — .agents/skills/data-compliance/SKILL.md | C1–C3, 명시 DTO·오류 비노출·감사 제외 판단 |
| secure-api-review — .agents/skills/secure-api-review/SKILL.md | 위 4항목별 확인 |
| ux-copy — .agents/skills/ux-copy/SKILL.md | 호출자가 대응할 수 있는 오류 문구 |
| stop-slop-ko — .agents/skills/stop-slop-ko/SKILL.md | 한국어 명세 문장 |
| sdlc-feedback — .agents/skills/sdlc-feedback/SKILL.md | D1 수락 기록·상위 참조·요구와 설계 일치 |

웹 화면이 없으므로 accessibility는 적용하지 않는다. 자격증명 구현/diff 검사 단계가 아니므로
secrets-scan은 이번 문서 작성에서 실행하지 않는다. TDD 선택은 plan에서 판단하며 지금 선택하지 않는다.
