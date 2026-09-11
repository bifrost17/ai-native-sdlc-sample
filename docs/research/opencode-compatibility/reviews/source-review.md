# OpenCode 1.18.30 migration: source-side skill review

Scope: read-only review of `org-skills/skills/*/SKILL.md`, `org-skills/agents/sdlc-verifier.md`, `org-skills/commands/spec-policy.md`, and the three authoring skills under `.claude/skills/`. This report does not assert OpenCode discovery syntax; the parent review is checking that separately. No install, global config, active skill, or repository file was changed.

## Decision

Do not install the Claude plugin tree wholesale. Most skill bodies are portable Markdown, but three distinct artifacts are mixed together: portable skill directories, a Claude-specific agent/command layer, and project-local authoring skills. Package them separately and adapt only the platform contracts.

## Straightforward directory copies

Copy the whole named directory, not only `SKILL.md`, so local references and license/provenance files stay with it.

- `brand`: body is platform-neutral (`org-skills/skills/brand/SKILL.md:1-30`). It expects the consuming project to provide `PROJECT-POLICY.md` P1 (`:11-12`). Its checker is explicitly only an example outside the skill directory (`:29-30`), so do not turn that script into a new automatic gate.
- `data-compliance`: platform-neutral policy body (`org-skills/skills/data-compliance/SKILL.md:1-36`). It expects `PROJECT-POLICY.md` P2/P3 (`:11-12`) and names sibling policies by logical skill name (`:17`, `:35`), not a Claude tool contract.
- `secure-api-review`: platform-neutral and intentionally advisory (`org-skills/skills/secure-api-review/SKILL.md:1-27`). The absent `scripts/check-endpoints.sh` is documented as deliberately removed (`:24-27`); do not manufacture or bundle a checker.
- `spec-policy-pass`: body is portable (`org-skills/skills/spec-policy-pass/SKILL.md:1-58`). Its provenance record asks for a namespace and manifest/installed version (`:23-26`); change that wording only if the OpenCode package has a different source/version identity.
- `tdd`: platform-neutral procedure (`org-skills/skills/tdd/SKILL.md:1-44`). The model/effort sentence is capability-neutral (`:43-44`) and does not declare a platform model.
- `stop-slop-ko`: self-contained content; frontmatter adds ordinary `metadata` fields (`org-skills/skills/stop-slop-ko/SKILL.md:1-16`). Preserve its provenance/license material with the directory.
- `accessibility`: the main body and its two local references are portable (`org-skills/skills/accessibility/SKILL.md:1-8`, `:196`, `:239`, `:267`, `:338`, `:342`, `:397`, `:401`, `:430`, `:463-464`). One optional cross-skill link is missing; see below.
- `secrets-scan`: portable if the entire directory is copied because it requires `plays/secrets-scan.md` and `templates/finding.md` (`org-skills/skills/secrets-scan/SKILL.md:9`, `:34`). Scanner binaries are optional runtime dependencies with a documented manual fallback (`:13-18`), not package dependencies.

## Adapter needed

### `pr-loop`

- Claude frontmatter permissions use `allowed-tools` plus Claude tool names and per-command Bash matchers (`org-skills/skills/pr-loop/SKILL.md:4-5`). Map or remove this only after the OpenCode permission contract is known; copying it does not by itself preserve the guardrail.
- Claude command interpolation appears as `!\`...\`` pre-execution and `$ARGUMENTS` (`:18-22`). These must become the OpenCode command argument/preload mechanism or ordinary instructions that run after invocation.
- The fallback explicitly reads `CLAUDE.md` (`:56`); an OpenCode adapter should read the active project instruction file(s) without renaming the team's policy source globally.
- The remaining `gh` workflow is ordinary shell/GitHub CLI logic (`:42-108`) and can be retained. It requires authenticated `gh` and write authority when actually invoked, which is a runtime precondition, not an install action.

### `sdlc-feedback` plus `sdlc-verifier`

