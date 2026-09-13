# 실험 0033 — 수락 spec의 독립 설계 충분성 평가

판정: **충분**. 수락한 spec 네 파일은 이번 **동일 기기·합성 데이터·로컬 시제품**을 구현할 때 필요한 중요한 제품·기술 결정을 담고 있다. 핵심 API, 입력 타입, 데이터 수명, 원자성, 동시 변경, 오류, 공개 경계를 구현자가 새로 정해야 하는 중요한 빈칸은 발견하지 못했다. 모든 잘못된 프로토콜 조합까지 해석의 여지가 전혀 없다는 뜻은 아니며, 아래에 작은 문구 보완을 별도로 남긴다.

## 판정 대상과 읽기 순서

- 제품 저장소: `/Users/jake/Projects/ai-native-sdlc-codex-astra-20260913/f05-r01`.
- 먼저 `git show`로 **spec 수락 원본 `e9d52f8ad20fb09c912df2138ca4d939d621fad7`**의 `intent/0001-shared-requests/spec.md`, `design/contracts.md`, `design/storage.md`, `design/openapi.json`을 전부 읽었다. 아래 제품 파일 행 번호는 현재 작업 트리가 아니라 이 원본 기준이다.
- 이 네 파일만 읽은 시점에 **“충분; 중요한 설계를 구현자에게 넘긴 흔적 없음”**으로 blind 1차 판단을 고정해 부모 검토자에게 전달했다. 그때 plan·제품 구현·실행결과는 읽지 않았다.
- 이후 intent 수락 원본 `e1e06501e3bc13bfb09d7d6feb4da3fb12b8b953`의 `intent.md`, `PROJECT-POLICY.md`, 기존 `tracker.py`, `requests.json`을 읽어 보존 범위와 상위 의도를 대조했다. 이어 **plan 수락 원본 `e797fdcf31e7b5788d30f71dfe8318ae06381334`**의 `plan.md` 전체를 읽어 중요한 설계가 뒤늦게 생겼는지 확인했다.
- 새 제품 구현 코드·제품 시험·실행 기록은 이 평가에 사용하지 않았다. 제품이나 실험을 실행하지 않았다. OpenAPI 문서의 JSON 파싱과 내부 참조 해석만 읽기 전용으로 확인했다.
- 기준은 현재 템플릿의 `tdd-optional/project/examples/skills/design-spec/references/design-depth.md` 전체와 `docs/verification/north-star-playbook.html:452–570`의 요구사항·설계 대목이다. 전자는 선택할 설계 표현과 중요한 결정의 완결성을 요구하며 모든 메서드나 UML을 강제하지 않는다. 후자는 intent 문제 해결, 미결 질문 처리, 정책 우려 표시, 엔지니어링 인계를 기준으로 삼는다.

## spec 집합만으로 결정되는 사항

아래 제품 문서 경로는 모두 `intent/0001-shared-requests/` 아래다.

