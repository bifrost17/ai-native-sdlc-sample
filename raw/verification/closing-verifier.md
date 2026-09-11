# Independent verifier addendum — 0018 neighbour, north-star annotations, E02b close

## What I ran

- `git diff --name-status 6a4f18e^..c4e0f10` and a direct read of
  `intent/0018-team-harness/plan.md` — exit 0. I compared every repository path in **Files that
  change** in both directions. I also ran `git merge-base --is-ancestor
  d7729514b8b7e911c4f2cd7f92636fe891938ff2 c4e0f10` and compared the spec blobs at those two
  revisions — both exit 0.
- A read-only byte comparison of `c4e0f10:docs/verification/north-star-playbook.html` and the
  working file. I removed complete `details.verify` blocks only for the outside-byte comparison,
  then indexed each block by verification ID and removed only the new `0019` paragraph for the
  inside comparison — script exit 0.
- `git show`/`git diff-tree`/`git merge-base` for E02b commits `8b4395f` and `f14c811`, direct reads
  of current spec/plan/code/tests/README, and `git status --porcelain` in `event-r03` — exit 0.
  I parsed the three preserved JSONL turns and `run-summary.json` for actual `Skill`/`Agent` calls,
  and read `product-final.json` for the independent product checks. I did not repeat `make check`,
  as requested; its earlier full output remains in `human-event-r01/maker-check-final.txt`.

## What I saw

- The 0018 neighbour is internally pinned. `d772951…` is an ancestor of `c4e0f10`, and
  `intent/0018-team-harness/spec.md` is byte-identical between them. The actual 0018 range changes
  exactly the 19 repository files named by the plan: the four `team-harness` files, its test,
  README/boundary/research material, v4 manifest/cases and experiment records, four verification
  documents, and the three 0018 intent artifacts. There is no planned repository path missing and
  no unplanned repository path. The plan explicitly places product conversations, logs, install
  targets, and the unchanged `add296d` template outside this Git diff.
- Outside all verification `details` blocks, the north-star bytes are identical to `c4e0f10`
  (both normalized SHA-256
  `31c395a2b617e4ca0b06c8ebb7d7a9d3c9aaa69c4afa46ac5338c53e1963ffdf`). Both versions have 179
  unique IDs with `v-ok=139`, `v-part=23`, `v-team=17`. Exactly eight blocks differ:
  `V4-11`, `V6-04`, `V6-05`, `V6-06`, `V7-09`, `V8-02`, `V8-09`, `V10-05`; removing one new
  `0019` paragraph from each makes all 179 blocks byte-identical to the base, so prior annotations
  are preserved. Every new relative link resolves to an existing local path:
  `docs/experiments/0019-event-review-skill.md` or `org-skills/README.md`.
- E02b is a single clean session, `421b4a77-c5f7-4228-8725-d399fc08c89a`. T1 contains one direct
  `Agent` call selecting `intent-sdlc-skills:sdlc-verifier`, whose messages use `claude-opus-5`;
  there is no `Skill` tool call in T1 or in T2/T3. The reviewer reads current project policy,
  artifacts, code and tests and reports the missing JSON contract. The public record correctly says
  that this is not a 0.1.4 main-skill load (`0019` lines 90–107), and the V6-06 annotation makes the
  same distinction. It also correctly avoids claiming a fresh native review of the final commit.
- HUMAN's T3 message explicitly accepts spec commit
  `8b4395f0fcb17a48a64d93ed79dca1f18831d1e5`. It is the immediate parent of product commit
  `f14c81133246c228a9fcf16e51a4f306e1f48912`; that second commit changes exactly `plan.md`,
  `tracker.py`, `tests/test_tracker.py`, and `README.md`. The plan points to the full accepted spec
  SHA, the spec blob remains unchanged in the product commit, and plan plus implementation,
  tests, and usage text are committed together. The final clone is clean.
- `product-final.json` records pass for 16 independent CLI cases, including JSON/text parity,
  exact and unknown/empty owner handling, completion changing counts, empty/bad data, and expected
  nonzero errors. The five original tests and two helpers remain in the AST, all seven new tests are
  additive, and `requests.json` is unchanged at Git level with fixture SHA-256
  `c038196ad9f748e482a446e4025e4c6c0746b23942c39f5f457ad37dd9a53795`. The preserved turn output
  independently shows 12 unit tests passing before commit.

## What does not match plan.md

None in the checked 0018 neighbour, north-star annotation scope, or E02b spec/plan/product chain.

The product plan's final Proof sentence, “이 계획 단계에서는 실행하지 않았다,” is a historical
plan-stage statement already present before E02b and is scoped by its preceding sentence to evidence
that would be produced at implementation time. The preserved turns and `product-final.json` show
that the commands were later executed, so I do not treat it as a false current result claim. Because
the plan was subsequently edited in the implementation commit, the wording is mildly easy to
misread; the 0019 record appropriately distinguishes the initial statement from current evidence.

## What I could not check and why

- The final E02 public archive commit, raw/public hash manifest, and its pin do not yet exist; the
  0019 record explicitly leaves that pin pending. Those must be checked after archival, including
  that adding records did not alter product `f14c811`.
- I did not rerun `make check` in this addendum. The earlier verifier run and its stored output cover
  that command; this pass was deliberately limited to the missing neighbour and closing evidence.
- This evidence supports the observed event flows, including one direct 0.1.4 native-agent choice.
  It does not establish a fresh 0.1.4 Skill-trigger success, a final-commit native approval, every
  event triggering every time, hosted PR/CI behavior, or general reviewer accuracy.
