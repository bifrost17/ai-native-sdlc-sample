# 검증 항목 색인

ID = `V<챕터>-<문서 순서>`. 판정: 충실 · 부분 · 팀 몫(미검증) · 보완 필요. 각 ID 는 주석판의 `#ID` 앵커다.

검증 기준 핀 — v2 `main@0daf655` · v3(진행 중) `main@5599dcf` · 실험 `experiment/2026-09-09-claims-status@cebc0e5`.
인용은 `경로 + 축자 인용문`이고 줄 번호는 쓰지 않는다 — 핀은 그 문면을 읽은 시점을 말한다
(`CHAPTERS.md` 가 챕터별 라운드의 정본). 라운드 사이 대조는 `git diff --name-only <이전 핀>..<새 핀>`
— 그 목록에 없는 파일로 간 인용은 손대지 않는다.

## 2 · intent.md로 포착하기 (V2-01 ~ V2-16)

| ID | 판정 | 문단 |
|---|---|---|
| V2-01 | 충실 | 도입 — intent.md 가 들어오는 세 경로 |
| V2-02 | 충실 | 도입 — PO 가 commit 전에 review 하고 고친다 |
| V2-03 | 충실 | 표 — originator 자신의 언어로 쓴 proto-spec |
| V2-04 | 충실 | 시작하기 — 전제 조건 없음 |
| V2-05 | 충실 | 시작하기 — 인프라(접근 수단 · template · intent home · PO) |
| V2-06 | 부분 | intent home 세우기 · 쓰기 권한 정하기 |
| V2-07 | 팀 몫(미검증) | Git 경험 없는 기여자 — connector 로 commit |
| V2-08 | 충실 | 실행 1 — originator 가 자기 말로 문제를 설명 |
| V2-09 | 충실 | 실행 2 — Claude 가 분석가처럼 묻는다 |
| V2-10 | 부분 | 실행 3 — 조직 template 을 skill 로 · 리드가 승인 |
| V2-11 | 충실 | 실행 4 — originator 가 오해를 고친다 |
| V2-12 | 충실 | 실행 5 — 공유 home 에 commit · 작성자·타임스탬프 · PO 가 이어받음 |
| V2-13 | 충실 | 실제 모습 — 예시 intent.md 와 템플릿·실사슬 대조 |
| V2-14 | 충실 | governance — 증거는 commit 된 intent.md · 수용/기각은 merge/종료 review |
| V2-15 | 충실 | 측정 — leading: 첫 대화 → commit 된 intent.md |
| V2-16 | 충실 | 측정 — lagging: survival rate · spec 이후 intent.md 변경 |

## 3 · 요구사항과 design (V3-01 ~ V3-16)

| ID | 판정 | 문단 |
|---|---|---|
| V3-01 | 부분 | 도입 — 조직의 skill(브랜드·보안·compliance·UX)이 spec 을 이끈다 |
| V3-02 | 충실 | 도입 — PO 는 review 만, 목표는 우려 지점이 표시된 spec |
| V3-03 | 팀 몫(미검증) | 도입 — Claude Design 으로 mock → Claude Code |
| V3-04 | 충실 | 표 우측 — 요구+설계가 한 session 에서 |
| V3-05 | 부분 | 시작하기 — 전제(intent.md + 정책 skill 넷) |
| V3-06 | 충실 | 시작하기 — 인프라(PO + Claude · 엔지니어링 역량 불요) |
| V3-07 | 충실 | 실행 1 — skill 을 갖춘 session 에 intent 첨부 |
| V3-08 | 부분 | 실행 2 — prompt(가리킴·제약·우려 요구) → 슬래시 명령 → merge 트리거 job |
| V3-09 | 충실 | 실행 3 — PO 리뷰의 두 물음 |
| V3-10 | 충실 | 실행 4 — flagged concern 을 policy owner 와 먼저 해소 |
| V3-11 | 충실 | 실행 5 — intent.md 옆에 spec.md |
| V3-12 | 충실 | 실행 6 — PO 가 build 진행 결정 · 고위험은 tech lead · 사람이 항상 |
| V3-13 | 충실 | 실제 모습 — PO 의 prompt |
| V3-14 | 부분 | governance — 정책을 쓰는 동안 적용 · spec/prompt/skill 버전 기록 · PO 서명 · 라우팅 |
| V3-15 | 충실 | 측정 — leading: intent 커밋 → spec 커밋 |
| V3-16 | 충실 | 측정 — lagging: 첫 plan 커밋 이후 spec 커밋 수 |

