# Plan: 보고서 호환 후 검증한 SQLite로 전환
Upstream: spec.md@efc65d9. Status: draft.
합성 예시: [spec](../../design-spec/examples/migration/spec.md)·그 context와
[추가 실행 맥락](context.md)의 M01을 읽는다. 실제 저장소 탐색·승인·운영 시험 결과가 아니다.

## Files that change
- PR-A: reports/nightly.py, tests/test_report.py — 기존 GET /requests로 보고서를 읽고 실패를 알림.
- PR-B: service/sqlite_store.py (new), tools/migrate_store.py (new),
  tests/test_sqlite_store.py (new), tests/test_migrate_store.py (new) — 비활성 저장소·이행/내보내기 도구.
- PR-C: service/store.py, config/service.toml, tests/test_api.py, tests/test_report.py,
  tests/test_cutover.py (new), docs/operations.md — 저장소 선택 연결·통합 검증·실제 운영 절차.
service/api.py·json_store.py는 읽을 기준이며 현재 변경할 계획은 없다. 필요해지면 이유와 plan을 갱신한다.

## Order of work
검증 방식: **혼합**. 보고서의 명확한 API 연결은 동작별 구현 후 테스트, 기존 API/JSON은 기존 테스트 활용,
데이터 무결성이 중요한 PR-B와 선택 경계 PR-C는 TDD를 선택한다. 기대는 spec/보존 원본 데이터에서 정한다.
공유 설계는 spec의 R1–R5, 실행 인터페이스는 context.md의 service/store.py다. 먼저 엔지니어가
이 판과 기존 계약 시험을 확인한다. A/B는 같은 최신 main에서 각각 branch/worktree를 만들 수 있다.

### PR-A — 보고서 입력 호환
보고서 담당은 기존 읽기 계정·응답 계약으로 API를 사용하고 옛 JSON fallback을 제거한다.
test_report.py에서 같은 입력의 보고서 결과와 API 오류 노출을 확인한다. 기존 JSON 저장소 상태에서
먼저 독립 검토·머지할 수 있다. 이 main은 기존 API/저장소와 새 보고서가 동작하며 저장소 전환은 아직 없다.

### PR-B — 비활성 저장소와 이행·복구 도구
저장소 담당은 파일별로 따로 PR을 만들지 않고 어댑터·이행·복구와 각 시험을 함께 제공한다.
각 동작은 아래 독립 기대를 시험에 먼저 고정하고 미구현 동작의 의미 있는 실패를 관측한 뒤 연결한다.
1. 기존 인터페이스에 맞는 목록·트랜잭션 완료·오류 정리를 구현한다. 서로 다른 연결의 완료를
   겹쳐 실행해 두 결과 보존, 같은 완료 재시도, 경합 상한과 I/O 오류를 확인한다(AC1/5).
2. `python3 tools/migrate_store.py import --source 원본.json --target 새.db`와
   `export --source 현재.db --target 새복구.json` 인터페이스를 구현·시험한다(추가 예정).
   원본·기존 출력은 덮어쓰지 않고 전체 입력 검증·단일 트랜잭션·값/순서 대조 후만 성공한다.
3. 실패·중단·재시도, 새 완료 뒤 내보내기와 사본 호환을 확인한다(AC3/4). 이 PR 뒤 main은
   여전히 JSON을 사용한다. SQLite는 자동 활성화하지 않으며 운영 전환을 성공으로 표시하지 않는다.

A와 B는 공유 파일을 수정하지 않고 확정한 API/저장 계약을 읽는다. A가 먼저 인도될 수 있으며 B는
A 코드에 의존하지 않는다. 계약 변경이 필요하면 독립성 판단을 다시 하고 관련 spec 결정을 먼저 맞춘다.
엔지니어가 통합과 공유 plan 조정을 맡는다. 병렬 담당은 이 계획이 달라지면 변경·이유를 알려
자기 관련 구현 커밋에 조정된 plan을 함께 담는다. 공유 plan 편집/커밋은 순차 조정하며 한 branch의
계획을 다른 branch의 최신 계획 위에 덮어쓰지 않는다. 통합 담당이 마지막에 몰아서 갱신하지 않는다.

