# 비교한 두 형태

## A — 다섯 핵심 구획 안에서 필요한 상세를 추가

Problem, Proposed outcome, Affected users and systems, Constraints, Open questions.
최종 후보는 [사용 양식](../../../../templates/intent.md)이다. 이유·근거는 Problem에서, 제안은
Proposed outcome에서, 확정 조건과 제외 범위는 Constraints에서 표현한다.

## B — 이유·근거·해결 제안을 분리

같은 입력을 아래처럼 분리하는 대안을 검토했다. 이 안은 채택한 양식이나 별도 설치 대상이 아니다.

```markdown
# Intent: ‹원하는 변화›
Author: ‹작성자 또는 출처›. Status: draft.
## Problem or opportunity
‹현재 상황›
## Why it matters
‹왜 바꿀 가치가 있는지›
## Evidence
‹알려진 사례나 근거›
## Desired outcome
‹누구에게 무엇이 나아지는지›
## Suggested approach
‹요청자의 제안, 확정 여부›
## Affected users and systems
‹영향받는 대상›
## Constraints and non-goals
‹확정 조건과 범위 밖›
## Open questions
‹질문과 답변 담당›
```

## 선택 판단

세 [대표 입력](examples-inputs.md)에 대해 A의 완성 예시를 root가 작성하고 B의 정보 배치와
대조했다. 실제 agent를 두 양식에 무작위 배정한 실험은 아니다.

| 사례 | A에서 읽히는 내용 | B를 기본으로 둘 때 추가되는 부담 |
|---|---|---|
| F01 기능 | 혼합 목록의 불편, 담당자 조회 기대, 유지할 계약, 미정 질문 | 이유가 Problem과 짧게 겹치며 별도 근거·제안이 없는 빈 절이 생김 |
| B01 버그 | 관측과 재현, 기대 결과, 보존 조건, 미정 입력 범위 | Problem·Evidence·Why 사이에서 같은 실패를 나눠 설명해야 함 |
| I03 정보 부족 | 제보·원인 추정·Redis 제안의 성격, 미확인 시스템과 담당 | 개별 절이 있다고 없는 수치·원인·담당자를 채울 수는 없음 |

현재 예시에서는 A로 중요한 정보를 구별할 수 있어 A를 선택했다. 많은 근거나 제안 비교가
실제 필요하면 A의 해당 절 아래 목록·하위 절을 추가할 수 있다. 반복 문구와 빈 구획을 줄이는
판단이며, 원본의 다섯 절이 모든 조직에 유일한 정답이라는 주장은 아니다.

기존 emitter가 다섯 절의 위치를 사용하는 점도 확인했다. 의미에 맞는 A가 우선이고 기존 소비자
호환성은 추가 이점이다. 그 소비자를 보존하기 위해 필요한 정보를 제거하지 않았다.
