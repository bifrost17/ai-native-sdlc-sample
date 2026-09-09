# Spec: 원장에 없던 건은 캐시하지 않는다 (from intent 0006-claims-status-stale-not-found)
Upstream: intent.md@386802088852c4c707de839f131bff41ceab873d. Status: draft.
Skills applied: design-spec, secure-api-review(읽기 전용 경로 — 인증·허용 목록·오류 문구 무변경, 아래 점검), plan.
Note: intent 는 아직 draft(PR A 미머지)다. 엔지니어(부모 세션)가 2026-09-09 draft 위에 착수를 지시했다(design-spec 「one exception」) — 승인은 여전히 PR A 의 머지다.
## Requirements
- R1 상류 조회가 「없음」(`None`)이면 그 결과를 캐시하지 않는다 — 다음 조회는 상류를 다시 부른다 (Problem: 원장에 생긴 건이 TTL 동안 not_found).
- R2 있는 건의 TTL 캐시는 그대로다: 같은 건 60초 안 재조회는 상류를 부르지 않는다 (intent C2 · 0002 R5).
- R3 응답 본문·오류 문구·허용 목록·소유 판정은 바뀌지 않는다 (intent C2 · 0002 R2~R4).
## Design
`records.py` `fetch_claim` 한 곳: 상류가 `None` 을 주면 `_CACHE` 에 쓰지 않고 그대로 돌려준다. 다른 모듈 무변경. 0002 spec Design 의
「없는 건도 캐시한다(없는 번호 반복 조회로 상류 예산을 태우지 못하게)」 결정을 이 사슬이 되돌린다 — 그 보호는 Flagged concerns 로 넘긴다.
secure-api-review 점검: ① 인증 — 경로·세션 판정 무변경 ② 입력 검증 — `C-<숫자>` 무변경 ③ 감사 — 읽기 전용, 없음 ④ 데이터 분류 — 캐시 내용·로그 정책 무변경(미스를 안 쓸 뿐).
## Constraints
- intent C1 draft 위 착수(엔지니어 지시) · C2 0002 계약 유지(R5·R3·R4·R2) · C3 범위 밖(claims-core·상담사 화면·알림·무효화 통지).
- 발견: 미스를 캐시하지 않으면 없는 번호 반복 조회가 상류로 그대로 간다 — 초당 50건 제한은 이 사슬이 지키지 않는다(F1).
## Open questions from intent
- Q1 상류 예산 보호의 대체 → carried forward: 이 사슬은 보호를 뺀다; 없는 번호에 대한 짧은 TTL·호출 상한은 별도 사슬 (claims-core 팀, 보안팀).
- Q2 09-02 실제 접수량·로그 → carried forward: 레포 밖 (포털 운영팀). 이 spec 은 코드 경로 재현만 근거로 삼는다.
## Flagged concerns
- F1 정확성(방금 접수한 건이 보인다)과 상류 예산(없는 번호 폭주) 이 맞선다 — 이 spec 은 정확성을 고른다. 누가 정하나: 서비스 오너 + claims-core 팀.
## Out of scope
없는 번호 전용 짧은 TTL · 호출 상한·레이트리밋 · 캐시 무효화 통지 · 밴드 설정 변경 · HTTP 배선.
## Acceptance criteria
- AC1 → R1 t=0 조회가 not_found 인 번호를 원장에 넣고 t=30 에 다시 조회하면 네 필드가 돌아오고 상류 호출은 2 다.
- AC2 → R2 있는 건을 t=0·t=59 조회하면 상류 호출 1 (기존 AC5 시험 그대로 그린).
- AC3 → R3 기존 `tests/test_claims_status.py` 전량 그린(시험 파일 무편집).
