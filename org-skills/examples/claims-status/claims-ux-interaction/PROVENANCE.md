# PROVENANCE — claims-ux-interaction (설계분)

이 스킬은 **직접 설계**했다. U4 는 세상의 관행이 정책과 **반대**였고(확인 대신 undo), U5 를 덮는 스킬은
하나도 없었으며, U6 를 덮는 스킬은 많았지만 전부 「감사(audit)」 자리에서만 뜨기 때문이다. 후보 정독과
판정은 `docs/research/ux/candidates.md`, 빈칸의 이유는 `docs/research/ux/coverage.md` 에 있다.

## 본문의 출처
- **정책 원문**: `policies/ux.md` 의 U4·U5·U6 을 조항 ID 와 함께 인용부호로 옮겼다. 인용 밖의 문장은
  그 조항을 spec·화면·컴포넌트에서 어떻게 확인하는지만 적는다.
- **형식**: 플레이북 「Skills as institutional knowledge」 레슨의 SKILL.md 꼴. 마지막 절 「In your summary」는
  같은 레포의 `claims-api-security`·`claims-ux-copy` 와 맞췄다.
- **채택분과의 경계**: U6 절의 마지막 문단이 채택분 `accessibility`(addyosmani, MIT)를 가리킨다.
  바닥선 세 가지는 이 스킬이 지고, WCAG 전체 감사는 그 스킬이 진다.

## 참고한 것 (문장을 옮기지 않고, 착상만)

| 착상 | 어디서 | 이 스킬의 어디에 |
|---|---|---|
| 확인 다이얼로그의 버튼은 **동작 이름**으로 — 「예/아니오」·「확인/취소」가 아니라 | anthropics/knowledge-work-plugins `ux-copy` `@2d6f7e2` (Apache-2.0, 채택분) 의 확인 다이얼로그 절 | U4 「확인 단계」의 버튼 규칙 |
| 확인 화면은 **결과를 구체적으로** 말한다("Are you sure?" 단독은 실패) | cuellarfr/design-skills `design-critique/references/heuristics-and-laws.md` `@b41750a` (MIT) · Ashutos1997/claude-design-auditor-skill(라이선스 불명, 착상만) | U4 「무엇이 일어나고 결과가 무엇인지」 |
| 파괴적 버튼을 **기본 포커스로 두지 않는다** | Intopia `references/topic/Topic - Keyboard and Focus.md` `@536afe6` 의 포커스 관리(라이선스 CC BY-NC-SA → 채택 불가, 착상만) | U4 「기본 포커스가 아니다」 |
| 다이얼로그는 **포커스를 가두고 닫을 때 되돌린다** | addyosmani `accessibility` `@c6b06ad` (MIT, 채택분) 의 modal focus trap · Intopia 위 파일 | U6-3(키보드) 의 다이얼로그 문장 |
| 같은 동작이 **버튼과 링크로 두 번** 나오지 않게 한다 | oil-oil/ui-ux-guide `skills/oiloil-ui-ux-guide/references/checklists.md` `@da6a44d` (Apache-2.0) 의 `One primary submit action` | U5 「한 화면에 주 동작 하나」 |
| 목록의 행마다 반복되는 동작은 중복이 아니다 | 위 체크리스트의 목록 패턴 해석 | U5 의 예외 한 줄 |
| 색 대신 **낱말을 병기**한 오류·상태 표시 | addyosmani `accessibility` `@c6b06ad` 129행의 나쁜 예/좋은 예 (MIT, 채택분) · cuellarfr `error-prevention.md` (MIT) | U6-2 의 「낱말이 늘 곁에 있다」 |
| 아이콘 전용 버튼에 **접근 가능한 이름**을 준다 | addyosmani `accessibility` (MIT) · mgifford `image-alt-text`(AGPL-3.0 → 채택 불가, 착상만) | U6-1 의 마지막 문장 |

