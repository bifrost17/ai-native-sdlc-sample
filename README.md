# intent-sdlc-sample

A small repo that applies the fourteen lessons of Anthropic's "The AI-Native SDLC Playbook"
(Claude Academy) as written — skills that say what to do, a few hooks that block what the lessons
say to block, and an `intent/` folder where each change is recorded as intent → spec → plan.
Unofficial; not an Anthropic project.

## Read in this order
1. `docs/PLAYBOOK-MAP.md` — each lesson, the device this repo uses for it, and which layer it lives
   in (person, tool, skill, or code).
2. `docs/BOUNDARY.md` — what the machine checks, what a skill says, what a person decides, and
   why a checker inside the tree is not an approval authority.
3. `.claude/skills/` — `capture-intent`, `design-spec`, `plan`, `secure-api-review`.
4. `intent/0004-lesson-only/` — the change that made this repo look like this, recorded as its own
   chain. `intent/0001-bootstrap-repo/` is the earlier chain, kept as history in the pre-slim
   convention (frontmatter, status fields); the current template is what 0004 uses.
5. `CLAUDE.md`, `REVIEW.md`, `.claude/agents/verifier.md` — the agent-facing files.
6. `docs/METRICS.md` — the lessons' indicators as git commands.

## What this repo does
- Encodes the intent, spec and plan templates in skills, with `templates/` as copies.
- Keeps the hooks the lessons name as deterministic (protected paths, test protection, secrets,
  format/lint, production gate). A plan-sync hook is optional in L4 329 ("Consider") — this repo
  does not have one.
- Runs `make check` (= `make test`) in CI; a red check is a red PR. Evals need an API key and run
  in their own workflow on config changes and on a schedule (L10 689). Without the
  `ANTHROPIC_API_KEY` secret that job exits 2 and shows red: it did not run, and "did not
  run" is not "passed". Add the secret to make it real.
- Records every change to itself as a chain under `intent/`.

## Chains
| Chain | Kind | Entry path | PR(s) |
|---|---|---|---|
| 0001 bootstrap-repo | record · pre-slim convention | this repo, self-recorded | #12 |
| 0002 claims-status | feature · person | `capture-intent` (person's idea) | #17, #18 |
| 0004 lesson-only | slim | this repo, self-recorded | #16 |
| 0005 ownerless-claim-visible | defect · ticket | GitHub issue | #20, #21 |
| 0006 claims-status-stale-not-found | incident · band | `ops/bands.yaml` → `scripts/detect_bands.py` → auto-draft | #22, #23 |
| 0007 claim-id-trailing-newline | defect · ticket | GitHub issue #24 | #28 |
| 0008 adjuster-claim-status | feature · person | `capture-intent` (person's idea) | #30 |

The ticket path is a GitHub issue — #24 (chain 0007), #25, #26.

## Source of truth
This repo is the source of truth (L4 380 "The repo as the source of truth"). There is no
external system of record — no Jira, no separate requirements tool — for the artifacts under
`intent/`; the commit is the timestamp authority.

## What this repo does not do
- It does not check artifact form, status or transitions in code. Approval is a merged PR;
  a missing section is caught by the skill and by the product owner reading the file.
- It does not enforce policy skills with code unless the lesson names the hook.
- It does not replace the playbook. Quotes are short and cite the line; the original is
  Claude Academy, `courses/ai-native-sdlc-playbook`, Copyright Anthropic.

## Commands
`make test` · `make evals` · `make check` (see `CLAUDE.md` for healthy output).