- The skill reads `../../agents/sdlc-verifier.md` (`org-skills/skills/sdlc-feedback/SKILL.md:7-10`). That path works only while a package preserves `skills/<name>` and sibling `agents/`; copying only the skill directory breaks it. Either keep a package-relative companion resource or copy the Review criteria into an OpenCode agent definition and link that exact installed location.
- Completion delegation names a Claude plugin-qualified agent, `intent-sdlc-skills:sdlc-verifier` (`:37-39`). Replace the namespace/call mechanism; preserve the fresh-context, wait-for-result, findings-only semantics (`:37-49`).
- The prose names Claude model families Opus/high and Sonnet (`:51-54`). Treat these as intent (`consequential cross-artifact review` versus ordinary work), then choose available OpenCode model/effort in the adapter. Do not retain model-brand names as if OpenCode resolves them.
- The verifier frontmatter is Claude agent schema: `tools: Read, Glob, Grep, Bash`, `disallowedTools: Edit, Write, Agent, Skill`, `model: opus`, `effort: high`, `maxTurns: 20` (`org-skills/agents/sdlc-verifier.md:1-9`). All six execution controls need an OpenCode agent/permission equivalent; a Markdown copy alone does not enforce read-only behavior.
- The body explicitly warns that Bash can mutate despite omitted edit tools (`:15-20`). Preserve this semantic guardrail in addition to platform permissions.
- It reads `CLAUDE.md` and `REVIEW.md` (`:28-31`). Keep `REVIEW.md`; adapt the instruction-file lookup to the actual developer CLI/project contract.

### `spec-policy` command

- This is a Claude custom command, not a skill directory. Its `argument-hint` frontmatter (`org-skills/commands/spec-policy.md:1-4`) and positional `$1` (`:17`) need the OpenCode command schema/argument variable.
- Its prompt can remain intact (`:5-21`). It composes `design-spec` and `spec-policy-pass` by logical name (`:5`, `:19`), so both must be discoverable in the same experiment or the command should report that limitation.

### `to-questionnaire`

- The body is portable, but `disable-model-invocation: true` is a Claude invocation-control field (`org-skills/skills/to-questionnaire/SKILL.md:1-5`). Map it to an explicit-only OpenCode mechanism if one exists; otherwise install only as an optional manually invoked skill and document that auto-invocation suppression is not enforced.

### `ux-copy`

- Claude-style command affordances appear in `argument-hint`, `/ux-copy`, and `$ARGUMENTS` (`org-skills/skills/ux-copy/SKILL.md:1-4`, `:7`, `:13-17`). Rewrite as OpenCode invocation/arguments or remove the usage snippet.
- `~~knowledge base` and `~~design tool` are Anthropic plugin connector placeholders (`:93-101`), not executable tool names. Either adapt them to available connectors or omit the connector section; the copy-writing core (`:19-91`) is independent.
- Its link is wrong even in the source tree: `../../CONNECTORS.md` (`:9`) resolves to absent `org-skills/CONNECTORS.md`, while the file is `org-skills/skills/ux-copy/CONNECTORS.md`. Correct to `CONNECTORS.md` in any experimental package.

### `grilling`

- The interview body is portable, but it requires dispatching a sub-agent for environmental facts (`org-skills/skills/grilling/SKILL.md:24-26`). If the OpenCode setup cannot guarantee sub-agent dispatch, soften this to the available exploration mechanism instead of silently promising concurrency. The user confirmation gate (`:28`) is semantic, not platform syntax.

## Project-local authoring skills

These are suitable for a project-local OpenCode experiment, not a global team package. Their same-directory resources must move with them, and their `../../../...` links assume the skill remains three levels below this repository root.

