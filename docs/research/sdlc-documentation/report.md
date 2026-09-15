# AI-native SDLC 문서·양식 조사

조사일: 2026-09-11 · 대상: 사내 서비스를 개발하는 팀의 얇은 템플릿·정책·스킬

## 핵심 판단

조사의 목적은 Anthropic Playbook의 취지에 맞는 **우리 intent·spec·plan 양식의 설계 근거**를
확보하는 것이다. 의도·요구사항과 설계·구현 계획의 역할은 전제이며, 기존 목차와 표현은 재설계할 수 있다.
양식의 출발점과 설계 방법에 대한 후속 권고는 [설계 접근 비교](design-approaches.md)에 있다. 조사한 자료는
플레이북이 모든 설계를 짧은 한 파일로 축약하라고 요구한다는 해석을 뒷받침하지 않는다.
반대로 문서 수와 승인 단계를 늘리는 것이 AI-native의 충실도를 높인다는 근거도 없다.
중요한 것은 사람과 에이전트가 같은 의도·결정·검증 기준을 읽고 다음 행동으로 이어가는 것이다.
플레이북은 초기 Markdown 산출물을 두 독자가 함께 읽고 행동하는 공통 기록으로 설명한다.[^anthropic-intro]

Fuchsia·TensorFlow RFC는 중요한 설계 판단을 설명하는 데 유용하다. Spec Kit·OpenSpec·Kiro는
요구를 검증 가능한 동작으로 표현하고 변경 뒤 다시 맞추는 방법을 제공한다. BMAD·GSD·Spec Kitty·
Superpowers는 크기 조절, 작업 분할, 에이전트 간 인계와 검토를 더 구체화한다. MADR는 오래 남겨야 할
결정의 이유를 짧게 기록하는 데 유용하다. 이들은 서로 다른 문제를 푸는 자료이므로 단일 점수로
우열을 정하지 않았다. 아래 권고는 **조사자의 적용 판단**이며 이번 작업에서 운영 정책으로 반영하지 않았다.

## 조사 방법과 근거의 범위

공식 문서·저장소 12개를 역할, 생성·갱신 이벤트, 사람의 판단, 검증 연결, 규모, 도구 의존성으로
비교했다. Git 원문은 commit으로 고정하고 원본 양식·작성 지침·채워진 예시·자체 분석을 분리했다.
최신 릴리스와 개발 브랜치가 다른 경우 같은 판처럼 섞지 않았다. 출처, 이용 조건, 조회 시각,
원래 경로와 로컬 파일의 SHA-256은 [전체 출처 색인](sources.json)에 있다.

양식이 실제로 사용되는 모습은 독립 제품 Opentu의 기능 확장과 OpenSpec 자체의 버그 수정 두 건에서
조사했다. 문서 → 코드·테스트 diff → PR → 현재 명세 반영을 가능한 범위까지 연결했다.
두 사례가 모두 OpenSpec 형식이므로 여러 프레임워크의 실사용 성과를 비교한 표본은 아니다.
프레임워크 CLI 설치, 개발 대화 실험, 외부 코드 실행, 생산성 벤치마크는 수행하지 않았다.
공개 기록에서 확인한 상류 CI와 우리가 직접 실행한 검사를 구별한다.

## 1. 북극성에서 intent·spec·plan이 맡는 역할

### Intent는 요청자의 문제와 바라는 변화를 보존한다

플레이북의 intent는 요청자가 무엇을 왜 원하는지, 어떤 제약과 미해결 질문이 있는지 포착하는
proto-spec이다. Claude가 질문하고 요청자가 오해를 고치는 대화를 거친다. 조직이 합의한 양식을
사용할 수 있으며, 예시는 문제·기대 결과·영향받는 사용자와 시스템·제약·열린 질문을 담는다.
초기 요구나 해결 방향을 포함할 수 있지만, 기술팀이 검토한 완성된 요구사항·설계 문서와 같지는 않다.[^anthropic-intent]

따라서 `intent.md`를 EARS 요구사항 목록으로 바꾸거나 requester에게 API 설계와 테스트 목록까지
완성하라고 요구하는 것은 우리 목적과 맞지 않는다. 반대로 의도라는 이유로 검증 가능한 기대 결과나
필수 제약을 빼는 것도 부적절하다. 예를 들어 “동료에게 상태를 물어보는 시간을 줄이고 싶다”가
문제와 이유라면, “내 신청 상태를 볼 수 있다”는 기대 결과이며, “다른 사람의 신청은 볼 수 없다”는
요청 시점부터 알 수 있는 제약이다. 이 예시는 조사자의 설명이며 공식 양식의 인용이 아니다.

