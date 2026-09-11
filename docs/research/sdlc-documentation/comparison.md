# 문서 역할·갱신·운영 부담 비교

조사일: 2026-09-11. 아래 표는 [종합 보고서](report.md)의 요약이며, 각 이름은 상세 분석과
공식 원문으로 연결된다. 필요성은 조사한 판과 선택 경로에 한정된다. 체크박스나 검토 프롬프트의
존재를 실행 성공으로 표시하지 않으며, 서로 다른 목적의 자료를 점수로 순위화하지 않는다.

## 1. 전체 비교

| 레퍼런스 | 주된 목적·핵심 산출물 | 크기와 필요성 | 갱신·수명 | 실행 의존성 / 우리에게 참고할 부분 |
|---|---|---|---|---|
| [Anthropic Playbook](references/anthropic-playbook/README.md) | intent → 요구·설계 spec → 구현 plan; 공통 기록으로 인계 | spec 고정 목차·분량은 제시하지 않음 | 계획 이탈은 해당 변경과 같은 커밋에 plan 반영 | 방법론과 조직 스킬·도구를 함께 사용; 우리 기준 |
| [Google 공개 지침](references/google-engineering/README.md) | 설계 협업과 독자가 찾을 수 있는 문서 구조 | 한 문서·연결된 여러 문서 모두 가능; 공통 빈 양식 미확보 | 팀별 관행; 단일 갱신 규칙으로 일반화 불가 | 문서 구조 원칙은 제품 비종속; 중요한 판단부터 설명 |
| [Fuchsia RFC](references/fuchsia/README.md) | 설계 수용과 이해관계자 합의 | 승인에 중요한 상세; 모든 구현 세부는 불필요 | 승인된 RFC는 당시 결정의 역사; 기능 문서는 별도 | 프로젝트 거버넌스; 결정·예시 구별, 문서 밖 합의 반영 |
| [TensorFlow RFC](references/tensorflow/README.md) | 사용자 가치·대안·생태계 영향 | 핵심 설계 본문과 선택 상세 설계; 해당 항목을 고려하거나 비적용 설명 | RFC 승인과 구현 완료 구별; community 저장소 보관됨 | 공개 커뮤니티 절차; 사용 예시와 영향·유지보수 판단 |
| [GitHub Spec Kit](references/github-spec-kit/README.md) | constitution, spec, 기술 plan, tasks | 기능 흐름과 선택 clarify; research/contracts 등 상황별 | flow-forward/living/flow-back 중 팀이 선택; analyze 읽기 전용 | CLI·명령·확장 hook; 요구/성공 기준과 작업 연결 |
| [OpenSpec](references/openspec/README.md) | proposal, behavior delta, design, tasks | 빠른 경로/세부 경로; 스키마는 의존 그래프 | 진행 변경과 main spec 분리; sync와 archive 별개 | CLI schema/status와 agent skill; 변경분·현재 계약 구별 |
| [Kiro Specs](references/kiro/README.md) | requirements 또는 bugfix, design, tasks | 기능·버그·Quick; 요구/설계 우선 가능 | 변경 뒤 설계 재검토·tasks 동기화 요청 | 제품 내 흐름; 조건-동작과 유지할 회귀 경계 |
| [BMAD](references/bmad/README.md) | 작은 spec 계약 또는 brief/PRD/architecture/stories | 크기·불확실성·공유 합의 필요에 따라 선택 | memlog에서 계약 재작성, companion 구별, course correction | skill·스크립트·workspace·tracking; 작은 계약과 중요한 공유 결정 |
| [GSD](references/gsd/README.md) | PROJECT/REQUIREMENTS/ROADMAP/STATE와 phase PLAN | phase SPEC 선택, phase/plan으로 큰 작업 분해 | 현재 맥락·진행·검증을 파일로 갱신; 조사한 기존 저장소 보관됨 | command·agent·worktree·검토 loop; 재개 맥락과 공유 상태 작성 책임 |
| [Spec Kitty](references/spec-kitty/README.md) | spec/plan/tasks, WP별 prompt·review 상태 | mission core와 optional 자료; tiny change에는 무거움 | WP lane·event 상태와 Git; 일반 living/archive 규칙 미확인 | CLI·runtime gate·worktree·외부 CI; 요구→WP→소유 파일과 리뷰 |
| [Superpowers](references/superpowers/README.md) | 대화 설계, 상세 spec/design·plan, task 검토 | spike/bounded/architectural; bounded는 별도 spec·plan 없음 | 승인 설계, 실행 ledger·Git; 일반 spec 변경 원장 없음 | skill 묶음; task별 문맥과 독립 검토, 작은 변경의 깊이 조절 |
| [MADR](references/madr/README.md) | 중요한 결정의 맥락·대안·이유 | full/minimal 및 설명 없는 bare 제공; 전체 SDD 아님 | 제안·수용·대체 등 결정 상태, 진행률과 다름 | 단순 Markdown 사용 가능; 의미 있는 선택만 짧게 기록 |

OpenSpec에서 design을 상황별로 작성한다는 지침과 tasks가 specs/design을 요구하는 기본 그래프의
결합은 정적 조사로 완전히 해명하지 못했다. “모든 design은 자유롭게 생략 가능”으로 읽지 않는다.
Spec Kitty의 테스트 관련 지침은 개발 스냅샷 안에서도 표현이 달라 운영 채택 시 재확인이 필요하다.

## 2. 파일명 대응보다 역할 대응

