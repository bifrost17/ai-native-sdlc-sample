---
name: localize-naturally
description: Localize product UI and locale resources with natural wording, preserved placeholders and ICU structure, project terminology, and layout checks. Use for translation and multi-locale synchronization.
---

# Localize Naturally

Create equivalent local experiences, not sentence-shaped copies of the source language.

Use for localization and locale-file synchronization. No other skill or external model is required. Read [setup and examples](references/setup.md) for dependencies and a first check.

## Establish the contract

Before writing:

1. Identify the source of truth, target locales, audience, region, surface, and product tone.
2. Search the current project for `docs/本地化风格与术语.md`, `LOCALIZATION_STYLE.md`, `localization-style.md`, or an equivalent project glossary. Read the relevant file completely when it exists.
3. Inspect available decisions in the current task and relevant project notes for wording the user explicitly approved, rejected, or corrected. Treat the latest explicit decision as part of the contract; do not reintroduce rejected terminology or undo a deliberately retained choice just because another wording sounds smoother.
4. Separate fixed interface copy from product data, customer content, legal facts, and internal implementation strings.
5. Lock factual invariants before naturalizing: names, quantities, negation, currencies, dates, release state, availability, conditions, permissions, privacy boundaries, and transaction responsibilities.
6. If the source meaning is ambiguous, inspect surrounding UI or code. Ask only when different interpretations would materially change the result.

Do not send private product, customer, health, account, or payment data to an external translation service unless the user explicitly authorizes that transfer.

## Load only the affected locale guidance

Use [references/locale-profiles.md](references/locale-profiles.md) to select the affected language/region profiles. The 12 available profiles cover English, Simplified/Traditional Chinese, Japanese, Korean, Spanish, French, German, Brazilian Portuguese, Italian, Russian, and Arabic. Read only the profiles in scope. A language example never narrows a request for all supported locales.

Keep locale-specific guidance separate from project facts. A source project's preferred pronoun, typography, brand glossary, or marketing tone is not a universal language rule. Maintain project terminology by meaning and surface using [references/terminology-context.md](references/terminology-context.md). Do not label existing resource text as human-approved without evidence.

## Write for the destination locale

For each target locale:

1. Restate the intended meaning in plain terms before translating difficult copy.
2. Write the phrase a competent local product team would naturally use in that context.
3. Match the local register and regional variant. Do not preserve source-language word order, metaphors, politeness, capitalization, or punctuation when local usage differs.
4. Keep the product's confidence level. Do not make restrained copy more promotional, uncertain copy more definite, or advisory copy sound like a guarantee.
5. Prefer familiar local product terminology over dictionary equivalence. Keep approved brand terms when the project profile requires them.
6. Translate the user outcome, not internal implementation. Buttons should describe the action or result.

Keep lifecycle states distinct. For example, review approval, release submission, rollout, listing visibility, availability, installation, and successful download are different facts. Never turn an earlier state into a later one without evidence.

Before drafting launch or status copy, write down the **currently verified state**. Every ready-to-use draft must describe that current state. Do not make a future post-release version the primary deliverable when only review approval or release preparation is known. If a future-state template is useful, place it after the current-state draft, label its activation condition, and do not invite download or update until the store page and download path are actually verified. Scan the delivered body for later-state claims; a closing self-check cannot cancel a contradiction in the draft itself.

Never claim that AI output was reviewed by a native speaker unless a real qualified reviewer completed that review.

## Protect layout and interaction

- Treat buttons, tabs, navigation, chips, and fixed controls as layout contracts.
- Keep icon and arrow slots fixed so long labels cannot move, shrink, or displace them.
- Shorten to the most natural compact expression before reducing font size.
- Keep stable control dimensions across locales unless the user approves a layout change.
- Allow body copy to wrap or scroll naturally.
- Check long compound words, CJK line breaks, Arabic RTL, mixed numerals, and native language names.
- When UI is in scope, verify the affected desktop and narrow mobile surface instead of checking locale files alone.

## Apply risk gates

Require explicit facts and flag unresolved uncertainty for:

- legal, privacy, consent, age, data retention, and cross-border processing;
- pricing, subscriptions, quotas, taxes, currencies, refunds, and payment obligations;
- health, safety, identity, authentication, and permissions;
- provenance, authenticity, investment value, guarantees, rankings, and superlatives.

Do not invent a legal entity, office, seller relationship, service region, certification, guarantee, or professional conclusion to make a translation sound smoother.

For legal, medical, financial, or high-spend campaign copy, deliver the best localized draft and mark it for qualified human review.

## Synchronize the real locale set

When shared user-visible copy changes:

1. Determine the locales actually supported by the product.
2. Update every supported locale in the same change unless the user explicitly narrows scope.
3. Preserve placeholders, interpolation keys, markup, accessibility labels, and plural behavior.
4. Distinguish missing translations from intentionally shared brand names.
5. Inspect dynamic translation keys and fallback paths manually; static key extraction cannot prove them complete. Include accessibility labels and non-page surfaces such as dialogs and notifications when affected.
6. Map application error codes to localized messages, with a localized fallback for unknown errors. Do not expose raw provider or server error strings in the UI.
7. Run the project's localization checker, parser, build, or targeted UI verification when available.

