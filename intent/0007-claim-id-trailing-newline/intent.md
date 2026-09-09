# Intent: 청구 번호 끝의 개행이 형식 검사를 통과해 상류를 한 번 부른다
Author: 리뷰어 (사슬 0005 입력 스윕 재현 · GitHub 이슈 #24). Status: draft.
## Problem
티켓 경로(GitHub 이슈 #24). 청구 상태 조회 핸들러(`src/claims_status/routes.py`, intent 0002)의 청구 번호 형식 검사가
spec 0002 AC4「형식이 틀린 번호는 `invalid_claim_id`」와 R2 계열의 「형식이 틀리면 상류 호출 0」을 어긴다.
사슬 0005 의 입력 스윕에서 관찰(2026-09-09 03:14 UTC, origin/main c03704d6)되어 별 티켓으로 넘긴 건이고,
2026-09-09 origin/main 553b881 에서 다시 잰다:
- 입력: `claim_id = "C-1001\n"`(끝에 개행 하나). 세션은 정상 `{"subscriber_id": "S-77"}`.
- 기대: `{"error":"invalid_claim_id"}` · 상류 호출 0 (spec 0002 AC4).
- 실제: `{"error":"not_found"}` · **상류 호출 1**.
- 재현: `python3 -c 'import sys;sys.path.insert(0,"src");from claims_status import records,routes;print(routes.get_claim_status("C-1001\n",{"subscriber_id":"S-77"},now=0), records.upstream_calls())'`
  → `{"error": "not_found"} 1`
- 같은 조회를 세션 `{}` 로 해도 `{"error":"not_found"}` · 상류 호출 1 이다 — 형식 검사가 아니라 소유 판정에서 걸린다.
- 스윕에서 같이 잰 이웃 입력은 형식 검사에서 걸린다: `"\nC-1001"` · `"C-1001\nX"` · `"C-1001\r"` 는 `invalid_claim_id` · 상류 호출 0.
- 응답 문구는 새지 않았다(`not_found` 는 없는 건과 같은 문구다). 새는 것은 **상류 호출 예산**이고, 형식이 틀린 입력이 원장까지 간다는 사실이다.
- 스윕 전량은 QA 기록 `raw-chain5/01-probe-inputs.txt`, 리뷰 기록 `raw-chain56R/05`(둘 다 세션 스크래치, 이 레포 밖).
## Proposed outcome
끝에 개행이 붙은 청구 번호는 형식 단계에서 `invalid_claim_id` 로 끊기고 상류 claims-core 를 부르지 않는다.
검수: 위 재현 명령이 `{"error": "invalid_claim_id"} 0` 을 찍고, 정상 번호 조회(0002 AC1)와 없는 번호 조회(0002 AC4)는 그대로다.
## Affected users and systems
사람: 포털 팀(고치는 쪽), claims-core 팀(초당 50건 예산을 대는 쪽), 클레임 운영팀(0002 검수자), 품질보증팀(스윕을 낸 쪽).
시스템: 고객 포털의 청구 상태 조회 핸들러, claims-core 원장(읽기만) · TTL 캐시. 데이터: 청구 번호 문자열 하나 — 응답에 새로 실리는 값은 없다.
## Constraints
- 0002 의 제약 그대로: 기존 인증만 · 새 개인정보 없음 · 응답 필드 넓히지 않음 · 남의 건과 없는 건은 같은 `not_found` · 오류 문구에 입력을 되비추지 않음.
- 0002 의 시험 `tests/test_claims_status.py`, 0005 의 `tests/test_claims_status_defect.py`, 0006 의 `tests/test_claims_status_incident.py` 는 손대지 않는다 — 고친 뒤에도 그대로 통과해야 한다.
- 범위 밖: 청구 번호 형식 규칙 자체를 넓히거나 좁히는 것(`C-<숫자>` 는 그대로) · 입력을 다듬어서 받아 주는 것(strip 후 통과는 형식 규칙 변경이다) · 세션 객체가 dict 가 아닐 때의 예외(이슈 #25) · 미스 캐시와 상류 예산(이슈 #26).
## Open questions
- 포털 프론트엔드나 게이트웨이가 경로 인자에 개행을 붙여 넘기는 경로가 실제로 있는가(로그 인젝션·URL 디코딩) — 답할 사람: 포털 팀.
- 형식이 틀린 입력이 상류까지 간 횟수가 운영에서 얼마나 되는가 — 답할 사람: claims-core 팀.
