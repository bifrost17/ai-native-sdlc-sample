---
name: design-spec
description: Reads an accepted intent.md and the organization's skills and writes spec.md next to it — requirements, design, constraints carried over, open questions answered or carried forward, and flagged concerns for the product owner. Does not write a spec on an intent that is not accepted, does not write plan.md, and does not sign the spec off.
---
# Design spec

> L3 245: "Once the product owner approves the intent.md, Claude takes it and produces a
> requirements and design spec. This is guided by the organization's skills for brand, security,
> compliance, and UX."
> L3 270: "Does the spec solve the stated problem, and are the open questions from intent.md
> answered or carried forward?"
> L3 276: "A human teammate always makes this call, and accepting the spec is what starts the
> plan mode play"

## Before writing
1. Open `intent/<NNNN>-<slug>/intent.md`. **It must be accepted — merged to main.** Accepted is
   a fact about git, not about the file: the `Status:` line stays `draft` forever by design (L2 231,
   the merge is the approval), so do not read it as "not accepted". Check
   `git log origin/main -- intent/<NNNN>-<slug>/intent.md` (a commit there = accepted) or
   `gh pr list --state merged --search <NNNN>`. If the file exists only on a branch, stop and say
   so. No machine checks this; you do. (Two headless runs in the org-skills experiment stopped on
   a merged intent because they read the `Status:` line — `docs/research/spec-command/`.)
2. Enumerate the skills actually available in this session: project-local `.claude/skills/` and
   the session's loaded plugin skill catalog. A directory listing of `.claude/skills/` alone misses
   plugin policy skills. Use the catalog's namespace and actual location; `org-skills/skills/` is
   this repository's plugin source, while an installed copy can live in a cache elsewhere. Do not
   assume that a source directory is installed or that a cached plugin lives under `.claude/skills/`.
   Record apply/skip with a reason for each available skill. If `spec-policy-pass` is available,
   open it and apply its policy procedure with this skill.

   Open every applicable skill's actual `SKILL.md` before naming it under "Skills applied" —
   chain 0007 named one without opening it. Record its source (project path or plugin namespace
   and actual file path) and the version read. For a Git-tracked file, use
   `git log -1 --format=%h -- <actual-path-relative-to-its-repository>` in that repository;
   check for local changes and label them `uncommitted` with the base SHA if known. For an
   organization plugin whose Git history is unavailable (including tool access), read that plugin's own
   `.claude-plugin/plugin.json` or installation metadata and record
   `namespace:skill@<manifest-or-installed-version>` plus its source. For a directory-loaded
   checkout, label the value as the manifest version and note any unverified Git/working-tree state.
   A cache without `.git` does not imply `uncommitted`; never borrow the consuming project's SHA.
   If no version can be verified, say `version-unverified` and why. L3 279 logs "the skill versions
   in force"; a name or guessed SHA cannot identify the file actually read.
3. Record `Upstream: intent.md@<sha>. Status: draft.` at the top of spec.md, and leave it `draft`:
   approval is the merge of the PR that carries the spec (L2 231), nothing flips this line by hand.
   One exception: an engineer may tell you to start on a draft (a single worker stacking PR B on
   the intent PR A). Immediately below the Upstream/Status line, write one line naming who told
   you and why, and repeat it in the PR body — approval is still the merge, not this note.

## Writing
Use `templates/spec.md`, section for section. Three rules carry the lesson:
- **Constraints** — restate every constraint from intent.md, then add any discovered here.
- **Open questions from intent** — each one gets `answered: …` or `carried forward: … (owner)`.
  Never drop one silently.
- **Flagged concerns** — where two policies conflict or a requirement breaches one, say what
  conflicts and who decides. Do not resolve a policy conflict yourself.

## Review question
Show the spec beside the intent and ask the product owner the lesson's question, verbatim:
"Does the spec solve the stated problem, and are the open questions from intent.md answered or
carried forward?"

## What this skill does not do
- Does not write a spec when intent.md is not accepted.
- Does not write plan.md — that is plan mode, after the product owner accepts the spec.
- Does not set the spec to accepted. The product owner signs off; the merge records it.
