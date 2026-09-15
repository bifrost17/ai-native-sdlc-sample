# GSD(Get Shit Done) 조사 메모

## 판과 자료 성격

이 폴더는 2026-09-11에 요청된 공식 저장소 `gsd-build/get-shit-done`의 기본 브랜치
`main`을 커밋
[`bdcaab2c752d9a33a1a1ca9acf3a3c81fb991815`](https://github.com/gsd-build/get-shit-done/tree/bdcaab2c752d9a33a1a1ca9acf3a3c81fb991815)로
고정한 **개발 브랜치 스냅샷**이다. 안정 릴리스라는 뜻이 아니다. 이 저장소는 현재 archived
상태이고, 고정 커밋의
[`README`](https://github.com/gsd-build/get-shit-done/blob/bdcaab2c752d9a33a1a1ca9acf3a3c81fb991815/README.md)는
개발이 `open-gsd/gsd-core`로 이동했다고 알린다. 이번 범위는 지정된 저장소 한 커밋의
양식과 workflow만 분석했으며 새 저장소의 판과 섞지 않았다. 라이선스는 고정 커밋의
[`LICENSE`](https://github.com/gsd-build/get-shit-done/blob/bdcaab2c752d9a33a1a1ca9acf3a3c81fb991815/LICENSE)에
있는 MIT License다. 원문 파일은 수정하지 않았고 세부 메타데이터와 해시는
[sources.json](sources.json)에 있다.

### 후속 프로젝트 확인

이동 대상 `open-gsd/gsd-core`는 확인 시점에 비보관 저장소였고, 기본 브랜치는 `next`,
고정 커밋은
[`eadcba5f53a52856a1149cfeb2ed79e01ec386b4`](https://github.com/open-gsd/gsd-core/tree/eadcba5f53a52856a1149cfeb2ed79e01ec386b4),
라이선스는 [MIT](https://github.com/open-gsd/gsd-core/blob/eadcba5f53a52856a1149cfeb2ed79e01ec386b4/LICENSE)다.
공식 [README](https://github.com/open-gsd/gsd-core/blob/eadcba5f53a52856a1149cfeb2ed79e01ec386b4/README.md)는
Discuss→Plan→Execute→Verify→Ship의 phase loop를 설명하고, 문서는 tutorial, how-to,
reference, explanation으로 나뉜다. 이는 이동 사실과 후속 판의 형태만 확인한 결과다. 현재
기능·양식 비교에는 후속 저장소를 별도 커밋으로 다시 조사해야 한다. 두 링크는 manifest의
`link-only` 항목이며 아래 archived 스냅샷의 원문 집합에 포함하지 않았다.

## 방법과 핵심 기록

GSD는 한 번의 대화가 길어질수록 사라지는 문맥을 `.planning/`의 작은 파일들과 단계별
실행 기록으로 외부화하는 계획·진행 시스템이다. 프로젝트 의도에서 phase와 PLAN을 만들고,
각 PLAN을 실행한 뒤 SUMMARY와 검증 기록으로 실제 상태를 되돌려 적는다. 따라서 핵심은
정적인 “좋은 spec 문서” 하나가 아니라, 다음 세션과 전문 agent가 읽을 권위 있는 파일을
계속 갱신하는 데 있다.

| 원본 양식 | 역할 | 기본 필요성 |
| --- | --- | --- |
| [PROJECT.md](templates/project.md) | 현재 제품 설명, 단 하나의 core value, 검증/활성/범위 밖 요구, 제약과 장기 결정을 보존한다. | 프로젝트 초기화의 핵심 |
| [REQUIREMENTS.md](templates/requirements.md) | testable·atomic한 요구에 ID를 주고 v1, v2, 제외 범위와 phase 추적성을 관리한다. | roadmap의 완료 기준을 만드는 핵심 |
| [ROADMAP.md](templates/roadmap.md) | phase별 목표, 의존 관계, 요구 ID, 사용자 관찰 가능 성공 조건과 plan 진행률을 기록한다. | 장기 작업 경로의 핵심 |
| [STATE.md](templates/state.md) | 현재 위치, 최근 결정, todo, blocker, 중단 지점을 작은 파일로 압축한다. | 모든 workflow가 이어 읽는 연속성 기록 |
| [phase SPEC.md](templates/spec.md) | 한 phase의 WHAT/WHY, 현재와 목표 상태, 명시적 경계와 pass/fail acceptance를 잠근다. | `spec-phase`를 선택한 경우에만 생성 |

PROJECT, REQUIREMENTS, ROADMAP, STATE는 지속되는 공용 기록이다. Phase SPEC은 계획 전
요구 모호성을 낮추는 선택 단계다. 구현 선호는 `discuss-phase`가 `CONTEXT.md`에 적고,
외부 PRD가 있으면 `plan-phase --prd`가 CONTEXT로 추출한다.

이 스냅샷에는 독립된 빈 `PLAN.md` 양식이 없다. PLAN의
header, `wave`, `depends_on`, `files_modified`, `autonomous`, `requirements`, `must_haves`,
objective, task, verification, success criteria 구조는
[`gsd-planner` agent 지침](evidence/gsd-planner-agent.md)에 내장되어 있다. 이를 임의로 떼어
빈 양식이라고 재구성하지 않고 workflow로 보관했다. 실제 결과인 SUMMARY, UAT,
VERIFICATION도 원본 양식 다섯 개와 구별했다.

## 생성과 크기 조절

[`new-project`](evidence/new-project-workflow.md)는 질문과 선택적 research를 거쳐 PROJECT,
REQUIREMENTS, ROADMAP, STATE를 만든다. Brownfield이면 먼저 codebase map을 제안한다.
사용자는 granularity, 병렬 실행, 문서 git 추적, research, plan checker, verifier와 model
profile을 정한다. Phase와 plan 수로 크기를 조절하지만 설정 항목도 많다.

[`spec-phase`](evidence/spec-phase-workflow.md)는 코드를 먼저 살펴 현재 상태를 파악하고,
목표·경계·제약·검증 가능성의 모호성을 여러 질문 라운드로 줄인다. 각 요구는 Current,
Target, Acceptance를 가져야 하고, acceptance는 주관적 표현이 아닌 pass/fail이어야 한다.
[`discuss-phase`](evidence/discuss-phase-workflow.md)는 고정된 phase 범위를 넓히지 않고 구현
선택만 CONTEXT에 적는다. 새 capability는 Deferred Ideas로 보낸다. WHAT/WHY와 HOW를
나눠 planner가 사용자 결정을 임의로 바꾸지 않게 한다.

[`plan-phase`](evidence/plan-phase-workflow.md)는 필요하면 research를 만들고 planner와 plan
checker의 최대 3회 수정 loop를 조정한다. PLAN은 파일, 행동, 자동 검증, 완료 조건을 담은
실행 prompt다. `must_haves`는 phase 목표에서 역으로 도출하며 너무 큰 plan은 분할한다.

## 실행, 공유 상태와 병렬 경계

[`execute-phase`](evidence/execute-phase-workflow.md)는 `depends_on`에서 미리 계산된 wave를
읽는다. 같은 wave의 plan은 파일 소유가 겹치지 않을 때 병렬 실행할 수 있고,
`files_modified`가 하나라도 겹치면 해당 wave를 순차 처리한다. 병렬 agent는 각자 worktree와
PLAN을 받아 구현·테스트·commit·SUMMARY를 만든다. 병렬 모드에서는 orchestrator 하나가
wave merge 뒤 공용 STATE와 ROADMAP을 갱신한다. Task 경계, 파일 소유권, 단일 작성자 규칙이
subagent 수보다 먼저다.

Planner는 의존 그래프와 공유 파일을 보고 plan을 나누고, 자동화할 수 없는 판단이나 수동
행동만 checkpoint로 둔다. 실행 뒤에는 SUMMARY와 실제 파일·commit을 spot-check하고 code
review, regression, drift gate, phase-goal verifier를 잇는다. 이번 조사에서는 실행하지 않았다.

## 갱신과 정합성

PROJECT와 REQUIREMENTS는 phase·milestone·roadmap 변경 뒤 요구와 추적성을 다시 본다.
STATE는 주요 행동 뒤 갱신한다. [`progress`](evidence/progress-workflow.md)는 PROJECT, STATE,
ROADMAP을 권위 원천으로 삼아 다음 plan 생성 또는 실행으로 route한다.

구현 중 scope가 달라지면 [`edit-phase`](evidence/edit-phase-workflow.md)가 ROADMAP의 phase와
의존 관계를 바꾸고 파급 문서를 함께 맞춘다. Plan 작성 뒤
[`gsd-plan-checker`](evidence/gsd-plan-checker-agent.md)는 requirement coverage, task 완전성,
dependency, artifact wiring, 범위, goal-backward verification, CONTEXT 준수를 blocker/warning으로
나눈다. 구현 뒤 [`verify-work`](evidence/verify-work-workflow.md)는 SUMMARY에서 사용자가 확인할
항목을 뽑아 UAT 상태를 파일에 누적하고, gap이 생기면 진단→수정 PLAN→plan checker로 되돌린다.

## 사내 얇은 양식에 참고할 점과 한계

가져올 만한 최소 집합은 PROJECT의 core value·active·out-of-scope, REQUIREMENTS의 안정된
ID와 phase 추적, ROADMAP의 관찰 가능한 phase 성공 조건, STATE의 현재 위치·결정·blocker,
PLAN의 파일 소유·의존·검증이다. 소규모 내부 팀은 이 다섯 역할을 issue 한 장과 짧은 상태
표 하나로 합칠 수 있다. 병렬 변경에서만 file ownership과 single writer 규칙을 추가하면 된다.

전체 GSD 흐름은 SDK query, 설치된 named agent, 여러 command와 config, planning directory,
자동 commit, wave/worktree 관리, research/checker/verifier/UAT loop를 전제로 한다. 긴 자율 작업의
복구에는 의미가 있지만, 얇은 템플릿만 필요한 팀에는 설정과 token·review 시간이 과할 수
있다. 저장소가 archived이고 active 개발 위치가 이동했다는 점도 그대로 제약이다. 이 분석은
공개 원문의 구조와 주장만 다루며 runtime 호환성, 성능, 실제 품질 향상을 확인하지 않았다.

## 보관 자료

- 상류 고정 링크: [phase spec](https://github.com/gsd-build/get-shit-done/blob/bdcaab2c752d9a33a1a1ca9acf3a3c81fb991815/get-shit-done/templates/spec.md), [planner](https://github.com/gsd-build/get-shit-done/blob/bdcaab2c752d9a33a1a1ca9acf3a3c81fb991815/agents/gsd-planner.md), [execute phase](https://github.com/gsd-build/get-shit-done/blob/bdcaab2c752d9a33a1a1ca9acf3a3c81fb991815/get-shit-done/workflows/execute-phase.md)
- 생성과 요구 잠금: [new project](evidence/new-project-workflow.md), [phase spec](evidence/spec-phase-workflow.md), [discussion](evidence/discuss-phase-workflow.md)
- 계획과 검토: [plan phase](evidence/plan-phase-workflow.md), [planner](evidence/gsd-planner-agent.md), [plan checker](evidence/gsd-plan-checker-agent.md)
- 실행과 정합성: [execute phase](evidence/execute-phase-workflow.md), [verify work](evidence/verify-work-workflow.md), [progress](evidence/progress-workflow.md), [edit phase](evidence/edit-phase-workflow.md)
