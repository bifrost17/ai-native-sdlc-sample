# Superpowers 조사 메모

## 판과 분류

이 폴더는 2026-09-11에 공식 저장소 `obra/superpowers`의 기본 브랜치 `main`을 커밋
[`b36e0829c6d0140e93cfef2ca599b1b07d4a7797`](https://github.com/obra/superpowers/tree/b36e0829c6d0140e93cfef2ca599b1b07d4a7797)로
고정한 **개발 브랜치 스냅샷**이다. 최신 안정 릴리스라는 뜻이 아니며 다른 tag나 예전 글의
절차를 섞지 않았다. 라이선스는 고정 커밋의
[`LICENSE`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/LICENSE)에
명시된 MIT License다. 원문은 수정하지 않았고 URL, 원래 경로, 해시는
[sources.json](sources.json)에 있다.

Superpowers는 독립된 spec schema보다 대화→설계→상세 계획→task별 구현·검토를 강제하는
composable skill 방법이다.
공식
[`README`](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/README.md)는
agent가 의도를 질문하고, 사람이 design을 승인한 뒤, 문맥 없는 구현자도 따를 plan을 만들어
subagent 또는 inline 실행으로 넘긴다고 설명한다. BMAD의 spec kernel이나 GSD의 상태
시스템과 같은 종류라고 단정해서는 안 된다.

## 빈 양식의 부재와 문서 역할

이 커밋은 복사해서 채우는 별도 blank spec 또는 implementation plan 파일을 배포하지 않는다.
`templates/` 폴더를 임의로 만들거나 skill의 일부를 떼어 “공식 양식”으로 재구성하지 않았다.
Spec 작성 지시는 [brainstorming skill](evidence/brainstorming-SKILL.md)에, plan 구조는
[writing-plans skill](evidence/writing-plans-SKILL.md)에 내장되어 두 원문을 workflow로 보관했다.
저장소에
[spec reviewer prompt](evidence/spec-document-reviewer-prompt.md)와
[plan reviewer prompt](evidence/plan-document-reviewer-prompt.md) 파일도 존재하지만, 현재 두
주요 skill은 inline self-review를 명시한다. Prompt 파일 존재만으로 모든 실행에서 별도
reviewer가 자동 호출된다고 해석하지 않는다.

| 내장된 산출물 | 역할 | 생성 조건 |
| --- | --- | --- |
| 채팅 안의 짧은 design | 기존 코드의 분명한 작은 변경에서 접근, 수정 파일, 검증 방법을 합의한다. | bounded path에서 필수, 별도 파일은 없음 |
| `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` | architecture, component, data flow, error handling, testing을 사람이 승인한 설계로 기록한다. | architectural path에서 필수 |
| `docs/superpowers/plans/YYYY-MM-DD-<feature>.md` | goal, architecture, tech stack, spec 경로, global constraints와 task별 파일·interface·TDD step을 기록한다. | 승인된 architectural spec 다음에 필수 |
| task brief/report/review package와 progress ledger | 각 구현자에게 필요한 범위만 전달하고, commit·test·review 상태를 재개 가능하게 남긴다. | subagent-driven 실행 경로에서 사용 |

## 크기에 따른 경로와 사람의 승인

현재 [`brainstorming`](evidence/brainstorming-SKILL.md)은 요청을 spike, bounded,
architectural로 먼저 분류한다. Spike는 가능성에 대한 답이 목적이라 probe 계획만 승인받고
결과를 보고한다. Bounded는 기존 flow의 작은 변경이며, 채팅의 짧은 design을 승인받은 뒤
별도 spec·plan 없이 구현한다. Architectural은 새 subsystem이나 공용 interface 변경이다.
이때 대안을 비교하고 design 문서, self-review, 사용자 review 뒤 implementation plan으로 간다.

모든 경로에 구현 전 승인 gate가 있지만 artifact 크기는 다르다. 숨은 복잡성이 나오면 더
무거운 경로로 올리고, 큰 요청은 subsystem별 spec→plan→구현 cycle로 나눈다. 사람의 확인
지점은 유지하면서 작은 변경의 문서량은 줄인다.

Spec에는 고정된 필드 schema가 없다. 질문은 목적, 제약, 성공 기준을 중심으로 하고, 표현은
복잡도에 맞춘다. 작성 후 placeholder, 모순, 큰 범위, 모호한 요구를 inline으로 고친다.
사람이 파일을 승인해야 plan을 만들며, 변경 요청 뒤에는 self-review를 다시 한다.

## Plan과 구현 경계

[`writing-plans`](evidence/writing-plans-SKILL.md)의 plan header는 한 문장 goal, 2~3문장
architecture, tech stack, 권위 있는 spec 경로, spec에서 정확히 복사한 global constraints를
요구한다. 각 task는 생성·수정·test 파일의 정확한 경로와 이웃 task가 소비하고 생산하는
interface를 적는다. Step은 failing test 작성, 실패 확인, 최소 구현, 통과 확인, commit처럼
2~5분짜리 한 행동으로 나눈다. TBD, “적절한 error handling”, “위와 비슷하게 구현” 같은
placeholder는 plan 실패다. 작성 후 spec의 모든 요구가 task에 연결되는지, placeholder가
없는지, 앞뒤 task의 type과 method 이름이 일치하는지 스스로 검사한다.

Task는 자체 test cycle과 독립 reviewer 판단이 의미 있는 최소 단위다. Setup, config,
scaffold, docs는 관련 deliverable task에 합치고, 인접 task를 따로 거절할 이유가 있을 때
나눈다. 얇은 양식도 `작업/파일/입력 interface/출력 interface/검증`은 남길 수 있다.

계획 뒤 사용자는 두 실행 방식을 고른다. [`executing-plans`](evidence/executing-plans-SKILL.md)는
별도 session에서 plan을 비판적으로 읽은 뒤 task를 순서대로 실행하고 검증한다. 치명적 plan
gap이나 반복 검증 실패가 있으면 사람에게 되돌아간다. 더 정교한
[`subagent-driven-development`](evidence/subagent-driven-development-SKILL.md)는 같은 session의
controller가 task마다 문맥을 새로 구성해 구현자를 보내고, task-scoped review와 마지막 전체
branch review를 조정한다.

Subagent 경로는 plan별 workspace와 ledger로 compaction 뒤 중복 dispatch를 막는다. Controller는
구현자에게 전체 대화 대신 task brief, 필요한 interface, report 경로만 준다. Implementer는
구현·test·commit·self-review를 끝내고, 독립 reviewer가 spec compliance와 code quality를 판정한다.
중요 finding은 수정과 범위가 제한된 re-review를 거치며, 모든 task 뒤에는 전체 branch review가
있다. 작은 반복 변경은 하나의 review surface로 묶을 수 있지만, 서로 충돌할 implementation
agent를 병렬로 보내지는 않는다. 모델도 task 난이도와 검토 판단 난이도에 맞춰 고르도록 한다.

## 변경과 정합성

이 workflow에서 spec은 binding authority이고 plan은 spec을 구현하기 위한 논증이다. 실행 전
plan 내부의 task·interface 충돌을 표로 검사하고, 충돌이 드러나면 controller가 spec을 기준으로
판정해 ledger와 후속 brief에 남긴다. 구현자가 예상 밖 architecture 선택이나 task 범위 확대를
만나면 임의로 재설계하지 않고 `NEEDS_CONTEXT`, `BLOCKED`, `DONE_WITH_CONCERNS`로 돌려보낸다.
Review 결과가 plan 문구와 충돌해도 plan 자체가 자기 정당성을 증명하지는 않으며, controller가
spec과 기술 근거로 판정한다.

다만 이 스냅샷에는 BMAD의 append-only spec memlog나 course-correction proposal,
OpenSpec식 변경 archive처럼 일반화된 spec 변경 원장이 없다. Design 단계에서는 사용자 수정
후 문서를 다시 검토하고, 실행 단계에서는 ledger와 git commit이 판단과 구현 이력을 맡는다.
기능 의도가 바뀌면 spec을 먼저 고치고 coverage review를 다시 하는 것이 authority 관계에
맞지만, 별도 update command는 정형화되어 있지 않다.

## 사내 얇은 양식에 참고할 점과 한계

가져올 핵심은 작업 크기별 artifact 생략, 구현 전 사람이 읽을 수 있는 design 승인, plan에
spec 경로와 global constraints를 명시하는 것, review 가능한 task 경계, 구현자와 reviewer의
문맥 격리, spec compliance와 code quality 판정의 분리다. 내부 팀의 bounded 변경은 issue에
의도·영향 파일·검증만 적고 승인하면 충분하다. Architectural 변경에만 design 문서와 상세
task plan을 추가하면 된다.

전체 subagent-driven 경로는 task마다 brief와 report, diff package, reviewer, fix loop, ledger,
worktree와 여러 model 호출을 요구하므로 작은 팀의 얇은 흐름보다 도구·token·시간 비용이
크다. 별도 subagent가 없는 환경에서는 inline 실행이 가능하지만 검토 구조가 달라진다. 이
조사는 공개 지침만 분석했고 skill을 설치·호출하거나 runtime 동작, 품질 향상, 장시간 자율 실행
주장을 실험하지 않았다.

## 보관 자료

- 상류 고정 링크: [brainstorming](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/brainstorming/SKILL.md), [writing plans](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/writing-plans/SKILL.md), [subagent-driven development](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/subagent-driven-development/SKILL.md)
- 설계와 계획: [brainstorming](evidence/brainstorming-SKILL.md), [writing plans](evidence/writing-plans-SKILL.md)
- 실행 선택: [executing plans](evidence/executing-plans-SKILL.md), [subagent-driven development](evidence/subagent-driven-development-SKILL.md)
- task 경계: [implementer prompt](evidence/implementer-prompt.md), [task reviewer](evidence/task-reviewer-prompt.md), [scoped re-review](evidence/re-review-prompt.md)
- 전체 검토: [requesting code review](evidence/requesting-code-review-SKILL.md), [code reviewer](evidence/code-reviewer-prompt.md)
