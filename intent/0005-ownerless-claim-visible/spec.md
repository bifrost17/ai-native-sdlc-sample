Note: intent 는 아직 draft(PR #20 미머지)다. 엔지니어(부모 세션)가 2026-09-09 draft 위에 착수를 지시했다(design-spec 「one exception」) — 승인은 여전히 PR #20 의 머지다.
# Spec: 소유 판정에서 빈 가입자 표시는 불일치다 (from intent 0005-ownerless-claim-visible)
Upstream: intent.md@56e60c891fe42b541c4d25f1b172bb3060072539. Status: draft.
Skills applied: secure-api-review (① 인증·④ 데이터 분류만 해당), design-spec.
## Requirements
- R1 원장 행의 `subscriber_id` 가 없거나 비어 있으면(`None`·`""`) 그 건은 어떤 세션에도 `not_found` 다 (Problem: 가입자 없는 행이 나갔다).
- R2 세션의 `subscriber_id` 가 없거나 비어 있으면 어떤 건도 `not_found` 다 — 「양쪽 다 비어 있음」은 일치가 아니다 (Problem: `None == None`).
- R3 0002 의 R1~R5 와 시험 `tests/test_claims_status.py` 는 그대로 통과한다 (Constraints).
## Design
`routes.py` 의 소유 판정 한 자리만 바꾼다: 원장의 `subscriber_id` 를 꺼내 **truthy 이고** 세션 값과 같을 때만 소유로 본다. 판정을 다른 모듈로 옮기지 않는다(0002 spec 「하나여야 하는 것은 한 파일에」). 오류 문구는 0002 의 고정 셋 그대로 — 새 코드·새 필드 없음.
secure-api-review: ① 인증 — 빈 세션은 여전히 세션 객체이므로 `unauthenticated` 로 바꾸지 않고 `not_found` 로 둔다(정책 변경은 Open questions). ④ 데이터 분류 — 응답·오류 문구에 새 값 없음.
## Constraints
- intent: 기존 인증만 · 새 개인정보 없음 · 응답 필드 불변 · 남의 건과 없는 건은 같은 `not_found` · 0002 시험 무편집 · 범위 밖(세션 형식 검증 전반·번호 형식·원장 정합성).
- 발견: 빈 세션이 상류를 한 번 부르는 것(R2 관점)은 이번에 바꾸지 않는다 — 판정 순서를 옮기면 0002 AC2 의 「세션 None → 상류 0」 계약과 얽힌다.
## Open questions from intent
- 원장 행에 `subscriber_id` 가 비는 경우가 실제로 생기는가 → carried forward (claims-core 팀). 설계는 「생기든 안 생기든 안 나간다」로 답하지 않고 막는다.
- 가입자 표시 없는 세션을 `unauthenticated` 로 볼 것인가 `not_found` 로 볼 것인가 → carried forward (포털 팀·보안팀). 답이 오기 전엔 `not_found`(존재 여부가 새지 않는 쪽).
## Flagged concerns
- F1 빈 세션 → `not_found` 는 0002 F2(오타 고객도 같은 문구) 와 같은 결의 결정이다. 문구를 나누려면 법무 개인정보 담당.
## Out of scope
세션 객체가 dict 가 아닐 때의 예외(리스트 세션 → AttributeError, 스윕에서 관찰) · 청구 번호 끝 개행(`"C-1001\n"`)이 형식 검사를 통과해 상류를 부르는 것(스윕에서 관찰 · 별 티켓) · 원장 데이터 정리.
## Acceptance criteria
- AC1 → R1 원장 행에서 `subscriber_id` 를 빼고 세션 `{}` 로 조회하면 본문이 정확히 `{"error":"not_found"}` 이고 상태·다음 단계·예정일 값이 본문에 없다.
- AC2 → R2 원장 행은 그대로(`S-77`) 두고 세션 `{"subscriber_id": None}` 으로 조회하면 `{"error":"not_found"}`; 원장 `None` × 세션 `None` 도 같다.
- AC3 → R3 `make check` rc=0, `tests/test_claims_status.py` sha256 불변.
