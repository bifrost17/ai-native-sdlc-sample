# 북극성 원문 발췌

기준: maker efa7339의 docs/verification/north-star-playbook.html.
요구·설계/plan/skill/병렬/feedback 원문 영역의 텍스트를 추출했다. details.verify 주석 제외.
HTML의 표·도식은 원본에서 확인한다. 출처·번역은 기존 북극성의 것을 유지한다.

03 / 14

요구사항과 design

원문 보기

product owner가 intent.md를 승인하면 Claude가 그것을 받아 요구사항·설계 스펙을 만든다. 이 과정은 브랜드·보안·compliance·UX를 다루는 조직의 skill이 이끈다.

product owner는 그 스펙을 review하지만 직접 쓰지는 않는다. 이 과정의 목표는 우려 지점이 표시된 채로, 엔지니어링 팀이 계획을 세울 기준이 될 스펙을 만드는 것이다.

프런트엔드 작업이 가장 분명한 예다. intent.md가 수락되면 product owner는 그 intent.md를 바탕으로 Claude Design(베타)에서 설계를 mock으로 만들고, mock을 반복해 다듬은 뒤, build하도록 Claude Code로 내보낸다.

무엇이 달라지는가

Traditional

요구사항과 설계는 서로 다른 팀이 수행하는 별개의 단계다. 분석가가 아이디어를 요구사항으로 정식화하고, 그다음 디자이너가 그 요구사항을 다시 해석해 설계로 옮긴다. 이 분리는 책임 소재를 위해 존재하지만, 느리고 손실이 크다.

AI-native

두 단계가 prompt로 진행되는 하나의 session에서 함께 일어난다. Claude가 intent.md를 받아 조직의 skill에 제약된 요구사항·설계 스펙을 만들고, 우려 지점을 표시한다.

시작하기

- 전제 조건: intent.md 파일을 작성하고, 브랜드·보안·compliance·UX 정책을 skill로 써 둔다.

- 인프라: Claude에 접근할 수 있는 product owner. 엔지니어링 역량은 필요 없다.

실행 방법

- product owner가 조직의 skill을 쓸 수 있는 상태로 session을 열고 intent.md를 첨부한다.

- product owner의 prompt는 intent를 가리키고, 제약을 명시하고, 표시된 우려 지점을 요구한다. 처음에는 손으로 실행하고, 그다음 조직 수준의 슬래시 명령으로 성문화한다. 거기서부터는 intent home에서 intent.md를 수락하는 것을 trigger로 삼아, merge에 발화하는 non-interactive job이 조직의 skill을 로드한 채로 그 패스를 실행하고 spec.md를 pull request로 commit하게 한다(plumbing은 Stage 5: Deploy의 CI/CD play가 다룬다). 그 시점부터 product owner가 처음 관여하는 지점은 review다.

- 같은 product owner가 그 스펙을 아이디어와 대조해 review한다. 스펙이 명시된 문제를 푸는가, 그리고 intent.md의 미결 질문은 답이 나왔거나 이월됐는가?

- 표시된 우려 지점은 분석가라면 escalation했을 지점이므로 먼저 처리하라. product owner는 엔지니어링이 스펙을 보기 전에 각 항목을 해당 policy owner와 함께 해소한다.

- spec.md를 intent.md 옆에 commit하라. 이 파일 쌍이 무엇을 요청했고 무엇을 결정했는지를 기록한다.

- product owner가 스펙과 intent를 build로 진행시킬지 결정하고, 조직이 고위험으로 분류하는 사안은 tech lead와 상의한다. 이 판단은 언제나 사람 동료가 내리며, 스펙을 수락하는 것이 Stage 3: Build의 plan mode play를 시작시킨다.

실제 모습

prompt:

첨부한 intent.md를 읽고, 그것을 우리 기존 코드베이스에 통합하기 위한 요구사항·설계 스펙을 만들어라. 사용할 수 있는 skill을 적용해 계획이 우리 브랜드 가이드라인, 보안 정책, UX 표준을 따르게 하라. 스펙을 spec.md로 온전히 문서화해 엔지니어링 팀에 넘길 수 있게 하라. 우려 지점은 무엇이든, 특히 서로 충돌하는 정책을 동시에 만족시킬 수 없는 곳을 분명히 기술하라.

governance 고려사항

정책 충돌이 몇 주 뒤 review에서 발견되는 대신, 살아 있는 정책을 스펙을 쓰는 동안 읽어 적용한다. 조직의 skill이 스펙의 제약으로 적용된다. 스펙, 그것을 만든 prompt, 그리고 효력을 가진 skill 버전이 모두 version control에 기록된다. product owner가 스펙을 승인하고, 표시된 우려 지점을 지정된 policy owner에게 보낸다.

측정 방법

- leading indicator: 같은 변경의 intent.md commit과 spec.md commit 사이 경과 시간(Git 타임스탬프 둘)을 기존 요구사항+설계 사이클과 비교한 값.

- lagging indicator: build 시작 이후의 요구사항 재작업. 같은 변경에서 첫 plan.md commit보다 날짜가 늦은 spec.md commit을 센다. Git log가 이 값을 바로 준다.

04 / 14

기본 출발점으로서의 Claude Code plan mode

원문 보기

엔지니어는 Claude Code session을 plan mode로 시작하고, Stage 2: Design에서 승인된 spec.md를 Claude에게 주고, Claude가 자신을 인터뷰하게 두면서 만족할 때까지 계획을 다듬는다.

무엇이 달라지는가

Traditional

엔지니어가 설계를 읽고 코드를 쓰기 시작한다. 어떤 파일과 어떤 test인지까지 포함해 변경을 어떻게 할지는 엔지니어의 머릿속에, 잘해야 ticket 댓글에 남는다. 다른 누구도 그것을 review할 수 없다. reviewer가 처음 보는 것은 완성된 diff이고, 그때가 되면 재작업은 느리다.

AI-native

작업은 Claude가 plan mode에서 만든 문서화된 계획으로 시작하는데, plan mode에서 Claude는 아무것도 바꾸지 않고 코드베이스를 읽을 수 있다. 엔지니어가 코드를 쓰기 전에 계획을 고치고, 승인된 판을 plan.md로 commit해 이후 단계가 대조할 수 있게 한다.

시작하기

- 전제 조건: intent artifact(intent.md 또는 spec.md)가 있다면 그것, 그리고 CLAUDE.md 파일이 도움이 된다.

- 인프라: repository에 접근할 수 있는 Claude Code.

실행 방법

- 엔지니어가 Claude와 함께 session을 plan mode로 시작한다.

- 엔지니어가 intent.md와 spec.md를 Claude에게 주고, 변경되는 파일, 작업 순서, 그리고 그것을 증명하는 test를 명시한 구현 계획을 요청한다.

- 그 변경이 무엇을 깨뜨릴 수 있는지, 어느 단계가 가장 위험한지, Claude가 하지 않기로 고른 다른 선택지는 무엇인지를 물어 계획을 따져라.

- 그 대화를 한 번도 보지 않은 엔지니어가 계획만으로 그 변경을 구현할 수 있을 때까지 반복하라.

- 승인된 계획을 plan.md로 commit하라. 그 계획은 audit trail에 합류하고, PR review play(Stage 5: Deploy)가 최종 diff를 그것과 대조한다.

- 계획을 수락하고 Claude가 구현하게 하라. 계획이 탄탄하면 구현은 대개 한 번의 패스로 끝난다.

- 구현이 계획에서 벗어나면 같은 commit에서 plan.md를 갱신하라. 둘 사이의 동기화를 강제하는 hook을 쓰는 것을 고려하라.

실제 모습

plan.md:

# Plan: claims status self-service (from intent.md 2026-06-02)

## Files that change

portal/src/claims/StatusPanel.tsx (new), claims-api/routes/status.py, claims-api/tests/test_status.py

## Order of work

1. Add the status endpoint behind existing auth.
2. Panel against the endpoint.
3. Wire into the portal nav.

## Risks

The claims-core API rate-limits at 50 rps; the panel must cache.

## Proof

test_status.py covers the four claim states; screenshot matches the approved mock.

governance 고려사항

설계 review는 코드가 생성되기 전에, 방향을 바꾸는 일이 아직 문서 편집으로 끝나는 시점에 일어난다. 엔지니어가 계획을 수락하기 전까지 Claude가 파일을 편집할 수 없으므로, plan mode가 이것을 스스로 강제한다. 계획과 그 개정본은 누가 그것을 수락했는지와 함께 기록된다. 일상적인 변경은 엔지니어가 승인하고, 조직이 고위험으로 분류하는 것은 tech lead나 아키텍트에게 간다.

측정 방법

- leading indicator: 첫 구현 패스에서 merge되는 변경의 비율, 그리고 계획 승인부터 merge된 PR까지의 시간 — 필요한 데이터는 PR 메타데이터 안에 있다.

- lagging indicator: 변경당 재작업 사이클, 이번에도 PR 메타데이터에서, 그리고 merge된 diff가 commit된 plan.md와 여전히 일치하는 빈도.

auto mode의 Claude Code

Claude Code는 auto mode로도 돌 수 있는데, 이 모드에서는 엔지니어가 계획을 다듬어 승인하면 Claude가 편집마다 prompt를 받지 않고 각 변경을 적용한다. 이후 play들의 guardrail이 성숙하면(조정된 CLAUDE.md, 정책을 담은 skill, 안전하지 않은 동작을 막는 hook, 그리고 Claude가 돌릴 수 있는 test suite), auto mode는 일상적인 작업 — 촘촘한 spec.md, 작은 blast radius, test가 이미 덮고 있는 코드 — 의 기본이 된다.

이제 전환은 사용자가 agent의 편집을 지켜보며 동작을 review하는 방식에서 벗어나, 더 긴 자율 session 뒤에 artifact를 review하는 방식으로 향한다. auto mode는 worktree와 함께 쓰면 개인과 팀 전반의 병렬성을 한층 더 열어 주며, Stage 6: Maintain에서 설명하는 대로 SDLC를 자율적으로 돌리고 loop를 닫는 데 근본이 된다.

legacy system과 source of truth

기존 SDLC process는 이미 artifact를 추적하고 있을 텐데, 다만 Markdown 파일로는 아니다. 작업 항목은 Jira에, 요구사항은 규제 traceability가 내장된 도구에, 설계는 Figma에, 변경 승인은 change board에 있을 수 있다. 감사인과 규제 기관이 그 시스템들을 이미 인정하고 다른 팀들도 그것에 의존하기 때문에 밀어내기가 어렵고, 따라서 AI-native SDLC는 이미 있는 것에 맞춰 들어가야 한다. process가 만드는 artifact마다 한 시스템을 source of truth로 지정하고 나머지는 사본이나 링크를 갖게 해야 한다.

아래 구성들은 artifact마다 선택을 달리하면서 하나의 source of truth를 두도록 설정할 수 있다:

- source of truth로서의 repo. Markdown artifact가 authoritative record이고, legacy system은 commit 안의 파일을 참조한다. 모든 기록이 하나의 타임스탬프 권위를 가진 한 도구 안에 살기 때문에, 엔지니어링이 주도하는 조직에서는 이것이 가장 깔끔한 구성 중 하나일 수 있다.

