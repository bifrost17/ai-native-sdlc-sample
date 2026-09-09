# PROVENANCE — spec-policy-pass

**설계분이다.** 채택한 원문 파일이 없다 — 아래 후보들의 문장을 근거로 삼아 직접 썼다.
조사 시각 2026-09-09T09:33Z ~ 2026-09-10T07:26Z (UTC). 판정 근거는
`docs/research/spec-command/candidates.md`, 실측은 같은 폴더의 `trigger-tests.md` 와 `raw/`.

## 왜 채택이 아니라 설계인가
네 요구를 함께 덮으면서 이 저장소에 그대로 꽂을 수 있는 스킬을 찾지 못했다.
- 가장 가까운 넷(`bibutikoley/ai-sdlc-claude`, `jsnkle/ai-native-sdlc`, `shawn-sandy/ai-native-engine`,
  `gaberger/hex`)은 모두 이 플레이북이 공개된 뒤 2주 안에 만들어진 **동료 구현**이고 별 0~4개다.
  「이미 있고 사람들이 쓰는」 스킬이라 부를 사용 신호가 없다.
- 넷 다 자기 저장소의 경로·명령·상태 규약에 묶여 있다(`sdlc/changes/_template/spec.md`, `sdlc-loop`,
  `/sdlc:spec`, `tracker-sync`, `hex adr`, `.agents/`). 원문 유지 채택은 곧 깨진 참조가 된다.
- SDD 프레임워크(spec-kit·cc-sdd·OpenSpec·BMAD·Pimzino·ai-dev-tasks)는 전부 **요구와 설계를 다른
  파일로 가르고 tasks 까지 쓴다.** 우리 프롬프트의 "requirements and design spec … as spec.md" 와
  정면으로 어긋난다. 게다가 조직 정책 스킬을 로드하는 층이 사실상 없다.

## 참고한 것 — 문장별 출처
MIT 와 Apache-2.0. 축자로 옮긴 문장은 없다(우리 스킬 본문은 한국어 재서술이다). 아이디어의 출처를 남긴다.

| 우리 스킬의 규칙 | 어디서 | 원문 |
|---|---|---|
| 정책 스킬이 하나도 없으면 spec 첫머리에 「제약 없이 쓰였다」를 적는다 | `shawn-sandy/ai-native-engine` `plugins/ai-native-sdlc/skills/spec-from-intent/SKILL.md` @8f6b84a (MIT) | "Load every one that is available. If none are available, say so at the top of spec.md — the spec is then unconstrained by policy and the product owner must know that." |
| 스킬이 저절로 뜨기를 기대하지 않고 이름을 불러 연다 | `gaberger/hex` `.claude/skills/hex-spec-design/SKILL.md` @247a0a7 (MIT) | "Name the constraints explicitly in the prompt; do not assume a skill triggers on its own." / "a spec is only as constrained as the skills loaded in the session that wrote it." |
| 우려 0건인 사소하지 않은 변경은 의심한다 | 같은 파일 @247a0a7 | "A spec with no flagged concerns on a non-trivial change usually means the policies were not read." |
| 요구는 관찰 가능한 말로, 함수 이름·내부 상태로 쓰지 않는다 | 같은 파일 @247a0a7 | "The behavior a user can observe, in user-facing terms — no function names, no internal state. This is what makes it an independent oracle for the build." |
| 우려를 표로, 결정 칸은 비워 둔다 | `bibutikoley/ai-sdlc-claude` `skills/spec/SKILL.md` + `templates/sdlc/changes/_template/spec.md` @fb225c3 (MIT) | "Every place a policy conflicts with the intent, with another policy, or with the codebase gets a row: concern, policy/skill, owner who must decide, decision (blank until made)." / 표 머리 `\| # \| Concern \| Policy / skill \| Owner \| Decision \|` |
| 「추정」을 우려의 한 종류로 둔다 | `jsnkle/ai-native-sdlc` `plugin/skills/spec/SKILL.md` @4d2bd9e (MIT) | "Wherever two policies conflict, a constraint cannot be met, **or you had to guess**, write it under *Areas of concern* with the policy or owner who has to resolve it." |
| 비대화형 실행에서는 묻지 않고 결정을 적으며 사람만 답할 것은 넘긴다 | `jsnkle/ai-native-sdlc` `plugin/template/.github/workflows/spec-on-intent-merge.yml` @4d2bd9e (MIT) | "Non-interactive: do not ask questions; decide where the intent leaves a decision open, state the decision, and carry forward what only a human can answer." |
| 충돌을 희석·재해석·조용한 선택으로 처리하지 않는다. 조항을 고치려면 이 명령 밖의 개정이다 | `github/spec-kit` `templates/commands/analyze.md` @86b7a01 (MIT) | "Constitution conflicts are automatically CRITICAL and require adjustment of the spec, plan, or tasks—not dilution, reinterpretation, or silent ignoring of the principle. If a principle itself needs to change, that must occur in a separate, explicit constitution update outside …" |
| 미결로 넘길 것과 지금 물을 것을 가른다 | `Fission-AI/OpenSpec` `src/core/templates/workflows/propose.ts` @9d4e597 (MIT) | "Open questions are for genuinely deferrable unknowns, not decisions you skipped. If a question would change the specs, the chosen approach, or the task breakdown, resolve it now" / "surface conflicts with existing specs instead of silently deciding which is correct." |
| plan·태스크·코드로 새지 않는다 | 같은 파일 @9d4e597 | "**Planning boundary**: This workflow creates planning artifacts only. … Do not edit project code. After the planning artifacts are complete, stop." |
| 결정자를 구체적인 사람·역할로 적는다. 아무도 지목되지 않으면 그 사실을 적고 소유자를 제안한다 | `anthropics/claude-for-legal` `commercial-legal/skills/escalation-flagger/SKILL.md` @4a6c651 (Apache-2.0) | "**Name the approver.** Be specific — a person or role, not \"legal leadership.\"" / "If the matrix doesn't name anyone for this situation, say so" |
| 의심스러우면 올린다 — 두 값은 대칭이 아니다. 좁히는 것은 결정자의 일 | 같은 파일 @4a6c651 | "The cost of an unnecessary escalation is ~30 seconds of the approver's time … The cost of a missed escalation is … a one-way door. The costs are not symmetric. **When in doubt, escalate.**" / "The approver narrows; the skill does not." |
| 승인하지 않고 넘기기만 한다. 선택지 사이에서 고르지 않는다 | 같은 파일 @4a6c651 | "It does not approve anything. It routes." / "It does not decide between the options." |
| 걸리지 않는 스킬은 걸리지 않는다고 적고 표를 채우려 늘리지 않는다 | `anthropics/claude-for-legal` `product-legal/skills/launch-review/SKILL.md` @4a6c651 (Apache-2.0) | "**Auto-skip honestly.** If a category doesn't apply, say so with a one-line reason. Don't pad." |
| 낡거나 어긋나는 조항에서 편한 쪽을 조용히 고르지 않는다 | `levnikolaevich/claude-code-skills` `plugins/review-suite/skills/ln-11-plan-reviewer/SKILL.md` @9a69af4 (MIT) | "expose stale or contradictory artifacts instead of silently selecting the convenient one." |
| 템플릿 섹션이 없다고 우려를 빠뜨리지 않는다 | `bmad-code-org/BMAD-METHOD` `skills/bmad-prd/SKILL.md` @abe4eb1 (NOASSERTION — 아이디어만, 문장 복사 안 함) | "Never include a section because it appears; never skip a concern because no template section covered it." |