### Spec은 검토된 요구와 설계를 함께 담는다

플레이북은 수용된 intent를 바탕으로 조직의 관련 스킬을 적용하여 요구사항과 설계를 한 세션에서
작성하고 제품 책임자가 원래 문제와 비교하도록 한다. 미해결 질문은 답하거나 명시적으로 이월하고,
정책 충돌은 드러내야 한다. spec을 온전히 문서화하라는 생성 지시는 있지만 고정된 Markdown 목차나
분량 제한은 제시하지 않는다.[^anthropic-spec]

같은 세션에서 함께 정리한다는 것은 요구와 설계의 관계를 잃는 반복 인계를 줄이는 방향이다.
둘 사이의 논리적 구분을 없애거나 모든 상세를 삭제하라는 뜻으로 해석하지 않는다. 우리 spec에서
요구, 수용 기준, 설계 결정을 구분하되 서로 참조하게 하는 방식은 이 취지에 부합한다.

### Plan은 실행 가능한 작업과 검증으로 연결한다

플레이북의 plan은 파일 경로, 작업 순서, 위험, 검증을 구체화하여 원래 대화에 참여하지 않은
엔지니어도 실행할 수 있는 기록을 지향한다. 구현이 계획을 벗어나면 그 변경과 같은 커밋에 plan을
갱신하도록 명시한다.[^anthropic-plan] 이는 계획을 구현 종료까지 동결한다는 뜻이 아니다.

이 문장은 `spec.md`까지 매 커밋마다 반드시 수정하라는 축자 규칙은 아니다. 설계나 동작 계약이
바뀌었을 때 해당 spec도 맞추어야 한다는 것은 우리의 일관성 원칙이다. 원문과 자체 해석을 구분해야
우리 정책을 다시 북극성의 요구인 것처럼 평가하는 순환을 피할 수 있다.

## 2. 전통적인 RFC 양식을 쓰면 AI-native 취지를 해치는가

**양식의 출생 시기보다 그 양식을 사용하는 방식이 중요하다.** Fuchsia의 지침은 승인 판단에
실질적으로 영향을 주는 설계 내용을 충분히 쓰고, 모든 구현 세부를 정하려 하지 않으며, 약속과
예시를 구별하라고 한다. 문서 밖에서 합의한 중요한 결론도 기록에 반영한다.[^fuchsia]
이 원칙은 사람이 결정하고 에이전트가 구현하는 흐름에도 직접 도움이 된다.

예를 들어 예시 코드의 함수명을 구현 선택으로 남긴 것인지 공개 API 계약으로 승인한 것인지
불분명하면, 에이전트는 불필요하게 설계에 묶이거나 지켜야 할 계약을 바꿀 수 있다. 이는 문서
부족만의 문제가 아니라 표현의 권위와 의미가 불명확한 문제다. 중요한 결정과 가정·예시를 분명히
쓰는 원칙은 차용하되, 예시마다 별도 상태 필드를 만드는 방식까지 필요하지는 않다.

TensorFlow RFC는 선택 이유, 다른 부분에 대한 영향, 최종 사용자의 처음부터 끝까지 이용 예시를
묻는다. 설계 제안 본문과 선택적인 상세 설계 절을 구분하며, 요약이 짧다고 전체 설계도 짧게
제한하지 않는다. RFC 승인과 실제 구현 완료도 구별한다.[^tensorflow-template][^tensorflow-process]
이를 참고해 우리의 Design과 Acceptance criteria를 충실히 쓰는 것은 AI-native 취지를 해치지 않는다.

다만 TensorFlow의 후원자·의견 수렴 기간·위원회나 Fuchsia의 승인된 RFC 보존 방식은 각각의
공개 커뮤니티 거버넌스다. 이 절차까지 그대로 가져오면 사내 팀의 가벼운 개발 흐름에 맞지 않을 수 있다.
특히 승인된 RFC의 역사적 성격을 현재 구현 중인 plan에 적용하여 수정하지 않게 만드는 것은
피해야 한다. **설계 질문은 참고하고, 조직 절차와 문서 수명은 따로 판단한다.**

