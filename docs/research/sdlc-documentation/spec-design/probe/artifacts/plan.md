# Plan: `list --owner <ID>`로 담당자 조회 좁히기 (from intent 0001-owner-filter)
Upstream: spec.md@f3b3bbb. Status: draft.

`list` 서브커맨드에 선택 인자 `--owner`와 `--include-done`을 추가한다. 기본은 담당자 일치 +
`status == "open"`, `--include-done`을 더하면 완료 포함. `--include-done`을 `--owner` **옵션 자체를
생략한 채** 쓰면 사용법 오류(rc=2)다 — `--owner ''`처럼 빈 문자열 값을 명시한 경우는 옵션 생략이
아니라 정상 조회이므로 이 둘을 구현에서 혼동하지 않아야 한다(spec.md R3). `show`/`complete`와
옵션 없는 `list`는 손대지 않는다. `--owner` 분기는 기존 `try/except`(OSError, ValueError, KeyError,
TypeError → rc=2) 안에서 동작하므로, 그 경로를 이번에 처음 시험으로 확인한다. 검증 명령은 spec에서
확정한 `python3 -m unittest discover -s tests -v`를 그대로 쓴다.

이 판은 spec.md@f3b3bbb(구현 착수 전 사용자 피드백 D4 반영, 아직 다음 단계가 수락한 판은 아님)에
미리 맞춘 것이다(HUMAN이 이번 대화에서 명시적으로 허용). spec이 이후 더 바뀌면 이 plan도 같은
Upstream 갱신 절차(docs/GIT-WORKFLOW.md)로 다시 맞춘다.

## Files that change
tracker.py
tests/test_owner_filter.py (new)

## Order of work
1. 기준선 확인: 변경 전 `python3 -m unittest discover -s tests -v`가 통과함을 확인한다. 또한 손상된
   JSON(예: 파싱 불가 텍스트)으로 현재 `tracker.py list`를 실행해, 읽기·파싱 실패 시 rc=2와 stderr
   메시지가 나오는 기존 동작을 실제로 관찰한다. 이 경로는 tests/test_tracker.py에 시험이 없으므로
   여기서 실제 동작을 먼저 확인해 이후 회귀 시험의 기준으로 삼는다.
2. tracker.py 구현: `list` 서브파서에 선택 인자 `--owner`(문자열, 기본값 `None`)와 `--include-done`
   (플래그, 기본 False)을 추가한다. 인자 파싱 직후 `args.command == "list"`이고 `args.include_done
   and args.owner is None`이면 `list` 서브파서(또는 최상위 parser 중 사용법 메시지가 더 정확한 쪽)의
   `.error(...)`를 호출해 rc=2로 종료한다 — 반드시 `args.owner is None`으로 판정하고 `not
   args.owner`(빈 문자열의 참·거짓)로 판정하지 않는다. `not args.owner`를 쓰면 `--owner ''`처럼
   빈 문자열 값을 명시한 정상 조회까지 옵션 생략으로 오판해 사용법 오류가 돼 버린다(spec.md R3).
   이 검사는 데이터 파일을 읽기 전에 끝내 R6(조회 무변경)에 영향이 없어야 한다(spec.md Design).
   데이터를 읽은 뒤 `args.owner is not None`이면 배열을 원래 순서대로 순회하며
   `request["owner"] == args.owner`이고, `args.include_done`이 아니면 `request["status"] == "open"`도
   함께 만족하는 행만 남기고 기존 `display()`로 출력한다. 대소문자 변환·부분 일치는 넣지 않는다.
   `--owner` 미지정 시(옵션 없는 `list`) 상태 제한 없이 기존 그대로 전체 출력한다. `show`/`complete`
   분기와 바깥 `try/except` 구조는 그대로 둔다.