- `capture-intent`: frontmatter is only `name`/`description` (`.claude/skills/capture-intent/SKILL.md:1-4`); quoted mentions of Claude are source quotations, not tool calls (`:7-10`). Copy its `examples/` directory (`:69-71`). It also depends on repository-root `templates/intent.md` and `tests/test_skill_template.py` (`:31-32`), both present in this checkout, so a global install would lose its intended project context.
- `design-spec`: copy both `references/` files (`.claude/skills/design-spec/SKILL.md:20`, `:24`). Its repository-root template and example links (`:23`, `:43-45`) are present and remain correct only at equivalent project-local depth. `references/skill-provenance.md:9-11` specifically names `.claude-plugin/plugin.json` and `namespace:skill`; adapt this provenance example to the OpenCode package/version evidence used by the experiment.
- `plan`: copy `references/execution-depth.md` (`.claude/skills/plan/SKILL.md:37`). Repository-root policy, template, and examples are linked at `:13`, `:16`, `:44-46`; equivalent project-local depth preserves them. Lines `:33-35` are maker-repository-specific protected-fix behavior and are a reason not to publish this authoring skill as a generic global skill.

## Broken or optional resource assumptions

- `accessibility` links to missing sibling `../web-quality-audit/SKILL.md` (`org-skills/skills/accessibility/SKILL.md:462`). Remove that optional link or install that separate skill intentionally; do not make it an implicit dependency. The required local `references/WCAG.md` and `references/A11Y-PATTERNS.md` exist (`:463-464`).
- `secrets-scan/templates/finding.md:30` says `data/opencre/README.md` is bundled, but no such directory exists under `org-skills/skills/secrets-scan/`. Drop that sentence or add an explicitly reviewed resource later; it is not needed for the basic scan workflow.
- `accessibility` suggests `npm install @axe-core/cli -g` (`org-skills/skills/accessibility/SKILL.md:413-417`). That is an execution-time optional tool install and should never run as part of skill installation.
- `brand`'s example checker lives outside its skill directory (`org-skills/skills/brand/SKILL.md:29-30`). Keep it as an example only, matching the team's no-new-checker decision.
- `secure-api-review` records that its upstream example checker is absent by product-owner decision (`org-skills/skills/secure-api-review/SKILL.md:24-27`). Preserve that decision.

## Claude-only packaging assumptions

- The current package manifest is `org-skills/.claude-plugin/plugin.json:1-10`; the marketplace entry points at `./org-skills` in `.claude-plugin/marketplace.json:7-13`. Neither describes an OpenCode package.
- Installation documentation invokes only `claude plugin validate/marketplace/install/update/list` (`org-skills/README.md:6-27`) and documents Claude-qualified slash names (`:38-41`, `:51-53`, `:61-65`). Reuse none of those commands for the OpenCode experiment.
- Provenance and license files are distribution material even when not read at runtime. A copied third-party-derived skill directory should retain them.

## Minimal packaging proposition

1. Create an isolated OpenCode experiment source, outside active/global config, with one directory per adopted skill. Preserve each complete skill directory and record the source commit; do not modify `org-skills/` or `.claude/skills/` during the first test.
2. Start with the low-risk org-specific core: `brand`, `data-compliance`, `secure-api-review`, `spec-policy-pass`, and `tdd`. Add `sdlc-feedback` only together with a verified OpenCode verifier adapter. This keeps policy thin and does not add an automatic checker.
3. Keep the three authoring skills as a separate project-local set because they rely on this repository's templates, docs, examples, acceptance process, and maker-specific fix workflow.
4. Keep third-party/general utilities (`accessibility`, `grilling`, `pr-loop`, `secrets-scan`, `stop-slop-ko`, `to-questionnaire`, `ux-copy`) as explicit opt-ins. `pr-loop`, `to-questionnaire`, and `ux-copy` need adapters before a meaningful invocation test; the others can be copied with the resource caveats above.
5. Validate discovery and explicit invocation first. Then test one natural trigger separately. For `sdlc-feedback`, test fresh-context delegation, wait behavior, read-only enforcement, current diff/untracked coverage, and returned findings before calling it compatible. Do not infer compatibility from a skill name appearing in a list.
