---
name: problem-solver
description: Systematic analytical frameworks for diagnosing root causes, evaluating options, and solving complex technical or operational problems.
---

# Problem-Solving Skill

Structured frameworks for diagnosis and solution evaluation. Read the reference file for whichever framework you select.

## Framework Selection

| Problem Signal | Framework | Reference |
|---|---|---|
| Unknown root cause, simple chain | Five Whys | `references/five-whys.md` |
| Conflicting requirements / trade-offs | TRIZ | `references/triz.md` |
| Slow throughput / capacity issue | Theory of Constraints | `references/theory-of-constraints.md` |
| Recurring / interconnected issues | Systems Thinking | `references/systems-thinking.md` |
| Multi-factor quality issue | Ishikawa / Fishbone | `references/ishikawa.md` |
| Critical incident, high stakes | Root Cause Analysis | `references/root-cause-analysis.md` |
| Comparing multiple solutions | Solution Evaluation Matrix | `references/solution-matrix.md` |

**Escalation path**: Start simple (Five Whys) → escalate to Ishikawa or full RCA if multiple factors emerge → finish with Solution Matrix when comparing options.

## Workflow

1. **Describe symptoms** — What, when, where, impact, what's NOT affected?
2. **Define boundaries** — Scope, recent changes, constraints, stakeholders
3. **Diagnose** — Pick framework from table above, read its reference, apply it
4. **Generate solutions** — 3-5 distinct options addressing root causes
5. **Evaluate** — Use Solution Matrix (read `references/solution-matrix.md`) to score options
6. **Plan implementation** — Actions, owners, timeline, risks, success metrics
7. **Monitor** — Track metrics, iterate if unresolved

## Diagnostic Questions

1. Symptom or root cause?
2. What changed before the problem appeared?
3. Can I reproduce it reliably?
4. Are there multiple root causes?
5. What feedback loops are at play?
6. Where is the bottleneck?
7. What's the technical contradiction?

## Anti-Patterns

- Jumping to solutions before diagnosis
- Treating symptoms instead of root causes
- Choosing solutions by ease alone
- Ignoring feedback loops
- Not monitoring after implementation
