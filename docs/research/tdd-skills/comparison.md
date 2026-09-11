# 공개 TDD 스킬 비교

조사일: 2026-09-11. 아래 판정은 고정 커밋의 지침을 읽은 결과다. 실행 성공률·토큰·지연·사용자
평판을 측정하지 않았다. 공개 저장소의 설명과 평가용 사례도 이 프로젝트에서 관측한 성과가 아니다.
정확한 SHA·URL·원문 해시·라이선스는 [sources.json](sources.json)에 있다.

## 비교 기준

TDD를 권한다는 문구보다 실제 행동 지시를 비교했다. 언제 시작하는지, 의도한 RED를 실행으로
확인하는지, 하나의 동작씩 최소 구현하고 리팩터링하는지, 기대값이 구현과 독립적인지, 기존 테스트를
약화하지 않는지, spec/plan과 연결되는지, 반복 승인·별도 상태·도구·수치 기준의 비용이 있는지를 봤다.

| 후보·고정 판 | 가져올 가치 | 그대로 가져오기 어려운 부분 |
|---|---|---|
| [Superpowers](references/superpowers/source/skills/test-driven-development/SKILL.md) · b36e082 | 의도한 RED 확인, 최소 GREEN, REFACTOR, 좋은/나쁜 테스트 예시 | 사전 구현 시 삭제·처음부터 다시, 모든 새 함수/메서드에 테스트라는 절대 문구. 주변 워크플로와 함께 쓰면 절차 확대 |
| [Matt Pocock](references/mattpocock/source/skills/engineering/tdd/SKILL.md) · 3cca18b | 공개 경계의 동작, 독립 기대값, 한 번에 테스트 하나 | 현재 판은 refactor를 code review로 넘김. 테스트 경계마다 사람 확인, companion skill 의존, 실제 RED 명령·최종 검증 지시 부족 |
| [Addy Osmani](references/addyosmani/source/skills/test-driven-development/SKILL.md) · 6ca0cd7 | 저장소 명령 탐색, 실제 focused 실행, RGR, 결과 중심 테스트, 완료 시 회귀 검증 | 광범위 활성화, 브라우저 MCP 결합, 매번 하나의 시나리오라는 명시 부족 |
| [ECC](references/ecc/source/skills/tdd-workflow/SKILL.md) · c9148d0 | plan 작업↔테스트↔RED/GREEN 연결, 실패 원인 구분 | 80% coverage, 별도 .tdd.md 보고서, 단계별 커밋, 명령 승인, 다수 테스트를 먼저 쓰는 예시 |
| [Kirjolab](references/kirjolab/source/.codex/skills/tdd/SKILL.md) · ac72a52 | 기존 spec/ADR과 일치시키는 얇은 현지화, 한 동작씩 진행 | Matt의 이전 판을 변형한 사례로 독립 방법론이 아님. 명시적 REFACTOR 단계는 생략됨 |
| [Glebis](references/glebis/source/tdd/SKILL.md) · d0bc206 | 한 행동씩 RGR, 실제 RED 분류, 구현자의 테스트 약화 방지 | slice당 3개 역할 호출, 상태 파일·반복 승인·계층 검사. 원 spec을 구현자에게 숨김 |

## Superpowers의 어느 부분이 무거운가

사용자가 전한 “무겁다”는 평을 비용 가설로 삼았다. 이 조사만으로 여론의 크기나 실제 성능을
확정할 수는 없다. TDD 본문과 전체 개발 워크플로를 구분하면 판단이 달라진다.

- **TDD 핵심:** 실제 실패 확인→최소 구현→다시 통과→필요한 리팩터링은 우리가 원하는 규율이다.
  이 실행 비용 자체를 불필요한 부담으로 보지는 않는다. TDD 본문은 하위 에이전트나 숫자 coverage를
  필수로 하지 않는다.
- **과도한 절대 규칙:** 구현을 먼저 썼다면 삭제하고 다시 시작하라는 지시가 여러 차례 나온다.
  복구 경로를 기계적인 재시작으로 고정하기보다 test-after 사실을 숨기지 않고 누락된 검증과 이후
  TDD를 회복하는 방법이 우리 환경에 맞는다. 이미 작성된 코드를 삭제해 과거가 test-first였다고
  바꿀 수도 없다.
- **테스트 품질 참고문서:** [writing-good-tests](references/superpowers/source/skills/test-driven-development/writing-good-tests.md)는
  독립된 기대값, 구현을 복제하는 테스트, source-text 검사, 과도한 mock, 의미 없는 단언을 다룬다.
  테스트를 조금 깨뜨려도 통과할지를 생각하는 mental mutation check는 유용하다. 매번 mutation
  도구를 실행하라는 요구로 확대하지 않는다. 본문의 “모든 함수/메서드” 체크리스트는 이 참고문서의
  사소한 전달 코드·상수·일반 문서는 테스트가 필요 없다는 설명과 긴장이 있다.
