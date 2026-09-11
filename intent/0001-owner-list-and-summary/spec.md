# Spec: 담당자별 조회(`list --owner`)와 상태 요약(`summary`) (from intent 0001-owner-list-and-summary)
Upstream: intent.md@17bf490414d601ee2da197b7e5363831d2fc7cea. Status: draft.
References applied: case.json (F02-F1~F4, constraints, baseline) — 저장소 내 데이터셋 계약 파일로 직접 확인.

이번 개정: PR2 구현·리뷰 중 합의한 `summary --json` 출력(R8, AC9)을 반영한다. R1–R7과 기존
AC1–AC8의 결정은 그대로 유지하고, R5는 `--json` 미지정 시로 범위를 한정하는 문구만 정정했다.
intent.md의 문제·제약은 바뀌지 않았으므로 intent.md는 갱신하지 않는다.

## Requirements

- R1. `list`에 `--owner <ID>` 옵션을 추가한다. 지정하면 그 담당자의 요청만, 기존 `list`와 같은
  탭 형식(ID, 상태, 담당자, 제목)·원본 파일 순서로 출력한다. `open`과 `done` 상태 모두 포함한다.
- R2. `--owner` 없이 `list`를 실행하면 지금과 동일하게 전체 요청을 원본 순서로 출력한다.
- R3. `--owner <ID>`가 데이터에 없는 값이거나 대소문자가 다른 값이면, `list --owner`는 표준출력이
  비고 종료코드 0이다. 오류로 취급하지 않는다.
- R4. 새 `summary` 명령을 추가한다. `--owner` 없이 실행하면 전체 요청(owner가 null인 미배정 포함)
  대상으로, `--owner <ID>`를 주면 `list --owner <ID>`와 같은 선택 대상으로 open 건수와 done 건수를
  집계한다.
- R5. `--json` 없이 `summary`를 실행하면 출력은 `open\t<건수>`, `done\t<건수>` 두 줄, 이 순서로
  고정한다. 대상이 0건이면 `open\t0`, `done\t0`을 출력하고 종료코드는 0이다.
- R6. `list --owner`와 `summary`는 어떤 경우에도 데이터 파일을 쓰지 않는다(조회 전용).
- R7. 담당자 ID 비교는 대소문자를 구분하는 정확 일치만 사용한다. 정규화나 유사 일치를 하지 않는다.
- R8. `summary`에 `--json` 옵션을 추가한다. 지정하면 R4가 고른 대상 집합의 open/done 집계를
  `open`, `done` 두 키를 가진 JSON 객체 한 줄로 출력한다. 각 값은 정수 건수이며, 키 순서와 공백은
  규정하지 않는다. `--owner`와 함께 쓸 수 있고, 대상이 0건이거나 `--owner`가 데이터에 없는 값·대소문자가
  다른 값이면 `{"open": 0, "done": 0}`을 출력하고 종료코드는 0이다(R3·R7과 일관). `--json` 없이
  실행하면 R5의 텍스트 출력을 그대로 유지한다.

## Design

- `tracker.py`의 `argparse` 서브파서 구성에 `--owner` 옵션을 `list`에 추가하고, `summary`라는 새
  서브파서를 만들어 같은 옵션을 받는다. 두 명령 모두 기존 `--data` 전역 옵션을 그대로 쓴다.
- 필터링은 로딩한 `requests` 리스트에 대한 순서 보존 선택(`[r for r in requests if ...]`)으로 구현한다.
  담당자가 없는 요청은 `owner`가 `None`이므로 `--owner` 필터는 문자열 값과 비교해 `None`과 절대
  일치하지 않는다(R7과 일관).
- `summary`는 `--owner` 유무로 대상 집합을 고른 뒤(`--owner` 없으면 전체, 있으면 위와 같은 필터),
  그 집합 안에서 `status == "open"`/`"done"` 개수를 세어 고정 순서로 출력한다. 별도 카운팅 유틸을
  두 명령이 공유할 필요는 없다 — `summary`는 필터링 후 집계만 하면 된다.
- 집계 결과(open/done 정수 건수)는 `--json` 여부와 무관하게 동일한 카운팅 한 번으로 얻는다.
  `--json`은 같은 집계를 `open\t<건수>`/`done\t<건수>` 텍스트 대신 JSON 객체로 직렬화하는 출력
  분기일 뿐, 별도 집계 경로를 두지 않는다.
- 기존 `display()`, `list`/`show`/`complete`의 파일 읽기·쓰기 로직, 예외 처리(`OSError, ValueError,
  KeyError, TypeError` → 종료코드 2)는 그대로 재사용한다. 새 명령도 같은 예외 처리 경로를 공유해
  파일이 없거나 스키마가 깨진 경우 기존과 같은 오류 메시지·종료코드를 낸다.
