---
description: Write spec.md for an accepted intent (L3 268 — "codify it as an organization-level slash command")
argument-hint: [intent-id]
---
<!-- TEAM: add a skill per policy (brand, compliance, UX, …) for "Apply the skills available to you" to reach — docs/ADOPTING.md · L11 -->
Read the attached intent.md and produce a requirements and design spec for integrating it into our
existing codebase. Apply the skills available to you so the plan conforms to our brand guidelines,
security policies and UX standards.
Document the spec fully as spec.md, ready to hand to the
engineering team. Describe clearly any areas of concern, especially where you cannot satisfy
contradicting policies.

(L3 282, the playbook's prompt, verbatim.) The intent is `intent/$1/intent.md`; if `$1` is empty,
ask which chain. Follow the `design-spec` skill — it stops if the intent is not accepted.
