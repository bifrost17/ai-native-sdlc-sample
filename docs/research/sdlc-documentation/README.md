# AI-native SDLC 문서·양식 리서치

Anthropic AI-Native SDLC Playbook을 기준으로 **12개 레퍼런스와 실제 적용 사례 2건**을 조사했다.
공식 저장소에서 배포한 **원본 양식 28개**와 관련 작성·갱신·검토 지침을 함께 보관했다.
조사일은 2026-09-11이며 판·출처·이용 조건·파일 해시는 [sources.json](sources.json)에 있다.

조사의 목적은 플레이북의 취지에 맞는 **우리 intent·spec·plan 양식의 설계 근거**를 확보하는 것이다.
흐름 유지는 이미 정해진 전제다. 문서별 출발점을 고르고 대표 개발 건의 완성 예시를 먼저 쓴 뒤,
공통 핵심과 상황별 상세를 갖춘 양식을 도출하는 접근을 추천한다.
[설계 방법 비교와 추천](design-approaches.md)에 구체적인 조합과 실행 순서를 정리했다.

## 읽는 순서

1. [설계 방법 비교와 추천](design-approaches.md): 우리 양식을 만드는 여덟 가지 접근과 권하는 조합.
2. [종합 보고서](report.md): 북극성 해석, intent와 요구사항의 차이, 한 파일의 의미, 적용 우선순위.
3. [비교표](comparison.md): 문서 역할·크기·갱신·사람/에이전트 역할·도구 의존성.
4. 아래 레퍼런스 분석과 원본 양식: 필요한 항목의 원래 취지와 필수성을 확인.
5. [실제 적용 사례](case-studies/README.md): 작성된 문서와 구현·리뷰·검증·명세 반영의 연결 및 한계.
6. [후보 선정 기록](candidates.md), [조사 계획과 완료 기록](plan.md), [자료·저장소 검증](verification.md).

## 레퍼런스와 바로 열어볼 원본

| 레퍼런스 분석 | 공식 배포 양식 또는 보관 자료 | 판과 자료 성격 |
|---|---|---|
| [Anthropic Playbook](references/anthropic-playbook/README.md) | [intent 예시](references/anthropic-playbook/evidence/intent-example.md), [plan 예시](references/anthropic-playbook/evidence/plan-example.md) | 기존 북극성에서 예시 추출 + 공식 문서 대조. 고정 spec 빈 양식 아님 |
| [Google 공개 지침](references/google-engineering/README.md) | [큰 문서 구성 지침](references/google-engineering/evidence/organizing-large-documents.html) | Google 공통 빈 양식 미확보; 책과 작성 지침 분석 |
| [Fuchsia RFC](references/fuchsia/README.md) | [RFC](references/fuchsia/templates/rfc-template.md) | main `a433f339…`; 양식 1개 |
| [TensorFlow RFC](references/tensorflow/README.md) | [RFC](references/tensorflow/templates/rfc-template.md) | master `18553018…`, 보관 저장소; 양식 1개 + 실제 RFC 2개 |
| [GitHub Spec Kit](references/github-spec-kit/README.md) | [constitution](references/github-spec-kit/templates/constitution-template.md), [spec](references/github-spec-kit/templates/spec-template.md), [plan](references/github-spec-kit/templates/plan-template.md), [tasks](references/github-spec-kit/templates/tasks-template.md) | main `c173bf19…`, 개발 스냅샷; 양식 4개 |
| [OpenSpec](references/openspec/README.md) | [proposal](references/openspec/templates/proposal.md), [spec](references/openspec/templates/spec.md), [design](references/openspec/templates/design.md), [tasks](references/openspec/templates/tasks.md) | `9d4e5974…`, v1.13.0과 동일; 양식 4개 |
| [Kiro Specs](references/kiro/README.md) | [EARS 짧은 패턴](references/kiro/evidence/ears-pattern.txt), 공식 문서 링크 | 독립 배포 빈 양식 미확보; 전체 requirements 양식으로 표시하지 않음 |
| [BMAD](references/bmad/README.md) | [brief](references/bmad/templates/product-brief-template.md), [PRD](references/bmad/templates/prd-template.md), [spec](references/bmad/templates/spec-template.md), [architecture](references/bmad/templates/architecture-spine-template.md), [epics/stories](references/bmad/templates/epics-and-stories-template.md) | main `abe4eb1b…`, 개발 스냅샷; 양식 5개 |
| [GSD](references/gsd/README.md) | [project](references/gsd/templates/project.md), [requirements](references/gsd/templates/requirements.md), [roadmap](references/gsd/templates/roadmap.md), [state](references/gsd/templates/state.md), [phase spec](references/gsd/templates/spec.md) | main `bdcaab2c…`, 기존 저장소 보관됨; 양식 5개. 후속 GSD Core는 별도 링크 확인 |
| [Spec Kitty](references/spec-kitty/README.md) | [spec](references/spec-kitty/templates/spec-template.md), [plan](references/spec-kitty/templates/plan-template.md), [tasks](references/spec-kitty/templates/tasks-template.md), [WP](references/spec-kitty/templates/task-prompt-template.md) | main `d96d0209…`, 개발 스냅샷; 양식 4개 |
| [Superpowers](references/superpowers/README.md) | [brainstorming](references/superpowers/evidence/brainstorming-SKILL.md), [writing plans](references/superpowers/evidence/writing-plans-SKILL.md) | main `b36e0829…`; 별도 빈 spec/plan 없이 skill 내부 작성 지침 |
| [MADR](references/madr/README.md) | [full](references/madr/templates/adr-template.md), [minimal](references/madr/templates/adr-template-minimal.md), [bare](references/madr/templates/adr-template-bare.md), [bare minimal](references/madr/templates/adr-template-bare-minimal.md) | 4.0.0 `2475fe19…`; 양식 4개 |

