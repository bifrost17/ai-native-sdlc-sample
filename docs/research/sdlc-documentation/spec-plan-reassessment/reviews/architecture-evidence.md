# GitLab·MediaWiki 설계 설명 방식과 현재 후보의 근거 비교

2026-09-11. 검토 범위는 GitLab HTTP Routing Service, MediaWiki AOSA 장, 현재 `spec.md`
양식·설계 블록 안내·M01 설계 패키지다. 이 문서는 구조를 전면 재설계하는 안이 아니라, 두 사례에서
확인되는 설계 커뮤니케이션의 장점을 현재 후보가 이미 갖춘 부분과 보강할 부분으로 나눈 근거 검토다.

## 먼저 구분해야 할 자료의 성격

GitLab 문서는 `status: accepted`인 Cells 라우팅 설계지만, 한 시점에 닫힌 사전 명세는 아니다
([D3 L1-L11](../../../exemplary-design-and-plans/originals/D3-gitlab-http-routing-service.md)).
초기 구조 제안, 배포 단계, 현재 규칙 세트의 점진 공개 절차가 한 문서에 누적되어 있다. 동시에
`Non-Goals`는 `Not yet defined`이고 FAQ에도 미정 답이 남아 있다
([D3 L180-L184](../../../exemplary-design-and-plans/originals/D3-gitlab-http-routing-service.md),
[L533-L537](../../../exemplary-design-and-plans/originals/D3-gitlab-http-routing-service.md)). 따라서 이 문서는
완결성의 기준이 아니라, 요구를 실제 요청·선택·운영으로 연결하는 방식의 근거로 쓴다. 조사 보고서도 이를
“사전 제안과 후속 운영 내용이 누적된 설계문서”로 한정한다
([system-designs L55-L67](../../../exemplary-design-and-plans/system-designs.md)).

MediaWiki 문서는 구현 전 승인용 spec이 아니라 역사와 당시 구조를 설명한 교육용 사후 장이다. 장 자체가
역사, 코드 관행, 저장, 요청·캐시, 언어, 사용자, 확장 순으로 시스템을 해설한다고 밝힌다
([D4 L85-L133](../../../exemplary-design-and-plans/originals/D4-mediawiki.html)). 조사 보고서 역시 2011년의
역사 자료이며 현재 아키텍처가 아니라고 한정한다
([system-designs L69-L87](../../../exemplary-design-and-plans/system-designs.md)). MediaWiki나 GitLab의
규모·인지도는 설계의 옳음을 증명하지 않는다. 여기서는 독자가 구조를 이해하도록 만드는 설명법만 비교한다.

## 비교 결과

