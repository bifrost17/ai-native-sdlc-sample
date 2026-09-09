# 조항 × 스킬 — secure-api-review (S5)

행은 `policies/api-security.md` 의 조항 ID, 열은 스킬. 칸은 **덮음** · **부분** · **—**.
「덮음」의 뜻: 그 스킬을 로드한 세션이 그 조항을 실제로 확인하게 만드는 문장이 있다.
「부분」: 소재는 건드리지만 조항이 요구하는 것까지는 가지 않는다(예: 「rate limit 을 걸어라」는 있으나 상류 예산·캐시 정책을 spec 에 적으라는 말은 없다).

## 채택·설계한 집합

| 조항 | secure-api-review (기준선·채택) | claims-api-security (설계) | secrets-scan (채택) |
|---|---|---|---|
| **S1** 인증 | 덮음 | — (org note 를 가리키기만) | — |
| **S2** 입력 검증 | 덮음 | — | — |
| **S3** 감사 | 덮음 | — | — |
| **S4** 데이터 분류(pii) | 덮음 | — | 부분 |
| **S5** 상류 호출 예산 | — | 덮음 | — |
| **S6** 열거 방지 | — | 덮음 | — |
| **S7** 세션 계약 | — | 덮음 | — |
| **S8** 비밀값 | — | 덮음 | 덮음 |

여덟 조항이 모두 덮인다. 근거는 각각:
- S1–S4 — 정책이 「문면은 그 스킬이 정본」이라고 못박은 4항목(`policies/api-security.md` 5행). 기준선 파일을 바이트 동일로 옮겼다(`skills/secure-api-review/PROVENANCE.md`).
- S5–S8 — 설계분이 조항 원문을 인용부호로 옮기고(`skills/claims-api-security/SKILL.md`), 각 절이 코드·spec 에서 무엇을 보는지 적는다.
- S8 (secrets-scan) — `SKILL.md` 3행 `…in source code and configuration files. Use when reviewing code for leaked secrets before commit/merge…` 와 21–24행의 패턴 목록.
- S4 (secrets-scan, 부분) — 28행 `Never include actual secret values in findings. Show redacted versions only` 는 「비밀값을 보고서에 싣지 말라」다. S4 는 pii 를 로그·오류 메시지에서 빼라는 것이라 대상이 다르다 — 그래서 부분.

## 겹침

- **S8 이 둘에 있다** — 설계분(`claims-api-security` S8 절)과 채택분(`secrets-scan`). 모순이 아니라 역할이 다르다: 설계분은 **규칙**(코드·설정·diff 에 자격증명 금지, 훅이 막으면 값을 바꾼다, spec 에는 변수 이름만)을 말하고, 채택분은 **찾는 법**(스캐너 우선순위, 패턴 목록, 고위험 파일, 원문 비노출, 회전)을 말한다. 트리거도 갈린다 — 채택분은 검토·감사 문구에서 뜨고(66–68), 설계분은 설정 파일을 새로 쓸 때 떴다(62).
- **S1** — 설계분 S7 절이 org note 를 한 번 더 가리킨다(「포털이 JWT 를 검증해 세션을 넘긴다… 이 스킬은 어느 키를 읽느냐의 문제다」). 기준선을 되풀이하지 않고 경계를 긋기 위한 것이다.
- 채택분의 발견 보고 형식(`templates/finding.md`)과 기준선의 「항목별로 요약에 적어라」가 한 답에 같이 놓일 수 있다. 셋을 함께 넣은 시험(raw/64)에서 절을 나눠 쓰고 충돌하지 않았다.

## 모순

집합 안에는 없다. 시험으로 확인한 범위는 `trigger-tests.md` (셋이 함께 뜬 raw/64, 둘이 함께 뜬 raw/53·54·57·58).

집합 **밖**에서는 흔했다 — 기각 사유의 다수가 이것이다. 되풀이된 두 가지:
1. **앱에서 게이트웨이 JWT 를 다시 검증하라** — 기준선 org note 가 「세션만 읽는 코드는 S1 을 만족, 다시 지적하지 말 것」이라 못박은 자리다. apisec-skills/api-security-review(L62-64) · UnitOneAI/api-security(L155·L164) · markusweldon/owasp-api(L178-196) · OWASP CheatSheetSeries REST(L50-57) · OWASP API Security 2023(0xa2 L25-27, 0xa1 L22-25) · anthropics/security-guidance(review_api.py L109) · everything-claude-code(L140-148) · pop123-ux(L130-162) · bobmatnyc.
2. **권한 없음에 403 을 돌려주라** — 정책 S6 은 없음과 권한없음을 같은 `not_found` 로 못박는데, 이 패턴은 청구번호 존재 여부를 알려 주는 열거 오라클이 된다. getsentry(api-security.md L83) · addyosmani(L131-147) · everything-claude-code(L152-167 과 그것을 못박는 시험 L434-438) · agamm(L123-129) · superagent-ai/authz-security(L57-62) · mukul975(L395-400) · apisec-skills/bola-detector(Spring `@PreAuthorize`) · OWASP CheatSheetSeries REST(L244-245).

