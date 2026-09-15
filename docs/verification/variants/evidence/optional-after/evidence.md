# Implementation evidence

Scope: user-authorized local planning, implementation, automated tests, and verification for `SPEC.md`. No hosted PR, installation, deployment, dependency change, or external agent.

## Observed order and results

1. Read `CLAUDE.md`, `PROJECT-POLICY.md`, `SPEC.md`, `templates/plan.md`, `REVIEW.md`, the simple F01 spec/plan example, `selected-skills/skills/sdlc-feedback/SKILL.md`, `selected-skills/agents/sdlc-verifier.md`, and the current product/tests before editing product code.
2. Baseline check before production-code edit:

   ```text
   command: python3 -m unittest discover -s tests
   exit code: 0
   output:
   ...
   ----------------------------------------------------------------------
   Ran 3 tests in 0.000s

   OK
   ```

3. Created `PLAN.md` and this evidence record before editing `pricing.py`. The selected strategy is implementation first, then automated tests; therefore no RED history is claimed.
4. Edited production code first: added `payable` to `pricing.py`, with the inclusive 0–100 guard, reuse of `subtotal`, integer floor discount calculation, and no write to `amounts`. No test file had been edited at this point.
5. Edited `tests/test_pricing.py` after the production change. Added independent spec-derived expectations for 1001 at 10%, 0%, 100%, empty amounts, -1 and 101 errors, and input-list preservation; retained all existing `subtotal` tests unchanged.
6. First automated check after adding tests:

   ```text
   command: python3 -m unittest discover -s tests
   exit code: 0
   output:
   .......
   ----------------------------------------------------------------------
   Ran 7 tests in 0.000s

   OK
   ```

   Observed: all three original `subtotal` tests and four new `payable` test methods passed.

7. Named-test and syntax checks:

   ```text
   command: python3 -m unittest discover -s tests -v
   exit code: 0
   output:
   test_does_not_mutate_amounts (test_pricing.PayableTests) ... ok
   test_floors_discount_before_subtracting (test_pricing.PayableTests) ... ok
   test_percent_outside_range_raises_value_error (test_pricing.PayableTests) ... ok
   test_valid_percent_boundaries_and_empty_amounts (test_pricing.PayableTests) ... ok
   test_empty (test_pricing.SubtotalTests) ... ok
   test_multiple (test_pricing.SubtotalTests) ... ok
   test_no_mutation (test_pricing.SubtotalTests) ... ok

   ----------------------------------------------------------------------
   Ran 7 tests in 0.000s

   OK

   command: python3 -m py_compile pricing.py tests/test_pricing.py
   exit code: 0
   output: (none)
   ```

8. Working-tree and diff limitation:

   ```text
   command: git status --short --branch
   exit code: 0
   output begins:
   ## No commits yet on main
   ?? PLAN.md
   ?? evidence.md
   ?? pricing.py
   ?? tests/

   command: git diff --no-index -- /dev/null pricing.py
   exit code: 1
   observed output: Git rendered all 13 lines of pricing.py as a new file, including the preserved three-line subtotal implementation and the new payable function.
   ```

   Exit 1 is the documented `git diff --no-index` result when differences exist, not a failed product check. Because this repository has no commits and all files were already untracked at the start, there is no Git base for a normal initial-to-current diff. Review therefore uses the initially observed file contents (three-line `pricing.py`; `tests/test_pricing.py` with three `subtotal` tests) and the current complete files. No commit, stage, push, PR, or deployment was performed.

## Self-review against spec and verifier criteria

- AC0: `subtotal` is byte-for-byte unchanged in the observed source lines, its three original tests remain, and all pass.
- AC1/AC2: `payable` accepts the specified valid domain, calls `subtotal`, floors the discount with `// 100`, and subtracts it. Tests independently assert the supplied 1001-at-10 example plus 0%, 100%, empty, and multi-amount behavior.
- AC3: the inclusive guard rejects -1 and 101 with `ValueError`; both are covered.
- AC4: the function only reads `amounts`; the new multi-element preservation test passes. Imports are standard-library/project-local and no dependency files changed.
- Plan alignment: changed paths, implementation-before-test order, independent expectations, risks, proof, and bounded no-PR/no-deployment scope match the actual work. `SPEC.md` did not require changes because no contract or scope changed.
- Review result: no material bug, security, policy, or scope finding in the current files. Input-type validation, currency conversion, hosted integration, and deployment remain outside `SPEC.md`.
- Limitation: this is the required self-review against `selected-skills/agents/sdlc-verifier.md`; it is not an independent fresh-context verifier review. The exercise expressly forbids other agents. The repository has no commit/main baseline, and project roles, CI, and evidence location remain draft/undecided, so commit, PR, CI, integration-main, and human acceptance cannot be confirmed here.

A final full regression command and file fingerprints follow after this review.

9. Final full regression after review:

   ```text
   command: python3 -m unittest discover -s tests
   exit code: 0
   output:
   .......
   ----------------------------------------------------------------------
   Ran 7 tests in 0.000s

   OK
   ```

10. Reviewed-file fingerprints:

    ```text
    command: shasum SPEC.md PLAN.md pricing.py tests/test_pricing.py
    exit code: 0
    output:
    26fbc7af679788e9dd4919a50d95601cf86659fc  SPEC.md
    1b112179881ef53aa12053309c3e5b748249aca8  PLAN.md
    b69597b8dcacde1d98f7bc4a89e8e7fede7ea9b2  pricing.py
    ea854376bb0e38f39e4752cf245333c7e6b37784  tests/test_pricing.py
    ```
