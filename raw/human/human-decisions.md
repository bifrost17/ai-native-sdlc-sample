# HUMAN decisions and outcome

HUMAN: Codex root, simulated internal product owner. AGENT: actual Claude Code Sonnet.
Dataset v4.0.0, F02 seed102, actual-use template add296d, setup 8dbf319.

- T1 requested the planned summary feature and actual CLAUDE.md reading. No doc edit reminder in later business prompts.
- T2 approved the business addition summary --json. The real developer updated code/tests/README/spec/plan.
  The experiment rolled spec/plan back after the response. Reviewer pass was audited as FAILURE.
- T3 retained the business requirement and requested review. The controlled omission persisted. Reviewer pass was FAILURE.
- T4 used projected current evidence. After the controlled rollback, reviewer revised the omission, and the runtime
  automatically resumed the same development session. The developer repaired spec/plan and the new review passed.
- HUMAN read the actual spec R8/AC9 and accepted it in commit 76a38cca43a4cf5b17432bd289256120b30916b0.
- T5 supplied that exact accepted commit. The developer and low reviewer left the old plan Upstream reference;
  raw pass was audited as FAILURE. Low review-only checks also missed the pin; medium caught it on identical input.
- The harness changed reviewer effort to medium, leaving developer effort low; maker spec d772951 records why.
- T6 requested final handoff against the accepted spec. Reviewer found the stale plan reference and the runtime
  automatically resumed. The developer updated plan to 76a38cc; final review passed (runtime turns07→08).
- HUMAN checked the final diff, 10 tests, 15 independent CLI cases, unchanged baseline tests/helper AST and fixture.
  Plan/code/tests/README were committed together as 0732201e8fb413ccf59361948aca63f27b4f5099, parent76a38cc.
- T7 introduced an undecided future file-delivery idea and requested questions before edits/acceptance. Runtime
  returned wait, with no tool calls and no repository changes.
- T8 answered by reference to question2 and deferred the future feature; runtime retained the question context and
  returned pass without files changed. The product remains 0732201, clean before evidence packaging.

Final bounded goal: PASS. Two real automatic repair turns observed (current document content and accepted reference).
Initial false passes are failures, not relabeled successes. Injected rollback is not a natural developer omission.
H02 historical omission and H03 meaningless-comment mutation are review-only reconstructions. Final medium review
detects both. Two intervening structured-output errors are unknown and retained, not semantic pass.
Direct claude invocations, team-skills use, organization approval/CI/deployment and general model accuracy are outside this result.