| 검토 축 | 문서 근거 | 독자가 추가 업무 질문 없이 구현할 수 있는 이유 |
|---|---|---|
| 문제와 설계 이유 | `spec.md:14–21,57–64` | JSON CLI 보존과 SQLite 독립, JSON 전체 쓰기를 배제한 이유, 공통 조회를 쓰는 이유, 표준 라이브러리와 짧은 직렬 쓰기라는 선택·비용을 설명한다. |
| 정확한 CLI/HTTP/CSV 계약 | `design/contracts.md:7–38,42–57,125–136` | 명령·인자 위치·기본 포트·종료 코드·스트림, 네 API 동작, 응답 envelope, 부분 PATCH, CSV 열·인코딩·행 끝·null 표현이 정해져 있다. |
| 데이터·공유 타입 | `design/storage.md:5–27,45–55` | JSON 최상위와 행 키 집합, 엄격 문자열/타입, 원문 보존, 중복 기준, 정수 상한, null과 누락, 서비스 입력·출력·오류를 구분한다. |
| 구조와 책임 | `design/storage.md:29–55` | transport/config/model/service/storage/serializer의 책임과 파일, 서비스 guard, 공개 네 메서드, 저장소와 출력의 분리를 제시한다. repository의 모든 보조 메서드까지 정할 필요는 없다. |
| 저장 수명·스키마 | `design/storage.md:59–89` | DDL, 스키마 판정, 허용되는 빈 DB, 기존 요청 거부, 생성 가능한 진입점, read-only/read-write 모드, URI 경로, 연결 수명, 저널·대기 한도가 정해져 있다. |
| 원자성과 동시성 | `design/storage.md:93–126` | 전체 검증 후 DB 접근, BEGIN IMMEDIATE 안의 적합성·빈 상태 재확인, 전체 삽입·rollback, 버전/전이/no-op 순서, 한 UPDATE, 커밋한 DTO 반환, 읽기 snapshot, 자동 재시도 없음까지 정해져 있다. |
| 오류와 부작용 | `design/contracts.md:72–123`; `design/storage.md:98–100,124–126` | framing/MIME/JSON/저장소 오류의 순서·코드·고정 문구, 실패 시 요청 불변, 실패한 새 빈 파일의 잔류 가능성, 커밋 뒤 응답·출력 실패의 한계를 구별한다. |
| 배포·공개 경계 | `spec.md:79–95,99–104`; `design/contracts.md:16–25` | loopback·프로세스 환경·명시 DB 위치, 기본 OFF, 시작 때 flag 고정, 업무 guard, health 예외, 동일 코드 ON, 사람의 공개·중단 책임을 기술한다. OFF가 데이터 복구는 아니라는 점도 정했다. |
| 독립 수용 기대 | `spec.md:25–50` | 고정 ID·버전·충돌·CSV 기대와 AC→R 대응이 있고, 실제 겹치는 두 작업·전후 전체 업무 행·원본 바이트 비교를 요구한다. 구현 출력의 사후 복사를 금지한다. |

예를 들어 `PATCH /requests/R-201`에 현재 v1과 `{"version":1,"owner":null,"status":"done"}`을 보내면 담당자 해제와 완료를 한 번 반영해 v2를 반환한다. 같은 v1을 다시 보내면 현재 값과 같더라도 `409 version_conflict`다. 현재 v2의 같은 값을 보내면 v2 그대로 성공한다. 이 판단을 위해 plan이나 구현을 읽을 필요가 없다(`contracts.md:52–57,89–92`; `storage.md:108–117`).

가져오기도 “SQLite를 쓴다”는 수준에 머물지 않는다. 첫 입력부터 끝까지 검증하고, 쓰기 잠금 안에서 스키마·빈 상태를 다시 확인하며, 두 실행이 겹치면 하나의 전체 집합만 남게 하는 순서와 실패 결과를 정했다(`storage.md:93–104`). 이 부분은 구현자가 원자성 전략을 추측하게 하는 명세와 구별된다.

## 중요한 findings

**없음.** 문서만으로 확인되는 중요한 결정 누락 또는 중요한 계약 모순(P0–P2)을 발견하지 못했다. 실제 구현이 이 계약을 지켰는지, AC가 실행됐는지에 대한 통과 판정은 아니다.

다음 한 건은 중요한 설계 미정으로 올리지 않는 **경미한 계약 문구 명료화**다.

| 위치·입력 예 | 관찰과 영향 | 작은 보완 |
|---|---|---|
| `design/contracts.md:64`, ON에서 `GET /requests/` | 같은 줄에 “빈 ID는 invalid_input”과 “끝 slash는 route_not_found”가 있다. `/requests/`는 두 표현에 걸려 독자가 400과 404 중 무엇을 기대할지 잠깐 해석해야 한다. 끝 slash라는 구체 규칙을 적용해 404로 구현할 수 있고, 어느 쪽도 저장소 변경이나 유효 요청의 의미를 바꾸지 않는다. | “`/requests/`는 404 route_not_found, `/requests/%20`는 400 invalid_input”이라는 예시 한 줄로 겹침을 없앤다. 새 업무 결정을 요구할 사안은 아니다. |

