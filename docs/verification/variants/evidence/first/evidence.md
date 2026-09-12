# Implementation evidence

Scope: the user-authorized local pricing change in `SPEC.md`. The repository had no commits at start, so evidence identifies the current working tree rather than a revision SHA. No hosted PR, deployment, installation, or commit was attempted.

## Execution log

1. Before editing `PLAN.md`, tests, or source, inspected `CLAUDE.md`, `PROJECT-POLICY.md`, `SPEC.md`, the plan template and example skill, `selected-skills/skills/sdlc-feedback/SKILL.md`, `selected-skills/skills/tdd/SKILL.md`, `selected-skills/agents/sdlc-verifier.md`, `REVIEW.md`, and the relevant process/Git/PR-size instructions.
2. Baseline command before source or test edits: `python3 -m unittest discover -s tests`
   - Exit code: 0
   - Observed output: `Ran 3 tests in 0.000s` and `OK`.
3. Created `PLAN.md`, then this evidence record. Production source and tests were still unchanged at this point.
4. First behavior edit: added only `PayableTests.test_calculation_examples` to `tests/test_pricing.py`; `pricing.py` was still unchanged.
5. RED command: `python3 -m unittest tests.test_pricing.PayableTests.test_calculation_examples`
   - Exit code: 1
   - Observed output: `Ran 1 test`; all four subcases errored with `AttributeError: module 'pricing' has no attribute 'payable'`; final status `FAILED (errors=4)`.
   - Interpretation: meaningful expected failure because the new public function did not exist, rather than a test setup or expectation error.
6. First production edit: added `payable` calculation to `pricing.py` using `subtotal` and integer floor division; no validation was added yet.
7. GREEN command: `python3 -m unittest tests.test_pricing.PayableTests.test_calculation_examples`
   - Exit code: 0
   - Observed output: `Ran 1 test in 0.000s` and `OK` (the single test contains four independent subcases).
8. Second behavior edit: added only the lower- and upper-percent rejection tests; the calculation-only source remained unchanged.
9. RED command: `python3 -m unittest tests.test_pricing.PayableTests.test_rejects_percent_below_zero tests.test_pricing.PayableTests.test_rejects_percent_above_one_hundred`
   - Exit code: 1
   - Observed output: `Ran 2 tests`; both failed with `AssertionError: ValueError not raised`; final status `FAILED (failures=2)`.
   - Interpretation: meaningful behavioral failure showing both invalid-percent boundaries were accepted.
10. Second production edit: added the inclusive 0-through-100 guard to `pricing.py`, raising `ValueError` outside the range.
11. GREEN command: `python3 -m unittest tests.test_pricing.PayableTests.test_rejects_percent_below_zero tests.test_pricing.PayableTests.test_rejects_percent_above_one_hundred`
    - Exit code: 0
    - Observed output: `Ran 2 tests in 0.000s` and `OK`.
12. Regression-only test edit: added `PayableTests.test_does_not_mutate_amounts` after the implementation already avoided mutation. No production change followed, and no artificial RED was manufactured.
13. Focused regression command: `python3 -m unittest tests.test_pricing.PayableTests.test_does_not_mutate_amounts`
    - Exit code: 0
    - Observed output: `Ran 1 test in 0.000s` and `OK`.
14. Required full regression command: `python3 -m unittest discover -s tests`
    - Exit code: 0
    - Observed output: `Ran 7 tests in 0.000s` and `OK`.

## Final bounded review

- Commands: `git status --short --branch` exited 0 and showed `No commits yet on main` with the entire supplied product copy still untracked; `git diff --check` exited 0 but cannot cover untracked files. `nl -ba SPEC.md PLAN.md pricing.py tests/test_pricing.py` exited 0 and was used to compare the complete current contents. `git diff --no-index -- /dev/null pricing.py`, the equivalent tests command, and the equivalent `PLAN.md` command each exited 1 as expected because each current untracked file differs from an empty file; their full added contents were inspected.
- Spec comparison: AC0 is covered by the unchanged `subtotal` body and its three passing existing tests. AC1-AC2 are implemented through `subtotal`, integer floor division, and subtraction, with the supplied 1001/10 example plus 0%, 100%, and empty-list cases. AC3 has both out-of-range boundary tests and an inclusive guard. AC4 has a passing caller-list equality regression and no new dependency or mutation operation.
- Plan/evidence comparison: final paths and execution order match `PLAN.md`; `SPEC.md`, policy files, and unrelated files were not edited. The two new behaviors have contemporaneous meaningful RED then GREEN output, while the already-GREEN mutation check is identified as regression evidence.
- Review result: no material bug, security, policy, or scope finding in the bounded local change. Input-type validation, nonnegative-amount validation, currency behavior, external interfaces, installation, CI, hosted PR, integration, and deployment remain outside the specified scope.
- Limits: there is no commit or tracked baseline, so a true Git delta cannot be reconstructed from this repository; review used the observed pre-edit source/tests, contemporaneous edit log, and complete final contents. The `sdlc-feedback` skill normally requests a fresh-context verifier, but the exercise expressly forbids delegated review, so this is a self-review against `selected-skills/agents/sdlc-verifier.md`, not independent verification or human approval.

After the final plan/evidence alignment edit, reran `python3 -m unittest discover -s tests`: exit code 0, `Ran 7 tests in 0.000s`, `OK`. No production or test edit followed this confirmation.
