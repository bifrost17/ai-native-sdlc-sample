# F03 작성 예시의 입력

> 활성 교육 사본. 원본 경로: `docs/research/sdlc-documentation/spec-plan-design/candidate/examples/F03/`; source commit: `2d3f2dc`.
> 문서의 `Upstream` SHA는 제작 당시 원본 배치를 가리키며, 이 이동 경로나 제품 수락을 뜻하지 않는다.

합성 draft. 과거 실험의 성공을 이 후보의 승인·실행 증거로 쓰지 않는다.
[고정 맥락](../../inputs/cases.md)의 F03, [데이터](../../inputs/f01-requests.json),
[기준 코드](../../inputs/baseline/tracker.py), [기준 시험](../../inputs/baseline/test_tracker.py)을 읽는다.
인계 정본은 이 폴더의 [현재 spec](spec.md)과 [현재 plan](plan.md)이다.
역사 spec `docs/research/sdlc-documentation/spec-plan-design/inputs/f03-spec-historical.md`(source commit `f1ba82e`)과
역사 plan `docs/research/sdlc-documentation/spec-plan-design/inputs/f03-plan-historical.md`(source commit `5fc8bdc`)은
선택적 출처 추적 자료이며 이 활성 패키지에 복제하지 않았다. 통상 인계의 필수 읽기가 아니다. 과거 R/AC/단계 번호와 현재 계약을 섞지 않는다.
제품 배치는 tracker.py, tests/test_tracker.py, requests.json, USAGE.md다. Python 3.9+ 표준 라이브러리.
목록+집계가 한 공개 단위라는 합성 오너 결정이 있다. 제어는 로컬 프로세스 환경 변수다.