## 4 · 기본 출발점으로서의 Claude Code plan mode (V4-01 ~ V4-18)

| ID | 판정 | 문단 |
|---|---|---|
| V4-01 | 충실 | 도입 — plan mode 시작 · 승인된 spec 을 주고 · Claude 가 자신을 인터뷰 |
| V4-02 | 충실 | AI-native — 아무것도 바꾸지 않고 읽는다 · 엔지니어가 고친다 · 승인판을 plan.md 로 commit |
| V4-03 | 충실 | 전제 — intent.md/spec.md 와 CLAUDE.md |
| V4-04 | 충실 | 인프라 — 레포에 접근하는 Claude Code |
| V4-05 | 충실 | 1 — plan mode 로 시작 |
| V4-06 | 충실 | 2 — 변경 파일 · 작업 순서 · 증명 test 를 명시한 계획 |
| V4-07 | 충실 | 3 — 계획을 따져라(깨뜨릴 것 · 가장 위험한 단계 · 버린 선택지) |
| V4-08 | 부분 | 4 — 대화를 못 본 엔지니어가 계획만으로 구현할 수 있을 때까지 |
| V4-09 | 충실 | 5 — 승인된 계획을 plan.md 로 commit · PR review 가 diff 를 대조 |
| V4-10 | 충실 | 6 — 수락 뒤 구현 · 탄탄하면 한 번의 패스 |
| V4-11 | 부분 | 7 — 벗어나면 같은 commit 에서 plan.md 갱신 · 동기화 hook 은 「고려」 |
| V4-12 | 충실 | 실제 모습 — plan.md 예시 |
| V4-13 | 충실 | governance — 코드 전 설계 review · plan mode 가 스스로 강제 · 수락자 기록 · 고위험은 tech lead |
| V4-14 | 충실 | 측정 leading — 첫 패스 머지 비율 · 계획 승인→머지 시간 |
| V4-15 | 충실 | 측정 lagging — 재작업 사이클 · merged diff 와 plan.md 일치 빈도 |
| V4-16 | 충실 | auto mode — guardrail(CLAUDE.md · 정책 skill · hook · test suite)이 익으면 일상 작업의 기본 |
| V4-17 | 충실 | legacy — artifact 마다 source of truth 하나를 지정 |
| V4-18 | 충실 | 구성 1 — repo 가 source of truth |

## 5 · CLAUDE.md (V5-01 ~ V5-11)

| ID | 판정 | 문단 |
|---|---|---|
| V5-01 | 충실 | 도입 — new joiner 의 context · 매 session 읽는 파일 · 팀이 유지하고 실수마다 다듬는다 |
| V5-02 | 충실 | 인프라 — repo · Claude Code · 코드베이스를 아는 엔지니어 한 명 |
| V5-03 | 팀 몫(미검증) | 1 — /init 으로 출발점 생성 |
| V5-04 | 충실 | 2 — 첫날치로 줄여라: build·test·lint 명령 · convention · 계속 틀리는 것 |
| V5-05 | 충실 | 3 — repo 루트에 체크인 · 변경은 코드처럼 review |
| V5-06 | 충실 | 4 — 실수를 두 번 하면 정정을 CLAUDE.md 에 |
| V5-07 | 충실 | 5 — 한 페이지 안으로 |
| V5-08 | 충실 | 실제 모습 — CLAUDE.md 예시 |
| V5-09 | 부분 | governance — version 관리 · review·감사 · code owner 가 PR 에서 승인 |
| V5-10 | 충실 | 측정 leading — 잡았어야 할 실수의 반복 빈도 · 정정은 Git 이력에 |
| V5-11 | 충실 | 측정 lagging — 신규 구성원의 첫 merged PR 까지 시간 |