## 3. 한 파일의 짧은 양식과 충분한 설계는 양립할 수 있다

Google의 공개 문서에서는 팀이 설계 문서를 통해 협업한다는 관행을 확인했으나 Google 전체가
공통으로 쓰는 단일 공개 빈 양식은 확보하지 못했다. 공개된 책은 2020년의 관행 설명이다.
Technical Writing 지침도 긴 한 문서와 연결된 여러 문서를 모두 다루며 독자가 내용을 찾고 이해할
수 있도록 구조화하는 데 초점을 둔다.[^google-book][^google-writing]

TensorFlow의 두 실제 RFC는 상세도가 무엇에 따라 달라지는지 보여준다.

| 문서 | 설명해야 했던 결정 | 이 조사에서 얻는 판단 |
|---|---|---|
| [oneDNN 기본 활성화](references/tensorflow/evidence/20210930-enable-onednn-ops.md) | 기본값, 비활성화 수단, 성능·수치 차이, 테스트와 유지보수 | 좁은 변경도 사용자 영향이 넓으면 충분한 설계 설명이 필요하다. |
| [분산 tf.data 서비스](references/tensorflow/evidence/20200113-tf-data-service.md) | 분산 구조, 사용자 흐름, API·통신 모델, 결정성과 부하 분산의 선택 | 시스템 경계와 대안이 많으면 상세 설계를 확장하는 것이 자연스럽다. |

두 문서의 수용 상태를 현재 구현 완료나 성능 우위의 증거로 읽지는 않는다. 실제 내용과 적용 범위는
[TensorFlow 분석](references/tensorflow/README.md)에 정리했다.

우리 팀에는 **핵심 판단을 먼저 읽고 필요할 때 세부로 내려가는 구조**가 적절하다. 작은 변경은
기존 spec의 몇 문단으로 충분할 수 있다. API 계약·상태 머신·이행 절차가 본문을 가리면 하위 절이나
연결된 상세 문서로 분리한다. 분리할 때는 무엇이 필수로 읽을 계약인지, 무엇이 배경 자료인지
명확히 한다. BMAD의 현재 spec은 짧은 계약과 필수 companion, 흡수된 원천 자료를 구별한다.
파일 분리가 정보 생략을 뜻하지 않도록 하는 참고 사례다.[^bmad]

## 4. SDD 프로젝트에서 이름보다 역할을 비교해야 한다

Spec Kit의 `spec.md`는 사용자 시나리오·요구·성공 기준이며 기술적 설계는 `plan.md`에 둔다.
실행 작업은 다시 `tasks.md`로 분리한다. Kiro도 요구·설계·작업을 구분한다.
따라서 이들의 spec 하나만 우리 spec과 비교하면 설계가 간소화된 것처럼 오해하기 쉽다.
우리의 combined spec과 비교하려면 상대의 요구 문서와 설계 문서를 함께 보아야 한다.[^speckit][^kiro-feature]

OpenSpec은 proposal, capability별 행동 변경분, design, tasks를 구분한다. 기본 스키마는 proposal 뒤에
specs와 design이 각각 의존하고 tasks가 둘을 요구하는 그래프다. 단순히 모든 파일을 정해진 순서로
한 번씩 쓰고 끝내는 모델이 아니다. 구현 발견은 기존 산출물을 다시 맞추는 update로 이어질 수 있다.
행동 변화가 없는 경우의 `skip_specs`와 archive 시 동기화를 생략하는 선택도 서로 다르다.[^openspec]

BMAD는 규모에 따라 작은 spec 계약이나 PRD·공유 아키텍처·story 분할을 선택한다. GSD는 프로젝트·
요구·roadmap·현재 상태·phase별 실행 계획으로 긴 작업의 문맥을 유지한다. Spec Kitty는 요구 ID에서
work package, 소유 파일, 의존 관계, review 상태로 이어지는 실행 체계를 둔다. Superpowers는
작은 변경과 아키텍처 변경의 문서 깊이를 달리하면서 승인된 설계와 task별 실행·검토를 잇는다.
각 문서 역할과 기본 필요성은 [비교표](comparison.md), 판별 근거는 각 레퍼런스 분석에 있다.

