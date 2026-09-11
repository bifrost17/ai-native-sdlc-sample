# 배포와 기능 공개 분리 조사

조사일: 2026-09-11. 목적은 작은 PR을 자주 통합하면서 미완성 기능을 내부에서 시험하는 얇은 팀 지침이다.
공식 문서·작성자 글·기업의 자체 사례를 읽었다. 원문 복제 대신 근거와 적용 판단을 요약한다.

## 북극성과의 관계

[북극성](../../verification/north-star-playbook.html)의 계획·구현·검증과 CI/CD/배포 절을 재독했다.
파일·순서·시험을 연결하는 계획, 변경과 함께 계획 갱신, 환경별 자율성, 사람이 수락하는 운영 전환과
복구 준비가 기준이다. 원문이 release flag를 필수라고 말한 것은 아니다. 아래 방법은 이 목적과
사용자의 미완성 기능 비공개 요구를 구현하기 위해 우리가 선택한 운영 지침이다.

## 1차 자료와 읽은 내용

| 출처 | 구분·핵심 근거 | 우리에게 주는 판단 |
|---|---|---|
| [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow) | 공식 현행 절차: 브랜치·PR·검토·통합 | 기능 공개의 시점과 대상은 별도로 정한다. 이 문서가 플래그를 의무화한다고 인용하지 않는다. |
| [DORA: Trunk-based development](https://dora.dev/capabilities/trunk-based-development/) | 연구 조직의 실천 안내: 작은 변경과 잦은 통합, 짧은 브랜치 | 공개 대기 때문에 장기 기능 브랜치를 기본으로 만들지 않는다. |
| [GitHub, How we ship with feature flags](https://github.blog/engineering/infrastructure/ship-code-faster-safer-feature-flags/) | 2021-04-27 자체 엔지니어링 사례: 직원 대상으로 미완성 기능 시험, 작은 배치, 배포 후 대상 확대/중단, 플래그 제거 | 같은 제어를 유지하고 설정을 바꾼다. 당시 사례이며 현재 GitHub 내부 구현을 확인한 것은 아니다. 규모와 자동 제거 도구까지 복제하지 않는다. |
| [Pete Hodgson, Feature Toggles](https://martinfowler.com/articles/feature-toggles.html) | 2017-10-09 개정 작성자 글: release와 deploy 분리, 수명이 다른 토글 종류, 판단과 사용 지점 분리, 운영/다음/복구 설정 시험 | 임시 공개 제어를 상시 권한과 구별하고 필요한 OFF/ON 및 상호작용만 확인한다. 모든 조합이나 거대한 프레임워크를 요구하지 않는다. |
| [OpenFeature Flag Evaluation API](https://openfeature.dev/specification/sections/flag-evaluation/) | 공식 규격 §1.3·§1.4: 호출자가 기본값을 제공하며 평가 오류 때 그 기본값 반환 | 미완성 release flag의 기본값 OFF는 우리 선택이다. 모든 종류의 플래그 OFF를 규격 의무로 오독하지 않는다. SDK 도입도 필수가 아니다. |
| [Martin Fowler, Branch By Abstraction](https://martinfowler.com/bliki/BranchByAbstraction.html) | 작성자 글: 추상화 아래 구현을 점진적으로 바꾸며 통합 유지 | 내부 교체에 적합하다. 단순 신규 기능마다 추상 계층을 만들 이유는 없다. |
| [Martin Fowler, Keystone Interface](https://martinfowler.com/bliki/KeystoneInterface.html) | 작성자 글: 기능으로 들어가는 인터페이스를 늦게 제공하는 대안 | 호출 경계가 실제로 닫혀 있고 부수 효과가 없어야 한다. 메뉴만 숨기는 것으로 서버 기능 비공개를 보장하지 않는다. |

## 선택과 비용

기본 선택은 조건부 단기 release flag다. 여러 PR이 하나의 미완성 공개 단위에 속하고 생산 배포물에
들어갈 때 쓴다. 완결된 작은 수정은 바로 기존 흐름을 따른다. 기존 설정을 쓰는 것이 사내 소규모 제품의
출발점이며, 분산 캐시·백분율 배포·SDK·제어판은 필요한 제품에서 선택한다. 설정 변경이 소스 변경을
없애도 프로세스 재시작이나 설정 배포까지 없애는 것은 아니다.

보안·데이터에 대한 적용 판단: 화면 숨김은 접근 제어가 아니다. 신뢰된 서버 대상 판정과 API/작업의
부수 효과 경계를 함께 검토해야 한다. OFF는 과거 쓰기나 비호환 migration의 복구 수단이 아니다.
이는 자료의 배포/노출 분리와 프로젝트 안전 요구를 결합한 우리의 설계 판단이다.

플래그는 분기·시험·운영 설정이라는 유지 비용을 만든다. 공개 후 안정화와 되돌림 기간을 정하고 제거한다.
설정 삭제가 OFF fallback을 되살리지 않게 코드 배포와 구버전 사용을 고려한다. 날짜·레지스트리·서비스를
일률적으로 요구하지 않고 해당 plan에 담당과 제거 조건을 남기는 것으로 시작한다.

## 반영과 검증

[사용 지침](../../RELEASE-CONTROL.md)을 기존 GitHub Flow·PR 크기·spec/plan·선택 스킬·리뷰에 연결한다.
기존 F02의 두 독립 기능은 각각 완성 후 공개할 수 있었으므로 역사 기록을 바꾸지 않는다. 새 실험은 같은
작은 데이터를 사용하되 목록+집계가 **한 공개 단위**라는 다른 입력을 명시한다. 실행 결과·독립 리뷰·전달
판정은 [독립 리뷰·전달](review-and-delivery.md)과 [실험 결과](probe/result.md)에 남겼다.
로컬 CLI 관측은 서버 권한·운영 배포 검증을 대신하지 않는다.
