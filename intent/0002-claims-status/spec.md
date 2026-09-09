# Spec: 청구 상태 조회 API (from intent 0002-claims-status)
Upstream: intent.md@d9d55ff90ed1d6407c9304fdc5a3e00e66faf07c. Status: draft.
Skills applied: secure-api-review (항목별 점검은 Design 끝에), design-spec.
Note: intent 는 아직 draft(PR #17 미머지)다. 엔지니어(부모 세션)가 2026-09-09 착수를 지시해 스킬의 「accepted 가 아니면 쓰지 않는다」를 지시로 넘긴다 — 다인 조직이면 PR #17 머지를 기다렸을 자리다.
## Requirements
- R1 포털 세션이 있고 그 세션의 고객이 낸 청구 건이면 `claim_id`·`status`·`next_step`·`due_date` 가 돌아온다 (Problem: 상담사가 읽어 주는 세 값).
- R2 세션이 없으면 `unauthenticated` 만 돌아오고 상류 조회도 일어나지 않는다 (Constraints: 기존 인증만).
- R3 응답에 나가는 필드는 허용 목록 한 곳이 정한다. 원장에 있는 다른 값(주민번호·계좌·내부 메모)은 응답·오류 문구 어디에도 실리지 않고, 원장에 새 필드가 생겨도 응답은 넓어지지 않는다 (Constraints: 새 개인정보 없음).
- R4 남의 청구 건과 없는 청구 건은 같은 `not_found` 로 답한다 — 구분하면 청구 번호의 존재 여부가 샌다 (Proposed outcome: 남의 번호는 아무것도 안 보인다).
- R5 같은 청구 건을 TTL(60초) 안에 다시 조회하면 상류 claims-core 를 다시 부르지 않고, TTL 이 지나면 다시 부른다 (Constraints: 초당 50건).
## Design
표준 라이브러리만으로 `src/claims_status/` 세 모듈. 기준은 「하나여야 하는 것」을 한 파일에 두는 것.
- `records.py` — 상류 접근 + TTL 캐시(`fetch_claim(claim_id, now)`). 원장 레코드를 거르지 않고 돌려주며, 캐시는 프로세스 메모리 밖으로 나가지 않는다. 시각은 인자로 주입(시험이 시간을 통제한다). 없는 건도 캐시한다(없는 번호 반복 조회로 상류 예산을 태우지 못하게).
- `response.py` — 허용 목록 `RESPONSE_FIELDS` 와 `build_response()` 하나. 응답 JSON 은 여기서만 만든다.
- `routes.py` — `get_claim_status(claim_id, session, now=None)`. 세션 없음 → `{"error":"unauthenticated"}` · 청구 번호 형식 불일치 → `{"error":"invalid_claim_id"}`(입력을 되비추지 않는다) · 없는 건/남의 건 → `{"error":"not_found"}` · 정상 → 허용 목록 네 필드. 소유 판정은 원장 레코드의 `subscriber_id` 와 세션의 `subscriber_id` 일치.
secure-api-review 점검: ① 인증 — 익명 경로 없음, 핸들러는 포털 세션 없이는 아무 값도 내지 않는다(게이트웨이 JWT 는 포털이 세션으로 바꿔 넘긴다는 전제 — 새 토큰을 만들지 않는다). ② 입력 검증 — GET 이라 본문 없음, 경로 인자 `claim_id` 는 `C-<숫자>` 형식만 받는다. ③ 감사 — 상태를 바꾸는 엔드포인트가 아니므로 감사 이벤트 없음(읽기 전용). ④ 데이터 분류 — pii(주민번호·계좌·내부 메모·이름)는 응답·오류 문구·로그에 없다; 이 모듈은 로그를 남기지 않는다.
## Constraints
- intent: 포털 세션에 새 개인정보를 넣지 않는다 · 기존 인증만 · claims-core 초당 50건 · 범위 밖(접수·수정·알림·상담사 화면).
- 발견: 캐시는 거르기 전 원장 레코드를 들고 있다 — 그래서 캐시는 `records.py` 밖으로 꺼내 보이지 않는다(진단 함수·로그 금지).
- 발견: 응답 조립을 한 함수로 모은다 — 허용 목록을 넓히는 것은 커밋(결정)이지 구현이 아니다.
## Open questions from intent
- 제3자 손해사정인 접근 → carried forward: 위임 관계의 정본이 정해지기 전에는 권한 모델을 만들지 않는다; 이번 설계는 위임 경로를 「없음」으로 둔다 (클레임 운영팀장·법무 개인정보 담당).
- 예상 완료일이 원장 값인가 계산 값인가 → answered: 이 설계는 원장의 `due_date` 를 그대로 보여 주고 계산하지 않는다; claims-core 팀이 「계산해야 한다」고 답하면 spec 변경이다.
- 초당 50건 수치·조회 결과 보관 가부 → carried forward: 수치는 claims-core 팀; TTL 캐시가 원장 레코드를 60초 메모리에 두는 것의 가부는 보안팀. 답이 「안 된다」면 R5 의 장치를 바꿔야 하고 그때까지 켜지 않는다.
## Flagged concerns
- F1 TTL 60초 동안 옛 상태가 보인다 — 「지급완료」 직후 최대 60초는 「심사중」. 60초가 맞는지: 클레임 운영팀장.
- F2 남의 건과 없는 건을 같은 문구로 합쳤다(R4) — 오타 낸 고객도 같은 문구를 본다. 문구를 나누면 정책 변경: 법무 개인정보 담당.
- F3 secure-api-review 는 「게이트웨이 JWT」를 말하고 intent 는 「기존 포털 인증」을 말한다. 둘이 같은 것인지(포털이 JWT 를 세션으로 바꾸는지) 포털 팀이 답한다; 이 spec 은 세션 객체만 본다.
## Out of scope
상담사 대리 조회 · 손해사정인 위임 조회 · 청구 접수와 수정 · 알림 · 포털 프론트엔드 화면 · claims-core 쪽 캐시 무효화 통지 · 실제 HTTP 서버·라우터 배선(핸들러 함수까지).
## Acceptance criteria
- AC1 → R1 세션(`subscriber_id` 일치)으로 조회하면 키 집합이 정확히 {claim_id, status, next_step, due_date} 이고 값이 비어 있지 않다.
- AC2 → R2 세션 `None` 이면 `{"error":"unauthenticated"}` 이고 상류 호출 수 0.
- AC3 → R3 원장 레코드에 새 민감 필드를 심어도 응답 키 집합이 같고, 주민번호·계좌·메모 문자열이 본문에 없다. 판정에 쓰는 키 집합은 구현에서 임포트하지 않고 시험이 따로 적은 것이다.
- AC4 → R4 남의 건과 없는 건의 응답이 바이트 단위로 같다(`{"error":"not_found"}`); 형식이 틀린 번호는 `invalid_claim_id` 이고 입력 문자열이 본문에 없다.
- AC5 → R5 같은 건을 now=0, now=59 로 조회하면 상류 호출 1, now=61 로 한 번 더 조회하면 2.
