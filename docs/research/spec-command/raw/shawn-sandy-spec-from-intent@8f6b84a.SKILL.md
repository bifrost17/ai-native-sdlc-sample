---
name: spec-from-intent
description: Produce a requirements-and-design spec.md from an accepted intent.md, applying the organization's brand/security/compliance/UX skills and flagging every concern (Stage 2 of the AI-native SDLC). Use when asked to "spec this out", "write requirements", or when an intent.md is attached or referenced.
license: MIT
compatibility: Designed for Claude Code (or similar agents). Plan/spec/intent skills need git; evals and close-the-loop need CI that can run Claude non-interactively.
metadata:
  author: shawn-sandy
  version: "1.0"
  sdlc-stage: "2-design"
  source: https://claude.com/blog/the-ai-native-sdlc-playbook
---

# Requirements and design from intent.md

Stage 2 (Design) of Anthropic's AI-native SDLC playbook (claude.com/blog/the-ai-native-sdlc-playbook). Requirements and design collapse into one session. Policy is applied while the spec is written, not discovered in a review weeks later. The product owner reviews the spec but does not write it.

Write only spec.md (and, if asked, design mock notes) under this skill. Do not write code or an implementation plan — plan.md belongs to the Build stage.

## Prerequisites

- An accepted intent.md. If none exists, stop and offer the `intent-capture` skill first; do not invent intent.
- The organization's policy skills (brand, security, compliance, UX, API standards). Load every one that is available. If none are available, say so at the top of spec.md — the spec is then unconstrained by policy and the product owner must know that.

## Procedure

1. **Read intent.md in full**, plus CLAUDE.md and any existing architecture notes, so the spec fits the codebase it will land in rather than a blank slate.
2. **Name the constraints out loud** before writing: list the policy skills in force and the constraints stated in intent.md. These become the frame the spec is judged against.
3. **Write spec.md** covering:
   - Problem restated from intent.md (do not drift from the originator's meaning).
   - Functional requirements — numbered, testable, each traceable to a line in intent.md.
   - Non-functional requirements — performance, security, privacy, accessibility, observability, as the policy skills demand.
   - Design — user flow, data model changes, API surface, UI description or reference to a mock. For front-end work, reference the mock produced in Claude Design or attach a description precise enough to build from.
   - Integration with the existing codebase — which services, modules, and contracts are touched.
   - **Areas of concern** — every place a requirement conflicts with a policy, two policies conflict with each other, or a constraint from intent.md cannot be satisfied. Name the policy and the policy owner for each. Never silently resolve a conflict; that decision belongs to a human.
   - Open questions — each one from intent.md either answered here or explicitly carried forward.
   - Out of scope.
4. **Put the concerns first in your summary.** They are the points an analyst would have escalated; the product owner resolves each with its policy owner before engineering sees the spec.
5. **Commit spec.md alongside intent.md** (same folder or the location the intent home specifies), as a pull request. Record in the commit message which policy skills and versions were applied.
6. **Do not decide progression.** A human product owner decides whether spec and intent go to Build, consulting a technical lead for anything the organization classes as higher risk. Accepting the spec is what starts plan mode (the `plan-from-spec` skill).

## Reference prompt (from the playbook)

> Read the attached intent.md and produce a requirements and design spec for integrating it into our existing codebase. Apply the skills available to you so the plan conforms to our brand guidelines, security policies and UX standards. Document the spec fully as spec.md, ready to hand to the engineering team. Describe clearly any areas of concern, especially where you cannot satisfy contradicting policies.

Run this by hand first. Once it is reliable, the organization can codify it as a slash command, and then as a non-interactive job that fires when intent.md merges and opens spec.md as a PR.

## spec.md skeleton

```markdown
# Spec: <title> (from intent/<slug>.md @ <sha or date>)

Policies applied: <skill names/versions, or "none available">

## Problem
## Functional requirements
FR-1 … (→ intent.md §Problem)
## Non-functional requirements
NFR-1 …
## Design
### User flow
### Data and API changes
### UI
## Codebase integration
## Areas of concern
1. <concern> — conflicts with <policy>, owner: <name/role>
## Open questions
- From intent.md: <question> → answered: … / carried forward
## Out of scope
```

## Review questions the product owner will ask

Check these yourself before handing over: Does the spec solve the stated problem? Are the open questions from intent.md answered or carried forward? Is every concern attributed to a policy and an owner? Could engineering plan against this without going back to the originator?

## What good looks like (measure)

- Leading: elapsed time between the intent.md commit and the spec.md commit for the same change.
- Lagging: requirements rework after build starts — spec.md commits dated after the first plan.md commit. Many of these mean concerns were under-flagged or requirements were not testable.

## Caveats

- Advisory control. Skills make the policy likely to be applied; they do not force compliance. Anything that must always hold needs a hook or a review pass behind it.
- Legacy source of truth: if requirements live in a regulated tool, either that tool is authoritative (read it at session start, write back via MCP in the same session) or link both ways (record ID here, commit SHA there). State which.
