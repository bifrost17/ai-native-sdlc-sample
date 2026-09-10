# H02/H03 review-only matrix

This is a review-only reconstruction using the installed runtime reviewer. It is not a rerun
of the original F02 experiment and does not test the automatic-resume controller.

- Baseline: `d22a9fe2f0d3bc5ea367ab6fd99545a347d90404` (the setup commit applying template candidate `80e90016a6b507d98d563e6abcdbbf56aecdca41`).
- H02: natural historical omission reconstructed by applying the original turn-02 diff; verdict `revise`.
- H03: the same omission plus meaningless comments in spec.md and plan.md; verdict `revise`.
- Both reviewers used Sonnet/low, no tools, no session persistence, and separate reviewer sessions.
- `manifest.json` records source, runtime, prompt, and evidence hashes.
