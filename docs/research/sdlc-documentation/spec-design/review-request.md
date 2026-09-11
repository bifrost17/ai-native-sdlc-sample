# Independent review of our combined spec form

Root authored this candidate after rereading the accepted design direction and research. You are a
read-only reviewer: inspect and report; do not write files, repair examples, install tools or launch agents.
Do not read another reviewer's report. The same request and candidate receipt go to Astra and Fable.

## Authority and inputs

Anthropic's original Lesson 3/4 in docs/verification/north-star-playbook.html is the north star.
The details.verify annotations are our evidence and historical assessments, not Anthropic requirements.
Use docs/research/sdlc-documentation/{design-approaches,report,comparison}.md and the original references
where helpful. This internal-service team deliberately uses thin policies and human review. We aim for
generally sound behavior, not perfect future-agent performance, maximal documents or new checkers.

Read the receipt's actual candidate files. Main authoring files are templates/spec.md,
.claude/skills/design-spec/SKILL.md, its two references, and three examples with their intent/context.
Read alternatives.md, alternative-feature.md, change-walkthrough.md, reading-notes.md and README.md here.
F01/B01 context contains explicit synthetic post-intent answers derived by root from the existing dataset;
this is a document design review, not a blind generation experiment. Do not read human.json or treat its
hidden oracles as part of agent performance. M01 is wholly synthetic, including its baseline/API/operations facts.

The receipt also covers the adopting worktree at /Users/jake/Projects/ai-native-sdlc-use-0021: templates,
optional capture-intent/design-spec guidance, examples and depth reference. Read the differing guidance
and check corresponding content. Main uses Skills applied; adopter uses References applied. Adopting skills
must remain optional and should not require this maker repo's tools/policies. The spec-example Upstream
SHAs identify real commits of each input intent but neither is organizational acceptance; their draft
authoring condition is explicit. Exact mirrored files can be compared using receipt hashes when possible.

## Questions that matter

1. Does the form support combined requirements + design, with visible human concerns and a useful
   input to planning? Does it preserve intent while avoiding duplicate implementation plans or an RFC bureaucracy?
2. Do the examples preserve all material input contracts, changed and unchanged behavior, actual choices
   and their reasons? Any invented facts, hidden assumptions, lost data/permissions, unjustified commitments
   or illustrative code being treated as a mandatory design?
3. Are the acceptance results useful beyond restating R clauses, including important failure/regression
   cases without requiring exhaustive checklists, invented targets or a test per line?
4. Is the level of detail proportionate across F01, B01 and M01? Can implementation make incidental choices?
   Is M01's migration/recovery/shared-consumer contract technically coherent and sufficiently explicit to plan?
5. Do unanswered/new questions, policy conflicts and important design uncertainty remain visible? Can a
   draft be honestly incomplete while preventing a name under carried forward from being treated as resolution?
6. Does the described change handling update the current contract and affected plan/intent with existing
   human decisions, without new ledgers, timestamp checks or repeated approval requests?
7. Do canonical metadata, R/AC references, Flagged concerns and existing policy/plan consumers still work?
   Eval 03 heading/fixture edits must not weaken the dropped-question failure or policy criteria.
8. Does the adopter keep References applied and optional examples with no mandatory plugin/tool installation,
   and actually receive the same design substance and previously reviewed intent principles?

## Read-to-handoff exercise

For each of the three completed examples, briefly state: what changes, what must stay, the important design
choice/reason, what would prove acceptance, and what judgment still prevents planning (if any).
For M01, identify what needed changing when the direct JSON report consumer was discovered, and which
execution details remain for plan. Check the input/context against the final example rather than trusting
root's narration. This is a reader-handoff review, not a claim that an implementation ran.

## Verdict

Return PASS or FAIL for the provided candidate, material findings with path and impact, and concise
advisory notes/limitations. Do not block on stylistic preferences, a fixed section count or hypothetical
future errors. Do block on important omissions/contradictions likely to produce a wrong plan or false
readiness/approval claim. Identify the receipt/hash and which files you actually read; distinguish a hash
you recomputed from one merely provided. PASS is review of this scope, not human approval or proof of
every future conversation. A missing capability is a limitation to report, not permission to fabricate proof.
