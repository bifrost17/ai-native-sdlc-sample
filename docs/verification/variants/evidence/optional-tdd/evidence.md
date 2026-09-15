# Execution evidence

Scope: the user authorized local planning, implementation, and verification in this isolated copy, selected TDD, and excluded installation, hosted PRs, deployment, and other agents. The repository starts with no commits, so evidence identifies the current working tree rather than a revision SHA.

## Edit order

1. Read the local instructions, policy, `SPEC.md`, plan form/examples, TDD and SDLC feedback skills, review guidance, verifier criteria, existing code, and existing tests.
2. Created `PLAN.md` and this evidence record before product or test edits.

## Commands and observed results

Further commands are appended after they run; planned checks are not recorded as completed.

### Baseline (before test and production edits)

Command: `python3 -m unittest discover -s tests -v`

Exit code: `0`

```text
test_empty (test_pricing.SubtotalTests) ... ok
test_multiple (test_pricing.SubtotalTests) ... ok
test_no_mutation (test_pricing.SubtotalTests) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```

Observed: the existing subtotal suite passes before the new behavior is introduced.

### RED (tests edited; `pricing.py` still unchanged)

Command: `python3 -m unittest discover -s tests -p 'test_pricing.py' -v`

Exit code: `1`

```text
test_pricing (unittest.loader._FailedTest) ... ERROR

======================================================================
ERROR: test_pricing (unittest.loader._FailedTest)
----------------------------------------------------------------------
ImportError: Failed to import test module: test_pricing
...
ImportError: cannot import name 'payable' from 'pricing' (.../pricing.py)

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (errors=1)
```

Observed: test discovery reaches the real module boundary and fails because the specified public function is absent. This is the expected missing-behavior failure, not a fixture, path, or syntax failure. No production file had been edited at this point.

## Edit order (continued)

3. Added the `PayableTests` expectations to `tests/test_pricing.py`.
4. Ran the focused test file and observed the RED import failure above.
5. Added the production implementation to `pricing.py` only after RED.

### GREEN (focused pricing test file)

Command: `python3 -m unittest discover -s tests -p 'test_pricing.py' -v`

Exit code: `0`

```text
test_does_not_mutate_amounts (test_pricing.PayableTests) ... ok
test_floors_discount_before_subtracting (test_pricing.PayableTests) ... ok
test_rejects_percent_outside_inclusive_range (test_pricing.PayableTests) ... ok
test_zero_full_and_empty_boundaries (test_pricing.PayableTests) ... ok
test_empty (test_pricing.SubtotalTests) ... ok
test_multiple (test_pricing.SubtotalTests) ... ok
test_no_mutation (test_pricing.SubtotalTests) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.000s

OK
```

Observed: the unchanged expectations that produced RED now pass with the implementation, including all specified examples and retained subtotal tests.

### Required full regression command

Command: `python3 -m unittest discover -s tests`

Exit code: `0`

```text
.......
----------------------------------------------------------------------
Ran 7 tests in 0.000s

OK
```

Observed: the exact command required by `SPEC.md` passes the combined existing and new suite.

### First final whitespace check

Command: `for f in PLAN.md evidence.md pricing.py tests/test_pricing.py; do git diff --no-index --check /dev/null "$f"; rc=$?; if [ "$rc" -gt 1 ]; then exit "$rc"; fi; done`

Exit code: `3`

```text
PLAN.md:36: new blank line at EOF.
```

Observed and response: the check found an extra blank line at the end of `PLAN.md`. Removed that blank line and corrected the plan's Proof wording to describe this untracked-file check accurately. This repository has no tracked baseline, so ordinary `git diff --check` would not inspect these files.

### Repeated whitespace check

Command: `for f in PLAN.md evidence.md pricing.py tests/test_pricing.py; do git diff --no-index --check /dev/null "$f"; rc=$?; if [ "$rc" -gt 1 ]; then exit "$rc"; fi; done; true`

Exit code: `0`

Output: none.

Observed: no whitespace errors remain in the four files changed or created for this exercise.

### Final verbose regression run

Command: `python3 -m unittest discover -s tests -v`

Exit code: `0`

```text
test_does_not_mutate_amounts (test_pricing.PayableTests) ... ok
test_floors_discount_before_subtracting (test_pricing.PayableTests) ... ok
test_rejects_percent_outside_inclusive_range (test_pricing.PayableTests) ... ok
test_zero_full_and_empty_boundaries (test_pricing.PayableTests) ... ok
test_empty (test_pricing.SubtotalTests) ... ok
test_multiple (test_pricing.SubtotalTests) ... ok
test_no_mutation (test_pricing.SubtotalTests) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.000s

OK
```

Observed: the latest product and test files pass all focused behavior and adjacent subtotal regressions.

## Final self-review

Reviewed the current contents of `SPEC.md`, `PLAN.md`, `pricing.py`, `tests/test_pricing.py`, and this evidence against `REVIEW.md` and the criteria in `selected-skills/agents/sdlc-verifier.md`.

- AC0: `subtotal` remains unchanged and its three original tests pass.
- AC1–AC2: `payable` calls `subtotal`, computes the discount with integer floor division, and subtracts it. Tests cover the exact `1001 @ 10% = 901` oracle plus 0%, 100%, and empty input.
- AC3: both invalid sides (`-1`, `101`) raise `ValueError`; the inclusive endpoints are exercised as valid.
- AC4 and scope: a multi-item list remains byte-for-byte/value-for-value unchanged, production code imports no dependency, and no CLI, web, installation, PR, or deployment work was added.
- TDD evidence: the tests were edited first, the missing public function produced exit code 1, the production implementation followed, and the unchanged expectations then passed.
- Plan alignment: the changed paths, one-change boundary, risks, test strategy, independent oracle, and proof match the implementation. No contract or design discovery required a `SPEC.md` change.

No material bug, security, policy, scope, or evidence finding remains in this bounded working-tree review.

Limitations: the user explicitly prohibited other agents for this exercise, so this is self-review rather than the fresh-context independent verification normally requested by `sdlc-feedback`. The repository has no commits and every file is untracked, so there is no commit SHA, tracked diff base, branch integration result, CI result, or hosted review to verify. Those integration activities are outside the authorized scope.

## Final command snapshot

- Whitespace command: `for f in PLAN.md evidence.md pricing.py tests/test_pricing.py; do git diff --no-index --check /dev/null "$f"; rc=$?; if [ "$rc" -gt 1 ]; then exit "$rc"; fi; done; true`
  - Exit code: `0`
  - Output: none.
- Regression command: `python3 -m unittest discover -s tests`
  - Exit code: `0`
  - Output: seven dots, `Ran 7 tests in 0.000s`, `OK`.
- State command: `git status --short`
  - Exit code: `0`
  - Observed: the repository still has no tracked baseline; all supplied repository content is untracked, including the four files changed or created here (`PLAN.md`, `evidence.md`, `pricing.py`, and `tests/`). No files were staged or committed.
