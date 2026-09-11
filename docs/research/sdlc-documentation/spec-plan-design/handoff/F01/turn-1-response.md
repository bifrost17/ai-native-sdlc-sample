# F01 문서 인계 점검 결과

## 판단: 대화 없이 구현 착수 가능
spec/plan/context/baseline이 서로 정합적이고, R1–R3·AC1–4·파일 목록·TDD 순서가 구체적으로 연결돼 있어 추가 질문 없이 착수할 수 있는 수준입니다. 다만 실행 시 확인해야 할 사소한 공백은 아래에 명시합니다.

## 작업 순서 (plan.md 기준, 예정)
1. main 기준 branch/worktree 생성, 기존 3개 시험(`test_tracker.py`)으로 베이스라인 확인.
2. `tests/test_owner.py`에 `test_owner_exact_and_order` 먼저 작성·실행 → 현재 `--owner` 미지원이므로 argparse rc2로 RED 확인(환경/fixture 오류와 구분).
3. `tracker.py`의 `list`에만 최소 변경(옵션 파싱 + owner 정확 비교)해 GREEN.
4. `test_owner_nonmatching`(nobody/HANA/- 각각 빈 stdout·rc0), `test_owner_no_option_and_io_error`(무옵션 회귀 + 없는 데이터파일 rc2/접두사) 추가.
5. 기존 3개 시험 재확인 → 필요 시 리팩터링 → README.md에 `--owner` 사용법·완료 포함·빈 결과 설명 갱신.
6. 최신 main과 합친 후 전체 시험 재실행(P1–P3), 명령/결과/미확인 범위를 PR에 기록.

## 변경 파일
- `tracker.py` (list에 `--owner` 옵션, R1)
- `tests/test_owner.py` (신규)
- `README.md` (사용법 갱신)
- `tests/test_tracker.py`는 수정 없이 회귀 기준으로 사용.

## 검증 명령 (예정, 미실행)
- `python3 -m unittest discover -s tests -v` (전체)
- `python3 -m unittest discover -s tests -p test_owner.py -v` (신규만)
- 각 테스트는 requests.json을 임시 사본에 복사해 격리 실행, 바이트 불변 비교 포함.

## PR/통합 후 동작
`--owner` 옵션은 병합 즉시 사용 가능(별도 feature flag/공개 제어 없음). 기존 `list`(옵션 없음)·`show`·`complete` 동작·출력 형식은 변경 없음. 남은 공개 범위 없음(spec.md 명시).

## 남은 미정/누락 (문서에서 확정되지 않음)
- **PR 대상 브랜치/저장소, 실제 승인자·머지 권한**: plan에 "최신 main"이라고만 있고 실제 PR 프로세스(리뷰어 지정 등)는 없음 — 이 예시가 합성 문서 작성 연습이라 명시(context.md line 3)되어 있어 실제 제품 승인 절차가 아님.
- **내부 보조 함수 분리 여부**: spec.md가 "구현 중 결정"으로 명시적으로 위임 — 이는 누락이 아니라 의도적 미정.
- **-owner 값이 빈 문자열이거나 옵션에 인자가 없을 때(`--owner` 뒤 값 누락)의 처리**: argparse 기본 동작에 맡기는 것으로 보이나 spec/plan 어디에도 명시적 AC 없음.

## 예정 검증 vs 관측 사실 구분
문서 내 모든 RED/GREEN, rc 값, stdout 결과는 **예정(plan.md 명시: "실제 RED/GREEN은 실행/PR에 남긴다")**이며, 이번 점검에서 실제로 실행·관측된 것은 없습니다. baseline 코드 3개 파일과 f01-requests.json 데이터 내용만 실제로 읽어 확인된 사실입니다.
