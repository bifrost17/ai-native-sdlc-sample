# Spec: 사내 집계 발행
Upstream: [intent.md](intent.md), 같은 고정 입력판. Status: draft.

## Requirements
- R1: `submit(requestId, values)`는 정해진 입력을 검증하고 내구성 원장에 요청을 한 번 등록한다.
- R2: 동일 ID/동일 값은 현재 상태를 돌려주고 다른 값이면 거절한다. 정수 순서도 입력의 일부다.
- R3: W가 합계를 계산하고 C가 결과를 확정한 뒤 기존 R에 정확히 같은 발행키/결과를 전달한다.
- R4: C·W·R의 독립 재시작에서 미완료 상태를 복구하고 늦은 작업자 응답·발행 응답 손실을 처리한다.
- R5: `get(requestId)`는 queued, calculating, publishing, published 중 현재 상태와 확정된 합계만 알려준다.

## Acceptance criteria
| ID | 입력·사건 | 기대 |
|---|---|---|
| AC1 | 새 ID a, 값 [2,0,3] | 최초 queued, 계산 결과 5를 확정한 뒤 R에 key a로 발행, published 조회는 total 5 |
| AC2 | a/[2,0,3]을 다시 제출 | 현재 상태 반환; 새 행·재계산·추가 발행 없음 |
| AC3 | a/[3,0,2] 제출 | id_conflict, 원래 행·결과 보존 |
| AC4 | 빈 값 목록, 범위 밖 정수, 부동소수, ID 공백 | invalid_input, 기존 ID 조회보다 입력 검증이 먼저이며 무변경 |
| AC5 | 원장 커밋 후 submit 응답 손실 | 재시도는 같은 원장 행을 조회, 이중 작업 생성 없음 |
| AC6 | W만 계산 중 종료, C/R 생존 | C가 해당 W의 실제 종료를 확인하고 attempt를 바꿔 queued로 재계산. 늦은 옛 결과는 stale_attempt |
| AC7 | C만 종료, W/R 생존 | 새 C는 이전 C 종료·원장 단독 잠금·옛 W 종료를 확인 후 계산 중 작업만 새 attempt로 재개. 확정된 합계는 재계산하지 않음 |
| AC8 | R만 종료·복구, C/W 생존 | publishing 유지. 같은 키·합계로 재시도해 한 결과만 발행. W를 다시 실행하지 않음 |
| AC9 | R 발행 커밋 후 응답 손실 또는 그 직후 C 종료 | 같은 키/합계의 재시도 결과로 발행 확인; 새 키나 새 합계로 대체하지 않음 |
| AC10 | C 기동 중 이전 W 종료를 확인할 수 없거나 원장 잠금 실패 | readiness false, submit/get는 unavailable, 결과 수락·새 작업·새 발행을 하지 않음. 운영자가 종료/잠금 문제를 해소하면 정해진 재기동 절차로 복구 |
| AC11 | R이 같은 키/다른 합계를 반환 | invariant_conflict로 해당 작업 발행 중단, publishing 상태·확정 합계 보존, 운영자에 오류 노출. 다른 작업은 계속 |

## Design
C는 요청 identity·원장의 단독 소유자이며 W에는 attempt별 순수 계산만 맡긴다. W가 직접 R에 발행하는
대안은 오래된 W를 차단하기 어렵고, 매 재시도 새 ID를 쓰는 대안은 중복 발행을 일으켜 채택하지 않았다.
R은 기존의 키 기반 멱등 발행을 제공한다. at-least-once 발행 호출과 요청당 한 저장 결과를 구분한다.

정본은 [contracts.md](contracts.md)의 입력·반환·원장/발행 계약과 [recovery.md](recovery.md)의
작업 수명·효과 순서·독립 장애 복구다. 모두 같은 판으로 읽는다. 영속 갱신은 C의 단일 원장 트랜잭션이다.
`queued → calculating → publishing → published`가 정상 흐름이다. 계산 단계로 돌아갈 수 있는 조건은 recovery가 정한다.
설계는 문장·표로 필요한 경계를 표현했다. 실제 코드·plan·시험 실행은 아직 작성하지 않았다.

## Constraints and scope
신뢰된 사내 호출자 범위만 다루며 HTTP 라우트·외부 API·인증을 새로 만들지 않는다. 메서드는 같은
배포 패키지의 typed service interface이고 프로세스 간 전달은 고정된 길이 제한 JSON 메시지를 사용한다.
영속 매체 손실·R의 계약 위반·계산 취소·작업 이력 삭제·사용자별 접근 제어는 지원 범위 밖이다.

## Open questions
- 내부 클래스·파일 분해와 원장 라이브러리는 plan에서 정한다. 원자 커밋·프로세스 간 단독 잠금과 재시작 내구성은 필수 제약이다.
- 배포 경로·실제 실행 UID·R 연결 주소는 배포 준비에서 담당 엔지니어가 정한다. W의 원장/R 접근 차단과 C 단독 writer 조건을 만족해야 한다.
- 실제 장애 시험·처리 성능은 구현 뒤 확인한다. 여기서는 설계 계약 충분성과 계획 인계 준비만 판단한다.

## Flagged concerns
원장/배포 구현이 위 제약을 만족하지 못하면 그 의존 구현 전에 설계를 재검토한다. 아직 성능·복구 실행을 통과했다고 주장하지 않는다.
