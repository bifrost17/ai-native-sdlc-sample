# F01 작성 예시의 입력

합성 문서 설계 예시다. 사용자에게 허가받은 설계 패키지 작성이며 제품 승인·구현·검증 성공이 아니다.
[고정 맥락](../../../inputs/cases.md)의 F01과 [데이터](../../../inputs/f01-requests.json),
[기준 코드](../../../inputs/baseline/tracker.py), [기준 시험](../../../inputs/baseline/test_tracker.py)을 읽는다.
제품 배치는 tracker.py, tests/test_tracker.py, requests.json, README.md다. 새 시험은 tests/에 둔다.
Python 3.9+ 표준 라이브러리, 명령은 `python3 -m unittest discover -s tests -v`.
담당자 규칙·완료 포함·빈 결과는 이 예시에 주어진 합의다. 질문 발견 능력 평가 데이터가 아니다.
