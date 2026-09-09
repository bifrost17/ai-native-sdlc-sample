# Stage 2 — Design: Requirements and design in one session

Requirements and design collapse into a single prompted session. Policy is applied while the spec is written, not discovered in a review weeks later.

## What changes

- **Traditional:** requirements and design are separate phases run by separate teams — analysts formalize the idea, designers parse it back. The separation exists for accountability but is slow and lossy.
- **AI-native:** both phases happen in one session. The agent takes the accepted `intent.md` and produces a requirements and design spec, constrained by the organization's skills, with areas of concern flagged.

## Prerequisites

- An accepted `intent.md` (Stage 1).
- Brand, security, compliance, and UX policies written as skills — these are the constraints applied to the spec.

## Infrastructure

A product owner with agent access. No engineering skill is required.

## How to execute

1. The product owner opens a session with the organization's skills available and attaches the `intent.md`.
2. Prompt the agent to produce the spec conforming to those skills, and to flag areas of concern — especially where policies contradict or cannot be satisfied. Run this by hand at first, then codify it as an organization-level slash command.
3. Automate next: make acceptance of `intent.md` the trigger. A non-interactive job fires on the merge, runs the pass with the org's skills loaded, and commits `spec.md` as a pull request. From that point the product owner's first involvement is the review.
4. The product owner reviews the spec against the idea: does it solve the stated problem, and are the open questions from `intent.md` answered or carried forward?
5. Work through the flagged concerns first — these are the points an analyst would have escalated. The product owner resolves each one with its policy owner before engineering sees the spec.
6. Commit `spec.md` alongside `intent.md`. The file pair records what was asked for and what was decided.
7. A human makes the go/no-go call, consulting a technical lead for anything the org classes as higher risk. Accepting the spec is what starts plan mode in Stage 3.

## The prompt

> Read the attached intent.md and produce a requirements and design spec for integrating it into our existing codebase. Apply the skills available to you so the plan conforms to our brand guidelines, security policies and UX standards. Document the spec fully as spec.md, ready to hand to the engineering team. Describe clearly any areas of concern, especially where you cannot satisfy contradicting policies.

## Governance

Policy is read and applied while the spec is written instead of surfacing in review. The spec, the prompt that produced it, and the skill versions in force are all logged in version control. The product owner signs off the spec and routes flagged concerns to the named policy owners.

## How to measure

| | Indicator |
| --- | --- |
| Leading | Elapsed time between the `intent.md` commit and the `spec.md` commit for the same change (two git timestamps), against the old requirements-plus-design cycle. |
| Lagging | Requirements rework after build starts: count `spec.md` commits dated after the first `plan.md` commit for the same change. |

## Gotchas

- The product owner reviews the spec — they do not write it.
- The spec's job is to be plannable by engineering: tight enough that Stage 3 can plan against it without re-eliciting requirements.