- legacy system이 source of truth이다. Jira, ServiceNow, 또는 요구사항 도구가 authoritative record를 갖고, Markdown artifact는 working copy이다. Claude는 session을 시작할 때 그 기록을 읽고, 스펙이나 계획을 만든 바로 그 session에서 Model Context Protocol(MCP) connector를 통해 결과를 다시 기록한다.

- 최소 기준으로서의 연계. 모든 artifact가 기록 ID를 적고, 모든 레거시 기록이 Markdown 파일의 commit SHA를 담는다. source of truth가 둘이므로, 연계 방식은 AI-native SDLC로 전환할 때 시작점으로 좋다.

둘 사이에 링크가 있거나 하나가 source of truth로 선언되어 있는 한, legacy system과 AI-native Markdown 우선 시스템은 공존할 수 있다.

06 / 14

institutional knowledge로서의 skill

원문 보기

skill은 조직이 자신의 institutional knowledge를 실제로 작동하게 만드는 방법이다. 그 지시는 명시적이고, version 관리되고, 폭넓게 적용되며, 정책이 바뀌면 중앙에서 갱신된다. 경험칙은 이렇다: 일관되게 적용되어야 하는 institutional knowledge는 skill로 쓰고, CLAUDE.md나 prompt에 속하는 구성 요소는 skill로 쓰지 마라.

시작하기

- 전제 조건: 필수 조건은 없다. CLAUDE.md가 있으면 agent의 작업 지식을 repo 안에 두게 되므로 도움이 되지만, skill이 그것에 의존하지는 않는다.

- 인프라: 지정된 오너와 문서화된 source of truth가 있는 정책 하나.

실행 방법

- 오늘 일관되지 않게 강제되고 있는 지식 하나를 고르라. 보안 표준, API 설계 convention, 브랜드 규칙 같은 것일 수 있다.

- 그것을 skill로 쓰라 — skill은 SKILL.md 하나를 담은 폴더이고, 그 frontmatter가 언제 trigger되는지를 말하고 본문이 무엇을 할지를 말한다. 엔지니어가 policy owner의 source of truth를 바탕으로, Claude의 도움을 받아 그것을 쓴다.

- skill을 repo의 .claude/skills/<name>/에 두어 코드와 함께 배포되게 하거나, plugin을 통해 조직 전체에 배포하라.

- skill이 trigger되는지 test하라. 관련 작업을 여러 방식으로 Claude에게 요청해 매번 skill이 로드되는지 확인하라.

- 정책이 바뀌면 skill을 바꾸고, 그 변경을 policy owner가 승인하게 하라.

- 엔지니어는 다음 session에서 새 버전을 자동으로 받는다.

실제 모습

.claude/skills/secure-api-review/SKILL.md:

---
name: secure-api-review
description: Apply the API security standard. Use whenever creating or
  modifying an external-facing endpoint, reviewing API code, or
  generating an OpenAPI spec.
---
# Secure API review
When you create or change an API endpoint:
1. Authentication: every endpoint requires the gateway JWT;
   no anonymous routes outside /health.
2. Input validation: validate request bodies against the OpenAPI
   schema and reject unknown fields.
3. Audit: every state-changing endpoint emits an audit event with
   actor, action, entity and timestamp.
4. Data classification: fields tagged pii in the schema must never
   appear in logs or error messages.
Run scripts/check-endpoints.sh and include its output in your summary.

governance 고려사항

skill은 통제 수단이지만, 권고적인 통제 수단이다. skill은 코드를 쓰는 동안 Claude가 정책을 적용할 가능성을 높이지만, session이 그것을 따르도록 강제하는 것은 없다. 언제나 성립해야 하는 정책에는 동작을 막는 hook이나 PR에서 정책을 다시 확인하는 review pass처럼, skill 뒤를 받치는 deterministic한 무언가가 필요하다. skill은 위반을 드물게 만들고, hook은 위반을 거의 불가능하게 만든다. skill 호출은 session traces에 기록되고, policy owner는 skill 변경을 코드처럼 review한다.

측정 방법