세 번째로 잦았던 것은 모순은 아니지만 이 레포에서 죽는 지시다: 없는 도구·스크립트를 돌리라는 것(trufflehog·gitleaks·ZAP·Burp·docker TruffleHog 훅·`npm audit`·Copilot MCP·`scripts/scan-secrets.ts`). 템플릿의 훅은 다섯 개뿐이고 제품 오너가 코드 백스톱을 두지 않기로 했다.

## 빈칸과 이유

이 집합에는 조항 차원의 빈칸이 없다. 채우는 과정에서 남은 빈칸은 「기존 스킬로 덮지 못한 것」이고, 이유는 하나씩 다르다.

| 빈칸 | 무엇을 못 찾았나 | 왜 비었나 |
|---|---|---|
| **S5 를 덮는 기존 스킬** | 후보 30건 중 S5 가 「덮음」인 것 0건 | 세상의 rate-limit 스킬은 전부 **인입** 통제다(자기 엔드포인트에 429 를 건다). S5 는 **상류** 예산이고, 요구하는 산출물이 코드가 아니라 **spec 에 적힌 캐시 정책과 호출 수 계산**이다. sylphxai/api-rate-limit-quota-review 는 파는 API 의 요금제 설계였고, sickn33/api-rate-limit-handler 는 클라이언트 백오프 구현이었다. 가장 가까웠던 UnitOneAI(L39-42)조차 「상류 의존을 적어 두라」에서 멈춘다. |
| **S6 를 덮는 기존 스킬** | 0건 | IDOR/BOLA 스킬은 많지만 전부 「소유권을 확인하라」에서 끝나고, 확인 실패 시 **403 을 돌려주는 예시**를 든다 — S6 이 금지하는 바로 그것이다. 「같은 지연」을 말한 곳은 로그인 타이밍 문맥의 getsentry error-handling.md(L200-228) 하나뿐이고, 그것도 청구 조회가 아니라 인증에 대한 것이다. |
| **S7 을 덮는 기존 스킬** | 0건 | 역할별로 **세션 키 이름이 다르고 핸들러가 자기 것만 읽는다**는 계약은 이 조직의 것이다. 세상의 스킬은 RBAC(역할로 권한을 가른다)나 세션 위생(HttpOnly·SameSite·고정 공격)을 말하지, 키 이름의 분리를 말하지 않는다. everything-claude-code 는 오히려 모든 역할이 `session` 하나를 쓰는 예시를 든다(L256). |
| **S8 을 덮는 기존 스킬** | 1건(secrets-scan) 채택 · 나머지는 부분 | 후보 여럿이 S8 에 가까웠지만(wshobson · patricio0312rev · addyosmani · getsentry · everything-claude-code) 적대 검토에서 전부 내려갔다 — 코드·설정·diff 세 축을 한 규칙으로 말하지 않거나(설정 축을 오히려 「지적하지 말 것」으로 두거나), 이 레포에 없는 도구를 설치하라 하거나, 라이선스가 불명·독점이었다. |
| **정책 조항 밖** | 코드로 강제하는 층 | 스킬은 권고적 통제다(플레이북 L6 503: 「A skill is a control, though an advisory one.」). S8 뒤에는 `no-secrets` 훅이 있지만 S5·S6·S7 뒤에는 아무것도 없다. 훅·리뷰 패스를 둘지는 정책 오너의 결정이라 여기서 만들지 않았다 — `README.md` 「정책 오너에게 묻는다」 1번. |

### 보류 2건이 남긴 빈칸
`OWASP API Security Top 10 2023` 과 `OWASP CheatSheetSeries` 는 라이선스(CC-BY-SA-4.0)는 쓸 수 있으나 **스킬이 아니라 참고 산문**이라 그대로 꽂을 수 없고, 옮겨 쓰면 위의 모순 두 가지가 따라온다. 설계분은 이들에서 문장을 옮기지 않고 착상만 가져왔다(`skills/claims-api-security/PROVENANCE.md`). 정책 오너가 「정책 문면의 근거를 OWASP 로 달자」고 하면 share-alike 의무가 붙는다 — 물어볼 것 4번.
