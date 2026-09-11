# 0019 E02a — controlled artifact omission, first review

This is a partial experiment, not a delivered product or a full SDLC run.
Base: `8dbf319f19fd8be2e006151867363b7867665bfb` from `codex/experiment-base-0019`.
Dataset: maker `docs/experiments/datasets/v5`, E02, seed 102.
Candidate: maker `02c63e4`, user-installed plugin 0.1.3.

HUMAN copied only tracker.py, tests/test_tracker.py and README.md from E01 T3;
spec/plan remained at the base. The code/test changes were uncommitted during the review.
The preceding product commit preserves that controlled fixture after the session ended;
it is not an AGENT delivery commit and does not claim document consistency.

Codex acted as HUMAN. A new Sonnet/high Claude Code session
`a6fed224-419f-4f47-9f30-1750d0e5ef7d` received one natural precommit/branch-review request.
The parent called the sdlc-feedback Skill and native sdlc-verifier Agent (Opus/high).
Both found the JSON contract missing from current spec/plan; 12 product tests passed.
The parent omitted the common criteria path from the child prompt. The child tried a denied
filesystem-wide search, could not load that file, and used in-repo policy instead.
**Artifact omission detection succeeded; shared-criteria delivery failed.** This is not a
passing final-candidate run. No files were changed by the reviewing agent.

The child/parent also inferred a squash from unavailable older objects. The experiment was
a shallow clone; absence of history did not establish a squash. The fresh retry supplies
that factual inheritance context. No original model response is corrected retroactively.

The result led to plugin 0.1.4: criteria reside in the native agent definition, referenced
by the main skill. Retry E02b uses another fresh clone/session (`event-r03`).

`raw/turns/` contains the public HUMAN request, observable model/tool stream, invocation
metadata and stderr. The transport excludes private thinking; this archive redacts emails.
`raw/manifest.json` records source/public hashes and the fixture commit before archiving.
No hosted PR, organization approval, CI or deployment was exercised.