- leading indicator: policy owner가 정책 변경을 승인한 시점부터 갱신된 skill이 merge되기까지의 시간 — skill 폴더의 PR에서 취한다.

- lagging indicator: 그 정책을 인용하는 PR review 발견 건수인데, 코드를 쓰는 동안 skill이 정책을 적용하게 되면 0을 향해 떨어져야 한다. 발견 건수가 0을 향해 떨어지지 않는다면, skill이 trigger되지 않고 있거나 그 문면이 공식 정책에서 벗어난 것이다.

build 시점 guardrail로서의 hook

skill은 권고적인 통제 수단이고, hook은 그 뒤를 받치는 deterministic한 층이다. Claude의 동작 대부분은 구현 중의 파일 편집과 셸 명령이므로, hook이 가장 자주 발화하게 되는 곳은 build 단계다.

build 단계 hook은 다음을 할 수 있다:

- 생성된 클래스나 동결된 패키지 같은 protected path의 편집을 막는다

- 파일 편집 뒤에 포매터와 린터를 돌려 drift가 쌓이지 않게 한다

- credentials이 diff에 들어가지 않게 한다

- 정책이 예외 없이 성립해야 하는 skill을 뒤에서 받친다

hook은 자신과 맞는 동작마다 돌기 때문에, build 단계 hook은 빠르고 변경된 파일로 범위가 좁혀져 있어야 한다. 전체 test suite 같은 더 무거운 검사는 commit이나 PR에 속한다.

build 중의 승인 prompt는 병렬로 도는 모든 session의 critical path에 사람을 다시 세우므로, 사람에게 승인을 묻는 hook은 Stage 5: Deploy의 gate에 속한다.

07 / 14

병렬 session과 subagent

원문 보기

엔지니어 한 명이 여러 갈래의 작업을 동시에 몰고 갈 수 있다.

parallel session은 또 하나의 완전한 Claude Code instance로, 자기 Git worktree 안에서 별도의 작업을 수행한다. 독립된 session들은 서로를 전혀 모르며, 이들이 공유하는 것은 이들을 조종하는 엔지니어뿐이다.

subagent는 자체 context window와 도구 제한을 가진 범위 한정 조력자로서 단일 session 안에서 돌고, 앱이 기대대로 도는지 검증하는 일처럼 여러 작업에서 반복되는 일에 어울린다.

parallel session은 엔지니어가 동시에 진행할 수 있는 작업 수를 늘리고, subagent는 각 session이 자기 작업에 집중하도록 붙잡는다. 엔지니어의 일은 그 전부를 조종하고 review하는 것이다.

무엇이 달라지는가

Traditional

엔지니어 한 명이 한 번에 한 작업을 하고, 하루·한 주의 상당 부분을 build와 test와 review에 쓴다. 기다리는 동안 작업 사이를 오갈 수는 있지만, context 전환이 충분히 피곤해서 그 길을 택하는 사람은 드물다.

AI-native

엔지니어 한 명이 여러 Claude session을 동시에 돌리고, 각 session은 자기 worktree에서 자기 작업을 맡는다. 반복되는 일은 자체 context와 도구 제한을 가진 subagent가 된다. 엔지니어의 일은 orchestration으로, 나아가 loop를 만들고 감시하는 일로 옮겨간다.

시작하기

- 전제 조건: CLAUDE.md — 모든 session이 이 파일을 읽기 때문이다. feedback loop(Stage 4: Test)도 여기서 도움이 되는데, session이 자기 작업을 검증할 수 있으면 엔지니어의 감독이 덜 필요하기 때문이다.

- 인프라: 격리가 worktree에서 나오므로 Git repository, 그리고 조직이 안전하다고 보는 명령을 두고 session이 승인 prompt를 기다리는 일이 없도록 조정한 권한 설정.

실행 방법

