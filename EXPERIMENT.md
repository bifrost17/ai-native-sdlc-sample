# Experiment branch — 2026-09-09 · claims-status chains

This branch is an **experiment record**, not a template version. It never merges into `main`.
`main` holds the template and the template's own chains (`intent/0001`, `intent/0004`, …);
what an experiment reveals about the template goes back to `main` as a PR.

- Template this experiment ran on: `main` up to `0daf6550` (PR #54). This branch starts from
  that commit — the tree at the branch point is identical to that `main`, so every path and
  line number cited in `docs/RUNS.md` and in the verification document resolves here.
- Chains in this experiment: `intent/0002` (feature, person) · `0005` (defect, ticket) ·
  `0006` (incident, band) · `0007` (defect, unbriefed solo agent) · `0008` · `0009` (feature,
  human–agent runs B and C). Example app `src/claims_status/`, its tests `tests/test_*_status*.py`,
  the incident eval `evals/cases/04-*` and its fixtures, and the run record `docs/RUNS.md`.
- Raw evidence the run record cites is under `raw/` on this branch only: `raw/raw-hac/` (runs B, C),
  `raw/raw-live/`, `raw/raw-liveR/` (run A), `raw/raw-chain2/`, `raw/raw-chain2R/`,
  `raw/raw-chain5/`, `raw/raw-chain6/`, `raw/raw-chain56R/` (lanes 0002/0005/0006 and their
  reviews). The `AKIAIOSFODNN7EXAMPLE` string in two files is the AWS documentation example key
  used by `tests/test_hooks.sh` as a no-secrets fixture, not a credential.
- Verification of this run against the playbook: `bifrost17/intent-sdlc-playbook-verification`.
