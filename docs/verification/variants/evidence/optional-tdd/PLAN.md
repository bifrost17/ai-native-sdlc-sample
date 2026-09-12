# Plan: pricing payable calculation
Upstream: user-authorized `SPEC.md` working-tree draft (the repository has no commits). Status: draft.
Implement `payable` beside the existing `subtotal`, using the supplied pricing contract and retaining the current public behavior.

## Files that change
| Path | Role | Contract |
|---|---|---|
| `tests/test_pricing.py` | Add contract-derived tests for discount calculation, boundaries, validation, and input preservation. | AC0–AC4 |
| `pricing.py` | Add `payable(amounts, discount_percent)` while preserving `subtotal`. | AC0–AC4 |
| `PLAN.md` (new) | Record the implementation and verification order. | Project policy |
| `evidence.md` (new) | Preserve actual commands, exit codes, outputs, and edit order. | Project policy |

## Order of work
Verification strategy: **TDD**, chosen by the user. Expectations come from `SPEC.md`: `[1001]` at 10% is independently calculated as `1001 - floor(1001*10/100) = 901`; 0%, 100%, empty input, invalid percentages, and unchanged input cover the remaining boundaries.

This is one cohesive local change; no PR, installation, or deployment is in scope.

1. Run the existing suite to establish AC0 behavior.
2. Before production edits, add focused `payable` tests and run them. A missing import/function is the expected meaningful RED.
3. Add the smallest production implementation using integer arithmetic, then rerun the focused and full suite to GREEN.
4. Review the complete working-tree diff against `SPEC.md`, this plan, `REVIEW.md`, and `selected-skills/agents/sdlc-verifier.md`; record the lack of independent-agent review as a limitation required by the exercise boundary.

## Risks
| Risk | Detection | Response |
|---|---|---|
| Floating-point division rounds large totals or computes the wrong floor. | Exact example and boundary tests plus code review. | Use integer floor division: `subtotal * percent // 100`. |
| New behavior mutates the caller's list or changes `subtotal`. | Mutation tests and the existing subtotal regression suite. | Compute from `subtotal(amounts)` without modifying the list. |
| Percentage validation misses either bound. | Tests for `-1`, `101`, `0`, and `100`. | Reject values outside the inclusive 0–100 range. |

## Proof
| Coverage | Check | Expected result / limit |
|---|---|---|
| AC0 | `python3 -m unittest discover -s tests -v` before and after implementation | Existing subtotal tests remain green. |
| AC1–AC4 | Focused `PayableTests`, then the full command above | Example, empty/0/100%, invalid bounds, and no mutation pass. Input types beyond the specified integers are outside scope. |
| Final consistency | Whitespace check over the four changed/new files, working-tree file inspection, and full suite | No material mismatch among spec, plan, implementation, and evidence. Review is self-review only under the explicit no-other-agents constraint. |
