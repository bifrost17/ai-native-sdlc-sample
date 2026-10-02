# 0020 — WSL 전체 게이트 비교 기준

판정: **문서·Git 대조 완료, 원문 임시 로그는 미수집.** Mac 게이트 실패를 비교할 WSL 기준 결과를 만들었다. full 실행의 판정은 94 PASS·1 FAIL이며, 나중의 `failed` 축소 재측정 PASS가 그 FAIL을 지우지 않는다.

고정 자료는 `.local/research/openwebagent-template-history/20261003/collection/` inventory·API·bare Git, 초기 main `a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e`다. [PR #373](https://github.com/bifrost17/openwebagent/pull/373)과 `intent/0020-wsl-full-gate-reference/`의 여러 문서 커밋을 구분한다.

| 순서 | 근거·확인 |
|---|---|
| 최초 문서 | [`9aad8df`](https://github.com/bifrost17/openwebagent/commit/9aad8dfe2) intent, [`e909326`](https://github.com/bifrost17/openwebagent/commit/e909326af) spec, [`312f552`](https://github.com/bifrost17/openwebagent/commit/312f5528b) plan이 순서대로 있다. intent `:4-30`은 Mac과 같은 gate ID 비교, 기존 :3080/volume 보호, WSL 한 호스트의 한계, 비밀·원문 로그 제외를 적는다. spec `:9-62`는 full 95개 ID·원시 결과·실패를 그대로 기록하는 계약이다. plan `:21-92`는 clean subject 확보→full 실행→결과 문서→독립 검토/PR 인도 순서다. |
| 실행 보고 | [`f9c76af`](https://github.com/bifrost17/openwebagent/commit/f9c76af75)가 `gate-results.md`를 추가했다. 문서 `:1-67`은 subject `6b88d078c132a025b3fe9387579e9acb1dce010e`와 tree, WSL·전용 Docker daemon, 명령 환경, 55분 54초, candidate rc 1을 기록한다. catalog 순서 표는 95 gate 중 94 PASS, `backend-runtime` FAIL, gate SKIP/MISSING 0이다. 이 수치는 PR 본문과 문서가 일치한다. |
| 통합·재검토 | [`c8d6cab`](https://github.com/bifrost17/openwebagent/commit/c8d6cab1a)이 최신 main 통합 subject에 맞추고 [`e81b4cc`](https://github.com/bifrost17/openwebagent/commit/e81b4ccf3)이 최종 검증 기록을 더했다. PR은 `failed` 선택 재측정의 `image-build`와 `backend-runtime` 2 PASS, full 1 FAIL 보존, fresh SDLC verifier 2회 차단 finding 없음이라고 보고한다. 축소 재측정은 전체 full의 재통과가 아니다. |

| 축 | 판정 |
|---|---|
| 의도 보존 | **충족.** Mac 문제 비교용 기준이라는 목적과 WSL 한정 범위를 모두 문서에 남겼다. |
| 설계 충실성 | **문서 대조 확인.** gate ID·순서·상태, subject, 환경, 로그 한계가 spec SP01·SP02와 대응한다. 제품 기능 변경은 없다. |
| 계획 실행성 | **충분.** 실행 전 보호 경계와 깨끗한 대상 판, 판정·인도 작업이 분리됐다. Git 문서 순서는 확인되나 실제 full 명령 실행은 원문 로그를 확보하지 못해 독립 재현하지 않았다. |
| PR·병렬 분할 | **문서 단일 PR.** 제품 경로 충돌·모듈 통합 사례가 아니다. |
| 변경 피드백 | **보존.** full 실패 뒤 축소 재측정과 최신 main subject 정정이 별도 문서 커밋으로 남았다. |
| 검증·보고 | **정확한 경계.** full rc 1/FAIL과 failed rc 0/PASS를 구별하고 live DB 7개·SQL Lab 라이브 축의 내부 제외, macOS 전이 불가, `/tmp` 로그 보존 한계를 적었다. 임시 원문은 이번 수집에 없어 산출값의 독립 감사는 제한된다. |

H1·H2·H3은 기능 설계·UI·모듈 통합 사례가 아니어서 이 자료만으로 판단할 수 없다. H4에는 독립 기대와 환경·관측 지점을 미리 정하고 실패까지 그대로 남긴 긍정 사례다. 다만 문서의 catalog 일치 주장은 원문 로그 없이 확인한 범위에서만 받아들인다. 당시 실제 스킬 호출은 미확인이다. 현행 0.1.8의 검증·보고 기준과 기존 WIP 계획 문구는 [baseline](../baseline.md)에 구분돼 있으며, 이 건은 새 규칙보다 실패를 지우지 않는 보고 관행의 사례다.