| 설명 품질 | 현재 후보 판단 | 근거와 차이 |
|---|---|---|
| 설명적 서사 | **약함** | 양식은 첫 문단에 “핵심 변화·선택”을 요구하고 Design에 구조 표를 두지만, 현재 문제의 작동 방식에서 목표 구조까지 이어지는 짧은 설명을 명시적으로 요구하지 않는다 ([template L5-L28](../../spec-plan-design/candidate/templates/spec.md)). M01은 계약 정본과 세부 조건은 명확하지만 독자는 요구 표, 세 설계 파일, 도식을 오가며 “현재 JSON 완료 경합 → SQLite 트랜잭션 → 보고서 API 소비”라는 변화의 이야기를 재구성해야 한다 ([M01 spec L6-L20](../../spec-plan-design/candidate/examples/M01/spec.md), [L44-L52](../../spec-plan-design/candidate/examples/M01/spec.md)). |
| 대표적인 종단 간 흐름 | **부분적으로 있음** | M01 구성도는 사용자·보고서→API→facade→저장소 경계를 보여 주고, 저장 시퀀스는 두 완료의 경합과 실패를 정확히 보여 준다 ([architecture L4-L17](../../spec-plan-design/candidate/examples/M01/design/architecture.md), [storage L31-L51](../../spec-plan-design/candidate/examples/M01/design/storage.md)). 그러나 인증/권한 확인부터 facade 선택, 트랜잭션, HTTP 결과까지 요청 하나를 끝까지 잇는 대표 흐름은 없다. GitLab은 구체 URL·헤더를 넣은 두 요청을 Router→Topology Service→Cell 응답까지 추적한다 ([D3 L341-L375](../../../exemplary-design-and-plans/originals/D3-gitlab-http-routing-service.md)); MediaWiki도 실제 `view` 요청의 진입, 분기, 커밋, HTML 출력, 지연 작업까지 순서대로 설명한다 ([D4 L457-L509](../../../exemplary-design-and-plans/originals/D4-mediawiki.html)). |
| 선택과 트레이드오프 | **있지만 기각 근거의 식별력 보강 가능** | 양식의 구조 표에는 선택 이유·영향 칸이 있고, M01은 JSON 잠금 보강 대신 SQLite를 선택하며 이행·복구 도구 유지 비용을 감수한다고 명시한다 ([template L22-L28](../../spec-plan-design/candidate/templates/spec.md), [M01 spec L44-L48](../../spec-plan-design/candidate/examples/M01/spec.md)). 이는 이미 좋은 최소 형태다. 다만 “보고서 소비자와 이행/복구까지 다시 다뤄야 한다”는 기각 근거가 두 선택의 동시성·운영 차이를 독자가 즉시 구별할 만큼 구체적인지는 보강할 수 있다. GitLab은 버퍼링과 동적 학습을 메모리, 혼합 버전, Cell 가용성 의존이라는 서로 다른 비용으로 구별한다 ([D3 L447-L466](../../../exemplary-design-and-plans/originals/D3-gitlab-http-routing-service.md)). 중요한 구조 선택에는 대안이 핵심 요구를 충족하지 못하는 이유와 감수할 비용을 한두 줄 더 남기면 검토자가 선택의 경계를 판단하기 쉽다. |
| 시스템 맥락 | **구성 맥락은 강하고 제품 맥락은 부분적** | M01의 컴포넌트·배포 도식은 실행 주체, 저장 위치, 설정, 권한 경계를 명확히 한다 ([architecture L4-L17](../../spec-plan-design/candidate/examples/M01/design/architecture.md), [L50-L65](../../spec-plan-design/candidate/examples/M01/design/architecture.md)). 반면 현재/목표 상태를 시각적으로 구분하지 않아 JSON과 SQLite가 동시에 보이는 그림의 의미를 본문에서 확인해야 한다. GitLab은 먼저 단일 도메인이라는 사용자 목표와 세 실제 URL의 라우팅 기대를 제시한 뒤 기술 목표로 들어간다 ([D3 L13-L58](../../../exemplary-design-and-plans/originals/D3-gitlab-http-routing-service.md)). MediaWiki는 비용·공동 편집·오픈 플랫폼이라는 제품 조건이 성능, 캐시, 권한 구조를 어떻게 만들었는지 먼저 설명한다 ([D4 L45-L83](../../../exemplary-design-and-plans/originals/D4-mediawiki.html)). 작은 변경에 이런 역사 서술은 필요 없지만, 여러 구성 요소를 바꾸는 M01급 예시에는 사용자/운영 문제와 구조 선택을 연결하는 짧은 맥락이 유용하다. |
| 운영 상태와 실패 조건 | **강함** | M01 operations는 이행 전제, 중지, import 실패, 전환 뒤 쓰기 유무, export 실패, 재개 조건을 표와 문장으로 구분하며 “코드 머지=운영 성공”도 부정한다 ([operations L4-L20](../../spec-plan-design/candidate/examples/M01/design/operations.md)). spec AC도 사본 리허설과 안전 경로 확인을 관찰 가능한 조건으로 연결한다 ([M01 spec L35-L42](../../spec-plan-design/candidate/examples/M01/spec.md)). GitLab의 5→25→50→75→100% 공개, 관찰 시간, SLO 확인은 위험한 전역 규칙 변경의 좋은 운영 예지만 ([D3 L416-L445](../../../exemplary-design-and-plans/originals/D3-gitlab-http-routing-service.md)), 이를 모든 소규모 서비스 spec에 복사할 이유는 없다. 현재 후보의 조건 기반 전환 표현을 유지하고, 실제 배포 순서는 plan/운영 정본에 두는 편이 더 얇다. |
| 유용한 도식 | **대체로 강함, 선택 기준 보강 가능** | 안내는 컴포넌트·시퀀스·클래스·상태·배포 중 필요한 것만 선택하고 작은 변경에는 그림을 강제하지 않는다 ([design-blocks L30-L40](../../spec-plan-design/candidate/guidance/design-blocks.md)). M01의 구성도·배포도·동시성 시퀀스는 각각 경계, 위치, 경합을 답하므로 유용하다. `SQLiteStore`와 논리 데이터형 `Request`를 함께 보인 클래스 그림도 공개 메서드·반환 형태를 한눈에 묶고, 본문은 실제 `Request`가 별도 런타임 클래스가 아닌 dict임을 명시한다 ([architecture L19-L42](../../spec-plan-design/candidate/examples/M01/design/architecture.md)). 따라서 필수 수정 사항은 아니다. 다만 독자가 논리 데이터형을 구현 클래스 요구로 읽을 우려가 있는 팀에서는 같은 계약을 인터페이스 표로 표현하는 편이 더 읽기 쉬울 수 있다. MediaWiki도 장 전체에 모든 종류의 그림을 쓰지 않고, 저장 구조의 전후 비교가 필요한 곳에 스키마 그림을 집중한다 ([D4 L354-L406](../../../exemplary-design-and-plans/originals/D4-mediawiki.html)). |

