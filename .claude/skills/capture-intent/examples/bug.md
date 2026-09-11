# Intent: 복사한 요청 ID로도 요청을 조회
Author: 실험 요청자 (합성 사례 B01). Status: draft.

## Problem
동료가 메시지에서 복사한 요청 ID로 조회하면 분명히 있는 요청인데 없다고 나온다. 앞뒤 공백이
없는 ID를 다시 입력하면 된다. 복사해 붙여 넣는 일상 사용에서 수동으로 입력을 고쳐야 한다.
확인된 예는 `python3 tracker.py --data requests.json show R-202`다. 이 입력은 성공하지만
같은 ID 양끝에 ASCII 공백이 있으면 rc=1이다. 근본 원인과 발생 시각·SHA는 입력에 없다.

## Proposed outcome
주변 공백이 붙은 ID를 복사해도 해당 요청을 조회하고 싶다. ID를 매번 손으로 고쳐 입력하지 않아도 된다.

## Affected users and systems
요청 ID를 복사해 사용하는 동료, tracker.py와 requests.json. 현재 list/show/complete 명령이 있다.

## Constraints
- 저장된 ID와 데이터 행은 재작성하지 않는다. 저장 ID는 대문자 R-와 숫자 세 자리다.
- 기존 시험은 수정·삭제하지 않고 재현/회귀 시험을 먼저 추가한다.
- Python 3.9 이상 표준 라이브러리를 사용하며 외부 서비스·계정·네트워크는 없다.
- 업무 코드는 2~4파일 이내로 유지한다.

## Open questions
- ASCII 공백 외의 탭·줄바꿈도 실제 복사에 포함되는지 요청자에게 확인한다.
- complete에도 같은 입력 처리가 필요한지 요청자에게 확인한다.
- ID 내부 공백·대소문자·공백만 있는 입력의 기대 결과는 요청자에게 확인한다.
