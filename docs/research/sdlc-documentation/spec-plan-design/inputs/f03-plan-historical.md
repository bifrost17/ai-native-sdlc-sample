# Plan: 담당자 목록 필터와 all/open/done 집계 (from intent f03-owner-insights)
Upstream: spec.md@f1ba82ecb285f69ae12136578e131972f6281753. Status: draft.
DRAFT 허용: HUMAN(Codex root)이 spec과 함께 검토하도록 초안 작성을 허용했다
(`intent/f03-owner-insights/decisions.md` "초안 동시 작성 허용"). 이 plan 자체의 실행·구현 허가는
아니며, HUMAN이 spec을 수락한 뒤 이 plan을 별도로 수락해야 한다.
새 세션이 대화 없이 실행할 수 있도록 필요한 참조: EXPERIMENT.md(검증 명령·역할·데이터),
docs/RELEASE-CONTROL.md, docs/GIT-WORKFLOW.md, docs/PR-SIZE.md, USAGE.md, tracker.py,
tests/test_tracker.py, requests.json, 위 spec.md 전체.

## Files that change
- `tracker.py`: PR1에서 플래그 읽기·조건부 서브파서 구성·`--owner` 필터, PR2에서 같은 플래그·
  필터를 재사용하는 `summary` 서브파서와 집계. 새 파일 아님.
- `tests/test_owner.py` (new, PR1): 플래그 OFF 거부, ON exact-match·순서·null 비매칭·빈 결과·
  read-only(AC1-AC3).
- `tests/test_summary.py` (new, PR2): all/open/done 형식·전체/담당자별/없는 담당자 집계·
  complete 이후 최신 상태 반영·read-only(AC4-AC5). PR2 시점에 test_owner.py도 재실행한다.
- `USAGE.md`: 플래그 이름·기본 OFF·개발자 시험 실행 예시, `list --owner`(PR1)와
  `summary [--owner]`(PR2) 사용법을 추가한다. 두 PR 모두 기존 세 줄(list/show/complete) 설명은 유지한다.
- 조건부(4단계, root의 명시적 정리 요청 후에만): `tracker.py`에서 플래그 읽기·조건부 분기 제거,
  `tests/test_owner.py`·`tests/test_summary.py`에서 OFF 거부를 확인하던 케이스 제거,
  `USAGE.md`에서 플래그 설정 언급 제거. 세 파일 모두 이번 PR1/PR2에서는 바꾸지 않는다.

## Order of work
1. **기준 확인.** 작업 브랜치를 최신 `main`에서 만들고 `python3 -m unittest discover -s tests -v`로
   기존 3개 시험이 그대로 통과하는지 먼저 확인한다(회귀 기준선).
2. **PR1 — 담당자 목록 필터, 공개 제어 도입.** `TRACKER_OWNER_INSIGHTS` 읽기와 조건부 argparse
   구성을 넣고, OFF에서 `--owner`/`summary`가 존재하지 않음을 먼저 확인한 뒤 ON 경로의 필터를
   구현한다(R1,R2,R4). `tests/test_owner.py`와 `USAGE.md`의 목록 절을 함께 커밋한다.
   main에 머지되면 일반 실행은 기존과 동일(OFF)하고, 개발자 프로세스만 플래그를 켜 목록 필터를
   시험할 수 있다. summary는 아직 없다 — 이 PR만으로 공개 단위가 끝난 것은 아니다.
3. **PR2 — all/open/done 집계.** PR1이 검토·통합된 뒤 그 최신 `main`에서 새 브랜치를 만들고
   `summary` 서브파서와 집계를 같은 플래그·같은 exact-match 의미로 연결한다(R3,R4,R5).
   `tests/test_summary.py`와 `USAGE.md`의 요약 절을 추가하고, `test_owner.py`를 다시 실행해
   목록 동작이 그대로인지 확인한다. main에서 목록·요약·기존 list/show/complete가 모두 ON/OFF
   양쪽에서 의도대로 동작하면 이번 공개 단위(F03)의 구현 범위가 끝난다.
4. **공개/중단 결정.** PR2 통합 후 root가 실제로 `TRACKER_OWNER_INSIGHTS`를 일반 기본으로 켤지
   결정한다(EXPERIMENT.md의 이후 단계: "같은 코드에서 설정 공개/중단"). 이 plan은 켜는 코드
   변경을 만들지 않는다 — 값 전환은 root의 로컬 환경 설정과 결정 기록
   (`intent/f03-owner-insights/decisions.md`)으로 이루어진다.
5. **정리 PR(조건부 — root의 명시적 요청 후에만 실행).** 트리거는 spec R6/Design "정리"의 모의
   안정화 조건: PR2의 ON/OFF와 인접 흐름(list/show/complete) 검증 완료, root의 모의 공개/중단
   관측 기록, 이 제어를 읽는 구버전 프로세스·롤백 대상이 없다는 root의 선언 — 이 세 가지가
   `intent/f03-owner-insights/decisions.md`에 기록된 뒤에만 착수한다. 이 단계는 이번 PR1/PR2
   작업의 일부로 지금 실행하지 않으며, root가 별도로 착수를 요청할 때 새 브랜치에서 수행한다.
   범위: `tracker.py`에서 `TRACKER_OWNER_INSIGHTS` 읽기와 조건부 서브파서 분기를 제거해
   `list --owner`/`summary`를 무조건 사용 가능한 명령으로 만든다(R6). `tests/test_owner.py`·
   `tests/test_summary.py`에서 OFF 거부를 확인하던 케이스만 제거하고, exact-match·all/open/done·
   read-only 등 최종 동작을 확인하는 나머지 시험은 그대로 남겨 회귀 시험으로 유지한다.
   `USAGE.md`에서 플래그 설정·시험 방법 언급을 지우고 두 명령을 기본 사용법으로 옮긴다. 기존
   list/show/complete 관련 시험·설명은 전혀 건드리지 않는다.

