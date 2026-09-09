# Metrics — the lessons' indicators as git commands

L3 292: "Git log will give this directly." Every indicator below is one command against this repo.
`CHAIN` is a chain directory, e.g. `intent/0004-lesson-only`. `created` (first conversation) is the
one value git does not know; the capture-intent skill puts it on the PR body's first line, read with
`gh pr view <n> --json body`.

## L2 capture-intent (233–239)
- Leading — time from first conversation to committed intent.md: the PR body's first line versus
  `git log --diff-filter=A --format='%aI %h' -- $CHAIN/intent.md`
- Lagging — survival rate (accepted = merged, closed = rejected):
  `gh pr list --state all --search 'intent.md' --json number,state,title`
- Lagging — intent.md changed after the first spec.md commit:
  `git log --format=%h --since="$(git log --diff-filter=A --format=%aI -1 -- $CHAIN/spec.md)" -- $CHAIN/intent.md`

## L3 requirements-and-design (288–294)
- Leading — intent.md commit → spec.md commit (two timestamps):
  `git log --diff-filter=A --format='%aI %f' -- $CHAIN/intent.md $CHAIN/spec.md`
- Lagging — spec.md commits dated after the first plan.md commit:
  `git log --format=%h --since="$(git log --diff-filter=A --format=%aI -1 -- $CHAIN/plan.md)" -- $CHAIN/spec.md`

## L4 plan-mode (362–366)
- Leading — share of changes merged from the first implementation pass:
  `gh pr list --state all --search "$CHAIN" --json number,state,title` — one implementation PR per
  chain and no CLOSED one is a first pass.
- Leading — plan approval (its merge) → merged PR of the code:
  `gh pr list --state merged --json number,title,mergedAt --search "$CHAIN"`
- Lagging — does the merged diff still match plan.md's "Files that change":
  `gh pr diff <n> --name-only` for the PR that carried the code, then read the list against the
  plan by eye. (Not `<plan commit>..HEAD` — that picks up every later chain's files; measured on 0008.)
- Lagging — rework cycles per change: `gh pr view <n> --json reviews,commits --jq '{reviews: (.reviews|length), commits: (.commits|length)}'`

## L5 CLAUDE.md (442)
- Leading — corrections/changes to CLAUDE.md: `git log --oneline -- CLAUDE.md`
- Lagging — outside this repo (new-joiner time-to-first-merged-PR is org PR history)

## L6 skills (505)
- Leading — policy-owner sign-off → skill merge: `git log --diff-filter=AM --format='%aI %h' -- .claude/skills/<name>/SKILL.md`
- Lagging — outside this repo (review findings citing the policy are read by a person on the PR)

## L7 hooks-as-build-time-guardrails (511)
No separate "How to measure it" section — it rides on L6's (505); nothing to add here.

## L8 parallel sessions and subagents (588)
- Leading — outside this repo (concurrent sessions per engineer is the OTel export)
- Lagging — merges per week: `git log --since=1.week --oneline --merges | wc -l | tr -d ' '` (rework rate is outside this repo)

## L9 feedback loop (659)
- Leading — first-pass CI success: `gh run list --workflow=check.yml --json conclusion,event`
- Lagging — review time: `gh pr view <n> --json createdAt,mergedAt`
  (change failure rate is outside this repo, from an incident tracker)

## L10 continuous evals (729)
- Leading — pass rate over time: stack `evals/run.sh`'s `result.json` per commit; a person reads the series (no script here)
- Lagging — outside this repo (incident-to-eval-case time is an incident tracker)

## L11 AI in the PR review loop (795)
- Leading — time to first review: `gh pr view <n> --json createdAt,reviews --jq '.reviews[0].submittedAt'`
- Lagging — outside this repo (pre/post-merge defects need an incident tracker)

## L12 hooks as approval gates (930)
- Leading — gate wait time and verdict: `.claude/hooks.log` (the decision log this repo writes), summed by a person
- Lagging — outside this repo (gate violations reaching production is an incident tracker)

## L13 CI/CD integration and deployment (997)
- Leading — pipeline failures resolved without a human: `gh run list --json conclusion,event`
- Lagging — outside this repo (DORA measures come from CI/deploy tooling itself)

## L14 closing the loop on metrics (1063)
- Leading — band breach → triage queue: compare bands.yml's run timestamp against `git log --diff-filter=A --format=%aI -- intent/*/intent.md` by hand
- Lagging — outside this repo (repeat-incident rate is an incident tracker)

Nothing here is computed by a script. The numbers are for a person to read once a quarter.
