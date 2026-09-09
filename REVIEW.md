# Review instructions

<!-- L11 776-789: the playbook's REVIEW.md, cut to this repo. L11 762: "Findings do not approve or
block a PR on their own" — the product owner merges. -->

<!-- TEAM: add a design-principles pass if wanted, and real CODEOWNERS people — docs/ADOPTING.md · L21 -->
## Passes
Run three passes and tag each finding with its pass:
- Bugs: logic errors, broken edge cases, subtle regressions — in hooks and scripts, a case the
  test file does not cover.
- Security: secrets in the diff, PII in logs, a hook that fails open when `jq` is missing.
- Compliance: the change matches spec.md and plan.md of its chain under `intent/`, and the
  boundary in docs/BOUNDARY.md — code that checks artifact form, status or transitions does
  not belong here. A code file under `.claude/hooks/`, `scripts/`, `evals/` whose header cites no
  lesson sentence is a compliance finding; `src/` and `tests/` cite their spec clause instead.
  In a defect chain, a diff that touches an existing test file is a finding (L9 631: "check the
  diff in review and reject any change that touches a test") — the hook only sees Edit/Write.

## What Important means here
Reserve Important for findings that would break behavior, leak data or breach a policy —
including the boundary above. Style and naming are nits.

## Cap the nits
Report at most five nits per review; summarize the rest as a count.

## Do not report
Anything `make check` already fails on, and the record chain `intent/0001-bootstrap-repo/`
(history, not a target).

## What findings do
Findings inform; they neither approve nor block. The product owner approves by merging.
