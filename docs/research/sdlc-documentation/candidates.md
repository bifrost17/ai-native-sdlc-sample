# 조사 대상 선정과 추가 후보

선정 기준은 인기도가 아니라 북극성의 의도·설계·실행·피드백 흐름을 더 잘 이해하게 하는지다.
조사 범위와 방법은 [plan.md](plan.md), 비교 결과는 [report.md](report.md)에 있다.

## 상세 조사한 12개 자료

| 분류 | 대상 | 선정 이유 |
|---|---|---|
| 기준 | [Anthropic Playbook](references/anthropic-playbook/README.md) | 우리 프로젝트의 북극성. 다른 양식의 파일명과 역할을 대조하는 기준 |
| 기존 조사 보존 | [Google 공개 지침](references/google-engineering/README.md) | Google 공통 양식이라는 주장과 팀별 작성 원칙을 구분 |
| 설계 검토 | [Fuchsia](references/fuchsia/README.md), [TensorFlow](references/tensorflow/README.md) | 전통적인 설계 양식의 충분성·대안·사용 예시와 조직 절차를 분리 |
| SDD 중심 | [Spec Kit](references/github-spec-kit/README.md), [OpenSpec](references/openspec/README.md), [Kiro](references/kiro/README.md) | 요구·설계·작업 문서와 변경·유지 흐름의 차이 |
| 확장 개발 방법 | [BMAD](references/bmad/README.md), [GSD](references/gsd/README.md), [Spec Kitty](references/spec-kitty/README.md) | 규모·장기 맥락·다중 작업·검토 상태를 어떻게 추가하는지 |
| 인접 원칙 | [Superpowers](references/superpowers/README.md), [MADR](references/madr/README.md) | skill을 통한 설계·계획 실행, 그리고 최소한의 설계 결정 기록 |

Spec Kitty는 Spec Kit과 유사한 산출물 구조가 있지만 현재 공식 저장소의 WP·실행 상태·검토
체계 차이를 조사했다. 공통 구조를 서로 독립된 효과 증거로 중복 집계하지 않는다. Superpowers와 MADR도
전체 SDD 프레임워크와 같은 범주라고 단정하지 않았다.

## 구조만 확인한 추가 후보

2026-09-11 공식 개요 또는 양식의 구조만 살폈다. 다음 대상은 별도 심층 분석·원문 양식
다운로드·실제 적용 이력 추적을 완료한 12개에 포함하지 않는다. Git 후보 링크는 판을 고정했고,
출처 색인에서 `screened-candidates`, `link-only`로 표시한다.

| 후보 | 추가로 유용할 수 있는 관점 | 이번 결정 |
|---|---|---|
| [Kubernetes KEP](https://github.com/kubernetes/enhancements/blob/e3ed21fdb51d359a2e73c714257f73cf453e8ba7/keps/NNNN-kep-template/README.md) | 테스트 계획, enable/disable, rollout/rollback, 운영 준비 질문이 설계와 연결됨 | 배포·운영 위험이 높은 개발 건의 다음 참고 후보. 사내 기본 spec 조사에서는 릴리스 거버넌스까지 확장하지 않음 |
| [Rust RFC](https://github.com/rust-lang/rfcs/blob/51783df9a76c355de7ceebeae101cba47f8ca463/0000-template.md) | 사용자를 가르치는 설명과 기술 참조 수준 설명을 구분하고 같은 예시로 연결 | 사람과 에이전트의 독자 깊이를 후속 설계할 때 유용. RFC 거버넌스 추가 비교는 보류 |
| [arc42](https://arc42.org/overview/) | 목적·제약·시스템 경계·구조·실행·배포·품질·위험의 12개 영역을 필요에 맞게 조절 | 큰 시스템 설계 문서로 범위를 넓힐 때 참고. 이번 기능별 intent/spec/plan 조사에서는 개요 확인에 한정 |
| [GSD Core 후속 프로젝트](references/gsd/README.md) | 기존 GSD README가 안내한 개발 이전 목적지 | 새 저장소의 판·비보관 상태·라이선스를 별도 링크로 확인. 기존 GSD 원문과 혼합하지 않았으며 후속 workflow 심층 분석은 보류 |

KEP·Rust·arc42의 양식 구조가 우리에게 유용할 수 있다는 판단과 그 프로젝트의 절차 전체를
채택하자는 판단은 다르다. 후속 필요가 구체화되면 라이선스·릴리스·작성 지침·사례를 함께 조사한다.

## 실제 적용 사례 선정

[사례 색인](case-studies/README.md)에 선정 2건과 보류 4건의 근거를 별도로 기록했다.
독립 제품 Opentu는 작은 기능의 문서·코드 연결과 남은 누락을, OpenSpec 자체 수정은
버그 계약·리뷰 보완·CI·현재 명세 반영을 보여 준다. 두 사례가 같은 프레임워크 형식이라는
표본 한계를 유지했다. `.specify` 설정이나 `specs/` 폴더 존재만으로 적용 사례를 늘리지 않았다.
