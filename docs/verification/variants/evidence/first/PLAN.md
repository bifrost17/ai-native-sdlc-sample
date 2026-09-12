# Plan: pricing payable calculation
Upstream: `SPEC.md` in the current working tree (the repository has no commits). Status: draft.

Implement the authorized pricing change as one cohesive local change. The existing `subtotal` function remains the calculation boundary, while `payable` adds the percentage discount contract from `SPEC.md`; no hosted PR, installation, or deployment is part of this exercise.

## Files that change

| Path | Role | Spec reference |
|---|---|---|
| `tests/test_pricing.py` | Add test-first examples, percent bounds, and mutation regression coverage | AC0-AC4 |
| `pricing.py` | Add the minimal `payable(amounts, discount_percent)` implementation | AC1-AC4 |
| `PLAN.md` (new) | Record order, risk, and planned proof | Authorized planning scope |
| `evidence.md` (new) | Record actual commands, outputs, and edit order | Local verification requirement |

## Order of work

This is one reviewable local change; no PR is created. First preserve the three-test baseline with the required discovery command. Add calculation examples first and observe failure because `payable` is absent, then add the smallest calculation implementation and rerun. Add the invalid-percent boundary tests next and observe their behavioral failure, implement `ValueError` validation, then add the non-mutation regression. Finish with the full test command, inspect the complete current files and Git status against `SPEC.md`, and apply the local verifier criteria as a bounded self-review. Because the repository has no commits and every file began untracked, Git cannot provide a pre-change diff baseline.

## Risks

| Risk | Detection | Response |
|---|---|---|
| Percentage arithmetic rounds incorrectly for non-divisible subtotals | `[1001]` at 10% must produce 901 | Use integer floor division before subtraction |
| Validation accepts a percent outside 0 through 100 | Explicit -1 and 101 tests | Validate before calculation and raise `ValueError` |
| New calculation mutates the caller's list or changes `subtotal` | Mutation test plus existing subtotal regressions | Calculate through `subtotal` without modifying the iterable |

## Proof

| ID | Planned evidence | Limit |
|---|---|---|
| P1 AC1-AC2 | Focused tests for the supplied rounding example, 0%, 100%, and empty input using `python3 -m unittest` | Covers specified integer inputs only |
| P2 AC3 | Focused lower- and upper-bound rejection tests | Does not define behavior for non-integer input types |
| P3 AC0, AC4 | Existing subtotal tests, payable mutation test, and final `python3 -m unittest discover -s tests` | Local Python runtime only; no CI or integration target is defined |
