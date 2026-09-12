# Plan: 재현을 먼저 고정한 ID 비교 수정
Upstream: spec.md@23845b5. Status: draft.
합성 작성 예시. 사용자 허가 범위는 설계 패키지이며 제품 계획 승인/구현 성공이 아니다.
[spec](spec.md)와 [입력](context.md)을 함께 읽는다. 모든 시험은 예정이며 이름은 추가 계획이다.

## Files that change
| 경로 | 변경 |
|---|---|
| tests/test_id_whitespace.py (new) | AC1–4의 회귀와 결함 재현 |
| tracker.py | 비교 입력만 지정 ASCII strip, 오류에는 원본 보존 |
| README.md | 허용 문자/보존 경계 설명 |
tests/test_tracker.py는 기존 기준이다.

## Order of work
검증 방식: **TDD**. 실제 제어문자로 재현 가능한 ID 비교 결함이며 spec의 허용/거부 경계를
고정한 시험으로 수정 전후를 대조하기 적합하다. 이 사례의 재현 커밋은 선택한 작업 순서이며 모든 버그의 의무가 아니다.
한 PR 안의 재현 커밋과 수정 커밋이다. 최신 main에서 시작한다.
1. 기존 세 시험을 실행한다. test_id_whitespace.py에 실제 argv 제어문자와 show/complete 사례를
   추가하고 AC1이 현재 rc1로 실패하는지 확인한다. AC2–4는 이미 통과할 수 있으며 회귀로 남긴다.
   고정하기 전에 fixture/기대값/각 사례의 데이터 사본을 확인한다.
2. 재현 시험과 결과를 먼저 커밋한다. 그 뒤 같은 시험을 바꾸지 않고 tracker.py를 수정한다.
   프로젝트의 실제 테스트 보호 방법이 있으면 재현 생성·관측·커밋 뒤 엔지니어가 해당 단계에 진입한다.
   이 사용 템플릿이 보호 훅을 설치한 것으로 가정하지 않으며 일반 기능의 TDD와 결함 재현 보호를 구별한다.
3. AC1 GREEN, AC2–4와 기존 회귀를 확인한다. 필요한 리팩터링 뒤 같은 시험을 다시 돌리고 설명을 갱신한다.
4. 최신 main 결합/머지 후 Proof를 확인하고 시험 커밋·실패 이유·수정 판·출력을 PR에 연결한다.
   전체 수정이 한 공개 단위이며 feature flag와 후속 기능 PR 없음.

시험 자체가 잘못됐다는 근거가 생기면 실패를 덮어 GREEN으로 만들지 않는다. 수정 단계를 멈추고
엔지니어에게 근거를 전달해 재현을 정정/다시 고정한 뒤 수정한다. 실제 보호 단계가 적용된다면 우회 편집하지 않는다.

## Risks
기본 strip()은 NBSP까지 지워 다른 ID를 찾을 수 있다. 원본 argv를 덮으면 오류 계약도 달라진다.
P1의 거부 사례와 원본 stderr, 대상 외 행/조회 바이트를 비교한다. 일반 JSON 정규화로 범위를 확장하지 않는다.

## Proof
| 연결 | 기존/추가 시험 | 명령·기대 |
|---|---|---|
| P1 AC1 | 추가 test_show_surrounding_ascii, test_complete_surrounding_ascii_and_repeat | tests/test_id_whitespace.py, 실제 공백/tab/CR/LF; 수정 전 요청 미발견 RED → 고정 시험 그대로 GREEN |
| P2 AC2/3 | 추가 test_nonaccepted_ids_keep_original_error | 내부 공백·소문자·NBSP·빈값·공백뿐·없는 ID 모두 show/complete rc1 원본 입력·파일 불변 |
| P3 AC4 | 기존 세 시험 + 추가 test_io_error_and_stored_ids_unchanged | 원 ID/순서/기존 오류 유지, 없는 파일 생성 없음 |
| 통합 | P1–3 | python3 -m unittest discover -s tests -v; 최신 main 결합과 통합 main에서 모두 통과 |

예정 시험은 아직 실행하지 않았다. 관련 구현이 계약/계획을 바꾸면 영향 문서도 같은 커밋에 반영한다.
