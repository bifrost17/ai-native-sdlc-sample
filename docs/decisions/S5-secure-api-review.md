# S5 — secure-api-review: 채택 2 · 설계 1

조사 일자 2026-09-09 (UTC, 09:35Z~22:09Z). 레인 `lane/S5-secure-api-review`.
근거: `docs/research/secure-api-review/README.md` · `candidates.md` · `coverage.md` · `trigger-tests.md` · `raw/`.

## 결정

1. **기준선을 그대로 채택한다** — `skills/secure-api-review/` 는 템플릿 `bifrost17/intent-sdlc-sample@016705e` 의
   `.claude/skills/secure-api-review/SKILL.md` 바이트 동일 사본이다(`raw/02` diff RC 0). S1–S4 를 덮는다.
   변수 블록의 지시(「본문의 예시 4항목은 한 글자도 바꾸지 않는다」)대로 보강은 곁에 더했다.
2. **`secrets-scan` 을 채택한다** — OWASP secure-agent-playbook `@79fea6b`(태그 v0.2.7), CC-BY-4.0.
   S8 을 덮는다. `SKILL.md` 가 가리키는 `plays/secrets-scan.md` · `templates/finding.md` 까지 함께 가져왔다
   (안 그러면 없는 경로를 가리킨다). 세 파일 모두 원문 유지 — `skills/secrets-scan/PROVENANCE.md`.
3. **`claims-api-security` 를 설계한다** — S5·S6·S7·S8 을 덮는다. 정책 조항 원문을 ID 와 함께 인용하고,
   그 조항을 코드·spec 에서 어떻게 확인하는지만 덧붙인다. 참고한 것과 일부러 따르지 않은 것은
   `skills/claims-api-security/PROVENANCE.md`.
4. **나머지 27건은 기각, 2건은 보류.** 판정과 이유는 `candidates.md`.

## 왜 설계가 필요했나 — 기각의 근거

후보 30건을 열어 읽고 후보마다 반박 담당을 따로 붙였다. S5–S8 중 하나라도 「덮음」으로 살아남은 것은
`secrets-scan`(S8) 하나뿐이다. 적대 검토에서 등급이 내려간 것이 여럿이다 —
`getsentry/security-review`(S8 덮음→부분, 채택→기각), `patricio0312rev/secrets-scanner`(채택→기각),
`addyosmani/security-and-hardening`(보류→기각), `anthropics/security-guidance`(보류→기각, 라이선스가
불명이 아니라 확정된 독점).

기각 사유의 뿌리는 셋이다(목록은 `coverage.md` 「모순」):
- **org note 위반** — 앱에서 게이트웨이 JWT 를 다시 검증하라는 지시. 후보 9건.
- **S6 위반** — 권한 없음에 403 을 돌려주는 예시. 후보 8건. 청구번호 존재 여부를 알려 주는 열거 오라클이 된다.
- **없는 도구** — trufflehog·ZAP·Burp·docker 훅·`npm audit`·Copilot MCP. 이 레포의 훅은 다섯 개뿐이고
  제품 오너가 코드 백스톱을 두지 않기로 했다.

## 트리거 시험

- 기준선 단독: 3/3 (`raw/59`–`61`).
- 2 스킬 집합(기준선 + 설계): 8/8 (`raw/51`–`58`).
- 3 스킬 집합(+ 채택분): 채택분 `secrets-scan` 4/4 (`raw/64`·`66`·`67`·`68`), 셋이 함께 뜬 `raw/64` 에서 지시 충돌 없음.
- 트리거 문장을 고친 적은 없다.

## 이 결정이 틀릴 수 있는 지점

- 「덮음」의 기준을 이 레인이 엄격하게 잡았다(S5 는 spec 의 호출 수 계산까지, S6 는 지연까지). 기준을 느슨하게
  잡으면 `getsentry`·`addyosmani` 는 S8 채택 후보로 돌아온다. 다만 둘 다 S6 와 충돌해 집합에 넣을 수는 없다.
- 설계분은 오너 서명 전이다. 정책 v0 이 바뀌면 스킬도 바뀌어야 한다(플레이북 L6 57행).
- 물어볼 것 6개는 `README.md` 「정책 오너에게 묻는다」.