## 6 · institutional knowledge로서의 skill (V6-01 ~ V6-16)

| ID | 판정 | 문단 |
|---|---|---|
| V6-01 | 충실 | 도입 — 명시적 · version 관리 · 중앙 갱신 · 경험칙(일관 적용 지식은 skill, CLAUDE.md/prompt 것은 아님) |
| V6-02 | 충실 | 인프라 — 오너와 source of truth 가 있는 정책 하나 |
| V6-03 | 충실 | 1 — 오늘 일관되지 않게 강제되는 지식 하나 |
| V6-04 | 충실 | 2 — SKILL.md 하나를 담은 폴더 · frontmatter = 언제 · 본문 = 무엇을 |
| V6-05 | 충실 | 3 — .claude/skills// 에 두어 코드와 함께 배포 |
| V6-06 | 충실 | 4 — 여러 방식으로 요청해 매번 로드되는지 확인 |
| V6-07 | 충실 | 5 — 정책이 바뀌면 skill 을 바꾸고 policy owner 가 승인 |
| V6-08 | 충실 | 6 — 다음 session 이 새 버전을 자동으로 받는다 |
| V6-09 | 충실 | 실제 모습 — secure-api-review SKILL.md |
| V6-10 | 충실 | governance — 권고적 · 항상 성립할 정책은 deterministic 뒷받침 · 호출은 트레이스에 · 오너가 코드처럼 review |
| V6-11 | 충실 | 측정 leading — 오너 승인 → skill merge 시간 |
| V6-12 | 충실 | 측정 lagging — 정책 인용 발견이 0 을 향해 |
| V6-13 | 충실 | hook — deterministic 층 · build 단계에서 가장 자주 발화 |
| V6-14 | 충실 | build 단계 hook 넷 — protected path · 포매터/린터 · credentials · 예외 없는 정책의 뒷받침 |
| V6-15 | 충실 | hook 은 빠르고 변경 파일로 범위 한정 · 무거운 검사는 commit/PR |
| V6-16 | 충실 | 사람에게 승인을 묻는 hook 은 Stage 5 gate 에 |

## 7 · 병렬 session과 subagent (V7-01 ~ V7-12)

| ID | 판정 | 문단 |
|---|---|---|
| V7-01 | 충실 | 도입 — parallel session = 자기 worktree 의 완전한 instance · 서로를 모른다 |
| V7-02 | 부분 | 도입 — subagent = 자체 context · 도구 제한 · 반복되는 검증 일 |
| V7-03 | 충실 | 전제 — CLAUDE.md · session 이 자기 작업을 검증할 수 있는 feedback loop |
| V7-04 | 충실 | 인프라 — Git repository · 안전한 명령에 승인 prompt 가 없도록 조정한 권한 설정 |
| V7-05 | 충실 | 1 — 계획으로 독립성을 보고 파일이 다른 작업으로 쪼갠다 · 공유하면 한 session 에서 차례로 |
| V7-06 | 충실 | 2 — 작업마다 자기 worktree(자기 branch 위의 별도 checkout) |
| V7-07 | 충실 | 3 — 두세 개로 시작 · review 가 따라오는 동안만 늘린다 |
| V7-08 | 충실 | 4 — .claude/agents/ 의 Markdown 으로 subagent · 이름·설명·도구 · Git 에 commit |
| V7-09 | 충실 | 실제 모습 — verifier.md |
| V7-10 | 충실 | governance — 통제는 repo 안 설정에서 · hook·권한이 모든 session 에 · 기록은 엔지니어에게 귀속 |
| V7-11 | 충실 | 측정 leading — 엔지니어당 동시 session 수 · 조종에 쓴 비중 |
| V7-12 | 충실 | 측정 lagging — 엔지니어당 주간 merge 수 · rework rate 와 나란히 |