- **주변 라우팅:** [using-superpowers](references/superpowers/source/skills/using-superpowers/SKILL.md)는
  가능성이 매우 낮아도 먼저 스킬을 호출하게 한다.
  [brainstorming](references/superpowers/source/skills/brainstorming/SKILL.md)은 현재 판에서
  Spike/Bounded/Architectural로 규모를 구분한다. 따라서 항상 정식 spec을 쓰게 한다는 평가는
  틀리다. 다만 작은 작업에도 명시적 사람 승인 단계가 남는다.
- **계획·실행 확대:** [writing-plans](references/superpowers/source/skills/writing-plans/SKILL.md)는
  세부 단계, 실제 테스트·구현 코드, 반복 코드까지 계획에 적도록 한다. 이 방식은 실험하며 설계를
  발전시킬 여지를 줄이고 plan을 코드의 사전 복제본으로 만들 수 있다.
  [subagent-driven-development](references/superpowers/source/skills/subagent-driven-development/SKILL.md)는
  선택한 실행 경로에서 작업별 구현·리뷰, 수정 재검토, 원장·보고서·검토 패키지와 전체 브랜치 리뷰를
  관리한다. 단순한 같은 모양의 작업을 묶거나 검토 범위를 줄이는 비용 제어도 있지만 우리 기본 TDD
  스킬의 책임으로 가져오기에는 넓다. 이 주변 절차가 TDD 단독 사용마다 모두 발생하는 것은 아니다.

문서 크기는 부담의 한 단서다. UTF-8 원문 바이트를 측정한 값이며 토큰 수·컨텍스트 상주량·실행
비용이 아니다. 참조 파일의 전체 의존 관계나 실제 로딩 여부도 이 숫자에 포함되지 않는다.

| 후보 | 주 SKILL.md 바이트 | 함께 살펴본 핵심 자료 |
|---|---:|---|
| Superpowers | 9,015 | writing-good-tests 8,268; 주변 워크플로는 별도 |
| Matt Pocock | 3,549 | tests 2,214 + mocking 1,481; codebase-design 의존은 별도 |
| Addy Osmani | 16,517 | testing-patterns 및 browser skill은 별도 |
| ECC | 21,473 | tdd-guide 3,865; 실행·패키지 관련 자료는 별도 |
| Kirjolab | 1,421 | 채택 ADR·별도 라이선스 |
| Glebis | 33,980 | agent_prompts 15,544; 다른 references와 scripts는 별도 |

## 다른 후보에서 발견한 중요한 차이

### 이름이 TDD여도 절차는 같지 않다

Matt의 현재 SKILL은 **red-green**에 집중하고 리팩터링을 code review에 넘긴다. 가볍다는 이유로
그대로 채택하면 우리가 합의한 RGR의 마지막 단계가 사라진다. 공개 경계의 예시와 독립 기대값은
유용하지만 “내부는 절대 시험하지 않는다”까지 일반화하지 않는다. 안정적인 내부 도메인 계약이나
복잡한 순수 로직도 의미 있는 테스트 대상일 수 있다.
[원문](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/tdd/SKILL.md),
[테스트 예시](references/mattpocock/source/skills/engineering/tdd/tests.md).

