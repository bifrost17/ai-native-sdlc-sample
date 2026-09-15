# Release controls phase-two independent verification

Pinned core maker: `4e766f82948a2eac832d8141445716df9bbfde2d`.
Pinned core adopter: `787af7765ad397abdabe853c5a069b2836da4c42`.
Runtime states: PR1 accepted branch `3fefacd` (code `85dc853`), PR2 accepted branch
`7bd1af4` (code `55394d9`), pre-cleanup integrated main `2e2bd22`, and final cleanup main
`f3126d1470f97cb112afe13e04150549cb49aeb3` (code `5786273`, HUMAN acceptance `ea0965e`).

## What I ran

- Manifest verification read all 23 paths in `reviews/core-final.json`, hashed the current files,
  read the same blobs with `git show <pinned-commit>:<path>`, and compared both hashes and bytes to
  each manifest entry — rc 0. Full output: [13-core-manifest.log](13-core-manifest.log).
- `python3 -m unittest discover -s tests -v` and direct OFF/ON/invalid-value CLI checks in
  `exp/f03-owner@3fefacd` — 7 tests, rc 0. Full commands and output:
  [14-partial-pr1-runtime.log](14-partial-pr1-runtime.log).
- The same full test command and direct OFF/ON/config-switch/temporary-copy checks in
  `exp/f03-summary@7bd1af4` — 10 tests, rc 0. Full output:
  [15-complete-precleanup-runtime.log](15-complete-precleanup-runtime.log).
- `env -u TRACKER_OWNER_INSIGHTS python3 -m unittest discover -s tests -v`, direct default-on
  commands, legacy environment values `0`, `bad`, `1`, and `TrUe`, and a copied-data `complete`
  observation on final product `main@f3126d1` — 8 tests, rc 0. Full output:
  [16-final-cleanup-runtime.log](16-final-cleanup-runtime.log).
- Git history, slice paths, accepted-branch/integrated-main tree equality, and `tracker.py` blob
  hashes at every code, acceptance, and integration commit. The first zsh pair-loop did not split its
  arguments and printed rc 128 ancestry helper failures; the tree, path, and hash checks in that log
  are valid. I preserved it in [17-runtime-history-scope.log](17-runtime-history-scope.log) and reran
  every ancestry relation explicitly with rc 0 in
  [20-runtime-ancestry-corrected.log](20-runtime-ancestry-corrected.log).
- Cleanup test-method and full test-file diff comparison plus
  `rg -n TRACKER_OWNER_INSIGHTS tracker.py tests USAGE.md` — `rg` rc 1, meaning no remaining runtime,
  test, or usage match. Full output: [18-cleanup-scope.log](18-cleanup-scope.log).
- Exact maker `88b367b..4e766f8` and adopter `f89a92a..787af77` patches, plus adopter forbidden-path
  filtering — rc 0. Full output: [19-final-core-deltas.log](19-final-core-deltas.log).
- Independent north-star comparison against `65a509a`, removing only the two identified V4-08/V12-08
  paragraphs before byte comparison — rc 0. Full output:
  [21-north-star-preservation.log](21-north-star-preservation.log).
- Phase-one/final core-manifest entry comparison — rc 0. Full output:
  [22-core-baseline-semantics.log](22-core-baseline-semantics.log).
- `git diff --unified=60 85dc853..55394d9 -- tracker.py` and pinned excerpts around gate/parser
  construction — rc 0. Full output: [23-shared-gate.log](23-shared-gate.log).

I did not rerun maker `make check` or `make evals`: the production checks and code are unchanged since
phase one, whose full outputs remain [01-make-check.log](01-make-check.log) and
[02-make-evals.log](02-make-evals.log). An attempted pre-cleanup command containing shell removal of a
temporary directory was rejected before execution. I reran it without deletion; no product file changed.

## What I saw

The final manifest declares combined SHA-256
`f768eeba3fa72203fe8de0e0a004d0bd3fa43023c714eb9a496c8c62ef705379`. All 23 entry hashes match both
the current filesystem and their actual pinned commit blobs, and the current bytes equal the commit
bytes. Comparing the phase-one and final manifests yields the same 23-path set: 18 entries are unchanged;
the five changed entries are maker `docs/ADOPTING.md`, maker/adopter `docs/GIT-WORKFLOW.md`, and
maker/adopter `docs/RELEASE-CONTROL.md`.

The final maker delta is exactly those three explanatory/adoption/source-footer documents. The final
adopter delta is exactly the two shared source-footer documents. No skill, template, review contract,
policy value, product code, or checker changed after the phase-one core. The adopter's full `82d7ad2..787af77`
scope still contains no active `.claude`, experiment, product source, tests/evals, intent, or research path.

