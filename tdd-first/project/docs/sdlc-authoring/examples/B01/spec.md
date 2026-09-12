# Spec: ID 비교 입력의 주변 ASCII 공백 허용
Upstream: intent.md@4a74823. Status: draft.
Skills applied: none（root가 고정 연구자료를 바탕으로 작성한 합성 예시）.
작성 권한: 사용자가 설계 패키지 작성을 허가했다. Upstream은 제작 입력이며 제품 수락을 뜻하지 않는다.

[입력](context.md). 조회·완료가 공유하는 ID 비교만 고친다. 이 파일이 spec 정본이다.

## Requirements
| ID | 바꿀 동작·유지할 계약 | 근거 |
|---|---|---|
| R1 | show/complete의 입력 ID 양 끝에서 ASCII space, tab, CR, LF만 제거해 비교 | Q1 |
| R2 | 내부 공백·대소문자·NBSP는 그대로 비교. 저장된 ID는 변경하지 않음 | intent/Q1 |
| R3 | 조회·오류 시 파일 불변. 정상 complete는 status만 변경, 이미 done이면 무쓰기 | 기존 계약 |
| R4 | 못 찾으면 rc1과 Request not found: 뒤에 원본 입력. 파일 오류는 기존 rc2·오류 접두사 | Q2/기존 계약 |

## Acceptance criteria
시험은 매번 새 데이터 사본을 사용한다. 아래 \t/\r/\n은 시험 argv의 실제 제어문자를 뜻한다.
| ID → 요구 | 입력·행동 | 기대 |
|---|---|---|
| AC1 → R1,R3 | show와 complete에 " \tR-201\r\n" | R-201 정상 결과. show 무쓰기, complete 대상만 done; 같은 완료 반복 무쓰기 |
| AC2 → R2,R3,R4 | R- 201, r-201, NBSP+R-201+NBSP 각각 show/complete | rc1·원본 입력 오류, 파일 불변 |
| AC3 → R4 | 빈 문자열, 허용 공백뿐, " R-999 " 각각 show/complete | rc1과 원본 입력(주변 공백 포함), 파일 불변 |
| AC4 → R2,R3,R4 | 기존 list/show/complete와 파일 I/O 실패 | 기존 동작·순서·원본 ID·오류 유지 |

## Design
비교용 값은 입력에 `strip(" \t\r\n")`와 동등한 변환을 적용한다. 인자 원본은 별도로 유지해
오류 출력에 쓴다. 기본 strip()의 전체 Unicode 공백 허용은 범위를 넘으므로 사용하지 않는다.
JSON을 읽은 뒤 show/complete가 공유하는 ID 검색에만 비교 값을 사용한다.
list, 출력과 저장 ID, 정상 완료의 쓰기 경로는 재사용한다. 새 클래스·정규식은 필요 없다.
그림 없이 이 흐름과 정확한 문자 집합으로 계약을 설명할 수 있다.

## Constraints and scope
R2의 구분을 보존한다. 입력 전체 치환·저장 데이터 청소·오류 형식 재설계는 제외한다.

## Open questions
- Q1 answered: 네 ASCII 문자만 주변에서 제거. 합성 오너 답을 R1/R2에 반영.
- Q2 answered: 오류는 원본 입력을 보존. 합성 오너 답을 R4에 반영.

## Flagged concerns
데이터 청소나 넓은 정규화로 범위를 확장하지 않는 한 별도 결정 우려 없음.
