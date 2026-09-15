# Plan: 담당자 필터를 한 PR로 제공
Upstream: spec.md@23845b5. Status: draft.
합성 작성 예시. 사용자 허가 범위는 설계 패키지이며 제품 계획 승인/구현 성공이 아니다.
[spec](spec.md)와 [입력](context.md)을 함께 읽는다. 현재 참조는 같은 변경에서 SP01을 추가한 spec 본문이며, Upstream은 기존 입력 판이다. 모든 시험은 예정이며 이름은 추가 계획이다.

## Files that change
| 경로 | 변경 | 연결 |
|---|---|---|
| tracker.py | list 옵션·필터 | SP01 / R1 |
| tests/test_owner.py (new) | 정확 비교·순서·미배정·기존/I/O 회귀 시험 | AC1–4 |
| README.md | 옵션 사용법·완료 포함·빈 결과 | R1/R3 |
기존 tests/test_tracker.py는 수정 없이 기준/회귀로 사용한다.

## Order of work
<a id="t01"></a>
### T01 — 담당자 필터의 구현·검증·인도
설계 근거는 [SP01](spec.md#sp01)이다. list의 옵션 파싱과 출력 전 배열 순회에 정확 비교를 연결해
기존 출력·다른 명령·파일 바이트를 보존한다. 소속은 아래 한 PR이며, Done은 P1–P3의 해당 관찰이다.
검증 방식: **동작별 구현 후 테스트**. 작은 list 옵션이며 독립 spec의 입력·출력 계약이 명확하고 기존 세 시험이
인접 명령을 보호한다. 새 옵션은 기존 시험에 없으므로 아래 AC 시험을 추가한다. 기대는 spec과 입력 사본에서 정한다.
한 PR: 기능·시험·설명을 묶는다. 최신 main에서 branch/worktree를 만들고 기존 세 시험으로 기준을 확인한다.
1. tracker.py의 list에 선택 인자와 정확 일치 필터를 연결한다. 곧바로 tests/test_owner.py에
   test_owner_exact_and_order를 추가·실행해 spec의 hana 두 행/기존 열·rc0·바이트 보존을 확인한다.
   `python3 -m unittest discover -s tests -p test_owner.py -v`가 이 동작을 검증한 뒤 다음 사례로 간다.
2. AC2의 no-match/null 구별을 확인할 test_owner_nonmatching을 추가한다. 필요한 구현을 작은 범위로
   조정하고 같은 명령으로 검증한다. 실제 출력에서 기대값을 복사하지 않고 독립 spec의 대소문자·null 경계를 대조한다.
3. AC3/4와 기존 시험을 확인하고 필요한 리팩터링 뒤 재실행, 사용 설명을 갱신한다.
4. 최신 main과 합친 판에서 Proof 전체를 실행하고 명령/판/출력·미확인 범위를 PR에 남긴다.
   검토 후 통합된 main에서도 같은 검증을 확인한다. 머지 뒤 이 기능은 바로 사용 가능, 남은 공개 범위 없음.

공통 절차는 프로젝트의 [선택형 정책](../../../../PROJECT-POLICY.md)과 적용한 관련 개발 스킬이다. 시험·구현을 별도 PR로 나누지 않는다.

## Risks
공유 검색/출력 수정이 show/complete를 깨뜨릴 수 있다. 변경을 list에 한정하고 P2로 발견한다.
fixture를 다른 시험이 수정하면 읽기 전용 판정이 흐려지므로 각 실행에 새 임시 사본을 쓴다.

## Proof
| ID·연결 | 기존/추가·실행 위치 | 명령·기대 |
|---|---|---|
| P1 T01 · AC1/2 | 추가 tests/test_owner.py: test_owner_exact_and_order, test_owner_nonmatching | python3 -m unittest discover -s tests -p test_owner.py -v; 전체 stdout/rc/바이트 비교 |
| P2 T01 · AC3/4 | 기존 tests/test_tracker.py의 세 시험 + 추가 test_owner_no_option_and_io_error | python3 -m unittest discover -s tests -v; 기존 정상/없는 ID/완료·반복, 무옵션·없는 파일의 rc2·접두사·파일 비생성 |
| P3 T01 · 통합 | P1/P2와 README 예시 | 최신 main과 합친 결과 및 통합 main에서 전체 GREEN·문서 계약 일치 |

실제 작성 순서·명령·판·검증 결과는 실행/PR에 남긴다. 사후 시험을 TDD 이력으로 소급하지 않는다.
경로·순서·검증 변경은 관련 구현 커밋에서 plan을 갱신한다.
정확 일치 등 계약이 바뀌면 spec/AC도 함께 고친다. 순수 회귀 추가가 계약/계획을 바꾸지 않으면 문서를 억지로 수정하지 않는다.
