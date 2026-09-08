---
id: 0002-claims-status
kind: plan
status: draft
upstream: spec.md@cf07fa4281c6f78efcc8a8eb3f87f3bce230bb75
---
# Plan: 청구 상태 조회 엔드포인트 (from intent 0002)

## Files that change
- src/claims_status/__init__.py
- src/claims_status/records.py
- src/claims_status/response.py
- src/claims_status/routes.py
- tests/test_claims_status.py
- scripts/gates/40-skills.sh

## Order of work
1. `tests/test_claims_status.py` 를 먼저 쓰고 **red 를 실측**한다. 이 시점에
   `src/claims_status/` 는 없으므로 임포트 자체가 실패해야 한다 — 「시험이 있다」가
   아니라 「시험이 지금 빨갛다」가 증거다.
2. `records.py` — 상류 레코드와 TTL 캐시. 상류 호출 수를 셀 수 있게 만든다
   (AC3 은 호출 수로 판정하므로 계기가 먼저 있어야 한다).
3. `response.py` — `RESPONSE_FIELDS` 와 `build_response()`. 백스톱이 요구하는
   정규 형태(허용 목록 컴프리헨션 하나 · 그 뒤 넓히는 문장 없음)로 쓴다.
4. `routes.py` — 라우트 등록과 핸들러. 레코드가 통로 말고 다른 곳으로 가지 않는다.
5. `__init__.py` — 패키지 표시만. 여기에 로직을 두지 않는다(임포트 부작용 금지).
6. 시험이 green 인 것과 `bash scripts/check_endpoints.sh src` 가 rc=0 인 것을 각각
   원문으로 확인한다.
7. `scripts/gates/40-skills.sh` 에 백스톱을 실코드에 겨누는 줄을 더한다. 이 줄이
   없으면 백스톱은 픽스처만 재고 실코드는 아무도 안 잰다.

## Risks
- TTL 시험이 실시간을 쓰면 느리고 흔들린다 → 시각을 인자로 주입해 `now` 를 시험이
  통제한다. 잠자기(sleep)로 재는 시험은 쓰지 않는다.
- 허용 목록 시험이 구현에서 `RESPONSE_FIELDS` 를 임포트하면 동어반복이 된다
  (구현이 넓어지면 시험도 같이 넓어져 영원히 green). 시험 파일에 네 이름을 독립적으로
  다시 적고, 그것이 진짜 독립인지 뮤테이션으로 실증한다.
- 캐시는 거르기 전 레코드를 들고 있다(C4). 캐시를 꺼내 보는 진단용 함수를 나중에
  누가 추가하면 통로를 우회하는 출구가 생긴다 → 백스톱의 R8(레코드 흐름)이 그 커밋을
  빨갛게 만든다. 지금 막는 것이 아니라 그때 울게 만들어 둔다.
- Q1(위임 조회)이 아직 열려 있다 — 위임 권한 모델이 정해지면 허용 필드와 인증
  경로가 둘 다 바뀔 수 있다. 그래서 둘 다 한 곳에만 둔다.

## Proof
- AC1 ← test_ac1_authenticated_session_returns_the_four_allowed_fields
- AC1 ← test_ac1_missing_session_returns_unauthenticated_and_no_claim_values
- AC2 ← test_ac2_new_upstream_field_does_not_widen_the_response
- AC2 ← test_ac2_response_keys_match_independently_written_allowlist
- AC3 ← test_ac3_second_lookup_within_ttl_does_not_call_upstream_again
- AC3 ← test_ac3_lookup_after_ttl_expiry_calls_upstream_again
- AC4 ← 게이트 「엔드포인트 백스톱(src)」 = bash scripts/check_endpoints.sh src

## Options not taken
- **응답(직렬화 결과)을 캐시한다** — PII 가 캐시에 남지 않아 C1 에는 더 좋다. 버린
  이유: 핸들러가 캐시된 문자열을 그대로 반환하게 되고, 그러면 「핸들러는 통로를 거쳐
  반환한다」는 계약이 깨진다. 통로를 우회하는 반환 경로를 하나 만들어 두면 다음 사람이
  그 자리에 다른 것을 넣는다. 캐시를 상류 접근 계층에 두고 통로를 하나로 지키는 쪽을
  택했다(C4 로 등재).
- **claims-core 에 웹훅을 붙여 상태 변경 시 캐시를 무효화한다** — F1(최대 60초 지연)이
  사라진다. 버린 이유: 상류 팀의 변경이 필요하고, 이번 intent 의 영향 범위(상류는
  읽기 전용)를 넘는다. Out of scope 에 적었다.
- **조회 결과에 amount_krw 를 넣는다** — 상담사가 전화로 함께 읽어 주는 값이라 자연스러워
  보인다. 버린 이유: intent 의 Problem 이 세는 것은 상태 · 다음 단계 · 예정일 셋뿐이고,
  C1 은 「지금 세션이 들고 있지 않은 값」을 넣지 말라고 한다. 필요하면 허용 목록에
  이름을 더하는 커밋으로 하면 된다 — 그 커밋이 곧 결정의 기록이다.

## Parallelisable
없음 — 파일 여섯 개가 한 사슬이고 총 200줄 남짓이다. 나누면 통로·허용 목록·등록처의
「하나여야 한다」를 두 사람이 각각 만들어 둘이 되는 위험이 나눠서 얻는 것보다 크다.