## 사례에서 가져올 구체적인 강점

### 1. 제약에서 구조, 구조에서 관찰 가능한 흐름으로 이어지는 설명

GitLab은 “단일 도메인에서 올바른 Cell로 투명하게 보낸다”는 사용자 결과를 실제 URL 세 개로 먼저
구체화하고, stateless·configuration/rule based 원칙을 제시한 다음, 실제 요청 두 개의 흐름을 보여 준다
([D3 L15-L58](../../../exemplary-design-and-plans/originals/D3-gitlab-http-routing-service.md),
[L184-L207](../../../exemplary-design-and-plans/originals/D3-gitlab-http-routing-service.md)). 현재 후보는 R/AC와
인터페이스 계약이 더 엄밀하지만, 이 연결은 여러 표와 파일 사이에 분산된다. 구현 가능성은 높아도 첫 독자의
설계 검토 비용이 커질 수 있다.

MediaWiki 저장 장의 핵심도 스키마 열거가 아니다. 기존 `cur`/`old`/`archive` 구조에서 이름 변경과 삭제가
대규모 복사를 일으키는 이유를 설명하고, `page`/`revision`/`text` 분리와 포인터 갱신이 그 비용을 어떻게
없애는지 이어서 말한다
([D4 L376-L422](../../../exemplary-design-and-plans/originals/D4-mediawiki.html)). 이 사후 설명의
형식을 사전 spec에 맞추면 “현재 동작과 실패 → 선택한 경계 → 변경 후 대표 흐름 → 유지 불변식” 정도의 짧은
문단이 된다. 역사 장의 분량을 복사할 필요는 없다.

### 2. 수치·운영 상태에 이유를 붙이는 방식

GitLab은 라우터 지연 50ms를 선언하는 데 그치지 않고 기존 `web`/`api`/`git` SLI와 여유 폭을 근거로 둔다
([D3 L80-L103](../../../exemplary-design-and-plans/originals/D3-gitlab-http-routing-service.md)). 현재
설계 블록 안내도 성능 수치에는 알려진 부하·측정 근거가 필요하며, 근거가 없으면 결정을 미정으로 남기라고 이미
요구한다
([design-blocks L7-L15](../../spec-plan-design/candidate/guidance/design-blocks.md)). 이 부분은 새 섹션이
필요한 결손이 아니라 유지해야 할 원칙이다.

MediaWiki는 replica lag가 일정 수준을 넘으면 읽기 대상을 제외하고 모두 지연되면 읽기 전용으로 바뀌며,
쓰기 직후 사용자가 과거 상태를 보지 않도록 세션에 master 위치를 보존한다고 설명한다
([D4 L424-L452](../../../exemplary-design-and-plans/originals/D4-mediawiki.html)). 운영 상태가 단순 인프라
설정이 아니라 사용자에게 보이는 일관성과 연결되어 있다. M01 operations도 같은 수준으로 실패/중지 상태와
데이터 보존을 연결하므로 이미 좋은 반례다.

### 3. 약점을 숨기지 않는 설명

MediaWiki 장은 parser의 형식 명세 부재, 테스트에 의존해 굳어진 호환성, 실패한 대체 parser 시도를 그대로
기록한다
([D4 L820-L845](../../../exemplary-design-and-plans/originals/D4-mediawiki.html)). 권한 모델이 전통 CMS의
콘텐츠별 접근 제어에 맞지 않는다는 한계와 extension 등록 방식의 성능 비용도 밝힌다
([D4 L772-L778](../../../exemplary-design-and-plans/originals/D4-mediawiki.html),
[L1017-L1049](../../../exemplary-design-and-plans/originals/D4-mediawiki.html)). 이는 해당 설계를 모범
정답으로 채택할 근거가 아니라, 중요한 부채·비용을 설명해야 독자가 선택의 실제 한계를 판단할 수 있다는 근거다.
현재 후보의 `Flagged concerns`, scope, open questions는 이 역할을 이미 갖추고 있고 M01의 Q4와 JSON 복귀
위험도 숨기지 않는다
([M01 spec L50-L63](../../spec-plan-design/candidate/examples/M01/spec.md)). 유지할 강점이다.

## 권고

1. **Design 첫 부분의 서술 프롬프트를 강화한다.** M01처럼 구성 요소나 저장 경계가 둘 이상 바뀌는 경우에만
   3~6문장으로 현재 흐름과 문제, 선택한 변화, 변경 후 대표 흐름, 반드시 유지할 불변식을 잇게 한다. 새 필수
   절을 늘리기보다 현재 “핵심 변화·선택”과 Design 안내를 구체화하면 충분하다.