3. 새 시험 작성 (tests/test_owner_filter.py, 각 시험은 requests.json을 임시 파일로 복사해 사용):
   - AC1: `list --owner hana`(단독)가 미완료 R-101만 출력하고(완료 R-103 제외) 파일이 변경되지
     않음을 확인.
   - AC2: `list --owner hana --include-done`이 R-101, R-103을 그 순서로 출력하고 파일이 변경되지
     않음을 확인.
   - AC3: `list --owner nobody`, `list --owner HANA`, `list --owner -`(모두 단독, 기본 open-only)
     각각 stdout이 비고 rc=0이며 파일이 변경되지 않음을 확인.
   - AC4: `list --include-done`(`--owner` 옵션 자체를 생략)을 실행하면 rc=2, stderr에 사용법
     메시지가 있고 파일이 변경되지 않음을 확인. 대조로 `list --owner ''`와
     `list --owner '' --include-done`은 둘 다 사용법 오류가 아니라 stdout이 비고 rc=0이며 파일이
     변경되지 않음을 같은 시험 메서드나 인접 시험으로 함께 확인해, 빈 문자열 값과 옵션 생략을
     혼동하지 않는지 드러낸다.
   - AC5: 옵션 없는 `list`가 네 행(모든 상태, 담당자 제한 없이)을 원래 순서·열로 출력함을 확인
     (기존 tests/test_tracker.py의 해당 시험과 별개로, 새 인자 추가가 회귀를 만들지 않았는지 이
     파일에서도 직접 확인).
   - 읽기·파싱 실패 회귀: 손상된 JSON 파일에 대해 `list`와 `list --owner hana`(단독) 양쪽 모두 rc=2와
     stderr 메시지를 반환함을 확인한다. `--owner` 분기가 같은 예외 처리 경로를 공유하므로, 이번
     변경 전에는 어느 명령에도 이 경로를 확인하는 시험이 없었다는 점을 감안해 새로 추가한다.
4. 검증 실행: `python3 -m unittest discover -s tests -v`를 다시 실행해 기존 시험과 새 시험이 모두
   통과하는지 확인하고, 실행한 명령과 결과를 보존 대화·커밋에 남긴다(spec.md Flagged concerns).

## Risks
- 인자 추가가 argparse의 기존 `list` 무옵션 경로나 `show`/`complete`의 필수 위치 인자 처리에
  영향을 줄 수 있다. → AC5 재확인과 기존 tests/test_tracker.py 전체 재실행으로 발견한다.
- `--include-done`과 `--owner`의 의존 관계를 argparse 표준 기능만으로 표현할 수 없어 수동 검사가
  필요하다. 검사 위치를 파일 읽기 이전에 두지 않으면 R6(조회 무변경)이 깨질 수 있다. → AC4로
  rc=2·무변경을 함께 확인한다.
- 옵션 생략 판정에 `not args.owner`처럼 빈 문자열의 참·거짓을 쓰면 `--owner ''`가 사용법 오류로
  잘못 처리된다. → AC4의 `--owner ''` 대조 사례로 발견한다.
- `--include-done` 없을 때의 기본 open-only 조건과 담당자 조건을 같은 줄에서 실수로 OR로 묶으면
  전혀 다른 결과가 나온다. → AC1(open만)과 AC2(완료 포함)를 대비시켜 발견한다.
- 필터 비교에서 실수로 `.lower()`나 부분 일치를 넣으면 R1·R2의 정확 일치 요구를 어긴다. → AC3의
  `HANA` 사례로 발견한다.
- `--owner` 분기가 기존 예외 처리 경로를 공유하는데, 그 경로는 이번 변경 전까지 어떤 명령에도
  시험이 없었다. 이번에 새 시험을 추가하지 않으면 이 공유 경로의 회귀를 아무 시험도 잡지 못한다.
  → 3단계의 읽기·파싱 실패 시험으로 닫는다.
- `null` 담당자가 필터에서 자연히 제외되는지(명시적 `is not None` 분기 없이)는 구현 실수로 깨지기
  쉽다. → AC3의 `-` 사례(화면 표시 문자열과 실제 값 혼동 방지)로 발견한다.

## Proof
`python3 -m unittest discover -s tests -v` 실행, 성공 기준은 전체 통과(기존 3개 + 새로 추가하는
AC1~AC5 및 읽기·파싱 실패 시험). 1단계의 손상 JSON 수동 실행 관측은 이 계획 작성 시점에는 아직
실행하지 않았으며, 구현 단계에서 실제로 실행하고 명령·출력·rc를 기록한다. 이 문서 작성 자체로는
어떤 검사도 실행하지 않았다.
