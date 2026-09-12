# M01 작성 예시의 입력

> 활성 교육 사본. 원본 경로: `docs/research/sdlc-documentation/spec-plan-design/candidate/examples/M01/`; source commit: `2d3f2dc`.
> 문서의 `Upstream` SHA는 제작 당시 원본 배치를 가리키며, 이 이동 경로나 제품 수락을 뜻하지 않는다.

실제 제품 코드가 없는 가상 서비스다. 보존할 API·데이터·권한·운영 조건과 확정된 후속 결정은
[현재 입력 계약](inputs/current-contract.md)에 모았다. 구현/리뷰는 그 문서를 직접 읽으며 과거 문서를 거칠 필요가 없다.
SQLite 스키마·저장 인터페이스의 자세한 계약은 spec과 design/ 정본의 제안이며 기존 코드를 관측했다는 뜻이 아니다.

제공된 합성 배치: service/api.py, service/store.py, service/json_store.py, reports/nightly.py,
tests/test_api.py, tests/test_json_store.py, tests/test_report.py, config/service.toml, docs/operations.md.
store.py의 공유 호출은 list_requests(), complete_request(id)다. api.py는 기존 인증·권한을 맡는다.
Python 3.9+ 표준 라이브러리 SQLite를 사용할 수 있고 시험 명령은
`python3 -m unittest discover -s tests -v`. 실제 서비스 관리 명령·경로·권한은 운영 담당이
운영 전환 전에 확인한다. 목록/완료에 공개 필드 추가, 새 계정, 새로운 성능 목표는 없다.

이 경로와 명령은 이 저장소에서 존재·실행을 확인한 제품 파일이 아니라 제공된 합성 가정이다.
plan의 신규 파일과 선행 시험 이름도 작성 제안이다. 실제 제품에 적용할 때 확인된 경로·명령·기존 계약 시험으로
구체화하며, 오류 본문처럼 주어지지 않은 값은 현재 입력 계약의 한계를 따른다.

출처: [고정 맥락](../../inputs/cases.md)의 M01과
제작 당시 경로 `.claude/skills/design-spec/examples/migration/context.md`의 기존 합성 입력(source commit `efa7339`).
이는 제작 이력이며 필수 계약은 current-contract.md의 고정 발췌에 있다. intent.md의 질문·작성 이력은 보존했다.
