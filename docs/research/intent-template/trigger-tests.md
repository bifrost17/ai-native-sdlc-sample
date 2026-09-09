# 트리거 시험 — intent-template (S1)

## 방법

임시 프로젝트 세 개를 만들어(각각 `git init` + `README.md` + 빈 `intent/`) `.claude/skills/<name>/SKILL.md` 로 스킬을 넣고, 헤드리스로 과제를 시켰다:

```
claude -p '<프롬프트>' --output-format stream-json --verbose --max-turns N < /dev/null
```

실행기는 `raw/run-trigger.sh`(레포에 커밋돼 있다). 매 실행마다 `raw/NN-<이름>.jsonl`(스트림 원문)과 `raw/NN-<이름>.txt`(`CMD:`·`AT_UTC:`·`RC:` 머리 + 도구 호출 요약)를 남긴다.

| 프로젝트 | 넣은 스킬 |
|---|---|
| `/tmp/s1-trig-a` | `capture-intent` 단독 |
| `/tmp/s1-trig-b` | `capture-intent` + `to-questionnaire` + `grilling` (**채택 집합**) |
| `/tmp/s1-trig-c` | `capture-intent` + superpowers `brainstorming` (충돌 시험용) |

**판정 근거 두 가지.** 모델이 스스로 부르는 스킬은 스트림에 `tool_use` `Skill{skill: …}` 로 찍힌다 — 이것이 로드의 직접 증거다. 반면 `disable-model-invocation: true` 인 스킬을 사람이 `/이름` 으로 부르면 **본문이 프롬프트에 인라인 확장되어 `Skill` 도구 호출이 남지 않는다.** 그래서 `to-questionnaire` 는 *그 스킬에만 있는 절차를 실제로 따랐는가*로 판정했다(「주제가 아니라 보내는 일을 인터뷰한다」 → 1단계 수신자, 2단계 필요한 것). 세션 시작 이벤트의 `slash_commands`·`skills` 목록에 세 스킬이 모두 실려 있는 것도 확인했다(`raw/50-tq-slash-1.jsonl` init 이벤트).

## 1. capture-intent (기준선) — 3/3

레슨이 말하는 세 유입 경로(사람의 아이디어 · 티켓 · 인시던트 알림)를 서로 다른 문구로 하나씩.

| # | 원문 | 문구 요지 | AT_UTC | RC | 로드된 스킬 | 결과 |
|---|---|---|---|---|---|---|
| 1 | `raw/40-ci-idea.txt` | "…support team spends a third of every call telling customers where their claim is… **Write this up as an intent file for our repo.**" | 2026-09-09T13:14:30Z | 0 | `capture-intent` | **통과.** 로드 후 `intent/` 를 세어 `0001` 을 정하고, 「제3자 추정인지 측정치인지」 등 관측 사실을 되물었다 |
| 2 | `raw/41-ci-ticket.txt` | "**Ticket JIRA-4412 from ops:** 'Nightly export job silently skips rows with a null region…' **Turn this ticket into an intent** for our repo." | 2026-09-09T13:15:16Z | 1(`error_max_turns`) | `capture-intent` | **통과.** 첫 턴에 로드. RC 1 은 트리거 실패가 아니라 `--max-turns 5` 소진 — 이미 `intent/0001-nightly-export-drops-null-region-rows/intent.md` 를 쓰는 중이었다 |
| 3 | `raw/42-ci-incident.txt` | "**An alert fired at 2026-09-08T03:14Z**: checkout p99 latency… **Capture it so the product owner can decide** whether we take it on." | 2026-09-09T13:16:31Z | 1(`error_max_turns`) | `capture-intent` | **통과.** 로드 후 앞선 intent 를 읽어 번호를 잇고 UTC 시각을 확보. RC 1 은 턴 소진 |

「intent」라는 낱말이 없는 3번에서도 떴다. 트리거 문장을 고칠 이유가 없었다.

## 2. to-questionnaire (채택) — 3/3 (슬래시), 자동 로드 0/1 (**의도된 것**)

| # | 원문 | 문구 요지 | AT_UTC | RC | `Skill` 호출 | 결과 |
|---|---|---|---|---|---|---|
| 1 | `raw/50-tq-slash-1.txt` | `/to-questionnaire` + "두 open question 을 Priya 와 Sam 이 답할 수 있다. PO 리뷰 전에 답이 필요하다" | 2026-09-09T13:17:03Z | 0 | 없음(인라인 확장) | **통과.** 스킬 고유 1단계로 들어갔다 — "**Step 1 — who's it going to?**" 그리고 수신자가 둘이니 문서를 나눌지부터 물었다 |
| 2 | `raw/51-tq-slash-2.txt` | `/to-questionnaire` + "finance 가 행 수 일치에 의존하는지 내가 답을 못 한다. Maria 가 안다" | 2026-09-09T13:18:28Z | 0 | 없음(인라인 확장) | **통과.** "**Step 1 — who is Maria?**" 로 역할·기술 수준을 먼저 물었다 |
| 3 | `raw/55-tq-slash-3.txt` | `/to-questionnaire` + "PO 가 intent 0003 을 보기 전에 claims-core API 오너가 무엇을 돌려줄 수 있는지 알아야 한다" | 2026-09-09T21:59:45Z | 0 | 없음(인라인 확장) | **통과.** "**Step 1 — who's receiving this?**" |
| 4 | `raw/52-tq-natural.txt` | 슬래시 없이 자연어: "Turn them into a questionnaire I can hand to her…" | 2026-09-09T13:18:53Z | 0 | 없음 | **의도대로.** 자동 로드되지 않았고, 모델이 스스로 "this repo has a `/to-questionnaire` skill built for exactly this task, but it's marked `disable-model-invocation`, so only you can trigger it" 라고 알렸다. 사람만 부르는 스킬이라는 성질이 실측으로 확인됐다 |

