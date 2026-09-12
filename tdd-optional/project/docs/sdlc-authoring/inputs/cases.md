# 네 예시의 입력과 관측 경계

이 자료는 합성 입력을 이미 합의한 상태에서 **문서 작성·인계**를 점검한다. 질문 발견 능력 평가용
비공개 oracle은 전달하지 않는다. 원 데이터와 역사 실행은 고치지 않는다. 후보가 추가한 설계는
후보의 선택이며 역사적 승인·실행 관측으로 바꾸어 쓰지 않는다.

## F01 / B01 공통 제품 맥락

원본은 datasets/v1/baseline. 이 폴더의 baseline 두 Python 파일은 수정 없는 입력 사본이다.
제품 배치: tracker.py, tests/test_tracker.py, requests.json, README.md(기본 사용 설명이 있다는 합성 조건).
시험 명령: `python3 -m unittest discover -s tests -v`. 기존 세 시험은 목록의 순서/읽기 전용,
show의 정상/없는 ID, complete의 대상 변경/반복 바이트 보존을 확인한다. I/O 실패는 추가 확인 대상이다.
명령: `python3 tracker.py --data requests.json list|show ID|complete ID`.
출력 행은 id/status/owner-or-'-'/title을 탭으로 잇고 개행한다. 없는 ID는 rc1과 원본 입력을 포함한
`Request not found: `, 파일 오류는 rc2와 `Cannot read or update requests: ` 접두사를 쓴다.
새 테스트는 각 사례별 데이터 사본과 격리된 실행으로 작성한다. 자료는 Python 3.9+ 표준 라이브러리
기준의 합성 CLI이며 실제 회사 서비스나 성능 측정이 아니다.

F01: f01-requests.json. hana의 완료 건 포함, 원순서, 대소문자 구별 정확 일치, null은 문자열과
비일치, 없는 담당자 빈 stdout/rc0, 조회 바이트 불변. list --owner ID를 추가하며 기존 명령 유지.
업무 코드 2~4파일 이내라는 원 입력의 상한은 시험·문서에 적용하지 않는다.

B01: b01-requests.json. show/complete의 주변 ASCII space/tab/CR/LF만 허용. 내부 공백·대소문자·
U+00A0은 그대로 구별. 빈 값·허용 공백뿐·없는 ID는 기존 오류, 저장 ID는 보정하지 않는다.
complete의 정상 status 변경/반복 무쓰기, 실패·조회 바이트 불변을 유지한다.

## F03 — 두 PR, 한 공개 단위

f01-requests.json과 같은 네 행을 사용한다. 제품 사용 문서는 USAGE.md다. F02의 open/done 두 줄
계약과 다르게 F03은 all/open/done 세 줄이다. 두 기능이 완성되기 전 일반 OFF, 완성된 부분만
개발자 프로세스 TEST ON. 설정은 로컬 프로세스 환경 변수이며 사용자 인증 장벽이 아니다.
상세 계약은 f03-spec-historical.md@f1ba82e, 실행 예시는 f03-plan-historical.md@5fc8bdc다.
선택형 교육 사본은 이 역사에서 출발해 작업별 검증 방식과 실제 양식을 보강하되 원 계약의 phase 조건을 보존한다.
현행 F03은 이 공개 제어 사례에 TDD를 선택하며 모든 기능의 고정 순서로 일반화하지 않는다.
공개/중단과 정리 요청·모의 안정화는 후보에서 아직 수행되지 않은 조건이다.

## M01 — 가상 서비스의 이행

근거는 .claude/skills/design-spec/examples/migration/{intent,context,spec}.md와
.claude/skills/plan/examples/{context,migration}.md (기준 efa7339). 실제 코드가 없는 가상 배치다.
단일 호스트 Python 서비스, 기존 웹/API·권한·저장 어댑터, JSON을 SQLite로 바꾸고 야간 보고서는
기존 GET /requests를 사용한다. 별도 서비스·계정·무중단 요구·성능 개선 수치는 없다.
GET은 200 {requests:[...]}, 완료는 200 행 객체, 미인증401/권한403/없는ID404/일시저장오류503.
503은 {error:temporarily_unavailable}. 담당자 본인·운영자만 완료, 거부된 쓰기는 불변이다.
필드 id/title 문자열·owner 문자열/null·status open/done·원래 순서를 보존한다. JSON schema_version=1.
이행은 중지 중 원본 보존/전체 유효성/중복·알 수 없는 필드·버전 거부/원자적 import 후 대조.
경합 대기는 기존 5초 상한. 서로 다른 요청의 겹친 완료 보존과 반복 완료의 멱등성이 요구다.
전환 후 쓰기 또는 여부 불명은 최신 DB를 일관된 JSON으로 내보내 보존한다. 구 JSON writer의
동시 쓰기 결함이 남으면 그 경로로 서비스를 재개하지 않는다. 복구는 안전한 최신 SQLite 경로가 기본이다.
직접 소비자는 보고서 한 개, 다른 writer 없음이라는 합성 후속 결정이 제공됐다.
운영 호스트의 중지/재개 명령은 미확인이다. 실제 전환 전에 운영자가 채워야 할 조건이며 코드 인계를
막는 미정과 구별한다. 후보의 데이터 스키마·공유 인터페이스·오류 전달은 spec에서 구체화한다.

예시 Upstream은 제작 입력을 가리키는 것으로 표기한다. 예시를 사용 제품에 복사할 때는 해당 제품의
실제 경로·수락 판·정책·검증 환경으로 바꾼다. 예정 테스트의 이름은 실행 성공의 증거가 아니다.
