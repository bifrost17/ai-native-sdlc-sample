# Intent: 담당자별 조회와 상태 요약이 안 된다
Author: HUMAN (Codex, simulated). Status: draft.

## Problem

사내 요청 CLI(`tracker.py`)는 `list`, `show <ID>`, `complete <ID>`만 제공한다. `list`는 항상 전체
요청을 원본 순서로 보여줄 뿐, 담당자로 골라 볼 방법이 없다. 주간 확인 때 한 담당자의 열린 요청과
완료 요청이 각각 몇 건인지 세려면 전체 목록을 사람이 직접 눈으로 세야 한다.

## Proposed outcome

두 가지를 더할 수 있다.

1. `list --owner <ID>`로 그 담당자의 요청만, 기존과 같은 탭 형식·원본 순서로 볼 수 있다.
   완료된 요청도 포함한다. 옵션이 없는 `list`는 지금처럼 전체를 보여준다.
2. `summary [--owner <ID>]`로 open 건수와 done 건수를 두 줄(`open\t건수`, `done\t건수` 순서)로
   볼 수 있다. `--owner` 없이 실행하면 미배정(owner가 null)을 포함한 전체 건수, `--owner <ID>`를
   주면 `list --owner <ID>`와 같은 선택 대상의 건수다.

두 기능은 별도 명령이며 독립적으로 쓸 수 있다. 담당자에게 먼저 인도할 대상은 `list --owner`이고,
`summary`는 다음 주간 확인 전까지 이어서 준비하는 별도 결과다. 구현·검토·인도 순서는 구현 계획에서
정한다.

## Affected users and systems

- 사내 요청 CLI를 쓰는 담당자와, 주간 확인을 하는 사람(제품 책임자 역할의 HUMAN).
- 영향 받는 파일: `tracker.py`(명령 추가), `tests/test_tracker.py`(신규 동작 검증). `requests.json`의
  스키마와 기존 명령 동작은 바꾸지 않는다.

## Constraints

- 기존 명령(`list`, `show`, `complete`)과 저장 필드는 그대로 유지한다 (`case.json` F02-F2, 제약).
- `list --owner`와 `summary`는 원본 파일을 바꾸지 않는다. 다만 사람이 복사본에서 `complete`를 실행한
  뒤 그 복사본으로 `summary`를 실행하면, 바뀐 상태를 반영해 보여준다.
- 담당자 ID는 대소문자를 구분해 정확히 일치하는 것만 비교한다. 소문자로 바꾸거나 유사 일치를
  시도하지 않는다 (`case.json` F02-F4: 담당자 ID는 소문자 ASCII).
- `--owner`에 데이터에 없는 ID나 대소문자가 다른 값(예: `HANA`)을 주면, `list --owner`는 빈 표준출력과
  종료코드 0, `summary --owner`는 `open\t0` / `done\t0` 두 줄과 종료코드 0으로 처리한다. 오류로
  다루지 않는다.
- `summary` 옵션 없이 실행할 때 담당자를 문자열로 고르는 것과 별개로 미배정만 따로 선택해 보는
  기능은 이번 범위에 없다.
- 서버·배포·외부 서비스를 더하지 않는 작은 CLI 변경이다 (`case.json` constraints).

## Open questions

- 없음 — 위 결정은 이번 의도 확인에서 모두 확정했다. spec 단계에서 새로 드러나는 사항이 있으면
  그때 이어서 기록한다.
