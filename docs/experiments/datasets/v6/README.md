# F04-release-json 데이터셋 6.0.0

이 판은 담당자별 조회와 상태 요약을 하나의 공개 단위로 개발하고, 두 번째 기능의 최초 구현 뒤 JSON
출력 요구를 추가하는 전체 실행용 합성 사례다. seed 102의 네 행을 재사용하므로 F02와 독립적인 성공률
표본으로 세지 않는다.

AGENT 제품 seed에는 아래 자료만 전달한다.

| 원본 | 제품 위치 | 용도 |
|---|---|---|
| `../v1/baseline/tracker.py` | `tracker.py` | 기존 CLI 구현, 변경 없이 재사용 |
| `../v1/baseline/test_tracker.py` | `tests/test_tracker.py` | 기존 회귀 시험, 변경 없이 재사용 |
| `F04-release-json/requests.json` | `requests.json` | 합성 입력 |
| `F04-release-json/public.json` | `case.json` | 공개 문제 카드 |

`F04-release-json/human.json`은 HUMAN 전용이다. 제품 seed나 AGENT checkout에 복사하지 않는다.
HUMAN은 실제 질문과 제출된 문서를 보고 관련 결정을 자연스럽게 공개하며, 고정 질문·답변 대본으로
운영하지 않는다. F04-D7은 PR2의 상태 요약 최초 코드와 시험 결과를 실제로 관측한 뒤 처음 공개한다.

입력 출처는 `../v1/manifest.json`의 baseline 경로·해시와 `../v2/manifest.json`의 F02 fixture
경로·해시다. 이 판의 `requests.json`은 `../v2/F02/requests.json`과 같은 바이트다. 파일별 고정값은
`manifest.sha256`과 `manifest.json`에 기록한다.

사용 템플릿은 `codex/use-template-0024@fbc23c04348bf9009f461c396ac23df1b3139f48`로
고정했으며 tree에는 71개 파일이 있다. 실행 시작 시 같은 SHA와 파일 목록인지 확인하고 기록한다.
