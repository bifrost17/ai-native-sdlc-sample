# BMAD Method 조사 메모

## 판과 자료 성격

이 폴더는 2026-09-11에 공식 저장소 `bmad-code-org/BMAD-METHOD`의 기본 브랜치
`main`을 커밋
[`abe4eb1bce919c9d22cd18b3519353d5824c4b75`](https://github.com/bmad-code-org/BMAD-METHOD/tree/abe4eb1bce919c9d22cd18b3519353d5824c4b75)로
고정해 읽은 **개발 브랜치 스냅샷**이다. 최신 안정 릴리스라고 부르지 않으며, 과거
튜토리얼이나 다른 태그와 섞지 않았다. 이 판의 `bmad-spec`은 Why, Capabilities,
Constraints, Non-goals, Success signal의 작은 계약 커널을 사용한다. 현재 PRD는 user
journey, 전역 FR ID, 성공 지표, 가정 색인과 상황별 확장 메뉴를 갖는다.

저장소 API의 license 분류는 `NOASSERTION`이지만, 고정 커밋의
[`LICENSE`](https://github.com/bmad-code-org/BMAD-METHOD/blob/abe4eb1bce919c9d22cd18b3519353d5824c4b75/LICENSE)는
MIT License를 명시한다. 같은 파일에는 BMad 관련 상표 고지도 있다. 내려받은 원문은
수정하지 않았고, 해시와 URL은 [sources.json](sources.json)에 있다.

## 방법과 문서의 역할

BMAD는 하나의 spec 양식이라기보다 아이디어 탐색부터 요구사항, 공유 설계, 작업 분할,
구현, 검토와 회고까지 포괄하는 넓은 개발 방법이다. 공식
[`choose-a-planning-path`](https://github.com/bmad-code-org/BMAD-METHOD/blob/abe4eb1bce919c9d22cd18b3519353d5824c4b75/docs/plan/choose-a-planning-path.md)는
먼저 “완료 뒤 무엇이 참이어야 하며, 무엇을 바꾸지 않고, 무엇이 범위 밖인가”가 충분히
분명한지를 묻는다. 이미 분명한 작은 변경은 `bmad-spec` 또는 곧바로 Build로 보내고,
명확하지 않거나 여러 사람이 합의해야 하는 일에만 brief, PRD, UX, architecture 같은
앞단 산출물을 더한다.

| 원본 양식 | 역할 | 기본 필요성 |
| --- | --- | --- |
| [product brief](templates/product-brief-template.md) | 문제, 대상, 차별점, 성공 기준, 최초 범위와 장기 비전을 짧게 공유한다. | 제품 서사가 필요할 때 선택 |
| [PRD](templates/prd-template.md) | 조직이 합의할 비전, 사용자 여정, 용어, 기능 요구, 비목표, 범위, 지표와 미해결 질문을 보존한다. | 여러 이해관계자나 여러 epic이 같은 제품 판단을 공유할 때 권장 |
| [SPEC](templates/spec-template.md) | 다음 작업자가 읽는 정규 계약이다. capability마다 의도와 검증 가능한 성공 조건을 둔다. | 정의된 의도를 구현 계약으로 넘길 때 핵심 |
| [architecture spine](templates/architecture-spine-template.md) | 서로 따로 구현하면 충돌할 기술 결정을 안정된 `AD-n` ID와 규칙으로 고정한다. | 여러 epic, 여러 구현자, 교차 시스템 변경에서 필요 |
| [epics and stories](templates/epics-and-stories-template.md) | PRD 요구를 사용자 가치 단위 epic과 Given/When/Then 수용 기준이 있는 story로 나눈다. | 프로젝트 규모 작업의 실행 분할에 필요 |

양식은 체크리스트가 아니다. Brief는 섹션을 버리거나 재배치하고, PRD는 기본 spine과 제품
유형별 선택 섹션을 나눈다. 작은 범위는 한두 쪽에 story까지 넣을 수 있다. Architecture
spine도 작은 의도에는 paradigm과 소수 결정만 남기고, 코드가 생기면 상세 구조를 코드에 맡긴다.

## 생성, 갱신, 검토 흐름

현재 흐름의 중심은 `SPEC.md` 한 파일만이 아니라 spec 폴더다. 공식
[`bmad-spec` 지침](evidence/spec-SKILL.md)은 `.memlog.md`를 append-only 결정 기록으로
두고, `SPEC.md`와 spec이 작성한 companion을 그 기록에서 다시 렌더링한다. 긴 용어표,
상태 머신, 다이어그램처럼 커널을 부풀리는 내용은 이름이 분명한 companion으로 분리한다.
외부 UX나 architecture 문서는 adopted companion으로 연결하고 원 작성 skill만 수정한다.
`sources`는 이미 완전히 흡수한 입력의 감사용 목록이고, downstream agent는 `companions`를
반드시 읽는다. 이 구분은 사람과 에이전트가 “무엇이 현재 계약이고 무엇이 배경 자료인가”를
같게 판단하도록 한다.

Spec 생성과 갱신 뒤에는 coherence와 source preservation을 별도로 검사한다. capability
ID는 재사용하거나 다시 번호 매기지 않는다. 기존 spec에 변경이 들어오면 memlog에 뒤의
결정을 추가해 앞 결정을 대체하고, 원본 입력의 판단까지 뒤집었다면 그 원본도 갱신할지
제안한다. `stories.yaml`은 선택적인 Story Breakdown 결과이며 계약 companion이 아니다.
Spec이 바뀌어 기존 story가 어긋나면 재분할을 제안하지만, spec 갱신만으로 story 파일을
몰래 덮어쓰지 않는다.

PRD도 create, update, validate를 구분한다. 공식
[`bmad-prd` 지침](evidence/prd-SKILL.md)은 사용자 결정을 memlog에 남기고, PRD에 어울리지
않는 기술적 깊이나 대안 근거는 addendum에 보존한다. 최종화 때 기록 누락, 입력 누락,
검토 결과, 가정과 미해결 질문을 차례로 정리한 뒤 `status: final`로 닫는다. stakes에 따라
검토 강도는 stakes에 맞추며 hobby/solo에서는 생략할 수 있다.

구현 중 큰 변경은 단순히 story 메모에 숨기지 않는다.
[`correct-course`](evidence/correct-course-SKILL.md)는 PRD, epic/story, architecture, UX,
spec을 함께 읽어 영향과 구체적인 이전/이후 편집안을 Sprint Change Proposal로 만든다.
사용자가 전체 제안을 승인한 뒤 minor, moderate, major에 따라 구현자나 PM/architect로
handoff한다. [`break-work`](evidence/break-work-into-stories-and-track-it.md) 지침은 tracking
재생성 시 완료 상태와 수기 메모를 보존하고, repair는 실제 파일과 git 이력을 바탕으로
제안 상태를 먼저 보여준 뒤 확인 후 쓴다.

## 사람과 에이전트, 병렬 작업

사람은 제품 의도, 중요한 대안, 가정 해소와 course correction 승인에 책임을 가진다.
에이전트는 입력 추출, 계약 재렌더링, 커버리지와 이력 대조를 맡는다. Architecture의
coaching 경로에서는 사람이 핵심 결정을 고르고, fast 경로는 `[ASSUMPTION]`을 붙인다.

병렬 작업은 문서 수보다 경계의 명시성이 먼저다. Architecture spine은 여러 epic이 공유할
불변 결정을 고정하고, epic별 spine은 부모 `AD`를 read-only로 상속한다. Spec의 stable
capability ID와 story의 수용 기준이 각 작업의 범위를 만든다. 공식 문서는 독립 epic stream에
각 owner와 공유 artifact 갱신 조정이 필요하다. 검토 결과는 파일에 쓰고 parent에는 요약만
돌려주는 방식으로 문맥 비용을 제한한다.

## 사내 얇은 양식에 참고할 점과 한계

가져올 핵심은 다섯 필드 spec 커널, 명시적 non-goal, ID가 있는 검증 가능한 capability,
계약과 배경 자료의 분리, 큰 변경의 영향 제안과 승인, 병렬 구현 전에 공유 결정만 기록하는
architecture spine이다. 사내 소규모 변경이라면 brief→PRD→spec→architecture→epic을 모두
거칠 이유가 없다. 기존 issue에 Why, capability/success, constraint, non-goal만 추가하고,
충돌 가능성이 실제로 있을 때만 얇은 architecture 결정표와 task 분할을 붙이는 편이 낫다.

반대로 BMAD 전체를 도입하면 skill 설치, 설정 병합, memlog 스크립트, artifact workspace,
여러 reviewer, sprint tracking 같은 운영 표면이 생긴다. 이는 조직형 다중 epic에는 유용한
구조일 수 있지만, 작은 내부 팀의 한 장짜리 명세에는 도구 비용이 더 클 수 있다. 이 조사는
문서 구조와 공개 지침을 분석했을 뿐, workflow를 실행하거나 생산성·품질 효과를 실험하지
않았다. 원문의 강한 품질·비용 주장은 검증된 효과로 취급하지 않는다.

## 보관 자료

- 상류 고정 링크: [현재 spec skill](https://github.com/bmad-code-org/BMAD-METHOD/blob/abe4eb1bce919c9d22cd18b3519353d5824c4b75/skills/bmad-spec/SKILL.md), [현재 PRD 양식](https://github.com/bmad-code-org/BMAD-METHOD/blob/abe4eb1bce919c9d22cd18b3519353d5824c4b75/skills/bmad-prd/assets/prd-template.md), [course correction](https://github.com/bmad-code-org/BMAD-METHOD/blob/abe4eb1bce919c9d22cd18b3519353d5824c4b75/skills/bmad-correct-course/SKILL.md)
- 원본 개요와 판 설명: [upstream README](evidence/upstream-README.md)
- 계획 경로: [planning path](evidence/choose-a-planning-path.md), [requirements/spec](evidence/define-requirements-and-specification.md), [UX/architecture](evidence/design-ux-and-architecture.md)
- 분할과 검토: [stories/tracking](evidence/break-work-into-stories-and-track-it.md), [change review](evidence/review-a-change.md)
- 원본 실행 지침: [PRD](evidence/prd-SKILL.md), [spec](evidence/spec-SKILL.md), [architecture](evidence/architecture-SKILL.md), [epics/stories](evidence/create-epics-and-stories-SKILL.md), [course correction](evidence/correct-course-SKILL.md)
