# pr-loop — 요약

세션 S7 · 브랜치 `lane/S7-pr-loop` · 조사 2026-09-09 (UTC) · 정책 파일 없음

레슨 L10「AI in the PR review loop」의 이 문장을 하는 슬래시 명령을 구해 오는 과제다.

> "Teams wrap the loop in a custom slash command that sweeps the PR's unresolved review comments
> and failing checks, addresses them and pushes fixes, until the PR is green and waiting on
> code-owner approval."

## 결론 — 채택 0건, 설계 1건

**채택 집합: 없음.** 후보 35건(공식 5 · 커뮤니티 30, 표 33행)을 전부 파일로 열어 확인했고,
기각 25행 · 보류 8행(전부 라이선스 불명).
**설계분: `skills/pr-loop/`** — `/intent-sdlc-skills:pr-loop [PR]`.

기각 사유는 셋이다(자세히는 `candidates.md`):

1. **라이선스** — 가장 완성도 높은 `tinyhumansai/openhuman`의 `ship-and-babysit`(★39578)가 GPL-3.0.
   채택 기준(MIT/Apache/CC-BY) 밖이라 문구도 착상도 가져오지 않았다. 라이선스 없음·NOASSERTION 8건도 보류.
2. **범위 절반** — 리뷰 코멘트만 하거나 CI 만 한다. `facebook/relay`의 `fix-ci`(★18962)가 후자다.
   레슨 문장은 둘을 한 루프에 묶으라고 한다.
3. **이식 불가·조직 고정** — `.agents/skills/babysit-pr` 계열 3건은 동봉된 `gh_pr_watch.py` 없이
   동작하지 않고, `SIAHRA`·`metaswarm` 은 그 조직의 봇 로그인과 체크 이름이 본문에 박혀 있다.

**공식 마켓플레이스에는 이 일을 하는 명령이 없다.** 리뷰를 *만드는* 것(`pr-review-toolkit:review-pr`,
`code-review`)과 범용 반복 기구(`ralph-loop`)는 있으나, 코멘트·체크를 걷어 고치고 push 해 그린까지
가는 것은 없다. `claude-code-action`(MIT)은 레슨이 말하는 픽스 루프의 CI 쪽 절반이다 — 리뷰 코멘트에
`@claude` 를 달면 고쳐서 PR 브랜치에 push 하지만, **멘션 한 번에 한 번 반응할 뿐 스스로 반복하지
않는다**(`raw/04-claude-code-action-capabilities.txt`). 슬래시 명령의 자리를 대신하지 못한다.

설계분이 후보들에서 빌린 것은 문장 단위로 `skills/pr-loop/PROVENANCE.md` 에 적었다(MIT/Apache 5건에서 9가지).

## 실증 — 임시 레포의 진짜 PR 4건, 4/4 완주

변수 블록의 지시대로 트리거 시험 대신 실제 PR 에서 시험했다. 레포 `bifrost17/s7-pr-loop-test`,
PR 마다 **리뷰 코멘트 2건 + 실패하는 체크 1건**. 문구 셋(슬래시 · 영어 자연어 · 한국어 자연어).

| PR | 문구 | 체크 | 스레드 | push | 최종 |
|---|---|---|---|---|---|
| #1 | `/pr-loop 1` (v1) | fail→**pass** | 2/2 | 1 | 보고 직전 중첩 세션 한도로 잘림 |
| #2 | `/intent-sdlc-skills:pr-loop 2` | fail→**pass** | 2/2 | 1 | `GREEN — waiting on code-owner approval` |
| #3 | 영어 자연어 → **자동 로드** | fail→**pass** | 2/2 | 1 | 같음 |
| #4 | 한국어 자연어 → **자동 로드** | fail→**pass** | 2/2 | 1 | 같음 |

모델의 주장이 아니라 GitHub 상태로 확인했다(`raw/34-tests-after-state.txt`): 네 PR 모두
`gh pr checks` rc=0, 미해소 스레드 0, 각 스레드에 고친 커밋 sha 를 인용한 답글, **머지·승인 안 함**
(state OPEN, reviewDecision 빈 값). 자세히는 `trigger-tests.md`.

