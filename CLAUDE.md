# intent-sdlc-sample

<!-- L5 414-436: the four sections of the playbook's CLAUDE.md. L5 412: "Keep it under a page" -->

## Commands
- Test: `make test` (python unittest + `bash tests/test_hooks.sh`; healthy: ends with `OK` and
  `hooks: N passed, 0 failed` — ‹exact line filled in by the parent after integration›)
- Evals: `make evals` (`bash evals/run.sh`; healthy: ‹filled in after integration›)
- Check: `make check` (test + evals; non-zero on any failure)

## Conventions
- Prose is English in artifacts; file names, section names and `Status:` words are fixed tokens.
- One chain per change under `intent/<NNNN>-<slug>/` — intent.md, spec.md, plan.md, in that
  order, each its own commit. `Status: draft` until the PR merges; the merge is the approval.
- Every code file under `.claude/hooks/`, `scripts/`, `evals/` opens with the lesson sentence it
  implements, quoted with its line number. No sentence, no file.
- python3 standard library only; bash 3.2 (no `mapfile`, no `declare -A`; `wc -l | tr -d ' '`).

## Architecture
- `.claude/skills/` — what the agent is told (advisory). `.claude/hooks/` + `settings.json` —
  what the machine blocks. `tests/`, `evals/`, `.github/` — what CI proves. See docs/BOUNDARY.md.
- `intent/` — the artifact chains; `templates/` — copies of the skill-embedded templates.
- `docs/PLAYBOOK-MAP.md` maps the 14 lessons to files; `docs/METRICS.md` is git commands.

## Verifying your work

- Build: make build (must finish with "Build succeeded")
- Test: make test (all green; never skip or delete a failing test)
- Lint: make lint (zero warnings)

Run all three before reporting any task complete, and paste the output.
If a test fails, fix the code, not the test.

(L9 635-645 verbatim. This repo has no `make build`/`make lint`; run `make check` and paste it.)

## Things Claude gets wrong
- Writing a checker for artifact sections, status or transitions. The skill says it, the product
  owner reads it, the merge records it. Do not build the machine again.
- Setting `Status: accepted` in a file. Only a merged PR means accepted.
- Pointing a skill or a doc at a script that does not exist. Run `ls` before you cite a path.
