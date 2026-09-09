# Intent: the machine built for chain 0001 went past the lessons
Author: the user (product owner), via the parent session. Status: draft.
First conversation: 2026-09-09 (stated by the author).
## Problem
Chain 0001 set out to make the artifact chain "machine-enforced". What it produced, measured by
the parent session on `origin/main` at 3de08318: 15,740 lines across the merged lanes, about 80%
of them checker code and its tests; on this lane's checkout, 10,408 tracked lines, of which the
files this lane owns are 1,102 and the metrics script alone is 2,010. The approval check — "no
`accepted` on a branch" — was rewritten three times and a variant got through each time. The
playbook never asked for that machine. It puts intent approval in the merge (L2 231), spec
approval in the product owner (L3 276), plan approval in plan mode (L4 360), and PR approval
in branch protection (L11 762); it calls a skill "an advisory control" (L6 503).
The author's words (2026-09-09): "너무 기계적인 검증과 플레이북에서 말하는 절차등을 체크하고
검증하고 강제하고 이런게 코드로 들어가면 안된다는거야. 어디까지나 에이전트가 유연하게 사용할수
있어야해. 다만 레슨에서 중요하게 체크하라고 한 부분이 있고 그걸 코드로 안깨지게 검증할수 있다면
추가되는게 맞겠지."
## Proposed outcome
The repo keeps only what a lesson itself names as a deterministic layer (a hook, a deterministic
script, a CI merge check). Everything else the lessons put in a skill, a tool, or a person goes
back there: templates live in skills, approval is the merge, indicators are git commands, and a
document maps every lesson to its device and layer. The whole tree fits in 2,500 lines, and
every code file opens with the lesson sentence it implements.
## Affected users and systems
The product owner reading chains; the agent reading skills; `make check` and the CI that calls
it; anyone who copies this repo as a starting point.
## Constraints
- Code that checks artifact form, status or transitions is removed and not rebuilt; a missing
  section is caught by the skill and the product owner reading the file (author's decision, not
  to be reopened).
- Hooks the lessons name (protected paths, test protection, credentials, format/lint, production
  gate) stay. A plan-sync hook is optional (L4 329 "Consider") — this repo does not have one.
- python3 standard library and bash 3.2 only. Quotes from the playbook are short and cite lines.
## Open questions
- Does `secure-api-review`, kept verbatim from L6, keep its last line pointing at
  `scripts/check-endpoints.sh` when no such script exists here? — the product owner.
- Which of the reference repos' ideas still need a NOTICE line after the trim? — the parent session.
