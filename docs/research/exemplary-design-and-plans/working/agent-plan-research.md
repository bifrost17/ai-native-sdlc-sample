# 에이전트 실행형 구현계획 후보 조사 기록

작성일: 2026-09-11

> 통합 편집 주: 아래의 “주 사례 0건”은 이 분담 경로의 결과다. 상위 조사에서는 별도로 Superpowers **Visual Companion Auth Hardening**의 사전 계획 커밋과 직접 후속 구현을 검증하여 최종 P3로 선정했다. Symphony도 별도 검증 후 설계 D1에 포함했다. 전체 선정 결과는 [README](../README.md)와 [P3 상세](../implementation-plans.md)를 기준으로 읽는다.

## 조사 상태와 판정 원칙

이 문서는 에이전트가 실제 구현에 사용할 목적으로 작성된 공개 계획을 찾기 위한 작업 기록이다. 1차 탐색은 중단됐지만, 이후 범위를 좁혀 GitHub connector와 공개 GitHub 이력으로 BranchLab 한 건을 독립 검증했다. 현재 판단은 **주 사례 확정 0건, 실행 연결성이 강한 보조 사례 1건**이다. BranchLab 사례는 에이전트 지시와 실제 코드 대응이 강하지만 계획과 구현이 같은 커밋에서 처음 공개되어 사전 계획성을 입증할 수 없다.

주 사례가 되려면 다음 근거가 모두 필요하다.

- 계획 원문의 고정 커밋과 최초 추가 커밋 또는 PR
- 계획이 구현보다 먼저 존재했다는 시각 증거
- 에이전트 사용을 명시한 문서, PR, 실행 기록 중 하나 이상
- 계획의 작업 단위와 실제 코드 변경의 대응
- 계획에 적힌 테스트·빌드·수동 검증이 실제 실행됐다는 기록
- 완료되지 않았거나 계획에서 이탈한 항목의 정직한 구분

계획의 문서 품질과 실행 확인 정도는 별도로 판정한다. 잘 작성된 미실행 계획은 참고 사례가 될 수 있지만, 실행까지 연결된 모범 사례로 세지 않는다.

## 독립 검증한 보조 사례

### BranchLab: Trace Physics + Golden Corpus

- 계획 고정판: <https://github.com/jlov7/branchlab/blob/25e9da5cf79d6fcb3e7bae93654d65a991bed98b/docs/superpowers/plans/2026-05-08-trace-physics-golden-corpus.md>
- 구현 커밋: <https://github.com/jlov7/branchlab/commit/25e9da5cf79d6fcb3e7bae93654d65a991bed98b>
- 현재 판단: **실행 연결성이 강한 보조 사례. 깨끗한 사전 구현계획 사례로는 채택하지 않음.**
- 에이전트 사용 근거: 계획 첫머리에 agentic workers가 `superpowers:subagent-driven-development` 또는 `superpowers:executing-plans`로 task-by-task 구현하라고 명시한다. 구현 커밋 메시지는 `Co-Authored-By: OpenAI Codex <noreply@openai.com>`를 포함한다. 파일명 추정이 아니라 계획 본문과 커밋 메타데이터의 명시적 근거다.
- 계획 품질: Goal, Architecture, Tech Stack, File Structure가 짧게 선행한다. Task 1은 모듈 부재 실패를 확인한 뒤 구현·export·통과를 요구하고, Task 2는 9개 JSONL corpus와 disk-backed test 및 알려진 divergence를 고정하며, Task 3은 package 전체 test와 `pnpm check`로 닫는다. 파일과 public symbol 이름, 명령, 기대 결과가 직접 대응한다.
- 실제 코드 대응: 같은 커밋이 `packages/core/src/tracePhysics.ts`, `packages/core/src/index.ts`, `packages/core/test/tracePhysics.test.ts`, `packages/core/test/goldenCorpus.test.ts`, `examples/traces/golden/*.jsonl`, 계획 문서, `.codex/PLANS.md`를 함께 변경했다. connector로 고정 커밋의 구현 파일과 두 테스트를 직접 읽어 계획 항목과의 대응을 확인했다.
- 자가 보고와 확인의 구분: 구현 파일과 테스트 assertion의 존재, 계획 대상 파일이 커밋에 포함됐다는 사실은 독립 확인했다. “처음에는 missing module로 실패”, “10 files/31 tests 통과”, `pnpm check` 통과는 계획과 커밋 메시지의 자가 보고이며 CI 실행 로그로 독립 확인하지 않았다.
- 핵심 한계: 계획, 구현, 테스트가 모두 동일한 최초 공개 커밋에 들어왔다. 공개 Git 이력만으로 계획이 코드보다 먼저 작성·사용됐다고 증명할 수 없다. 따라서 결과-계획을 사후 정리했을 가능성을 배제하지 못한다. PR·issue 링크도 확보하지 못했다.
- 템플릿에 가져올 부분: 상단 4문장 요약, 파일별 책임, RED→구현→GREEN 순서, fixture 표본과 관측값 고정, 전체 gate, self-review. 가져오지 말아야 할 부분은 실행 로그 없이 체크박스를 완료 처리하는 방식이다.

