---
name: design-spec
description: Reads an accepted intent.md and the organization's skills and writes spec.md next to it — requirements, design, constraints carried over, open questions answered or carried forward, and flagged concerns for the product owner. Does not write a spec on an intent that is not accepted, does not write plan.md, and does not sign the spec off.
---
# Design spec

> L3 245: "Once the product owner approves the intent.md, Claude takes it and produces a
> requirements and design spec. This is guided by the organization's skills for brand, security,
> compliance, and UX."
> L3 270: "Does the spec solve the stated problem, and are the open questions from intent.md
> answered or carried forward?"
> L3 276: "A human teammate always makes this call, and accepting the spec is what starts the
> plan mode play"

## Before writing
1. Open `intent/<NNNN>-<slug>/intent.md`. **It must be accepted — merged to main.** If it is
   still a draft, or only exists on a branch, stop and say so. No machine checks this; you do.
   One exception: an engineer tells you to start on a draft (a single worker stacking PR B on
   the intent PR A). Then write one line at the top of spec.md saying who told you and why, and
   repeat it in the PR body — the intent is still approved by merging PR A, not by you.
2. Read the skills in `.claude/skills/` that apply to this change (an endpoint that returns customer
   data → `secure-api-review`). Name them under "Skills applied" in the spec.
3. Record `Upstream: intent.md@<sha>` — the commit of the intent you read.

## Writing
Use `templates/spec.md`, section for section. Three rules carry the lesson:
- **Constraints** — restate every constraint from intent.md, then add any discovered here.
- **Open questions from intent** — each one gets `answered: …` or `carried forward: … (owner)`.
  Never drop one silently.
- **Flagged concerns** — where two policies conflict or a requirement breaches one, say what
  conflicts and who decides. Do not resolve a policy conflict yourself.

## Review question
Show the spec beside the intent and ask the product owner the lesson's question, verbatim:
"Does the spec solve the stated problem, and are the open questions from intent.md answered or
carried forward?"

## What this skill does not do
- Does not write a spec when intent.md is not accepted.
- Does not write plan.md — that is plan mode, after the product owner accepts the spec.
- Does not set the spec to accepted. The product owner signs off; the merge records it.
