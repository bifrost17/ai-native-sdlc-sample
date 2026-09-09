# Intent: 방금 접수된 청구가 포털에서 최대 60초 동안 「없는 건」으로 보인다
Author: detect_bands (automatic, 2026-09-09T12:16:23+09:00) · triaged by 서비스 오너(청구 상태 API). Status: draft.
## Problem
- 검출: 청구 상태 API 의 `not_found` 응답 비율(일 1점, 0~1)이 2026-09-02 에 0.310 — 기준선 20일 mean 0.101 · σ 0.004611, z=+45.32,
  규칙 `rule1_one_point_beyond_3sigma`, tier `3sigma`(action `propose`). 표본 `tests/data/bands/claims-status-not-found-spike.jsonl`,
  양성 대조 `normal.jsonl` 은 tier none. 검출기 출력의 지표 이름은 설정의 `ci_test_failure_rate` 였다 — 이 표본은 그 지표가 아니라
  청구 상태 API 의 not_found 비율이다(ops/bands.yaml 에 지표가 하나뿐이라 이름을 사람이 바로잡았다).
- 트리아지(코드에서 재현): 어떤 청구 번호를 원장에 없을 때 한 번 조회하면 그 「없음」이 60초 캐시된다. 그 사이 원장에 그 건이
  생겨도 같은 고객의 재조회는 `not_found` 다(t=0 없음 → 원장 등록 → t=30·t=59 `not_found`, 상류 호출 1 → t=61 에야 네 필드).
  자리: `src/claims_status/records.py` `fetch_claim` — `record` 가 `None` 이어도 `_CACHE[claim_id] = (now + 60, None)`.
- 접수 직후 상태를 확인하는 고객이 많을수록 not_found 비율이 오른다. 표본이 그 이유로 튀었다는 것은 이 코드 경로가 재현된다는
  뜻이지 그날 접수량을 센 것은 아니다(로그 확인 못 함).
## Proposed outcome
원장에 생긴 청구 건은 그 즉시(다음 조회부터) 네 필드로 보인다 — 「없음」 응답을 받은 뒤 원장에 건이 생기면 다음 조회가
`not_found` 가 아니다. 검수: 위 재현 순서에서 t=30 조회가 네 필드를 돌려주면 된다. 그 뒤 not_found 비율이 기준선으로 돌아오는지 검출기로 다시 본다.
## Affected users and systems
사람: 청구를 막 접수한 고객(포털에서 「없는 건」을 본다), 그 전화를 받는 콜센터 상담사, 우리 서비스 오너(검수). 시스템: 청구 상태 API
`src/claims_status/records.py` 의 캐시, 상류 claims-core(호출 수가 바뀔 수 있다).
## Constraints
- C1 Status 는 draft — 이 PR 의 머지가 승인이다. 하류(spec·plan)는 엔지니어 지시로 draft 위에 착수한다(design-spec 「one exception」).
- C2 0002 의 나머지 계약은 그대로다: 있는 건의 TTL 60초 캐시(R5) · 허용 목록(R3) · 남의 건=없는 건 같은 문구(R4) · 기존 인증만(R2).
- C3 범위 밖: claims-core 쪽 변경, 상담사 화면, 알림, 캐시 무효화 통지.
## Open questions
- Q1 「없는 번호」 반복 조회로 상류 예산(초당 50건)이 새는 것을 미스 캐시가 막고 있었다 — 그 보호를 어떻게 대체하는가? — 답할 사람: claims-core 팀, 보안팀.
- Q2 09-02 의 실제 접수량·조회 로그가 이 경로를 뒷받침하는가(로그는 이 레포에 없다)? — 답할 사람: 포털 운영팀.
## Triage
Fix now — 재현되는 코드 경로가 있고, intent 0002 의 Proposed outcome(「내 청구 건을 열면 세 값이 보인다」)을 직접 깨뜨린다. 밴드 조정 없음.
