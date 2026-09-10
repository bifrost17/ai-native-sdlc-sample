# Plan: 담당자별 조회(`list --owner`)와 상태 요약(`summary`) (from intent 0001-owner-list-and-summary)
Upstream: spec.md@4d310729d5b9061b12441061737a6773b28c0502 (제품 책임자 수락 — R5를 `--json` 없는 기본
출력으로 명확히 하고 R8/AC9로 `summary --json`을 추가한 개정; AC8 참조를 R7에서 Constraints로 정정한
것 등 이전 개정의 기능 결정도 그대로 포함). Status: draft.

## Revision (PR2 구현 중)

- 계획 이탈: PR2에 `summary --json` 구현을 추가했다. spec.md R5(기본 출력 범위 명확화)/R8/AC9로
  반영했고, 제품 책임자가 spec.md@4d310729d5b9061b12441061737a6773b28c0502를 수락했다. 대상 선택·
  집계 로직은 기존 `summary`와 공유하고 출력 형식만 분기한다. 새 분기가 생긴 만큼 위험·검증 범위를
  아래 Risks/Proof에 반영했다 — "별도 위험 없음"으로 단정하지 않는다.
- 커밋 반영: 이 plan.md 개정은 `tracker.py`(`--json` 구현), `tests/test_tracker.py`(`--json` 시험),
  `README.md`(`--json` 사용법) 변경과 정확히 한 구현 커밋에 함께 담는다(PROCESS.md, GIT-WORKFLOW.md
  "구현 도중 변경 파일·작업 순서·PR 경계·검증 계획이 달라지면 이유와 plan.md를 해당 구현과 같은
  커밋에 담는다").

두 기능은 같은 파일(`tracker.py`)을 바꾸고 순서 우선순위(조회 먼저)가 정해져 있으므로 순차로
진행한다. 동시에 맡기면 같은 파일을 두 작업이 바꿔 병합 충돌과 교차 검증 비용이 생기고,
[GIT-WORKFLOW.md의 "작업과 PR"](../../docs/GIT-WORKFLOW.md)이 "같은 파일을 바꾸는 작업은 순차
진행하고, 파일이 달라도 공유 계약이나 실행 순서에 의존하면 독립적이라고 보지 않는다"고 명시한다.
`list --owner`를 먼저 검증·인도해 바로 쓰게 하고, `summary`는 그 위에서 이어간다.

각 기능의 구현·시험·사용 설명은 [PR-SIZE.md](../../docs/PR-SIZE.md)의 "한 동작의 구현·관련 시험·
사용 설명은 함께 둘 수 있다"에 따라 같은 PR에서 함께 다룬다.

## Files that change

- `tracker.py`
- `tests/test_tracker.py`
- `README.md`

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
5. `README.md`에 `list --owner <ID>` 실제 사용법(예시 명령과 예시 출력)을 남긴다. 기존 `list`,
   `show`, `complete` 사용법이 문서화돼 있지 않으므로 이번에 `list --owner`만 추가하면 동료가 참고할
   최소 사용 설명이 된다.
6. HUMAN이 diff와 동작을 검토하고 PR1을 `main`에 merge commit으로 통합한다. 통합 후 담당자들이
   `list --owner`를 바로 쓸 수 있다 — `summary` 완료를 기다리지 않는다.

**PR2 — `summary [--owner <ID>]` (PR1 머지 후 최신 `main`에서 시작)**

1. PR1이 머지된 `main`에서 새 브랜치를 만들고, `python3 -m unittest discover -s tests -v`로 PR1의
   기준이 그대로 통과하는지 먼저 확인한다.
2. `tracker.py`에 `summary` 서브파서(`--owner` 선택 인자, `--data`는 전역 옵션 공유)를 추가한다.
   `main()`에 `summary` 분기를 만들어 PR1의 필터 로직과 같은 방식으로 대상 집합을 고르고
   (`--owner` 없으면 전체, 있으면 `list --owner`와 동일한 선택), `status`별 개수를 세어
   `open\t<건수>`, `done\t<건수>` 순서로 출력한다(spec R4–R6).
2a. (개정, PR2 구현 중 추가) `summary` 서브파서에 `--json`(플래그) 인자를 추가한다. 대상 선택·집계는
    위와 동일 로직을 공유하고, `--json`이 있으면 `{"open": <건수>, "done": <건수>}` JSON 객체 한
    줄을, 없으면 기존 탭 두 줄을 출력한다(spec R8).
3. `tests/test_tracker.py`에 다음을 추가한다.
   - `summary`(옵션 없음) → `requests.json` 기준 `open\t3`, `done\t1` (AC4).
   - `summary --owner hana` → `open\t1`, `done\t1` (AC4).
   - `summary --owner nobody` → `open\t0`, `done\t0`, 종료코드 0 (AC5).
   - `summary`/`summary --owner` 실행 전후 데이터 파일 바이트 동일 (AC6의 summary 부분).
   - 임시 복사본에서 `complete R-101` 실행 후 같은 복사본으로 `summary --owner hana` →
     `open\t0`, `done\t2` (AC7, 상태 변화 반영 확인).
   - (개정) `summary --json`, `summary --owner hana --json` → `{"open": 3, "done": 1}`,
     `{"open": 1, "done": 1}` (AC9). `summary --owner nobody --json` → `{"open": 0, "done": 0}`
     (AC9). `--json` 실행 전후 데이터 파일 바이트 동일 (AC9, R6).
4. 전체 시험 실행, PR1이 추가한 `list --owner` 시험과 기존 `show`/`complete` 시험이 함께 통과하는지
   확인한다(회귀 없음).
5. `README.md`에 `summary`, `summary --owner <ID>` 사용법(예시 명령과 예시 출력)을 PR1에서 남긴
   `list --owner` 설명 옆에 이어 적는다. (개정) `summary --json` 사용법과 예시 출력도 함께 적는다.
6. HUMAN이 diff와 동작을 검토하고 PR2를 `main`에 merge commit으로 통합한다.

## Risks

- 가장 위험한 지점은 필터 비교에서 `None`과 문자열 비교 실수로 미배정 요청이 의도치 않게
  `--owner`에 걸리는 것이다 — AC3/필터 테스트로 바로 드러난다.
- `summary`가 필터 로직을 `list --owner`와 다르게 구현하면 두 명령의 대상 집합이 어긋날 수 있다.
  같은 필터 표현을 재사용해 방지한다.
- PR2를 시작하기 전 `main`이 PR1 이후 추가로 바뀌었다면 최신 판에서 다시 시험을 돌려 확인한다.
- 기존 `list`/`show`/`complete` 동작 회귀는 기존 시험 3개가 그대로 신호를 준다 — 실패 시 숨기지
  않고 원인을 고친다.
- (개정) `--json` 출력 분기를 추가하면서 기본(탭) 출력 경로를 실수로 바꿀 위험이 있다 — 대상
  선택·집계 로직은 공유하고 렌더링만 분기해 최소화했고, 기존 `summary` 시험(AC4/AC5, `--json`
  없음)과 신규 `--json` 시험(AC9)을 모두 돌려 두 경로가 각각 올바른지 확인한다.
- (개정) 검증한 범위: `--json` 결과의 키·값과 종료코드, 파일 미변경(R6)을 자동 시험으로 확인했다.
  검증하지 않은/남은 한계: JSON 출력의 키 순서·공백 형식은 spec R8이 규정하지 않으므로 고정 문자열
  비교 대신 파싱 비교로만 확인했다 — 다른 JSON 직렬화 방식(예: 들여쓰기)으로 바뀌어도 이 계획
  기준으로는 문제 삼지 않는다. `--json`과 다른 새 플래그의 동시 사용, 대용량 데이터에서의 동작은
  이번 범위에서 다루지 않는다(범위 밖).

## Proof

- PR1: `python3 -m unittest discover -s tests -v` 전체 통과(기존 3개 + 신규 `list --owner` 시험),
  `python3 tracker.py --data requests.json list --owner hana` 수동 실행 결과 관찰. (PR1 머지로 이미
  완료.)
- PR2: (개정, 이미 실행·확인함) `python3 -m unittest discover -s tests -v` 10개 전체 통과 —
  기존 3개(AC2/AC8) + PR1의 `list --owner` 2개(AC1/AC3) + `summary` 기본 출력 3개(AC4/AC5/AC7) +
  `summary --json` 2개(AC9). `python3 tracker.py --data requests.json summary`,
  `summary --owner hana`, 복사본에서 `complete` 후 `summary --owner hana` 재실행,
  `summary --json`, `summary --owner hana --json`, `summary --owner nobody --json` 수동 실행 결과를
  모두 직접 관찰해 spec 값과 일치함을 확인했다.
- 아직 실행하지 않은 항목: 없음(코드·시험 구현 범위 안에서는 모두 실행·확인함). 남은 것은 HUMAN의
  diff 검토와 PR2 merge 통합 승인뿐이다(Order of work 6단계) — 이 승인은 검증 실행과 별개다.
