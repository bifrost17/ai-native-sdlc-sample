# Plan: 두 PR로 구현하고 설정으로 한 번 공개
Upstream: spec.md@23845b5. Status: draft.
Current change: 이 커밋의 spec 개정과 함께 읽는다. 공개 전 리허설·실제 공개 기록 위치를 명료화한 연구 r2 개정이다.
합성 작성 예시. 사용자 허가 범위는 설계 패키지이며 제품 계획 승인/구현 성공이 아니다.
[spec](spec.md)와 [입력](context.md)을 함께 읽는다. 모든 시험은 예정이며 이름은 추가 계획이다.

## Files that change
| PR | 경로 | 목적 |
|---|---|---|
| 1 | tracker.py, tests/test_owner.py (new), tests/test_release_control.py (new), USAGE.md | 공유 제어·목록·일반 OFF/목록 TEST ON |
| 2 | tracker.py, tests/test_summary.py (new), tests/test_release_control.py, USAGE.md | 같은 제어의 집계·전체 ON/OFF |
| cleanup (조건부) | tracker.py, tests/test_release_control.py, tests/test_owner.py, tests/test_summary.py, USAGE.md | 제어 제거와 최종 계약 시험/문서 정리 |
tests/test_tracker.py는 기존 회귀. spec.md/plan.md는 계약·실행 변경이 있을 때 관련 구현과 같이 갱신한다.

## Order of work
PR1→PR2 순차. tracker.py/USAGE.md를 공유하므로 두 구현을 병렬 branch로 동시에 편집하지 않는다.
각 PR은 최신 main에서 짧은 branch/worktree로 시작해 기능·시험·설명을 함께 담는다.

| PR | 완성할 목적·선행 | 머지 후 main과 일반/시험 상태 | 남은 범위·Proof |
|---|---|---|---|
| 1 | 담당자 목록과 공통 제어. 선행 없음 | 기존 명령 사용 가능. 일반 OFF에서 두 새 명령 거부, TEST ON에서 목록만 가능 | 집계·전체 공개 남음. P0/P1/P2 |
| 2 | 집계와 같은 제어. PR1 main에 의존 | 일반 OFF 유지, TEST ON에서 목록+집계 전체 가능 | 공개/중단 결정과 조건부 제거 남음. P0–P4 |
| cleanup | 공개/중단 관측·안정화/구버전 의존 해소·오너 정리 요청 뒤 | 설정 없이 최종 기능 제공 | 제품 범위 완료, 설정 제거 확인. P0/P1/P3/P5 |

PR1: 기준 P0 → AC1 전체 stdout·rc0를 기대하는 목록 시험을 ON 환경에서 먼저 작성·실행한다.
현재는 --owner 미지원 rc2가 예상 RED다. 최소 목록/제어 연결로 GREEN 후 OFF 거부/설정 값별 P2를 확인한다.
OFF는 기존 코드에서도 실패할 수 있으므로 그 자체를 새 기능 RED로 주장하지 않는다.
ON 성공과 OFF 거부를 함께 보여 제어가 작동하는지 판정한다. ON의 summary 부재는 PR1 시점 관측만 남긴다.

PR2: 새 tests/test_summary.py에서 all/open/done 세 줄 시험을 먼저 실행, 현재 명령 미지원 rc2 RED 확인
→ 최소 집계 → 담당자별/완료 후 사례와 읽기 전용·설정 조합 확인. 각 새 동작의 예상 실패를 확인하며
이미 GREEN인 경우에는 그대로 회귀로 보존한다. PR1의 목록·OFF 거부 시험은 유지한다.
summary가 ON에서도 없어야 한다는 PR1의 단계 한정 관측은 영구 회귀로 고정하지 않는다.

각 PR의 필요한 리팩터링 후 전체 시험, 최신 main과 결합한 판·통합 main 검증을 한다.
RED/GREEN의 명령·코드판·실패 이유·출력과 일반/시험 환경을 PR 기록에 남긴다.

