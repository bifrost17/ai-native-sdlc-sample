<!--
사슬 4문 — intent → spec → plan → 코드 순서가 이 PR 에서 실제로 지켜졌는지 스스로 답한다.
답 없이 올린 PR 은 REVIEW.md 의 compliance 패스에서 Important 로 잡힌다.
-->

## 1. 상류 아티팩트

이 PR 이 이어받는 상류 아티팩트(intent.md 또는 spec.md)와 그 커밋 sha 는?

- 상류: ‹intent.md@<sha> 또는 spec.md@<sha>›
- 그 상류는 지금 `accepted` 상태인가? ‹예/아니오 — 아니오면 왜 진행하는지›

## 2. Files that change 일치

`plan.md` 의 `## Files that change` 절에 적힌 목록과 이 diff 의 실제 변경 파일이 일치하는가?

- ‹일치 / 불일치 — 불일치면 어떤 파일이 plan 밖인지, 같은 커밋에서 plan 을 고쳤는지›

## 3. Proof

`plan.md` 의 `## Proof` 절이 지목한 시험을 실제로 돌린 출력을 붙여라(명령 + rc + 결과 줄).

```
‹여기에 원문 출력›
```

## 4. status 전이

이 PR 이 바꾸는 아티팩트의 `status:` 는 무엇에서 무엇으로 바뀌는가? (바뀌는 게 없으면 "없음"이라 적는다.)

- ‹예: 0002-claims-status/intent.md — draft → accepted›
