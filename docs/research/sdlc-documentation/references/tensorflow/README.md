# TensorFlow RFC

TensorFlow RFC는 요구와 해결 방안을 제안하고, 사용자 가치와 생태계 영향을 검토하기 위한
설계 문서다. 양식만 보아서는 많은 항목을 채우는 절차처럼 보일 수 있지만, 실제 자료는 왜
그 선택을 하는지와 다른 부분에 어떤 영향을 줄지를 설명하는 데 무게를 둔다.[^1]

이 자료는 2025-07-10 보관 처리된 `tensorflow/community`의 마지막 master 판
`185530183d8f3734795beb520d02b8265c230a12`에서 수집했다. 이를 현재 TensorFlow 또는 Google
전체의 최신 공통 개발 절차로 표시하지 않는다.

## 양식의 구조

| 부분 | 검토하려는 내용 |
|---|---|
| 목적·동기·사용자 효익 | 해결할 문제, 목표·비목표, 근거, 사용자의 이익 |
| 설계 제안·대안 | 선택한 방법과 다른 방법을 배제한 이유 |
| 성능·의존성·개발 영향 | 실행·빌드·테스트 비용, 유지보수와 주변 프로젝트 영향 |
| 플랫폼·호환성 | 지원 환경과 기존 생태계의 계약 |
| 사용 예시·사용자 영향 | 실제 작업 흐름과 도입 후 변화 |
| 상세 설계·질문 | 필요한 깊이의 추가 설명과 검토받을 미해결 사항 |

`Objective`는 요약이지만 설계 본문도 짧게 쓰라는 지시는 아니다. `Detailed Design`은 복잡한
세부를 분리하는 선택 항목이며, 중심인 설계 제안까지 선택 사항이라는 뜻도 아니다. 하위 검토
항목은 고려하거나 비적용 이유를 설명하도록 한다.[^2]

## 사용 예시와 설계 검증

API 변경은 최종 사용자의 관점에서 처음부터 끝까지 이용하는 예시를 요구한다. 설계 시점에는
예제 코드가 실행되지 않아도 되지만, 기능 병합 전에는 동작하기를 기대한다. 변경 지점과 멀리
떨어진 부분의 영향을 발견하기 위한 목적도 명시한다.[^2]

우리 팀에 대한 해석은 대표 사용 예시를 spec의 수용 기준과 plan의 검증으로 연결하는 것이다.
예를 들어 사내 신청 목록을 조회한다면, 본인의 신청이 보이는 경우뿐 아니라 권한이 없는 경우와
조회할 항목이 없는 경우도 필요한 만큼 명확히 한다. 양식에 장식적인 예제를 붙이는 것과 구분된다.

## 실제 승인 문서 두 편

[oneDNN 기본 활성화 RFC](evidence/20210930-enable-onednn-ops.md)는 기존 선택 기능의 기본값을
바꾸는 제안이다. 기본 활성화와 비활성화 수단, 성능 저하 가능성, 수치 오차, 테스트와 유지보수를
함께 설명한다. 별도의 상세 설계 절 없이 본문에 필요한 내용을 담고 알려진 제약을 추가했다.
좁은 코드 변경도 넓은 사용자 영향을 가질 수 있음을 보여준다.[^3]

[분산 tf.data 서비스 RFC](evidence/20200113-tf-data-service.md)는 새 분산 시스템이므로 배치
구조, 사용자 흐름, Python API, C++ 인터페이스와 통신 모델까지 확장된다. 부하 분산과 결정성
사이의 선택, 비적용 환경의 이유, 논의 후 결정도 남는다. 두 문서 모두 `Accepted` 상태이며,
이 상태를 현재 제품 구현 완료의 증거로 바꾸어 읽지 않는다.[^4]

문서 분량은 코드 줄 수보다 설명해야 할 결정의 수와 영향 범위에 맞춰야 한다는 것이 이 두
사례에 대한 분석이다. 모든 변경에 대규모 시스템 수준의 목차를 강제할 근거는 아니다.

## 양식 밖의 검토 기준

[설계 검토 기준](evidence/design-review-criteria.md)은 성능·범위·유연성·통합·유지보수·사용자
집단을 묻고, 특정 하위 시스템의 고려사항은 따로 구분한다. 새 기능이 TensorFlow 본체에 들어갈
필요가 있는지, 누가 유지보수할지까지 검토한다. 이 기준의 높은 통합 부담은 여러 하드웨어와
라이브러리를 연결하는 플랫폼의 특성을 반영한다.[^5]

우리 템플릿 프로젝트에서도 보완점을 발견할 때 기본 템플릿, 선택 팀 스킬, 개별 프로젝트의 설계
중 어디에 둘지 판단하는 데 이 질문을 활용할 수 있다. 기능을 만드는 방법만큼 기본 영역을
불필요하게 키우지 않는 판단이 중요하다.

## AI-native 흐름과의 관계

RFC 전체는 우리 spec 하나와 일대일 대응하지 않는다. 배경은 intent, 결정된 동작과 설계는 spec,
실행 순서와 검증은 plan에 걸친다. TensorFlow 양식에는 요구사항 목록·항목별 수용 기준·파일별
구현 순서가 독립된 기본 절로 정해져 있지 않으므로, RFC를 채웠다는 사실만으로 구현 입력이
완비됐다고 판단할 수 없다.[^2]

공식 절차의 후원자·최소 2주 의견 수렴·검토위원회는 대형 공개 커뮤니티의 운영 방식이다.
승인은 구현을 약속하지 않으며 실제 구현은 코드 리뷰를 거친다. 이 절차를 우리 사내 개발의
기본값으로 이식할 이유는 없지만, 검토된 설계와 실제 전달 완료를 구별하는 원칙은 유용하다.[^1]

## 적용 판단

선택의 근거, 대표 사용 예시, 기존 연동 영향은 높은 우선순위의 참고 요소다. 기존 Design·
Acceptance criteria·Proof에 필요할 때 포함할 수 있다. 전 항목 의무화, 플랫폼 전용 호환성
질문, 일정이 고정된 위원회 절차는 채택하지 않는다. 원본 양식을 그대로 설치할 도구가 아니라
설계의 충분성을 판단하는 참고자료로 사용한다.

## Sources

[^1]: TensorFlow community, [RFC process](https://github.com/tensorflow/community/blob/185530183d8f3734795beb520d02b8265c230a12/governance/TF-RFCs.md).
[^2]: TensorFlow community, [RFC template](https://github.com/tensorflow/community/blob/185530183d8f3734795beb520d02b8265c230a12/rfcs/yyyymmdd-rfc-template.md).
[^3]: TensorFlow community, [Enabling oneDNN operations for x86 CPUs](https://github.com/tensorflow/community/blob/185530183d8f3734795beb520d02b8265c230a12/rfcs/20210930-enable-onednn-ops.md), 2021.
[^4]: TensorFlow community, [Distributed tf.data service](https://github.com/tensorflow/community/blob/185530183d8f3734795beb520d02b8265c230a12/rfcs/20200113-tf-data-service.md), 2020년 RFC. 메타데이터의 Updated 연도는 문서에 적힌 값을 보존하며 제출 연도와 동일하다고 가정하지 않는다.
[^5]: TensorFlow community, [Design review criteria](https://github.com/tensorflow/community/blob/185530183d8f3734795beb520d02b8265c230a12/governance/design-reviews.md).

[원본 양식](templates/rfc-template.md) · [출처·판·해시](sources.json) · [Apache-2.0 LICENSE](licenses/LICENSE).
