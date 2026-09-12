# Plan: 목록을 먼저 쓰고 상태 요약을 추가하기
Upstream: spec.md@2a3d1b0. Status: draft.
합성 예시: [spec 입력](two-pr-spec.md)과 [현재 코드·데이터](context.md)를 읽는다. 위 SHA는 제작 입력 판이다.

## Files that change
- tracker.py: PR1의 list 선택, PR2의 summary와 공통 선택 재사용.
- tests/test_owner.py (new): PR1 정확 일치·순서·읽기 전용 시험.
- tests/test_summary.py (new): PR2 집계·같은 선택 의미·완료 뒤 반영 시험.
- README.md: 각 PR에서 제공하는 명령의 사용 설명.

## Order of work
검증 방식: **동작별 구현 후 테스트**. 각 CLI 계약이 독립 입력에 고정되어 있고 두 PR을 순차 인도한다.
목록·집계 동작마다 구현 직후 아래 named 시험을 추가·실행한다. 기존 세 시험과 PR1 시험은 회귀로 활용한다.
1. **PR1 — 담당자 목록 인도.** 최신 제품 main의 작업 브랜치에서 기준 시험을 돌리고
   list --owner와 test_owner.py·사용 설명을 함께 구현한다. AC1과 기존 세 시험을 통과시킨다.
   이 PR만 main에 머지해도 동료가 목록을 사용한다. 요약은 아직 없으며 전체 목표 완료가 아니다.
2. **PR2 — 상태 요약.** PR1의 사람 검토·main 통합 뒤 그 최신 판에서 새 브랜치를 만든다.
   summary [--owner ID]를 연결하고 목록과 선택 의미를 공유한다. test_summary.py·설명을 함께
   제공한다. main에서 목록·요약·기존 show/complete가 모두 동작하면 이번 범위가 끝난다.

두 작업은 tracker.py·README.md와 선택 의미를 공유하므로 순차 실행한다. 작은 코드량을 이유로
PR 하나에 모아 목록 인도를 미루거나, 시험·문서만 별도 PR로 떼지 않는다. 별도 병렬 세션은 쓰지 않는다.
실제 브랜치 이름·PR 번호·수락 SHA는 실행 기록에 남긴다. 두 번째 PR은 첫 PR의 파일을 다시
포함한 diff가 아니라 최신 main 대비 남은 변경으로 검토한다.

## Risks
PR2의 선택 공통화가 PR1의 null·정확 일치·순서를 바꿀 수 있다. PR2에서도 test_owner.py를 다시
실행하고 complete 후 같은 데이터로 요약한다. 명령 추가 시 show/complete 분기 유입을 함께 확인한다.
실패하면 PR2를 고쳐 재검증하고 이미 사용 중인 목록까지 성공했다고 재판정하지 않는다.

## Proof
각 PR은 `python3 -m unittest discover -s tests -v`로 그 시점의 모든 시험을 통과한다.
- PR1: 새 test_owner_exact_and_order로 hana 두 행·HANA/nobody/- 빈 결과·무옵션 네 행,
  모든 조회의 바이트 보존(AC1). 기존 세 시험은 show와 정상·반복 complete를 확인한다.
- PR2: 새 test_summary_counts로 전체 open=3/done=1, hana=1/1, 없는 담당자=0/0의
  탭·개행·rc=0과 바이트 보존(AC2/3). test_complete_then_summary로 새 복사본의 R-101 완료 뒤
  hana=0/2와 요약의 읽기 전용을 확인한다. test_owner.py와 기존 세 시험도 유지한다.

통합 담당 엔지니어는 각 PR 머지 전 최신 main과 합친 결과에서 위 검사를 확인하고 실제 명령·출력을
그 PR에 남긴다. 로컬 merge만 실험했다면 hosted PR/CI·운영 인도 성공이라고 기록하지 않는다.
