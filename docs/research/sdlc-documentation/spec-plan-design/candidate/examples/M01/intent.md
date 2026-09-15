# Intent: 여러 동료의 완료 결과가 서로 덮어써지지 않게 보존
Author: 합성 업무 오너 M01. Status: draft.

## Problem
JSON 전체를 읽고 쓰는 서비스가 서로 다른 요청의 동시 완료 중 먼저 쓴 결과를 잃을 수 있다.
## Proposed outcome
여러 동료의 처리 결과와 기존 데이터를 보존하고 기존 웹/API를 계속 사용하고 싶다.
개발자가 SQLite를 제안했으며 이행·복구까지 검토해야 한다.
## Affected users and systems
웹/API, 저장소, 아직 확인이 필요한 API 밖 소비자.
## Constraints
ID·필드·순서·API·권한 유지, 외부 서비스·계정 추가 없음. 짧은 중지는 허용, 결과 유실은 금지.
## Open questions
- Q1 API 밖 읽기/쓰기 소비자가 있는가?
- Q2 실패·재실행·전환 후 복구는 어떤 데이터를 보존해야 하는가?
- Q3 환경과 운영 책임자는 누구인가?

[context](context.md)의 후속 합성 결정으로 질문에 답한다.
