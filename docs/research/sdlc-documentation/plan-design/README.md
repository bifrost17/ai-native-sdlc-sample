# 우리 plan 양식 설계

북극성의 **Files that change / Order of work / Risks / Proof**를 기본으로 유지했다.
구체적인 파일·작업 결과·검증을 연결하고, 여러 PR에는 각 머지 뒤 main에서 동작할 범위와 남은
작업을 적는다. 병렬 인계·운영 전환은 필요한 변경에만 상세를 붙인다.

- [공통 양식](../../../../templates/plan.md), [작성 스킬](../../../../.claude/skills/plan/SKILL.md)
- 완성 예시: [작은 기능](../../../../.claude/skills/plan/examples/feature.md),
  [결함](../../../../.claude/skills/plan/examples/bug.md), [두 PR](../../../../.claude/skills/plan/examples/two-pr.md),
  [이행·병렬 작업](../../../../.claude/skills/plan/examples/migration.md)
- [정독과 선택](reading-notes.md), [두 배치 비교](alternatives.md), [계획 변경 판단](change-walkthrough.md)
- [Astra·Fable 독립 리뷰와 최종 판정](review-record.md), [사용판 전달](delivery.md)
- [실제 F02 새 문맥 구현·두 순차 통합·계획 갱신 실험](probe/README.md)

최종 사용 후보는 `codex/use-template-0022@82d7ad2`다. 기본 양식과 선택형 자체 스킬 예시를
포함하며 새 필수 설치·문서 의미 검사기는 없다. 실험에서 발견한 에이전트 누락은 HUMAN의
피드백으로 고쳤고 원래 실패를 남겼다. 사람 개입을 포함해 대체로 잘 동작하는 수준의 통과다.