두 PR은 `tracker.py`·`USAGE.md`와 플래그·exact-match 의미를 공유하므로 병렬 세션 없이 순차
진행한다. 코드량이 작다는 이유로 한 PR에 몰아 목록 인도를 늦추거나, 시험만 별도 PR로 떼지 않는다.
실제 브랜치명·PR 번호·수락 SHA·머지 커밋은 실행 시 `intent/f03-owner-insights/decisions.md`에 남긴다.

## Risks
- 가장 위험한 단계는 PR2에서 플래그 읽기·필터 로직을 목록과 공유하도록 리팩터링하는 부분이다.
  잘못 공유하면 PR1이 이미 통과시킨 exact-match·null 비매칭·순서·OFF 거부가 깨질 수 있다.
  대응: PR2에서 `test_owner.py`를 반드시 재실행하고, 실패하면 공유 리팩터링을 수정한 뒤
  재검증한다 — 이미 사용 가능한 목록 기능이 계속 됐다고 재판정하지 않는다.
- OFF 기본값이 새지 않는지가 두 번째 위험이다. argparse 구성을 조건 없이 항상 추가해 버리면
  일반 실행에서도 `--owner`/`summary`가 노출된다. 대응: AC1을 각 PR에서 실제로 실행해 OFF에서
  거부됨을 관측하고, 커밋 전 플래그 관련 조건문 위치를 diff에서 직접 확인한다.
- status 값이 open/done 외의 값을 갖게 되는 향후 변경이 있으면 all과 open+done 합이 달라질 수
  있음을 spec Design에 남겼다 — 지금 데이터·완료 흐름(complete는 done만 만든다)에서는 발생하지
  않는 낮은 위험이라 이번 plan에서 추가 코드를 두지 않는다.

## Proof
각 PR은 `python3 -m unittest discover -s tests -v`로 그 시점의 전체 시험을 통과해야 한다(기존
3개 + 해당 PR까지 추가된 시험).
- PR1: `test_owner.py`에 다음을 포함한다 — 플래그 미설정/무효 값에서 `list --owner hana`와
  `summary`가 각각 argparse 오류로 거부됨(AC1); 플래그 `"1"`에서 `list --owner hana`가 R-101,
  R-103만 원래 순서로 출력(AC2); 같은 상태에서 `nobody`/`HANA`/`-`가 빈 stdout·rc=0(AC3); 위 모든
  케이스에서 파일 바이트 불변. 기존 3개 시험도 변경 없이 통과해야 한다(R5 회귀 확인).
- PR2: `test_summary.py`에 다음을 포함한다 — ON에서 옵션 없는 `summary`가
  `all\t4\nopen\t3\ndone\t1\n`(AC4); `--owner hana`가 `all\t2\nopen\t1\ndone\t1\n`, `--owner min`이
  `all\t1\nopen\t1\ndone\t0\n`, `--owner nobody`가 `all\t0\nopen\t0\ndone\t0\n`(AC4); 별도 복사본에서
  `complete R-101` 후 `summary --owner hana`가 `all\t2\nopen\t0\ndone\t2\n`이고 `list --owner hana`의
  두 행이 모두 done(AC5); 모든 케이스 파일 바이트 불변(R4). `test_owner.py`를 다시 실행해 회귀가
  없는지 확인한다.
- 두 PR 모두 머지 전 최신 `main`과 합친 판에서 위 명령을 다시 실행하고, 실제 실행한 명령·판·출력을
  해당 PR 기록에 남긴다(로컬 merge만 했다면 hosted CI·운영 인도라고 쓰지 않는다 — EXPERIMENT.md는
  로컬 모의만 다룬다).
- 수동 관측(자동 시험 보완): 개발자 셸에서 `TRACKER_OWNER_INSIGHTS=1 python3 tracker.py --data
  requests.json list --owner hana`와 동일 조건의 `summary`를 직접 실행해 OFF 기본과 ON 동작의
  차이를 눈으로도 확인하고, 그 출력을 PR 설명에 붙인다.
- 정리 PR(조건부, 5단계 실행 시): `python3 -m unittest discover -s tests -v`를 플래그를 전혀
  설정하지 않은 셸에서 실행해 `list --owner`/`summary`가 이제 기본으로 통과함을 확인한다(R6).
  OFF 거부를 확인하던 옛 케이스가 삭제됐는지, 나머지 exact-match/all·open·done/read-only 시험과
  기존 list/show/complete 시험이 모두 그대로 통과하는지 diff와 실행 결과로 함께 남긴다.

이 Proof는 계획된 검사이며 실제 근거는 각 구현 PR/커밋 기록에 남긴다. 구현 중 파일·순서·PR
경계·검증이 달라지면 그 이유를 같은 구현 커밋에서 이 plan에 반영한다. 수용 기준·동작·범위가
바뀌면 spec.md를 먼저 개정하고 Upstream을 다시 고정한다.
