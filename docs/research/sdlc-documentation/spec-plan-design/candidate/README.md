# spec·plan 상세화 설계 후보

검토용 초안. 활성 templates·작성 스킬·팀 플러그인·정책을 교체하거나 설치한 결과가 아니다.
기본 여섯/네 정보 역할은 유지하고 실제 답을 채울 양식, 조건부 설계, TDD 실행 방법으로 보강한다.
2026-09-11 재검토 개정: 설명·대표 흐름·정확한 계약을 잇는 spec, PR 아래 작업을 따라 읽는 plan,
다문서 정책 검토와 사내 웹 예시를 반영했다. 근거/리뷰는 [후속 보완 기록](../../spec-plan-reassessment/implementation/README.md)에 있다.

## 양식과 작성법
- [spec 양식](templates/spec.md): 요구·관측 기대·구조/계약·설계 정본 목록·질문/우려.
- [plan 양식](templates/plan.md): 실제 파일·선행 시험/작업·PR/통합·위험·증명.
- [설계 블록](guidance/design-blocks.md), [실행/갱신 블록](guidance/execution-blocks.md).
- 작성 스킬 초안: [design-spec](skills/design-spec/SKILL.md), [plan](skills/plan/SKILL.md).
- [TDD 자체 스킬](skills/tdd/SKILL.md), [정책·검토 문장 및 설치/전달 초안](policy-and-delivery.md).
- 팀 정책 검토의 수정본: [spec-policy-pass](skills/spec-policy-pass/SKILL.md), [spec-policy 명령](commands/spec-policy.md).

## 연결된 완성 예시
| 사례 | 설계 | 실행 계획 | 보여주는 차이 |
|---|---|---|---|
| 작은 기능 F01 | [spec](examples/F01/spec.md) | [plan](examples/F01/plan.md) | 단일 문서, 정확한 작은 계약, 한 PR·행동 시험 선행 |
| 버그 B01 | [spec](examples/B01/spec.md) | [plan](examples/B01/plan.md) | 실제 제어문자 재현·시험 커밋 후 보호된 수정 |
| 단계 공개 F03 | [spec](examples/F03/spec.md) | [plan](examples/F03/plan.md) | 두 PR·한 공개 단위, 일반/시험 상태·설정 공개·제거 |
| 이행 M01 | [spec 진입점](examples/M01/spec.md) | [plan](examples/M01/plan.md) | 다중 설계 문서·API/스키마/동시성/배포·병렬/운영 인계 |
| 사내 웹 W01 | [spec](examples/W01/spec.md) | [plan](examples/W01/plan.md) | 화면→서버 세션/권한→본인 데이터, 오류·재시도·두 PR와 한 공개 단위 |

F01/B01은 작은 변경의 짧은 형태다. 여러 책임의 설명은 M01, 화면과 API의 사용자 흐름은 W01,
공개 단계에 따라 달라지는 시험은 F03에서 선택해 읽는다. 모든 사례의 항목을 합친 문서를 만들 필요는 없다.

예시의 intent/context는 각 폴더에 있다. Upstream은 실제 제작 입력 커밋이지만 제품 수락이 아니다.
예정 시험·명령은 실행 성공이 아니며 실제 존재하는 baseline과 새로 만들 예정인 파일을 구별한다.
[구현 중 변경 walkthrough](change-walkthrough.md)는 관련 정본·구현의 동시 갱신 범위를 설명한다.

작성 깊이는 중요한 결정을 다음 사람에게 다시 떠넘기지 않는 수준이다. 모든 클래스/다이어그램,
완전한 내부 구현, 모든 RGR 원장이나 새로운 의미 검사기는 요구하지 않는다.
