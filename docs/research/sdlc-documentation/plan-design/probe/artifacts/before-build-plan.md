# Plan: 담당자 목록을 먼저 쓰고 상태 요약을 잇기
Upstream: spec.md@fa3d4ba6f1bb38a5c183a4e0eee6dfc0ab187a0f. Status: draft.
HUMAN root가 이 SHA를 계획 입력으로 확인했다. `git log --oneline -- intent/0001-owner-list-summary/spec.md`
기준 spec.md의 유일한 커밋이며 이후 변경이 없다. 목록을 먼저 인도하고 요약을 잇는 순서, 정확 일치·
보존 계약(R1–R3, AC1–AC3)이 이번 계획의 근거다.

`intent.md`/`spec.md`/`plan.md`는 아직 `main`(34f41ee)에 없고 브랜치 `plan/owner-list-summary`
(현재 HEAD `e14345b`, 이번 개정 포함 후 새 SHA)에만 있다. PR1 구현 브랜치는 `main`이 아니라
이 문서 브랜치의 최신 커밋에서 시작한다. 문서를 먼저 `main`에 통합하는 Draft PR을 선택해도 되며,
그 경우 병합 SHA로 이 문단을 갱신한다. 아래 "최신 `main`"은 이 문서가 `main`에 합류된 이후를
가리키며, 그 전까지는 이 브랜치의 최신 커밋을 기준판으로 쓴다.

## Files that change
- `tracker.py`: `list`에 `--owner ID` 옵션 추가(PR1), 선택 로직을 공유하는 `summary [--owner ID]`
  서브커맨드 추가(PR2). 두 커맨드가 쓰는 정확 일치 helper(`_owner_matches(request, owner)`)를
  PR2에서 도입해 `list`도 재사용하도록 최소 리팩터링한다. 기존 `display`, `show`, `complete`
  분기와 파일 쓰기 경로는 건드리지 않는다.
- `tests/test_owner_list.py` (new, PR1): `--owner` 정확 일치·원래 순서·done 포함·대소문자
  불일치/없는 담당자 빈 결과·무옵션 전체 4행·파일 바이트 보존(AC1).
- `tests/test_summary.py` (new, PR2): 전체/`--owner hana`/없는 담당자 집계, 탭·개행 형식,
  `complete` 후 재요약, 파일 바이트 보존(AC2, AC3). 같은 픽스처로 PR1 시험도 재확인한다.
- `tests/test_tracker.py`: 변경 없음. 기존 list/show/complete 회귀 기준으로 유지한다.
- `USAGE.md`: PR1에서 `list --owner ID` 사용법 한 줄 추가, PR2에서 `summary [--owner ID]`
  사용법과 출력 형식 한 줄 추가.
- `requests.json`: 변경 없음. 현재 픽스처(R-101/102/103/104)가 이미 AC1–AC3의 기대값과 일치한다.

## Order of work
1. **PR1 — 담당자 목록 인도.** 최신 `main`에서 브랜치를 만들어 `python3 -m unittest discover -s tests -v`로
   기존 3개 시험이 통과함을 먼저 확인한다(기준선). `tracker.py`의 `list`에 `--owner ID`를 추가해 owner
   문자열 정확 일치·원래 순서·`done` 포함으로 선택하고, 옵션이 없으면 전체를 출력한다. null owner는
   어떤 문자열과도 일치시키지 않는다. `tests/test_owner_list.py`와 `USAGE.md` 한 줄을 함께 커밋한다.
   이 PR만 `main`에 머지해도 동료는 목록을 바로 쓸 수 있다. 요약은 아직 없고 F02 전체 목표는
   완료가 아니다.
2. **PR2 — 상태 요약.** PR1이 사람 검토를 거쳐 `main`에 머지된 뒤 그 최신 판에서 새 브랜치를 만든다.
   `_owner_matches` helper로 선택 로직을 `list`와 공유하도록 옮기고, `summary [--owner ID]`를
   추가해 같은 선택 규칙으로 open/done 건수를 `open\t{n}\ndone\t{n}\n` 형식으로 출력한다(쓰기 없음).
   `tests/test_summary.py`와 `USAGE.md` 한 줄을 함께 커밋하고, `tests/test_owner_list.py`를 다시
   실행해 리팩터링이 PR1의 정확 일치·순서·null 처리를 바꾸지 않았는지 확인한다.
   `main`에서 목록·요약·기존 show/complete가 모두 동작하면 이번 F02 범위가 끝난다.

두 PR은 `tracker.py`·`USAGE.md`와 선택 의미를 공유하므로 순차 실행하며 병렬 세션을 쓰지 않는다.
코드량이 작다는 이유로 하나의 PR에 모아 목록 인도를 미루거나, 시험·문서만 별도 PR로 떼지 않는다.
PR2는 PR1의 파일을 다시 포함한 diff가 아니라 PR1 머지 후 최신 `main` 대비 남은 변경으로 검토한다.
실제 브랜치 이름·PR·수락 SHA는 구현 시점의 실행 기록(Draft PR 또는 보존 대화)에 남긴다.

## Risks
가장 위험한 단계는 PR2에서 선택 로직을 `list`와 공유하도록 옮기는 리팩터링이다. 이 과정에서
PR1이 세운 정확 일치·원래 순서·null 비일치 계약이 깨질 수 있다. PR2에서 `tests/test_owner_list.py`를
반드시 재실행해 감지하고, 실패하면 `summary`가 아니라 공유 helper를 고쳐 재검증한다. 이미 동료가
쓰는 `list --owner`의 회귀를 "요약이 통과했다"는 이유로 넘기지 않는다.
두 번째 위험은 `complete`의 파일 쓰기 경로다. `summary`·`list --owner` 추가가 새 분기를 만들면서
`show`/`complete`의 오류 처리·반복 실행 바이트 보존에 영향을 주지 않는지 각 PR에서 기존
`tests/test_tracker.py` 세 시험으로 확인한다.

## Proof
각 PR은 `python3 -m unittest discover -s tests -v`로 그 시점의 모든 시험을 통과해야 한다(rc=0).
- PR1: 새 `tests/test_owner_list.py`로 `list --owner hana`가 R-101/R-103 순서(AC1),
  `HANA`/`nobody`/`-`가 빈 stdout·rc=0, 무옵션 `list`가 기존 네 행·열·순서를 유지, 각 호출 후
  `requests.json` 사본의 바이트가 변하지 않음을 확인한다. 기존 `tests/test_tracker.py` 세 시험은
  그대로 통과해야 한다.
- PR2: 새 `tests/test_summary.py`로 전체 `open\t3\ndone\t1\n`, `--owner hana`가
  `open\t1\ndone\t1\n`, 없는 담당자가 `open\t0\ndone\t0\n`(AC2), `complete R-101` 후 같은
  사본에서 `--owner hana`가 `open\t0\ndone\t2\n`이고 요약 자체는 파일을 바꾸지 않음(AC3)을
  확인한다. `tests/test_owner_list.py`와 기존 `tests/test_tracker.py` 세 시험도 함께 재실행한다.

두 PR 모두 위 시험 실행 결과(명령·rc·stdout 요약)를 구현 커밋 또는 Draft PR 기록에 남긴다.
로컬 merge만 수행했다면 hosted PR·CI·운영 인도 성공이라고 기록하지 않는다. 실행이 계획에서
벗어나면 이 `plan.md`와 이유를 해당 구현 커밋에 반영하고, 동작·범위가 바뀌면 `spec.md`를 먼저
갱신한다.
