# Independent R1 review request

Read-only design review of the root-authored execution plan form. Use Read/Glob/Grep only; do not edit,
spawn agents, read unrelated user files or other reviewers' reports. Your result is a review, not approval
of a real product or proof that the plans have been executed.

Read candidate-r1.json under this folder's reviews/ and all 20 files it names in maker/adopter roots.
The supplied combined SHA256 is cbcf049bf2e0776c4a3f82f9da3e31c098d03295b8e5fb55cc8163dc9c4ff9d5.
Read the referenced spec/context examples, this folder's reading-notes.md, alternatives.md,
alternative-feature.md, change-walkthrough.md, intent/0022-plan-form/spec.md and current
docs/GIT-WORKFLOW.md and docs/PR-SIZE.md in the maker repo.

For source alignment read the relevant original lessons 4, 7, 8, 10 in
docs/verification/north-star-playbook.html; details.verify is our historical assessment, not original.
Avoid embedded image lines; text sections are around 570–729, 971–1076, 1077–1210, 1329–1443.
Use the saved research design-approaches/report and primary source snapshots as needed, not a new
large external research project. The reference filenames plan/tasks differ in meaning across tools.

The user wants a thin internal-service template that broadly follows the playbook with human judgment.
No semantic document checker, mandatory external skills, state engine, LOC cap or perfect-compliance goal.
Small plans should stay short. Larger plans must connect each PR scope/dependency to working main state,
remaining work and concrete proof. Parallel boundaries need shared contracts and integration/plan coordination.
Review same-commit plan revision, affected upstream changes/pins, and stage acceptance versus final merge.
Check that maker verifier does not treat future PR tests/files as defects in the current completed slice.
Adopter remains optional examples only, with disable-model-invocation; maker controls are not exported.

Return PASS or FAIL, the exact supplied candidate hash, files actually read, and important findings with
path/line, triggering situation, consequence, smallest sufficient correction. Nonblocking suggestions are
optional. Do not make style or more tables a blocker. Identify residual limitations explicitly.
Root will run a separate bounded Sonnet F02 plan/implementation dialogue and independent verifier;
do not claim those already passed. Runtime hosted PR/CI and real migration are outside this review.
