# Intent: 복사한 요청 ID로도 요청을 조회
Author: 합성 요청자 B01. Status: draft.

## Problem
`show R-202`는 성공하지만 같은 ID 양끝에 ASCII 공백이 붙으면 rc=1이다. 동료가 메시지에서
복사한 ID를 매번 손으로 고쳐야 한다. 근본 원인과 발생 시각은 원래 제보에 없다.

## Proposed outcome
메시지에서 복사한 ID의 주변 공백 때문에 조회가 실패하는 불편을 없애고 싶다.

## Affected users and systems
작은 팀의 tracker.py와 requests.json, list/show/complete 명령. Python 3.9 이상 표준
라이브러리 CLI이며 외부 서비스·계정·네트워크는 없다.

## Constraints
입력 공백을 보정하려고 저장된 ID와 데이터 행을 재작성하지 않는다. complete의 원래 상태
변경은 유지한다. 기존 시험을 수정·삭제하지 않고 새 재현/회귀 시험을 먼저 추가한다.
업무 코드는 2~4파일 이내다.

## Open questions
- Q1 어떤 주변 공백까지 허용하는지 요청자에게 확인한다.
- Q2 내부 공백·대소문자·공백뿐인 입력의 기대 결과를 요청자에게 확인한다.
- Q3 complete에도 같은 규칙이 필요한지 요청자에게 확인한다.