`/health`의 미지원 메서드와 Origin이 동시에 존재하는 경우도 검토했다(`contracts.md:74–80`). 첫 단계의 health 메서드 규칙과 뒤의 Origin/일반 메서드 규칙이 떨어져 있어 읽기가 매끄럽지는 않지만, 문서가 번호로 우선순위를 명시하므로 독립적인 확정 모순으로 세지 않았다.

## OpenAPI와 JSON Schema 정합성

읽기 전용 문서 검사에서 JSON 파싱이 성공했고 `$ref` **45개, 고유 10개**가 모두 같은 문서의 대상에 도달했다. 환경에 `jsonschema`가 없어 전용 JSON Schema/OpenAPI validator 통과를 주장하지 않는다. 아래는 스키마 본문과 부가 계약을 대조한 결과다.

| 확인 항목 | 정합성 판단 |
|---|---|
| Request의 다섯 필드 | `openapi.json:457–484`는 전부 required이며 additionalProperties=false다. storage의 DTO 계약과 맞는다. title의 RequestId 재사용은 명칭이 다소 범용적이지 않을 뿐 문자열 제약은 같으므로 모순이 아니다. |
| owner null·status null | `openapi.json:436–450`에서 Owner는 string/null, Status는 string enum이다. minLength는 문자열에 적용되므로 owner=null 허용과 충돌하지 않는다. |
| 부분 변경·빈 변경 | `openapi.json:485–515`의 version required와 owner/status anyOf는 한 필드 또는 두 필드를 허용하고 version만 있는 변경은 거부한다. `{"version":1,"owner":null}`은 유효하고 `{"version":1,"status":null}`은 무효다. |
| 정수 표현 | `openapi.json:451–455`는 1~2^63−1이며 1.0 같은 wire 표현의 추가 거부를 description에 쓴다. JSON Schema의 integer만으로 lexical 정수 표현까지 보장하지 않는 한계를 `openapi.json:6`, `contracts.md:89–90`이 명시했다. 따라서 `{"version":1.0,"owner":"x"}`의 schema 수준 통과 가능성을 실제 API 허용 약속으로 해석하면 안 된다. |
| 공백 문자열·중복 키·Unicode | `openapi.json:431–442`의 minLength만으로 공백만인 문자열이나 고립 surrogate·중복 JSON 키를 모두 거르지는 못한다. 그러나 추가 엄격 파싱을 `contracts.md:89–90`, `storage.md:5–14`에 배정했으므로 누락된 제품 규칙이 아니다. |
| 오류 | `openapi.json:556–599`의 envelope·code enum은 `contracts.md:99–123`의 HTTP 오류와 맞는다. 고정 문구와 상태별 허용 code 조합은 prose 정본을 함께 읽어야 한다. 스키마 단독으로 모든 오류 계약을 완전히 검증하는 형태는 아니다. |

따라서 **OpenAPI 하나만 개발의 전체 정본으로 사용하면 부족하지만, spec이 선언한 네 파일 집합은 이 차이를 알고 명시한 설계**다(`spec.md:66–75`). 기계 검증 가능한 범위를 넓히는 개선과 중요한 업무 결정 누락을 혼동해서는 안 된다.

## intent 충실성과 plan으로 넘긴 내용

intent의 초기 가져오기, 필드·상태, 낡은 버전 거부, 실제 경합, 정확 필터, CSV, 무쓰기 조건(`intent.md:21–38`)은 각각 spec의 R2–R7 및 AC2–14로 구체화됐다. 로그인·감사·실데이터·사내망을 제외한 범위(`intent.md:51–59`, `PROJECT-POLICY.md:35–50`)도 유지한다. 스키마/flag/API를 설계에서 제안하라는 intent의 질문(`intent.md:74–75`)에는 네 파일이 실제 답을 제공한다.

