# M01 작성 예시의 입력

실제 제품 코드가 없는 가상 서비스다. [고정 맥락](../../../inputs/cases.md)의 M01과
[기존 합성 입력](../../../../../../../.claude/skills/design-spec/examples/migration/context.md)을 근거로 삼았다.
입력 판은 efa7339. 아래 설계에서 새로 정한 SQLite 스키마·저장 인터페이스의 자세한 계약은
새 후보의 제안이며, 기존 코드를 관측했다는 뜻이 아니다.

가상 배치: service/api.py, service/store.py, service/json_store.py, reports/nightly.py,
tests/test_api.py, tests/test_json_store.py, tests/test_report.py, config/service.toml, docs/operations.md.
store.py의 공유 호출은 list_requests(), complete_request(id)다. api.py는 기존 인증·권한을 맡는다.
Python 3.9+ 표준 라이브러리 SQLite를 사용할 수 있고 시험 명령은
`python3 -m unittest discover -s tests -v`. 실제 서비스 관리 명령·경로·권한은 운영 담당이
운영 전환 전에 확인한다. 목록/완료에 공개 필드 추가, 새 계정, 새로운 성능 목표는 없다.
