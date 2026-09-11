# Claude Code fable result

Filtered CLI export; private reasoning omitted. Final result below is verbatim.

**PASS** for candidate `529e440826eda29572976e0ffcafb936816d8b50453ff17d053f70d2728c1590`, maker 8248910 and adopter 82d7ad2, 22 files. No Important regression against my R1 judgment. Every R1 finding is either corrected or explicitly accepted as style, and no correction added a checker, state engine, size cap or mandatory skill.

## What changed and how it holds

- **Baseline path and pin explanation.** Both `context.md` copies now cite docs/experiments/datasets/v1/baseline at line 10, which exists, and lines 19-20 state that the example Upstream pin stands for the linked contract while a real plan pins the product's real spec.md and accepted SHA. Both copies share one hash and read identically.
- **Fix-mode sequencing.** `.claude/skills/plan/SKILL.md:40-41` now says to write and commit the reproduction test before the fix session starts with the fix variable, because the hook also blocks creating new tests. That matches the hook's behaviour I read in R1. The adopter skill keeps its generic wording and is unchanged.
- **Verifier and chain documents.** `.claude/agents/verifier.md:16-17` checks the chain's own artifact revisions for consistency and no longer implies a plan must list its own filename. The slice and future-test rules from R1 are intact.
- **Review pass scoped to the slice.** `REVIEW.md:12-13` matches the change to spec and plan for this PR's declared slice and says future PR work is not missing from it. The rest of the file is unchanged.
- **Lesson map acceptance wording.** `docs/PLAYBOOK-MAP.md:13` now describes stage acceptance as the document SHA plus human decision per GIT-WORKFLOW, separate from final merge, and lists GIT-WORKFLOW as a file with person as a layer.
- **Spec and plan name the linked corrections.** Spec R7 at line 19 now covers verifier, REVIEW and lesson map. The plan repins to spec.md@1ab184e at line 2 and lists the two files with the reason at lines 12-13. That follows the skill's own rule of committing the upstream decision before repinning.
- **Unchanged files.** I re-read every candidate file whose manifest hash did not change: the four example plans, the two-PR spec input, execution-depth, templates/plan.md in both roots, the adopter README and the adopter skill. All read identically to R1. The adopter tree has the same file list as before, no `.claude/` directory, and the adopter skill keeps `disable-model-invocation: true`.

## Nonblocking notes and limits

- `README.md:159-160` still says the engineer's next prompt is the acceptance in headless plan mode, citing chain 0008. It describes tool mechanics from a past run, but it sits in the Commands section and can be read against the skill's statement that plan mode is not approval evidence. One clause pointing to the GIT-WORKFLOW decision record would close it. README is already in the 0022 plan's file list.
- `docs/METRICS.md:28-30` compares one PR's diff to the whole Files that change list. For a multi-PR plan that reads as a mismatch unless taken per slice. A few words would align it. It is a measurement note, not a gate.
- The design-spec example contexts at `feature/context.md:19` and `bug/context.md:19` keep the short dataset path. The plan context now gives the full path, so a reader can resolve it. That is 0021 scope.
- `context.md:21-22` has a stray line break. Style only. The uncommitted change to alternative-feature.md is a one-word typo fix and is outside the candidate.
- Header suffix in `templates/plan.md:1` is unchanged and accepted as style.

Hash-check limits: I recomputed no SHA256 values. I confirmed the manifest's combined hash equals the supplied string and the maker head equals the branch snapshot. The adopter head and the contents of commits 1ab184e and 8248910 are unverified. Content equality for unchanged entries rests on re-reading, not hashing. I did not open the probe folder or any other reviewer's report, and nothing was executed.

Files read this round: `reviews/candidate-r2.json`, `review-r2-request.md`, maker `.claude/agents/verifier.md`, `.claude/skills/plan/SKILL.md`, `.claude/skills/plan/examples/context.md`, `REVIEW.md`, `docs/PLAYBOOK-MAP.md`, `intent/0022-plan-form/{spec,plan}.md`, `docs/METRICS.md` lines 18 to 37, `plan-design/alternative-feature.md`, the eight unchanged maker candidate files, all ten adopter candidate files, plus greps for stale acceptance wording and the baseline path and a listing of the adopter tree.
