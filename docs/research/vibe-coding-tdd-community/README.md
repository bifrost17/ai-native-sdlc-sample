# 바이브 코딩에서 TDD 스킬을 사용하는가: 커뮤니티 조사

조사일: **2026-09-12**. 사용자 요청에 따라 일반 TDD 관행에서 **에이전트용 TDD 스킬의 실제 사용·유지·선택·중단**으로 질문을 좁혔다.
이 문서는 공개 경험을 조사한 보고서다. 템플릿 정책을 변경하거나 TDD와 구현 후 테스트의 효과를 실험한 결과가 아니다.

## 답

**TDD 스킬을 실제로 사용하고, TDD를 유지하기 위해 계속 사용한다는 개발자가 확인된다.**
동시에 적용 범위가 과도하다는 비판, 더 가벼운 스킬로 옮기려는 선택, Superpowers 전체를 중단한 경험도 있다.
따라서 ‘아무도 안 쓰는 이론’이라고 보기도 어렵고, ‘바이브 코딩의 보편적인 기본값’이라고 결론 내리기도 어렵다.

스킬 사용 여부로 좁히면 **구체적인 도구와 선택을 확인하기가 더 쉬워진다.** 다만 Superpowers를 쓰는
사람이 반드시 TDD 스킬을 쓰는 것은 아니고, Superpowers를 지웠어도 다른 TDD 스킬을 쓸 수 있다.
이번 탐색에서는 이 질문을 직접 측정하면서 모집 경로·분모가 공개된 대표 설문을 찾지 못했다.
**전체 사용률이나 ‘대략 절반’ 같은 비율은 산출하지 않는다.** 검색으로 고른 경험담의 비중도 전체 채택률로 해석할 수 없다.

## 직접 확인한 사용과 선택

아래는 본인 경험을 말한 공개 글·댓글이다. ‘확인’은 **그 발언의 존재와 맥락을 확인했다**는 뜻이며,
개인 작업의 모든 호출·실패·통과 이력을 독립적으로 검증했다는 뜻은 아니다.

