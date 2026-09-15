# Spec: 담당자 문자열로 요청 목록 필터
Upstream: intent.md@4a74823. Status: draft.
Skills applied: none（root가 고정 연구자료를 바탕으로 작성한 합성 예시）.
작성 권한: 사용자가 설계 패키지 작성을 허가했다. Upstream은 제작 입력이며 제품 수락을 뜻하지 않는다.

[입력](context.md). 새 옵션을 기존 list 흐름에 추가한다. 이 파일 하나가 이 변경의 spec 정본이다.

## Requirements
| ID | 바꿀 동작·유지할 계약 | 근거 |
|---|---|---|
| R1 | list --owner ID는 담당자 대소문자 구별 정확 일치, 완료 포함, 원래 순서로 출력. null은 어느 문자열과도 일치하지 않음 | Q1,Q2 답 |
| R2 | 옵션 없는 list와 show/complete, 탭 출력 열·데이터 형식 유지 | intent 제약 |
| R3 | 조회는 파일 바이트 불변. 일치 없음은 빈 stdout·rc0 | Q3, intent |

## Acceptance criteria
모두 격리된 원 데이터 사본. 열은 id/status/owner-or-'-'/title, 각 행 개행.
| ID → 요구 | 조건·행동 | 관찰할 결과 |
|---|---|---|
| AC1 → R1,R3 | list --owner hana | R-101, R-103 순서·기존 열/값, rc0, 바이트 불변 |
| AC2 → R1,R3 | nobody, HANA, - 각각 지정 | 빈 stdout, rc0, 바이트 불변 |
| AC3 → R2,R3 | 옵션 없는 list, show R-101, 없는 ID, complete R-101과 반복 | list 네 행 원순서, show 기존 결과/오류. complete는 대상 status만 done, 반복은 파일 무변경 |
| AC4 → R2 | 없는 데이터 파일로 list --owner hana | rc2, stderr는 기존 Cannot read or update requests: 접두사, 파일 생성 없음 |

## Design
<a id="sp01"></a>
### SP01 — list 담당자 필터 계약
관련 요구: R1, R2, R3. 기존 R/AC는 보존한다. 아래 경계와 선택이 SP01의 정본이다.
| 경계 | 정한 계약·선택 |
|---|---|
| CLI | list에만 선택 인자 --owner ID. 생략과 문자열 입력을 구별. show/complete 옵션은 불변 |
| 데이터→출력 | JSON 읽기 → list에서 owner 정확 비교 → 기존 display. 재정렬·대소문자 변환·부분 일치 없음 |
| 미배정 | 실제 null과 출력용 '-'를 구별. 이번 fixture에는 문자열 '-' 담당자가 없음. 실제 '-' 문자열이 저장돼 있다면 그 문자열과는 일치 |
| 구조 | 기존 배열 순회로 충분. 새 클래스·인덱스 없이 좁은 경로 변경. 내부 보조 함수 분리는 구현 중 결정 |

입출력 계약은 고정이고 보조 함수 이름은 고정하지 않는다. 새 옵션 전체가 한 PR에서 사용 가능하므로
별도 공개 제어는 필요 없다. 구현 방향의 중요한 미정이 없고 도식보다 위 흐름이 짧고 명확하다.

## Constraints and scope
R2/R3와 업무 코드 2~4파일 이내. 미배정 전용 옵션·다중 담당자·정렬·저장 형식 변경은 제외한다.

## Open questions
- Q1 answered: 완료 포함. 고정 입력의 오너 답변.
- Q2 answered: 정확 일치·null 비일치. 입력의 오너 답변을 R1/Design에 반영.
- Q3 answered: 빈 stdout·rc0. 입력의 오너 답변을 R3에 반영.

## Flagged concerns
제공된 CLI·파일 범위에서 정책 충돌/새 권한/외부 의존 변경 없음. 별도 사람 결정이 필요한 우려 없음.
