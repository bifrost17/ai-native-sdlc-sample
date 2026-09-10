# Plan: 문서 갱신 누락을 재현하고 작은 지침으로 보완
Upstream: spec.md@ab53dbd9a060507cafcc6ae0c2f41b1d589c5d10. Status: draft.
root가 설계·실험 판단을 위임받아 진행한다. spec 제목의 언어 오타 정정은 기능 결정에 영향이 없다.

## Files that change
- 사용 후보 codex/use-template-0017: CLAUDE.md, REVIEW.md, docs/PROCESS.md, docs/GIT-WORKFLOW.md.
- 제작 docs/GIT-WORKFLOW.md: 사용판과 동일한 정책 원문.
- docs/experiments/datasets/v3/manifest.json, cases.json(new): 기존 F02 기반과 JSON/파일 출력의 공개 업무 조건.
- docs/experiments/0017-artifact-sync.md(new), README.md, docs/experiments/README.md,
  docs/experiments/0016-flow-pilot.md: 원래 실패 재판정·새 후보·입력·실행 결과와 한계.
- docs/verification/north-star-playbook.html, README.md, INDEX.md, CHAPTERS.md: 변경된 사용판 근거와 판정.
- intent/0017-artifact-sync/{intent,spec,plan}.md: 이 변경의 사슬.
- 제품·대화·코드·실제 커밋·실행 출력은 별도 실험 clone/브랜치에만 보존한다.

## Order of work
1. 원문 plan 개정/governance와 원래 누락을 읽는다. CLI 지침 주입 여부를 독립 감사하고 과거 근거의
   한계를 명시한다. 설계 검토로 후속 요청/완료 조건과 기존 spec→plan SHA 순서의 연결을 확인한다.
2. 기존 문서 4개를 작게 보완하고 새 사용 후보를 고정한다. 누락을 중요한 실패로 재분류한다.
3. 두 사례의 업무 사실을 고정하고 서로 다른 새 세션에서 PR2를 구현한 뒤 후속 요구를 전달한다.
   HUMAN은 사업 결정·문서 수락·Git 작업을 맡되 'spec/plan 수정' 상기를 하지 않는다.
4. 필요한 문서 갱신·수락 대기를 보고하면 실제 산출물을 읽고 판을 커밋/수락한다. 깨진 참조나
   문서 누락을 남긴 완료 보고는 해당 실행 실패다. 피드백 후 복구를 통과로 바꾸지 않는다.
5. 제품 시험·독립 동작·기존 시험/fixture 보존, 문서·코드·Upstream과 같은 커밋을 확인하고 기록한다.
6. 독립 verifier가 제작 make check, 변경/계획 양방향, 이전 사슬, 나쁜 hook 입력, 새 실험 근거와
   전체 흐름의 중요한 인계를 확인한다. 고정 가이드는 재사용하고 새 관측만 북극성에 반영한다.

## Risks
규칙 주입 실패를 모델 준수 실패와 혼동, HUMAN이 정답 문서 수정을 지시해 실험을 오염,
무조건 spec/plan 편집이나 매번 승인으로 과도한 절차를 생성, 코드 시험만으로 통과 처리하는 위험.

## Proof
새 세션 init/실제 지침 읽기, 공개 업무 프롬프트와 개정 diff/결정 기록, 실제 커밋의 변경 파일과
Upstream SHA, 각 제품 unittest·독립 CLI 관측. 두 사례의 초기 누락 여부를 별도로 기록한다.
make check와 .claude/agents/verifier.md 네 부분 보고, 사용 정책 동일성·원문 불변·링크·입력/기록 해시.
기본 60분/12 HUMAN 턴 안에서 진행하고 도구·스킬·모델·비용은 관측된 값만 보존한다.
