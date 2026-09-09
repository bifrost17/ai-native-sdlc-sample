# PROVENANCE — secrets-scan (채택분, 원문 유지)

- 출처: https://github.com/OWASP/secure-agent-playbook — `plugins/code-security-skills/skills/secrets-scan/SKILL.md`
- 판: HEAD `79fea6b9115b55687818f8c4073844ee9ba907a6` = 주석 태그 `v0.2.7`(태그 객체 13678d0). 파일 자체의 마지막 커밋 2026-05-17T20:08:10Z. 조사 시각 2026-09-09T13:1xZ (UTC).
- 라이선스: **CC-BY-4.0** — 세 곳이 같은 말을 한다: 레포 `LICENSE.md`(SPDX-License-Identifier: CC-BY-4.0, 이 폴더에 `LICENSE-OWASP.md` 로 복사), SKILL.md frontmatter 4행 `license: CC-BY-4.0`, `plugins/code-security-skills/.claude-plugin/plugin.json` 의 `"license": "CC-BY-4.0"`.
  `gh api repos/OWASP/secure-agent-playbook --jq .license.spdx_id` 는 `NOASSERTION` 을 준다 — GitHub 이 산문형 `LICENSE.md` 를 자동 판별하지 못하기 때문이며, 레포에 다른 LICENSE 파일은 없다.
  저작자 표시: OWASP Secure Agent Playbook (OWASP Foundation), CC BY 4.0. 이 파일이 그 표시다.
- 사용 신호(조사 시각): 별 164 · 포크 23 · 이슈 8 · skills.sh 설치 142 · OWASP 공식 프로젝트이며 `.claude-plugin/marketplace.json` 으로 배포된다.
- **수정 여부: 없음.** 세 파일 모두 바이트 동일 사본이다(`cmp` 통과):
  - `SKILL.md` ← `plugins/code-security-skills/skills/secrets-scan/SKILL.md` · sha256 `dcb0c823…fa707d`
  - `plays/secrets-scan.md` ← `plugins/code-security-skills/plays/secrets-scan.md` · sha256 `69bd30f6…3a438ac`
  - `templates/finding.md` ← `plugins/code-security-skills/templates/finding.md` · sha256 `aad190ef…584993b2`
  본문 9행이 `plays/secrets-scan.md`, 32행이 `templates/finding.md` 를 가리키므로 **둘을 함께 가져왔다** — 안 그러면 스킬이 없는 파일을 가리킨다(템플릿 CLAUDE.md 의 「존재하지 않는 경로를 가리키지 말 것」).
- 덮는 조항: **S8** (덮음). S5·S6·S7 은 이 스킬이 다루지 않는다 — `docs/research/secure-api-review/coverage.md`.
  근거 문장(SKILL.md): 3행 `…in source code and configuration files. Use when reviewing code for leaked secrets before commit/merge…` 가 정책 S8 의 「코드·설정·diff」 세 축과 겹친다. 21–24행이 실제로 찾을 패턴(AKIA…, `://user:pass@host`, PEM, `.env`/`docker-compose*.yml`), 28행이 「비밀값 원문을 발견 보고에 넣지 말 것」.
- 판정 기록: 정독 `docs/research/secure-api-review/raw/11-candidate-owasp-secure-agent-playbook-secrets-scan.txt`, 적대 검토 `raw/71-refute-owasp-secure-agent-playbook-secrets-scan.txt` (인용 9개 전부 `grep -F` 로 확인, 반박 실패).

## 이 레포에서 알아 둘 것 (원문은 고치지 않았다)
1. **13–17행의 스캐너**(trufflehog · gitleaks · detect-secrets)는 이 레포에도 템플릿에도 없다. 18행이 `If no scanner available, proceed with manual pattern analysis.` 로 스스로 물러서므로 스킬은 그대로 동작한다 — 그래서 문장을 고치지 않았다.
2. **play 89–92행 「Is it active? … Check if the key format is currently valid for the service」** 는 발견한 자격증명을 실제 서비스에 대 보라는 뜻으로 읽힌다. spec 을 쓰는 세션이 할 일이 아니다. 원문을 고치는 대신 정책 오너에게 묻는다 — `docs/research/secure-api-review/README.md` 의 「정책 오너에게 묻는다」 3번.
3. finding 템플릿(`templates/finding.md`)의 발견 보고 형식은 기준선 `secure-api-review` 의 「항목별로 요약에 적어라」와 형식이 다르다. 모순은 아니다(하나는 발견 1건의 꼴, 하나는 요약의 꼴). 트리거 집합 시험에서 두 지시가 부딪히지 않았다 — `trigger-tests.md` 62–64.