## 독립 이력 검증으로 제외한 사례

### Superpowers: Visual Brainstorming Companion

- 현재판: <https://github.com/obra/superpowers/blob/main/docs/plans/2026-01-17-visual-brainstorming.md>
- 문서 추가 커밋: <https://github.com/obra/superpowers/commit/e4226df22e4a3800dacdcbda9f7c5adea8533138>
- 선행 구현 커밋: <https://github.com/obra/superpowers/commit/866f2bdb4748ad934cd73ded4dc1176902130478>
- 판정: **사전 구현계획 사례에서 제외**
- 문서 품질: agentic workers 지시, 파일별 코드, 실행 명령, 예상 결과, 작업별 커밋 명령까지 매우 구체적이다.
- 제외 근거: GitHub compare에서 계획 문서 추가 커밋 `e4226d…`를 base, 구현 커밋 `866f2b…`를 head로 비교하면 `status=behind`, `behind_by=1`, merge base가 구현 커밋으로 나온다. 즉 공개 ancestry에서 구현 커밋이 먼저고 계획 문서 추가가 그 다음이다. 파일 날짜 `2026-01-17`은 Git 이력보다 앞서지만 그 자체로 공개 사전 계획 증거가 아니다.
- 추가 한계: 서버 시작 확인과 manual/smoke 중심 단계가 많으며, task별 코드 블록이 장대해 구현 결과를 거의 복제한다. 문서 표현 사례로는 참고할 수 있지만 “계획이 실제 구현을 이끌었다”는 실물 증거로 집계하면 안 된다.

## 미완료 검증 대상

### Apache SkyWalking BanyanDB: Replication Integration Tests

- 고정판: <https://github.com/apache/skywalking-banyandb/blob/9065ed8ba8a5280b05f78d4e4f3de37beda48036/docs/superpowers/plans/2026-03-20-replication-integration-tests.md>
- 관련 공개 알림: <https://www.mail-archive.com/notifications%40skywalking.apache.org/msg240508.html>
- 유형: 외부 유명 프로젝트의 Superpowers 형식 통합 테스트 구현계획
- 현재 판단: **실제 사례 유력, 검증 명령 결함 가능성 때문에 단독 모범 사례로는 보류**
- 좋은 점: 고정 커밋을 인용할 수 있고, agentic workers용 계획임을 명시한 공개 흔적이 있다. 복제 통합 테스트라는 실제 저장소 작업을 대상으로 한다.
- 실행 근거 상태: 문서 추가 커밋은 특정됐지만, 후속 구현 PR·커밋과 테스트 성공 기록은 미검증이다.
- 한계: 계획의 `go test -run 'Measure.*Replication'` 명령은 Ginkgo suite에서 Go 테스트 함수 이름만 필터링해 의도한 spec을 선택하지 못할 가능성이 있다. 명령이 통과하더라도 대상 테스트가 실행됐다는 증거가 아닐 수 있다.
- 최종 채택에 필요한 확인: 해당 명령의 실제 테스트 선택 결과, 구현 diff, CI 로그, 계획 항목의 완료 여부.

## 제외 또는 보조 후보

### EveryInc Compound Engineering Plugin: Unified Plan Doc Artifact Refactor

