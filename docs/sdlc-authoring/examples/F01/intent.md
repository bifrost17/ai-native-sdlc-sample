# Intent: 담당자가 자기 요청만 빠르게 확인
Author: 합성 업무 오너 F01. Status: draft.

## Problem
동료들이 전체 요청 목록에서 자기 담당 건을 매번 찾아야 한다.
## Proposed outcome
CLI에서 담당자를 지정하면 해당 요청만 볼 수 있기를 바란다.
## Affected users and systems
사내 요청 CLI의 목록 사용자. JSON 저장소와 기존 조회·완료 명령.
## Constraints
기존 명령과 데이터·출력 형식을 유지하고 목록 조회가 데이터를 바꾸면 안 된다.
업무 코드 변경은 2~4파일 이내, 시험·설명은 이 상한에서 제외한다.
## Open questions
- Q1 완료 건도 포함하는가?
- Q2 대소문자와 미배정 담당자는 어떻게 비교하는가?
- Q3 일치하는 담당자가 없으면 무엇을 표시하는가?

답변과 근거는 [context](context.md)에 연결된 고정 입력을 사용한다.
