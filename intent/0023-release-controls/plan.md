# Plan: 릴리스 제어 조사·양식 연결·사용 실험
Upstream: spec.md@5800b05. Status: draft.
사용자의 위임으로 draft에서 진행한다. codex/release-controls는 65a509a에 의존하는 한 문서 PR 범위다.
선행 작업이 main에 통합되면 실제 PR의 base를 재설정한다. 원격 PR·merge·배포는 이번에 하지 않는다.

## Files that change
- docs/research/release-controls/** (new): 1차 자료 비교, 설계 리뷰, 실제 대화 실험과 검증·전달 기록.
- docs/RELEASE-CONTROL.md (new), docs/GIT-WORKFLOW.md, docs/PR-SIZE.md: 조건부 공개 정책.
- templates/{spec,plan}.md, .claude/skills/{design-spec,plan}/SKILL.md와 references/{design-depth,execution-depth}.md:
  해당 상황의 공개 계약·PR 실행 상태·검증 안내. 각 참조는 해당 스킬 아래에 있다.
- REVIEW.md, docs/ADOPTING.md, README.md: 소비자·도입·결과 연결.
- docs/verification/north-star-playbook.html: 관측한 범위의 기존 주석만 보충한다.
별도 codex/use-template-0023을 82d7ad2에서 파생한다. 정책·양식·선택형 examples/skills를 의미상
동기화하고 PROJECT-POLICY의 기존 운영 슬롯에 공개 결정/설정/기록을 연결한다. 제작 자산은 전달하지 않는다.

## Order of work
1. 원문과 조사 자료를 읽고, root가 연구·정책·양식 변경을 작성한다. 독립 조사·소비자 감사 결과를 검토한다.
2. 사용판을 갱신하고 Astra/ultra 및 실제 Claude Code Fable/max에 한정된 설계 delta를 독립 리뷰받는다.
   중요한 지적은 수정하고 같은 최종 후보의 판단을 남긴다. 완결된 한 목적의 문서 PR로 통합 가능해야 한다.
3. 사용판의 초기 실험 브랜치와 파생 작업을 보존한다. root HUMAN과 Sonnet/medium AGENT가 계획·
   PR1·PR2·설정 공개/복구를 대화하며 진행한다. 각 main에서 기존 동작과 일반 OFF/테스트 ON을 검증한다.
   합의한 한 공개 단위가 완성되기 전에는 전체 성공을 주장하지 않는다. 제거는 운영 기간 대신 명시적 모의 조건으로만 시험한다.
4. 독립 verifier가 make check와 계획 범위·인접 흐름을 확인한다. 연구·전달·실험 근거와 주석을 로컬 커밋한다.

## Risks
정책 비대화는 새 필수 양식/엔진을 추가하지 않고 조건부 참조로 줄인다. UI만 숨겨 실제 동작이 열리는
문제와 OFF로 migration을 복구할 수 있다는 오해는 설계 리뷰에서 확인한다. CLI 실험을 서버 보안이나
장기 운영 증명으로 확대하지 않는다. 기존 F02의 먼저 쓸 수 있는 완결 PR 사례는 수정하지 않는다.

## Proof
- AC1: 1차 출처 비교, Astra·Fable 설계 리뷰 및 필요한 수정 후 판단.
- AC2: 실제 Claude Code 대화·분기·커밋·두 통합 결과, 기존 시험 및 OFF/ON·입력 보존·설정 전환 관측.
- AC3: make check와 독립 verifier, 사용판 경계·파일 대응·로컬 링크·북극성 원문/기존 주석 불변 대조.
  스킬은 frontmatter와 참조를 확인한다. 예정 시험은 실행 증거와 구별한다.
