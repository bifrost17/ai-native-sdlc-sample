# Metrics — the lessons' indicators as git commands

L3 292: "Git log will give this directly." Every indicator below is one command against this repo.
`CHAIN` is a chain directory, e.g. `intent/0004-lesson-only`. `created` (first conversation) is the
one value git does not know; the intent's author states it in the file.

## L2 capture-intent (233–239)
- Leading — time from first conversation to committed intent.md: the author's stated time versus
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
- Leading — plan approval (its merge) → merged PR of the code:
  `gh pr list --state merged --json number,title,mergedAt --search "$CHAIN"`
- Lagging — does the merged diff still match plan.md's "Files that change":
  `git diff --name-only $(git log --diff-filter=A --format=%h -1 -- $CHAIN/plan.md)..HEAD`
  then read the list against the plan by eye.
- Lagging — rework cycles per change: `gh pr view <n> --json reviews,commits --jq '{reviews: (.reviews|length), commits: (.commits|length)}'`

Nothing here is computed by a script. The numbers are for a person to read once a quarter.
