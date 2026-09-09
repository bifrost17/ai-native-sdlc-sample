```yaml
---
id: {{ID}}
kind: intent
status: accepted
---
```

---
id: {{ID}}
kind: intent
status: draft
author: 홍길동 (청구운영팀)
created: 2026-09-09T10:12:00+09:00    # 첫 대화 시각(발의자 신고)
record: none
supersedes: none
---
# Intent: 청구 상태 자가조회

문서가 **먼저** 예시 frontmatter 를 펜스로 보여 주고 그 다음에 진짜
frontmatter 를 쓴다. 코드 펜스를 벗기지 않으면 첫 `---` 블록이 예시 쪽이라
`status` 가 accepted 로 읽힌다 — 위조가 통하는 자리다.

## Open questions (미결)
- Q1 캐시 만료를 몇 초로 하는가 — 청구운영팀
