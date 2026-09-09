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
1. Open `intent/<NNNN>-<slug>/intent.md`. **It must be accepted — merged to main.** Accepted is
   a fact about git, not about the file: the `Status:` line stays `draft` forever by design (L2 231,
   the merge is the approval), so do not read it as "not accepted". Check
   `git log origin/main -- intent/<NNNN>-<slug>/intent.md` (a commit there = accepted) or
   `gh pr list --state merged --search <NNNN>`. If the file exists only on a branch, stop and say
   so. No machine checks this; you do. (Two headless runs in the org-skills experiment stopped on
   a merged intent because they read the `Status:` line — `docs/research/spec-command/`.)
2. Read the skills in `.claude/skills/` that apply to this change (an endpoint that returns customer
   data → `secure-api-review`). Open each one before you name it under "Skills applied" in the
   spec — chain 0007 named one without opening it. Write each as `name@sha`, the sha from
   `git log -1 --format=%h -- .claude/skills/<name>/SKILL.md` — L3 279 logs "the skill versions
   in force"; a name alone does not say which version wrote the spec.
3. Record `Upstream: intent.md@<sha>. Status: draft.` at the top of spec.md, and leave it `draft`:
   approval is the merge of the PR that carries the spec (L2 231), nothing flips this line by hand.
   One exception: an engineer may tell you to start on a draft (a single worker stacking PR B on
   the intent PR A). Immediately below the Upstream/Status line, write one line naming who told
   you and why, and repeat it in the PR body — approval is still the merge, not this note.

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
