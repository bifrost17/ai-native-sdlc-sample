# Experiment: <run-id>

## Identity

- Scope: full-process / partial (단계: ...)
- Case / dataset version / seed:
- Protocol main commit / persona commit:
- Clean use-template commit / seed commit:
- Integration branch / final commit:
- Stage branches:
- Started / ended (UTC):
- Result: completed / failed / undecidable / budget-stopped / contaminated
- HUMAN actor: Codex, simulated / product-owner·engineer hat
- AGENT: Claude Code

## Environment and exposure

- OS / Python / Claude CLI:
- Requested model / effort:
- Observed model / fallback:
- Working directory / available Git refs and history:
- Settings sources / managed settings / hooks / MCP:
- Installed global plugins (names·versions only):
- Selected team skills (default none) / source·version·provenance:
- Actually available skills and plugins / unexpected exposure:
- Isolation method and observed evidence / limitations:
- Public files delivered (source path → destination, SHA-256):
- HUMAN-private data location (AGENT에는 전달하지 않음):
- Existing baseline test command / rc / output path:

## Session and budget

- Claude session ID (제한된 원본 기록에만 보존) / resume linkage:
- Command arguments / permission mode / tool scope:
- Initial limit: <60 minutes or 12 HUMAN turns; owner may change before run>
- Limit changes / reason / approving experiment owner:
- Wall time / model-response time:
- HUMAN turns / AGENT responses / tool calls:
- Input tokens / output tokens / cache tokens: unknown unless observed
- Actual reported cost / currency: unknown unless observed
- Interruptions / context resets / resumed-from record:

## Conversation and decisions

원문은 실험 브랜치의 `raw/`에 보존한다. 아래 행은 고정 대화 순서가 아니라 실제 발생한 턴의 색인이다.
계정·토큰·숨겨진 추론은 저장하지 않는다.

| Turn | UTC | Role / hat | Session link | Raw path | Artifact commit | 공개 fact/decision ID · 관측 |
|---|---|---|---|---|---|---|

| Decision ID | Question / alternatives | Source or runtime-decision | Owner / answer | Revealed at turn | Changed condition |
|---|---|---|---|---|---|

## Stage review and acceptance

| Stage | Source → target branch | Reviewed commit | HUMAN decision / reason | Merge or closing commit | Remaining questions |
|---|---|---|---|---|---|

실행한 branch·commit·merge 명령과 rc, 리뷰 원문 경로를 붙인다. 로컬 기록과 실제 hosted PR을 구분한다.

## Product checks

| Oracle ID / agreed requirement | Input or action | Expected behavior | Observed output / rc | File before/after | Result / evidence |
|---|---|---|---|---|---|

- Bug reproduction before fix / after fix:
- Existing tests unchanged / new regression tests:
- Fresh-directory handoff command / rc / output:
- Maintenance observation / follow-up owner / actual incident or none:

## Process and skill observations

| Phase | Available / selected skill | Applicable or skip reason | Successful body read / exact source and version | Concrete application / artifact | Finding / limit |
|---|---|---|---|---|---|

- Scope·policy assumptions raised and resolved:
- Human decisions versus agent self-approval:
- Tool failure / hook effect versus advisory behavior:
- Incomplete steps / contamination / unobserved behavior:

## Outcome and retained evidence

- Product outcome:
- Process outcome:
- First failure (verbatim), or none:
- Budget stop position / resumable next step:
- Raw command outputs / tests / artifact paths:
- Preserved integration commit / stage commits:
- Suggested template feedback (separate from product change):
- Main index entry only: case/version/seed, branch, base/final, scope/result, evidence path.
