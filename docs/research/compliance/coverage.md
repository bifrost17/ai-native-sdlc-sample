# 정책 조항 × 스킬 — compliance (S3)

행 = `policies/compliance.md` 의 조항 ID. 열 = 스킬. 칸 = **덮음 · 부분 · —**.
조사 시각(UTC) 2026-09-09T09:32Z ~ 2026-09-10T00:05Z. 근거 인용은 `candidates.md`, 결론은 `README.md`.

## 채택·설계한 스킬

열 두 개는 이 레인이 **설계**한 것이다(채택 0건 — 이유는 `README.md`).
`secure-api-review` 는 템플릿에 이미 있는 스킬이고 S5 레인의 것이라 참고로만 둔다.

| 조항 | claim-data-compliance | claim-notice-compliance | secure-api-review (S5 영역, 참고) |
|---|---|---|---|
| **C1** 식별번호 전체 금지 · 마스킹만 | **덮음** | 부분(통지 본문에 한해 C1 을 다시 걸고, 규칙은 C1 조항으로 넘김) | — |
| **C2** 응답 필드 허용 목록 · 근거를 spec 에 | **덮음** | — | — |
| **C3** 로그·오류·audit 에 PII 금지 | **덮음** | — | **S5 영역** — 4항이 로그·오류를 덮는다(audit 이벤트는 제외) |
| **C4** 동의된 채널로만 · 확인 못 하면 미발송 | — | **덮음** | — |
| **C5** 통지 본문 = 근거 + 문의 경로, 그 외 민감정보 금지 | — | **덮음** | — |
| **C6** 조회·통지 이력 누가·무엇·언제(UTC) · 3년 | **덮음** | 부분(통지 이력도 남는다는 사실만 적고 문면은 C6 으로 넘김) | — (3항은 **상태 변경** 엔드포인트만 — 조회는 밖) |
| **C7** 대리 조회는 본인확인 기록 있을 때만 · 기록 ID 병기 | **덮음** | — | — |

**7개 조항 전부 「덮음」이 하나씩 있다. 빈 조항은 없다.** 조항 문면은 두 스킬 본문에 축자 전사돼 있고,
`policies/compliance.md` 와 바이트 단위로 일치하는지 기계로 확인했다(7/7 일치, `README.md` 「확인한 방법」).

## 겹침
- **C1 — 두 스킬이 함께 언급한다.** `claim-data-compliance` 가 규칙의 정본이고,
  `claim-notice-compliance` 는 "C1 은 통지에도 그대로 걸린다"만 적고 규칙을 다시 쓰지 않는다.
  통지가 C1 의 사정권("어떤 응답·화면·**통지**")에 명시돼 있어 통지 쪽에서 이 조항을 못 보고 지나칠
  위험이 실제로 있기 때문에 남겼다. 문면이 갈라질 여지는 두지 않았다.
- **C6 — 마찬가지.** `claim-notice-compliance` 는 「통지 이력」 절에서 "문면과 규칙은
  `claim-data-compliance` 의 C6 에 있다. 여기서 다시 쓰지 않는다"로 넘긴다. 3년·UTC·역할+ID 를
  두 곳에 적으면 개정 때 한쪽만 고쳐져 갈라진다.
- **C3 × `secure-api-review` 4항 — S5 영역과 겹친다.** 같은 자리(로그·오류 메시지의 PII)를 두 스킬이
  덮는다. `claim-data-compliance` 는 본문에 **「둘이 어긋나면 `secure-api-review` 가 정본」**이라고
  적어 우선순위를 고정했고, 자기가 더하는 것은 **대상이 audit 이벤트까지 넓다**는 한 가지뿐이라고
  밝혔다. 집합 충돌 시험(`trigger-tests.md` 12번)에서 두 스킬이 함께 적용됐고 어긋나지 않았다.
