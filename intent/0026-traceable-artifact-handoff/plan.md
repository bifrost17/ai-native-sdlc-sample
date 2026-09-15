# Plan: 추적 가능한 문서와 커밋·인계 확인
Upstream: spec.md@57c7721. Status: draft.
Current change: 이 커밋의 spec에 적용 지침 출처를 보충하며, 제품 설계 계약은 유지한다.
현재 인계: T01–T04 완료. 60개 제품 소스의 독립 리뷰와 정적·임시 설치 확인을 마쳤고,
선택형 커밋·인계 fixture는 한 번의 HUMAN 피드백 뒤 두 문서 누락을 해소했다.
결과와 한계는 [실행 기록](execution/README.md), 실제 제품 실험 판은 bc80ef8이다.
T05의 제작용 커밋·로컬 main fast-forward가 남는다. 개인 설치·원격 게시·제품 완료는 범위 밖이다.

사용자가 설계·활성 수정까지 허용했다. 기준 코드는 00fd7334, 작업 브랜치는
codex/traceable-artifact-handoff다. 기존 미추적 003 감사·plan 연구는 보존한다.
이번 인도는 양 판의 문서·패키지 변경 한 묶음이다. 제품 구현·개인 설치본 갱신은 포함하지 않는다.

## Files that change
| 경로 | 역할 | 설계 |
|---|---|---|
| tdd-*/project/templates/{spec,plan}.md | 추적 ID와 작업 양식; intent 양식 유지 | SP01, SP02 |
| tdd-*/project/examples/skills/{design-spec,plan}/ | 작성/인계·재계획 지침과 필요한 참조 | SP01, SP02 |
| tdd-*/project/docs/sdlc-authoring/ | 추적 규칙·작고 큰 실제 작성 예 | SP01, SP02 |
| tdd-*/project/{CLAUDE,REVIEW}.md, docs/{PROCESS,GIT-WORKFLOW}.md | 짧은 정책·시점·검토 | SP03 |
| tdd-*/org-skills/skills/sdlc-feedback/, agents/와 제공 runtime 사본/patch | 커밋·중단·재개 대조와 verifier 기준 | SP03, SP04 |
| 배포판/루트 .claude-plugin, 패키지·adapter README | 기본형 0.1.11 / 선택형 0.1.7 | SP04 |
| intent/0026-traceable-artifact-handoff/ | 설계·리뷰·검증·인계 근거 | 전체 |

## Order of work
로컬 검토 후보는 두 배포판의 같은 추적·인계 계약을 함께 전달한다. 작성 자산과 정책은 서로의
용어를 읽으므로 별개 불완전 배포로 나누지 않는다. GitHub PR/원격 push는 실행 범위로 가정하지 않는다.

### T01 — 작성 양식·스킬
SP01/SP02. worker가 양 판의 spec/plan 양식·작성 스킬·깊이 안내와 추적 참조를 소유한다.
기존 네 plan 절, 명시 호출 정책, 원문 질문·TDD 차이를 유지하며 고정 ID·설계 의미→실제 방법을 넣는다.
Done: AC01/02에 맞게 기존 R/AC 호환과 새 FR/NFR/SP/T의 정본·수명이 보이고, intent는 불변이다.

### T02 — 정책·feedback·verifier
SP03/SP04. 별도 worker가 양 판의 프로젝트 CLAUDE/PROCESS/GIT/REVIEW, feedback과 verifier 사본을 소유한다.
실제 diff 출발, staged/미포함 범위, 중단·인계·재개를 연결하고 기존 완료 검토와 구분한다.
Done: AC03/04/05의 사건과 책임이 실제 사용 지침에서 이어진다. T01과 파일 소유가 분리돼 병렬 수행한다.

### T03 — 예시·패키지 통합
SP01/SP02/SP04. root가 기존 F01/M01의 설계·작업 연결을 보강하되 기존 R/AC와 제품 계약을 유지한다.
T01/T02 뒤 제공 패치를 재생성·시험하고 버전/설치 안내를 맞춘다. 새 설계 사본을 runtime에 중복 설치하지 않는다.
M01에서는 T06 문서 준비/완료와 T07 리허설/전환을 구분해 순환 선행조건을 제거했다.
Done: 작고 큰 예시에서 실제 정본을 찾으며, Claude strict 및 제공 OpenCode/Codex patch가 적용된다.

### T04 — 독립 검토와 제한 행동 확인
전체 SP·AC06. Astra/high 또는 동등 역량의 새 검토자가 현재 spec/plan/diff/실제 근거를 검토한다.
적합한 새 에이전트로 한정 문서 변경·인계 사례를 별도 임시 작업 공간에서 확인한다. 실제 제품 구현은 하지 않는다.
중요한 발견만 고쳐 해당 근거를 재확인한다. 직접 독립 리뷰는 meaningful delivery 전체에서 한 번 수행하며
수정 확인만 이어간다. 검사·리뷰 결과는 실행 기록에 저장한다.
실제 제한 확인은 Sol/medium의 커밋·인계와 새 독자 읽기로 수행했다. 첫 제출의 PR/Done·결정 근거 누락은
기존 원칙으로 한 번 보완했으며 새 규칙을 추가하지 않았다. 두 제품 branch는 Git bundle로 보존한다.

### T05 — 완료 인계
검증된 관련 변경을 커밋하고 현재 main의 상태·차이를 확인한다. 기존 사용자 허가에 따라 제작용
개선을 로컬 main에 반영할 수 있으면 안전한 fast-forward로 반영한다. 원격 게시·사용자 설치를 완료로 주장하지 않는다.
완료·미실행·다음 단계와 실제 판을 execution에 남긴다.

## Risks
가장 위험한 단계는 T02/T03의 runtime 복제본·patch와 기본형/선택형 차이 보존이다.
새 커밋 스킬이나 단어 존재 검사기는 호출 누락·의미 불일치를 보장하지 못해 선택하지 않았다.
ID 재번호·전수 행렬은 과거 링크와 경량성을 깨므로 기존 번호와 단일 정본을 유지한다.

## Proof
| ID | 확인 | 범위·한계 |
|---|---|---|
| P1 | make check, diff/링크·버전·intent 해시 | 기존 정적 회귀; 에이전트 행동 보증 아님 |
| P2 | Claude plugin validate --strict, 제공 패치의 임시 적용·설치 모양 대조 | 패키지/adapter 조합; 개인 설치 아님 |
| P3 | 독립 최종 검토와 제한 문서 행동 결과 | 실제 관찰한 추적·인계만 판정; 전체 SDLC/TDD 실행 아님 |
