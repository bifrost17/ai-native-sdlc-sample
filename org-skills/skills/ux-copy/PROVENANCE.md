# PROVENANCE — ux-copy (채택분, 원문 유지)

- 출처: https://github.com/anthropics/knowledge-work-plugins — `design/skills/ux-copy/SKILL.md`
  (플러그인 `design` v1.1.0, Anthropic 이 배포하는 지식노동 플러그인 묶음).
- 판: 파일의 마지막 커밋 `2d6f7e22dd25593f0f748010430ef86f19659735` (2026-03-13T15:57:57Z). 사본은 그 ref 에서 받았다.
  조사·복사 시각 2026-09-09T22:50Z (UTC).
- 라이선스: **Apache-2.0** — 레포 API `license.spdx_id = Apache-2.0`, 레포 루트 `LICENSE` 본문 머리
  `Apache License / Version 2.0, January 2004`. 그 사본을 이 폴더에 `LICENSE-anthropic-knowledge-work-plugins.md`
  로 두었다(Apache-2.0 4(a) 의 라이선스 사본 동봉 의무). 저작자 표시: Anthropic, knowledge-work-plugins.
  **사본은 스킬과 같은 ref(`2d6f7e2`) 에서 받은 판(11,358 B)이다** — 그 뒤 main 의 `LICENSE` 는 커밋
  `d6c8015`(2026-04-28)로 Apache-2.0 본문 뒤에 다른 문단이 덧붙어 11,607 B 가 됐다. 우리가 받은 판이
  스킬 사본의 시점과 일치하는 쪽이라 그대로 둔다(적대 검토 `raw/31-refute-accessibility.txt`).
- 사용 신호(조사 시각): 레포 별 23,943 · 포크 2,884 · 최근 푸시 2026-09-09T07:33:58Z ·
  skills.sh 설치 3,733(`docs/research/ux/raw/02-discover-catalogs.txt` 의 skills.sh 검색 응답).
- **수정 여부: 없음.** `SKILL.md` 는 원본과 바이트 동일하다 — sha256 `d46a00a6…cdcde7`, 3,436 B,
  `cmp` 통과(`docs/research/ux/raw/12-adopt-copies.txt`).
- 덮는 조항: **U1 덮음** · **U3 부분** · **U4 부분**. 근거 문장(SKILL.md 원문):
  - U1 — `### Error Messages` 절 `Structure: What happened + Why + How to fix` 와 예시
    `"Payment declined. Your card was declined by your bank. Try a different card or contact your bank."`
    — 정책 U1 의 세 요소(무엇 · 왜 · 다음 행동)와 순서까지 같다.
  - U3 — `### Loading States` 절은 `Set expectations, reduce anxiety` 한 줄뿐이다. 예상 시간·확인 시점을
    적으라는 말은 없다 → 부분.
  - U4 — `### Confirmation Dialogs` 의 `Make the action clear: "Delete 3 files?" not "Are you sure?"`,
    `Label buttons with the action: "Delete files" / "Keep files" not "OK" / "Cancel"` 는 U4 의 확인 단계와 같다.
    되돌리는 경로는 없고 오히려 `Describe consequences: "This can't be undone"` 를 예로 든다 → 부분.
  - U2 · U5 · U6 — 없음. 자세히는 `docs/research/ux/coverage.md`.
- 판정 기록: 정독 `docs/research/ux/raw/02-discover-catalogs.txt`(발굴) · `raw/11-read-adoption-candidates.txt`(판·라이선스) ·
  적대 검토 `raw/30-refute-ux-copy.txt`. 트리거 원문 `docs/research/ux/trigger-tests.md`.

## 이 레포에서 알아 둘 것 (원문은 고치지 않았다)
1. **상대 경로 링크가 이 레포에서는 가리키는 곳이 없다.** 본문 9행이
   `[CONNECTORS.md](../../CONNECTORS.md)`(사본 9행) 로 원 레포의 `design/CONNECTORS.md` 를 가리킨다. 우리 배치에서
   `skills/ux-copy/` 기준의 `../../` 는 레포 밖이다. 원문을 고치지 않는 대신 그 파일의 사본을
   같은 폴더에 `CONNECTORS.md` 로 두었다(sha256 `242e232b…41d141f`). 링크를 고치려면 원문 수정이 되므로
   정책 오너에게 먼저 묻는다 — `docs/research/ux/README.md` 「정책 오너에게 묻는다」 5번.
2. **커넥터(MCP) 절은 이 조직에 아직 해당이 없다.** `## If Connectors Available` 는 `~~knowledge base`(브랜드
   보이스·용어 표준)와 `~~design tool`(Figma 화면 맥락·글자 수 제한)이 붙어 있을 때의 지시다. 이 레포에는
   그런 서버가 없다. 스킬은 그 절 없이도 동작한다 — 그래서 문장을 고치지 않았다. 브랜드 보이스는
   커넥터가 아니라 `policies/brand.md` 와 S2 의 스킬이 정본이다.
3. **한국어 규범이 없다.** 예시가 전부 영문이고 존댓말·해요체 같은 한국어 문체 규정이 없다. 고객 문구의
   어조·표기는 `policies/brand.md`(B1~B7), 청구 도메인의 문면은 설계분 `claims-ux-copy` 가 맡는다.
   이 스킬은 마이크로카피의 **일반 형(型)** 을 준다.
4. **U4 에서 이 스킬만 따르면 정책에 못 미친다.** `"This can't be undone"` 을 예로 드는 데서 멈추므로,
   확인 단계와 **되돌리는 경로**를 함께 두라는 U4 를 만족시키려면 설계분 `claims-ux-interaction` 을 함께 써야 한다.
   집합 시험에서 두 스킬이 한 답에 같이 떠 지시가 부딪히지 않는 것을 확인했다 — `trigger-tests.md`.
5. 본문이 `# /ux-copy` · `## Usage` · `$ARGUMENTS` 꼴이다(원 레포에서 스킬이 명령처럼도 쓰인다). 우리 레포에서는
   같은 이름의 명령을 만들지 않는다 — 이름이 겹치면 하나로 합쳐진다(`docs/work/NOTES.md` 1, S8 실측).