- **C6 × `secure-api-review` 3항 — 겹치는 것처럼 보이지만 겹치지 않는다.** 3항은 *상태를 바꾸는*
  엔드포인트의 audit 이벤트이고, C6 은 *조회*(상태를 바꾸지 않는 읽기) 이력이다. 집합 시험에서
  모델이 이 구분을 스스로 짚었다("이 chain 에는 상태를 바꾸는 엔드포인트가 없다 … 읽기 경로의
  이력은 C6 이 따로 요구하는 것"). 이 구분을 놓치면 조회 이력이 통째로 빈다.

## 모순
**설계한 두 스킬 사이에는 모순이 없다**(집합 시험 1회로 실증, `raw/13-set-test-spec-output.txt`).
아래는 **채택하지 않기로 한 이유가 된 모순**이다 — 외부 후보를 그대로 넣었을 때 정책과 부딪히는 것들.

| 모순 | 어디서 | 무엇과 부딪히나 |
|---|---|---|
| 보존 기간 숫자가 제각각 | `gdpr-compliant` 12–24개월/6개월 · `audit-logging` 6년 · `hipaa-compliance` 6년 · `gdpr-compliance` 1년 · `data-privacy-compliance` 2년/7년/26개월 | **C6 의 3년.** 18건 중 **3년을 말하는 파일은 하나도 없다.** 섞을수록 숫자가 흐려진다 |
| 삭제권·TTL 을 이력에까지 적용 | `gdpr-compliance` `Cascade to: logs (redact)` · `security-and-hardening` "모든 개인정보 저장소에 TTL 과 삭제 경로" · `email-compliance` 30일 내 삭제 | **C6 의 3년 보존.** 삭제·익명화는 C6 이 요구한 "누가·무엇을"을 파괴한다 |
| 마스킹 해제 예외 경로 | `data-masking` (admin 역할 전체값 반환) · `implementing-data-minimization-architecture` (escalation 티어 해제) | **C1 의 예외 없는 금지** |
| 거래성 메시지는 동의 불필요 | `email-compliance` (contractual necessity) · `sms` | **C4 의 "확인 못 하면 보내지 않는다"** — 정확히 반대 결론 |
| 모든 메시지에 구독 해지/STOP | `notification-design` · `double-opt-in-email` · `email-compliance` · `sms` | **C5 의 본문 구성** — 청구 통지에 마케팅 푸터가 붙는다 |
| 본문 개인화·미리보기 권장 | `notification-design` (`Clear numbers`) · `sms` (Value·이름 토큰) | **C5 의 "상태 이외의 민감 정보 금지"** |
| audit 에 IP·UA·변경 전후를 담으라 | `audit-logging` · `healthcare-phi-compliance` · `consent-record-keeping` · `data-privacy-compliance` | **C3 의 "식별자는 청구 번호·내부 ID 만"** |
| 업무 식별자를 로그에서 배제하라 | `healthcare-phi-compliance` (`even patient.id should be an opaque UUID`) | **C3 이 청구 번호를 허용 식별자로 둔 것** — 따르면 조사 가능한 로그를 못 쓴다 |
| 소유자 불일치 403 으로 대리 조회 차단 | `gdpr-compliant` (`if (resource.OwnerId != currentUserId) return 403`) | **C7 의 조건부 허용** — 대리 조회는 이 서비스의 정상 경로다 |

## 빈칸과 이유
**정책 조항 쪽에는 빈칸이 없다**(C1~C7 모두 「덮음」). 빈칸은 전부 **후보 스킬 쪽**에 있고, 이유는 셋이다.

| 빈칸 | 이유 |
|---|---|
| `secure-api-review` 열의 C1·C2·C4·C5·C6·C7 | **S5 영역이라 이 레인이 손대지 않는다.** 이 스킬의 본문은 플레이북 예시 축자라 S5 브리프가 한 글자도 바꾸지 말라고 못박았다. C3 만 겹치므로 위 「겹침」에 우선순위를 적어 두었다 |
| 후보 18건 전부의 C7 | **덮는 후보가 하나도 없었다.** 「제3자가 고객 **대신** 조회한다」는 자리 자체가 공개 스킬 생태계에 없다. 가장 가까운 것이 `purpose-based-access` 의 "전제 레코드 없으면 거부 + 결정 감사" 골격과 `data-privacy-compliance` 의 본인확인 게이트인데, 둘 다 대상이 **정보주체 본인**(DSAR)이지 대리인이 아니다. 그래서 C7 은 자작 외에 길이 없었다 |
| 후보 18건 전부의 C6 「덮음」 | 조회(read)를 감사 대상으로 삼은 파일이 `audit-logging`·`purpose-based-access` 둘뿐이고, **3년을 말하는 파일은 0건**이라 어느 것도 「덮음」에 이르지 못했다 |
| 후보 18건 전부의 C5 | 거래성 통지 본문에 **무엇을 싣지 말라**고 말하는 스킬이 사실상 없다. 한 문장(`notification-design` 의 민감정보 배제)이 전부이고, 같은 파일이 다른 곳에서 그것을 반박한다 |
| 후보의 C2 「덮음」 1건뿐 | `pii-scrubber` 만 허용목록+필드별 근거+문서화를 함께 갖췄다. 다만 대상이 로그·데이터셋이라 응답 필드라는 C2 의 자리와 어긋난다 |
| 「사용 신호」 열의 신뢰도 | 별 수는 모음 레포 전체를 향하는 값이라 **그 스킬 하나의 채택 증거가 못 된다**. 스킬 단위 설치 수를 보여 주는 지표는 찾지 못했다 — 「확인 못 함」 |
