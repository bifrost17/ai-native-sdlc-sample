# Plan: move the 2026-09-09 experiments off `main` (from intent.md 2026-09-09)
Upstream: spec.md@611b54fb90ca85945433067aeaf5ef1162faf1c8. Status: draft.
## Files that change
- `intent/0010-experiments-on-branches/{intent,spec,plan}.md` (new) — this chain.
- removed: `intent/0002-claims-status/`, `intent/0005-ownerless-claim-visible/`, `intent/0006-claims-status-stale-not-found/`, `intent/0007-claim-id-trailing-newline/`, `intent/0008-adjuster-claim-status/`, `intent/0009-agent-proxy-claim-status/`, `src/`, `tests/test_claims_status.py`, `tests/test_claims_status_defect.py`, `tests/test_claims_status_format.py`, `tests/test_claims_status_incident.py`, `tests/test_adjuster_status.py`, `tests/test_agent_status.py`, `tests/data/bands/claims-status-not-found-spike.jsonl`, `evals/cases/04-incident-stale-not-found.json`, `evals/fixtures/04-incident-stale-not-found/`, `docs/RUNS.md`.
- `README.md` — chain table down to the template's own chains; new "Experiments" section; `docs/RUNS.md` references → branch.
- `docs/PLAYBOOK-MAP.md` — rows 9 and 14 "executed as chain 0005/0006" → on the experiment branch.
- `docs/BOUNDARY.md`, `docs/ADOPTING.md` — eval case count four → three, with where the fourth went.
- `tests/data/bands/README.md` — drop the 0006 sample row.
## Order of work
1. Push `experiment/2026-09-09-claims-status` from `0daf6550` with `raw/` + `EXPERIMENT.md` (done: `cebc0e5`).
2. This chain's three artifacts, one commit each.
3. `git rm` the paths above; edit the five documents; `make check`.
4. PR; `check` green; merge.
## Risks
The riskiest step is 3: a template test that silently depended on the example app. Checked before
this chain: `grep` over the template tests and evals harness for `src/`, `test_claims_status`,
`intent/000[2-9]`, `claims-status-not-found` found nothing. `make check` in step 3 is the proof.
## Proof
`make check` output on the stripped tree (unit tests, `test_hooks: 28 passed`, `8 passed`,
`PASS managed-settings`); `git ls-files | grep -c 'src/\|test_.*_status\|RUNS'` = 0; the PR's
`check` run on GitHub.
