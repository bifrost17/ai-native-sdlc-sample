# Anthropic AI-Native SDLC Playbook

이 조사의 기준은 사람과 에이전트가 같은 기록을 읽고 다음 작업을 이어가는 개발 흐름이다.
플레이북은 기존 통제 목적을 유지하면서 작성·인계·검토·피드백 방식을 에이전트의 역량에 맞춰
바꾸는 접근을 설명한다. 초기 Markdown 문서는 제품 책임자와 에이전트가 함께 읽고 행동할 수
있는 공통 기록이다. 문서의 짧음이나 개수가 AI-native 여부를 결정하지 않는다.[^1]

## 문서의 역할

| 산출물 | 원문에서 맡기는 역할 | 혼동하기 쉬운 점 |
|---|---|---|
| `intent.md` | 요청자의 말로 원하는 것·이유·제약을 포착한 proto-spec | 완성된 요구사항 명세와 동의어가 아니다. 초기 요구·구체적 제약은 포함할 수 있다. |
| `spec.md` | 수용된 intent를 요구사항과 설계로 구체화하고 조직 정책을 적용 | 고정 Markdown 양식이 제시된 것은 아니다. |
| `plan.md` | 변경 파일·작업 순서·위험·검증을 구체화 | 대화에 참여하지 않은 엔지니어도 구현할 수 있는 수준을 지향한다. |

Intent는 요청자와 Claude의 대화에서 구체화한다. 모호한 점은 질문하고 요청자가 오해를 수정한다.
조직이 합의한 양식을 사용할 수 있으며, 실제 예시는 문제·기대 결과·대상·제약·미해결 질문을
담는다. 포털에서 상태를 조회한다는 해결 방향도 포함하므로, 모든 해결 제안을 금지하는 것으로
해석할 근거는 없다. 요청자의 제안과 반드시 지켜야 하는 조건을 구별하는 것이 적절하다.[^2]

Spec 단계에서는 Claude가 요구사항과 설계를 한 작업 세션에서 작성하고 제품 책임자가 원래
문제와 비교한다. 미해결 질문은 답하거나 다음 단계로 명시적으로 이어가며, 정책 충돌은 사람이
관련 책임자와 해결한다. 원문은 충분한 spec을 요구하지만 특정 목차나 길이를 강제하지 않는다.[^3]

## 갱신과 사람의 판단

구현이 계획과 달라지면 같은 커밋에서 `plan.md`를 갱신하도록 명시한다. 이는 승인된 계획을
구현 완료 시점까지 고정하라는 뜻과 다르다. 다만 이 문장을 모든 문서를 매 커밋마다 수정하라는
규칙이나 `spec.md`에 관한 동일한 축자 지시로 확대해서는 안 된다.[^4]

이 프로젝트의 spec/plan 동기화 가이드는 관련 변경이 생겼을 때 영향받는 문서를 갱신하도록
구체화한 자체 운영 선택이다. 북극성 원문과 우리의 운영 해석을 구분해야 평가가 순환 논리가
되지 않는다. 자동 작성·검토 지침의 존재만으로 에이전트의 누락이 사라졌다고 판정할 수도 없다.

## 참고 양식의 상태

- [intent 실제 예시](evidence/intent-example.md), [plan 실제 예시](evidence/plan-example.md)는 기존
  저장소의 북극성 문서에서 코드 블록을 추출한 것이다. 비어 있는 범용 양식으로 배포된 파일은 아니다.
- `spec.md`는 원문에 생성 프롬프트와 검토 지침이 있다. 이 조사에서는 가상의 공식 빈 양식을 만들지 않는다.
- 기존 [북극성 문서](../../../../verification/north-star-playbook.html)의 평가 주석은 추출 대상에서 제외했다.
- 출처 메타데이터의 local revision은 이 저장소의 커밋이다. Anthropic의 원문 커밋으로 표시하지 않는다.

## 적용 판단

기존 intent → spec → plan을 유지하는 것이 기준이다. 다른 레퍼런스는 이 흐름에서 빠진 중요한
판단을 돕는 데 사용한다. 의도 문서에 완성된 기술 설계를 앞당겨 요구하거나, 각 양식에 별도
승인 절차를 추가하는 것은 필요성을 따로 입증해야 한다. 문서와 판단을 충분히 남기되 사람이
검토할 핵심과 에이전트가 실행할 세부를 같은 기록에서 찾을 수 있게 한다.

## Sources

[^1]: Anthropic, [Introduction](https://academy.claude.com/courses/ai-native-sdlc-playbook/introduction), 2026-09-11 확인.
[^2]: Anthropic, [Capture as intent.md](https://academy.claude.com/courses/ai-native-sdlc-playbook/capture-intent), 2026-09-11 확인.
[^3]: Anthropic, [Requirements and design](https://academy.claude.com/courses/ai-native-sdlc-playbook/requirements-and-design), 2026-09-11 확인.
[^4]: Anthropic, [Plan mode](https://academy.claude.com/courses/ai-native-sdlc-playbook/plan-mode), 2026-09-11 확인.

원문 URL·추출 경로·해시: [sources.json](sources.json).
