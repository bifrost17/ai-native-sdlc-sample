# Independent verifier — 0019 event-driven review candidate

Target: `ai-native-sdlc-sample@893b79e` and E01 product
`ai-native-sdlc-experiments/event-r01@c547048`.

## What I ran

- `make check 2>&1 | tee /Users/jake/Projects/ai-native-sdlc-experiments/human-event-r01/maker-check-final.txt`
  — rc=0. The saved output contains the complete run.
- `printf '%s\n' '{"tool_input":{"command":"scripts/deploy.sh production"}}' | env -u RELEASE_APPROVAL .claude/hooks/production-gate.sh`
  — rc=2, the expected denial for an unapproved production action.
- `claude plugin validate --strict ./org-skills` — rc=0.
- `git diff --name-status main...HEAD`, `git diff main...HEAD -- <planned paths>`, and
  `git status --short` in the sample repository — rc=0. I compared the plan's file list in both
  directions against the committed candidate and inspected the current working tree separately.
- `claude plugin list --json` and the `intent-sdlc-skills` entry in
  `~/.claude/plugins/installed_plugins.json` — rc=0. I also hashed the installed and source copies
  of `sdlc-feedback/SKILL.md` and `sdlc-verifier.md`; both pairs matched.
- `git show --stat --oneline f706c6d`, `git diff --name-status f706c6d..3873db9`,
  `git show --stat --oneline c547048`, and `git merge-base --is-ancestor f706c6d c547048`
  in the E01 product — rc=0, including the ancestor check.
- `python3 -m unittest discover -s tests -v` in the E01 product — rc=0, 12 tests passed.
- `python3 tracker.py --data requests.json summary` and
  `python3 tracker.py --data requests.json summary --owner hana --json` — rc=0 for both.
- `shasum -a 256 requests.json` before and after the product checks — rc=0 and identical:
  `c038196ad9f748e482a446e4025e4c6c0746b23942c39f5f457ad37dd9a53795`.

## What I saw

No unexpected failing line occurred. The sample `make check` completed with 96 unit tests passing
(one skipped), `test_hooks: 28 passed, 0 failed`, `8 passed, 0 failed` for the deterministic eval
harness, and `PASS  managed-settings 키·훅 계약`. The expected hook denial was:

> `[production-gate.sh] BLOCKED: Production deploys need a release authorization.`

The plugin validates strictly and the enabled user installation is version `0.1.4` at
`~/.claude/plugins/cache/intent-sdlc-skills/intent-sdlc-skills/0.1.4`, recorded at candidate SHA
`893b79e`. Its installed skill and agent hashes match the source candidate.

The shared-criteria simplification is internally consistent. The developer skill reads the
`Review criteria` section from the plugin's agent file; the native agent receives the same section
as part of its own definition, so the caller no longer has to discover or pass a separate criteria
file. The removed `references/review-criteria.md` has no remaining reference. Reviewer-only
restrictions are not copied into the developer skill.

The agent boundary matches the spec: `model: opus`, `effort: high`, `maxTurns: 20`, tools
`Read, Glob, Grep, Bash`, and `disallowedTools: Edit, Write, Agent, Skill`. Its body explicitly
limits Bash to inspection and verification and retains parent permissions; it does not claim Bash
is intrinsically read-only. The ordinary developer guidance remains Sonnet with effort selected by
task difficulty. No files under `templates/`, `.claude/skills/`, or the existing project
`.claude/agents/verifier.md` changed, so this remains an optional organization plugin rather than a
new requirement in the adopting template.

For E01, `f706c6d` records R8/AC9. Its descendant `3873db9` changes `tracker.py`,
`tests/test_tracker.py`, `README.md`, and `plan.md` together; that plan points exactly to
`spec.md@f706c6d`. The final `c547048` changes only the README title, an unaffected prose correction.
The original product tests remain present, all 12 current tests pass, manual text output is
`open\t3` then `done\t1`, JSON owner output is `{"open": 1, "done": 1}`, and the fixture hash is
unchanged.

## What does not match plan.md

No discrepancy was found in the completed plugin `0.1.4` slice or the completed E01 product slice.

The full 0019 plan is not complete at this snapshot. These planned delivery files are not yet in
`main...893b79e`: `docs/experiments/0019-event-review-skill.md`, the corresponding update to
`docs/experiments/README.md`, `docs/verification/north-star-playbook.html`, `INDEX.md`, and
`CHAPTERS.md`. Consequently `org-skills/README.md` currently links to an experiment record that is
not present yet. This is an outstanding finalization item, not evidence that the implemented
plugin/E01 behavior contradicts the accepted spec.

During inspection the sample working tree gained uncommitted E02/final-record edits, including
`docs/experiments/datasets/v5/cases.json`, `docs/experiments/README.md`, and `README.md`. I treated
them as concurrent root work and did not change or grade them as part of candidate `893b79e`.

## What I could not check and why

- E02's rerun, correction, renewed acceptance, and same-commit result are still in progress, so I
  could not confirm AC2/AC3 for that controlled omission case or the final `0.1.4` evidence record.
- The final north-star annotations, 179-ID preservation result, experiment index, and chapter/index
  totals do not yet exist in this candidate and require a final check after root writes them.
- I did not rerun a paid Claude session. E01's preserved trace reports a Sonnet parent, one native
  `intent-sdlc-skills:sdlc-verifier`, and an Opus child, but this review independently confirmed the
  resulting repository state rather than treating that trace as a new live invocation.
- I did not verify hosted PR/CI integration, organization permissions, or human merge approval;
  they are outside this local candidate and remain explicitly outside the plugin's authority.