- 데이터 흐름: `--data` 경로 읽기 → JSON 파싱(원본 dict 유지) → `requests` 리스트 선택/필터 →
  출력. `list --owner`와 `summary`는 파싱한 `data`를 쓰기 없이 그대로 버린다(`complete`만 쓰기).

## Constraints

intent.md에서 이어받음:

- 기존 명령(`list`, `show`, `complete`)과 저장 필드는 그대로 유지한다.
- `list --owner`와 `summary`는 원본 파일을 바꾸지 않는다. 복사본에서 `complete`를 실행한 뒤 그
  복사본으로 `summary`를 실행하면 바뀐 상태를 반영한다(다음 실행마다 파일을 새로 읽으므로 자연히
  만족됨 — 별도 캐시나 상태를 두지 않는다).
- 담당자 ID는 대소문자를 구분해 정확히 일치하는 것만 비교한다.
- `--owner`가 데이터에 없거나 대소문자가 다른 값이면 오류가 아니라 빈 결과(종료코드 0)로 다룬다.
- 미배정만 따로 선택해 보는 기능은 이번 범위에 없다.
- 서버·배포·외부 서비스를 더하지 않는 작은 CLI 변경이다.

## Open questions from intent

- 없음 (intent.md에 기록된 대로, 이번 의도 확인에서 모두 확정됨).

## Flagged concerns

- 없음. 적용할 정책 중 `PROJECT-POLICY.md`의 "적용할 정책" 표는 대부분 미정이지만, 이 변경 범위
  (로컬 조회 전용 CLI, 외부 전송 없음)에는 해당 미정 항목이 걸리지 않는다고 판단했다. 다른 판단이
  필요하면 제품 책임자가 정한다.

## Out of scope

- 미배정(owner=null)을 별도 값으로 선택해 조회/집계하는 기능.
- `--owner`에 대소문자 정규화, 부분 일치, 여러 담당자 동시 선택.
- `show`/`complete`의 동작 변경, 저장 스키마 변경, 새 필드 추가.
- 서버화, 원격 데이터 소스, 인증·권한 처리.

## Acceptance criteria

- AC1 → R1: `list --owner hana`가 `requests.json` 기준 `R-101`, `R-103`을 원본 순서(R-101 먼저)로,
  기존과 동일한 탭 형식으로 출력한다. `R-103`(done)도 포함된다.
- AC2 → R2: `--owner` 없는 `list`가 지금과 동일하게 전체 4건을 원본 순서로 출력한다(기존 시험
  `test_list_preserves_order_and_does_not_write`가 계속 통과).
- AC3 → R3: `list --owner HANA`(데이터에 없는 대소문자 변형)와 `list --owner nobody`가 표준출력
  없이 종료코드 0을 반환한다.
- AC4 → R4, R5: `summary`(옵션 없음)가 `requests.json` 기준 `open\t3`, `done\t1` 두 줄을 이 순서로
  출력한다. `summary --owner hana`는 `open\t1`, `done\t1`을 출력한다.
- AC5 → R5: `summary --owner nobody`가 `open\t0`, `done\t0`을 출력하고 종료코드 0이다.
- AC6 → R6: `list --owner`와 `summary` 실행 전후로 데이터 파일의 바이트가 동일하다(기존
  `test_list_preserves_order_and_does_not_write`와 같은 방식으로 검증).
- AC7 → R6(복사본 시나리오): 임시 복사본에서 `complete R-101`을 실행한 뒤 그 복사본으로
  `summary --owner hana`를 실행하면 `open\t0`, `done\t2`를 반환한다(상태 변화가 반영됨).
- AC8 → Constraints(기존 명령·저장 필드 유지): 기존 `show`/`complete`의 ID 미존재 처리(종료코드 1,
  stderr 메시지)는 이번 변경으로 달라지지 않는다 — 기존 시험 `test_show_existing_and_missing_id`,
  `test_complete_changes_only_target_status_and_is_repeatable`가 그대로 통과해야 한다.
- AC9 → R8: `summary --json`이 `requests.json` 기준 `{"open": 3, "done": 1}`을 출력한다(JSON으로
  파싱한 값 비교, 키 순서·공백은 무관). `summary --owner hana --json`은 `{"open": 1, "done": 1}`을,
  `summary --owner HANA --json`과 `summary --owner nobody --json`은 각각 `{"open": 0, "done": 0}`을
  종료코드 0으로 출력한다. 위 실행 전후로 데이터 파일 바이트가 동일하다(R6).