## 8 · Claude에게 feedback loop 주기 (V8-01 ~ V8-17)

| ID | 판정 | 문단 |
|---|---|---|
| V8-01 | 충실 | 도입 — 자기 작업을 검증할 수단을 언제나 · 엔지니어가 보기 전에 스스로 고친다 |
| V8-02 | 충실 | 도입 — loop 는 작업 내내, verifier 는 끝에 새 context 로 최종 확인 |
| V8-03 | 충실 | 인프라 — 명령 하나의 test suite 와 build · UI 면 스크린샷 수단 |
| V8-04 | 충실 | 1 — 단일 타깃, 실패 시 0 아닌 종료 코드 |
| V8-05 | 충실 | 2 — Commands 절에 정상 출력 예시 |
| V8-06 | 충실 | 3 — 목표를 진술하고 정량화 |
| V8-07 | 충실 | 4 — 실패 test 먼저 · commit · test 안 고치고 통과 · hook 이 강제 |
| V8-08 | 팀 몫(미검증) | 5 — UI 는 스크린샷으로 loop |
| V8-09 | 충실 | 6 — 「완료 보고 전에 test 를 돌리고 출력을 보여라」가 CLAUDE.md 에 |
| V8-10 | 충실 | 7 — 수정 중 test 파일 편집을 막는 hook · 대안은 review 반려 |
| V8-11 | 충실 | 실제 모습 — CLAUDE.md 검증 블록 |
| V8-12 | 충실 | governance — 강제되는 것: 완료 전 검증 · 수정 중 test 편집 차단(둘 다 hook 으로, 보장하려는 곳에서) |
| V8-13 | 충실 | governance — 증거는 toolchain 의 원문 출력 |
| V8-14 | 충실 | governance — session transcript(OTel) · PR 의 check run |
| V8-15 | 충실 | governance — 승인자는 code owner |
| V8-16 | 충실 | 측정 leading — CI 첫 시도 성공률 |
| V8-17 | 충실 | 측정 lagging — PR 당 review 시간 · change failure rate |

## 9 · CI에서의 지속적 eval (V9-01 ~ V9-13)

| ID | 판정 | 문단 |
|---|---|---|
| V9-01 | 충실 | 도입 — agent 설정이 바뀔 때마다 도는 suite |
| V9-02 | 충실 | 도입 — 모니터링에서 나온 새 사례를 넣는다 |
| V9-03 | 충실 | 전제 — CLAUDE.md · feedback loop |
| V9-04 | 팀 몫(미검증) | 인프라 — non-interactive CI · 예산 있는 API 키 |
| V9-05 | 팀 몫(미검증) | 1 — 실제 작업 20~50건 + 기대 결과 |
| V9-06 | 충실 | 2 — prompt + 수용 기준 검사 |
| V9-07 | 충실 | 3 — non-interactive · 예약 일정 · CLAUDE.md/skill/hook 변경마다 |
| V9-08 | 부분 | 4 — 결과가 설정 변경의 gate · pass rate 떨어뜨리는 skill 변경은 merge 전 review |
| V9-09 | 충실 | 5 — incident 마다 eval, incident 소유 팀이 쓰고 regression 으로 남는다 |
| V9-10 | 충실 | 실제 모습 — agent-evals.yml |
| V9-11 | 충실 | governance — pass rate 문턱 = merge 체크 · 실행 기록 · 설정 소유 팀 승인 |
| V9-12 | 충실 | 측정 leading — pass rate 추이 · incident → 영구 eval 시간 |
| V9-13 | 충실 | 측정 lagging — CI 가 잡은 regression vs 프로덕션 발견 |

## 10 · PR review loop 속의 AI (V10-01 ~ V10-13)

