# 공유 계약

## 호출과 타입
requestId는 ASCII `[a-z0-9-]{1,32}` 문자열이다. values는 길이 1..8의 정수 배열이고 값 범위는 intent와 같다.
boolean/null/누락/추가 필드/부동소수는 허용하지 않는다. 정규화·정렬 없이 배열을 비교한다. 합계 최대 8,000,000,000은
정확한 정수로 표현한다. 호출자는 인자 이름·타입·결과를 아래대로 사용하며 전달 JSON은 UTF-8 객체, 최대 4096 bytes다.
필드 순서는 무관하고 중복 키·유효하지 않은 JSON·초과 bytes는 invalid_input이며 상태를 바꾸지 않는다.

| 호출 | 허용 입력 | 결과·오류와 효과 |
|---|---|---|
| submit | `{requestId, values}` | 전제 readiness 확인 후 전체 입력 검증, ID 조회. 기존 값과 같으면 snapshot; 다르면 id_conflict. 없으면 queued/attempt 0 등록 커밋 뒤 snapshot |
| get | `{requestId}` | readiness와 ID 검증 후 snapshot, 없으면 not_found. 무변경 |
| compute (C→W) | `{requestId, attempt, values}` | C가 유효 attempt를 커밋한 후 한 번 전달. W는 순수 합계 계산. 동등 메시지 중복은 같은 total이며 외부 효과 없음 |
| result (W→C) | `{requestId, attempt, total}` | 현재 calculating의 같은 ID/attempt이고 total이 해당 저장 values의 정확 합계이면 합계와 publishing을 함께 커밋하고 ack. 불일치 attempt/상태는 stale_attempt, 잘못된 total은 invalid_result. 거절은 무변경 |

snapshot의 정확한 형태는 `{requestId, state, total}`이다. state는 네 값 중 하나, total은 queued/calculating이면 null,
publishing/published이면 확정 정수다. submit/get 성공은 `{ok:true,value:snapshot}`, 실패는 `{ok:false,error:code}`다.
result 성공은 `{ok:true}`, 실패는 같은 error 형태다. 오류 코드는 위 표와 `invalid_input`, `unavailable`이다.
C는 readiness가 false이면 모든 호출에서 unavailable을 먼저 반환한다. 그 후 입력 유효성, ID/attempt, 업무 판단 순이다.
attempt는 0 이상 안전한 정수이며 dispatch 직전에 1 증가한다. 안전 정수 최대값에 도달하면 새 dispatch를
차단하고 운영자에게 unavailable을 보고한다. 모듈이 임의 attempt나 새 ID를 만들지 않는다.

원장 행은 requestId(유일키), values(불변), state, attempt, total이며 R 발행 충돌은 별도 `publishError`에
`invariant_conflict`로 기록한다. 평상시는 null이다. 이 오류는 get 실패로 노출하지 않고 운영자 진단에서
해당 ID/오류를 제공한다. 사용자 get는 실제 publishing과 확정 total을 유지한다. 삭제/키 재사용은 없다.
원장 읽기/쓰기 실패는 서비스 readiness를 false로 만들고 현재 호출은 unavailable이다.
submit이 커밋됐는지 불명이어도 임의 보상 삭제하지 않고 재시작 복구 후 동일 ID로 조회하게 한다.

## 기존 R의 고정 계약
C만 `put({key:requestId,total})`을 호출한다. R은 key를 유일키로 원자적으로 저장하며 결과는
`{kind:"created",total}` 또는 동일 값이 이미 있으면 `{kind:"existing",total}`이다.
동일 키/다른 값이면 `{kind:"conflict",total:storedTotal}`로 원래 값을 보존한다. R 내부 실패는
`{kind:"unavailable"}`이거나 연결 유실이며, 둘 다 커밋 여부를 보장하지 않는다.
created/existing와 요청 합계가 같을 때만 C는 published로 커밋한다. 응답 손실·unavailable은 publishing을 유지한다.
R 응답 형식이 잘못됐거나 합계가 어긋나면 해당 작업을 invariant_conflict로 중단한다.
R은 영속 결과를 재시작에도 보존한다. R의 디스크 손실·idempotency 규칙 변경은 이번 제품의 지원 계약 밖이다.
