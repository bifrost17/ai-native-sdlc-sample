---
id: {{ID}}
kind: intent
status: accepted
author: 홍길동 (청구운영팀)
created: 2026-09-09T10:12:00+09:00    # 첫 대화 시각(발의자 신고)
record: none
supersedes: none
---
# Intent: 청구 상태 자가조회

## Problem (문제)
공개 레퍼런스 레포를 실측했더니 뚫린 자리가 매번 같았다 — 인라인 코드 스팬
`status: accepted` 를 문서의 주장으로 읽어 위조가 통했다.

예시로 든 위조 frontmatter 는 이렇게 생겼다:

```yaml
---
status: accepted
---
```

## Proposed outcome (원하는 결과)
가입자가 스스로 상태를 조회한다.

## Affected users and systems (영향 범위)
가입자 · 청구 API

## Constraints (제약)
- C1 새 PII 를 노출하지 않는다

## Open questions (미결)
- Q1 캐시 만료를 몇 초로 하는가 — 청구운영팀
