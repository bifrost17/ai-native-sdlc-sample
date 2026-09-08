---
id: {{ID}}
kind: intent
status: `accepted`
author: 홍길동 (청구운영팀)
created: 2026-09-09T10:12:00+09:00    # 첫 대화 시각(발의자 신고)
record: none
supersedes: none
---
# Intent: 청구 상태 자가조회

frontmatter 의 **값 자체**가 인라인 코드 스팬이다. 스팬을 벗기면 값이 빈
문자열이 되고, 벗기지 않으면 백틱째로 읽힌다 — 어느 쪽이든 승인이 아니다.

본문에도 픽스액스가 셀 문자열이 하나 있다: `status: accepted` (예시일 뿐이다).

## Open questions (미결)
- Q1 캐시 만료를 몇 초로 하는가 — 청구운영팀
