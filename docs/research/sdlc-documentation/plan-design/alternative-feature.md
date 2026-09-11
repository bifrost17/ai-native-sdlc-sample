# Alternative B: 단계별 묶음으로 쓴 F01

비교용 작성본. [선택안 A](../../../../.claude/skills/plan/examples/feature.md)와 같은 입력이다.
실제 승인·구현 결과가 아니다.

## Context
계약은 design-spec/examples/feature/spec.md@efc65d9, 실행 맥락은 plan/examples/context.md다.
한 PR로 list --owner 기능·시험·설명을 제공한다. 최신 main에서 시작하고 통합 후 전체 기능을 인도한다.

## Work package 1: 기준 동작과 선택 입력
- Files: tracker.py, tests/test_owner.py(new).
- Action: 기존 세 시험 확인 후 list의 선택 인자를 연결하고 JSON 읽기 뒤 정확 일치 필터를 적용한다.
- Check: test_owner_exact_and_order(new)는 hana 두 행·HANA/nobody/- 빈 stdout·rc=0·바이트 보존.
- Risk: show/complete의 공용 조회에 필터를 끼워 넣지 않는다. 기존 세 시험으로 확인한다.

## Work package 2: 사용과 통합
- Files: README.md, tests/test_owner.py(new).
- Action: 무옵션·오류 보존 시험과 사용 설명을 추가하고 최신 main과 합친 결과를 확인한다.
- Check: test_owner_no_option_and_io_error(new)는 무옵션 네 행·없는 파일 rc=2·기존 오류 접두사.
  python3 -m unittest discover -s tests -v로 기존/새 시험 모두 통과해야 한다.
- Risk: show/complete의 정상 쓰기는 보존해야 한다. 별도 DB·캐시·UI는 필요 없다.

각 묶음의 시험/설명은 같은 PR에 포함한다. 실행 출력은 PR에 남기며 계획에서 통과를 주장하지 않는다.
