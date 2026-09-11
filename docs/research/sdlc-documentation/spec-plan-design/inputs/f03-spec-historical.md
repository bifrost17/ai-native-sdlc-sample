# Spec: 담당자 목록 필터와 all/open/done 집계 (F03)
Upstream: intent.md@f35b19e. Status: draft.
References applied: EXPERIMENT.md(F03 확정 입력·역할·검증 명령), PROJECT-POLICY.md(미정 슬롯·검증 위치),
docs/PROCESS.md, docs/GIT-WORKFLOW.md, docs/PR-SIZE.md, docs/RELEASE-CONTROL.md(공개 제어 설계 절),
templates/spec.md; examples/skills/design-spec/SKILL.md과 그 참조
examples/skills/design-spec/references/design-depth.md(작성 절차·"staged exposure" 표 항목);
examples/skills/plan/examples/two-pr-spec.md·two-pr.md·plan/references/execution-depth.md는
같은 "목록 먼저, 집계 이어서"의 합성 작성 예시로 형식·분할 판단만 참고했고 실제 승인 근거로 쓰지
않았다(EXPERIMENT.md의 all/open/done 집계·표시 형식은 이 예시와 다르며 spec에서 새로 정한다).
tracker.py, tests/test_tracker.py, requests.json, USAGE.md를 읽고 현재 계약과 데이터를 확인했다.

`list`에 선택 `--owner <ID>`를 더해 exact-match 필터를 적용하고, 신규 `summary [--owner <ID>]`로
all/open/done 집계를 낸다. 두 동작은 EXPERIMENT.md가 정한 한 공개 단위이며, 완성 전에는 개발자
프로세스만 환경 변수로 켜서 시험하고 일반 실행은 기존 동작 그대로 유지한다(OFF 기본). 사람이 먼저
판단할 우려는 없다 — 아래 Flagged concerns에서 살핀 범위를 밝힌다.

## Requirements
- R1. 신규 동작은 환경 변수 `TRACKER_OWNER_INSIGHTS`로 켠다. 값이 미설정이거나 `"1"`/`"true"`
  (대소문자 무관) 이외이면 OFF다. OFF에서 `list`는 `--owner`를 인식하지 않고 `summary`
  하위 명령 자체가 존재하지 않는다(argparse가 알 수 없는 옵션/명령으로 거부). 기존
  list/show/complete의 동작·출력 열·JSON 필드·오류 메시지는 플래그 값과 무관하게 완전히 동일하다.
- R2. ON일 때 `list --owner <ID>`는 owner 필드가 `<ID>`와 문자열 그대로 정확히 일치하는 행만
  원본 순서로 출력한다. 완료(done) 행도 포함한다. owner가 `null`인 행은 어떤 문자열 ID와도
  일치하지 않는다(화면 표시용 `-`는 실제 값이 아니다). 대소문자 변환·부분 일치·정규화는 하지 않는다.
  일치하는 행이 없으면 stdout은 비고 rc=0이다. `--owner` 없이 쓴 `list`는 R1의 기존 동작과 같다.
- R3. ON일 때 `summary [--owner <ID>]`는 대상 집합(전체 또는 R2와 같은 exact-match 조건을 만족하는
  행)에서 all/open/done 개수를 `all\t<n>\nopen\t<n>\ndone\t<n>\n` 형식으로 그 순서대로 출력하고
  줄바꿈으로 끝난다. `--owner` 없으면 전체 4행 기준 집계다. 존재하지 않는 owner나 매칭되는 행이
  없으면 `all\t0\ndone\t0\nopen\t0\n`이 아니라 `all\t0\nopen\t0\ndone\t0\n`으로 0을 출력한다
  (오류가 아니다). 이 요구는 status가 `open`/`done` 두 값만 쓰는 현재 데이터 계약(requests.json,
  기존 complete 로직)에서 성립하는 불변식이다: all은 항상 open+done과 같다. 이 계약을 벗어난
  status 값의 처리는 이번 개발 항목의 범위 밖이다(Design, Constraints and scope 참고).
- R4. `list --owner`와 `summary`는 조회 전용이다. 두 명령 모두 대상 JSON 파일을 절대 쓰지 않는다.
  실행 전후 파일 바이트가 같다.
- R5. OFF 상태에서 산출한 결과는 현재 baseline(`tests/test_tracker.py`)과 완전히 같다. 즉 이번
  변경은 플래그 OFF인 한 어떤 기존 사용자에게도 관측 가능한 차이를 만들지 않는다. R1·R5의 이
  OFF/ON 구분은 `TRACKER_OWNER_INSIGHTS`와 그 조건부 분기가 존재하는 동안 적용된다 — 정리 이후의
  계약은 R6을 따른다.
