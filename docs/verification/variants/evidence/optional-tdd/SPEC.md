# Pricing change
Owner: user supplied specification. Status: draft.
This bounded exercise is authorized to plan, implement and verify; no hosted PR, installation or deployment.
AC0 Preserve subtotal(amounts) and existing tests.
AC1 Add payable(amounts, discount_percent) for a list of nonnegative integer amounts and integer percent.
AC2 Compute discount as floor(subtotal * discount_percent / 100), then subtract it from subtotal.
Example: [1001] at 10 gives 901; 0 percent leaves subtotal; 100 percent gives 0; empty list gives 0.
AC3 Percent below 0 or above 100 raises ValueError.
AC4 Do not mutate amounts. No new dependencies.
Outside scope: currency conversion, other input types, CLI/web/installation/PR/production use.
Use python3 -m unittest discover -s tests for local checks.