- 원문: <https://github.com/EveryInc/compound-engineering-plugin/blob/main/docs/plans/2026-06-18-001-refactor-unified-plan-doc-artifact-plan.md>
- 관련 구현 커밋: <https://github.com/EveryInc/compound-engineering-plugin/commit/7ef752aa422b6f860101f0794856f19c9c65eff2>
- 관련 PR: <https://github.com/EveryInc/compound-engineering-plugin/pull/972>
- 판정: **최상급 사례에서 제외, 반면교사 또는 보조 사례**
- 좋은 점: 계약, 작업 단위, 검증 조건이 매우 구체적이고 실제 커밋·PR 리드가 있다.
- 제외 이유: 프레임워크가 자기 계획 문서 체계를 개선하는 자기 예제다. 더 심각하게는 본문에서 Goal Launch Block과 Reader Index를 두지 않겠다고 하면서 Global Definition of Done은 이를 요구하는 내부 모순이 있다는 검토 결과가 있다. 문서 길이와 세부 항목 수를 품질로 오인하면 안 된다.

### Rhapsody: Fix Xfailed Integration Tests

- 원문: <https://rhapsody-cli.readthedocs.io/en/stable/superpowers/plans/2026-07-21-fix-xfailed-integration-tests.html>
- 판정: **최상급 사례에서 제외**
- 좋은 점: 실제 프로젝트의 구체적인 테스트 수정 계획이다.
- 제외 이유: `collect-only | grep -c xfail` 같은 간접 검증에 의존하며, 계획의 50건과 파일 합계 49건이 맞지 않는다는 사전 검토 결과가 있다. 구현 이력과 실행 결과도 미검증이다.

### OpenAI Symphony SPEC/plan

- 판정: **미검증 리드, 집계하지 않음**
- 제외 이유: 정확한 원문·고정판·구현 이력을 확보하지 못했다. 제품 또는 프레임워크의 지침 문서만 존재한다면 실제 작성된 구현계획 사례가 아니다.

## 후보군·검색 기록

초기 탐색 경로로 Superpowers 실제 `docs/plans`, ExecPlans, `.planning`, `.kiro/specs`, OpenSpec을 사용한 외부 제품의 archived changes, Symphony SPEC/plan을 설정했다. 실제 확보된 리드는 다음 다섯 계열이다.

1. `obra/superpowers` visual brainstorming
2. Apache SkyWalking BanyanDB replication integration tests
3. `jlov7/branchlab` ExecPlan 및 release master plan
4. EveryInc compound-engineering-plugin unified plan refactor
5. Rhapsody xfailed integration tests

브라우저 조사 스킬 지침에 따라 Aside CLI 업데이트를 시도했으나 제한된 네트워크에서 실패했다. 승인 요청 도중 1차 조사가 중단됐다. 이후 지시에 따라 Aside를 사용하지 않고 GitHub connector와 web만으로 범위를 BranchLab 한 건과 Superpowers 이력 반증으로 좁혔다.

- BranchLab 계획 원문과 `.codex/PLANS.md`를 읽었다.
- `trace physics` 커밋 검색으로 구현 커밋 `25e9da…`를 특정했다.
- 해당 커밋의 전체 변경 파일 목록을 확인했다.
- 고정 커밋의 `tracePhysics.ts`, `tracePhysics.test.ts`, `goldenCorpus.test.ts`, 구현계획을 직접 대조했다.
- Superpowers visual brainstorming의 문서 추가 커밋과 구현 커밋을 비교해 구현이 먼저라는 ancestry를 확인했다.

따라서 목표였던 15~20개 후보 수집, 6~8개 정독, 3~4개 최종 추천은 수행되지 않았다. 최소 3개 최상급 사례를 확보하지 못했으며, 이를 숨기기 위해 기준을 낮추지 않았다.

## 후속 검증 순서

추가 조사가 허용되면 다음 순서가 효율적이다.

1. BranchLab의 실제 release master plan 하나를 고정하고 per-ID evidence를 끝까지 추적한다.
2. BranchLab `Trace Physics + Golden Corpus` 실행의 CI run이나 PR을 찾아 test pass 자가 보고를 독립 확인한다.
3. BanyanDB 계획 명령이 실제 Ginkgo spec을 선택하는지 CI 또는 로컬 실행 로그로 확인한다.
4. 위 후보가 실패하면 `.kiro/specs`와 OpenSpec `archive`를 쓰는 외부 제품 저장소에서 실제 완료된 change를 두 번째 라운드로 찾는다.
5. 각 사례에 대해 계획 품질과 실행 확인 정도를 별도 표로 기록하고, 둘 다 강한 사례만 최종 3~4건에 넣는다.
