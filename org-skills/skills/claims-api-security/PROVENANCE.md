# PROVENANCE — claims-api-security (설계분)

이 스킬은 **직접 설계**했다. 기존 스킬 중 정책 S5–S8 을 덮는 것을 찾지 못했기 때문이다 —
후보 30건의 정독·적대 검토 기록은 `docs/research/secure-api-review/candidates.md`,
빈칸의 이유는 `docs/research/secure-api-review/coverage.md` 에 있다.

## 본문의 출처
- **정책 원문**: `policies/api-security.md` 의 S5·S6·S7·S8 을 조항 ID 와 함께 인용부호로 옮겼다.
  스킬은 정책을 옮기지 만들지 않는다 — 인용 밖의 문장은 그 조항을 코드/스펙에서 어떻게 확인하는지만 적는다.
- **형식**: 플레이북 L6 「Skills as institutional knowledge」의 SKILL.md 꼴(frontmatter `name`·`description`,
  본문은 무엇을 할지) — 원문 `docs/research/secure-api-review/raw/03-playbook-skills-lesson-fetch.txt` 50–58행.
  마지막 절 「In your summary」는 기준선 `secure-api-review` 의 마지막 줄
  (`Include what you checked, item by item, in your summary.`)과 같은 꼴로 맞췄다 — 두 스킬이 한 답에서 한 형식으로 보고하도록.

## 참고한 것 (문장을 옮기지 않고, 착상만)
아래는 정독한 후보에서 가져온 착상이다. 어느 것도 문장을 그대로 옮기지 않았다 — 라이선스 의무가
따라붙는 전사를 피하고, 정책 문면이 정본이기 때문이다. sha 는 정독 시각의 값이다.

| 착상 | 어디서 | 이 스킬의 어디에 |
|---|---|---|
| 인입 rate limit 과 **상류 예산**은 다른 것이며 창/리셋 의미를 글로 남긴다 | sickn33/api-security-best-practices `@bdfbf79` L156-157 (CC-BY-4.0) | S5 의 「호출 수 계산」을 spec 에 적게 한 이유 |
| 새 경로를 보기 전에 상류 의존과 호출 수를 먼저 적게 하는 선행 게이트 | UnitOneAI/api-security `@70bc259` L39-42 (MIT) | S5 첫 항목의 순서(먼저 적고 나서 리뷰) |
| 재시도·팬아웃이 상류 호출 수를 곱한다 | sickn33/api-rate-limit-handler `@bdfbf79` L85-136 (MIT) | S5 셋째 항목(재시도·팬아웃도 계산에 넣는다) |
| 소유권 필터를 **조회 질의 자체**에 넣으면 없음/권한없음이 한 경로로 합쳐진다 | apisec-skills/bola-detector `@60350c8` L105-107 (MIT) | S6 둘째 항목(같은 경로로 조회) |
| 없는 사용자와 있는 사용자의 **지연 차이**가 존재를 누설한다(더미 해시로 상수 시간) | getsentry/security-review `@c2f99a5` references/error-handling.md L200-228 (CC-BY-SA-4.0) | S6 의 「같은 지연」을 코드 수준으로 풀어 쓴 부분 |
| 존재 누설은 목록·개수 같은 곁길로도 샌다 | OWASP CheatSheetSeries IDOR Prevention `@382113b` (CC-BY-SA-4.0) | S6 셋째 항목(목록·개수·HEAD·감사 문구) |
| 자격증명은 코드·설정만이 아니라 **커밋/머지 전 diff** 에서 본다 | OWASP secure-agent-playbook/secrets-scan `@79fea6b` L3 (CC-BY-4.0) | S8 의 「diff」 범위 |
| 자리표시자가 실제 비밀값 모양과 겹치면 훅이 막는다 | 템플릿 `.claude/hooks/no-secrets.sh` `@016705e` (MIT) | S8 둘째 항목(훅이 걸리면 값을 바꾼다, 우회하지 않는다) |
| 새 비밀값이 필요하면 **변수 이름만** spec 에 적는다 | wshobson/secrets-management `@a30778f` L229 (MIT) | S8 셋째 항목 |

## 일부러 따르지 않은 것
- **JWT 를 앱에서 다시 검증하라**는 지시(apisec-skills/api-security-review L62-64, UnitOneAI L155/L164,
  markusweldon/owasp-api L178-196, pop123-ux L130-162 …). 기준선의 org note 가 「세션만 읽는 코드는 S1 을 만족,
  다시 지적하지 말 것」이라 못박았다. 이 스킬은 S7 절에서 그 노트를 한 번 더 가리키기만 한다.
- **권한 없음에 403 을 돌려주는 패턴**(everything-claude-code L152-167, agamm L123-129, superagent-ai/authz-security L57-62,
  mukul975 L395-400, apisec-skills/api-security-review L159). 정책 S6 은 없음과 권한없음을 같은 `not_found` 로 못박는다.
  이 스킬은 「`forbidden` 없음」을 명시해 그 패턴을 막는다.
- **스캐너·훅·플러그인 실행 지시**(trufflehog/gitleaks/ZAP/Burp/TruffleHog docker hook/Copilot MCP …).
  이 레포에는 그런 스크립트가 없고, 제품 오너가 코드 백스톱을 두지 않기로 했다(기준선 파일 안 주석).
- **공격 절차**(합성 신원으로 실제 요청을 보내 관찰, 자격증명 유효성 시험). spec 을 쓰는 세션이 할 일이 아니다.

## 라이선스
- 이 파일과 `SKILL.md` 는 이 레포의 것이다. 위 표의 착상 제공자에게서 **문장을 옮기지 않았으므로**
  CC-BY-SA(getsentry·OWASP)의 share-alike 의무가 이 스킬에 붙지 않는다. 만약 나중에 그 문장을 그대로 쓰려면
  같은 라이선스와 저작자 표시를 달아야 한다 — 그때는 정책 오너에게 먼저 묻는다.

## 트리거
`docs/research/secure-api-review/trigger-tests.md` — 집합 시험 8/8 로드(51–58). 트리거 문장을 고친 적은 없다.
