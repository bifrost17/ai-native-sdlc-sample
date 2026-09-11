Export note: the report below is preserved from /tmp/plan0022-verifier/report.md.
Its command outputs were copied to [verifier-logs](verifier-logs/).

# Plan form R3 independent verifier report

Pinned snapshots: maker `b4ab13270836f97c67f72817200dbde55f0d096b`, adopter `82d7ad20128399c51492503db0788167cf774a8c`, product integrated main `f20a165859be6f409e8284e457b1eef01ef5d21b`.

## Result

No material mismatch was found in the committed R3 core, the maker/adopter delivery boundary, or the locally integrated F02 product result.

The R3 manifest contains 23 files. All individual blob hashes match the declared heads, and the recomputed combined SHA-256 is `bbba590806c2afb160d858553fdf5d86815ce259ed4abdbe003551247e3537b1`. All 22 R2 entries are byte-identical in R3; the sole new core file is `docs/METRICS.md`.

The maker scope `064c785..b4ab132` has 21 files, all covered by plan.md. The adopter scope `ca87cdb..82d7ad2` has exactly the ten allowed files. The previous 0021 scope `a734b29..064c785` matches its own plan. No parser, state engine, semantic checker, production code, or new test criterion was added.

`make check` was rerun only to preserve full final-R3 evidence under `/tmp`: exit 0, 96 Python tests with one acknowledged skip, hooks 28/0, eval fixtures 8/0, managed-settings PASS. `make evals` exited 2 with the documented no-key SKIP and was not run or passed. Maker skill quick validation and maker/adopter YAML parsing succeeded; adopter retains `disable-model-invocation: true`. The malformed hook input was blocked with rc=2. Sixty-nine local links in the committed maker/adopter Markdown scope resolved.

## Runtime

The product history is sequential and locally integrated:

- shared documents merged at `d6660fb`;
- abandoned PR1 state `1033eea` and corrected PR1 `10b08bc` are sibling children of `d6660fb`;
- `10b08bc` contains plan.md, tracker.py, the new owner-list tests, and USAGE.md in the same commit;
- the PR1 omission is not an autonomous pass: HUMAN feedback caused the corrected sibling commit;
- PR1 integrated at `91ccf7f`, whose tree equals `10b08bc`;
- abandoned PR2 state `ee972b0` and final PR2 `63328e1` are sibling children of `91ccf7f`; their only difference is the HUMAN-requested plan evidence reference;
- PR2 integrated at `f20a165`, whose tree equals `63328e1`.

At PR1 state `91ccf7f`, all eight tests pass, owner filtering works, and `summary` is absent with rc=2. At integrated main `f20a165`, all 16 tests pass. Direct checks produced the planned list ordering, summary totals `3/1`, Hana totals `1/1`, missing-owner totals `0/0`, and post-complete Hana totals `0/2`. List and summary preserved bytes; summary after completion preserved the completed bytes. These results agree with the preserved HUMAN oracle JSON.

The intent and spec blobs are unchanged from `d6660fb` through final main. `requests.json` and `tests/test_tracker.py` are unchanged from baseline `34f41eee` through final main. PR1 and PR2 each change only the plan, implementation, its new tests, and usage text declared for that slice.

## Limits

No hosted PR, hosted CI, remote merge, deployment, real migration, or parallel product development was checked. Semantic evals could not run without `ANTHROPIC_API_KEY`. Maker final indexes, research records, and north-star annotations were being written separately and are outside this pinned R3/core verdict. The product repo remained clean after verification.

Full outputs are `01-r3-snapshot.log` through `16-final-status-and-log-inventory.log` in this directory. `03-product-history.log` preserves one malformed ancestry helper attempt; the corrected explicit ancestry results are in `04-product-ancestry-and-recovery.log`.
