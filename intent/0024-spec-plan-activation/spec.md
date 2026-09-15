# Spec: spec·plan 활성화, 팀 스킬 배포, 실제 개발 검증
Upstream: intent.md@944ce6b. Status: draft.
Skills applied: skill-creator — /Users/jake/.codex/skills/.system/skill-creator/SKILL.md, 시스템 제공 판(버전 미노출), 실제 읽고 적용.
작성/실행 허가: 2026-09-11 프로젝트 오너가 잔여 활성화·설치·실험 진행을 요청했다. 제품 실험 수락은 root의 모의 HUMAN 판단과 구별한다.

## Requirements
| ID | 동작·보존 계약 |
|---|---|
| R1 | 후보 2d3f2dc의 양식/작성 지침/다섯 예시/정책 검토/TDD를 실제 maker와 새 사용판에 전달. 링크·정본 역할과 출처 보존 |
| R2 | 팀의 모든 새/변경 동작 TDD 의무는 얇은 정책에, 공통 수행법은 자체 선택 스킬에, 해당 작업의 첫 시험은 plan에 둠 |
| R3 | org-skills 후속판을 사용자 범위에 설치하고 새 Claude Code 세션의 실제 로드/읽기·적용을 확인 |
| R4 | 제작 자료가 없는 새 사용 기준→제품 seed→파생 작업과 통합 브랜치에서 실제 제품을 개발. 원 기준/대화/실행/Git 이력 보존 |
| R5 | root HUMAN이 응답을 읽고 업무 변경/수락/리뷰를 제공. TDD·문서 동기화·PR 크기/노출·전체 회귀를 실제 근거로 평가 |
| R6 | 중요한 실패를 숨기지 않고 보완·필요한 재실험. 통과한 관측 범위만 주석에 추가, 고정 안내 재사용과 미관측 범위 명시 |

## Acceptance criteria
| ID | 관측 |
|---|---|
| AC1 → R1/R2 | 활성 양식·reference·예시와 org 스킬이 일관되고 상대 링크가 해소됨. 작은/다문서 형태, 공개/복구/TDD 계약 보존; 기존 make check 통과 |
| AC2 → R3 | validate·update·list 성공, 실제 설치 경로/판/내용 확인. 새 정상 세션의 스킬/팀 정책 적용 증거; 후보 폴더 존재만으로 판정하지 않음 |
| AC3 → R4 | 고정된 use/seed/파생/통합 SHA와 tree, shallow 격리·노출 범위 확인. 비공개 HUMAN 데이터와 maker 이력 제외 |
| AC4 → R5 | intent/spec/plan 및 질문·수락, 의미 있는 첫 RED 후 구현/GREEN, 기존 동작 회귀, 최신 결합/머지 후 main, 일반 OFF/시험 ON·완성 공개/중단이 관측됨 |
| AC5 → R5/R6 | plan 수락 뒤 업무 계약 변경에서 영향 spec/plan을 관련 구현과 함께 갱신. HUMAN이 문서 갱신을 지적해야 복구했다면 자발적 성공으로 세지 않음 |
| AC6 → R6 | 독립 검토/검증자로 활성 변경과 실험 근거 확인. 북극성 원문·기존 실패 보존, 새 결과·한계·다음 범위 기록 |

## Design
설계 정본은 [후보 전달안](../../docs/research/sdlc-documentation/spec-plan-design/candidate/policy-and-delivery.md)과
[최종 후보/리뷰](../../docs/research/sdlc-documentation/spec-plan-reassessment/implementation/README.md)이며 입력 판은 2d3f2dc/4774086이다.
이번 사슬은 그 결정을 활성 경로로 전달하고 실제 행동을 검증한다. 양식/스킬을 다시 새로 설계하지 않는다.

maker의 templates, .claude 작성 스킬/reference, docs/sdlc-authoring 예시를 함께 갱신한다. 정책 검토 스킬/명령과
TDD를 org-skills에 배포하고 sdlc-feedback/verifier의 기존 기준에 다문서·test-first·최신 통합/전체 공개 검토를 통합한다.
플러그인은 다음 실제 버전으로 올리며 기존 다른 플러그인과 사용자 설정은 유지한다. 마켓플레이스/설치/세션 읽기 판을 구별한다.

새 use-template는 0023@787af77에서 파생한다. 양식/프로젝트 정책을 전달하고 자동 로드 스킬은 넣지 않는다.
자체 예시는 examples에 두며 선택한 작성 스킬은 실험 제품에서 명시적으로 설치한다. 연구 자료를 실행 입력으로 복제하지 않는다.
제품은 별도 얕은 복제본에서 만들어 maker refs/비공개 기대를 읽지 않게 한다. 실험 refs/공개 증거는 작업 후 maker에 보존한다.

처음에는 기존 작은 Python CLI 데이터로 한 공개 단위/두 PR을 개발한다. 웹 플랫폼을 새로 구축하지 않아도 핵심
작성→실행→변경→검토 흐름을 시험할 수 있다. 서버 인증/브라우저/실운영은 이 실행에서 입증하지 않는다.
공개 문제와 필요한 답만 AGENT에게 주고 HUMAN만 후속 사실·평가 기준을 보관한다. 제품 구현은 Claude Code가 맡는다.
실험의 보완 범위와 재실행은 실제 실패의 영향에 맞게 정하며, 표기 오독마다 새 검사기를 만들지 않는다.

## Constraints and scope
설치·로컬 제품 실행과 로컬 Git 통합을 수행한다. 호스티드 PR/CI·외부 운영 배포는 이 관측을 대체하지 않으며 실행 여부를 따로 기록한다.
정책 스킬과 예시의 선택 가능성, 원문/역사 보존, 분기 고정, 실제 모델/추론/허가 한계는 기존 실험 정책을 따른다.
새 문서 의미 검사기·CLI 하네스·매 응답 독립 검토·모든 UML 강제는 추가하지 않는다.

## Open questions
- 작은 사례와 후속 요청의 정확한 입력은 실행 전 versioned 데이터로 고정한다. root가 기존 페르소나 위임 범위에서 결정한다.
- 실제 설치/호출 경로와 독립 verifier의 가용성은 현재 CLI/실행 근거로 확인한다. 이미 허가된 설치를 재질문하지 않는다.

## Flagged concerns
이전 읽기 전용 인계에서 에이전트가 입력 판과 수락을 혼동하고 변경 영향을 놓쳤다. 실제 근거·사람 피드백·난도에 맞는
모델 선택으로 다룬다. 모델 리뷰/제품 테스트 하나로 프로세스 전체 성공을 추론하지 않는다.