Every locale-sync plan or completion report must cover these five gates explicitly, even when files are not yet available: the real locale set, parsed argument identity/type and message structure, locale-resource parsing, the project checker or targeted build, and the affected narrow-screen UI (including RTL when supported). Mark unavailable gates as pending; do not silently omit them.

Treat placeholders and ICU messages as executable structure, not prose. Preserve placeholder identity and type, and translate the full plural or select message without guessing what a value represents.

For locale-file work, compare runtime argument identity/type for printf or simple templates; for ICU, validate parsed structure and locale grammar rather than requiring identical plural-branch counts. Recognize the project's actual printf, Android, ICU, or template syntax and distinguish escaped or literal percent signs; a naive `%` search is not a valid checker. Also parse every changed locale resource and report the real locale set, not only the languages shown in the request.

When a changed message contains placeholders, run `scripts/check_placeholders.py` even if only inline source and target strings were provided. Example:

```bash
python scripts/check_placeholders.py \
  --source '今天还可识别 %d 次' \
  --target 'ja=本日はあと%d回認識できます' \
  --target 'ru=Осталось распознаваний: %d'
```

Keep the real `PLACEHOLDER_OK ...` or `ICU_OK ...` stdout in completion evidence; do not invent checker output. `VALIDATION_UNAVAILABLE` is not a pass. The checker supports indexed printf reordering and routes ICU to the pinned FormatJS parser. Set `--source-locale` for non-English ICU source grammar. For explicit syntax selection and limits, read [references/message-validation.md](references/message-validation.md). Source/target resources still need their platform parser; inline checks do not validate XML, .strings, or rendered UI.

For Arabic and other RTL locales, check direction, bidi isolation around placeholders and brand text, numeral and punctuation order, mirrored icons where appropriate, and the real rendered control. A correct string and preserved placeholder do not establish RTL UI correctness. When no UI artifact is available, state that runtime RTL remains unverified and give these exact checks as pending acceptance criteria; do not pretend an inline string proves the UI.

Treat translation memory, generated caches, and temporary outputs as untrusted inputs. Existing non-empty translations in the authoritative locale directory win by default. Diff cache against the authoritative files, import only reviewed missing values, and never bulk-overwrite approved translations merely because a cache is newer.

## Run the naturalness review

Reject or revise copy that contains any of these signals:

- source-language grammar or unnatural word order;
- repeated words such as `private private`;
- false friends or wrong-domain dictionary meanings;
- mixed source and target language without a deliberate reason;
- unnecessarily formal, bureaucratic, or generic AI phrasing;
- one long sentence where local product writing would use two;
- translated idioms that a local reader would not use;
- changed negation, number, unit, price, date, responsibility, or confidence;
- changed release, review, availability, or download state;
- wording the user already rejected, or a deliberately retained choice silently undone;
- claims that are stronger than the source;
- text that fits the locale file but overflows the real UI.

When work is incomplete or blocked, inventory each delivery surface separately: in-app locale resources, `InfoPlist` or permission strings, store-listing metadata, screenshots, server/runtime copy, and generated caches. Do not let completion on one surface imply coverage of another. Preserve useful partial outputs and caches when an external service is rate-limited; stop unbounded retries and record the exact remaining gaps.

For broader audits or difficult cases, read `references/review-patterns.md`.

## Evaluate runtime-generated copy

Treat AI-generated user-visible text as a distribution of possible outputs, not as fixed copy. A natural prompt or one good response does not prove native-quality output.

When localized text is generated at runtime:

1. Build a locale-stratified evaluation set from realistic inputs, including ambiguity and failure cases.
2. Run the same inputs more than once when output can vary; keep provider, model, prompt version, locale, and sampling settings fixed and recorded.
3. Measure target-language compliance, established local terminology, mixed-language leakage, invented literal translations, meaning changes, and unsafe increases in certainty.
4. Report failure counts and rates per locale. Do not hide a weak locale inside one global average.
5. Separate deterministic checks from qualified human review. English fluency checks or script detection do not establish native quality in every other language.
6. Add deterministic post-processing only for true invariants; do not use it to conceal recurring model-language failures.

For evaluation design, scoring, repetition, and reporting boundaries, read `references/runtime-ai-output-evaluation.md`.

## Report completion honestly

State:

- which locales and surfaces were changed;
- which project glossary or terminology governed the result;
- which checks passed;
- which phrases remain uncertain or require a specialist;
- whether verification covered source files, build, browser/device, or production.
- for runtime-generated copy, the tested models, prompt versions, sample counts, repetition policy, and per-locale failure rates.

Do not describe a translation as complete when only one locale, one screenshot, or a static file check was covered.