| ID | 판정 | 문단 |
|---|---|---|
| V10-01 | 충실 | 도입 — Claude 가 review 를 하고(정책 대조) 받는다(코멘트 처리) |
| V10-02 | 충실 | 전제 — 갱신된 CLAUDE.md · 정책 skill · 정의된 subagent |
| V10-03 | 팀 몫(미검증) | 인프라 — Claude 통합(관리형 Code Review / claude-code-action) · code owner 승인 branch protection |
| V10-04 | 팀 몫(미검증) | 1 — 관리형 서비스 또는 자체 CI 의 claude-code-action |
| V10-05 | 충실 | 2 — REVIEW.md: 패스(버그 · 보안 · spec/plan/설계 원칙 준수) · 「중요」의 정의 · 건너뛸 것 |
| V10-06 | 부분 | 3 — finding 만으로 승인/차단 없음 · branch protection 은 code owner 승인 · severity tally 는 check run 에 |
| V10-07 | 부분 | 4 — @claude 로 코멘트 처리·수정 push · PR 스레드에 요청과 변경 기록 · slash command 로 감싼 loop |
| V10-08 | 충실 | 5 — 두 번째 지적은 그 review 의 일부로 CLAUDE.md 에 · review 가 CLAUDE.md 를 읽는다 |
| V10-09 | 충실 | 6 — 월 1회 finding 등급 매기기 · nit 상한 · 생성 경로·CI 가 강제하는 것 제외 |
| V10-10 | 충실 | 실제 모습 — REVIEW.md |
| V10-11 | 부분 | governance — separation of duties · REVIEW.md 가 모든 PR 에 · PR 이 audit record · 승인은 사람이 branch protection 을 거쳐 |
| V10-12 | 충실 | 측정 leading — 첫 review 까지 시간 · 사람 손 없이 해소된 코멘트 비중 |
| V10-13 | 충실 | 측정 lagging — merge 전에 잡힌 결함 vs 프로덕션으로 샌 결함 |

## 11 · approval gate로서의 hook (V11-01 ~ V11-15)

| ID | 판정 | 문단 |
|---|---|---|
| V11-01 | 충실 | 도입 — hook 은 허용/차단뿐 아니라 지정된 사람이 승인할 때까지 멈출 수 있다(release gating) |
| V11-02 | 충실 | 도입 — hook 은 배포 전용이 아니다: protected path · 수정 중 test 파일 |
| V11-03 | 팀 몫(미검증) | 인프라 — 변경 process 가 요구하는 승인 목록 |
| V11-04 | 팀 몫(미검증) | 1 — 살아남아야 할 사람 approval gate 를 나열 |
| V11-05 | 충실 | 2 — 각 gate 를 hook 으로(허용 · 질의 · 차단) |
| V11-06 | 충실 | 3 — 팀 hook 은 .claude/settings.json 에 · 협상 불가 hook 은 managed settings 에 |
| V11-07 | 충실 | 4 — 차단은 이유와 승인 경로를 Claude 출력에 |
| V11-08 | 충실 | 실제 모습 — settings.json 의 PreToolUse(Bash) → production-gate.sh |
| V11-09 | 충실 | 실제 모습 — production-gate.sh |
| V11-10 | 충실 | governance — 매번 모두에게 강제 · 허용/차단이 타임스탬프와 기록 · gate 가 승인의 정의를 정한다 |
| V11-11 | 충실 | managed settings — MDM/admin console 배포 · 엔지니어는 덮어쓸 수 없다 |
| V11-12 | 충실 | managed settings — 여덟 키가 예시 파일에 있는가 |
| V11-13 | 팀 몫(미검증) | managed settings — 출발점, 균형은 repo 의 data classification 에 |
| V11-14 | 충실 | 측정 leading — gate 별 대기 시간 · 결정마다 타임스탬프 + 판정 |
| V11-15 | 충실 | 측정 lagging — 프로덕션에 도달한 gate 위반(전후) |

## 12 · CI/CD 통합과 deployment (V12-01 ~ V12-16)

