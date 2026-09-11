# 0019 E01/E03 — resumed work and normal boundaries

Partial SDLC experiment, F02 PR1 baseline plus the bare adopting template; dataset v5, seed 102.
Base: `8dbf319f19fd8be2e006151867363b7867665bfb` (`codex/experiment-base-0019`).
Product: `c547048c8a3c5803881d4ebd93b2b4b0b4bef3e7` before this archive commit.
No product files are changed by archiving records.

Codex was HUMAN and Claude Code was the developer. HUMAN read each actual response, supplied
business facts and acceptance, and did not remind the agent to update spec/plan. All five turns
resumed session `a9a40e15-5b0e-4e8c-874c-32c096ce5091` (first turn created it).

| Turn | Candidate and task | Observed outcome |
|---|---|---|
| T1 | plugin 0.1.2 / maker 1784593; status-only, Sonnet/medium | No edits or Skill/Agent call; expected normal boundary |
| T2 | same candidate; implement summary, Sonnet/medium | 9 tests passed, but no Skill/Agent call; invocation/completion-review failure retained |
| T3 | same candidate; JSON business addition, Sonnet/high | Natural sdlc-feedback Skill and native sdlc-verifier Agent. Spec/plan revised; child found lost upstream SHA, developer repaired it |
| T4 | plugin 0.1.3 / maker 02c63e4; accept actual spec and allow related local commit, Sonnet/high | Supplied SHA propagated to plan; plan+implementation+tests+README committed together; no new native review |
| T5 | same candidate; README title only, Sonnet/low | Only README title committed; no unrelated artifact edits or independent implementation review |

Actual model evidence: parent `claude-sonnet-5`, native reviewer `claude-opus-5` with the configured
Opus/high agent. Init reports Claude Code 2.1.265 and the user-installed plugin loaded from the
maker `org-skills` source path, not proof of execution from an isolated cache. Source was not
modified during a running turn. T4 onward metadata includes pre-run plugin source hashes; T1–T3
predate that metadata field and are tied to the committed 1784593 candidate.

HUMAN reviewed and committed spec `f706c6d12d392206b931c4c2a7a81454f17f192c`.
AGENT commit `3873db9c6416301aad3ac4ce71e6ca6c0d637ea6` has that parent and includes plan,
tracker.py, tests and README. Its plan refers to the exact accepted spec SHA. The following
`c547048` changes only the README heading. The native T3 review covered uncommitted work at that
time; it is not an approval of the later final commit. The final independent verifier confirms
the actual commit/artifact state separately.

Tests: 12 product tests pass, independent 16 CLI cases pass, original 5 tests and 2 helpers have
unchanged ASTs, fixture SHA256 is `c038196ad9f748e482a446e4025e4c6c0746b23942c39f5f457ad37dd9a53795`.
The native review found a real document reference error and also supplied lower-priority notes.
Its inference that missing old objects implied a squash was unproven; this was a shallow clone.
HUMAN clarified inherited acceptance in T4. Original outputs remain unchanged.

The final cumulative CLI-reported costs per turn total $2.71568255; process duration 489.8 seconds.
T3 emitted both pending and final result events: count only the last cumulative cost, not both.
These are CLI list-cost estimates, not subscription billing or Codex usage charges.

`raw/turns` preserves public prompts, observable tool/model output, command metadata and stderr.
The transport excludes private thinking; public copies redact emails. Source/public file hashes
and redaction counts are in `raw/manifest.json`. Verification contains observed product checks and
the independent maker/product report; private oracle code and undisclosed expectations remain
outside the agent repository. Current plugin 0.1.4 and E02 retry are documented separately in
maker `docs/experiments/0019-event-review-skill.md`.

No hosted PR, organization approval, CI, production deployment or general reliability rate was
measured. A failed invocation is not converted into a pass by the later successful turn.