spec의 Q2/Q3에 carried forward가 남아 있는 것은 **설계내용을 비워 둔 것**이 아니라 작성 당시 PO의 이 제안 수락을 남긴 것이다(`spec.md:111–112`). 대상 SHA가 수락됐다는 이번 평가 전제에서 미해결 기술 질문으로 다시 세지 않는다. draft 표기 역시 수락 실패의 증거로 쓰지 않는다. 실제 수락 절차의 이행 여부는 이 문서 충분성 평가와 별개다.

plan에서 뒤늦게 확인한 내용은 다음과 같이 **실행·검증의 구체화**에 해당한다.

- `plan.md:74–88`: 가져오기→조회/CSV→변경의 세 PR과 부분 ON 공개 상태, 공통 파일 때문에 순차 진행한다는 이유. spec이 PR 순서·검증 방식의 소유권을 plan에 준 범위다(`spec.md:88–91,113`).
- `plan.md:98–116,125–138,147–166`: 시험 파일, fixture, 실제 프로세스/HTTP barrier, 실패 주입, 원본·업무행 비교. 원자성 전략·오류 기대 자체는 이미 spec에 있다.
- `plan.md:31–34`: 관측한 Python/SQLite 환경과 그 환경을 지원하는 구현상의 제약. 새 외부 의존·제품 지원 약속을 뒤늦게 도입하지 않는다.
- `plan.md:202–282`: 명령과 사람 실행 대행·기록·최종 공개의 절차. 기존 spec의 ON/OFF·커밋 보존·사람 결정 계약을 실행 가능한 순서로 만든다.

plan을 읽은 뒤 blind 판단을 바꿔야 할 중요한 설계 이월은 발견하지 못했다. plan은 상당히 상세하지만 그 길이가 spec의 설계 부재를 대신한 사례는 아니다.

## 도식·내부 설계와 판단 한계

설계 집합에 다이어그램은 없다. 그러나 모듈 책임 표(`storage.md:31–50`), 트랜잭션의 번호 순서(`storage.md:93–104`), 상태·버전 분기(`storage.md:108–117`), 프로세스/설정/데이터 경계(`spec.md:79–95`)가 도식이 답해야 할 핵심 질문을 이미 답한다. 따라서 UML·클래스 그림 부재를 결함으로 세지 않는다. HTTP/CLI→RequestService→SQLite 및 CSV 분기 그림 하나를 더하면 첫 독자의 탐색은 쉬워질 수 있지만, 새로운 결정을 대신할 필수 산출물은 아니다.

F05 예시를 더 읽기 쉽게 강화한다면 **컴포넌트 그림 한 장과 변경 시퀀스 한 장**이 적당하다. 전자는 두 진입점의 공통 guard/조회 경계와 독립 JSON CLI를, 후자는 잠금 획득→버전 확인→상태 전이→no-op/UPDATE→COMMIT→응답 및 충돌 분기를 기존 문장과 같은 이름으로 보여주면 된다. 이는 사람의 문서 탐색 효율을 높이는 **예시·템플릿 개선 후보**다. 이 실험에서 미작성된 중요한 설계의 증거도, 모든 변경에 두 그림/UML을 의무화할 근거도 아니다.

남아 있는 repository 보조 메서드, DTO의 구체적 Python 표현, 함수 내부 분할, 시험 지원 코드 구성은 합리적인 구현 재량이다. 인증·감사·TLS·다중 호스트 배포·성능 SLA를 덧붙이지 않았다는 이유로 부족 판정을 내리는 것도 수락한 시제품 범위를 벗어난다.

이 평가는 실제 SHA의 문서와 기존 baseline을 읽은 독립 정적 판단이다. 스킬 사용 자기기록을 실행 증거로 확정하지 않았고, 실제 동시성·원자성·HTTP 호환성의 구현 성공을 검증하지 않았다. 질문에 대한 답은 **“이번 범위에서는 spec와 선언된 하위 설계를 함께 읽으면 중요한 설계를 새로 묻지 않고 개발할 수 있을 만큼 충분히 작성됐다”**이다.
