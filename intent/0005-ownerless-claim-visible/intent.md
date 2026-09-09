# Intent: 가입자 표시가 없는 세션이 가입자 표시가 없는 청구 건을 볼 수 있다
Author: QA 엔지니어 (품질보증팀). Status: draft.
## Problem
티켓 경로. 청구 상태 조회 핸들러(`src/claims_status/routes.py`, intent 0002)를 입력 스윕으로 재어 보니 한 조합이
spec 0002 R1「그 세션의 고객이 낸 청구 건이면」을 어긴다. 2026-09-09 03:14 UTC, origin/main c03704d6, 20개 입력 중 재현 1건:
- 입력: 원장 행 `C-1001` 에서 `subscriber_id` 필드를 뺀다(또는 값이 `None`). 세션은 `{}` 또는 `{"subscriber_id": None}` — 가입자를 가리키지 않는 세션.
- 기대: `{"error":"not_found"}` (R4 — 세션의 고객이 낸 건이 아니면 남의 건과 같은 답).
- 실제: `{"claim_id":"C-1001","status":"심사중","next_step":"손해사정 결과 접수","due_date":"2026-09-15"}` — 청구 건 전체가 나간다.
- 같은 원장 행을 정상 세션 `{"subscriber_id":"S-77"}` 으로 조회하면 `not_found` 다. 즉 「양쪽이 다 비어 있으면 일치」로 판정된다.
- 재현: `python3 -c 'import sys;sys.path.insert(0,"src");from claims_status import records,routes;del records._UPSTREAM["C-1001"]["subscriber_id"];print(routes.get_claim_status("C-1001",{},now=0))'`
- 원장에 `subscriber_id` 가 비는 일이 실제로 있는지는 재지 못했다 — claims-core 팀이 답할 자리다. 스윕 전량은 QA 기록 `raw-chain5/01-probe-inputs.txt`.
## Proposed outcome
가입자를 가리키지 않는 세션은 어떤 청구 건도 보지 못하고, 가입자가 비어 있는 원장 행은 누구에게도 보이지 않는다. 검수: 위 재현 명령이 `{"error":"not_found"}` 를 찍고, 정상 세션의 자기 건 조회(0002 AC1)는 그대로 통과한다.
## Affected users and systems
사람: 청구를 낸 고객(남의 건이 보이는 쪽), 포털 팀(고치는 쪽), 클레임 운영팀(0002 검수자), 보안팀.
시스템: 고객 포털의 청구 상태 조회 핸들러, claims-core 원장(읽기만). 데이터: 청구 번호·상태·다음 단계·예정일 — 이 네 값이 소유자 확인 없이 나간다.
## Constraints
- 0002 의 제약 그대로: 기존 인증만 · 새 개인정보 없음 · 응답 필드 넓히지 않음 · 남의 건과 없는 건은 같은 `not_found`.
- 0002 의 시험 `tests/test_claims_status.py` 는 손대지 않는다 — 고친 뒤에도 그대로 통과해야 한다.
- 범위 밖: 세션 객체의 형식 검증 전반(리스트 세션이 예외를 내는 것은 별건), 청구 번호 형식 규칙 손질, 원장 데이터 정합성 정리.
## Open questions
- 원장 행에 `subscriber_id` 가 비는 경우가 실제로 생기는가(이관 중 건·법인 청구)? — 답할 사람: claims-core 팀.
- 가입자 표시가 없는 세션은 「세션 없음」(R2 `unauthenticated`)으로 볼 것인가, 「남의 건」(`not_found`)으로 볼 것인가? — 답할 사람: 포털 팀, 보안팀.