- R6. 정리(clean-up) 이후 계약: Design의 모의 안정화 조건을 root가 실제로 충족했다고 선언하고
  별도 정리 PR을 진행하면, `TRACKER_OWNER_INSIGHTS`와 관련 조건부 분기를 제거한다. 이후
  `list --owner`와 `summary`는 플래그 없이 항상 존재하는 기본 명령이 되며 R2~R4의 동작(정확 일치·
  all/open/done 집계·read-only)은 그대로 유지한다. 정리 이후에는 R1의 "OFF에서 명령이 존재하지
  않는다"와 R5의 "OFF 결과가 baseline과 같다"는 전제 자체가 없어진다(플래그가 사라졌기 때문이다) —
  이는 계약을 약화한 것이 아니라 안정화된 최종 동작이 새 기본값이 된 것이다. 정리 이전에는 R1~R5가
  그대로 적용된다.

## Acceptance criteria
데이터는 `requests.json`의 4행(R-101 hana/open, R-102 min/open, R-103 hana/done, R-104 owner=null/open)
을 기준으로 하며, 쓰기 시험은 임시 복사본을 쓴다(기존 test_tracker.py 방식과 동일).
- AC1 → R1,R5: 플래그 미설정에서 `list --owner hana`, `list --owner=hana`류 시도는 argparse 오류로
  거부되고(`unrecognized arguments`), `summary`도 알 수 없는 명령으로 거부된다. 같은 상태에서
  옵션 없는 `list`/`show`/`complete`는 기존 baseline 세 시험과 동일하게 동작한다.
- AC2 → R1,R2: 플래그를 `"1"`로 설정하면 `list --owner hana`가 R-101, R-103만 그 순서로 출력한다.
  `TRACKER_OWNER_INSIGHTS=yes`처럼 인정하지 않는 값은 OFF와 같다(AC1 재확인).
- AC3 → R2,R4: ON에서 `list --owner nobody`, `list --owner HANA`, `list --owner -` 각각 빈 stdout·
  rc=0이며 파일 바이트가 실행 전과 같다. `owner=null`인 R-104는 어떤 문자열로도 매칭되지 않는다.
- AC4 → R3,R4: ON에서 `summary`(옵션 없음)는 `all\t4\nopen\t3\ndone\t1\n`, `summary --owner hana`는
  `all\t2\nopen\t1\ndone\t1\n`, `summary --owner min`은 `all\t1\nopen\t1\ndone\t0\n`,
  `summary --owner nobody`는 `all\t0\nopen\t0\ndone\t0\n`을 출력하고 각각 파일은 변경되지 않는다.
- AC5 → R2,R3,R4: 별도 복사본에서 `complete R-101` 실행 후 ON 상태로 `summary --owner hana`를
  호출하면 `all\t2\nopen\t0\ndone\t2\n`이 되고, `list --owner hana`는 두 행 모두 status가
  `done`으로 출력된다(complete 자체 재검증이 아니라 집계·필터가 최신 파일 상태를 읽는지 확인).

## Design
argparse 서브파서 구성 전에 `os.environ.get("TRACKER_OWNER_INSIGHTS", "")`를 읽어 켜짐 여부를
정하고, ON일 때만 `list`에 선택 `--owner` 인자를 추가하고 `summary` 서브파서를 등록한다. OFF에서는
현재 파서 구성과 동일해 새 옵션·명령이 애초에 존재하지 않는다 — 이는
docs/RELEASE-CONTROL.md가 요구하는 "메뉴만 숨기지 않고 직접 접근 경로도 막는다"를 CLI 인자
차원에서 만족한다. 파일 읽기·JSON 파싱은 기존 흐름을 그대로 쓰고, 목록 필터와 집계 모두 이미 읽은
`requests` 배열을 한 번 순회해 만든다. 별도 인덱스·정렬·저장은 두지 않는다(intent 제약).

필터: `[row for row in requests if row["owner"] == args.owner]`처럼 원본 순서를 보존하는 단순
비교면 충분하다. 집계는 대상 집합에서 `len(subset)`과 status별 개수를 세어 all/open/done 세 줄로
출력한다. 이 항목의 데이터 계약은 status가 `open`/`done` 두 값만 쓰는 현재 스키마로 한정된다
(requests.json, 기존 complete 로직과 같은 전제). all=open+done 불변식(R3)은 이 계약 안에서만
보장하는 것이며, 계약을 벗어난 값(예: 새 상태 추가)의 처리는 이번 개발 항목의 범위 밖이다 — 두
경쟁하는 처리 방식을 제안하지 않는다. 스키마가 바뀌면 별도 intent/spec에서 R3를 다시 정의한다.

