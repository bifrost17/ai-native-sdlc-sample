# Plan: 작은 안내 보완과 F01 대화형 pilot
Upstream: spec.md@2efb6fa. Status: draft.
사용자 위임에 따라 구현과 실험을 진행한다.
## Files that change
- 별도 사용 후보 `codex/use-template-0015`: CLAUDE.md, docs/PROCESS.md, REVIEW.md, templates/plan.md, PROJECT-POLICY.md. 안내·검토 방식·계획의 충분성만 보완한다. 독립 검토에서 발견한 정책 표의 PR 전용 제목도 같은 검토·수락 용어로 맞춘다.
- 제작 브랜치 docs/experiments/README.md, docs/experiments/0015-f01-pilot.md(new): 기준·평가 범위·실행 색인·판정과 근거.
- README.md와 docs/experiments/PERSONA.md: 사용자 후속 설명인 사내 프로그램·얇은 정책·직접 대응 가능한 환경을 반영한다.
- docs/verification/north-star-playbook.html, README.md, INDEX.md, CHAPTERS.md: 해당 주석의 관측 근거와 범위를 추가한다.
- 독립 실험 복제본: PROJECT-POLICY.md·CLAUDE.md의 실제 프로젝트 값, 선택 F01 fixture/baseline, intent 사슬, 코드·시험·사용 안내, 공개된 대화·도구 기록. 결과는 실험 브랜치에 보존하며 제작 브랜치로 합치지 않는다.
## Order of work
1. 원래 사용 기준선을 보존한 후보에서 짧은 문구를 수정하고 diff를 읽는다.
2. 얕은 독립 복제본에 F01 공개 입력만 놓고 환경·기준 시험을 확인한다.
3. Sonnet·low 같은 세션과 자연스럽게 질문·검토·수정·수락·인도를 이어 간다.
4. 중요한 실패는 동작으로 피드백하고 필요한 범위를 고친 뒤 다시 확인한다. 계획 밖 파일이 필요하면 근거를 갱신한다.
5. root가 제품 동작과 전체 흐름 회귀를 판단한다. 결과·한계를 기록하고 통과한 범위만 주석에 추가한다.
## Risks
주석의 제작 환경과 사용 환경 혼동, 비공개 결정 유출, 고정 질문으로 답을 유도하는 실험, 같은 세션으로 대화 없이 구현 가능성을 주장하는 오류를 피한다. 사소한 편차를 없애려 새 강제 장치를 만들지 않는다.
## Proof
F01 baseline과 기존 시험, 오너 결정 기반 외부 동작·파일 불변·최종 diff 확인. 프로젝트 make check와 별도 verifier, HTML 원문 보존·주석 ID 확인. Claude 도구 기록과 실제 HUMAN 입력·단계 수락 커밋을 보존한다.
