---
name: claims-ux-interaction
description: Apply the org's UX behaviour and accessibility policy (U4 destructive actions need a confirmation step and a way back · U5 no duplicated information or buttons on a screen · U6 alt text, never colour alone, keyboard-only operation) to any screen or flow of the claims status service — customer portal, adjuster and agent paths. Use whenever writing or reviewing spec.md, designing a screen or flow, adding a cancel/withdraw/delete action, or building and reviewing UI markup and components, instead of deciding these yourself or reading the policy files.
---
# Claims UX — behaviour and accessibility (U4 · U5 · U6)

`policies/ux.md` v0 is the source of truth. Each clause is quoted verbatim (Korean); the lines after
it say what to check in a spec, a screen or a component. Wording for the dialogs and messages these
rules produce is `claims-ux-copy` (U1–U3) — apply both.

## U4 Destructive and irreversible actions
> **U4** 파괴적·비가역 동작(취소·철회·삭제)은 확인 단계와 되돌리는 경로를 함께 둔다.

Both are required. A confirmation step alone does not satisfy U4, and an undo alone does not either
— many UX guides say "undo beats an are-you-sure dialog"; this policy does not follow that.

- **확인 단계** — a separate, deliberate step before the action runs: what will happen, what its
  consequence is, and two distinct labelled buttons. The confirming button names the action
  (「청구 철회」), never 「예/확인」 against 「아니오」. The destructive action is never the default focus.
- **되돌리는 경로** — write down, in the spec, how the person gets back:
  - a real undo (a window during which the action can be reversed, with its length stated), or
  - a documented recovery path (재신청 절차, 상담사가 되돌릴 수 있는 조작, 고객센터 경로) shown at the
    moment of confirmation and on the result screen.
  If nothing can be undone, that is not a design decision to make quietly — record it as an open
  question for the policy owner, because U4 requires a way back.
- One button never means two things. If a screen has both 「취소」 in the sense of closing a dialog and
  「청구 취소」 the business action, that ambiguity is a real risk here — but **no policy clause names the
  wording** (U4 does not, and brand B4/B5 cover claim status words and official names, not these verbs).
  So: raise it as an open question for the policy owner rather than deciding the words in the spec.
- Applies to adjuster and agent screens as much as to the customer portal.

## U5 One screen, one place for a fact
> **U5** 같은 정보는 한 화면에 한 번만 — 중복 안내·중복 버튼 금지.

- Each fact — 청구 번호, 상태, 금액, 다음 예정, 안내 문구 — appears **once** per screen. If a header
  and a card both want to show the status, the screen keeps one and the other refers to it.
- One primary action per screen; the same action does not appear as both a button and a link, and
  not both at the top and at the bottom. A repeated action in a long list is one action per row,
  which is not duplication.
- The same guidance is not repeated as a banner *and* helper text *and* a tooltip. Choose the place
  the person reads at the moment they need it.
- When you add a string or a control, check the screen for one that already says or does it — the
  change is then to move or replace, not to add.

## U6 Accessibility
> **U6** 모든 아이콘·이미지에 대체 텍스트, 색만으로 상태를 구분하지 않는다(문구 병기), 키보드만으로 조작 가능.

Three checks, all mandatory on every screen the change touches:
1. **대체 텍스트** — every icon and image carries a text alternative that says what it means
   (상태 아이콘 → 그 상태의 낱말), not what it looks like. An icon-only button carries an accessible name.
   U6 says **모든** 아이콘·이미지, with no exception written into it. WCAG's usual answer for a purely
   decorative image is an empty alt so a screen reader skips it — that is an **exception the policy text
   does not grant**, so take it as an open question for the policy owner instead of applying it silently.
2. **색만으로 구분 금지** — status, errors, required fields and links never rely on colour alone;
   the word is always present next to the colour (심사중 badge shows the word 「심사중」, an error field
   shows the error sentence, not only a red border). This is why U2 fixes words, not colours.
3. **키보드만으로 조작 가능** — every flow completes with the keyboard alone: focus order follows the
   reading order, focus is visible, dialogs from U4 trap focus while open and return it on close, and
   nothing is reachable only by hover or pointer.

These three are the **floor**, not the whole of accessibility. Whenever the change touches markup,
a component, or a screen — and always when the task is an audit, a screen-reader problem, a keyboard
problem or a contrast question — **also load the adopted `accessibility` skill** (`intent-sdlc-skills:accessibility`)
and work through it: it carries the method (automated pass, manual keyboard pass, screen reader pass,
severity) and the WCAG 2.2 criteria behind these three lines. Clear the floor first, then run its checks.

## What this skill does not do
- It does not write the dialog and message strings — `claims-ux-copy` (U1–U3) does.
- It does not decide policy. If a change needs a destructive action with no way back, or a fact that
  genuinely must appear twice, record it for the policy owner instead of deciding.

## In your summary
List U4, U5 and U6 one by one: which destructive actions the change has and what their confirmation
and way back are, what you removed or kept as the single place for each fact, and the result of the
three accessibility checks. Unsatisfiable clauses go under "areas of concern".
