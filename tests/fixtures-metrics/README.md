# tests/fixtures-metrics — 지표 계기의 입력 픽스처

`tests/test_metrics.py` 가 `tempfile` 로 **진짜 git 저장소**를 만들고 여기 있는 본문을
`intent/<ID>/{intent,spec,plan}.md` 로 심은 뒤 `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE` 를
고정해 커밋한다. 모의(mock)는 쓰지 않는다 — 재는 대상이 git 이력 그 자체이므로
git 을 대역으로 갈아 끼우면 계약을 증언하지 못한다.

치환 토큰은 `{{ID}}` 하나(사슬 ID). 변형은 `intent-*.md` 파일명이 구분한다:

| 파일 | 무엇을 심는가 |
|---|---|
| `intent-draft.md` | 정상 `created`(오프셋 있음) · `status: draft` |
| `intent-accepted.md` | `intent-draft.md` 와 같은 본문에서 `status: accepted` 만 다름 |
| `intent-created-future.md` | `created` 가 최초 커밋보다 미래 |
| `intent-created-missing.md` | `created` 키 자체가 없음 |
| `intent-created-no-offset.md` | `created` 가 오프셋 없는 ISO8601 |
| `intent-draft-code-span.md` | `status: draft` 인데 **본문**에 인라인 코드 스팬과 코드 펜스로 `status: accepted` 예시가 있다(픽스액스 오판 재현) |
| `intent-accepted-code-span.md` | 위와 본문이 같고 frontmatter `status` 만 `accepted` — **진짜** 승인 커밋 |
| `intent-draft-one-example.md` | `status: draft` 인데 본문 예시가 **정확히 한 번**만 나온다 — 「같은 커밋에서 예시를 지우면서 승인(등장 1→1)」 갈래를 만들려면 등장 횟수가 1 이어야 한다 |
| `intent-fence-before-frontmatter.md` | 예시 펜스가 **진짜 frontmatter 앞**에 있다 — 코드 펜스를 벗기지 않으면 첫 `---` 블록이 예시 쪽이라 accepted 로 읽힌다 |
| `intent-span-valued-status.md` | frontmatter 의 **값 자체**가 인라인 스팬(`` status: `accepted` ``) — 벗기면 빈 값, 안 벗기면 백틱째로 읽힌다 |
| `intent-fence-only-no-frontmatter.md` | frontmatter 가 아예 없고 예시 펜스만 있다 — 벗기지 않으면 그 예시가 frontmatter 로 승격한다 |
| `spec.md` · `spec-v2.md` | spec 최초 커밋 · 그 이후 수정 1회 |
| `plan.md` | plan 최초 커밋 |
