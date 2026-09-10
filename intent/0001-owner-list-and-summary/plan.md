# Plan: 담당자별 조회(`list --owner`)와 상태 요약(`summary`) (from intent 0001-owner-list-and-summary)
Upstream: spec.md@892d6a501c2653a0a66e9cc2a7b4899b3e42462b (AC8 참조를 R7에서 Constraints로 정정한 것 외
기능 결정은 동일). Status: draft.

두 기능은 같은 파일(`tracker.py`)을 바꾸고 순서 우선순위(조회 먼저)가 정해져 있으므로 순차로
진행한다. 동시에 맡기면 같은 파일을 두 작업이 바꿔 병합 충돌과 교차 검증 비용이 생기고,
PR-SIZE 가이드도 같은 파일을 바꾸는 작업은 순차 진행을 권한다. `list --owner`를 먼저 검증·인도해
바로 쓰게 하고, `summary`는 그 위에서 이어간다.

## Files that change

- `tracker.py`
- `tests/test_tracker.py`

## Order of work

두 개의 PR로 나눈다. PR2는 PR1이 `main`에 머지된 뒤 그 판에서 시작한다.

**PR1 — `list --owner` (먼저 인도)**

1. 기존 기준 확인: `python3 -m unittest discover -s tests -v` 실행해 현재 3개 시험이 통과함을 확인한다.
2. `tracker.py`의 `list` 서브파서에 `--owner`(선택, 기본값 없음/None) 인자를 추가한다.
   `main()`의 `list` 분기에서 `args.owner`가 있으면 `requests`를 `row["owner"] == args.owner`로
   필터링해 원본 순서를 유지한 채 출력한다(spec R1–R3, R7).
3. `tests/test_tracker.py`에 다음을 추가한다.
   - `list --owner hana` → R-101, R-103을 이 순서로 반환하고 done 포함 (AC1).
   - `--owner` 없는 `list`가 기존과 동일 — 기존 `test_list_preserves_order_and_does_not_write`는
     그대로 유지해 회귀를 잡는다(AC2).
   - `list --owner HANA`, `list --owner nobody` → 빈 stdout, 종료코드 0 (AC3).
   - `list --owner hana` 실행 전후 데이터 파일 바이트 동일 (AC6의 list 부분).
4. 전체 시험 실행, `show`/`complete` 관련 기존 시험이 그대로 통과하는지 확인(AC8).
5. HUMAN이 diff와 동작을 검토하고 PR1을 `main`에 merge commit으로 통합한다. 통합 후 담당자들이
   `list --owner`를 바로 쓸 수 있다 — `summary` 완료를 기다리지 않는다.

**PR2 — `summary [--owner <ID>]` (PR1 머지 후 최신 `main`에서 시작)**

1. PR1이 머지된 `main`에서 새 브랜치를 만들고, `python3 -m unittest discover -s tests -v`로 PR1의
   기준이 그대로 통과하는지 먼저 확인한다.
2. `tracker.py`에 `summary` 서브파서(`--owner` 선택 인자, `--data`는 전역 옵션 공유)를 추가한다.
   `main()`에 `summary` 분기를 만들어 PR1의 필터 로직과 같은 방식으로 대상 집합을 고르고
   (`--owner` 없으면 전체, 있으면 `list --owner`와 동일한 선택), `status`별 개수를 세어
   `open\t<건수>`, `done\t<건수>` 순서로 출력한다(spec R4–R6).
3. `tests/test_tracker.py`에 다음을 추가한다.
   - `summary`(옵션 없음) → `requests.json` 기준 `open\t3`, `done\t1` (AC4).
   - `summary --owner hana` → `open\t1`, `done\t1` (AC4).
   - `summary --owner nobody` → `open\t0`, `done\t0`, 종료코드 0 (AC5).
   - `summary`/`summary --owner` 실행 전후 데이터 파일 바이트 동일 (AC6의 summary 부분).
   - 임시 복사본에서 `complete R-101` 실행 후 같은 복사본으로 `summary --owner hana` →
     `open\t0`, `done\t2` (AC7, 상태 변화 반영 확인).
4. 전체 시험 실행, PR1이 추가한 `list --owner` 시험과 기존 `show`/`complete` 시험이 함께 통과하는지
   확인한다(회귀 없음).
5. HUMAN이 diff와 동작을 검토하고 PR2를 `main`에 merge commit으로 통합한다.

## Risks

- 가장 위험한 지점은 필터 비교에서 `None`과 문자열 비교 실수로 미배정 요청이 의도치 않게
  `--owner`에 걸리는 것이다 — AC3/필터 테스트로 바로 드러난다.
- `summary`가 필터 로직을 `list --owner`와 다르게 구현하면 두 명령의 대상 집합이 어긋날 수 있다.
  같은 필터 표현을 재사용해 방지한다.
- PR2를 시작하기 전 `main`이 PR1 이후 추가로 바뀌었다면 최신 판에서 다시 시험을 돌려 확인한다.
- 기존 `list`/`show`/`complete` 동작 회귀는 기존 시험 3개가 그대로 신호를 준다 — 실패 시 숨기지
  않고 원인을 고친다.

## Proof

- PR1: `python3 -m unittest discover -s tests -v` 전체 통과(기존 3개 + 신규 `list --owner` 시험),
  `python3 tracker.py --data requests.json list --owner hana` 수동 실행 결과 관찰.
- PR2: 위 시험군 전체 통과(기존 3개 + PR1 시험 + 신규 `summary` 시험),
  `python3 tracker.py --data requests.json summary`와 `summary --owner hana` 수동 실행 결과 관찰,
  복사본에서 `complete` 후 `summary` 재실행한 결과 관찰.
- 아직 실행하지 않은 항목: 위 명령들은 각 PR 구현 시점에 실제로 실행해 근거를 남긴다. 이 계획
  단계에서는 실행하지 않았다.
