# H01 — installed team harness, current artifacts and accepted references

**Bounded result: pass after iteration.** This is a partial process experiment on the F02 request tracker.
The bare template remains add296d; an external user-installed sdlc-claude runs developer→independent reviewer→
automatic resume. Developer is Sonnet/low; final reviewer Sonnet/medium. The actual user of the product is represented
by Codex root as HUMAN. No hidden reasoning or private oracle/transport helper was supplied to the product agent.

Setup: 8dbf319f19fd8be2e006151867363b7867665bfb. Accepted spec: 76a38cca43a4cf5b17432bd289256120b30916b0.
Final product: 0732201e8fb413ccf59361948aca63f27b4f5099, with plan/code/tests/README committed together.

Eight HUMAN turns and two automatic reviewer-feedback turns ran in the same development session.
The first document rollbacks were missed: runtime turns02/03 are false passes. After current-state evidence
projection, turn04 revised the missing spec/plan and automatic turn05 repaired them and passed. After spec acceptance,
turn06 falsely passed an old Upstream pin. Medium review found it; turn07 revised, automatic turn08 repaired and passed.
Turn09 waited for business decisions; turn10 understood a short answer referring to that question and ended without edits.

The rollback fault is controlled, not a natural developer failure. Previous actual omission and a meaningless comment
mutation were independently replayed as H02/H03. Final medium reviewers detect both. Failed structured output is retained
as unknown. Earlier false passes and failed implementations are preserved in raw records and HUMAN audit notes.

Product validation: 10 tests, 15 independent CLI cases, original five tests/two helpers AST and fixture unchanged.
Maker verification and focused regressions are in raw/verification. Current runtime sources are raw/runtime.
Current docs, actual tools, HUMAN acceptance and outcomes—not mere edit detection—support the judgment.

See `run-summary.json` for unique model calls, displayed costs, input/source hashes, and per-turn HUMAN audit.
Its public SHA map is authoritative for published bytes. Original SHA map identifies the bytes before email redaction
that original runtime digests refer to. Raw pass verdicts on failed turns are deliberately unchanged. Early turns predate
per-turn reviewer prompt capture; final runtime records prompt source, runtime/prompt SHA and actual argv.

Records live under raw/session, raw/human, raw/replay, and raw/matrix. This record commit adds evidence after product
validation; product source and chain content are unchanged. No new product PR, organization rules, deployment, or
general success-rate estimate is claimed. Ordinary direct claude calls do not use this harness.
