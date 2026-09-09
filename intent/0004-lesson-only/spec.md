# Spec: keep only what the lessons name as code (from intent 0004-lesson-only)
Upstream: intent.md@eb9e63dafb081391a0892be80e50265710deb192. Status: draft.
Skills applied: none — this change has no external-facing endpoint; the skills it writes are its output.
## Requirements
- R1 Each artifact template is embedded in the skill that produces it; `templates/` holds copies.
- R2 The rules the lessons put in a skill are stated by a skill, not checked by code: an
  unaccepted intent gets no spec (L3 245); status stays draft until the merge (L2 229).
- R3 Only hooks a lesson names stay, wired in `.claude/settings.json` (lane A).
- R4 CI runs `make check`; a red check is a red PR (lane C).
- R5 Every code file opens with the lesson sentence it implements, with the line number.
- R6 One document maps the 14 lessons to device, file and layer; one states the boundary.
- R7 Indicators are git commands, not a script.
- R8 The tree stays ≤ 2,500 lines; this change is itself a chain under `intent/`.
## Design
Three lanes, disjoint files: A owns hooks, Makefile, scripts and tests; B owns skills, agents,
docs, templates and chains; C owns CI. The shared contract is `make test` / `make evals` /
`make check`. Nothing in B's files runs as code except one unittest that keeps the skill's
embedded template and `templates/intent.md` identical (R1).
## Constraints
- From intent: no code that checks artifact form, status or transitions (author's decision).
- From intent: hooks the lessons name stay; standard library and bash 3.2 only; short quotes.
- Discovered: `secure-api-review` is kept verbatim, so its last line cites a script path this
  repo does not have; that is a known gap, not a hidden one (see Flagged concerns).
## Open questions from intent
- `secure-api-review` last line → carried forward: the product owner decides at merge whether
  to keep the verbatim line or strike it with a note.
- NOTICE lines after the trim → answered: three MIT sources remain (jcuervo, imsungbin,
  bashebr); the others contributed only to code that is now removed.
## Flagged concerns
- F1 The skill example says "Run scripts/check-endpoints.sh"; the repo has none. Keeping the
  line as printed is faithful to L6; dropping it is honest to the tree. Decider: product owner.
## Out of scope
Hooks, Makefile, CI, evals (lanes A and C). Managed settings and the managed review service.
## Acceptance criteria
- AC1 → R1 `tests/test_skill_template.py` is green, and red when the template is edited.
- AC2 → R2 the three skills each contain a "What this skill does not do" section.
- AC3 → R5 `grep -L 'L[0-9]* [0-9]'` over code files returns nothing (parent runs at integration).
- AC4 → R6,R7 `docs/PLAYBOOK-MAP.md`, `docs/BOUNDARY.md`, `docs/METRICS.md` exist within budget.
- AC5 → R8 `git ls-files | xargs wc -l` ≤ 2,500 after the three lanes merge.
