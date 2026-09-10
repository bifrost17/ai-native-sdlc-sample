# 챕터별 집계

| 챕터 | 블록 | 충실 | 부분 | 팀 몫 | 보완 | 반영 PR(ai-native-sdlc-sample, 옛 이름 intent-sdlc-sample) | 커밋 |
|---|---|---|---|---|---|---|---|
| 1 소개 | — | — | — | — | — | 검증 대상 아님 | — |
| 2 intent.md로 포착하기 · v1 | 16 | 12 | 3 | 0 | 1 | — | 5fb7b8d |
| 2 intent.md로 포착하기 · v2 | 16 | 12 | 3 | 1 | 0 | #44 (c76bff04 · leading 분자 · 비엔지니어 커밋 경로 · intent/** 코드오너 · H 발화 미기록) | |
| 3 요구사항과 design · v1 | 16 | 11 | 4 | 1 | 0 | — (보완 후보 2: Skills applied 에 스킬 sha · /spec 명령 안 팀 마커 이동) | 3542a00 |
| 3 요구사항과 design · v2 | 16 | 11 | 4 | 1 | 0 | #45 (409ea98 · Skills applied name@sha · 팀 마커 프롬프트 밖으로) | |
| 4 Claude Code plan mode · v1 | 18 | 13 | 5 | 0 | 0 | — (보완 후보 5: Status 문면 통일 · 고위험→tech lead 팀 자리 · 첫 패스 비율 명령 · plan 대조 명령 PR 단위로 · auto mode 한 줄 · RUNS 증거 한계 L4 317) | 239d0a6 |
| 4 Claude Code plan mode · v2 | 18 | 16 | 2 | 0 | 0 | #46 (8350fc1 · Status draft 고정 · 고위험 경로 팀 자리 · L4 측정 명령 2 · auto mode 줄 · L4 317 미측정 기록) | 54db497 |
| 5 CLAUDE.md · v1 | 11 | 7 | 3 | 1 | 0 | — (보완 후보 2: 「두 번째면 CLAUDE.md」 규칙 줄 · RUNS L5 정정 PR 목록·반복 횟수) | 5542b75 |
| 5 CLAUDE.md · v2 | 11 | 9 | 1 | 1 | 0 | #47 (6084fcf · REVIEW.md 규칙 줄 · RUNS L5 정정+반복 실측) | |
| 6 skill · v1 | 16 | 13 | 1 | 2 | 0 | — (경미 2: RUNS 에 L6 470 트리거 실측 · L6 lagging 수열) | cd71c39 |
| 6 skill · v2 | 16 | 14 | 0 | 2 | 0 | #48 (1adef5a · RUNS L6 470 · L6 505) | |
| 7 병렬 session·subagent · v1 | 12 | 8 | 4 | 0 | 0 | — (보완 후보 2: verifier 호출 계기(CLAUDE.md 한 줄) · settings.json 권한 allow 목록) | abdc58e |
| 7 병렬 session·subagent · v2 | 12 | 11 | 1 | 0 | 0 | #49 (2f00415 · CLAUDE.md verifier 줄 · permissions.allow · RUNS L8) | |
| 8 feedback loop · v1 | 17 | 14 | 2 | 1 | 0 | — (보완 후보 3: RUNS Not confirmed 의 Actions 오기 · BOUNDARY Stop hook 결정 · ADOPTING UI 도구 행) | c7a9a4d |
| 8 feedback loop · v2 | 17 | 16 | 0 | 1 | 0 | #50 (64c7100 · RUNS Actions 정정 · BOUNDARY Stop hook · ADOPTING UI 행) | |
| 9 CI 지속적 eval · v1 | 13 | 8 | 3 | 2 | 0 | — (보완 후보 3: ADOPTING required checks 행 · 워크플로 결과 artifact 보존 · METRICS L10 명령 2 · 커밋 메시지의 7/4 는 오기) | a8774b4 |
| 9 CI 지속적 eval · v2 | 13 | 10 | 1 | 2 | 0 | #51 (cd5c3af · artifact 보존 · ADOPTING branch protection 행 · METRICS L10 · RUNS) | |
| 10 PR review loop · v1 | 13 | 6 | 5 | 2 | 0 | — (보완 후보 3: ADOPTING Claude review 통합 행 + BOUNDARY · REVIEW.md 발견은 PR 코멘트로 · METRICS L11 명령 · 커밋 메시지의 5/6 은 오기) | 0876639 |
| 10 PR review loop · v2 | 13 | 8 | 3 | 2 | 0 | #52 (464bac1 · ADOPTING reviewer 통합 행 · BOUNDARY · REVIEW.md 발견은 PR 에 · METRICS L11 · RUNS) | |
| 11 approval gate hook · v1 | 15 | 12 | 0 | 3 | 0 | — (보완 없음 · v2 불요) | |
| 12 CI/CD · v1 | 16 | 2 | 9 | 5 | 0 | — (보완 후보 2: check.yml 에 실패 build 분류 단계(예시 축자, 키 게이트) · METRICS L13 leading) | d7a847b |
| 12 CI/CD · v2 | 16 | 5 | 6 | 5 | 0 | #53 (09cb128 · check.yml Triage failed build · METRICS L13 · MAP · RUNS) | |
| 13 metrics 로 loop 닫기 · v1 | 16 | 8 | 6 | 2 | 0 | — (보완 후보 3: bands.yml 2σ/3σ claude -p 진단 단계(키 게이트) · METRICS L14 leading detected_at · ADOPTING Claude Tag 행) | 22e1946 |
| 13 metrics 로 loop 닫기 · v2 | 16 | 11 | 3 | 2 | 0 | #54 (0daf655 · bands.yml 진단 단계 · ADOPTING 채널 유입 행 · METRICS L14 · RUNS) | |
| 14 맺음말과 참고 자료 | — | — | — | — | — | 검증 대상 아님(가이드 문단 없음 · 참고 자료 목록) | — |

## 최종 집계 (2026-09-09, 챕터 2~13 마지막 라운드 기준)

블록 179 · 충실 135 · 부분 24 · 팀 몫 20 · 보완 필요 0. 샘플 레포 반영 PR: #44 #45 #46 #47 #48 #49 #50 #51 #52 #53 #54 (main `0daf655`).
「부분」은 단일 계정·API 키 없음으로 이 검증에서 실행하지 못한 것(코드오너 승인 · required checks · evals/triage/진단 단계 · 다음 사슬에서 확인할 문면)이고, 「팀 몫」은 조직 정책·인프라(정책 스킬 · 승인 목록 · 배포·sandbox·MCP · 채널 유입 · 20~50 eval · /init)로 ADOPTING.md 에 자리가 적힌 것이다.

