---
name: capture-intent
description: Turns a person's idea, a ticket or an incident into intent/<NNNN>-<slug>/intent.md by asking the questions an analyst would ask and writing the answers in the originator's own words. Does not propose solutions, does not write spec.md or plan.md, and does not mark the intent accepted — approval is the merge.
---
# Capture intent

> L2 200: "Brainstorm until the idea is concrete. Claude asks the questions an analyst would ask:
> scope, users, constraints, and what success looks like."
> L2 202: "Ask Claude to write the result as intent.md using the organization's template, which can
> be encoded as a skill set up by a technical team member and signed off by a lead."
> L2 231: "the accept or reject decision that sends the intent into Stage 2: Design is recorded as
> the merge or the closing review."

## What to ask
Ask in the originator's words and keep their words. Four things, then dig where answers are thin:
- **Scope** — what is in, what is out. Walk each borderline item.
- **Users** — who is affected, and who was not mentioned (operations, security, upstream teams).
- **Constraints** — what must hold: regulation, existing auth, upstream load, data retention.
- **Success** — what is different when done, in a sentence the originator can verify later.
If the originator brings a solution ("add a cache"), ask for the problem under it and record the
solution as a constraint only if they insist on it.

## What to write
Write `intent/<NNNN>-<slug>/intent.md` from this template, verbatim structure. `<NNNN>` is the
largest number under `intent/` plus one (`ls intent/`), zero-padded to four digits. `templates/intent.md`
is a copy of it; `tests/test_skill_template.py` keeps the two identical.
If two chains start at the same moment, `<NNNN>` is not "max + 1" alone: whoever ordered the
concurrent start assigns the numbers and writes the assignment in the PR body.

<!-- TEAM: adjust the intent.md template to the org's own — docs/ADOPTING.md · L13 -->
```markdown
# Intent: ‹what cannot be done today — the subject, not the solution›
Author: ‹name (team)›. Status: draft.
## Problem
‹observed facts — counts, time, frequency. Not a cause, not a fix›
## Proposed outcome
‹what is different when this is done, in a sentence the author can verify›
## Affected users and systems
‹people (which team, which customers) and systems (which service, which data)›
## Constraints
‹lines that must hold — existing auth only, no new PII, what is out of scope›
## Open questions
‹what nobody could answer yet, and who can — one per line›
```

Leave no `‹…›` behind. An open question you cannot answer stays in Open questions with the name
of who can — do not invent an answer. Show the draft to the originator and let them correct it.
If no originator is in the session (a ticket or an alert opened the chain), the PR review is
where that correction happens — say so in the PR body (0002 and 0007 both hit this).
From a ticket or an incident, Problem carries the observed facts themselves — input, expected,
actual, the command that reproduces it, and the time/SHA — not only the reporter's idea of it.

## What this skill does not do
- Does not write solutions, technology choices or estimates — spec.md and plan.md own those.
- Does not write spec.md or plan.md.
- Does not change `Status: draft`. Approval is the merge of the PR that adds this file; rejection
  is the closing review. No separate approval file, no status edit by this skill.
