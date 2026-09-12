# PROVENANCE — claim-data-compliance

**설계분이다.** 기존 스킬을 옮긴 것이 아니라 이 레인에서 썼다. 채택한 원문이 없으므로 「수정 여부」는 해당 없음.

- **정본**: `policies/compliance.md` v0 (Status: draft — 오너 서명 대기). 덮는 조항 **C1 · C2 · C3 · C6 · C7**.
- **전사**: 본문의 `> **C1**` … `> **C7**` 인용 블록은 정본에서 **축자로** 옮긴 것이다.
  `policies/compliance.md` 와 바이트 단위로 일치함을 확인했다(5/5 일치, 방법은 `docs/research/compliance/README.md`).
  그 아래 항목들은 조항을 이 서비스의 자리(응답 DTO·로그·이력·대리 조회)로 푼 것이고, 정본에 없는
  의무를 새로 만들지 않았다.
- **조사·판정**: `docs/research/compliance/candidates.md`(후보 18건), `coverage.md`(조항 × 스킬),
  `trigger-tests.md`(로드 3/3 + 집합 1회). 결정 1쪽은 `docs/decisions/S3-compliance.md`.
- **라이선스**: 이 레포의 것. 외부 스킬의 문장을 복사하지 않았다.

## 참고한 것 (착상만 · 문장 복사 없음)
후보 18건 중 **채택 0건**이라 이 파일에 옮겨 온 원문은 없다. 아래는 구조를 짤 때 본 것과,
그것을 **그대로 쓰지 않은 이유**다. 사본은 모두 `docs/research/compliance/raw/` 에 있다.

| 참고한 것 | 판(sha) · 라이선스 | 무엇을 가져왔나 | 왜 그대로 쓰지 않았나 |
|---|---|---|---|
| SkillMedev/skills `pii-scrubber` | 7eb6f5e · MIT | **C2 의 논리** — 차단목록은 새 필드가 생기면 fail open 이고 허용목록은 fail closed 라는 논증. 「목록에 없으면 응답에 없다」는 문장의 뼈대 | 사정권이 로그·데이터셋·LLM 프롬프트라 C1 의 자리(응답·화면·통지)와 어긋나고, C6·C7 이 없다. 모범 로그 예시가 뒤 4자리·토큰을 로그에 남겨 C3 의 식별자 한정보다 느슨하다 |
| affaan-m/everything-claude-code `healthcare-phi-compliance` | 316d399 · MIT | **C3 의 세 자리** — 오류 메시지·콘솔·로그를 각각 짚고 식별자를 내부 ID 로 한정하는 짜임 | audit 레코드에 `changes.before/after` 와 `ip_address` 를 담아 C3 을 깬다. `even patient.id should be an opaque UUID` 는 **청구 번호 사용을 막아** C3 의 허용 식별자와 정면으로 어긋난다. 전편이 환자·시설 어휘 |
| TerminalSkills/skills `audit-logging` | cb6bc00 · Apache-2.0 | **C6 의 필드 골격** — 역할과 ID 를 나눠 적고, 시각을 ISO 8601 UTC 로 두고, **조회(read)를 1급 감사 대상**으로 삼는 것 | 보존이 6년(HIPAA 표·S3 Object Lock)이라 C6 의 3년을 덮어쓴다. `ip_address` 를 필수로 요구해 C3 위반. 해시체인·WORM 은 정책이 요구하지 않는 인프라 |
| mukul975 `purpose-based-access` | b120c9e · Apache-2.0 | **C7 의 형태** — 전제 레코드가 없으면 **상류를 부르기 전에** 거부하고, 그 결정과 근거 ID 를 함께 남긴다 | `_apply_column_masking` 이 이름과 달리 원본 SQL 을 그대로 돌려주는 스텁이라, 그대로 두면 「마스킹 적용됨」으로 오판해 C1 을 뚫는다. 504줄 중 정책에 닿는 건 14줄 |
| mukul975 `implementing-data-minimization-architecture` | a68a177 · Apache-2.0 | **C2 의 자리** — 허용목록을 엔드포인트마다 두고 필드마다 근거를 남긴다는 착상 | 지시문이 아니라 논문형이라 행동을 바꾸지 못한다. escalation 티어의 마스킹 해제 경로가 C1 을 깨고, 가상 회사의 필드 목록이 우리 허용목록으로 복사될 위험 |
| github/awesome-copilot `gdpr-compliant` | a2fde31 · MIT | **어법** — MUST/MUST NOT 로 규칙을 세우고 마지막에 점검 목록을 두는 꼴 | 보존표(12–24개월 · 6개월)가 C6 의 3년과 충돌하고, `if (resource.OwnerId != currentUserId) return 403` 이 C7 의 대리 조회를 원천 차단한다 |

## 기준선에서 가져온 규칙
- `secure-api-review`(템플릿, S5 영역)와 **겹치는 C3 의 우선순위를 본문에 적었다** — 어긋나면 그쪽이 정본.
  그 스킬의 본문은 플레이북 예시 축자라 이 레인이 손대지 않는다.
- `design-spec`(템플릿)의 「Flagged concerns — 정책 충돌을 스스로 풀지 않는다」를 그대로 따르게 했다.
- 트리거 문장은 S8 이 실측한 것(`docs/work/NOTES.md` 3번)에 따라 **자리를 겨냥**했다 —
  spec 을 쓸 때 · 엔드포인트를 만들 때 · 로그를 붙일 때 · 리뷰할 때.

## 고칠 때
정책이 바뀌면 **정본을 먼저 고치고**(정책 오너의 PR), 그다음 이 스킬을 고쳐 오너 서명을 받는다
(L6: "When the policy changes, change the skill and have the policy owner sign off on the change").
이 스킬을 고쳐 정책을 바꾸지 않는다. 인용 블록을 고칠 때는 정본과의 축자 일치를 다시 확인한다.
