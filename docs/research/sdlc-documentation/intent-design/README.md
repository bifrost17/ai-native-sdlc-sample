# 우리 intent 양식 설계

상태: Astra·Fable의 같은 최종 후보 독립 리뷰 통과. 작성자: Codex root. 2026-09-11.
[리뷰 결과와 검사 범위](review-record.md)에 지적·수정·근거를 보존했다.

플레이북의 목적은 요청자의 말로 무엇을 왜 원하는지와 제약을 포착하고, 사람과 에이전트가 같은
기록으로 다음 단계에 진입하게 하는 것이다. 이를 기준으로 [입력](examples-inputs.md)에서
완성 예시를 먼저 작성하고 [두 형태](alternatives.md)를 비교했다.

## 결과 파일

- [intent 양식](../../../../templates/intent.md)
- [capture-intent 작성 스킬](../../../../.claude/skills/capture-intent/SKILL.md)
- 완성 예시: [기능](../../../../.claude/skills/capture-intent/examples/feature.md),
  [버그](../../../../.claude/skills/capture-intent/examples/bug.md),
  [불완전한 요청](../../../../.claude/skills/capture-intent/examples/incomplete-ticket.md)

## 항목을 남기는 이유

| 구획 | 다음 독자의 판단 | 상세도 |
|---|---|---|
| Problem | 현재 상황·기회와 바꿀 이유가 무엇인가 | 알려진 근거만 쓴다. 원인 추정은 구별하고 없는 측정은 요구하지 않는다. |
| Proposed outcome | 누구에게 무엇이 나아지며 요청자가 어떻게 확인할 수 있는가 | 제안한 방법을 보존하되 확정된 기술 선택으로 바꾸지 않는다. |
| Affected users and systems | 누구·무엇이 영향을 받는가 | 아는 범위를 쓰며 없는 조직·시스템을 만들지 않는다. |
| Constraints | 무엇을 지키고 무엇은 이번에 하지 않는가 | 확인된 제한과 보존할 동작. 미확인 조건은 열린 질문으로 둔다. |
| Open questions | 다음 단계가 추측하지 말아야 할 것은 무엇인가 | 가능한 답변 담당을 적고, 모르면 미정임을 밝힌다. |

양식에는 답을 남기고 스킬에는 질문·관측과 추정의 구별·상세 추가 판단·원저자 정정 반영을 둔다.
없으면 잡아낼 수 없는 정보까지 작성 완료 조건으로 요구하지 않는다. 반대로 아는 중요한 제약을
간결함을 이유로 생략하지 않는다. 제목은 불가능한 행동뿐 아니라 바라는 개선이나 기회를 표현할 수 있다.

## 기존 양식 대비 달라진 점

해결책을 포괄적으로 금지하던 문구를 없애 요청자의 제안과 확정 제약을 구별했다. 수치·명령·SHA가
없는 요청도 출처와 불확실성을 드러내며 포착한다. 답변 담당자를 모르는 경우를 허용하고 사실처럼
만들지 않는다. 스킬은 답변이 있는 질문을 반복하거나 기술 설계로 확장하지 않으며 원저자의 정정을
문서에 반영한다. 합성 예시 세 개를 필요한 경우에만 읽을 수 있다.

다섯 구획과 두 번째 줄의 작성자·draft 메타데이터는 유지한다. 선택한 형태가 실제 예시에 충분하고,
기존 자동 생성과 하류 인계도 그대로 사용할 수 있기 때문이다. spec·plan의 사용 양식은 이번 대상이 아니다.

## 배포와 검토 범위

기존 프로젝트 스킬 폴더를 갱신했으므로 새 skill 설치 명령이나 외부 plugin 의존성을 추가하지 않는다.
복사해서 사용하는 팀은 capture-intent 폴더 전체와 templates/intent.md를 같은 판으로 갱신하면
예시와 작성 지침을 함께 받는다. 기존 [도입 안내](../../../ADOPTING.md)의 팀 조정 지점을 따른다.

두 리뷰어는 같은 파일을 읽고 보고만 한다. 검토 기준은 [리뷰 요청](review-request.md)에 있다.
이 작업은 양식 설계·작성 예시·소비자 회귀의 부분 검증이며, 전체 SDLC 대화 실험이나 새로운 양식의
자연 스킬 호출 성공률을 측정한 것은 아니다. 리뷰 통과와 사람의 승인·merge도 구별한다.

## 근거

- [Anthropic intent 원문](https://academy.claude.com/courses/ai-native-sdlc-playbook/capture-intent),
  [소개](https://academy.claude.com/courses/ai-native-sdlc-playbook/introduction)
- [보관된 원본 예시와 해석](../references/anthropic-playbook/README.md)
- [수용된 설계 접근](../design-approaches.md)