Addy는 저장소의 README·CI에서 실제 명령을 찾고 cycle마다 focused 검증을 실행한다. 기존
프레임워크를 무시하고 JavaScript 예시 명령을 복사하는 문제를 피하는 데 도움이 된다. 브라우저
작업에 특정 MCP를 결합한 부분은 별도의 UI 검증 책임으로 분리하는 편이 적절하다.
[평가 사례](references/addyosmani/source/evals/cases/test-driven-development.json)는 보고된 버그
예시와 일반 불변식을 함께 검사해 과적합을 줄이도록 구성되어 있다. 평가 정의가 있다는 사실은
우리가 그 평가를 실행해 통과했다는 뜻이 아니다.
[원문](https://github.com/addyosmani/agent-skills/blob/6ca0cd7db39b41b1c37e26d335c507ee92382c6d/skills/test-driven-development/SKILL.md).

### 추적성은 좋지만 별도 장부는 필요하지 않다

ECC는 실제 RED의 원인을 분류하고 plan 작업과 테스트를 연결한다. 다만 여정을 위한 여러 테스트를
먼저 작성하는 예시, 80% coverage, 별도 .tdd.md, RED/GREEN checkpoint commit을 모두 가져오면
일상적인 작은 PR에도 절차가 커진다. 필요한 추적성은 plan의 검증 대상과 PR의 실행 근거 연결로
얻을 수 있다. **ECC가 100% coverage를 요구한다고 쓰면 부정확하다.**
[원문](https://github.com/affaan-m/ECC/blob/c9148d0bb239ed01a95724a5928b98cdf9c30658/skills/tdd-workflow/SKILL.md).

Glebis는 한 slice에 Test Writer·Implementer·Refactorer를 둔다. 상태 파일, 초기 분해 승인,
대화 모드의 단계별 승인, 반복 전체 suite·계층 검사는 TDD 핵심보다 넓다. 구현자에게 원 spec을
숨기는 [역할 프롬프트](references/glebis/source/tdd/references/agent_prompts.md)는 단일 테스트를
만족하는 hardcoding도 허용한다. TDD의 작은 임시 구현 자체가 결함이라는 뜻은 아니다. 다만
테스트 하나가 전체 계약을 대표하지 못하는 상황에서 문서까지 감추면 후속 요구·제약을 놓칠 수 있다.
우리의 spec→plan 인계 목적에는 불리한 설계라고 판단한다. 별도 역할 분리가 필요한 고위험 작업의
실험 대상으로는 남길 수 있다. Glebis에는 숫자 coverage gate가 없다.
[원문](https://github.com/glebis/claude-skills/blob/d0bc2063d00d9d1a76d9fde5cd098fd8c92a68bc/tdd/SKILL.md).

### 이미 존재하는 얇은 현지화 사례

Kirjolab은 Matt의 이전 판을 기존 spec·ADR·코드 규약에 맞춘 짧은 저장소 스킬로 바꿨다.
[ADR-219](references/kirjolab/source/docs/adrs/implemented/ADR-219-adopt-local-spec-and-tdd-skills.md)는
원문 전체 도입 시 생기는 다른 문서 체계·도구·승인 의존을 채택하지 않은 이유와 유지 비용을 설명한다.
이는 “몇 줄이면 효과가 입증된다”는 사례가 아니라 **같은 TDD 핵심을 팀의 기존 문서 체계에 맞게
줄일 수 있다는 설계 선례**다. 현재 Matt 판과도 같지 않으며 명시적 refactor는 보완해야 한다.
[원문](https://github.com/bebraw/kirjolab/blob/ac72a52670c537a4f468f994f4ed6ba855392733/.codex/skills/tdd/SKILL.md).

## 우리 설계에 참고할 조합

**한 후보를 통째로 표준화하기보다 작은 자체 TDD 스킬을 만들 때 다음 요소를 참고한다.**

1. Matt·Kirjolab: 기존 계약을 읽고 한 관찰 가능한 동작씩 진행. 승인된 경계는 다시 묻지 않음.
2. Superpowers: 의도한 실제 RED, 최소 GREEN, 필요한 REFACTOR, 독립적인 기대값과 테스트 품질.
3. Addy: 실제 저장소 명령·환경을 사용하고 작업 경계에서 관련 회귀를 확인.
4. ECC: 계획의 검증 대상과 관측된 테스트 근거 연결. 별도 원장은 만들지 않음.
5. Glebis: 테스트를 지우거나 약화해 GREEN을 만드는 행위 경계. 다중 에이전트는 필요할 때만 선택.

이것은 **참고 요소 선정**이다. 아직 새 스킬을 설치·작성해 실행한 결과가 아니며, spec·plan에 어떤
정보를 남길지는 [책임 배치 설계](responsibility-design.md)에서 별도로 판단한다.

## 보존·검토 범위

6개 저장소의 선택 원문 40개를 `references/<id>/source/<원래 경로>`에 보존했다. 모든 저장소의
MIT 라이선스와 Kirjolab 내부의 Matt 라이선스를 포함한다. 관련 직접 참조·주변 워크플로 중 비교에
필요한 부분만 수집했으므로 완전한 설치 패키지가 아니다. 스크립트는 원문 자료로만 저장했고
실행하지 않았다. 미수집 원문의 상대 링크는 고정 커밋의 원 저장소에서 확인한다.

Addy의 `../../references/testing-patterns.md`를 처음에 잘못 해석한 다운로드 404는 조사자의
경로 해석 오류였다. 올바른 저장소 루트 경로로 내려받았다. 상류 결함으로 세지 않는다.

행동·테스트 품질 비교와 오케스트레이션 비교는 Sol/high 하위 에이전트 두 개가 독립적으로 읽고
root가 원문과 종합했다. 인기도 순위나 외부 스킬의 성능을 입증하는 테스트는 수행하지 않았다.
