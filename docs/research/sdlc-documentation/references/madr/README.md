# Markdown Architectural Decision Records

MADR는 중요한 아키텍처 결정을 기록하는 양식이다. 전체 요구사항과 구현 계획을 대체하는
SDD 프레임워크는 아니며, 어떤 상황에서 무엇을 선택했고 왜 선택했는지를 남기는 참고자료다.
이 조사는 조회 시 최신 공개 릴리스인 4.0.0의 커밋
`2475fe1973f66a12aaf58a91d8fa7b42c0f5ea3d`로 원본을 고정했다.[^1]

## 네 가지 배포 양식

| 파일 | 내용 | 설명 문구 |
|---|---|---|
| [adr-template.md](templates/adr-template.md) | 전체 항목 | 있음 |
| [adr-template-minimal.md](templates/adr-template-minimal.md) | 필수 항목 중심 | 있음 |
| [adr-template-bare.md](templates/adr-template-bare.md) | 전체 항목 | 없음 |
| [adr-template-bare-minimal.md](templates/adr-template-bare-minimal.md) | 필수 항목 중심 | 없음 |

공식 자료가 최소형을 별도로 제공한다는 점이 유용하다. 문서 구조가 자세할수록 항상 우수하다는
가정 없이, 기록해야 할 핵심과 설명을 위한 보조 항목을 구별할 수 있다.[^2]

## 판단의 핵심

기본 내용은 맥락과 문제, 고려한 선택지, 결정과 이유다. 전체 양식에는 결정 요인, 결과의
장단점, 선택지 비교, 확인 방법, 추가 정보가 있다. 상태·날짜·결정 참여자 등의 메타데이터도
선택 가능하다고 표시한다. 확인 방법은 결정과 구현이 일치하는지 리뷰나 테스트로 살피는
자리이며, 양식의 존재가 그 검증을 실행해주지는 않는다.[^3]

우리 spec에 대한 해석은 실제로 중요한 선택이 있었을 때 그 이유와 감수한 단점을 남기자는
것이다. 단순한 기존 패턴 적용에 의미 없는 대안 세 개를 만들거나, 파일 하나를 더 만들기 위해
형식적인 결정을 기록할 필요는 없다. 독립된 결정 기록이 장기적으로 재사용될 때만 별도 ADR을
고려하고, 작은 기능은 기존 spec의 Design에서 충분히 설명할 수 있다.

## 문서 수명과 다른 산출물의 관계

양식은 제안·수용·폐기·대체 등의 상태를 표현할 수 있다. 이는 현재 작업의 진행률과 다르다.
어떤 구조를 선택했다는 판단이 승인됐어도 구현이 완료됐다는 뜻은 아니다. 과거 결정이 왜
바뀌었는지 추적하는 필요와 현재 코드에 맞춰 실행 계획을 갱신하는 필요도 구분한다.[^3]

| 목적 | 적절한 기록 |
|---|---|
| 요청자가 바라는 변화와 제약 | intent |
| 이번 변경의 동작과 설계 | spec |
| 변경 파일·실행 순서·검증 | plan |
| 여러 변경에 걸쳐 유지할 중요한 설계 선택 | 필요한 경우 결정 기록 또는 기존 spec의 명확한 참조 |

MADR만으로 사용자의 문제, 모든 요구사항, 구현 작업과 수용 기준이 자동으로 정리되지는 않는다.
문서 종류를 하나 더 추가하기 전에 기존 기록에서 그 결정을 찾을 수 있는지 확인하는 것이
우리 팀의 얇은 운영 원칙에 맞다.

## 실제 예시와 이용 조건

[MADR 자체를 선택한 결정 기록](evidence/0000-use-madr.md)을 원본 사례로 보관했다. 양식 선택도
기록할 수 있음을 보여주지만, 이것을 독립 제품의 실사용 성과나 구현 추적 사례로 세지는 않는다.
저장소는 MIT 또는 CC0-1.0 중 선택 가능한 이중 라이선스를 명시한다. 원본 파일과
[LICENSE](licenses/LICENSE), [MIT](licenses/LICENSE.MIT), [CC0](licenses/LICENSE.CC0-1.0)를 함께 보관했다.[^1]

## 적용 판단

최소형과 설명형을 구별하는 방식, 선택 이유와 결과를 짧게 남기는 방식은 참고 우선순위가 높다.
다만 모든 기능마다 ADR 작성·승인을 필수화하거나 별도의 상태 관리 체계를 기본 템플릿에
추가하는 것은 권하지 않는다. 우리에게 필요한 것은 중요한 판단의 추적이지 문서 종류의 증가가 아니다.

## Sources

[^1]: MADR contributors, [MADR 4.0.0](https://github.com/adr/madr/releases/tag/4.0.0), 2024-09-17 릴리스, 2026-09-11 확인.
[^2]: MADR contributors, [Template README](https://github.com/adr/madr/blob/2475fe1973f66a12aaf58a91d8fa7b42c0f5ea3d/template/README.md).
[^3]: MADR contributors, [Full ADR template](https://github.com/adr/madr/blob/2475fe1973f66a12aaf58a91d8fa7b42c0f5ea3d/template/adr-template.md).

[원본 출처·판·해시](sources.json).