## 3. grilling (채택) — 3/3

| # | 원문 | 문구 요지 | AT_UTC | RC | 로드된 스킬 | 결과 |
|---|---|---|---|---|---|---|
| 1 | `raw/54-grill-idea.txt` | "**Grill me on this idea** before I write it up as an intent…" | 2026-09-09T21:57:46Z | 0 | `grilling` | **통과.** 게다가 "as phrased, this isn't an intent, it's a solution … The intent template wants the thing that can't be done today" 라며 해법을 문제로 되돌렸다 |
| 2 | `raw/56-grill-2.txt` | "**Stress-test my thinking** on this before it becomes an intent… **Push back hard**" | 2026-09-09T22:00:03Z | 0 | `grilling` | **통과.** 「해법으로 위장한 인과 주장」을 첫 표적으로 지목 |
| 3 | `raw/57-grill-3.txt` | "**Interrogate me** about the claims status idea until we actually agree what the problem is…" | 2026-09-09T22:01:17Z | 0 | `grilling` | **통과.** 라운드 1 을 열며 "답에 dashboard·portal 같은 명사가 나오면 해법이라 되받겠다"는 규칙을 먼저 선언 |

「grill」이 없는 2·3번 문구(stress-test / interrogate)에서도 떴다. 트리거 문장을 고칠 이유가 없었다.

## 4. 집합 시험 — 지시가 어긋나는가

| # | 프로젝트 | 원문 | 과제 | AT_UTC | RC | 로드 | 결과 |
|---|---|---|---|---|---|---|---|
| A | `s1-trig-b`(채택 집합 3종) | `raw/53-set-idea.txt` | §1-1 과 **같은** intent 과제를 세 스킬이 다 있는 상태에서 한 번 더 | 2026-09-09T13:17:24Z | 0 | `capture-intent` | **통과.** `grilling` 도 `to-questionnaire` 도 끼어들지 않았다. 그리고 `capture-intent` 규칙대로 물었다 — "the skill's rule is that Problem carries observed facts in your words, and anything nobody can answer stays an open question rather than getting invented" |
| B | `s1-trig-b` | `raw/52-tq-natural.txt` | 질문지 과제를 자연어로 | 2026-09-09T13:18:53Z | 0 | 없음 | **통과.** 위 §2-4 참조 — 사람이 부르라고 안내 |
| C | `s1-trig-b` | `raw/54,56,57` | grill 계열 3문구 | — | 0 | `grilling` | **통과.** intent 를 쓰라는 과제가 아닐 때만 `grilling` 이 뜬다 |
| D | `s1-trig-c`(기준선 + superpowers `brainstorming`) | `raw/60-bs-collision.txt` | §1-1 과 같은 intent 과제 | 2026-09-09T21:58:33Z | 0 | `capture-intent` | **통과(단 조건부).** `brainstorming` 의 "You MUST use this before any creative work" 에도 불구하고 `capture-intent` 가 이겼다. 그러나 이 한 문구에서 드러나지 않았을 뿐 두 스킬의 지시는 서로 어긋난다(설계 문서 산출 vs 해법 금지) — 그래서 `brainstorming` 은 기각이다 |

**결론: 채택 집합(capture-intent + grilling + to-questionnaire)에서 어긋난 지시는 관측되지 않았다.** 자리 배분은 문구가 가른다 — 「intent 로 써 달라」는 기준선, 「grill/stress-test/interrogate」는 grilling, 질문지는 사람이 슬래시로.

## 5. 확인 못 한 것

- **`to-questionnaire` 의 파일 산출을 끝까지 보지 못했다.** 세 번 모두 스킬 절차의 1단계(수신자 확인)에서 사용자 답을 기다리며 멈췄고, 헤드리스라 답할 사람이 없었다. `to-questionnaire-<slug>.md` 가 실제로 쓰이는 것까지는 확인 못 함.
- **슬래시 확장의 직접 증거(도구 호출 기록)는 존재하지 않는다.** 확장된 본문은 스트림에 실리지 않는다. 위 판정은 행동 증거(스킬 고유 2단계 절차)와 init 이벤트의 스킬 목록에 근거한다.
- **`raw/41`·`raw/42` 의 RC 는 1**(`error_max_turns`)이다. 트리거는 성공했고 종료 코드는 턴 상한 때문이다. 초기 실행 두 건(`54`·`60`)은 세션 한도(429)로 무효였고 같은 프롬프트로 다시 돌려 위 표의 값을 얻었다 — 무효 실행의 흔적은 재실행으로 덮였다.