등호가 아니라 기능이 겹치는 범위를 나타낸다. RFC 한 파일이 아래 여러 역할을 담을 수 있으며
목차가 없다고 내용도 없다고 판단하지 않는다.

| 역할 | Anthropic / 우리 기준 | 가까운 다른 표현 | 주의 |
|---|---|---|---|
| 요청자의 문제·이유·기대·제약 | intent | BMAD brief/Why, GSD PROJECT, proposal의 동기 | 정제된 요구사항을 요청자의 원래 의도와 동일시하지 않음 |
| 검토된 행동 계약·수용 기준 | spec의 요구·AC | Spec Kit spec, OpenSpec spec delta, Kiro requirements/bugfix, BMAD capability | intent의 미해결 문제를 임의 가정으로 덮지 않음 |
| 기술 선택·인터페이스·영향 | spec의 Design | Spec Kit plan, Kiro/OpenSpec design, RFC, architecture spine | Spec Kit plan은 우리 실행 plan과 정확히 같지 않음 |
| 실행 순서·파일·검증 | plan | tasks, GSD PLAN, Spec Kitty WP, Superpowers plan | 단순 체크리스트만으로 파일·의존·검증이 충분하다고 단정하지 않음 |
| 현재 작업 상태·재개 맥락 | 필요한 진행 기록 | GSD STATE, WP lane, progress ledger | 단기 진행 상태를 제품 요구의 기준으로 만들지 않음 |
| 현재 제품이 제공하는 계약 | 팀이 선택할 지속 명세 | OpenSpec main specs, living spec | 완료 변경 문서가 항상 현재 전체 계약은 아님 |
| 당시 결정의 근거 | Git 이력, 필요한 결정 기록 | RFC, ADR, archive | 수용 상태가 구현 완료·테스트 성공을 뜻하지 않음 |

## 3. 사람과 에이전트의 역할·검증 연결

| 방법 | 사람이 결정하는 주요 지점 | 에이전트가 수행하는 주요 작업 | 검증에 대한 한계 |
|---|---|---|---|
| Anthropic | 요청 정정, intent/spec/plan 판단, 충돌 해결 | 작성·관련 스킬 적용·구현·검토 | 산출물 사슬이 에이전트의 실수를 제거하지 않음 |
| Spec Kit | 중요 모호성 응답, 체크리스트/수정 판단 | 명세·설계·작업 생성, 정적 analyze, implement | analyze가 파일을 자동 수정하거나 테스트 통과를 보장하지 않음 |
| OpenSpec | 계획/코드 검토, update와 archive 선택 | 산출물 생성·apply·verify·semantic sync | verify 휴리스틱·형식 validate와 실제 테스트를 구별 |
| Kiro | 질문 응답, 문서 수정·재검토와 작업 요청 | 요구/설계/작업 생성·구현 | 공식 제품 설명 조사이며 생성 품질·동기화 실행 미검증 |
| BMAD | 제품 판단, 중요한 가정·설계·course correction | 입력 보존, 계약 갱신, 작업 분해, 검토 | 기록과 검토 절차의 존재는 품질 효과의 실증이 아님 |
| GSD | 초기 경로·granularity, 중요한 checkpoint, UAT | 전문 agent 계획·wave 실행·상태·검증 갱신 | 여러 verifier와 gate의 효과·runtime은 실행 미검증 |
| Spec Kitty | 의도·설계·AC, accept/reject/merge 모델 | WP 구현·review·상태 인계 | 파일 gate·runtime·외부 CI가 서로 다름 |
| Superpowers | 경로별 설계 승인과 중요한 재판단 | 계획, task 구현, 자체/독립 검토 | 파일에 reviewer prompt가 있어도 매번 별도 reviewer를 호출하는 것은 아님 |

Google·Fuchsia·TensorFlow·MADR는 이 조사에서 에이전트 실행 프레임워크로 분류하지 않았다.
해당 문서의 사람 역할은 설계 작성·검토·결정의 맥락이며 AI 실행 역할을 추정해 채우지 않았다.

## 4. 우리 양식에 가져올 정도

| 상황 | 충분한 기록의 예 | 조건부로 더할 내용 |
|---|---|---|
| 기존 동작의 작은 변경 | 문제·기대 결과, 바뀔 동작/유지할 동작, 영향 파일, 검증 | 새 결정이 있을 때 이유·단점 |
| 결함 수정 | 재현 조건, 기대 동작, 회귀 경계, 테스트 방법 | 데이터 보존·복구가 중요하면 실패 상태와 이행 절차 |
| 새 기능 | 사용자 예시·AC, 기존 구조와 연결, 주요 계약, 실행·PR 분할 | 불확실한 설계 대안, UX/API 상세 |
| 여러 모듈·병렬 작업 | 공유 목표·인터페이스, 작업 의존·소유 경계, 통합 검증 | 별도 상세 문서·WP, 공용 기록의 단일 작성 책임 |
| 장기 재사용 설계 선택 | 기존 spec에서 찾을 수 있는 이유·영향 | 여러 변경이 같은 선택을 참조하면 별도 ADR 고려 |

이는 문서 파일 개수를 새로 규정하는 표가 아니다. 기존 intent/spec/plan 안에서 필요한 깊이를
고르고, 실제로 읽기 어려워질 때만 분리하는 적용 제안이다. 현재 템플릿에 이미 있는 항목은
중복 추가하지 않는다. 자세한 이유와 후속 적용 우선순위는 [보고서](report.md)에 있다.
