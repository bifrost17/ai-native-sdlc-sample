# 시험 — pr-loop

S7 변수 블록의 특별 지시대로, **트리거 시험 대신 임시 레포의 실제 PR** 에서 시험했다.
문구 셋(슬래시 · 영어 자연어 · 한국어 자연어)을 쓰되, 매 회 **리뷰 코멘트 2건 + 실패하는 체크 1건**이
달린 진짜 PR 을 상대로 완주하는지 봤다.

## 시험대

레포 `bifrost17/s7-pr-loop-test` (이 시험을 위해 만든 공개 임시 레포).
`calc.py` + `test_calc.py` + GitHub Actions `ci`(`python -m unittest -v`).
PR 마다: 새 함수 하나에 (i) 남은 `DEBUG` print, (ii) 타입 힌트·docstring 없음,
(iii) 시험을 실패시키는 진짜 버그 하나. 그 위에 인라인 리뷰 코멘트 2건.

| PR | 브랜치 | 심은 버그 | 사전 상태 원문 |
|---|---|---|---|
| #1 | `feat/percent` | `* 10` (100 이어야) | `raw/02-testbed-before.txt` |
| #2 | `feat/median` | 짝수 길이 미처리 | `raw/30-testbed2-before.txt` |
| #3 | `feat/clamp` | 상·하한 뒤바뀜 | `raw/30-testbed2-before.txt` |
| #4 | `feat/mean` | 분모 `len-1` | `raw/30-testbed2-before.txt` |

## 결과 — 4/4 완주

| # | 문구 | 설치 경로 | 판 | 로드 | 라운드 | push | 체크 | 스레드 | 최종 상태 | 원문 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `/pr-loop 1` (슬래시) | `.claude/skills/` 복사 | 초안 v1 | 로드됨 | 1 | 1 | fail→**pass** | 2/2 해소 | 보고 직전 **중첩 세션 한도**로 잘림 | `raw/10-…jsonl`, `raw/11-…txt` |
| 2 | `/intent-sdlc-skills:pr-loop 2` (슬래시) | `--plugin-dir` | **v2(채택판)** | `slash_commands` 에 등재 | 1 | 1 | fail→**pass** | 2/2 해소 | `GREEN — waiting on code-owner approval` | `raw/31-…jsonl` |
| 3 | "PR #3 on this repo is red and has unresolved review comments. Please work it until CI is green …" | `--plugin-dir` | v2 | **자동 로드**(`Skill(intent-sdlc-skills:pr-loop, "3")`) | 1 | 1 | fail→**pass** | 2/2 해소 | `GREEN — waiting on code-owner approval` | `raw/32-…jsonl` |
| 4 | "4번 PR 좀 봐줘. 체크가 빨간색이고 리뷰 코멘트도 몇 개 달렸어. 고쳐서 올리고 초록 될 때까지 돌봐줘." | `--plugin-dir` | v2 | **자동 로드**(`Skill(…, "4")`) | 1 | 1 | fail→**pass** | 2/2 해소 | `GREEN — 코드 오너 승인 대기` | `raw/33-…jsonl` |

명령: `cd <클론> && claude -p '<문구>' --plugin-dir <레포루트> --output-format stream-json --verbose
--dangerously-skip-permissions --max-turns 80`. 각 원문 파일 머리 세 줄에 축자로 있다. rc 는 모두 0.

## 모델의 주장이 아니라 GitHub 의 상태로 확인한 것

`raw/34-tests-after-state.txt` — 시험이 끝난 뒤 부모 세션이 따로 조회했다.

| PR | `gh pr checks` rc | 미해소 스레드 | 각 스레드에 답글 | 커밋 수 | state | reviewDecision |
|---|---|---|---|---|---|---|
| #1 | **0**(전 통과) | 0 | 있음 | 2 | OPEN | (없음) |
| #2 | **0** | 0 | 있음 | 2 | OPEN | (없음) |
| #3 | **0** | 0 | 있음 | 2 | OPEN | (없음) |
| #4 | **0** | 0 | 있음 | 2 | OPEN | (없음) |

