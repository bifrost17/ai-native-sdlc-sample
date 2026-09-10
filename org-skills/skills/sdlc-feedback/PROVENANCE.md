# Provenance

자체 작성한 팀 스킬이다. 원문 스킬을 복제하지 않았다. 설계·실험 기록은 제작 저장소의
`intent/0019-event-review-skill/`와 `docs/experiments/0019-event-review-skill.md`에 둔다.

- 북극성 V4-11: 구현이 계획에서 벗어나면 관련 구현과 같은 커밋에 plan을 갱신.
- V7-09·V8-02·V8-09: 작업 내 피드백과 완료 전 새 문맥의 최종 검증 구분.
- V10-05: PR에서 spec/plan/설계 원칙 준수 여부를 검토.
- V6-04·V6-06: 스킬 사용 조건을 description에 적고 실제 표현을 바꿔 호출을 시험.
- 후속 요구·수락 판·커밋 준비는 위 원칙을 적용하는 팀 선택이며 원문의 별도 의무라고 쓰지 않는다.

0017/0018에서 과거 편집 주장과 현재 파일, HEAD와 plan의 실제 상류 참조가 혼동된 관측을
공통 검토 기준에 반영했다. 같은 모델의 오판을 모두 막는다는 목표는 두지 않는다.
CLI 전용 증거 패킷·JSON 판정·자동 재시도는 옮기지 않았다.

배포 문법은 2026-09-11 [공식 skills 문서](https://code.claude.com/docs/en/skills)와
[subagent 문서](https://code.claude.com/docs/en/sub-agents)를 확인했다. 운영 스킬은 주 세션에
유지하고 검증만 별도 agent에 맡겨 업무 대화의 합의를 인계한다.