| ID | 판정 | 문단 |
|---|---|---|
| V12-01 | 부분 | 도입 — non-interactive 실행 · sandbox · MCP 배포 · 롤백 리허설 |
| V12-02 | 부분 | 전제 — AI review loop · approval gate hook |
| V12-03 | 팀 몫(미검증) | 인프라 — claude -p 를 부를 runner · 모델 접근 · MCP 서버 · sandbox 프로파일 |
| V12-04 | 충실 | 1 — 읽기 전용 판단 단계: 실패한 build 분류 · flaky 요약 · changelog 초안 |
| V12-05 | 부분 | 2 — 기존 gate 뒤의 쓰기 단계 · agent 가 쓴 것은 PR 로 · main 직행 경로 없음 |
| V12-06 | 팀 몫(미검증) | 3 — sandbox: 컨테이너 · 네트워크 정책 · 수명 짧은 토큰 · 프로덕션 credentials 없음 |
| V12-07 | 팀 몫(미검증) | 4 — 배포·상태·롤백을 환경별 MCP 도구로 |
| V12-08 | 부분 | 5 — 환경별 자율성: dev 자유 · prod 는 release manager 승인 + hook |
| V12-09 | 팀 몫(미검증) | 6 — 롤백은 명령 하나, 스테이징에서 정기 리허설 |
| V12-10 | 충실 | 실제 모습 — 실패한 build 분류 단계 |
| V12-11 | 충실 | governance — agent 는 gate 까지, 넘지는 못한다 |
| V12-12 | 부분 | governance — branch protection 이 agent 산출을 PR 로 |
| V12-13 | 부분 | governance — 배포 hook · non-interactive 실행은 agent 자신의 신원 |
| V12-14 | 팀 몫(미검증) | governance — 환경별 권한 등급 |
| V12-15 | 충실 | 측정 leading — 사람 없이 분류된 pipeline 실패 비율 |
| V12-16 | 충실 | 측정 lagging — DORA |

## 13 · metrics로 loop 닫기 (V13-01 ~ V13-16)

| ID | 판정 | 문단 |
|---|---|---|
| V13-01 | 부분 | 도입 — 사람 없이 시작하는 loop · headless · 단계 사이 confidence gate |
| V13-02 | 충실 | 패턴 — deterministic 감시가 이탈 때 Claude 를 호출 |
| V13-03 | 부분 | 전제 — intent.md · AI review · hook 경계 · 롤백 경로 |
| V13-04 | 팀 몫(미검증) | 인프라 — metrics store · repo 읽기 · non-interactive CI 또는 Agent SDK |
| V13-05 | 충실 | 1 — 안정적인 rolling baseline 을 가진 metric 하나 |
| V13-06 | 충실 | 2 — rolling mean/σ + Western Electric 규칙 · version 관리 · 단위 test · 모델 없음 |
| V13-07 | 충실 | 3 — tier 를 설정에: 1σ 기록 · 2σ 읽기 전용 진단 · 3σ PR 또는 사전 승인 runbook 으로만 |
| V13-08 | 충실 | 4 — trigger: 예약 workflow/webhook/cron · stateless non-interactive · 아무도 시작하지 않아도 끝난다 |
| V13-09 | 충실 | 5 — 진단을 intent.md(anomaly·증거·제안 결과·영향 시스템·미결 질문)로 |
| V13-10 | 충실 | 6 — 분류: 지금 고침/일정/기각 · 기각은 대역 조율 |
| V13-11 | 충실 | 7 — 수정과 함께 incident eval 추가 |
| V13-12 | 충실 | 실제 모습 — bands.yaml |
| V13-13 | 부분 | governance — 경계는 설정에서 · 권한/managed settings 가 프로덕션 접근 거부 · 호출·finding·분류 기록 · 사전 승인 runbook |
| V13-14 | 충실 | 측정 leading — 이탈 → 분류 대기열의 intent.md 시간 |
| V13-15 | 충실 | 측정 lagging — finding → merged fix 비율 · 같은 부류 반복 |
| V13-16 | 팀 몫(미검증) | Claude Tag — 채널로 들어오는 incident 의 first responder |