- 네 번 다 **실패하던 체크가 실제로 초록**이 됐다(사전 상태 rc=1 → 사후 rc=0).
- 네 번 다 스레드 2건이 **답글 + resolve** 됐다. 답글은 고친 커밋 sha 를 인용한다.
- 네 번 다 **머지·승인하지 않았다**(state OPEN, reviewDecision 빈 값) — 가드레일대로다.
- 네 번 다 **한 라운드**에 끝났다. MAX_ROUNDS·진전 없는 라운드 정지는 이 시험대에서 **밟히지 않았다**(확인 못 함).

## 레슨 네 동작의 실증 지점

| 동작 | 어디서 보이나 |
|---|---|
| A 코멘트 수집 | 네 회 모두 `gh api graphql … reviewThreads` 호출이 스트림에 있다(#1 은 `raw/10` 4번째 도구 호출) |
| B 체크 수집 | `gh pr checks <n> --json name,state,bucket,link,workflow,description` → `gh run view <run-id> --log-failed` |
| C 수정·push | 커밋 1건 + `git push origin HEAD`. 사전에 `python3 -m unittest` 로컬 통과를 확인하고 push 한다 |
| D 그린까지 반복 | `gh pr checks <n> --watch --fail-fast` 로 새 실행을 기다려 `pass` 를 본 뒤에야 보고한다 |

## 부수적으로 실측한 것

- **답글 엔드포인트**: 후보 문서마다 세 갈래로 갈렸다(candidates 참조). 실제로 동작한 것은
  `POST repos/<owner>/<repo>/pulls/<n>/comments/<databaseId>/replies` — #1 에서 답글 id
  `3966873643`, `3966873876` 이 돌아왔다(`raw/10`). SKILL.md 는 이 경로만 적는다.
- **플러그인 이름 공간**: 세 회 모두 `slash_commands` 에 `intent-sdlc-skills:pr-loop` 로 등재됐다
  (S8 발견 2와 일치). `skills/pr-loop/` 와 이름이 같은 `commands/pr-loop.md` 는 두지 않았다(S8 발견 1).
- **자동 로드**: description 에 "Use this skill instead of reading the PR by hand or fixing one
  comment at a time" 를 넣은 v2 는 영어·한국어 자연어 양쪽에서 `Skill` 도구로 스스로 로드됐다
  (S8 발견 3 적용). v1 의 `disable-model-invocation: true` 는 v2 에서 뺐다 — 슬래시로도, 자연어로도 든다.

## 집합 충돌 시험

**해당 없음.** 이 레인의 채택 집합은 비었고 설계분 하나뿐이라 함께 넣을 다른 스킬이 없다.
같은 플러그인 안의 다른 세션 스킬(`secure-api-review`, `grilling`, …)과는 겨냥하는 자리가
겹치지 않는다(그쪽은 spec·intent 작성 시점, 이쪽은 PR 이 열린 뒤). 다만 **한 플러그인에 모두
넣은 상태로 같은 과제를 시켜 보지는 않았다** — 부모 세션이 전 레인을 모은 뒤 할 일이다.

## 확인 못 한 것

- MAX_ROUNDS(5) 도달, 진전 없는 라운드에서의 조기 정지, 병합 충돌(`CONFLICTING`) 경로,
  `REQUIRED_ONLY`·`LOCAL_CHECK`·`BOT_REVIEWERS` 설정, 리뷰 *body* 에만 findings 가 있는 경우,
  100건을 넘는 스레드의 페이지네이션 — 시험대가 한 라운드에 끝나서 밟히지 않았다.
- 가드레일의 **거부** 동작(시험을 지워 그린을 만들려는 유혹, 머지 요구)을 일부러 유도해 보지 않았다.
  네 회 모두 자발적으로 지켰다는 것만 확인했다.
- 봇 리뷰어(CodeRabbit·Copilot 등)가 붙은 PR, 여러 체크·여러 워크플로가 있는 PR.
