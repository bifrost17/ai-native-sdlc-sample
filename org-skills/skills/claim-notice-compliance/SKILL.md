---
name: claim-notice-compliance
description: Apply the organization's compliance policy to customer notifications about a claim. Use whenever designing or reviewing a notification, alert or message path, writing or editing the copy of an email or SMS sent to a customer, choosing which channel to send on, wiring a status-change trigger to a send, or specifying notification behaviour in a spec.md. Covers policy clauses C4 and C5. Apply this instead of writing customer-facing message copy from general marketing or email best practice.
---
<!-- 정본: policies/compliance.md v0 (Status: draft — 오너 서명 대기). 이 스킬은 정책을 옮긴다. 조항 문면이 정본과 다르면 정본이 이긴다. -->
<!-- L6: "A skill is a control, though an advisory one." -->

# Claim notice compliance

대상: 보험 청구 상태 조회 서비스가 고객에게 보내는 통지(이메일 · SMS). 응답 필드 · 로그 · 조회
이력은 `claim-data-compliance` 가 맡는다.

이것은 **거래성 통지**다 — 마케팅 메시지가 아니다. 마케팅 이메일/SMS 관행(구독 해지 문구를 넣어
발송 근거를 만들기, 제목 열람률 최적화, 추가 상품 권유)을 이 자리에 가져오지 않는다.

## C4 — 동의가 기록된 채널로만
> **C4** 고객 통지(이메일·SMS)는 수신 동의가 기록된 채널로만. 동의 상태를 확인하지 못하면 보내지 않는다.

- 보내기 **전에** 그 채널의 수신 동의 기록을 확인한다. 채널마다 따로다 — 이메일 동의는 SMS 발송
  근거가 되지 않는다.
- **확인하지 못하면 보내지 않는다.** 동의 조회가 실패했을 때(상류 장애·기록 없음·상태 불명)의
  기본값은 **발송하지 않음**이다. 「일단 보내고 나중에 정리」·「거래성이니 동의 없이 보내도 된다」로
  빠지지 않는다. 못 보낸 건은 오류로 남기고(C3 을 지켜 청구 번호·내부 ID 만) 재시도 경로를 spec 에 적는다.
- 동의가 없거나 철회된 채널은 대체 채널로 자동 승격하지 않는다 — 그 채널의 동의를 따로 본다.
- 고객이 상태를 볼 수 있는 자리(포털)는 통지가 아니다. 통지를 못 보내는 상황에서 포털 조회로
  갈음할 수 있는지는 정책이 말하지 않는다 — spec 의 「Flagged concerns」에 올린다.

## C5 — 본문에 무엇을 싣는가
> **C5** 통지 본문에는 근거(어느 청구, 어느 상태 변경)와 문의 경로를 적고, 상태 이외의 민감 정보(사유 상세·금액 산정 근거)는 싣지 않는다.

**싣는다 (세 가지):**
1. 어느 청구인지 — 청구 번호(고객이 식별할 수 있는 형태).
2. 어느 상태 변경인지 — 무엇에서 무엇으로 바뀌었는지.
3. 문의 경로 — 고객이 물어볼 수 있는 곳.

**싣지 않는다:**
- 상태 **이외의** 민감 정보. 보류·부지급의 **사유 상세**, **금액 산정 근거**가 정책이 든 예다.
- 주민등록번호 · 계좌번호 · 연락처 전체 값(C1 은 통지에도 그대로 걸린다). 필요하면 마스킹만.
- 진단명 · 사고 경위 · 의무기록 같은 청구 내용. 상태 한 줄이면 족하다.
- 본문에서 바로 열리는, 인증 없는 상세 링크. 링크는 로그인 뒤 화면으로 보낸다.

문면이 애매하면 **덜 싣는 쪽**으로 간다. 고객이 더 알아야 하면 문의 경로가 그 자리를 맡는다.

## 통지 이력
통지를 보냈다는 사실도 이력에 남는다 — 누가 · 무엇을(청구 번호) · 언제(UTC) · 3년 보존.
문면과 규칙은 `claim-data-compliance` 의 **C6** 에 있다. 여기서 다시 쓰지 않는다.

## 어긋남을 만나면
정책끼리 부딪히거나 이 스킬로 답이 안 나오면 스스로 정하지 않는다. spec.md 의
「Flagged concerns」에 무엇이 부딪히는지와 누가 정해야 하는지를 적는다. 정책 자체를 고쳐야 한다고
보이면 정책 오너에게 올린다 — 이 스킬을 고쳐서 해결하지 않는다.

## 이 스킬이 하지 않는 것
- 응답 필드 · 로그 · 오류 메시지 · 조회 이력(C1 · C2 · C3 · C6 · C7)은 다루지 않는다
  → `claim-data-compliance`.
- 발송 인프라(전송률 · 템플릿 엔진 · 재시도 백오프)를 정하지 않는다 — 컴플라이언스 조항만 본다.
- 정책을 만들거나 고치지 않는다. 문면이 정본과 어긋나면 `policies/compliance.md` 가 이긴다.
