# 조사 색인

| 스킬 | 세션 | 폴더 | 결론 | 조사 일자 |
|---|---|---|---|---|
| intent-template | S1 | `intent-template/` | 기준선 `capture-intent` 유지 + `to-questionnaire`·`grilling` 채택(mattpocock/skills@3cca18b, MIT, 원문 그대로 — 부모가 상류 sha256 재대조 MATCH) · 트리거 9/9 · 오너 질문 5 · PR #2 | 2026-09-09 |
| brand | S2 | `brand/` | (진행 중) | |
| compliance | S3 | `compliance/` | 채택 0(후보 18: 보류 4 · 기각 14 — 3년 보존·C4 동의·C7 대리 조회를 덮는 공개 스킬 없음) · 설계 2(`claim-data-compliance` C1·C2·C3·C6·C7 · `claim-notice-compliance` C4·C5) · 트리거 6/6 · 오너 질문 8 · PR #8 | 2026-09-10 |
| ux | S4 | `ux/` | 채택 2(`ux-copy` Apache-2.0 공식 · `accessibility` MIT, 원문 그대로) · **설계 2**(`claims-ux-copy` U1~U3 · `claims-ux-interaction` U4~U6) · 기각 30 · 보류 7(라이선스 불명·KWCAG) · 오너 질문 10 | 2026-09-09 |
| secure-api-review | S5 | `secure-api-review/` | 채택 2(기준선 · secrets-scan) · 설계 1(claims-api-security) · 기각 27 · 보류 2 | 2026-09-09 |
| spec-command | S6 | `spec-command/` | (진행 중) | |
| pr-loop | S7 | `pr-loop/` | 채택 0 · **설계** `pr-loop` · 실 PR 4/4 완주 | 2026-09-09 |
| plugin | S8 | `plugin/` | 레포 = 플러그인 1 + 마켓플레이스 1(`.claude-plugin/`) · 헤드리스 로드 12/12 · 대체 경로 `.claude/skills/` 복사 · 오너 질문 6 · PR #1 | 2026-09-09 |

겹치는 후보는 부모 세션이 여기서 한 번 묶는다.