## 남는 구멍

- **한 라운드로 끝나는 시험대만 밟았다.** MAX_ROUNDS(5) 도달, 진전 없는 라운드 조기 정지,
  병합 충돌 경로, 100건 넘는 스레드의 페이지네이션, 리뷰 *body* 에만 findings 가 있는 경우는
  문서에는 있으나 **실행되지 않았다**.
- **가드레일을 일부러 깨 보지 않았다.** 시험을 지워 그린을 만들라거나 머지하라고 유도하는 시험은
  하지 않았다. 네 회 모두 자발적으로 지켰다는 것만 확인했다.
- **봇 리뷰어가 없다.** CodeRabbit·Copilot 같은 봇이 붙은 PR, 체크가 여럿인 PR 은 시험하지 않았다.
  `BOT_REVIEWERS` 설정은 미검증이다.
- **집합 충돌 시험을 하지 않았다** — 이 레인은 스킬 하나뿐이다. 전 레인을 한 플러그인에 모은 뒤
  같은 과제를 시켜 보는 것은 부모 세션의 몫이다.
- 후보 목록은 **망라적이지 않다**. GitHub code search 가 403 을 반복했고, 열지 못한 것이 있다:
  `michael-denyer/pstack-plugins`(repo 404) · claudepluginhub 페이지(403) · `solberg.is` 글의
  명령 본문(미공개) · `nakamasato` Medium(403) · `.agents/skills/babysit-pr` 계열의 upstream 원본.
- **임시 레포 `bifrost17/s7-pr-loop-test` 는 살아 있다.** 시험 원문의 링크가 가리키는 곳이라 남겼다.
  오너가 지우기로 하면 지워도 된다(질문 6).

## 정책 오너에게 묻는다

1. **이 루프에 정책 파일이 필요한가.** 지금은 `policies/*.md` 가 없어 `coverage.md` 의 행이 레슨
   문장이다. MAX_ROUNDS·resolve 주체·필수 체크 범위를 조직 정책으로 세우면 `policies/pr-review.md`
   가 생기고 스킬은 그것을 옮기게 된다. 세울 것인가, `SKILL.md` 의 「Team settings」 블록으로 둘 것인가.
2. **`RESOLVE_THREADS` 기본값.** 지금 기본은 `yes` — 고친 뒤 스킬이 스레드를 닫는다. 리뷰어가
   직접 닫아야 한다는 조직도 있다(후보 중 gabrielshanahan 은 명시적으로 금지). 어느 쪽인가.
3. **`claude-code-action` 과의 역할 분담.** 둘 다 켜면 같은 지적을 두 번 고칠 수 있다.
   리뷰어의 `@claude` 멘션은 action 에, PR 전체 훑기는 이 명령에 — 이 나눔이 맞는가.
4. **필수 체크만인가 전부인가.** `REQUIRED_ONLY` 기본은 `no`(전부 그린). advisory 봇 체크가 많은
   레포에서는 `yes`(branch protection 필수 체크만)가 맞을 수 있다.
5. **`LOCAL_CHECK` 에 무엇을 넣나.** 조직의 실제 사전 검사 명령(`make check` 등). 지금은 비어 있다.
6. **임시 레포를 남길 것인가.** `bifrost17/s7-pr-loop-test` — 시험 원문의 링크 대상.

## 파일

| 파일 | 무엇 |
|---|---|
| `candidates.md` | 후보 35건: 출처·판·라이선스·사용 신호·트리거 문장·덮는 동작·판정과 이유 |
| `coverage.md` | 레슨 네 동작 × 스킬 행렬, 겹침·모순·빈칸 |
| `trigger-tests.md` | 문구 셋의 실 PR 시험 결과 + GitHub 상태로 한 확인 |
| `raw/` | 레슨 원문 · 후보 사본(sha) · 후보 재확인 표 · 시험 스트림 원문과 전후 상태 |
| `../../decisions/S7-pr-loop.md` | 결정 1쪽 |
| `../../../skills/pr-loop/` | 설계분 `SKILL.md` + `PROVENANCE.md` |