2. **대표 흐름을 AC와 구별해 한 번 끝까지 보여 준다.** 순서·경계가 설계 판단에 영향을 줄 때 정상 흐름 하나와
   중요한 실패/대체 흐름 하나를 실제 입력·행위자로 설명한다. 짧으면 문장이나 번호 목록, 경합·분기가 있으면
   시퀀스를 쓴다. AC는 판정 계약이고 이 흐름은 구성 요소가 그 결과를 만드는 인과 설명이다.
3. **중요한 선택에만 작은 대안 기록을 둔다.** 선택, 실제 고려한 대안, 핵심 요구에서 두 선택을 구별하는 기각
   이유, 감수한 비용 또는 재검토 조건을 각각 한두 줄 남긴다. 대안 수를 채우거나 단일 함수 변경까지 ADR·대안
   표를 요구하지 않는다. M01의 SQLite 선택은 이 구별 근거를 조금 더 선명하게 할 수 있는 좋은 출발점이다.
4. **여러 상태가 한 그림에 있으면 현재/목표/전환 의미를 표시한다.** M01 구성도는 JSON과 SQLite가 동시에
   존재하는 이유와 어느 저장소가 활성인지 범례·상태 표시 또는 작은 전후 그림으로 바로 알 수 있게 할 수 있다.
   단일 경계 변경에는 현재 표와 문장으로 충분하다.
5. **도식 종류보다 답할 질문을 먼저 고르게 한다.** “누가 누구를 호출하는가”, “요청 하나가 어디서 실패하는가”,
   “어떤 상태에서 무엇이 허용되는가”, “무엇이 어느 호스트에 있는가” 중 문장만으로 모호한 질문에만 그림을
   쓴다. M01의 class diagram은 논리 데이터형이라는 본문 설명으로 정당화되며 유지할 수 있다. 독자가 이를 구현
   클래스 요구로 오해할 가능성이 크다면 인터페이스 표로 바꾸는 것은 선택적 가독성 개선이다. 구성·배포·동시성
   그림은 유지 가치가 높다.
6. **운영 게이트는 현재 강도를 유지하되 GitLab 절차를 보편 양식으로 만들지 않는다.** 전역 라우팅처럼 작은
   오류가 큰 장애로 이어지는 시스템은 점진 비율·관찰 시간·SLO 게이트가 필요하다. 단일 호스트 내부 서비스는
   M01처럼 중지/보존/검증/재개 조건이면 충분하다. 구체 명령과 반복 배포 단계는 plan 또는 운영 문서가 소유하게
   한다.
7. **다음 완성 예시는 서술과 흐름의 기준도 보여 준다.** M01은 저장·동시성·복구의 좋은 예이므로 유지하고,
   UI 또는 외부 서비스 연동 예시 하나에서 제품 맥락→대표 요청/사용자 흐름→선택→실패 상태가 자연스럽게
   이어지는 짧은 설계를 보여 주면 양식의 독자 경험을 더 잘 고정할 수 있다.

적용 기준은 얇게 유지할 수 있다. 한 경계 안의 가역적 변경은 현재 R/AC와 짧은 Design 표면 충분하다. 여러
구성 요소·비동기 순서·데이터 이행·공개 상태가 얽힐 때만 설명 문단, 대표 흐름, 필요한 도식을 추가한다. 여러
팀·리전·전역 트래픽을 전제로 한 GitLab 수준의 운영 절차를 작은 내부 서비스에 기본 부과하지 않는다.

## 한계

- 이 검토는 보관된 문서의 설명 품질 비교다. GitLab 운영 대시보드나 프로덕션 동작을 재현하지 않았고,
  MediaWiki의 현재 구현도 확인하지 않았다.
- GitLab 문서의 미정 항목과 후속 운영 개정 때문에 한 파일의 모든 절을 동일한 시점의 사전 결정으로 보지 않았다.
- MediaWiki의 수치, 기술 선택, 역사적 성공·실패는 현재 후보에 대한 구현 권고가 아니다. 사후에 잘 설명할 수
  있다는 사실만으로 사전에 옳은 선택이었다고 결론내리지 않았다.
- M01은 합성 예시이므로 실제 제품의 사용자 조사·운영 명령·성능 측정을 대신하지 않는다. Q4를 명시적으로
  이월한 현재 표현은 이 한계를 올바르게 드러낸다.
- 모든 diagram 종류, 단일 spec 파일, 장문의 아키텍처 장을 요구하지 않는다. 권고의 목표는 계약의 엄밀성을
  유지하면서 사람이 중요한 결정과 대표 동작을 더 빨리 검토하게 하는 것이다.
