# Release controls phase-one independent verification

Pinned maker: `88b367baef0bfe0a9f7dc8b382b3b16243eff7cb` on `codex/release-controls`.
Actual dependent base: `65a509ac8c270bbffcdf9d517f656f4040afc363`.
Pinned adopter: `f89a92a354736474fe5676c52c62f2868c2e2a04`, based on
`82d7ad20128399c51492503db0788167cf774a8c`.

## What I ran

- `make check` — rc 0. Full output: [01-make-check.log](01-make-check.log).
- `make evals` — rc 2. Full output: [02-make-evals.log](02-make-evals.log).
- `printf '{not json' | /bin/bash .claude/hooks/production-gate.sh` — rc 2, the expected
  fail-closed result. Full output: [03-hook-bad-input.log](03-hook-bad-input.log).
- `/tmp/intent-form-validation-venv/bin/python /Users/jake/.codex/skills/.system/skill-creator/scripts/quick_validate.py .claude/skills/design-spec`
  — rc 0.
- `/tmp/intent-form-validation-venv/bin/python /Users/jake/.codex/skills/.system/skill-creator/scripts/quick_validate.py .claude/skills/plan`
  — rc 0. Both full outputs: [04-maker-skill-validation.log](04-maker-skill-validation.log).
- `ruby -ryaml -e '...'` over both maker and both adopter changed `SKILL.md` frontmatters — rc 0.
  The exact files, parsed mappings and command result are in
  [05-frontmatter-parse.log](05-frontmatter-parse.log).
- `git diff --name-status 65a509a..88b367b`, `git diff --name-status 064c785..65a509a`,
  and `git -C /Users/jake/Projects/ai-native-sdlc-use-0023 diff --name-status 82d7ad2..f89a92a`,
  followed by explicit allow-list and forbidden-boundary filters — rc 0. Full commands and outputs:
  [06-scope-boundaries.log](06-scope-boundaries.log).
- Base-aware `git diff --unified=3` comparisons of the maker and adopter release deltas — rc 0.
  Full patches: [09-base-aware-delivery-delta.log](09-base-aware-delivery-delta.log).
- A one-off read-only Python resolver over local Markdown links in maker/adopter changed files — rc 0;
  57 local links checked, zero broken. Output: [10-local-links.log](10-local-links.log).
- `git merge-base --is-ancestor main 65a509a` and
  `git merge-base --is-ancestor 65a509a 88b367b` — both rc 0. Snapshot:
  [11-phase1-snapshot.log](11-phase1-snapshot.log).
- `rg -n -C 4 'allowed_properties' /Users/jake/.codex/skills/.system/skill-creator/scripts/quick_validate.py`
  — rc 0. Output: [12-codex-validator-scope.log](12-codex-validator-scope.log).

An initial zsh helper intended to compare full maker/adopter files did not split path pairs and printed
`diff: ... No such file or directory`; its wrapper returned rc 0 because each exploratory diff was allowed
to continue. I disregarded that output, preserved it in [07-maker-adopter-diffs.log](07-maker-adopter-diffs.log),
and ran explicit corrected diffs in [08-maker-adopter-diffs-corrected.log](08-maker-adopter-diffs-corrected.log).

## What I saw

`make check` had no failing line. It reported:

```text
Ran 96 tests in 31.159s

OK (skipped=1)
```

It then reported `test_hooks: 28 passed, 0 failed`, deterministic eval fixtures `8 passed, 0 failed`,
and `PASS  managed-settings 키·훅 계약`.

The semantic eval command did not run an eval. Its first result line was:

```text
SKIP: ANTHROPIC_API_KEY 없음 — evals 는 돌지 않았다(rc=2, 통과 아님)
```

The deliberately malformed hook input changed no files and was blocked:

```text
[production-gate.sh] BLOCKED: hook input is not valid JSON; refused. Route: run the hook with a Claude Code PreToolUse/PostToolUse JSON on stdin.
```

Both changed maker skills passed the requested Codex quick validator. All four maker/adopter
frontmatters parsed as YAML. The adopter skills retain `disable-model-invocation: true`. That key is
supported by the adopter's Claude skill format and is not a defect. The Codex quick validator is not
an appropriate validator for that Claude-only key: its allow-list contains only `name`, `description`,
`license`, `allowed-tools`, and `metadata`.

The maker diff contains 15 committed paths. Every path is covered by the plan's declared document,
template, skill/reference, research, or chain-artifact scope. It changes no path under `tests/`, `evals/`,
`scripts/`, or `.claude/hooks/`, and adds no `.py`, `.sh`, `.js`, or `.ts` checker. The previous 0022
own diff `064c785..65a509a` also has no path outside its own plan categories.

The adopter diff contains exactly 12 policy, documentation, template, and optional example-skill paths.
It contains no active `.claude` configuration, experiment material, product source, tests/evals, intent
chain, or research records. Base-aware comparison shows the release-control changes are carried across;
full-file differences such as the Korean adopter `REVIEW.md`, `References applied` in its spec template,
and the shorter optional design example predate this release delta or are required by adopter packaging.

Local `main` (`5d67b0f`) is an ancestor of the declared base, and that base is an ancestor of the maker
head. Thus the pinned result includes the available local-main history plus the dependent 0022 work.

## What does not match plan.md

None in the committed phase-one maker slice, the previous 0022 neighboring own diff, or the pinned
adopter delivery boundary.

This is not a verdict that the whole 0023 plan is complete. At the final snapshot, `README.md` and
`docs/research/release-controls/README.md` had tracked working-tree edits beyond the pinned maker head,
and probe/review/verification records were untracked. The plan also reserves final research, handoff,
experiment, and north-star evidence for later work. Those are future or in-progress parts, not missing
files from this pinned phase-one candidate.

## What I could not check and why

- I did not inspect or make any claim about the ongoing runtime experiment, per the verification brief.
- Semantic evals were unavailable because `ANTHROPIC_API_KEY` was absent; rc 2 is a skip, not a pass.
- I did not run Claude CLI, install anything, use the network, fetch a remote main, open a hosted PR/CI
  run, merge, deploy, or observe production behavior.
- This report is pinned to the two stated commits. Concurrent working-tree material, including later
  research and runtime records, is outside this verdict and requires the planned follow-up verification.
