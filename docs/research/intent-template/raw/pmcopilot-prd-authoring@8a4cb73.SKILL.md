---
name: prd-authoring
description: Use this skill when the user asks to "write a PRD", "write a spec", "product requirements document", "generate a PRD", "turn this into a spec", "create product requirements", "write acceptance criteria", or explicitly asks for a PRD or product specification. This skill writes a full PRD. For a chained workflow with JTBD analysis, OST framing, and prototype-ready spec, use the /write-prd command instead. Do NOT use this skill if the user only wants to evaluate an idea strategically — use strategy-stack or the pre-mortem skill for that.
version: 2.0.0
---

# PRD Authoring

You are writing a production-ready PRD. The PRD should be complete enough to hand to an engineer and start building — but no longer than needed to achieve that bar.

Frameworks: Lenny's PRD guide (problem-oriented, clear success criteria, just enough direction, urgency, short), Alberto Savoia (pretotype thinking), Pyramid Principle.

Key principle from Lenny: "The best PRDs are problem-oriented. They define the problem so clearly that an engineer could propose a better solution than the PM did." — Lenny's PRD guide

## Step 1 — Load Context

Read in parallel:
- `memory/user-profile.md` — PRD format preference (brief / detailed / bullet-heavy / narrative), product context, stakeholders
- `context/product/personas.md` (fallback: template)
- `context/product/roadmap.md` (fallback: template) — for OKR linkage and strategic fit
- `context/company/analytics-baseline.md` — for realistic success metrics
- `context/company/past-prds.md` — if it exists, match the team's tone and level of detail
- `context/templates/prd-template.md` — the output template

Apply `prd_format_preference` from memory. If "brief", keep sections tight. If "detailed", expand with examples.

## Step 2 — Parse the Input

Extract from the user's input:
- The feature or initiative being specced
- The user problem it solves (if stated; if not, infer from context)
- Any constraints or requirements already stated
- Any stakeholders or review requirements mentioned

## Step 3 — Clarify If Needed (One Question Only)

If the input is too vague to write a PRD (e.g., "write a PRD about AI"), ask ONE clarifying question:
"What specific problem are you trying to solve with this? Who is affected and what are they doing today?"

Do not ask multiple questions. If the problem is somewhat clear, proceed and document assumptions in Open Questions.

## Step 4 — Write the PRD

Fill in every section of `context/templates/prd-template.md`:

**Problem:** Be specific. Name the persona, describe the situation, quantify the pain where possible. The problem section should make it obvious why this is worth building now.

**Users:** Pull from `personas.md`. Primary user = most affected. User stories should be demand-side: "When [struggling moment], I want to [action] so I can [progress]."

**Solution:** Describe the core mechanic. Include explicit out-of-scope items — minimum 2. These prevent scope creep and make alignment faster.

**Key Flows:** Write 2–3 flows covering: (1) happy path, (2) an edge case or alternative path. Each flow should be numbered steps, not prose.

**System Architecture (AI features only):** If AI/ML is involved, specify model tier, prompt structure, retrieval layer, eval framework, and AI-specific failure modes. If not AI: skip this section.

**Acceptance Criteria:** 4–6 binary criteria. Each must be testable in isolation by QA. Avoid: "the feature works correctly" (not testable). Use: "When a user [action], the system [specific response] within [time/condition]."

**Edge Cases & Failure Modes:** At least 3 scenarios. Include: empty state, error state, and at least one scenario that would surprise a junior engineer.

**Success Metrics:** 2–3 metrics with baseline, target, timeframe, and measurement method. All must be outcome-oriented and measurable within 30 days of ship.

**Open Questions:** List assumptions made. Flag the one assumption that, if wrong, would most change the spec. Every high-priority open question should have an owner.

**Dependencies & Risks:** Be specific about what must be true before shipping and what could derail it.

## Step 5 — AI Feature Handling

If the feature involves AI, expand the System Architecture section:
- **Model recommendation:** claude-haiku-4-5 (fast, cheap, routine tasks), claude-sonnet-4-6 (balanced quality/cost, most PM tasks), claude-opus-4-6 (complex reasoning, strategy)
- **Prompt structure:** What does the system prompt instruct? What does the user message contain?
- **Context window needs:** What context does the model need per request?
- **Eval framework:** How will quality be measured? What's the minimum bar to ship?
- **Failure modes:** Hallucination (how detected?), latency spike (UX fallback?), cost overrun (guard and alert?)

## Step 6 — Quality Check

Before outputting, verify:
- [ ] Every bracketed placeholder is replaced
- [ ] At least 2 explicit out-of-scope items
- [ ] At least 1 failure mode that would surprise a junior engineer
- [ ] Success metrics are measurable within 30 days
- [ ] Acceptance criteria are binary and independently testable
- [ ] Top open question has an owner

## Step 7 — Save Offer

Offer to:
1. Save to `outputs/prd-[feature-name]-[date].md`
2. Update `memory/user-profile.md` with decisions made, open questions, and risks identified