최신 릴리스와 main 스냅샷을 구별했다. 보관된 역사 자료도 유용한 작성 원칙의 참고 대상으로
포함했으며, 해당 프로젝트의 현재 운영 방식이라고 일반화하지 않는다.

## 자료를 구분하는 방법

- `references/<name>/README.md`: 우리 분석. 원문 사실, 해석, 적용 권고와 한계를 구분한다.
- `templates/`: 상류에서 배포한 빈 양식을 원본 바이트로 보관한다. 수정하거나 번역하지 않았다.
- `evidence/`: 작성·검토 지침, 실제 예시, 그림, 프롬프트, 제한된 발췌와 출처 메타데이터.
  전체 원문·발췌·가공된 API 사실은 manifest의 `kind`와 `notes`로 구분한다.
- `case-studies/<name>/artifacts/`: 실제 변경에서 채워진 문서. 빈 양식 수에 포함하지 않는다.
- `licenses/`: 관련 원문 이용 조건. API의 자동 라이선스 판정보다 직접 확인한 파일 설명을 따른다.

Anthropic의 추출 예시는 기존 저장소 자료의 출처를 유지한 것이며 독립적인 오픈소스 양식으로
표시하지 않는다. Kiro 전체 문서와 Google 책은 링크와 분석 중심으로 보관했다. 별도 공개 빈
양식을 확보하지 못한 자료를 임의로 재구성하여 공식 원본이라고 부르지 않는다.

원문 Markdown의 상대 링크와 예시 placeholder는 수정하지 않았다. 일부는 상류 저장소 전체가
있어야 열리므로 해당 항목의 `browse_url` 또는 `source_url`에서 원래 맥락을 확인한다.
우리 분석 문서의 로컬 링크는 별도로 검사했다. 전체 프레임워크 저장소를 복제한 자료집은 아니다.

이 폴더는 연구 결과와 참고 원문이다. 원문에 포함된 명령·skill·agent prompt는 **설치나 실행을
위한 이 프로젝트의 지침이 아니다.** 이번 작업은 운영 템플릿·정책·스킬과 북극성 평가 주석을
수정하지 않았으며, 후속 반영 후보와 근거를 제공한다.
