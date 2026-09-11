---
name: capture-intent
description: Captures a person's idea, a ticket or an incident as a numbered intent.md under intent/ through proportionate questions and the originator's own words. Preserves what is wanted, why, constraints and unresolved questions for human review; leaves technical design and implementation planning to later stages.
---
# Capture intent

> L2 200: "Brainstorm until the idea is concrete. Claude asks the questions an analyst would ask:
> scope, users, constraints, and what success looks like."
> L2 202: "Ask Claude to write the result as intent.md using the organization's template, which can
> be encoded as a skill set up by a technical team member and signed off by a lead."
> L2 231: "the accept or reject decision that sends the intent into Stage 2: Design is recorded as
> the merge or the closing review."

## What to ask
Use the originator's language and terms. Ask about missing information that changes understanding;
do not repeat answered questions or require a fixed number of rounds:
- **Scope** — what is in, what is out. Walk each borderline item.
- **Users** — who is affected, including other teams or systems when they matter to this request.
- **Constraints** — confirmed limits, behaviour that must stay, and what is outside this change.
- **Success** — what is different when done, in a sentence the originator can verify later.
If the originator brings a solution ("add a cache"), ask what it should improve. Preserve it as a
proposal in Proposed outcome; record it as a constraint only when the originator confirms it is
required. Do not silently discard the proposal or turn it into an approved technical decision.
Keep observations, reported facts and suspected causes distinguishable. Numbers and evidence help
when available; a qualitative problem or opportunity is valid without invented measurements.

## What to write
Write `intent/<NNNN>-<slug>/intent.md` using the five sections below. Keep the metadata on line 2.
Use brief prose or bullets; add detail within the relevant section only when it helps the next reader.
The prompts describe what to capture, not mandatory sentence counts or technical analyses. `<NNNN>` is the
largest number under `intent/` plus one (`ls intent/`), zero-padded to four digits. `templates/intent.md`
is a copy of it; `tests/test_skill_template.py` keeps the two identical.
If two chains start at the same moment, `<NNNN>` is not "max + 1" alone: whoever ordered the
concurrent start assigns the numbers and writes the assignment in the PR body.

<!-- TEAM: adjust the intent.md template to the org's own — docs/ADOPTING.md · L13 -->
```markdown
# Intent: ‹요청자가 바라는 변화의 짧은 이름›
Author: ‹작성자와 팀 또는 요청의 출처›. Status: draft.

## Problem
‹현재 상황이나 기회, 왜 바꾸려는지. 알려진 사례나 근거가 있으면 함께 적는다.›

## Proposed outcome
‹누구에게 무엇이 달라지며 어떻게 나아졌다고 알 수 있는지. 요청자의 해결 제안은 제안임을 밝혀 보존한다.›

## Affected users and systems
‹영향받는 사람·팀·시스템. 현재 아는 범위만 적는다.›

## Constraints
‹확인된 제한, 유지할 동작, 이번에 하지 않을 범위. 확인되지 않은 조건은 질문으로 남긴다.›

## Open questions
‹남은 질문과 답할 사람·팀. 담당을 모르면 미정, 남은 질문이 없으면 없음이라고 적는다.›
```

Leave no `‹…›` behind. Keep unanswered questions with the person or team who can answer when known;
otherwise say the owner is unassigned. Use the known author or source in the Author line; if unknown,
say so rather than substituting the agent or inventing a person. Say when no constraints or questions
are currently known; distinguish missing information that matters from a confirmed lack of constraints.
Show the draft to the originator and let them correct it. Reflect corrections in the relevant section
and resolve or update the corresponding open question before handing the draft on.
If no originator is in the session (a ticket or an alert opened the chain), the PR review is
where that correction happens — say so in the PR body.
For a ticket or incident, include available evidence (input, expected/actual behaviour, reproduction,
time or revision) where it helps explain the problem. Missing reproduction steps, metrics or SHA do
not block capture; keep material unknowns visible for follow-up. This draft is not an approved spec.

When an example would help, read only the relevant synthetic example: [small feature](examples/feature.md),
[bug](examples/bug.md), or [incomplete ticket](examples/incomplete-ticket.md). Their facts are not defaults
for a new request; preserve that request's own facts and uncertainties.

When opening the PR, put the first conversation's timestamp (ISO, UTC) on the PR body's first
line when known — L2 227's leading indicator is the gap from that moment to the commit, and git does
not record when the conversation started. If unavailable, label it unknown instead of guessing.

## What this skill does not do
- Does not select or validate a technical solution or invent estimates. A captured proposal or
  confirmed constraint is input for spec.md and plan.md, not completed design work.
- Does not write spec.md or plan.md.
- Does not change `Status: draft`. Approval is the merge of the PR that adds this file; rejection
  is the closing review. No separate approval file, no status edit by this skill.
