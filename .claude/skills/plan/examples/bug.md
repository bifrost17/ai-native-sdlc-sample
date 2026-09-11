# Plan: 복사한 요청 ID 양끝의 네 ASCII 공백 허용
Upstream: spec.md@efc65d9. Status: draft.
합성 예시: [입력 경계](context.md), [계약과 AC](../../design-spec/examples/bug/spec.md)를 읽는다.

## Files that change
- tests/test_id_whitespace.py (new): show/complete 재현과 과잉 정규화·데이터 회귀.
- tracker.py: 공유 조회에서 비교 입력만 보정하고 원본 오류 입력은 유지.
- README.md: 허용하는 양끝 문자와 내부/대소문자 미보정 설명.

## Order of work
재현 커밋과 수정 커밋을 하나의 결함 PR에 담는다. 최신 제품 main에서 진행한다.
1. 기존 세 시험을 확인한 뒤 아래 재현·회귀 시험을 추가한다. 실제 ASCII 제어 문자를 전달해
   기대한 이유(존재하는 ID를 못 찾음)로 실패하는지 확인하고 시험을 먼저 커밋한다.
2. 시험을 고치지 않고 공유 조회의 입력 사본만 spec R1대로 보정한다. 저장 ID·원본 오류 입력은
   보존한다. 설명을 추가하고 같은 시험과 인접 흐름을 모두 확인한다.
3. 최신 main과 통합한 결과로 Proof를 확인한다. 머지 후 두 명령의 보정과 기존 동작이 함께 사용 가능하다.

## Risks
인자 없는 strip은 NBSP까지 허용한다. show만 수정하면 complete가 달라진다. 같은 입력 집합을
두 명령에 적용하는 아래 회귀로 확인한다. 저장 파일 전체 보정은 spec의 보존 계약과 충돌한다.

## Proof
`python3 -m unittest discover -s tests -v`에서 기존 세 시험과 다음 추가 시험을 실행한다.
test_allowed_ascii_both_commands: show의 ` \tR-202\r\n`은 조회·바이트 보존, complete의
` R-202\n`은 대상 status만 변경, 재실행은 바이트 보존(AC1/3). escape는 실제 문자를 전달한다.
test_rejected_inputs_preserve_data: 내부 공백, 소문자, 공백뿐, NBSP, 빈 ID, 없는 ID 모두 두 명령에서
rc=1·파일 동일·원본 입력을 포함한 기존 오류를 확인한다(AC2). 각 사례는 새 복사본에서 시작한다.
test_exact_id_and_io_errors와 기존 세 시험으로 정확 ID·목록·기존 I/O 오류를 확인한다(AC4).
실패/수정 후 성공 출력은 실제 실행 때 보존한다. 테스트가 있다는 사실만으로 재현 성공이라 쓰지 않는다.
