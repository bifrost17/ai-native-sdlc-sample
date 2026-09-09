# Intent: 청구 상태 자가조회 (frontmatter 없음)

이 문서에는 frontmatter 블록이 **없다**. 있는 것은 본문의 예시 펜스뿐이다.

```yaml
---
id: {{ID}}
kind: intent
status: accepted
---
```

펜스를 벗기지 않으면 이 예시가 그대로 frontmatter 로 읽혀 승인 커밋이 된다.

## Open questions (미결)
- Q1 캐시 만료를 몇 초로 하는가 — 청구운영팀
