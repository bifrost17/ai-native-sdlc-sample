# tests/fixtures-metrics — 지표 계기의 입력 픽스처

`tests/test_metrics.py` 가 `tempfile` 로 **진짜 git 저장소**를 만들고 여기 있는 본문을
`intent/<ID>/{intent,spec,plan}.md` 로 심은 뒤 `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE` 를
고정해 커밋한다. 모의(mock)는 쓰지 않는다 — 재는 대상이 git 이력 그 자체이므로
git 을 대역으로 갈아 끼우면 계약을 증언하지 못한다.

치환 토큰은 `{{ID}}` 하나(사슬 ID). `created` 변형 4종은 `intent-*.md` 파일명이 구분한다:

| 파일 | 무엇을 심는가 |
|---|---|
| `intent-draft.md` | 정상 `created`(오프셋 있음) · `status: draft` |
| `intent-accepted.md` | `intent-draft.md` 와 같은 본문에서 `status: accepted` 만 다름 |
| `intent-created-future.md` | `created` 가 최초 커밋보다 미래 |
| `intent-created-missing.md` | `created` 키 자체가 없음 |
| `intent-created-no-offset.md` | `created` 가 오프셋 없는 ISO8601 |
| `spec.md` · `spec-v2.md` | spec 최초 커밋 · 그 이후 수정 1회 |
| `plan.md` | plan 최초 커밋 |