| 사례·시점 | 확인한 내용 | 판정과 한계 |
|---|---|---|
| `YUL438`, r/ClaudeCode, 2026-08-22 | Superpowers를 써 왔고 brainstorming·TDD·subagent 관련 스킬을 선호한다고 직접 설명. Fable·Opus high 사용도 언급 | **TDD 관련 스킬 사용 자기보고.** 정확한 버전·호출 로그는 없음. [원문](https://www.reddit.com/r/ClaudeCode/comments/1vvgsia/is_superpowers_still_relevant/) · [로컬](sources/reddit/R06-superpowers-relevant.json) |
| `artofbullshit`, 같은 스레드, 2026-08-22~23 | 모든 빌드에서 TDD를 따르도록 하기 위해 계속 쓴다고 설명. 답글에서는 Superpowers만 필수라는 뜻이 아니라 모든 스킬을 제거하고 모델 기억에 맡기는 것이 불안하다고 명확히 함 | **TDD를 이유로 지속 사용.** 스킬 필요성에 관한 경험·신뢰이며 실제 준수율 측정은 아님. [댓글](https://www.reddit.com/r/ClaudeCode/comments/1vvgsia/comment/p59gg2p/) · [후속 설명](https://www.reddit.com/r/ClaudeCode/comments/1vvgsia/comment/p5c7kss/) · [로컬](sources/reddit/R06-superpowers-relevant.json) |
| `rubanbhatia`, 같은 스레드, 2026-08-23 | 작은 변경마다 TDD를 하고 큰 Markdown 문서를 반복 생성하는 것을 비판 | **일괄 적용을 줄이길 바라는 의견.** 실제 TDD 스킬 비활성화 완료라고는 하지 않음. [댓글](https://www.reddit.com/r/ClaudeCode/comments/1vvgsia/comment/p5d8r0n/) · [로컬](sources/reddit/R06-superpowers-relevant.json) |
| `cartoonist498`, 같은 스레드, 2026-08-22 | 시간·토큰 부담에 비해 결과 개선이 적다고 느껴 Superpowers 사용 중단. 별도 모델 orchestration으로 전환 | **프레임워크 중단 자기보고.** TDD 스킬 전부를 중단했는지, 비용 중 얼마가 TDD 때문인지는 모름. [댓글](https://www.reddit.com/r/ClaudeCode/comments/1vvgsia/comment/p59ddh8/) · [로컬](sources/reddit/R06-superpowers-relevant.json) |

한 토론 안에서 상반된 선택이 보인다는 점은 유용하지만, 이 네 행을 네 유형의 모집단 비율로 바꾸면 안 된다.
세부 사용자·대체 스킬 사례는 [영문 스킬 조사](working/skills-english.md), [국내 스킬 조사](working/skills-korean.md)에 이어진다.

다른 두 토론에서는 **대체 스킬을 실제 쓰는 사람**과 **끄고 비교 중인 사람**까지 구별할 수 있었다.

| 작성자·시점 | 직접 설명 | 판정 |
|---|---|---|
| `elwutang`, 2026-07-02 | 직장에서는 Claude, 개인 작업에서는 Codex와 Superpowers 사용. 이전에는 모델이 구현으로 건너뛰었는데 Superpowers에서 Red→구현→Green이 된다고 설명 | **지속 사용 + 순서 준수 자기보고.** 별도 로그는 없음. 완료 뒤 E2E 테스트도 작성·실행해 혼합 검증을 사용. [댓글](https://www.reddit.com/r/codex/comments/1ul5hyu/comment/ov1yeqj/) · [로컬 읽기 사본](sources/skills-english/reddit-1ul5hyu-selected.txt) |
| `soggy_mattress`, 2026-07-02 | TDD 스킬의 적용 범위가 지나치고 unit tests 통과를 작동 보증처럼 다룬다고 비판. 스킬들을 며칠 끄고 비교 중이라고 설명 | **TDD 스킬 비판 + 전체 스킬 중단 시험.** 영구 중단이나 이후 결과는 미상. [댓글](https://www.reddit.com/r/codex/comments/1ul5hyu/comment/ov1xxug/) · [로컬 읽기 사본](sources/skills-english/reddit-1ul5hyu-selected.txt) |
| `sarcasmguy1`, 2026-05-26 | Superpowers의 TDD 대신 더 가벼운 Matt Pocock의 TDD 스킬을 쓴다며 정확한 파일 링크 제시 | **다른 TDD 스킬 현재 사용.** Superpowers 비판을 TDD 포기로 셀 수 없는 직접 사례. [댓글](https://www.reddit.com/r/codex/comments/1to6329/comment/onyry7t/) · [로컬 읽기 사본](sources/skills-english/reddit-1to6329-selected.txt) |
| `Spirited-Car-3560`, 2026-05-26 | Superpowers를 시험한 뒤 삭제·되돌렸으며, TDD 스킬만 나중에 자체 하네스에 넣을 수 있다고 설명 | **프레임워크 중단 완료 / TDD 스킬 이식은 예정.** 아직 이식한 사용자로 세지 않음. [후속 댓글](https://www.reddit.com/r/codex/comments/1to6329/comment/onzgv1h/) · [로컬 읽기 사본](sources/skills-english/reddit-1to6329-selected.txt) |

국내에서는 **호출 명령까지 공개한 실제 운영 사례**도 찾았다.

| 작성자·시점 | 스킬과 실제 경험 | 확인 범위 |
|---|---|---|
| 김예림·비브로스, 2026-06-10 | `/tdd-pipeline:run`으로 여러 에이전트를 실행하는 사내 TDD 플러그인을 설명하며 한 달간 기능 구현에 사용했다고 보고. 모든 프로젝트에 필수로 쓸 계획이 아니어서 **명시적 TDD 요청 때만 호출**하도록 구성 | 이름·진입점·선택 정책이 구체적이다. 운영 실패와 평가 예시도 있으나 원시 실행 로그·플러그인 저장소 전체는 미공개. 테스트 묶음→구현→리뷰→선택적 Refactor 방식. [원문](https://boostbrothers.github.io/2026-06-10-claude-code-tdd-subagent-harness/) · [로컬](sources/skills-korean/boostbrothers-tdd-subagent-harness.html) |
| Tony Cho, 2026-02-08 | 개인 TDD Planning 스킬을 사용했지만 병렬 작업의 호출 망각·환경별 설정 부담 때문에 자주 생략. 이후 Superpowers로 옮겨 TDD 워크플로를 활용한다고 설명 | **개인 스킬 사용·생략·프레임워크 전환 자기보고.** Superpowers TDD 하위 스킬의 호출 로그는 없음. [원문](https://flowkater.io/posts/2026-02-08-superpowers-introduction/) · [로컬](sources/skills-korean/flowkater-superpowers.html) |
| 햄스터아저씨, 2026-03-29 | Opus 4.6로 CLI·웹앱 3과제를 Superpowers 사용/미사용으로 비교. 일회성·프로토타입에는 과하고 유지할 서비스에는 가치가 있다고 판단 | **실제 프레임워크 비교 + 조건부 사용 권고.** 이후 일상 작업에서 켜고 끄는 지속 관행은 미공개. TDD 단독 비교·RED 실행 증거 아님. [원문](https://blog.hamsterapp.net/review-claude-code-superpowers/) · [로컬](sources/skills-korean/hamster-superpowers-review.html) |

햄스터아저씨가 보고한 합계는 36,975→60,239토큰, 179→483초다. 단일 비교이고, 계획·질문·리뷰까지
함께 달라져 **TDD 스킬 때문에 이만큼 증가했다**고 해석할 수 없다. 장기 재작업 비용이나 동일 인수 기준에 따른
최종 품질을 통제한 실험도 아니다. 숫자는 보급률과 무관하다.

## 무엇을 ‘TDD 스킬 사용’으로 세어야 하는가

| 관찰 | 말할 수 있는 것 | 아직 모르는 것 |
|---|---|---|
| TDD 스킬 설치·다운로드·저장소 star | 관심 또는 설치 흔적 | 실제 작업에서 호출하는지, 유지하는지 |
| Superpowers로 계획·리뷰 사용 | 프레임워크 사용 | TDD 스킬까지 쓰는지 |
| 이름 있는 TDD 스킬을 계속 쓴다는 본인 설명 | 실사용 자기보고 | 빈도와 실제 RED 실행·검증 품질 |
| 테스트부터 하라고 지시 | test-first 의도 | 모델이 지시대로 했는지 |
| 의도한 동작으로 실패한 테스트→구현→통과 기록 | 해당 작업에서의 공개 test-first 실행 | 다른 작업의 빈도, 결과의 완전성 |

R01의 `rustyrazorblade`는 TDD와 **SuperClaude**·개인 Kotlin/Java 스킬 사용을 함께 말한다.
하지만 이름이 비슷하다는 이유로 Superpowers TDD 사용자로 바꾸지 않았다.
R05 작성자도 Superpowers 계획 스킬과 TDD를 함께 언급하지만 TDD 스킬 호출 자체는 명시하지 않는다.
[구체 판정과 원문](working/reddit.md)

조사일에 고정한 실제 스킬 정의도 차이가 있다. Superpowers의 `test-driven-development`는 신규 기능·버그 수정 등
넓은 범위에 테스트 선행을 요구하고, 버리는 프로토타입·생성 코드·설정 파일 예외에는 사람과 상의하도록 한다.
Matt Pocock의 `tdd`는 사용자와 합의한 공개 경계에서 하나씩 Red→Green을 반복하며,
**리팩터링은 루프 밖의 리뷰 단계**로 구분한다. 이 둘을 동일한 교과서 RGR 절차로 묶지 않았다.
[Superpowers 고정 원문](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/skills/test-driven-development/SKILL.md) ·
[Matt Pocock 고정 원문](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/tdd/SKILL.md) ·
[로컬 정의·버전 목록](sources/skill-definitions/manifest.json)

이것은 **2026-09-12에 확인한 정의**다. 과거 댓글 작성자가 이 버전을 썼다고 소급하지 않으며,
스킬 안의 ‘더 빠르다’ 같은 주장을 효과 검증 결과로 채택하지 않는다. 제3자 스킬은 연구 자료로만 읽었다.

## 사용 이유와 불편에서 반복되는 쟁점

**유지 이유는 에이전트의 작업 순서를 일정하게 만들고 기대 동작을 먼저 고정하는 데 있다.**
이는 위의 TDD 스킬 지속 사용 설명과 연결된다. 일반 TDD 경험에서도 사람이 테스트를 작성·검토하고,
구현 담당 에이전트가 테스트를 바꾸지 못하게 하거나, 작업을 작게 나누는 방식이 나온다.
예를 들어 `Dry-Willingness-506`은 사람이 Red를 검토하고 Claude로 Green, 사람이 Refactor를 판단한다고 설명했다.
[당사자 댓글](https://www.reddit.com/r/ClaudeAI/comments/1ot02iz/comment/no2spjf/) · [로컬](sources/reddit/R01-consistent-tdd.json)

**불편은 순서 유지 비용, 불필요한 테스트, 프레임워크 전체의 시간·토큰 부담이다.**
그러나 사람이 호소하는 부담을 TDD 스킬 하나의 비용으로 분해한 측정치는 없다. 모델·도구·과제·개인 숙련도도 섞여 있다.
Superpowers 전체의 subagent·계획·리뷰 비용을 TDD 비용으로 단정하지 않는다.
[지속 사용과 중단이 함께 있는 토론](https://www.reddit.com/r/ClaudeCode/comments/1vvgsia/is_superpowers_still_relevant/) · [로컬](sources/reddit/R06-superpowers-relevant.json)

**TDD 지시를 넣어도 검증 품질과 실행 순서는 따로 확인해야 한다.** r/vibecoding의 경험담에는
TDD를 요청했는데 모델이 구현을 먼저 하거나, mock·stub에 맞춘 테스트를 만들어 통과시키는 문제가 나온다.
이는 모든 모델이 그러거나 TDD가 실패한다는 실험 결과가 아니라, 지시의 존재를 실행 증거로 볼 수 없다는 사례다.
[원문](https://www.reddit.com/r/vibecoding/comments/1r58l0p/how_is_tdd_for_vibe_coding/) · [로컬](sources/reddit/R03-tdd-failures.json)

**테스트 수와 TDD 채택은 제품 품질을 대신하지 않는다.** `Peerless-Paragon`은 약 3,000 unit tests를 만든 뒤
변경이 어려워졌다고 썼지만, 이후 TDD를 버린 것이 아니라 Testing Trophy를 참고해 테스트 전략을 바꿨다.
이를 ‘TDD 포기’로 인용하면 원문의 결론을 뒤집게 된다.
[원문 댓글](https://www.reddit.com/r/ClaudeAI/comments/1ot02iz/comment/no1558i/) · [로컬](sources/reddit/R01-consistent-tdd.json)

## 일반 TDD 경험은 배경으로 분리

스킬 사용을 밝히지 않은 사례를 스킬 채택자에 합산하지 않았다. 다만 선택 배경을 이해하는 데 도움이 된다.

- HN의 `dkn`은 일부 영역만 TDD, 나머지는 경계의 integration tests를 택한다고 설명한다.
  `mlmonkey`는 기존 코드를 모델에 보여 주고 테스트를 작성시킨다. [HN 원문](https://news.ycombinator.com/item?id=48495660) ·
  [구현 후 작성](https://news.ycombinator.com/item?id=48493898) · [HN 조사와 보관 링크](working/hn.md)
- 국내 에피는 사람이 기대 동작을 정의한 테스트를 먼저 두고 Claude Code에 구현을 맡긴다고 설명한다.
  강준현은 Copilot의 테스트·구현·리팩터링용 prompt를 선택 실행하는 팀 경험을 썼다.
  **test-first 또는 TDD 경험이지, 이 사실만으로 SKILL.md 기반 TDD 스킬 채택은 아니다.**
  [에피 원문](https://maily.so/effy/posts/8do7kyqnrgq) ·
  [강준현 원문](https://junhyunny.github.io/ai/ai-agent/copilot/prompt/improve-development-process-by-vibe-coding/) · [국내 원문·판정](working/korean.md)
- 자동화 테스트 없이 PC·휴대폰에서 수동 확인하고 일부 앱을 배포했다는 자기보고도 있다.
  ‘자동 테스트 없음’은 ‘검증을 전혀 안 함’과 다르며, 해당 앱의 운영 품질은 확인되지 않는다.
  [원문](https://www.reddit.com/r/vibecoding/comments/1vklmm8/ive_made_about_20_apps_some_in_production_for/) · [로컬](sources/reddit/R04-no-tests.json)

## 우리 SDLC에 적용할 수 있는 해석

이번 결과는 **TDD 스킬을 선택지로 제공할 실사용 근거**를 보태지만, 전 작업에서 강제할 효과 근거는 아니다.
반대로 스킬에 대한 불만만으로 test-after가 더 낫다고 결론 낼 수도 없다. 다음은 커뮤니티 경험을 바탕으로 한 설계 해석이다.

1. 계획에서 테스트 접근과 TDD 스킬 적용 범위를 함께 정한다. ‘Superpowers 사용’이라는 한 줄만으로 테스트 전략을 대체하지 않는다.
2. TDD 스킬을 고르면 핵심 기대 동작·테스트 품질·의도한 실패를 확인한다. 스킬 호출이나 테스트 개수만 완료 증거로 보지 않는다.
3. 구현 후 테스트나 혼합 방식을 골라도 구현과 독립적으로 정한 인수 조건, 실제 경계·회귀 검증을 유지한다.
4. 스킬을 빼거나 바꾸는 이유가 토큰·시간·테스트 유지 비용이라면, 어떤 검증을 대신할지도 계획에 남긴다.

플레이북을 북극성으로 삼는 기존 원칙과 연결하되, **이번 조사에서 플레이북·두 템플릿의 정책은 수정하지 않았다.**
이전 비교 연구는 [TDD 대 구현 후 테스트 조사](../tdd-vs-test-after/README.md)에서 별도로 볼 수 있다.

## 조사 범위·원문·재검토

2025-02-01~2026-09-12의 공개 자료를 탐색했다. 브라우저에서 읽은 Reddit 8개 스레드,
HN 핵심 6개와 보조 1개, 국내 일반 경험 5개와 보조 1개에 더해 스킬 중심 자료를 추가했다.
서로 같은 경험의 재게시·번역, 작성자의 반복 댓글, 스킬 소개·홍보는 독립 사용 사례로 세지 않았다.
상세 채택·제외·검색·열람 범위는 아래 기록에서 확인할 수 있다.

- [조사 방법과 추가 지시 반영](methodology.md)
- [Reddit 본문·댓글 확인](working/reddit.md), [영문 스킬 경험](working/skills-english.md), [국내 스킬 경험](working/skills-korean.md)
- [HN 일반 경험](working/hn.md), [국내 일반 경험](working/korean.md)
- [원문 보관 안내](sources/README.md), [URL·로컬 파일·해시 통합 목록](sources/manifest.json)
- [독립 검토와 반영](review.md), [파일·링크·해시 확인 결과](artifact-check.json)

일부 커뮤니티 원문은 서버 HTML을 보관했고, Reddit은 Aside에서 로드된 공개 본문·댓글의 텍스트와
HTML 조각 및 접근성 사본을 저장했다. **숨겨진 댓글 전체나 전체 서버 원문을 내려받았다는 뜻은 아니다.**
본문의 직접 경험도 대부분 자기보고이며, 스킬 호출 로그와 실제 Red/Green 실행을 연결하는 증거는 부족하다.
검색 가능성·자기선택·주제 선택·댓글 정렬·미열람 답글 때문에, 이 자료에서 사용률을 만드는 것은 적절하지 않다.
