# 변수 블록 — S7 · pr-loop

- {N} = 7 · {SKILL} = pr-loop · {POLICY} = 없음
- 브랜치 lane/S7-pr-loop · 산출 폴더 docs/research/pr-loop/ · 결정 docs/decisions/S7-pr-loop.md
- 해당 레슨: https://academy.claude.com/courses/ai-native-sdlc-playbook/ai-in-the-pr-review-loop

## 특별 지시
레슨 문장: "Teams wrap the loop in a custom slash command that sweeps the PR's unresolved review comments and failing checks, addresses them and pushes fixes, until the PR is green and waiting on code-owner approval."
과제: 이 일을 하는 slash command 를 구해 온다 — 공식 PR 리뷰/수정 플러그인·명령과 대조해 채택하거나 `/pr-loop` 를 설계한다. `gh` CLI 로 코멘트·체크를 읽고, 고치고, push 하고, 다시 확인하는 루프여야 한다.
트리거 시험 대신 **임시 레포의 실제 PR** 에서 시험한다: 리뷰 코멘트 2건 + 실패하는 체크 1건을 만들어 두고 명령이 완주하는 원문(코멘트 해소 · 체크 그린 · push 이력)을 raw/ 에. 정책 파일 없음 — coverage 는 레슨 문장의 네 동작(코멘트 수집 · 체크 수집 · 수정 push · 그린까지 반복)을 행으로.
