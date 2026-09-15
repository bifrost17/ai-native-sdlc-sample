# Reddit 원문 열람 기록

조사일 2026-09-12. Aside Browser로 아래 8개 공개 스레드의 본문과 로드된 댓글을 읽었다.
사용자가 중간에 질문을 **TDD 스킬 사용 여부**로 좁혔으므로 R06을 주요 근거로 삼고,
R01~R05는 스킬 사용이 명시된 부분과 일반 TDD 경험을 구분한다.

## 열람 범위

| ID | 원문·게시일 | 로드된 댓글 객체 / 화면의 전체 댓글 표시 | 로컬 본문·댓글 사본 |
|---|---|---|---|
| R01 | [Who has actually been using TDD consistently with Claude Code?](https://www.reddit.com/r/ClaudeAI/comments/1ot02iz/who_has_actually_been_using_tdd_consistently_with/), 2025-11-10 | 26 / 41 | [JSON](../sources/reddit/R01-consistent-tdd.json) |
| R02 | [Writing tests](https://www.reddit.com/r/vibecoding/comments/1qam0a6/writing_tests/), 2026-01-12 | 11 / 13 | [JSON](../sources/reddit/R02-writing-tests.json) |
| R03 | [How is TDD for Vibe Coding?](https://www.reddit.com/r/vibecoding/comments/1r58l0p/how_is_tdd_for_vibe_coding/), 2026-02-15 | 19 / 22 | [JSON](../sources/reddit/R03-tdd-failures.json) |
| R04 | [I've made about 20 apps… never wrote a test](https://www.reddit.com/r/vibecoding/comments/1vklmm8/ive_made_about_20_apps_some_in_production_for/), 2026-08-10 | 15 / 17 | [JSON](../sources/reddit/R04-no-tests.json) |
| R05 | [I feel like I've just had a breakthrough…](https://www.reddit.com/r/ClaudeAI/comments/1q85tlf/i_feel_like_ive_just_had_a_breakthrough_with_how/), 2026-01-09 | 25 / 95 | [JSON](../sources/reddit/R05-large-task-workflow.json) |
| R06 | [Is Superpowers still relevant?](https://www.reddit.com/r/ClaudeCode/comments/1vvgsia/is_superpowers_still_relevant/), 2026-08-22 | 65 / 70 | [JSON](../sources/reddit/R06-superpowers-relevant.json) |
| R07 | [Superpowers/Planning-focused skills worth using in Codex?](https://www.reddit.com/r/codex/comments/1ul5hyu/superpowersplanningfocused_skills_worth_using_in/), 2026-07-02 | 15 / 17 | [JSON](../sources/reddit/R07-superpowers-planning.json) |
| R08 | [Superpowers, is it really worth it?](https://www.reddit.com/r/codex/comments/1to6329/superpowers_is_it_really_worth_it/), 2026-05-26 | 27 / 27 | [JSON](../sources/reddit/R08-superpowers-worth.json) |

**위 숫자는 브라우저에서 확보한 범위를 밝히는 기록이며 응답자 수나 채택률의 분모가 아니다.**
삭제된 댓글 객체, 봇, 반복 답글이 들어갈 수 있고 접힌 댓글은 모두 펼치지 않았다.
R01에서는 Kotlin/Java 스킬 관련 답글을 추가로 펼쳐 확인했다. 각 파일의 `created` 절대 시각을 사용했다.
R04의 검색 도구 상대 날짜와 브라우저 상대 날짜가 달라, 원문 DOM의 2026-08-10을 채택했다.

## 스킬 사용 여부에 직접 도움이 되는 사례

| 사례 | 사용 상태와 근거 | 한계 |
|---|---|---|
| R06 OP `YUL438`, 2026-08-22 | Superpowers를 써 왔고 brainstorming·TDD·subagent 관련 스킬을 선호한다고 직접 밝힘. **TDD 관련 스킬 사용 자기보고** | ‘지난 1년’은 작성자의 회고. Fable/Opus high라는 도구 진술은 있으나 정확한 스킬 버전·호출 로그 없음 |
| R06 [`artofbullshit`](https://www.reddit.com/r/ClaudeCode/comments/1vvgsia/comment/p59gg2p/), 2026-08-22 | 모든 빌드에서 TDD를 따르게 하기 위해 Superpowers를 계속 사용한다고 함. **TDD를 이유로 지속 사용** | 다음 날 [답글](https://www.reddit.com/r/ClaudeCode/comments/1vvgsia/comment/p5c7kss/)은 Superpowers만 필수라는 뜻이 아니라, 모든 스킬을 제거하고 모델 기억에 맡기기 불안하다는 뜻으로 설명. 실행 검증 아님 |
| R06 [`rubanbhatia`](https://www.reddit.com/r/ClaudeCode/comments/1vvgsia/comment/p5d8r0n/), 2026-08-23 | 작은 변경마다 TDD를 하고 문서를 반복 생성하는 점을 비판. **전면 적용에 대한 비판·수정 희망** | 본인이 TDD 스킬을 껐다고는 하지 않음. 중단 사례로 분류하지 않음 |
| R06 [`cartoonist498`](https://www.reddit.com/r/ClaudeCode/comments/1vvgsia/comment/p59ddh8/), 2026-08-22 | 토큰·시간 부담 대비 효과가 적어 Superpowers를 중단하고 Fable/Opus orchestration을 쓴다고 함. **프레임워크 중단** | 모든 TDD 스킬·테스트를 포기했는지 미상. 프레임워크 전체 비용을 TDD 단독 비용으로 귀속할 수 없음 |
| R06 [`seatlessunicycle`](https://www.reddit.com/r/ClaudeCode/comments/1vvgsia/comment/p5a45v5/), 2026-08-22 | Superpowers를 수개월 안 쓰고 Matt Pocock 쪽으로 옮겼다고 함. **워크플로 전환** | Matt의 어떤 스킬인지 명시하지 않아 TDD 스킬 전환으로 확정할 수 없음. 다른 사용자 `Seerix`는 grill-me만 쓴다고 답함 |
| R01 [`rustyrazorblade`](https://www.reddit.com/r/ClaudeAI/comments/1ot02iz/comment/no7q7o8/), [후속 답글](https://www.reddit.com/r/ClaudeAI/comments/1ot02iz/comment/no7torg/), 2025-11-11 | TDD+정적분석, SuperClaude와 개인 Kotlin/Java 스킬을 쓴다고 구체화 | SuperClaude는 Superpowers와 다른 명칭이다. 개인 스킬이 TDD 전용인지 원문 없음. **TDD 실사용 + 일반 스킬 사용**, 이름 있는 TDD 스킬 사용은 미확정 |
| R05 OP `wynwyn87`, 2026-01-09 | Go용 스킬, Superpowers brainstorming/writing-plans, 모든 신규 기능 TDD를 함께 사용한다고 함 | TDD 스킬의 정확한 이름/호출은 제시하지 않음. TODO를 작게 나눠 계획 누락·문서 부담을 줄였다는 자기보고가 글의 주제 |

R05의 `crunchy_code`는 세 에이전트 TDD 글을 소개하면서 **자기는 아직 사용하지 않았다**고 명시한다.
추천 링크가 구체적이라는 이유로 실사용자로 세지 않았다. R04의 `JT-1963`는 Superpowers가 테스트를
많이 만든다고 말하지만 테스트 수만으로 TDD 스킬의 RED 실행을 인정하지 않았다.
자동 요약 봇이 ‘합의’나 ‘많은 사용자가 중단’이라고 쓴 문장은 분석 근거에서 제외했다.

## 배경: 스킬 여부와 별개인 TDD·테스트 경험

| 원문 | 실제 서술 | 해석 |
|---|---|---|
| R01 [`Dry-Willingness-506`](https://www.reddit.com/r/ClaudeAI/comments/1ot02iz/comment/no2spjf/), 2025-11-10 | 사람이 테스트를 쓰거나 AI 테스트를 검토한 뒤 Claude로 Green, 사람이 Refactor 판단 | 상세 RGR 사용 자기보고. 스킬 이름 없음 |
| R01 [`lev606`](https://www.reddit.com/r/ClaudeAI/comments/1ot02iz/comment/no79lxz/), 2025-11-11 | 큰 기능·권한 같은 민감한 부분에 TDD 사용 | 선택적 TDD 자기보고. 스킬 여부 미상 |
| R01 [`cogencyai`](https://www.reddit.com/r/ClaudeAI/comments/1ot02iz/comment/no1r6co/), 2025-11-10 | 대체로 테스트를 먼저 쓰지 않고 계약 경계의 동작 테스트를 AI에 요청 | 구현 후 테스트 선호. 스킬 여부 미상 |
| R01 [`psychometrixo`](https://www.reddit.com/r/ClaudeAI/comments/1ot02iz/comment/no1jkc9/), 2025-11-10 | 모델을 RGR 순서로 유지하는 데 시간이 많이 들었다 | 순서 준수 비용 경험. 훅은 들은 이야기로만 구분 |
| R01 [`Peerless-Paragon`](https://www.reddit.com/r/ClaudeAI/comments/1ot02iz/comment/no1558i/), 2025-11-10 | 첫 프로젝트에서 약 3,000 unit tests·높은 coverage에도 변경이 어려워졌다고 함 | **TDD를 계속하되 Testing Trophy 방향으로 테스트 전략을 바꿈. TDD 포기 아님.** 수치·프로덕션 상태는 자기보고 |
| R02 OP `Lowkey_Hi` | 구현 코드를 AI에게 보내 테스트를 만들게 하지만 품질이 낮다고 함 | 구현 후 테스트 경험. 다른 댓글의 TDD 강제 권장은 사용 증거 아님 |
| R03 OP `NullzeroJP`, 댓글 `Ok-Hotel-8551` | TDD 지시에도 코드와 맞춘 mock/stub 테스트가 생기거나 구현부터 하고 Green tests를 붙임 | **TDD 요청과 실행의 차이**. GLM/Claude Code 진술은 있으나 호출·실행 로그 없음 |
| R03 `guywithknife` | strict RGR, 테스트 작성과 구현의 맥락 분리를 사용한다고 설명 | 명시적 사용 자기보고이지만 이름 있는 스킬 증거는 아님 |
| R04 OP `10c70377` | 약 20개 앱과 일부 사업용 배포를 주장. PC/휴대폰 수동 확인만 하고 자동화 테스트를 쓰지 않았다고 함 | 무자동시험 자기보고. **아무 검증도 안 했다는 뜻은 아님.** 앱·배포·회귀 품질은 미검증 |

## 접근과 보관 한계

- 본문·댓글은 실제 화면을 snapshot으로 먼저 읽고, 공개 post/comment DOM만 별도 JSON으로 보관했다.
  JSON에는 텍스트와 원문 HTML 조각, 작성자·시각·permalink가 있다. 서버 전체 HTML이나 Reddit 전체 댓글 export가 아니다.
- 같은 이름의 `-snapshot.txt`는 접근성 읽기 사본이다. 계정 선택·프로필 정보 줄은 제거했다.
  광고나 UI 문구가 남는 접근성 사본보다 공개 본문만 추출한 JSON을 인용용으로 사용한다.
- 초기 일회성 Aside 호출의 탭 연결 실패와 `role:main` selector 오류가 있었다. 이후 지속 세션에서
  관찰한 `main` 요소로 재열람했다. 실패 호출은 원문 열람 증거로 세지 않았다.
- R05는 95개 중 25개 댓글 객체만 확보했다. 미열람 댓글의 방향을 추정하지 않았다.
- 검색어와 종료 기준은 [조사 방법](../methodology.md)에 있다. 추가 스킬 질문의 Reddit 스레드는
  [영문 스킬 조사](skills-english.md)에 별도로 수록한다. 해당 2개도 R07/R08로 Aside에서 재열람했다.
  R08에는 자체 TDD 스킬 맥락을 밝히는 `tonyboi76`의 `onz74u1` 부모 댓글과 후속 `onzk3lr`를 함께 보관했다.
  댓글 표시 수와 로드된 객체 수가 같아도 삭제된 내용이나 과거 수정본 전체를 확보했다는 뜻은 아니다.
