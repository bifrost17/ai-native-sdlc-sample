# PROVENANCE — accessibility (채택분, 원문 유지)

- 출처: https://github.com/addyosmani/web-quality-skills — `skills/accessibility/SKILL.md`
  (+ 본문이 가리키는 `references/A11Y-PATTERNS.md`, `references/WCAG.md`).
- 판: 파일의 마지막 커밋 `c6b06ad1285cd6b129b58455b2eec96ab6b67fa7` (2026-08-24T20:50:49Z). 사본은 그 ref 에서 받았다.
  frontmatter 의 `metadata.version` 은 `"2.0"`. 조사·복사 시각 2026-09-09T22:51Z (UTC).
- 라이선스: **MIT** — 세 곳이 같은 말을 한다: 레포 API `license.spdx_id = MIT`, 레포 루트 `LICENSE`
  (`MIT License / Copyright (c) 2026 Addy Osmani`, 이 폴더에 `LICENSE-web-quality-skills.md` 로 복사),
  SKILL.md frontmatter 4행 `license: MIT`. 저작자 표시: Addy Osmani, web-quality-skills.
- 사용 신호(조사 시각): 별 2,774 · 포크 249 · 최근 푸시 2026-08-24T21:07:36Z ·
  skills.sh 설치 **51,383** — 이번 조사에서 본 UX·접근성 스킬 가운데 가장 큰 값이다
  (`docs/research/ux/raw/02-discover-catalogs.txt` 의 skills.sh 검색 응답).
- **수정 여부: 없음.** 네 파일 모두 원본과 바이트 동일하다(sha256, `docs/research/ux/raw/12-adopt-copies.txt`):
  - `SKILL.md` 14,358 B · `267fb2a0…62b5d` (`cmp` 통과)
  - `references/A11Y-PATTERNS.md` 6,036 B · `f10e238d…58140`
  - `references/WCAG.md` 9,079 B · `16683e02…7a2361`
  - `LICENSE-web-quality-skills.md` · `c122223a…3587c3`
  본문 196·239·267·338·342·397·401·430·463·464행(10곳)이 `references/…` 를 가리키므로 **두 참조 파일을
  함께 가져왔다** — 안 그러면 스킬이 없는 경로를 가리킨다. 그 10곳은 상대 경로가 원 레포와 같아 그대로 맞는다.
  **맞지 않는 링크가 하나 있다**: 462행 `- [Web Quality Audit](../web-quality-audit/SKILL.md)` 는 원 레포의
  형제 스킬을 가리키는데 우리는 그 스킬을 가져오지 않았다(같은 저장소의 다른 스킬이고 이 레인의 조항과 무관).
  원문을 고치지 않는 원칙에 따라 링크는 그대로 두고 여기에 적는다 — 고칠지 여부는 README 「묻는다」 5번.
- 덮는 조항: **U6 덮음** · U1 부분. 근거 문장(SKILL.md 원문):
  - U6 「대체 텍스트」 — 48행 `**Images require alt text:**` 와 예시
    `<img src="chart.png" alt="Bar chart showing 40% increase in Q3 sales">`,
    장식용은 `<img src="decorative-border.png" alt="" role="presentation">`.
  - U6 「색만으로 구분 금지」 — 129행 `**Don't rely on color alone:**` 와 나쁜 예/좋은 예
    (`<!-- ❌ Only color indicates error -->` ↔ `<!-- ✅ Color + icon + text -->` 로 오류 문장을 병기).
  - U6 「키보드만으로 조작」 — 171행 `**All functionality must be keyboard accessible.**`,
    196행 `**No keyboard traps.** Users must be able to Tab into and out of every component.`,
    204행 `/* ✅ Use :focus-visible for keyboard-only focus */`.
  - U1 부분 — 342행은 오류를 `role="alert"`/`aria-live` 로 **알리는 법**이다. 문면의 세 요소(무엇·왜·다음 행동)는
    다루지 않는다.
  - U2 · U3 · U4 · U5 — 없음. 자세히는 `docs/research/ux/coverage.md`.
- 판정 기록: 발굴 `docs/research/ux/raw/02-discover-catalogs.txt` · `raw/06-discover-a11y.txt`,
  판·라이선스 `raw/11-read-adoption-candidates.txt`, 적대 검토 `raw/31-refute-accessibility.txt`.
  트리거 원문 `docs/research/ux/trigger-tests.md`.

## 이 레포에서 알아 둘 것 (원문은 고치지 않았다)
1. **도구 지시가 이 조직에 없다.** 18–20행은 Chrome DevTools MCP 의 `lighthouse_audit`·`take_snapshot` 을,
   24행은 Lighthouse CLI·axe 를 쓰라고 한다. 이 레포에도 템플릿에도 그런 MCP 서버와 스크립트가 없다.
   23행이 스스로 `If the live tools are unavailable, use Lighthouse CLI or axe … complete the same manual checks`
   로 물러서고 수동 검사 절차가 본문에 다 있으므로 스킬은 그대로 동작한다 — 그래서 문장을 고치지 않았다.
   도구를 도입할지는 정책 결정이라 `docs/research/ux/README.md` 「정책 오너에게 묻는다」 4번에 적었다.
2. **기준이 WCAG 2.2, 정책 U6 은 세 가지만 요구한다.** 이 스킬은 U6 보다 넓다(명도 대비, 터치 표적, 랜드마크,
   드래그 대체 수단 …). 넓은 것은 모순이 아니다. 다만 **한국 서비스의 법정 기준은 KWCAG 2.2(KS X OT0003)**
   이고 이 스킬은 그것을 언급하지 않는다 — 어느 기준을 정본으로 삼을지는 정책 오너 몫이다(README 「묻는다」 2번).
   조사에서 KWCAG 스킬을 찾긴 했으나 라이선스가 없어 채택하지 못했다(`candidates.md` 의 jun-2525/kwcag22-skills · a11ykr/kwcag22).
3. **트리거가 감사(audit) 문구에 맞춰져 있다.** description 은 `"improve accessibility"`, `"a11y audit"`,
   `"WCAG compliance"` … 에서 뜬다. spec 을 쓰거나 화면 문구를 고치는 자리에서는 뜨지 않을 수 있어,
   U6 의 바닥선(대체 텍스트·색 병기·키보드)은 설계분 `claims-ux-interaction` 이 직접 지고 이 스킬을 가리킨다.
   두 스킬이 함께 뜬 기록은 `trigger-tests.md` 의 집합 시험.
4. **본문 예시가 웹(HTML/CSS/JS) 전용이다.** 사정인·상담사 화면이 웹이 아닌 경우(데스크톱 앱 등)에는
   패턴을 그대로 옮길 수 없다. 그런 화면은 U6 의 세 요구를 설계분 쪽에서 확인한다.
