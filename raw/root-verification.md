# HUMAN의 독립 관측 요약

실행 명령: `python3 /Users/jake/Projects/ai-native-sdlc-experiments/human-f02-plan-sync/verify_product.py`.
종료코드 0. 제품 코드의 마지막 수정은 턴2이며 이후에는 spec/plan만 수정했다.
이 파일은 실행 출력의 관측 요약이며 stdout 원본 전체는 아니다.

| 관측 | 실제 결과 |
|---|---|
| 목록 전체 | R-101, R-102, R-103, R-104 |
| 담당자 hana 목록 | R-101, R-103 |
| 기본 요약 전체 / hana / nobody | 각각 open·done = 3·1 / 1·1 / 0·0, 탭 두 줄 |
| JSON 요약 전체 / hana / nobody | 각각 open·done = 3·1 / 1·1 / 0·0, JSON 정수 |
| JSON HANA / 문자열 null 담당자 | 각각 0·0 |
| 임시 복사본 complete R-101 후 JSON / 기본 요약 | 각각 hana 0·2 |

12개 관측이 모두 기대와 일치했다. 조회 후 원본 requests.json의 바이트는 같았다.
baseline d22a9fe의 기존 시험 5개와 setUp/invoke 함수의 AST는 현재 파일에서 모두 그대로였다.
제품 책임자/HUMAN의 요구 변경·리뷰와 spec 수락은 공개 turn-02~05.human.md에 있다.

초기 turn2는 spec/plan 갱신을 누락했다. turn3에서 문서를 고쳤지만 같은 커밋을 '계열'로 느슨하게
표현하고 구 spec SHA에 개정 설명을 덧붙였다. turn4에서 수락 전 문서 정합성을 정정했고,
turn5는 실제 커밋된 spec SHA를 plan Upstream으로 이어받았다. 이것을 첫 시도 성공으로 계산하지 않는다.
