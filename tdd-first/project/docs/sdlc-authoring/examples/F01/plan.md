# Plan: 담당자 필터를 한 PR로 제공
Upstream: spec.md@23845b5. Status: draft.
합성 작성 예시. 사용자 허가 범위는 설계 패키지이며 제품 계획 승인/구현 성공이 아니다.
[spec](spec.md)와 [입력](context.md)을 함께 읽는다. 모든 시험은 예정이며 이름은 추가 계획이다.

## Files that change
| 경로 | 변경 | 연결 |
|---|---|---|
| tracker.py | list 옵션·필터 | R1 |
| tests/test_owner.py (new) | 정확 비교·순서·미배정·기존/I/O 회귀 시험 | AC1–4 |
| README.md | 옵션 사용법·완료 포함·빈 결과 | R1/R3 |
기존 tests/test_tracker.py는 수정 없이 기준/회귀로 사용한다.

## Order of work
한 PR: 기능·시험·설명을 묶는다. 최신 main에서 branch/worktree를 만들고 기존 세 시험으로 기준을 확인한다.
1. tests/test_owner.py에 test_owner_exact_and_order를 먼저 작성·실행한다.
   hana 두 행/기존 열·rc0·바이트 보존을 기대하고 현재 미지원 옵션의 argparse rc2로 실패하는지 확인한다.
   import/fixture 오류는 동작 RED가 아니므로 먼저 시험 환경을 고친다.
2. tracker.py의 list에만 최소 연결해 그 시험을 통과시킨다. AC2의 no-match/null 구별을 다음 시험으로
   확인한다. 이미 GREEN이면 구현을 일부러 망가뜨리지 않고 회귀로 보존한다. 필요한 새 동작은 같은 test-first 순서로 진행한다.
3. AC3/4와 기존 시험을 확인하고 필요한 리팩터링 뒤 재실행, 사용 설명을 갱신한다.
4. 최신 main과 합친 판에서 Proof 전체를 실행하고 명령/판/출력·미확인 범위를 PR에 남긴다.
   검토 후 통합된 main에서도 같은 검증을 확인한다. 머지 뒤 이 기능은 바로 사용 가능, 남은 공개 범위 없음.

공통 절차는 프로젝트의 [TDD 정책](../../../../CLAUDE.md#conventions)과 설치된 관련 개발 스킬. 시험·구현을 PR로 나누거나 모든 RGR마다 커밋하지 않는다.

## Risks
공유 검색/출력 수정이 show/complete를 깨뜨릴 수 있다. 변경을 list에 한정하고 P2로 발견한다.
fixture를 다른 시험이 수정하면 읽기 전용 판정이 흐려지므로 각 실행에 새 임시 사본을 쓴다.

## Proof
| ID·연결 | 기존/추가·실행 위치 | 명령·기대 |
|---|---|---|
| P1 AC1/2 | 추가 tests/test_owner.py: test_owner_exact_and_order, test_owner_nonmatching | python3 -m unittest discover -s tests -p test_owner.py -v; 전체 stdout/rc/바이트 비교 |
| P2 AC3/4 | 기존 tests/test_tracker.py의 세 시험 + 추가 test_owner_no_option_and_io_error | python3 -m unittest discover -s tests -v; 기존 정상/없는 ID/완료·반복, 무옵션·없는 파일의 rc2·접두사·파일 비생성 |
| P3 통합 | P1/P2와 README 예시 | 최신 main과 합친 결과 및 통합 main에서 전체 GREEN·문서 계약 일치 |

실제 RED/GREEN은 실행/PR에 남긴다. 경로·순서·검증 변경은 관련 구현 커밋에서 plan을 갱신한다.
정확 일치 등 계약이 바뀌면 spec/AC도 함께 고친다. 순수 회귀 추가가 계약/계획을 바꾸지 않으면 문서를 억지로 수정하지 않는다.