이들에서 가져올 가치는 이름이나 파일 수가 아니라 **다음 작업자가 추측하지 않아도 되는 연결**이다.
예를 들어 사용자 시나리오 ↔ 수용 기준, 요구 ID ↔ 작업, 작업 ↔ 소유 파일·검증, 변경 판단 ↔ 관련
문서가 그런 연결이다. 사소한 작업까지 모든 ID와 표를 강제할 필요는 없다.

## 5. 현재 명세와 과거 결정은 같은 기록이 아니다

문서를 계속 최신으로 유지할지, 완료한 변경의 역사로 보존할지 결정하지 않으면 “spec을 업데이트한다”는
말도 서로 다르게 이해하게 된다. 비교 결과 적어도 다음 세 목적을 구분해야 했다.

| 목적 | 예 | 변경 시 처리 |
|---|---|---|
| 현재 작업의 계약과 계획 | 구현 중 spec·plan | 바뀐 요구·설계·순서·검증을 관련 문서에 반영한다. |
| 현재 제품이 제공하는 동작 | OpenSpec main specs, 팀이 선택한 living spec | 완료 변경을 통합하고 현재 동작을 읽을 수 있게 한다. |
| 당시의 제안과 결정 이력 | 승인된 RFC, archive된 변경, Git의 이전 판 | 원래 판단의 맥락을 보존하고 후속 변경과 연결한다. |

Spec Kit은 flow-forward, living spec, flow-back을 팀이 선택할 유지 모델로 설명하며 하나를 CLI
기본값으로 강제하지 않는다. 분석 명령은 불일치를 보고하는 읽기 전용 검토다.[^speckit-persistence]
OpenSpec은 delta를 현재 명세에 반영하는 sync와 변경을 보관하는 archive가 별도 동작이며, 명시적으로
sync 없이 archive하는 선택도 있다.[^openspec-archive] Kiro도 수정 뒤 설계 재검토와 tasks 동기화
행동을 안내한다.[^kiro-update] 문서가 있다는 이유만으로 최신성이 자동 유지되는 것은 아니다.

우리 팀의 당장 필요한 최소 원칙은 작업 중인 spec/plan을 현재 결정에 맞추고, 변경 이력은 Git으로
남기는 것이다. 서비스 전체의 영구 명세 폴더와 별도 archive 체계까지 지금 추가할지는 장기 유지
수요를 보고 판단해야 한다. 이번 조사만으로 새 명세 저장소나 상태 기계를 도입할 근거는 부족하다.

## 6. 갱신을 인식할 이벤트와 사람의 판단

다음 표는 원문들의 공통 문제를 우리 흐름에 적용한 **후속 설계 제안**이다. 새로운 강제 정책이나
실험을 통과한 규칙이 아니다. 기존 이벤트 검토 스킬을 보완할 때 중복 없이 확인할 후보로 쓴다.

| 이벤트 | 다시 볼 기록 | 충분한 행동 |
|---|---|---|
| 요청자의 답으로 목적·제약이 바뀜 | intent와 이미 파생된 spec | 답을 반영하고 이전 가정이 어디에 전파됐는지 확인한다. |
| 요구·인터페이스·중요 설계 결정이 바뀜 | spec, 관련 plan | 바뀐 계약·이유·영향을 기록하고 실행 순서·검증을 맞춘다. |
| 구현 중 파일·작업 순서·PR 경계가 달라짐 | plan, 설계 변화가 있으면 spec | 다음 작업자가 실제 계획을 따라갈 수 있게 수정한다. |
| 리뷰나 테스트가 빠진 요구·회귀를 드러냄 | 요구·검증 기준, 코드·테스트 | 요구 변경인지 기존 요구의 검증 보강인지 구별한다. |
| 관련 변경을 커밋·인계하거나 PR을 준비함 | 해당 diff와 의도·설계·계획 | 바뀐 판단이 반영됐는지, 유지한 계약의 증거가 있는지 대조한다. |

매 커밋마다 모든 문서를 고치거나 “검토 완료” 로그 파일을 추가하는 것이 목표는 아니다.
내용 변화가 없는 문서의 수정 시각을 갱신해도 의미상 정합성은 입증되지 않는다. 에이전트가
판단해야 할 질문을 이벤트에 붙이고, 중요한 설계·회귀 판단에서는 충분한 모델·추론과 필요시
독립 검토를 쓰는 것이 우리 팀의 방향에 맞다. 그래도 실수 가능성은 남으며, 사람의 검토를 통해
중요한 누락을 발견하고 고치는 SDLC라는 전제를 유지한다.