공개 전 개발자 프로세스/사본에서 P4 전환 리허설과 P0–P3 전체를 확인한다.
공개 담당(root 역할)이 이 근거와 완료 범위를 확인해 실제 일반 공개 여부를 결정한다.
같은 완성 코드에서 일반 실행 환경의 TRACKER_OWNER_INSIGHTS=1로 새 프로세스를 실행해 ON,
설정을 제거해 OFF를 관측한다. 명령 예:
`env TRACKER_OWNER_INSIGHTS=1 python3 tracker.py --data <사본> summary`,
`env -u TRACKER_OWNER_INSIGHTS python3 tracker.py --data <사본> summary`.
후자는 제어가 있는 판에서 rc2. 설정 변경은 코드 PR이 아니며 결정·적용·관측 판/시각을 제품의 기존
intent/f03-owner-insights/decisions.md에 남긴다. 사본 리허설과 실제 일반 환경 관측을 구별한다.

cleanup은 조건이 충족됐다는 근거와 오너 요청이 있을 때 시작한다. 최종 무설정 동작 시험을 먼저 실행해
기존 OFF 거부가 예상 RED인지 확인한 뒤 flag 판정/조건을 제거한다. 최종 AC1–4는 유지하며 이전 OFF
거부·값별 토글 시험은 이제 폐기된 계약이라 교체/제거 이유를 spec/plan/PR에 명시한다.
코드/시험/설명 배포 확인 후 남은 환경 설정을 제거한다. 현재 예시에서 공개/cleanup은 미실행 조건이다.

## Risks
부분 TEST ON을 일반 공개로 오인하거나 PR1 summary 부재 기대를 PR2까지 유지하면 계약과 시험이 충돌한다.
단계별 표와 P2/P3로 구분한다. 개발 PC의 환경 변수가 시험에 섞이지 않게 각 subprocess에 변수를 명시 설정/제거한다.
완료 후 집계 무쓰기 비교는 complete가 끝난 새 바이트를 기준으로 한다. 원본 fixture는 바꾸지 않는다.

## Proof
기본 실행: `python3 -m unittest discover -s tests -v`. 기존 3개를 제외한 아래 시험은 모두 추가 예정이다.
| ID·연결 | 시험/관측 | 기대 |
|---|---|---|
| P0 R3 | tests/test_tracker.py + 각 명령의 기존 파일 오류 회귀 | 기존 list/show/complete·없는 ID·I/O rc2 유지 |
| P1 AC1/2 | test_owner.py의 test_owner_exact_and_order, test_owner_nonmatching | ON에서 순서/열·rc·바이트, null/-/HANA/nobody |
| P2 AC5 | test_release_control.py의 test_off_rejects_new_commands, test_setting_values | unset/0/false/공백true는 OFF; 1/true/TRUE는 ON. 기존 명령은 양쪽 정상. PR1 ON summary 부재는 단계 관측 |
| P3 AC3/4 | test_summary.py의 test_counts_and_owner, test_counts_after_complete | 네 담당자 조합·전체 세 줄, 완료 후 (2,0,2), all=open+done, 조회 무쓰기 |
| P4 AC6 | PR2 결합/통합 main 동일 판의 사본에서 OFF→ON→OFF 수동 명령 + P0–3 | 설정만으로 전환. 일반 공개는 이 리허설 뒤 별도 결정·실제 환경 관측. 일부 PR의 ON 성공만으로 전체 통과 아님 |
| P5 AC7 | cleanup 전체 시험 + 설정 없는 직접 목록/집계 | 최종 기능 유지. 없어진 OFF 계약은 제외, 제거된 제어에 의존하는 실행 대상 없음 |

검증 한계: 로컬 모의, 실제 배포/인증/장기 안정성 아님. 계약·단계가 바뀌면 영향 spec/plan과 시험을
같은 구현 커밋에서 갱신한다. 단순 시험 보강과 공개 계약의 교체를 구분한다.