## 우리가 스스로 더한 것 (출처 없음 — 실측에서 나왔다)
1. **「연 스킬만 적는다」와 그 근거.** sha 를 `git log` 로 얻어 적는 것은 적용이 아니라는 규칙. 후보
   어디에도 없다. `raw/20-BASE-01-baseline-run.txt` 의 실측(4개 중 1개가 열리지 않은 채 인용됨)에서 나왔다.
2. **스킬 전량 열거 표(적용/미적용 + 이유).** 후보들은 "load every policy skill available" 까지만 말한다.
   빠뜨린 것을 눈에 보이게 하려면 미적용에도 이유가 필요하다.
3. **우려 종류 네 갈래(충돌 · 공백 · 미확인 · 추정)와 「양쪽 조항 ID」 규칙.** 후보들은 충돌과 공백을
   가르지 않는다. 기준선이 공백을 「조항의 정신」으로 충돌처럼 적은 실측에서 나왔다(같은 raw 파일).
4. **수치 제약은 세어 본다.** 기준선이 90자 제한을 우려로 적으면서 자기 문구를 세지 않은 실측에서 나왔다.
5. **`uncommitted` 표기.** 스킬 파일이 아직 커밋 전이면 sha 칸을 비우지 않고 그렇게 적는다.

## 수정 여부
채택한 원문이 없으므로 「원문 수정」은 없다. 위 표의 문장들은 우리 저장소의 낱말(조항 ID · `design-spec`
· `templates/spec.md` · 정책 오너)로 재서술했고, 축자 인용은 이 파일과 SKILL.md 의 인용부호 안에만 있다.

## 라이선스
참고한 파일은 spec-kit·OpenSpec·bibutikoley·jsnkle·shawn-sandy·gaberger 모두 MIT,
snarktank/ai-dev-tasks 는 Apache-2.0. BMAD-METHOD 는 NOASSERTION,
`tianjianjiang/smith` 와 `daviddlow/claude-sdlc-starter` 는 라이선스 없음 — 이 셋은 **문장을 옮기지
않았고** 아이디어 층위에서만 참고했다(BMAD 한 줄은 위 표에 출처와 함께 인용만 했다).
