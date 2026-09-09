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

본문에 예시 frontmatter 가 **정확히 한 번** 나온다. 등장 횟수를 1 로 고정해야
「같은 커밋에서 예시를 지우면서 승인한다(1→1)」 갈래를 만들 수 있다.

```yaml
---
status: accepted
---
```

## Open questions (미결)
- Q1 캐시 만료를 몇 초로 하는가 — 청구운영팀
