# Plan: 담당자별 요청 목록
Upstream: spec.md@efc65d9. Status: draft.
합성 예시: [입력 경계](context.md), [계약과 AC](../../design-spec/examples/feature/spec.md)를 읽는다.

## Files that change
- tracker.py: list 인자와 정확 일치 필터. 기존 display와 show/complete 경로 보존.
- tests/test_owner.py (new): 새 옵션과 읽기 전용·기존 동작 회귀 시험.
- README.md: list --owner 예시와 정확 일치·완료 포함 설명.

## Order of work
검증 방식: **동작별 구현 후 테스트**. 작은 list 옵션이며 spec의 정확한 출력과 기존 세 시험을 기준으로 검증할 수 있다.
기대는 spec/입력에서 정하고 각 동작을 구현한 직후 해당 시험을 추가·실행한다.
한 PR로 기능·시험·설명을 함께 검토한다. 최신 제품 main에서 시작한다.
1. 기존 세 시험으로 기준 동작을 확인한다. list 파서에 선택 인자를 연결하고 읽은 행에서 필터링한다.
   곧바로 tests/test_owner.py에 정확 일치·순서 시험을 추가하고 Proof의 명령으로 실행한다.
2. no-match와 무옵션/I/O 사례를 추가·실행하고 필요한 구현을 조정한다. 모든 AC1–3을 대조하고 사용 설명을 추가한다.
3. 최신 main과 합친 결과를 다시 확인하고 인도한다. 이 PR 뒤 목록 필터가 동작하며 후속 PR은 없다.

## Risks
공용 출력/조회 코드를 바꾸면 show/complete까지 영향받는다. 기존 경로를 재사용하되 필터는 list에만
적용하고 기존 세 시험으로 발견한다. UI·DB·캐시를 추가할 이유가 없는 변경이다.

## Proof
`python3 -m unittest discover -s tests -v`가 기존 세 시험과 새 시험을 모두 실행해 통과해야 한다.
추가할 test_owner_exact_and_order는 hana→R-101/R-103, nobody/HANA/-→빈 stdout·rc=0과
매번 파일 바이트 보존을 확인한다(AC1/2). test_owner_no_option_and_io_error는 무옵션 출력 보존과
없는 파일의 기존 rc=2·오류 접두사를 확인한다(AC3). 기존 complete 시험은 정상 쓰기까지 금지하지 않는다.
이는 예정 검사이며 실행 출력은 구현/PR에 남긴다.
