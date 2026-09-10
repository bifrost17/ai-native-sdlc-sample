# PROVENANCE — claim-notice-compliance

**설계분이다.** 기존 스킬을 옮긴 것이 아니라 이 레인에서 썼다. 채택한 원문이 없으므로 「수정 여부」는 해당 없음.

- **정본**: `policies/compliance.md` v0 (Status: draft — 오너 서명 대기). 덮는 조항 **C4 · C5**.
- **전사**: 본문의 `> **C4**` · `> **C5**` 인용 블록은 정본에서 **축자로** 옮긴 것이다.
  `policies/compliance.md` 와 바이트 단위로 일치함을 확인했다(2/2 일치).
- **조사·판정**: `docs/research/compliance/candidates.md`, `coverage.md`, `trigger-tests.md`(로드 3/3 + 집합 1회).
- **라이선스**: 이 레포의 것. 외부 스킬의 문장을 복사하지 않았다.

## 참고한 것 (착상만 · 문장 복사 없음)
동의·통지 축의 후보 6건은 **전부 기각 또는 보류**다. 이 축은 후보 품질이 가장 나빴다 —
공개 스킬 생태계의 이메일/SMS 스킬은 거의 **마케팅** 스킬이고, 우리 통지는 거래성이라 결론이 반대로 난다.

| 참고한 것 | 판(sha) · 라이선스 | 무엇을 가져왔나 | 왜 그대로 쓰지 않았나 |
|---|---|---|---|
| chunkydotdev/email-skills `notification-design` | 5717a78 · MIT | **C5 의 예시 어법** — `Never include sensitive data in the email body - say "your payment was processed" not "your payment of $4,231.00 was processed."` 가 C5 의 「금액 산정 근거 금지」와 정확히 같은 자리를 짚는다. **인용 출처로만** 남긴다 | 같은 문서가 `Clear numbers. "You've used 8,500 of your 10,000…"` 와 미리보기 문구를 권해 스스로를 반박한다. 모든 메일에 unsubscribe·선호센터를 요구하고, 빈도 캡(`max 5/day … overflow goes to digest`)과 무반응 고객 발송 중단이 **의무 통지를 지연·누락**시킨다 |
| chunkydotdev/email-skills `email-compliance` | 57d751b · MIT | **거래성 / 영업성 분리** — 서비스 메시지에 영업성 내용을 섞지 말라는 규칙(C5 의 절반) | 핵심 결론이 우리와 반대다: `covered by the **contractual necessity** basis - no separate consent needed`. 청구 통지가 정확히 그 범주라 「동의 확인 불필요, 보내라」로 결론난다 — **C4 가 막으려는 바로 그 실패**. 30일 내 삭제 절차는 C6 3년과 충돌 |
| mukul975 `consent-record-keeping` | 08870b9 · Apache-2.0 | **동의 기록을 채널·목적별로 두고 발송 시점의 상태를 조회한다**는 골격(C4 를 구현할 때의 스키마 참고) | `ip_address`·`user_agent`·`session_id` 를 기록에 권해 C3 을 깬다. `controller_name … DEFAULT 'CloudVault SaaS Inc.'` 가 가상 회사명을 DB 디폴트로 박는다. C4 의 핵심인 「확인 불가 → 발송 금지」가 없다 |
| davila7/claude-code-templates `Data Privacy Compliance` | cd804d3 · MIT | **deny-by-default 게이트의 꼴** — 허용된 목적이 아니면 예외를 던져 막는다. C4 의 「확인 못 하면 보내지 않는다」와 구조가 같다 | 보존 수치(2년 · 7년 · 26개월)가 C6 의 3년을 덮어쓰고, 동의 레코드에 IP/UA 저장을 권한다. 614줄 중 유효한 건 30~40줄 |
| mukul975 `double-opt-in-email` · coreyhaines31 `sms` | 6102f4f · 50cfa8d | **반면교사** — 이 둘이 보여 준 오발이 이 스킬의 「마케팅 관행을 가져오지 않는다」 문단을 쓰게 했다 | 구독 동의(DOI)로 게이팅하면 확인 안 한 청구인에게 통지가 영영 안 나간다. STOP 푸터·이름 토큰 개인화·quiet hours 는 청구 통지를 오염시키거나 지연시킨다. `sms` 는 `Generally OK without separate marketing consent if directly related to a transaction` 로 C4 를 정면으로 거스른다 |

**기각한 후보들이 이 스킬의 내용을 만들었다.** 본문의 「거래성 통지다 — 마케팅 메시지가 아니다」 문단과
「일단 보내고 나중에 정리·거래성이니 동의 없이 보내도 된다로 빠지지 않는다」는, 후보 4종이 실제로
그 방향을 가르치는 것을 읽고 막으려고 쓴 것이다. 집합 시험에서 이 문장이 작동했다(`trigger-tests.md` 12번).

## 경계
- **C6(통지 이력)은 여기서 다시 쓰지 않는다** — 문면은 `claim-data-compliance` 에 있고 이 스킬은 가리키기만 한다.
  3년·UTC·역할+ID 를 두 곳에 적으면 개정 때 한쪽만 고쳐져 갈라진다.
- **C1 은 통지에도 걸린다**는 사실만 적고 규칙은 C1 조항으로 넘긴다.
- 트리거 문장은 자리를 겨냥했다(`docs/work/NOTES.md` 3번) — 통지 설계 · 고객 문구 작성 · 채널 선택 · spec 기재.

## 고칠 때
정책이 바뀌면 정본을 먼저 고치고, 그다음 이 스킬을 고쳐 오너 서명을 받는다
(L6: "When the policy changes, change the skill and have the policy owner sign off on the change").
인용 블록을 고칠 때는 정본과의 축자 일치를 다시 확인한다.
