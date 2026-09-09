# Intent: ci_test_failure_rate 밴드 이탈 (3sigma · rule1_one_point_beyond_3sigma)
Author: detect_bands (automatic, 2026-09-09T12:16:23+09:00). Status: draft.
## Problem
`ci_test_failure_rate` 최신 표본 2026-09-02T00:00:00+09:00=0.31 이 규칙 `rule1_one_point_beyond_3sigma` 로 tier `3sigma` 를 냈다 (n=20 mean=0.101 sigma=0.004611199181854631 z=45.32443552263554).
## Proposed outcome
`ci_test_failure_rate` 가 기준선 안으로 돌아오고, 행동 `propose` 가 이 초안으로 이행됐다.
## Affected users and systems
지표 `ci_test_failure_rate` 를 생산하는 CI 와 그 지표로 머지를 판단하는 사람 전부.
## Constraints
- C1 Status 는 draft — 이 초안의 PR 이 머지되기 전엔 하류(spec·plan)를 시작하지 않는다.
- C2 원인·처방은 여기 없다 — diagnose 단계의 몫이다.
## Open questions
- Q1 이탈이 코드 변경 때문인지 인프라 변동 때문인지 diagnose 단계가 답한다.
