---
name: spec
description: Stage 2 (Design) of the AI-native SDLC. Read an accepted intent.md and produce a requirements-and-design spec.md constrained by the organisation's policy skills (security, compliance, brand, UX), with flagged concerns first. Use when an intent is accepted, when asked for a spec/requirements/design from an intent, or on /sdlc:spec. Also used non-interactively by CI.
argument-hint: "<change-id or path to intent.md> [--figma <url>]"
---

# /sdlc:spec — requirements and design in one pass

Read `sdlc-loop`. The product owner reviews this spec; they do not write it.

## Preconditions

1. Resolve the change: `$ARGUMENTS` is a change id, a path to `intent.md`, or empty (then list changes whose
   `intent.md` is `status: accepted` and has no `spec.md`, and ask which one).
2. `intent.md` must be `status: accepted`. If it is `draft`, stop and say the product owner must accept it
   first (merge). If the user explicitly overrides, proceed and write `override: intent not accepted` in the
   spec frontmatter.
3. Load every policy skill available: `security-policy`, `compliance-policy`, `brand-guidelines`,
   `ux-standards`, `secure-api-review`, plus any under the repo's `.claude/skills/`. Record which ones you
   applied in `skills_applied` (name@last-reviewed date from the skill header).
4. If a Figma URL is given or referenced in the intent and the Figma connector is available, read the frames
   with `get_design_context` / `get_screenshot` and treat them as the approved mock.
5. If the tracker holds the record (`sourceOfTruth: tracker|linked`), read the ticket first (`tracker-sync`).

## Produce `spec.md`

Use `sdlc/changes/_template/spec.md`. The prompt you are executing is, in the course's words:

> Read the intent.md and produce a requirements and design spec for integrating it into our existing codebase.
> Apply the skills available to you so the spec conforms to our brand guidelines, security policies and UX
> standards. Document the spec fully as spec.md, ready to hand to the engineering team. Describe clearly any
> areas of concern, especially where you cannot satisfy contradicting policies.

Rules:
- **Flagged concerns come first.** Every place a policy conflicts with the intent, with another policy, or
  with the codebase gets a row: concern, policy/skill, owner who must decide, decision (blank until made).
  These are the points an analyst would have escalated.
- Read the codebase (read-only) so the design names real modules, endpoints and conventions. Cite paths.
- Requirements are numbered and testable and each traces to a line in `intent.md`.
- Acceptance criteria are observable checks an engineer can turn into tests.
- Carry every open question from `intent.md` forward as answered (where) or still open (who answers).
- Set `intent_commit` to the SHA of the accepted intent.md. Inherit `risk`; raise it if the design reveals
  money movement, auth changes, PII, regulated data or infra.

## Commit and hand over

- Branch `sdlc/spec/<change-id>`, commit `spec: <title>` with trailer `SDLC-Change: <id>`, PR titled
  `Spec: <title>` assigned to the product owner (from `owner`). In CI, label the PR `sdlc:spec`.
- If the tracker is authoritative, write a summary + SHA back to the ticket.
- Report: the path, the list of flagged concerns with owners, and the gate: **the product owner resolves each
  flagged concern with its policy owner, then accepts by merging with `status: accepted`. A tech lead must also
  approve if `risk: high`. Acceptance starts plan mode (`/sdlc:plan`).**

## Do not

- Do not write code or an implementation plan (files, order of work). That is Stage 3.
- Do not silently resolve a policy conflict. Flag it.
- Do not mark `status: accepted`.
