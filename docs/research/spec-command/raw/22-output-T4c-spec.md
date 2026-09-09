Upstream: intent.md@a5dfb88. Status: draft.

# Spec: 청구 상태 변경 고객 통지

## Skills applied
- brand@0c29619
- compliance@0c29619
- ux@0c29619
- secure-api-review@0c29619

## Requirements
1. 사정인이 claims-core 에서 청구 상태를 바꾸면, 그 변경이 저장된 시점부터 24시간 이내에 고객에게 통지(문자 또는 앱 푸시)가 발송된다.
2. 통지는 앱 설치 여부로 채널을 정한다: 앱 설치·로그인 이력이 있는 고객은 푸시, 없는 고객은 SMS. 두 채널 모두 실패하면 재시도하지 않고 실패를 기록한다(콜센터가 대신 안내할 근거를 남기기 위함).
3. 통지에는 청구 상태(브랜드 정책 B4 다섯 어휘 중 하나)와 포털의 해당 청구 화면으로 가는 링크가 들어간다. 링크를 통해 들어가면 기존 포털 SSO 로그인 화면을 거치고, 로그인 후 해당 청구로 바로 이동한다(로그인 없이 청구 내용 노출 금지 — intent 제약).
4. 통지 발송·실패 이력은 청구 번호, 채널, 발송 시각(UTC), 성공/실패를 기록하고 3년 보존한다(compliance C6).
5. 통지는 SMS 수신 동의가 기록된 고객에게만 SMS로, 푸시 동의(앱 알림 권한)가 확인된 고객에게만 푸시로 보낸다. 동의 상태를 확인할 수 없으면 발송하지 않고 실패로 기록한다(compliance C4).
6. 상태 변경 이벤트를 소비하는 API(notify-gw 가 claims-core 로부터 받는 웹훅/이벤트)는 게이트웨이 JWT 로 인증하고, 요청 스키마 외 필드는 거부하며, 상태 변경마다 actor(사정인 ID)·action·entity(청구 번호)·timestamp 로 audit 이벤트를 남긴다(secure-api-review 1–3).

## Design
- **트리거**: claims-core 가 상태 변경 시 이벤트를 발행 → notify-gw 가 소비 → 채널 결정(푸시 우선, 없으면 SMS) → 발송.
- **링크**: 포털 도메인의 딥링크(예: `portal.example.com/c/<claim-id>`)를 그대로 쓴다. 단축 URL(외부 서비스)은 쓰지 않는다 — 아래 "단축 URL" 플래그 참조.
- **문구**: SMS/푸시 본문은 브랜드 정책(B1–B7)과 컴플라이언스 정책(C5)을 따른다. 본문에는 상태와 문의 경로만 담고, 사유 상세·금액 산정 근거는 넣지 않는다. 청구 번호를 문자 본문에 넣을지는 아래 "청구 번호 노출" 플래그 참조.
- **야간 발송**: 22:00–08:00 KST 도착 건은 기본적으로 08:00 이후로 지연 발송한다 — 아래 "야간 발송" 플래그 참조. 사정인 팀 요청대로 즉시 발송하는 옵션은 고객경험팀장 결정 이후 별도 반영.
- **재조회/대리조회**: 상담사가 고객 대신 통지 이력을 조회할 때는 본인확인 기록 ID 를 함께 남긴다(compliance C7).
- **감사/로그**: 발송 파이프라인의 로그·오류 메시지에는 청구 번호·내부 ID 만 쓰고 전화번호·주민번호 등 PII 는 넣지 않는다(compliance C1, C3).

## Constraints (carried over from intent, plus discovered here)
- 기존 포털 SSO 만 사용, 통지 링크는 로그인 없이 청구 내용을 보여주지 않는다. (intent)
- 새 PII 수집 없음 — 전화번호는 claims-core 기존 값만 사용. (intent)
- 통지 문구는 브랜드·컴플라이언스 정책을 따른다. (intent, brand B1–B7, compliance C5)
- SMS 링크는 90자 제한 안에 들어가야 한다. (intent)
- 통지·조회 이력은 3년 보존, who/what/when 기록. (compliance C6 — spec 에서 추가)
- SMS/푸시는 각각 기록된 수신 동의가 있을 때만 발송. (compliance C4 — spec 에서 추가)
- 상태 변경 이벤트 API 는 게이트웨이 JWT 인증 + 스키마 외 필드 거부 + audit 이벤트. (secure-api-review — spec 에서 추가)

## Open questions from intent
- **앱 미설치 고객에게 문자를 보낼 때 청구 번호를 문자 본문에 넣어도 되는가 — 컴플라이언스 오너.**
  carried forward (컴플라이언스 오너). compliance C1 은 연락처·계좌·주민번호를 금지하지만 청구 번호를 명시적으로 금지하지 않아, C2(허용 목록 근거 필요)에 따라 오너 판단이 필요하다. 판단 전까지는 청구 번호를 넣지 않고 "고객님의 청구"로만 표기하는 쪽을 기본값으로 한다.
- **단축 URL 서비스(외부)로 청구 화면 링크를 보내도 되는가 — 보안 오너.**
  carried forward (보안 오너). 이 spec 은 기본값으로 포털 도메인 링크(단축 URL 미사용)를 채택했다. 90자 제한과 부딪히면(도메인+청구 ID 조합이 90자를 넘는 경우) 보안 오너 승인 후 단축 URL 도입을 재검토한다.
- **야간 발송을 허용할 것인가 — 고객경험팀장.**
  carried forward (고객경험팀장). 이 spec 은 기본값으로 야간 지연 발송(08:00 이후)을 채택했다. 사정인 팀의 즉시 발송 요청은 팀장 결정 후 반영.

## Flagged concerns
- **야간 즉시 발송 vs UX/컴플라이언스**: 사정인 팀은 22:00–08:00 에도 즉시 발송을 요청하지만, UX 정책에 야간 발송을 금지하는 조항은 없으나 고객 경험상 심야 알림은 일반적으로 지양된다. 컴플라이언스 정책도 발송 시각을 제한하지 않는다. 즉, 정책 간 충돌은 없으나 intent 의 열린 질문(고객경험팀장 결정)과 사정인 팀 요청이 서로 다른 결론을 요구한다 — 고객경험팀장이 결정.
- **청구 번호를 SMS 본문에 노출 vs compliance C1/C2**: 위 열린 질문과 동일 — 컴플라이언스 오너 결정 전까지 미노출을 기본값으로 한다.
- **단축 URL vs compliance C1 (링크에 PII 없음) 및 보안**: 단축 URL 서비스는 외부 3rd-party 이므로 청구 ID 가 그 서비스 로그에 남을 수 있어 compliance C1/C3 취지와 부딪힐 수 있다 — 보안 오너 결정 전까지 미사용.

## Traceability
- 24시간 내 통지, "내 청구 어떻게 됐나요" 콜 감소 목표(intent Proposed outcome) → Requirement 1, 2, 3.
- 로그인 없이 청구 노출 금지(intent Constraints) → Requirement 3.
- 새 PII 수집 없음(intent Constraints) → Design(문구), Constraints.
- SMS 90자 제한(intent Constraints) → Design(링크), Open questions(단축 URL).
- 야간 즉시 발송 요청(intent Constraints) → Design(야간 발송), Open questions, Flagged concerns.
