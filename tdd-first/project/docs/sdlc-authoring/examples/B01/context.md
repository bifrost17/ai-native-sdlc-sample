# B01 작성 예시의 입력

> 활성 교육 사본. 원본 경로: `docs/research/sdlc-documentation/spec-plan-design/candidate/examples/B01/`; source commit: `2d3f2dc`.
> 문서의 `Upstream` SHA는 제작 당시 원본 배치를 가리키며, 이 이동 경로나 제품 수락을 뜻하지 않는다.

합성 draft, 제품 승인·수정 실행 결과가 아니다.
[고정 맥락](../../inputs/cases.md)의 B01, [데이터](../../inputs/b01-requests.json),
[코드](../../inputs/baseline/tracker.py), [기존 시험](../../inputs/baseline/test_tracker.py)을 읽는다.
제품 배치 tracker.py, tests/test_tracker.py, requests.json, README.md. Python 3.9+ 표준 라이브러리.
확정 답: 주변 ASCII space/tab/CR/LF만 비교 입력에서 제거. 저장 ID·원본 오류 입력은 보존.
재현 시험을 추가·실행·커밋한 뒤 수정한다. 보호된 fix 단계에서 시험을 고치지 않는다.