공개 단위(RELEASE-CONTROL.md 적용): 공개 단위는 "담당자 목록 필터 + all/open/done 집계" 전체다.
PR1~PR2 개발 기간에는 시험 ON 상태에서 목록만 동작하고 집계가 아직 코드에 없는 부분 상태가 실제로
존재하며, 이는 개발자 프로세스의 시험용 **부분 TEST 노출**로 허용된다(RELEASE-CONTROL.md의
"독립적으로 완성한 부분부터 시험") — plan의 PR1이 이 상태다. 허용되지 않는 것은 **부분 GENERAL
공개**다: root는 목록과 집계가 둘 다 완성·검증되기 전에는 일반 기본(OFF→ON)을 전환하지 않는다.
하나의 환경 변수 `TRACKER_OWNER_INSIGHTS`를 PR1·PR2가 공유해 이 구분을 표현한다. 신뢰 대상은
로컬 개발자 프로세스가 같은 셸에서 이 변수를 켜고 호출하는 시험 실행뿐이며 원격 서버 대상이나
사용자 그룹 구분은 없다(EXPERIMENT.md: 로컬 모의). 설정 실패/미설정/인식 못 하는 값은 모두 OFF로
접힌다(R1). 이 변수는 프로세스 시작 시 매 실행마다 새로 읽으므로 별도 캐시나 재시작 절차가 없다 —
CLI가 실행될 때마다 새 프로세스이기 때문이다. 공개(=OFF→ON 기본 전환) 결정과 그 근거는
EXPERIMENT.md에 따라 root(HUMAN)가 하며 결정 기록 위치는 `intent/f03-owner-insights/decisions.md`와
root가 보존하는 대화다. 중단(다시 OFF)도 같은 변수 값을 되돌리는 것으로 충분하며 파일 쓰기가 없어
데이터 되돌림은 필요 없다.

정리(clean-up, R6): PR2까지 통합되고 root가 명시적으로 정리를 요청하면 별도 정리 PR을 진행한다.
이번 로컬 프로브의 모의 안정화 조건은 root가 정한 다음 값이다 — PR2의 ON/OFF와 인접 흐름(list/
show/complete) 검증을 마친 뒤, root가 모의 공개/중단 관측을 기록하고 이 제어를 읽는 구버전
프로세스나 롤백 대상이 없다고 선언한다. 이 조건은 로컬 정리 시험을 대신할 뿐이며 실제 운영
안정화 기간이나 다중 배포 대상의 안전성을 입증하지 않는다. 조건 충족 여부와 그 선언은
`intent/f03-owner-insights/decisions.md`에 남긴다. 정리 PR의 실행 상세(제거 대상 코드·시험·문서,
남길 회귀 시험)는 plan이 갖는다.

## Constraints and scope
Python 3.9+ 표준 라이브러리만 쓰고 원본 `requests.json`은 보존하며 쓰기 시험은 사본을 쓴다(intent).
업무 코드 변경은 `tracker.py` 한 파일이면 충분하고 시험·문서는 별도 파일이다. 작은 순차 PR
(목록 → 집계)과 동일한 공개 제어 재사용은 plan에서 다룬다. 미배정 전용 조회, 부분/대소문자 무관
일치, 복수 담당자 동시 조회, status 재정의·새 저장 필드·원격 시스템·설치·배포는 범위 밖이다.
표시 형식(`all/open/done` 순서의 탭 구분 줄)은 이번 spec에서 새로 확정한 계약이며 바꾸려면 이
문서 개정이 먼저 필요하다.

## Open questions
없음 — intent의 질문 없음을 이어받았고, EXPERIMENT.md가 확정한 입력(exact-match, all/open/done,
빈 결과 0, 원본 순서, read-only, 같은 공개 제어)을 그대로 반영했다. 표시 형식과 플래그 이름/값은
이 spec에서 새로 제안하는 결정이며, 위 Design에 근거를 남겼다. 리뷰에서 형식이 바뀌면 이 문서를
개정한다.
- Q4 answered: root의 32d64b9 리뷰에서 세 가지를 확인했다 — (1) 부분 TEST 노출과 부분 GENERAL
  공개는 서로 다른 것이며 전자는 PR1 시점에 허용된다(위 공개 단위 문단, R1 유지), (2) all=open+done
  불변식(R3)은 open/done만 쓰는 현재 데이터 계약에 한정하고 다른 status 처리는 범위 밖이다(R3,
  Design), (3) 모의 안정화 조건과 정리 이후 계약을 root가 직접 정의했다(R6, Design "정리"). 세
  결정 모두 이 spec에 반영했으며 `intent/f03-owner-insights/decisions.md`에 근거를 남겼다.

## Flagged concerns
없음 — 확인한 범위: 외부 연동·인증·권한 경계를 바꾸지 않고, 새 저장 형식이나 원격 전송이 없으며,
플래그 기본값이 OFF라 일반 실행에 관측 가능한 변화가 없다(R1,R5). PROJECT-POLICY.md의 다른
미정 슬롯(이름·정책·CI 등)은 이번 F03 범위와 무관해 건드리지 않았다. 이는 팀의 모든 정책을
검토했다는 뜻은 아니며, 채택 팀이 별도 제약을 주면 관련 R·Design을 다시 검토한다.
