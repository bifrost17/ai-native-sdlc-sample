# 조항 × 스킬 — pr-loop

**정책 파일이 없는 레인이다**(S7 변수 블록: `{POLICY} = 없음`). 그래서 행은 `policies/*.md` 의
조항 ID 가 아니라 **레슨 문장의 네 동작**이다 — 변수 블록의 지시 그대로.

> "Teams wrap the loop in a custom slash command that sweeps the PR's unresolved review comments
> and failing checks, addresses them and pushes fixes, until the PR is green and waiting on
> code-owner approval." — AI in the PR review loop (L10), 원문 `raw/lesson-ai-in-the-pr-review-loop.txt`

열은 후보 중 살아남은 것과 설계분. 공식 후보 5건은 A~D 를 하나도 온전히 덮지 못해 열에서 뺐다
(candidates.md 첫 표).

| # | 동작(레슨 문장) | `pr-loop`(설계) | `claude-code-action`(공식) | `review-pr`·`code-review`(공식) | `ralph-loop`(공식) |
|---|---|---|---|---|---|
| ① | unresolved review comments 수집 | **덮음** — GraphQL `reviewThreads`, `isResolved==false`, 두 커넥션 페이지네이션, 리뷰 body 도 읽음 | 부분 — `@claude` 가 달린 **그 코멘트 하나**만 본다 | — 리뷰를 만들 뿐 읽지 않는다 | — |
| ② | failing checks 수집 | **덮음** — `gh pr checks --json bucket…`, `gh run view --log-failed`, pending 대기, base 브랜치 대조 | 부분 — `actions: read` 가 있으면 워크플로 로그를 볼 수 있다 | — 명시적으로 "Do not check build signal" | — |
| ③ | addresses them and pushes fixes | **덮음** — 고치고, 로컬 시험 통과 확인 후 커밋·push, 스레드에 sha 답글 | **덮음** — 열린 PR 이면 그 브랜치에 직접 push | — | — |
| ④ | until green and waiting on code-owner approval | **덮음** — `--watch --fail-fast` 후 ①로 되돌아감, MAX_ROUNDS·진전없음 정지, 승인·머지 금지 | — 멘션 한 번에 한 번 반응. 스스로 반복하지 않는다 | — | 부분 — 반복 기구만. PR 을 모른다 |

## 겹침

- ③은 `pr-loop` 와 `claude-code-action` 이 함께 덮는다. **모순은 아니다** — 자리가 다르다.
  action 은 CI 안에서 리뷰어의 `@claude` 멘션에 반응하고, `pr-loop` 는 작성자 쪽 세션에서 PR 전체를
  훑는다. 레슨도 둘을 같이 놓는다("This fix loop runs through the claude-code-action. … Teams wrap
  the loop in a custom slash command"). 둘 다 켠 조직에서는 같은 지적을 두 번 고칠 수 있으므로,
  누가 먼저 손대는지는 **오너 결정 사항**(README 질문 3).
- ②는 `claude-code-action` 과 부분적으로 겹치지만 그쪽은 자기가 태그된 PR 의 로그를 *볼 수 있다*는
  능력이지 실패를 훑는 동작이 아니다.

## 모순

- **없음.** 단, `pr-loop` 의 가드레일 「승인·머지 금지」는 커뮤니티 후보 `duyet/…/babysit-pr` 의
  `--auto-merge` 와 정면으로 어긋난다. 그래서 그 후보를 기각했다(candidates.md). 우리 집합 안에는
  머지하는 스킬이 없다.
- 공식 `code-review` 의 "Do not check build signal … it is safe to assume that they will be run
  separately" 와 `pr-loop` 의 ②는 어긋나 보이나 자리가 다르다 — 전자는 *리뷰를 쓸 때* CI 를 대신
  하지 말라는 것이고, 후자는 *이미 나온 CI 결과*를 읽는 것이다.

## 빈칸과 이유

| 빈칸 | 왜 비었나 |
|---|---|
| `claude-code-action` ④ | 문서에 반복·재확인이 없다. `raw/04-claude-code-action-capabilities.txt` 를 직접 받아 확인했다 — 반복·CI 재실행에 관한 서술이 아예 없고, 승인·머지는 명시적으로 못 한다 |
| `review-pr` / `code-review` ①②④ | 설계 의도가 리뷰 *생성*이다. `code-review` 의 `allowed-tools` 에는 `git push` 조차 없다(`raw/official-code-review_…`) |
| `ralph-loop` ①②③ | PR·`gh` 를 모르는 범용 반복 기구다. `raw/official-ralph-loop_…` 전문 확인 |
| 정책 조항 행 자체 | 이 레인에는 `policies/*.md` 가 없다(S7 변수 블록). 조직이 나중에 PR 루프 정책을 쓰면 그때 행이 생긴다 — README 질문 1 |
| `pr-loop` 의 ④ 중 「진전 없는 라운드 정지」 | 문서에는 있으나 **시험에서 밟히지 않았다**(네 회 모두 1라운드로 끝남). trigger-tests 「확인 못 한 것」 |
