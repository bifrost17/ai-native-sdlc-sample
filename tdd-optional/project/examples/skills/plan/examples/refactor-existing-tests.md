# Plan: ID 조회를 작은 함수로 분리하고 동작 보존

가상 plan-only 예시다. 교육 입력의 [tracker.py](../../../../docs/sdlc-authoring/inputs/baseline/tracker.py)와
[기존 시험](../../../../docs/sdlc-authoring/inputs/baseline/test_tracker.py)을 실제로 읽어 경로와 현재 검증 범위를 맞췄다.
채택 제품에서는 `tracker.py`, `tests/test_tracker.py` 배치를 가정한다. 명령을 실행하거나 제품의 spec·수락 SHA를
확인한 기록은 아니다. 상류 결정은 “list/show/complete의 현재 외부 동작을 바꾸지 않는다”는 가상 입력이며,
실제 계획은 그 제품의 수락된 spec 판과 현재 명령을 기록해야 한다.

## Files that change

- `tracker.py`: `main()` 안의 정확 ID 조회를 작은 내부 함수로 분리한다. 비교 규칙·첫 일치 행·오류·쓰기 경로는 바꾸지 않는다.

`tests/test_tracker.py`는 변경하지 않고 읽어 사용하는 기존 Proof다. 실제 diff가 새로운 동작이나 검증 공백을 만들면
그 판단을 갱신하며, “기존 시험 활용”이라는 선택 때문에 필요한 검사를 금지하지 않는다.

## Order of work

검증 방식: **기존 시험 활용**. 외부 계약을 바꾸지 않는 좁은 리팩터링이고, 기존 세 시험이 변경 지점을 통과해
목록 순서·조회 성공/실패·완료 쓰기와 반복 무쓰기를 관찰한다. 기대는 가상 보존 결정과 기존 시험의 독립 fixture에서
가져오며 리팩터링 뒤 출력에 맞춰 바꾸지 않는다. 인위적인 RED나 새 테스트 파일은 계획하지 않는다.

1. 제품의 실제 수락된 보존 계약과 diff base를 확인한다. 변경 전
   `python3 -m unittest discover -s tests -v`를 실행해 기존 결과와 대상 판을 기록한다.
2. 행 순서를 그대로 순회해 첫 exact-ID 일치를 반환하는 내부 함수로 조회 코드만 옮긴다. `list`, `display`,
   오류 문자열과 `complete`의 쓰기 조건은 손대지 않는다.
3. 같은 명령을 다시 실행하고 실제 diff가 조회 분리로 한정됐는지 읽는다. 기존 검사가 기준판에서 실패하거나
   변경한 분기를 판별하지 못한다는 근거가 생기면 완료로 밀어붙이지 않고 원인을 확인해 plan과 필요한 검증을 보강한다.
4. 최신 main과 합친 결과에서 같은 Proof를 확인한다. 이 작은 변경은 다른 작업과 묶을 수 있으며 별도 PR이나 승인 단계를 요구하지 않는다.

## Risks

조회 함수를 옮기며 첫 일치 순서를 바꾸거나 `show`와 `complete`가 다른 경로를 쓰게 만들 수 있다. 기존 조회·완료
시험과 diff 대조로 발견한다. 기존 세 시험은 중복 ID, 손상 JSON, 모든 오류 본문을 포괄하지 않는다. 이번 변경이
그 경계까지 건드리면 현재 Proof만으로 충분하지 않으므로 특성화 또는 회귀 검증을 추가한다.

## Proof

예정 증명은 `python3 -m unittest discover -s tests -v`의 변경 전·후 및 최신 main 결합 결과다.

- `test_list_preserves_order_and_does_not_write`: 목록 순서와 읽기 전용 동작.
- `test_show_existing_and_missing_id`: 정확 ID 조회 성공과 없는 ID 실패.
- `test_complete_changes_only_target_status_and_is_repeatable`: 대상 상태만 변경하고 반복 완료는 파일을 다시 쓰지 않음.

실제 명령·코드판·출력은 채택 제품의 실행/PR 기록에 남긴다. 기존 시험과 diff가 보존 계약을 판별한 경우에만
제품 리팩터링 완료 근거가 되며, 새 테스트가 없다는 사실이나 이 합성 문서 자체는 완료 증거가 아니다.