- 엔지니어는 plan mode play(Stage 3: Build)에서 나온 계획으로 작업이 어디서 독립적인지 확인해, 서로 다른 파일을 건드리는 작업들로 일을 쪼갠다. 파일을 공유하는 작업은 한 session에서 차례로 돌린다.

- 병렬 작업은 각각 자기 worktree를 갖는다 — 예를 들어 한 터미널에서는 claude --worktree feature-auth, 다른 터미널에서는 claude --worktree fix-rate-limit이다. worktree는 자기 branch 위의 별도 checkout이고, session들이 파일에서 충돌하는 것을 막는다.

- session 두세 개가 합리적인 출발점이다. 실질적인 상한은 한 사람이 제대로 review할 수 있는 갈래의 수이므로, review가 따라오는 동안에만 session을 늘린다.

- 반복되는 일은 .claude/agents/의 Markdown 파일에 정의하는 subagent로 만들되, 각각 이름과 언제 쓰는지를 적은 설명과 건드려도 되는 도구를 갖게 한다. 예로는 메인 agent가 끝난 뒤 불필요한 복잡도를 걷어내는 code simplifier, 앱을 띄워 동작을 확인하는 verifier, 메인 context를 채우지 않으면서 코드베이스를 탐색해 보고하는 researcher가 있다. 팀 전체가 공유하도록 그 정의를 Git에 commit해 둔다.

실제 모습

.claude/agents/verifier.md:

---

name: verifier
description: Runs the app and checks the change works before the session reports done
tools: Bash, Read

---
Start the app with make run. Exercise the changed behavior and the two
nearest neighboring flows. Report what you ran, what you saw, and any
behavior that does not match plan.md. Do not fix anything; report only.

governance 고려사항

session이 늘면 artifact도 늘어나므로, 통제는 repo 안의 설정에서 나와야 한다. 거기 있는 hook과 권한 설정은 모든 session에 적용되고, session이 하는 일은 기록되어 그것을 돌린 엔지니어에게 귀속된다.

측정 방법

- leading indicator: OpenTelemetry 익스포트에서 세는, review 품질이 유지되는 동안의 엔지니어당 동시 session 수, 그리고 기다리기보다 조종에 쓴 하루의 비중.

- lagging indicator: PR 이력으로 판정한 rework rate와 나란히 읽는, 엔지니어당 주간 merge된 변경 수.

08 / 14

Claude에게 feedback loop 주기

원문 보기

test든 build든 스크린샷 diff든, Claude에게 자기 작업을 검증할 수단을 언제나 준다. session은 엔지니어가 보기 전에 자기 작업을 확인하고 자기 실수를 고친다.

feedback loop를 verifier subagent(Stage 3: Build)와 혼동하면 안 된다. feedback loop는 작업이 요구하는 횟수만큼 작업 전체를 관통하며 돈다. 반면 verifier subagent는 session이 작업을 끝냈다고 판단한 시점에 새 context window를 띄워 최종 확인을 묶어 내는 한 가지 방법이다. 이렇게 하면 코드를 만들어 낸 가정이 판정을 물들이지 않는다.

무엇이 달라지는가

Traditional

코드가 동작한다는 신호가 늦게 온다. CI는 몇 분 뒤, 테스터는 며칠 뒤, 프로덕션은 몇 주 뒤다. agent가 코드를 만들어 내는 상황에서 신호가 늦다는 것은 사람이 그 artifact 전부를 확인해야 한다는 뜻이고, 그 사람이 bottleneck이 된다.

AI-native

session은 사람이 보기 전에 자기 작업을 확인할 수단을 받는다. test를 돌리고, build를 돌리고, 스크린샷을 찍는다. Claude는 그 확인이 통과할 때까지 반복하므로, 엔지니어에게 닿는 것은 이미 통과한 것이다. loop를 세우는 일은 session을 돌리는 엔지니어의 몫이고, 아래 단계는 그 사람을 위해 쓰였다.

