# plan 설계 전 정독과 선택

root는 [설계 방향](../design-approaches.md), [종합 보고](../report.md), [비교](../comparison.md),
[후보 기록](../candidates.md), [PR 조사](../../pr-size/README.md), 현재 PR-SIZE·GIT-WORKFLOW를
다시 읽고 아래 원문과 대조했다. Astra의 독립 설계 도전과 Sol의 소비자 감사도 함께 받았다.
고정된 기존 조사 원본을 읽은 것이며 새로 상류 최신판을 조사하거나 모든 workflow를 실행한 것은 아니다.

| 근거 | 적용 | 가져오지 않는 것 |
|---|---|---|
| 북극성 L4 원문과 실제 plan 예시 | 네 정보 역할, 실제 코드 읽기, 대화 없이 실행할 인계, 같은 커밋 갱신 | 모든 단계의 코드 복제, 완전성 자동 검사 |
| L7 원문 | 독립 세션의 branch/worktree, 공유 파일 순차 실행, 한정된 subagent | 작업·에이전트·PR 일대일, 파일만 다르면 독립이라는 판정 |
| L8 원문 | 작업 중 반복 검증, 최종 새 context 확인, 결함 재현 실패를 먼저 확인·커밋 | 모든 기능에 실패 테스트부터라는 보편 순서 |
| L10 원문 | spec/plan과 최종 diff의 일치·위험을 사람이 판단 | AI PASS를 사람 승인으로 간주 |
| [Spec Kit tasks](../references/github-spec-kit/templates/tasks-template.md) | 독립 사용자 결과, 파일과 작업, 통합 후 확인 | 설계 역할 plan-template 전체, 고정 phase·ID·체크박스 |
| [OpenSpec tasks](../references/openspec/templates/tasks.md) 및 schema 지침 | 개별 결과의 확인, 여러 작업을 가로지르는 통합 확인 | 파서 구문·CLI 운영 체계 |
| [Superpowers writing](../references/superpowers/evidence/writing-plans-SKILL.md) / executing | 파일 역할·소비/제공 계약·신규 독자 | 전 코드 작성, 2–5분 단계, 필수 외부 sub-skill |
| [Spec Kitty WP](../references/spec-kitty/templates/task-prompt-template.md) | 문맥·소유·의존·인계 | 상태 이벤트·profile·계획 변경을 별도 WP로 강제 |
| [GSD](../references/gsd/README.md), planner의 dependency graph | 결과에서 역으로 Proof, 공유 계획 조정 | wave/state 엔진, 고정 작업 수·토큰비율, 파일 비중복만의 독립 판정 |
| [Kiro](../references/kiro/README.md), [BMAD](../references/bmad/README.md) | 보존할 동작·관련 산출물 갱신·공유 결정 | 전체 문서 체계·모든 작은 변경의 승인 gate |

원문 L4 실제 예시는 endpoint→panel→nav이며 범용적인 failing-test-first 예시가 아니다.
L8의 결함 재현 규칙을 해당 작업에 적용한다. plan은 spec의 HOW 설계를 다시 쓰기보다 실제
파일·순서·통합·확인에 내려간다. spec-kit plan이라는 이름만 보고 우리 plan과 같은 역할로 취급하지 않는다.

## 현재 정책과 소비자

현재 사용판 ca87cdb에는 이미 PR 묶음·통합 뒤 동작 안내가 있고 maker의 plan보다 최신이다.
그 의미를 보존하고 더 구체화한다. maker 스킬의 문서별 origin/main 수락과 “plan mode만이 기록”
문구는 현재 GIT-WORKFLOW의 SHA를 가진 사람 결정과 다르므로 고친다. 모드와 수락 증거는 별개다.
네 절/Upstream/Status는 유지한다. 현재 verifier만 whole-plan과 current-PR 범위를 구분하도록
고친다. eval·harness는 plan 본문을 고정 절로 파싱하지 않아 새 검사나 fixture 변환이 필요 없다.

이 제작 변경은 064c785에 의존한다. main부터의 전체 diff를 이번 plan 변경이라고 보고하지 않는다.
사용판은 ca87cdb에서 별도 파생해 선택성·제작 자산 제외를 보존한다. 역사 예시·주석을 새로운
양식에 맞춰 고쳐 과거 성과를 다시 쓰지 않는다.
