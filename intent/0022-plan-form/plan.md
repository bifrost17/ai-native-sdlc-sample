# Plan: 예시에서 도출한 실행 계획과 PR 통합 인계 검증
Upstream: spec.md@1ab184e. Status: draft.
사용자의 작성·반영 위임으로 draft에서 진행한다. 제작 기준은 선행 0021 완료 064c785이며,
codex/plan-template-design은 그 판에 의존한다. 실제 PR을 열면 선행 작업을 base로 표시하고
선행 merge 뒤 최신 main에 재설정한다. 이번 변경 자체는 한 목적의 PR이며 원격 작업은 하지 않는다.

## Files that change
- intent/0022-plan-form/{intent,spec,plan}.md: 이번 변경의 단계별 근거와 실행 기록.
- templates/plan.md, .claude/skills/plan/SKILL.md: 네 절 양식·작성/인계/갱신 지침.
- .claude/skills/plan/{examples,references}/** (new): root의 기능·버그·여러 PR·이행 예시와 조건부 상세.
- .claude/agents/verifier.md: 현재 PR 범위를 확인하여 미래 PR 파일을 누락으로 판정하지 않도록 수정.
- REVIEW.md, docs/PLAYBOOK-MAP.md: 독립 리뷰에서 확인한 현재 소비자의 PR 범위·수락 설명을
  기존 GIT-WORKFLOW와 맞춘다. 사용자 위임 범위의 연동 정정이며 spec 1ab184e에 범위를 기록했다.
- docs/METRICS.md: 후속 리뷰에서 확인한 plan 관련 측정 안내도 PR 개수가 아닌 계획된 범위·
  실제 수락 기록으로 읽도록 맞춘다. 새 측정 코드나 전체 지표 재평가는 추가하지 않는다.
- docs/research/sdlc-documentation/plan-design/** (new): 정독·예시 맥락·대안·갱신·리뷰·전달·실험 근거.
- docs/research/sdlc-documentation/README.md, README.md: 최종 결과와 실제 사용 후보 연결.
- docs/verification/north-star-playbook.html: 이번에 확인한 범위만 기존 주석에 추가. 원문·등급 보존.

별도 사용판 codex/use-template-0022는 codex/use-template-0021@ca87cdb에서 파생한다.
templates/plan.md, examples/skills/plan/{SKILL.md,examples/**,references/**}, examples/README.md만
전달하며 예시가 참조하는 기존 spec은 사용판 위치에 맞춘다. 선택 스킬·제작 자산 제외를 유지한다.
여기서 F02 제품 baseline을 얹은 별도 실험 기준 브랜치와 파생 작업 브랜치/worktree를 보존한다.
실험 코드·시험은 실험 브랜치에만 남기고 maker에는 재현 입력·결과·필터링한 대화 기록을 보존한다.

## Order of work
1. root가 종합 조사·설계 방향·원본 L4/L7/L8/L10 및 관련 자료·PR 정책을 재독한다. 독립 Astra
   설계 도전과 Sol 소비자 감사는 읽기 전용으로 병렬 진행한다. root가 완성 예시부터 작성한다.
2. 네 절과 작업별 묶음 두 배치를 실제로 대조해 공통 양식·선택 상세를 도출한다. 작성 스킬과
   현재 verifier의 범위 해석을 맞춘다. 중요 설계 문제는 spec으로 돌리고 작은 변경은 plan에서 결정한다.
3. 사용 후보를 전달하고 핵심 파일 해시를 고정한다. Astra/ultra와 실제 Fable/max에 서로의 결과
   없이 같은 후보를 제공한다. root가 중요 지적을 수정하고 같은 최종 판의 두 PASS를 받는다.
4. F02에서 Sonnet/medium과 HUMAN 역할 root가 실제 대화한다. 계획 생성 후 새 세션에 승인된
   문서와 선언된 참조만 넘겨 첫 실행·통합을 확인한다. 후속 파일/검증 계획 변경은 대화로 결정하고
   관련 구현 커밋의 plan 갱신을 확인한다. 종속 두 작업을 가짜 병렬 성공으로 집계하지 않는다.
5. 독립 verifier가 make check와 아래 Proof, 선행 0021·훅 부정 입력·사용판 경계를 확인한다.
   최종 자료와 주석, 로컬 커밋으로 닫는다. 공개 원문과 역사 기록은 수정하지 않는다.

## Risks
양식이 사실상 작업 엔진으로 커지는 위험은 작은 예시의 중복·필수 표를 대조해 발견하고 덜어낸다.
첫 PR에서 제품이 깨지는 분할은 해당 main 상태의 시험으로 확인한다. 병렬 파일 경계만으로 공유
계약·계획 갱신을 놓치는 위험은 이행 예시와 독립 리뷰로 다루되 실제 병렬 실행 관측으로 표시하지 않는다.
모델의 실수는 기록·수정하며 규칙을 계속 늘리지 않는다. 승인된 판과 수정 중인 파일, 예정 Proof와
실제 결과를 구별한다. 실험용 데이터는 각 시험에서 복사하고 사용자 파일·기존 이력을 덮어쓰지 않는다.

## Proof
- AC1: 네 유형의 작성 예시, 두 배치 비교, 변경 전후 기록과 독립 독자의 인계 판단.
- AC2: Astra/ultra·Fable/max의 같은 후보 파일 해시 PASS와 원문 결과(비공개 추론 제외).
- AC3: F02 실제 Claude Code 대화·새 세션 ID·Git 분기/커밋/통합 기록, 기존 세 테스트 및
  추가 기능 테스트, HUMAN oracle의 목록·요약·complete 후 요약·바이트 보존 결과.
- AC4: make check 전체 출력(기존 Python·hooks·eval fixtures·managed settings), make evals의
  실제 가용 여부, skill quick_validate.py와 선택 스킬 frontmatter의 도구 차이 설명, 독립 verifier.
  로컬 참조·후보 해시·전달 파일·북극성 원문/기존 주석 불변은 일회성 자료 대조로 확인한다.

검사는 이 단계에서는 예정이다. 실제 결과·실패·수정·한계는 plan-design 기록에 연결한다.

## Execution record

root 정독·예시·두 배치 비교 후 R1을 cea1abf/95c0933에 보존했다. 두 독립 리뷰의 비차단 소비자
지적을 필요한 범위로 고쳐 최종 maker b4ab132/adopter 82d7ad2의 같은 23파일 후보를 Astra/ultra와
실제 Claude Code Fable/max가 PASS했다. [선택·수정·리뷰 기록](../../docs/research/sdlc-documentation/plan-design/review-record.md).

F02는 사용판에서 별도 초기 제품 34f41ee를 만들고 파생 branch/worktree로 실행했다. Sonnet/medium
세 세션·여섯 대화에서 새 문맥의 구현과 두 순차 로컬 통합을 확인했다. PR1의 plan 갱신 누락은
1033eea에 보존했고 HUMAN 피드백 후 10b08bc에 계획·구현을 함께 담았다. 이를 자발적 통과로
계산하지 않는다. PR2는 검증 방법 보강을 plan·구현 같은 커밋에 반영했고 잘못된 증거 참조를
리뷰 후 고쳤다. 최종 실험 main f20a165는 16시험과 HUMAN의 12동작 확인을 통과했다.
[실험 입력·단계·실패·회복·한계](../../docs/research/sdlc-documentation/plan-design/probe/README.md).

독립 verifier가 기존 make check, 최종 제품 통합·첫 PR 상태, 원래 입력 보존, 문서·구현 커밋,
23파일 해시와 전달 경계를 확인했다. make evals는 키 없음 rc=2 SKIP이며 통과로 세지 않았다.
[검증 보고](../../docs/research/sdlc-documentation/plan-design/reviews/verifier-final.md).
root가 최종 색인·기록·관련 주석을 추가하고 원문/179 주석 ID·등급 불변과 로컬 링크를 대조했다.
새 프로덕션 검사기나 필수 설치는 추가하지 않았다. 이 계획은 로컬 반영까지 완료했으며 hosted
PR/CI·운영 배포·실제 병렬 개발·M01 이행을 실행한 것으로 확대하지 않는다.