## 7. 작은 작업·큰 작업·병렬 작업의 차이

작은 변경에는 요청 이유, 바뀔 동작, 유지할 계약, 검증이 충분히 드러나면 된다. 별도 상세 설계가
필요한지는 코드 줄 수보다 새로운 결정과 영향으로 판단한다. 현재 BMAD와 Superpowers의 여러 경로,
Kiro Quick Spec은 산출물의 깊이와 중간 승인 대기 횟수를 구분할 수 있음을 보여준다.[^bmad][^superpowers][^kiro-quick]
이는 우리 기존 intent/spec/plan을 즉시 생략하자는 결정이 아니라, 상세도를 조절할 참고 근거다.

큰 작업은 공유 목표·제약·인터페이스를 먼저 합의하고 독립적으로 검증 가능한 작업으로 나누는 것이
적절하다. Spec Kitty의 WP 소유 경계와 GSD의 plan 의존 관계·공유 상태 단일 작성자는 병렬 작업의
구체적 참고 사례다. 이들 규칙은 실행 도구와 상태 관리에도 의존하므로 템플릿 파일만 가져와서는
같은 작동을 얻을 수 없다.[^speckitty][^gsd]

작업 분할과 PR 분할도 별개다. 한 작업이 꼭 한 PR일 필요는 없지만, PR에서 함께 검토해야 할
계약과 회귀 범위는 설명되어야 한다. 이번 조사는 [기존 PR 크기 조사](../pr-size/README.md)를
대체하지 않는다. 우리 plan에 이미 있는 PR 분할·검증 기준과 새 문서 항목이 중복되지 않게 하는 것이
후속 적용의 조건이다. 플랫폼의 정해진 작업 시간·에이전트 수·worktree 절차까지 보편 정책으로
옮기는 것은 권하지 않는다.

## 8. 실제 적용 기록이 보여 준 것과 보여 주지 못한 것

### Opentu: 짧은 문서도 코드와 연결되지만 요구 누락이 남을 수 있다