## 일부러 따르지 않은 것
- **「undo 가 확인보다 낫다」**(wondelai/skills `ux-heuristics` `@0dea03f`: `Undo beats "Are you sure?" dialogs`,
  `prefer undo over confirmation dialogs`; cuellarfr `interaction-design/references/error-prevention.md`:
  `Confirmation dialogs ("Are you sure?") are excise… Undo is almost always better.` 와 표의
  `Delete immediately. Show "Undo" toast for 10 seconds`). 정책 U4 는 **둘 다** 요구한다. 그래서 이 스킬은
  U4 절 첫 문단에서 그 관행을 이름 대신 내용으로 부르고 「이 정책은 그것을 따르지 않는다」고 못박는다.
  두 후보를 기각한 이유도 이것이다(`candidates.md`).
- **확인 **또는** undo 의 택일**(vercel-labs/web-interface-guidelines `command.md` `@e3d624b`:
  `Destructive actions need confirmation modal or undo window—never immediate`). 같은 이유로 따르지 않았다.
- **되돌릴 수 없음을 강조하는 문면으로 끝내기**(`This can't be undone` — 채택분 `ux-copy` 와 szilu 양쪽).
  경고는 필요하지만 U4 는 되돌리는 경로를 함께 요구한다. 채택분과의 이 간극은
  `skills/ux-copy/PROVENANCE.md` 4번에도 적어 두었다.
- **접근성을 UI 에서 언급하지 말라 · disabled 상태를 아예 쓰지 말라**(KreerC/ACCESSIBILITY.md `@4cffe22`).
  정책에 근거가 없는 강한 지시다.
- **도구 실행 지시**(axe · Lighthouse · Playwright · 전용 MCP). 이 레포에도 템플릿에도 없다. 도입 여부는
  정책 결정이라 `docs/research/ux/README.md` 「정책 오너에게 묻는다」 4번에 적었다.
- **WCAG 조항 번호로 감사 절차를 다시 쓰기**. 채택분 `accessibility` 가 이미 한다 — 되풀이하면 두 스킬이
  같은 자리에서 경쟁한다.

## 정책을 넘어선 곳 (적대 검토가 지목한 것)
`raw/31-refute-accessibility.txt` 의 축 D 검토에서 **정책 원문에 없는 규범**이 지목됐고, 그 자리를 고쳤다:
- 「취소/철회/삭제 낱말을 브랜드 B4/B5 가 정한다」는 **사실이 아니었다**(B4 는 상태 어휘, B5 는 기관·상품 이름).
  그 문장을 빼고, 낱말 구분은 정책 근거가 없으니 **오너에게 묻는다**로 바꿨다(SKILL.md U4 절 마지막 항목).
- 「장식용 이미지는 장식으로 표시해 스크린리더가 건너뛴다」는 U6 의 「**모든** 아이콘·이미지」에 **예외를 신설**하는
  것이었다. WCAG 의 표준 답이지만 정책 문면에는 없으므로, 그대로 적용하지 말고 오너에게 묻도록 고쳤다.
- 「한 화면에 주 동작 하나」·「기본 포커스 금지」·「undo 창 길이 명시」는 위 표에 출처가 공개된 확장이다.
  정책이 요구하는 것과 이 스킬이 더하는 것이 구분되도록 표를 남긴다.

## 라이선스
`SKILL.md` 와 이 파일은 이 레포의 것이다. 위 표의 착상 제공자에게서 문장을 옮기지 않았다.
특히 **Intopia(CC BY-NC-SA 4.0)와 mgifford(AGPL-3.0)** 는 라이선스 때문에 채택하지 않은 곳이므로,
그쪽 문장은 한 줄도 들어 있지 않다 — 착상만 적었고 그 사실을 여기 남긴다.

## 트리거
`docs/research/ux/trigger-tests.md` — 문구 3종 3/3 로드(raw/23·24·25), 집합 시험 포함.
**트리거 문장(frontmatter)은 고친 적이 없다.** 대신 **본문 U6 절 마지막 문단을 고쳤다** — 채택분
`accessibility` 가 이 스킬에 가려 1/3 밖에 뜨지 않아서, 「마크업·화면을 건드리면 그 스킬을 함께 로드하라」로
바꿨다(커밋 `f62ad52`). 그 뒤 같은 문구 3종에서 3/3(raw/42·43·44).