### PR-C — 연결과 전환 준비
명시 SQLite 선택과 누락 DB 시작 거부의 시험을 먼저 작성해, 아직 JSON만 사용하는 facade가 새 기대를
만족하지 못하는 실패를 확인한 뒤 선택 경계를 연결한다. 이미 만족하는 API 회귀에 실패를 꾸미지 않는다.
A/B가 main에 통합된 뒤 최신 main에서 시작한다. 저장소 선택을 연결하되 실제 운영 설정 전환은
아래 리허설을 통과한 뒤 운영 담당이 한다. tests/test_cutover.py와 API·보고서 시험으로 AC1–6을
같은 저장소에서 확인한다. main은 JSON 기본을 유지하면서 검증된 SQLite 경로를 선택할 수 있다.
개발 파일의 머지는 데이터 이행·운영 전환 자체가 아니다. 테스트 이름만 있고 환경 검증이 없으면 전환하지 않는다.

운영 담당과 실제 서비스 관리 명령을 docs/operations.md에 확인해 기록한다. 서비스·보고서를
중지하고 writer가 없는지 확인 → 원본 보존 → 새 DB import와 값/순서 비교 → 선택 설정 전환 →
API·보고서·권한·완료/재조회 리허설 → AC1을 만족하는 쓰기 경로 확인 후 재개 순서다.
리허설은 사본에서 수행한다. 운영 데이터 경로·권한·중지/재개 명령의 확인이 남으면 운영 단계는 미실행으로 남긴다.

## Risks
가장 위험한 부분은 PR-C 이후의 운영 전환·복구다. Git revert만으로 처리 데이터를 되돌리지 않는다.
쓰기 이후 또는 여부 미확인에는 중지 상태에서 현재 DB를 새 JSON으로 내보내고 전체 값·순서를
비교한다. 구버전 조회/완료 호환은 사본에서만 시험하고 원래 복구 파일은 보존한다. 기본 복구는
최신 데이터를 가진 SQLite 경로를 복구하는 것이다. R1 미충족인 구 JSON writer를 재개하지 않는다.
내보내기·검증·안전한 쓰기 경로 중 하나라도 실패하면 중지하고 DB·원본·복구 데이터를 보존한다.
쓰기 전임이 확실할 때만 원본을 복구 입력으로 쓸 수 있다. DB/journal을 임의 복사·삭제하지 않는다.

## Proof
`python3 -m unittest discover -s tests -v`를 각 PR과 최신 main 통합 결과에서 실행한다.
- A: test_report.py의 API 응답 기반 집계·오류 노출(추가), 기존 API·JSON 시험 유지(AC2/6).
- B: test_sqlite_store.py의 두 연결 동시 완료·재시도·순서·경합/오류(추가, AC1/2/5),
  test_migrate_store.py의 유효 전량·중복 ID·필드/상태/버전 오류·중단 재시도·새 완료 후 export·
  기존 출력 거부·원본 바이트 보존(추가, AC3/4). 동시 시험은 호출이 실제 겹쳤는지도 확인한다.
- C: test_cutover.py의 JSON→SQLite 목록 대조·완료 뒤 보고서·중단/복구 실패 시 재개 금지,
  tests/test_api.py의 200/401/403/404/503 및 거부된 쓰기 보존(AC1–6). A/B의 시험도 모두 실행한다.
  통합 담당과 운영 담당은 사본 리허설의 중지 확인·실제 명령·행/값/순서 비교·새 완료 보존·재개 판단을
  기록한다. 이 계획에서 실행 결과나 구체 호스트 명령을 발명하지 않는다.