오디오 재생 모드 변경은 proposal/spec/tasks와 서비스·두 UI·단위 테스트가 같은 commit에 있다.
별도 design 파일은 확인되지 않았다. 짧은 문서에서도 공유 상태와 네 가지 재생 동작을 전달하는
형태를 볼 수 있다. 그러나 proposal·tasks·코드에는 있는 저장·복원 계약이 delta spec의 독립
시나리오에는 없다. 현재 명세만 읽으면 그 계약을 놓칠 수 있다.
[구현 commit](https://github.com/ljquan/opentu/commit/204da5a4433aa8e7b41b509cafc40ee99b94da07)
및 [사례 분석](case-studies/opentu/README.md).

Tasks는 공개 경로에 처음 등장할 때부터 모두 완료 표시였으며, 초안 작성 대화와 그 순서는
확인되지 않았다. 구현 제목과 PR 범위도 이 기능만을 설명하지 않는다. 해당 SHA의 성공 CI 기록은
확보하지 못했다. 이 사례는 문서 존재와 코드 연결을 보여 주지만 계획이 실제로 구현보다 먼저
작성됐다는 증거나 테스트 통과 증거는 아니다.

### OpenSpec 자체 수정: 리뷰·검증·현재 명세 반영을 구분할 수 있다

`schema init --force`의 잘못된 입력이 기존 파일을 삭제하는 버그 수정은 재현 조건, 보존할 동작,
설계 결정, 제외 범위, 실제 명령을 호출하는 회귀 테스트를 연결했다. 리뷰에서 성공 경로의 종료
상태 확인을 요구했고 후속 commit이 그 테스트를 보완했다. 이는 기존 요구의 검증 보강이며, 설계가
개정되어 spec도 바뀐 사례로 확대해서는 안 된다.
[PR #1446](https://github.com/Fission-AI/OpenSpec/pull/1446) 및 [사례 분석](case-studies/openspec/README.md).

구현 SHA의 [CI run 30300699482](https://github.com/Fission-AI/OpenSpec/actions/runs/30300699482)에서는
Linux·macOS·Windows 테스트와 lint/type check 성공을 확인했다. 다른 실행은 취소 상태였으므로
모든 실행이 성공했다고 요약하지 않았다. 이후 [PR #1467](https://github.com/Fission-AI/OpenSpec/pull/1467)이
완료 변경을 archive하고 현재 명세에 반영했다. 구현 병합과 영구 명세 정리가 별도 작업일 수 있으며
책임과 완료 조건을 명확히 해야 한다는 시사점이 있다.

두 사례 모두 생산성 향상, 결함 감소율, 사람·에이전트의 기여도, 조직 전체의 SDD 성숙도를
입증하지 않는다. 성공 사례 수로 프레임워크의 우수성을 순위화하지 않는다.

## 9. 우리 팀에 권고하는 적용 순서

우선 기존 양식과 스킬에 아래 내용이 이미 들어 있는지 대조한다. 중복이면 문구를 늘리지 않고
실제 대화에서 빠지는지 살핀다. 후보를 채택할 경우 별도 개발 건으로 최소 변경과 실험을 진행한다.

| 우선순위 | 제안 | 넣을 자리와 적용 조건 | 피할 과잉 |
|---|---|---|---|
| 1 | 의도·결정·실행의 역할을 명확히 유지 | 기존 intent/spec/plan 작성 설명 | intent를 기술 명세로 대체 |
| 1 | 대표 동작과 중요한 회귀 경계를 검증에 연결 | spec 수용 기준과 plan의 Proof; 동작 변화가 있을 때 | 모든 요구에 새 추적 시스템 강제 |
| 1 | 중요한 선택의 이유·단점·계약과 예시를 구별 | spec의 Design; 실제 선택이 있을 때 | 형식적인 대안 나열과 기본 ADR 추가 |
| 1 | 구현 발견·인계·PR 준비에서 문서 정합성 판단 | 기존 이벤트 검토 스킬과 관련 diff | 수정 시각·키워드로 의미 검증을 대체 |
| 2 | 큰 변경만 상세 문서·작업 의존·소유 경계 확장 | spec 상세 참조와 plan 분할 | 작은 작업에도 WP·원장·다중 승인 강제 |
| 보류 | 영구 제품 명세·자동 archive·상태 엔진 도입 | 반복적인 유지 문제와 효용이 확인된 경우 | 도구 전체를 템플릿의 기본 역할로 확대 |

MADR 최소형의 핵심인 맥락·대안·선택 이유는 별도 ADR 파일 없이 기존 Design에 쓸 수 있다.
프레임워크의 전체 설치보다 작은 작성 원칙을 먼저 참고하는 권고다.[^madr]

후속 검증은 작은 기능, 동작을 보존해야 하는 버그, 구현 중 설계가 달라지는 변경을 같은 데이터와
사람 페르소나로 대화하며 비교하는 방식이 적절하다. 기준은 중요한 의도·계약·계획 변경이 기록되고,
다음 작업자가 이어갈 수 있으며, 관련 회귀를 발견·수정하는가다. 문서 수·체크박스 수·스킬 호출 횟수를
성공 지표로 삼지 않는다. 이번 조사 결과는 후속 실험 설계의 근거이며 통과 판정 자체가 아니다.

## 10. 남은 불확실성과 자료 사용법

- Google 공통 빈 양식, Anthropic의 고정 spec 빈 양식, Kiro의 독립 배포 빈 양식은 이번 공식 자료
  범위에서 확보하지 못했다. 예시나 자체 재구성을 공식 양식으로 표시하지 않았다.
- GSD의 요청된 기존 저장소와 TensorFlow community는 보관 상태다. Spec Kit·BMAD·Spec Kitty·
  Superpowers 일부 자료는 개발 스냅샷이다. 운영 도입 시 적용할 릴리스를 다시 확인해야 한다.
- OpenSpec의 design 작성 조건과 기본 tasks 의존성에서 design 생략의 구체적인 상태 전이는
  선택 원문의 정적 조사만으로 완전히 확인하지 못했다.
- Spec Kitty 개발 스냅샷에는 테스트 작성 정책의 표현이 자료별로 다르다. 명시적 요구를 그대로
  조합하면 모순이 생길 수 있어 운영 채택 전 해당 릴리스와 설정을 확인해야 한다.
- 두 실제 사례는 OpenSpec 형식에 한정된다. 다른 프레임워크의 독립 제품 적용과 장기 문서 유지,
  문서 변경이 실제 품질에 미치는 효과는 추가 증거가 필요하다.

[비교표](comparison.md)에서 필요한 원칙을 고르고 해당 레퍼런스 README와 원본을 함께 읽는 것이
좋다. 원문 디렉터리는 참고 자료이며 설치된 스킬이나 이 저장소의 실행 지침이 아니다.

## 주요 출처

아래는 종합 판단을 뒷받침하는 공식 원문이다. 세부 파일별 출처는 레퍼런스 README와
[sources.json](sources.json)에 있으며 웹 페이지는 조회 시점의 내용이다.

[^anthropic-intro]: Anthropic, [Playbook introduction](https://academy.claude.com/courses/ai-native-sdlc-playbook/introduction).
[^anthropic-intent]: Anthropic, [Capture as intent.md](https://academy.claude.com/courses/ai-native-sdlc-playbook/capture-intent).
[^anthropic-spec]: Anthropic, [Requirements and design](https://academy.claude.com/courses/ai-native-sdlc-playbook/requirements-and-design).
[^anthropic-plan]: Anthropic, [Plan mode](https://academy.claude.com/courses/ai-native-sdlc-playbook/plan-mode).
[^fuchsia]: Fuchsia, [RFC best practices](https://fuchsia.googlesource.com/fuchsia/+/a433f3399c4de6ef5ccb1690d7e51b6568efb1e1/docs/contribute/governance/rfcs/best_practices.md).
[^tensorflow-template]: TensorFlow community, [RFC template](https://github.com/tensorflow/community/blob/185530183d8f3734795beb520d02b8265c230a12/rfcs/yyyymmdd-rfc-template.md).
[^tensorflow-process]: TensorFlow community, [RFC process](https://github.com/tensorflow/community/blob/185530183d8f3734795beb520d02b8265c230a12/governance/TF-RFCs.md).
[^google-book]: [Software Engineering at Google, Chapter 10](https://abseil.io/resources/swe-book/html/ch10.html), 2020.
[^google-writing]: Google, [Organizing large documents](https://developers.google.com/tech-writing/two/large-docs).
[^speckit]: GitHub Spec Kit, [templates at captured commit](https://github.com/github/spec-kit/tree/c173bf19a6654e3b05386ec3599349a55282b897/templates); [분석](references/github-spec-kit/README.md).
[^speckit-persistence]: GitHub Spec Kit, [Spec persistence](https://github.com/github/spec-kit/blob/c173bf19a6654e3b05386ec3599349a55282b897/docs/spec-persistence.md).
[^openspec]: OpenSpec, [spec-driven schema](https://github.com/Fission-AI/OpenSpec/blob/9d4e5974e5c0d9a09b9c6c1e1eb0975e80ec4461/schemas/spec-driven/schema.yaml); [분석](references/openspec/README.md).
[^openspec-archive]: OpenSpec, [archive skill](https://github.com/Fission-AI/OpenSpec/blob/9d4e5974e5c0d9a09b9c6c1e1eb0975e80ec4461/skills/openspec-archive-change/SKILL.md); [보관 원문](references/openspec/evidence/skills/archive-change.md).
[^kiro-feature]: Kiro, [Feature Specs](https://kiro.dev/docs/specs/feature-specs/).
[^kiro-update]: Kiro, [Specs best practices](https://kiro.dev/docs/specs/best-practices/).
[^kiro-quick]: Kiro, [Quick Spec](https://kiro.dev/docs/specs/quick-spec/).
[^bmad]: BMAD, [captured repository](https://github.com/bmad-code-org/BMAD-METHOD/tree/abe4eb1bce919c9d22cd18b3519353d5824c4b75); [분석과 spec·planning 원문](references/bmad/README.md).
[^gsd]: GSD, [captured repository](https://github.com/gsd-build/get-shit-done/tree/bdcaab2c752d9a33a1a1ca9acf3a3c81fb991815); [분석과 planner·execution 원문](references/gsd/README.md).
[^speckitty]: Spec Kitty, [captured repository](https://github.com/spec-kitty/spec-kitty/tree/d96d0209b82318a641234812aff0817afbf09681); [분석과 WP·review 원문](references/spec-kitty/README.md).
[^superpowers]: Superpowers, [brainstorming skill](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/brainstorming/SKILL.md); [분석](references/superpowers/README.md).
[^madr]: MADR 4.0.0, [minimal template](https://github.com/adr/madr/blob/2475fe1973f66a12aaf58a91d8fa7b42c0f5ea3d/template/adr-template-minimal.md).
