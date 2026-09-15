I reviewed spec@32d64b9 and plan@9e1188f. The proposed flag name, accepted true values and tab output
format are suitable. Before I accept the documents, please correct these concrete inconsistencies:

- Spec Design says neither feature can be enabled alone and later says both finish in one PR. Our plan
  correctly has PR1 test-ON list only, summary not yet present; ordinary release waits for both PRs.
  Say explicitly that incomplete partial TEST availability is allowed while partial GENERAL release is not.
- R3 promises all=open+done, then Design discusses other statuses. Scope that invariant to the supported
  open/done data contract; future unknown statuses are outside this development item, not two competing contracts.
- Keep the eventual cleanup in plan as a conditional follow-up, rather than outside all planning. For this
  local probe I define the mock stabilization condition: after complete PR2 ON/OFF and neighboring flows pass,
  HUMAN records a simulated release/disable observation and declares no older process or rollback version uses
  the control. This substitutes only for local cleanup testing, never proves real stabilization time.
  Plan the separate cleanup PR after my explicit request: final behavior remains available; remove temporary
  code/tests/docs settings references after the safe transition; preserve relevant product regression tests.
  Explain the ordinary default contract change at cleanup in spec (R1/R5 apply while control exists), and
  what expected results/tests change when that lifecycle condition has actually been accepted.

Update the affected spec and then separately repin/update plan; preserve initial drafts and this feedback
in decisions.md. These revisions remain review drafts; do not implement code or merge. Stop with new SHAs.
All previous checkout/tool/side-effect scope restrictions remain.
