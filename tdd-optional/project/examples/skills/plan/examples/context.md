# 실행 예시의 입력 경계

root가 작성한 합성 계획들이다. 실행 결과나 사람의 실제 수락을 뜻하지 않는다. Upstream의 판은
제작 저장소에서 입력을 보존한 commit이며 채택 프로젝트의 승인 SHA로 재사용하지 않는다.
실제 작성에서는 해당 프로젝트의 수락된 spec과 현재 코드를 읽는다. 예시의 시험명 중 추가 예정은
아직 존재하지 않는다. 여기 적힌 파일·명령·제약은 모든 프로젝트의 기본 규칙이 아니다.

## F01, B01, F02의 코드 맥락

제작 저장소 docs/experiments/datasets/v1/baseline/tracker.py와 test_tracker.py를 읽었다. 제품 배치에서는
tracker.py, tests/test_tracker.py, requests.json이다. argparse의 list/show/complete를 사용한다.
list는 JSON requests의 순서대로 display를 호출한다. show/complete는 같은 ID 조회를 공유하며
complete만 대상 상태를 바꾸고 이미 done이면 쓰지 않는다. 기본 시험 명령은
`python3 -m unittest discover -s tests -v`다. 기존 ExistingTrackerTests의 세 시험은
list 순서·읽기 전용, show 기존/없는 ID, complete 대상 상태 변경·반복 바이트 보존을 확인한다.
I/O 실패와 새 옵션은 아직 시험하지 않는다. 새 시험은 매번 별도 데이터 복사본에서 실행한다.

F01과 B01의 계약은 각각 ../../design-spec/examples/feature/와 bug/의 spec.md·context.md다.
F02는 아래 two-pr-spec.md가 계약이며 F01과 같은 네 행을 쓴다. 예시 Upstream의 spec.md는 이
링크된 계약의 역할을 나타낸다. 실제 계획은 제품의 실제 spec.md 경로와 수락 SHA를 사용한다.
이 예시에는 제품 README.md가
있고 기본 명령만 설명한다고 가정한다. baseline 소스에는 README가 없으므로 추가한 합성 조건이다.

## M01의 합성 실행 맥락

../../design-spec/examples/migration/{spec,context}.md의 가상 서비스에 다음 실행 배치를
추가한 **설계 예시**다. 실제 저장소를 읽고 확인한 경로·명령이 아니다. 실제 도입 때 먼저 확인한다.

- 기존 파일: service/api.py(인증·응답), service/store.py(저장소 선택과 인터페이스),
  service/json_store.py, reports/nightly.py(JSON 직접 읽기), tests/test_api.py,
  tests/test_json_store.py, tests/test_report.py, config/service.toml, docs/operations.md.
- 기존 API 시험은 정상·401·403·404·503 계약을 검사한다. 저장소 시험은 목록 순서와 반복 완료,
  보고서 시험은 목록 기반 집계를 검사한다. `python3 -m unittest discover -s tests -v`로 실행한다.
- 공유 인터페이스는 service/store.py의 list_requests()와 complete_request(id)다. 리스트 순서,
  완료 행·없는 ID·저장 오류의 전달 의미는 migration/spec.md의 R1/R2 및 context.md와 같다.
  함수 시그니처는 이 합성 입력에서 제공한 사실이며 실제 새 계약 합의를 대신하지 않는다.
- 운영 담당이 기존 서비스 관리 도구로 API와 야간 작업을 중지하고 실제 PID·스케줄 비활성 상태를
  확인한다. 재개도 그 도구를 쓴다. 호스트 명령을 발명하지 않고 docs/operations.md에 실제 명령을
  확인해 넣는 것은 전환 리허설 전 조건이다. 미확인 상태에서 실제 전환을 수행하지 않는다.
- 새 도구의 인터페이스는 계획 제안이다. import/export 명령은 입력과 별도 출력 경로를 받고
  출력이 이미 있으면 거부한다. 경로·전체 값·순서 대조와 rc=0을 전환 판단에 사용한다.

이 맥락은 F02 대화 실험에 제공할 정답 대본이 아니다. F02 실험은 별도 수락된 문서·현재 코드를
입력으로 사용하며 질문 능력 측정과 계획 실행 측정을 구별한다.
