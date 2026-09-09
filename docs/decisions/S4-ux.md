# 결정 S4 — ux: 공식 마이크로카피 + WCAG 감사 스킬을 채택하고, 정책 문면은 직접 설계한다

날짜 2026-09-09 (UTC) · 세션 S4 · 브랜치 `lane/S4-ux` · 상태: 오너 서명 대기

## 결정
1. **채택 2**(원문 유지):
   - `ux-copy` — anthropics/knowledge-work-plugins `design/skills/ux-copy/SKILL.md` `@2d6f7e2`, **Apache-2.0**.
     U1 을 같은 구조(`Structure: What happened + Why + How to fix`)로 덮는다.
   - `accessibility` — addyosmani/web-quality-skills `skills/accessibility/SKILL.md` `@c6b06ad`, **MIT**,
     참조 파일 2개 동봉. U6 의 세 요구를 코드 수준으로 덮고 WCAG 2.2 감사 절차를 준다.
2. **설계 2**(정책 원문을 조항 ID 와 함께 전사):
   - `claims-ux-copy` — U1 · U2 · U3(문면).
   - `claims-ux-interaction` — U4 · U5 · U6(동작·접근성 바닥선).
3. **어조는 이 레인이 아니다.** 한국어 UX 라이팅 스킬 4건(토스 계열 3 · gayoung0316)은 해요체·존댓말
   수준을 정하는 스킬이라 기각했다 — 그 자리는 `policies/brand.md` B1 과 S2 레인이다.
4. 설계분 `claims-ux-interaction` 은 마크업·화면을 건드릴 때 채택분 `accessibility` 를 **함께 로드하라**고
   지시한다(트리거 실측으로 필요해진 문장).

## 근거
- 후보: `docs/research/ux/candidates.md` — 본문을 연 39건, 채택 2 · 기각 30 · 보류 7. 발굴 6갈래의 명령·출력은 `raw/01`~`raw/09`, `raw/13`.
- 덮음: `docs/research/ux/coverage.md` — U1~U6 이 모두 덮이고, 겹침 3 · 집합 밖 모순 3 · 빈칸 7건의 이유가 있다.
- 실증: `docs/research/ux/trigger-tests.md` — 설계분 3/3 · 3/3, 채택분은 자리에 맞춰 다시 시험, 집합 시험 포함.
- 사본·해시: `raw/12-adopt-copies.txt`(네 파일 `cmp` 통과) · 각 `skills/*/PROVENANCE.md`.
- 적대 검토: `raw/30-refute-ux-copy.txt` · `raw/31-refute-accessibility.txt`. 발견을 반영한 커밋 `893c61f`.
- 레슨: 「Skills as institutional knowledge」(권고적 통제 · 트리거 시험 · 오너 서명) — `raw/40-lesson-notes.txt`.

## 기각·보류의 요점
- **U4 는 업계 관행이 정책과 반대다.** `Undo beats "Are you sure?" dialogs`(wondelai, 별 2,130) ·
  `Undo is almost always better.`(cuellarfr) · `confirmation modal **or** undo window`(vercel-labs).
  정책 U4 는 둘을 함께 요구하므로 셋 다 기각했다.
- **라이선스로 못 쓴 것**: Intopia(CC BY-NC-SA 4.0 — API 는 NOASSERTION 이라 함정), mgifford(AGPL-3.0),
  KWCAG 2.2 스킬 2건(라이선스 없음), design-auditor · Front-End-Checklist · AccessLint(불명).
- **자리 중복**: rampstackco · masuP9 · AccessLint · wshobson · anthropics accessibility-review 등 감사 스킬은
  채택분과 같은 자리이고 신호가 더 작다.

## 확인 못 한 것
브랜드 스킬 부재로 어조 충돌 시험을 못 했다 · 웹이 아닌 화면 · KWCAG 대응 · 실제 포털 코드 · 상류 판 갱신 흐름 ·
`ux-copy` 가 청구 레포 안에서 단독으로 뜬 적 없음. 자세히는 README 「남는 구멍」.

## 오너 결정 필요
README 「정책 오너에게 묻는다」 10건 — 다섯 어휘 밖 상태(철회) · 접근성 정본 기준 · 결정적 통제 · 도구 도입 ·
깨진 상대 경로 수정 허용 · 일반 카피 스킬 단일화 · 되돌리는 경로의 정의 · U3 수치의 정본 · 장식 이미지 예외 ·
B7 사정거리.
