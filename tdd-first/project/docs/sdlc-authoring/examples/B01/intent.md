# Intent: 복사한 요청 ID 주변 공백 때문에 조회·완료가 실패하는 문제 수정
Author: 합성 업무 오너 B01. Status: draft.

## Problem
메시지에서 ID를 복사하면 앞뒤 공백이나 줄바꿈 때문에 실제 요청을 찾지 못한다.
## Proposed outcome
이런 ID로도 기존 요청을 조회·완료할 수 있고 다른 ID를 잘못 처리하지 않기를 바란다.
## Affected users and systems
CLI show/complete와 JSON 저장소.
## Constraints
ID 대소문자·내부 공백·원본 데이터 형식, 오류 형식, 반복 완료의 동작을 유지한다.
## Open questions
- Q1 허용하는 주변 문자는 무엇인가?
- Q2 공백뿐이거나 없는 ID의 오류 입력도 정규화하는가?

[context](context.md)의 합성 답변을 설계 입력으로 쓴다.