The initial `spec@32d64b9` and `plan@9e1188f` were not an autonomous success. They conflicted over
partial test exposure versus partial general release, left the `all=open+done` status boundary unclear,
and omitted a usable conditional cleanup step. HUMAN identified all three issues in turn 2. The accepted
`spec@f1ba82e` and `plan@5fc8bdc` resolve them before implementation, and the decision record preserves
both the initial drafts and the correction. This supports the narrower conclusion that the thin template
and selected examples were enough for an iterative human-agent handoff; it does not show perfect drafting
or automatic policy enforcement.

At the partial PR1 state, all 7 tests passed. With the setting absent or invalid, ordinary `list`/`show`
worked, `list --owner` was rejected before data access, and `summary` was absent. With
`TRACKER_OWNER_INSIGHTS=1`, `list --owner hana` returned R-101 and R-103 in source order while `summary`
remained absent. `tracker.py` stayed at SHA-256 `be28924a...`, `requests.json` stayed at `c038196a...`,
and the checkout remained clean.

At the complete pre-cleanup PR2 state, all 10 tests passed. Default OFF still rejected both new direct
paths before data access. ON enabled owner filtering and all/open/done summary; a copied-data completion
changed Hana's summary from `all 2/open 1/done 1` to `all 2/open 0/done 2`. The same HEAD `7bd1af4` and
same `tracker.py` SHA-256 `afa894f4...` were observed before, during, and after the config-only switch;
the source fixture and checkout stayed unchanged. The accepted branch tree equals integrated
`main@2e2bd22` exactly.

PR2 reused PR1's `owner_insights_enabled()` function, the same `TRACKER_OWNER_INSIGHTS` value contract,
the same conditional parser block, and the same exact-match `rows` path. It added `summary` inside that
existing gate rather than introducing another control. Git ancestry is sequential: accepted planning →
PR1 code/acceptance/integration → PR2 code/acceptance/integration → cleanup code/acceptance/integration.
Each accepted branch tree equals its corresponding merge result.

I observed product `main` move from `2e2bd22` to cleanup `f3126d1` while phase two was running. At the
final state all 8 tests passed. `list --owner` and `summary` work by default, and legacy values `0`, `bad`,
`1`, and `TrUe` no longer disable or alter the feature. There is no `TRACKER_OWNER_INSIGHTS` reference in
`tracker.py`, `tests/`, or `USAGE.md`. The cleanup test diff removes only
`test_off_rejects_owner_option_and_summary` and `test_off_rejects_summary`, along with their environment
plumbing; baseline list/show, exact-match/order/no-match/read-only, summary totals, post-complete summary,
and the three original tracker tests remain. Source, fixture, HEAD, and clean status were unchanged by my
final observations.

The independent north-star check found 179 annotations before and after, identical IDs/classes/grades,
and byte equality to `65a509a` after removing exactly the new V4-08 and V12-08 paragraphs. Its current
SHA-256 matches `north-star-preservation.json`.

## What does not match plan.md

None in the pinned core, adopter boundary, PR1/PR2 runtime sequence, config-only release/disable
observation, or authorized cleanup result.

The initial draft issues are recorded failures followed by HUMAN correction, not plan mismatches in the
accepted execution. Cleanup matches spec R6 and plan step 5: it preserves final feature behavior, removes
the temporary setting and its two obsolete OFF assertions, retains relevant product regressions, and
updates usage and the decision record in the same bounded slice.

## What I could not check and why

- This was a local synthetic CLI experiment. It does not verify authenticated test audiences, server/API
  bypasses, background work, database migration, multiple running versions, hosted PR/CI, deployment,
  production release, or a real stabilization period.
- The release/disable event used process-local environment changes at a fixed source and HEAD. It proves
  that bounded mechanism for this CLI, not security isolation or an operating-service control plane.
- The combined hash value is present in the manifest and every constituent entry was independently
  verified. The manifest does not state the serialization/concatenation rule used to derive the combined
  value, so I did not claim an independent recomputation of that aggregate.
- Phase-one `make evals` remains a no-key rc 2 skip, not a semantic-eval pass. No Claude CLI, network,
  remote fetch, install, merge, or external message was performed by this verifier.
- Maker README/research/review/probe/verification material remains concurrent working-tree material
  outside the pinned 23-file core. This report verifies the artifacts read and commands run here; it does
  not claim that another session's final commit or cleanup of maker worktrees has completed.