시작하기

- 전제 조건: 없음.

- 인프라: 각각 명령 하나로 로컬에서 도는 test suite와 build. UI 작업에서는 Claude가 결과를 볼 수단이 결정적인데, 브라우저 도구이거나 MCP로 연결한 스크린샷 유틸리티다.

실행 방법

- 지금 작업을 확인하는 데 명령을 여러 개 이어 붙여야 하고 환경 지식도 필요하다면, 실패 시 0이 아닌 종료 코드로 끝나는 make test나 npm test 같은 단일 타깃으로 감싼다.

- CLAUDE.md의 명령어 절에 각 명령을 정상 출력 예시와 함께 나열한다.

- Claude가 되묻지 않고 작업을 확인할 수 있도록 목표를 진술하고 정량화한다 — 예를 들어 「test_status.py의 모든 test가 통과한다」, 「스크린샷이 첨부된 mock과 일치한다」, 「엔드포인트가 새 필드와 함께 200을 반환한다」이다.

- 버그 수정에서는 실패하는 test를 먼저 쓴다. Claude에게 버그를 test로 재현하고, 돌리고, 예상한 이유로 실패하는지 확인하게 한다. 그 test를 commit한다. 그러고 나서야 test를 고치지 않고 통과시키라고 Claude에게 요청하며, 마지막 단계의 test 파일 hook이 그 제한을 강제한다. 수정 전부터 있었고 agent가 다시 쓸 수 없었던 test는 버그가 사라졌다는 증명이다.

- UI 작업에서는 시각 확인으로 loop를 닫는다. Claude에게 브라우저나 스크린샷 도구를 주고, mock을 주고, 반복하게 한다. 구현하고, 스크린샷을 찍고, 비교하고, 조정한다. 두세 라운드가 정상이고, 결과는 라운드마다 나아져야 한다.

- 검증을 「완료」의 일부로 만든다. 그 지시는 CLAUDE.md에 있다: 「작업 완료를 보고하기 전에 test를 돌리고, 그 출력을 보여라.」

- 마지막으로 loop 자체를 보호해야 하는데, 코드를 고치는 agent가 그 코드를 보는 검사를 약화시킬 수 있어서는 안 되기 때문이다. 수정 작업 중 test 파일 편집을 막는 hook이 그 일을 한다. 대안은 review에서 diff를 확인하고 test를 건드리는 변경을 전부 반려하는 것이다.

실제 모습

CLAUDE.md 검증 블록:

## Verifying your work

- Build: make build (must finish with "Build succeeded")
- Test: make test (all green; never skip or delete a failing test)
- Lint: make lint (zero warnings)

Run all three before reporting any task complete, and paste the output.
If a test fails, fix the code, not the test.

governance 고려사항

- 강제되는 것: 작업 완료를 보고하기 전의 검증, 그리고 수정 중 agent의 test 파일 편집 차단이며, 조직이 이를 보장받고자 하는 곳에서는 둘 다 hook으로 구현한다.

- 증거: Claude가 돌려서 붙여 넣은 make test의 원문 출력, build 로그, 또는 스크린샷 diff이며, 따라서 증거는 toolchain에서 나온다.

- 기록 위치: OpenTelemetry 익스포트가 조직의 observability stack으로 전달하는 session transcript, 그리고 reviewer와 나중의 감사자가 둘 다 볼 수 있는 PR의 check run.

- 승인자: PR을 review하는 code owner이며, 기계적 증거가 이미 붙어 있으므로 의도와 위험에 집중할 수 있다.

측정 방법

- leading indicator: agent가 쓴 변경의 CI 첫 시도 성공률이며, CI 시스템이 이미 지원한다.

- lagging indicator: test가 reviewer들이 잡던 것을 잡기 시작하면 줄어야 할 PR당 review 시간(PR 메타데이터에서), 그리고 incident tracker에서 얻는 change failure rate.
