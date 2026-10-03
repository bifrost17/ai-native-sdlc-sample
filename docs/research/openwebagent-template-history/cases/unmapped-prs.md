# 번호 없는 후속 PR 판정

조사 기준 시점은 2026-10-03이며, 원격 `main` 기준판은 `a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e`다. 템플릿 채택 경계는 2026-09-14, 기준 PR은 #258이다. 여기서는 채택 경계 뒤의 미매핑 PR 다섯 건을 원래 PR 기록·파일 변경·커밋·관련 댓글·현재 main 파일 지문으로 검토했다. 모두 numbered intent 경로, 제목/브랜치의 intent 번호, 본문의 명시적 intent 참조가 없어 기존 30개 intent entity의 alias로 합치지 않았다. PR #268과 #404는 동일한 저장소 지침·정책 파일을 잇달아 바꾸고 같은 정책 목적을 공유하므로 하나의 번호 없는 정책 사건에 개별 이벤트로 묶었다. 나머지는 별도 사건이다.

이 문서는 PR 본문이 주장한 시험을 재실행 결과로 취급하지 않는다. 원격 상태·파일 SHA는 manifest에 기록된 수집 판이다. 현재 파일은 PR metadata와 별도로 `main SHA:path` 및 blob SHA를 대조했다. 여섯 평가축 가운데 실제 증거가 있는 축만 판정하며, 문서 UI가 없는 작업에 UI 조건을 만들어 붙이지 않는다.

## 판정 요약

| 번호 없는 사건 | 포함 PR | 실제 변경 범위 | intent/design/plan 문서 | 평가 경계 |
|---|---|---|---|---|
| 저장소 에이전트 지침·정책 정렬 | [#268](https://github.com/bifrost17/openwebagent/pull/268), [#404](https://github.com/bifrost17/openwebagent/pull/404) | 루트 `AGENTS.md`, `CLAUDE.md`; #404는 `PROJECT-POLICY.md`도 변경 | 없음 | 본문에 요청/목표가 남고 문서 diff로 구현을 확인할 수 있다. 별도 spec/plan의 선행 충분성은 미확인이다. |
| 오케스트레이터 종료 컨테이너 재생성 | [#363](https://github.com/bifrost17/openwebagent/pull/363) | 오케스트레이터 바쁨 판정과 회귀 시험 | 없음 | 단일 코드+회귀시험 PR이며 PR 본문에 시험 범위가 구체적이다. PR 주장의 실행 결과는 별도 독립 재실행으로 확인하지 않았다. |
| 실행기 설정 계약·기동 자가검사 | [#326](https://github.com/bifrost17/openwebagent/pull/326) | 로컬/에어갭 compose, preflight, 기동 스크립트, gate catalog 및 계약 시험 | 없음 | 두 변경 조각은 두 커밋으로 연결됐다. PR 본문에 계약/뮤테이션 시험이 특정돼 있지만 선행 spec/plan은 찾지 못했다. |
| seed 컨텍스트 출처 표시 | [#301](https://github.com/bifrost17/openwebagent/pull/301) | seed 출력, 운영 안내, 회귀 시험 | 없음 | test-red → 구현 → 문서 → 표현 정리의 4 커밋이 보인다. 본문에서 #298~#300은 합친 기준판/재실행 맥락으로 인용되며, #301 자체를 0001 alias로 만들 근거는 아니다. |

다섯 PR 모두 GitHub formal review object 0건과 inline review comment 0건이다. 이는 댓글이 없었다는 뜻이 아니다. 각 PR에는 CodeRabbit 계정의 issue comment가 하나씩 있고, #404/#268은 요청 한도 알림, #363/#326/#301은 change-stack/자동 요약 유형이다. PR #404 본문은 프로젝트 `code-review` 스킬을 사람이 요청해 사용했다고 기록하지만, CodeRabbit 댓글은 리뷰 승인이나 발견 목록이 아니다. 수집 당시 head 커밋의 Check Runs는 모두 0개였다. 별도로 읽은 commit status는 #404/#326/#301/#268에서 CodeRabbit `success`였고 #363은 CodeRabbit `pending`이었다. 이 context는 자동 리뷰 서비스 상태이며 제품 gate/test 성공 증거가 아니다. [수집된 댓글·리뷰·status 요약과 원본 경로](../../../../.local/research/openwebagent-template-history/20261003/collection/api/curated-scope-adjudication.json)에 분리해 보존했다.

| PR | 수집 당시 commit status | status 세부 링크 |
|---|---|---|
| #268 | CodeRabbit `success` (rate limited) | [head checks](https://github.com/bifrost17/openwebagent/commit/13ce54bbbaa9bba640d7130ffa39c40d1bc05b8e/checks) |
| #301 | CodeRabbit `success` (review completed) | [head checks](https://github.com/bifrost17/openwebagent/commit/786fcd6ce93d4a572afbbff117358d896d8fbf5a/checks) |
| #326 | CodeRabbit `success` (review completed) | [head checks](https://github.com/bifrost17/openwebagent/commit/50f437b35900e6bd3954a37afa2c32d28e588b1d/checks) |
| #363 | CodeRabbit `pending` (review in progress) | [head checks](https://github.com/bifrost17/openwebagent/commit/380e3716d4227f796c0066d370fab2c8c09a4bd3/checks) |
| #404 | CodeRabbit `success` (rate limited) | [head checks](https://github.com/bifrost17/openwebagent/commit/1dd2ec5a66cc4f61b2dbcebb2ba2c24c50b2671c/checks) |

## 저장소 에이전트 지침·정책 정렬: #268 → #404

**이벤트 사실.** #268은 2026-09-15에 `AGENTS.md`와 `CLAUDE.md`를 맞췄다. 본문은 두 진입점의 서로 다른 규칙을 합치고, 공통 workflow 본문을 동기화하며, 충돌 시 정본을 정하는 변경이라고 설명한다. 커밋 [`13ce54b`](https://github.com/bifrost17/openwebagent/commit/13ce54bbbaa9bba640d7130ffa39c40d1bc05b8e)가 두 파일을 수정했다. #404는 2026-09-30에 `PROJECT-POLICY.md`에 PR 병합 전 `code-review` 스킬 사용 절차를 추가하고, 두 진입점에서 정본을 가리켰다. 두 커밋은 [`af7c39f`](https://github.com/bifrost17/openwebagent/commit/af7c39f5e60d71cb2db4e17d59d7c83a11a2c04e)와 [`1dd2ec5`](https://github.com/bifrost17/openwebagent/commit/1dd2ec5a66cc4f61b2dbcebb2ba2c24c50b2671c)다. 두 번째 커밋은 #404 자체를 리뷰한 뒤 규칙을 좁히고 중복 문장을 덜어낸 후속 수정이다. 원 PR 본문은 첫 작성자 메시지를 프로젝트 소유자의 직접 요청이라고 기록한다. 원문에는 계정 식별자 등 이 요약에 필요하지 않은 정보가 있어 재게시하지 않았다. 자동 댓글은 [#268 댓글](https://github.com/bifrost17/openwebagent/pull/268#issuecomment-5689588845)과 [#404 댓글](https://github.com/bifrost17/openwebagent/pull/404#issuecomment-5901876696)이며 둘 다 review limit 알림이다.

**판본 분리.** #268 PR head `13ce54bbbaa9bba640d7130ffa39c40d1bc05b8e`의 `AGENTS.md`·`CLAUDE.md` blob은 현재 main과 다르다. #404 head `1dd2ec5a66cc4f61b2dbcebb2ba2c24c50b2671c`의 `AGENTS.md`, `CLAUDE.md`, `PROJECT-POLICY.md` blob은 현재 main의 같은 파일 blob과 같다. 이는 파일판의 일치만 말하며 지침이 각 에이전트 실행에서 실제 로드·준수됐다는 뜻은 아니다.

**여섯 축.** 의도 보존은 요청/목표와 변경 파일의 연결이 본문에 남아 있다는 범위에서 확인된다. 별도 spec/plan은 없어서 설계 충분성 및 다음 구현자의 작업 가능성은 중요한 근거가 부족하다. 단일 문서 PR이므로 병렬 구현 분할이나 UI 시안/심미성 축은 적용되지 않는다. #404에서 리뷰 뒤 문서 수정은 커밋 그래프로 확인되나, 어떤 문장을 왜 바꿨는지에 대한 인과는 PR 본문 주장으로 제한된다. #268은 diff 일치 검사, #404는 diff 검사와 gate catalog 검증을 실행했다고 본문이 말한다. 별도 제품 gate 변경은 없다고 기록했으며 실제 로컬 시험은 재실행하지 않았다.

**가설 경계.** H1(설계 부족으로 변경 발생)과 H4(검증 방법 미정으로 결함 누락)는 작성된 선행 spec/plan이 없어 지지·반증할 수 없다. H3(모듈 구현 뒤 늦은 통합)은 두 파일 변경의 순서와 관련된 사례가 아니다. H2(UI 설계와 실제 제품 시각 품질)는 UI 개발이 아니므로 적용하지 않는다. 이는 정책 자체가 정확하거나 실제로 효과적이었다는 판정이 아니다.

## 오케스트레이터 종료 컨테이너 재생성: #363

**이벤트 사실.** 2026-09-28 PR은 종료/미생성 컨테이너를 HTTP busy probe로 검사하면 probe 실패가 fail-safe `busy`가 되어 이미지 drift 재생성을 계속 막는 결함을 다뤘다. 종료 상태에서는 busy gate를 건너뛰도록 하고 `test_stopped_sandbox_recreates_even_when_busy_probe_fails` 회귀 시험을 추가했다. 커밋 [`380e371`](https://github.com/bifrost17/openwebagent/commit/380e3716d4227f796c0066d370fab2c8c09a4bd3); 변경은 `orchestrator/orchestrator/app.py`와 `orchestrator/tests/test_image_drift_recreate.py`다. 원 PR 본문은 focused test 86건과 전체 orchestrator test suite green을 보고하지만, 이 보고는 수집자가 다시 실행한 결과가 아니다. [CodeRabbit 자동 change-stack 댓글](https://github.com/bifrost17/openwebagent/pull/363#issuecomment-5870832479)은 formal review object가 아니다.

**판본 분리.** PR head와 현재 main의 두 파일 blob은 모두 다르다. 따라서 위 커밋을 사건의 실제 변경판으로 인용하고, 최신 제품판은 manifest에 기록된 `main SHA:path` blob으로 가리킨다. PR merge 뒤 후속 변경이 있으므로 PR 당시 diff를 현재 코드 동작으로 그대로 일반화하지 않는다.

**여섯 축.** PR 본문은 고장 조건과 바뀐 상태 조건을 연결해 의도를 전달하고, source diff는 구현 및 회귀 시험을 확인시킨다. 별도 spec/plan 부재로 사전 설계 충분성·Done 계약은 판단할 수 없다. 한 PR에 구현과 대표 회귀 시험이 같이 있어 외부 모듈 간 늦은 통합 증거는 없다. 의도한 test-red → 수정 후 green과 전체 시험 실행은 PR 작성자의 보고다. 수집 중 CodeRabbit issue comment는 change-stack 링크이고 status는 `pending`이지만, 이는 test 실패나 merge 차단 원인으로 해석하지 않는다.

**가설 경계.** 이 한 건의 구체적인 예외를 담은 회귀 시험은 H4 우려에 대응하는 증거다. 그러나 원 설계가 검증을 정하지 않았다는 자료가 없어 H4 원인을 뒷받침하지는 않는다. H1은 문서 부재로 미확인, H3는 관련 없는 축, H2는 UI가 아니어서 미적용이다.

## 실행기 설정 계약·기동 자가검사: #326

**이벤트 사실.** 2026-09-22의 두 커밋은 로컬/에어갭 실행기 설정을 영속 env-file에서 요구하도록 하고, dev-worktree 기동 때 경로/모델 경계를 검사하도록 바꿨다. 첫 커밋 [`7d85c90`](https://github.com/bifrost17/openwebagent/commit/7d85c90fdc9bb69612a4645501a2310834e8ff20)는 compose·preflight·로컬 기동·gate 입력과 계약 시험을 고쳤다. 두 번째 [`50f437b`](https://github.com/bifrost17/openwebagent/commit/50f437b35900e6bd3954a37afa2c32d28e588b1d)는 Codex 모델 경로 self-check와 검증을 추가했다. PR 본문은 실제 crash-loop와 반복 실패 사례를 설명하고, origin-coherence 시험, 여러 삭제 뮤테이션의 실패 기대, 관련 gate 및 500개 unittest 성공을 주장한다. 재수행은 하지 않았다. [CodeRabbit 자동 change-stack 댓글](https://github.com/bifrost17/openwebagent/pull/326#issuecomment-5770554031)은 formal review object가 아니다.

**판본 분리.** PR head와 현재 main의 변경 파일 8개 blob이 모두 다르다. 사건판은 위 두 commit SHA, 최신 실제 파일판은 manifest의 current-main refs다. 최근 PR 설명의 재현/해결 서술을 최신 동작 확인으로 취급하지 않는다.

**여섯 축.** 본문은 고장 조건, 환경 차이, 성공 조건을 상당히 구체적으로 남긴다. 다만 선행 spec/plan 또는 AC가 없어 설계 충실성과 계획상 Done의 실행 가능성은 판정할 수 없다. 여러 경로를 두 커밋으로 연결했지만 독립 PR 간 늦은 interface integration 증거는 아니다. 변경 뒤 추가 self-check/test가 생긴 사실은 source commit과 PR 본문 양쪽에 보인다. 실제 수정 전 계획 또는 test oracle이 있었는지는 확인되지 않는다. UI 시안 축은 해당 없음이다.

**가설 경계.** 여러 launcher 경로와 설정 수명주기의 확인은 H3 관점에서 주목할 신호지만, 통합이 늦었거나 모듈 단위로 구현해 실패했다는 증거는 아니다. H1/H4는 선행 문서 부재로 근거 부족이다. 런타임/운영 변경은 자동으로 템플릿 실패가 되지 않는다.

## seed 컨텍스트 출처 표시: #301

**이벤트 사실.** 2026-09-17 PR은 `model_info` 실측값과 내장 이름표/공통 fallback으로 추정한 컨텍스트 크기를 로그에서 구별했다. 네 커밋 [`93f1537`](https://github.com/bifrost17/openwebagent/commit/93f1537987974b6fba438c9e5de1a64ac6ed32fe)(red test), [`ca3e1dd`](https://github.com/bifrost17/openwebagent/commit/ca3e1dd5cc2a8b7c7c823c6c0636c4346f1faa8f)(구현), [`63c77ef`](https://github.com/bifrost17/openwebagent/commit/63c77efe1e7c492791d47d92b82a69ae047d66ec)(운영문서), [`786fcd6`](https://github.com/bifrost17/openwebagent/commit/786fcd6ce93d4a572afbbff117358d896d8fbf5a)(시험 문구 조정)이 그 순서를 보여준다. 변경 경로는 `deploy/airgap/seed.sh`, `deploy/airgap/GUIDE-20-OPERATIONS.md`, `scripts/tests/seed-multi-model.test.sh`다. 본문은 매칭 알고리즘은 그대로 두고, 추정값에 경고 표시를 추가했다고 설명한다. [CodeRabbit 자동 change-stack 댓글](https://github.com/bifrost17/openwebagent/pull/301#issuecomment-5708290789)은 formal review object가 아니다.

**관련 참조의 경계.** 본문에서 #298·#299·#300은 PR-301을 최신 main에 합쳐 재실행한 기준판 문맥으로 연결된다. 이 세 PR은 `intent/0001-project-structure` 경로를 변경하지만 #301의 자체 변경은 해당 경로를 건드리지 않는다. 따라서 관련 PR 참조만으로 #301을 0001에 합치지 않았다. 본문에 등장한 #618은 같은 저장소의 `issues/618` endpoint에서 404였고, 접근 가능한 이슈 metadata를 찾지 못했다. 이를 확인된 저장소 issue나 case ID로 간주하지 않는다.

**판본 분리.** `seed.sh`의 PR head blob은 current main과 같고, 운영 가이드와 test 파일은 다르다. 당시 출력 변경을 말할 때는 구현 commit을, 최신 문서/시험을 말할 때는 main SHA와 각각의 blob SHA를 써야 한다.

**여섯 축.** PR 본문에는 “실측 대 추정”이라는 의도가 있고, red/green 구현·운영문서·문구 조정의 피드백 사슬이 커밋에 남았다. 선행 spec/plan이 없어 설계 충분성·완료 계획은 근거가 없다. 네 commit은 하나의 PR 안에서 한 경계에 붙어 있어 독립 모듈의 뒤늦은 결합 문제를 보여주지 않는다. 본문은 이 PR이 최신 main에서 시험을 통과했다고 주장하고 commit status는 CodeRabbit `success`이나, status는 test 실행이 아니며 시험 자체도 재실행하지 않았다. UI 축은 적용하지 않는다.

**가설 경계.** 구체적인 로그 문구와 입력 유형별 test는 H4에서 검증 기대를 구체화하는 긍정 신호다. 그러나 작성 전 AC/시험 계획이 없어서 초기 설계의 결함 여부는 판정할 수 없다. H1/H3는 근거 부족 또는 비적용, H2는 비적용이다.

## 다섯 PR의 증거 행렬

| 평가축 | 정책 정렬 #268/#404 | 오케스트레이터 #363 | 실행기 #326 | seed 로그 #301 |
|---|---|---|---|---|
| Intent 보존 | 두 PR 본문이 문서 목적/요청을 밝힘. 별도 intent 없음. | 본문에 상태별 사고와 수정 목적이 있음. 별도 intent 없음. | 실패 모드 두 가지와 적용 launch 경로를 본문에 기록. 별도 intent 없음. | 실측/추정 값 구별이라는 목적과 scope 제외 알고리즘이 본문에 있음. 별도 intent 없음. |
| Spec 설계 충분성 | spec/AC 없음. 판정 근거 부족. | spec/AC 없음. 판정 근거 부족. | spec/AC 없음. 판정 근거 부족. | spec/AC 없음. 판정 근거 부족. |
| Plan 실행 가능성 | 계획 파일 없음. 두 문서 변경은 commits로 확인. | 구현+회귀 test 범위는 구체적이나 별도 plan 없음. | 두 launcher 경로/자체 검사/test가 PR 본문 및 commits에 특정됨. 별도 plan 없음. | 시험→구현→문서→표현 수정 순서가 한 PR 안에서 보임. 사전 plan은 없음. |
| PR/독립 작업 분할 | PR 단위 단일 문서 주제, 내부 병렬 분담 근거 없음. | 구현과 시험이 한 PR에서 결합. 늦은 통합 근거 없음. | 두 커밋이 같은 PR 안에서 결합. cross-PR interface 분할 근거 없음. | 단일 사건 네 커밋이며 독립 PR 간 통합 근거 없음. |
| 변경 뒤 spec/plan 갱신 | 선행 spec/plan 없어서 갱신 여부 판정 불가. #404는 리뷰 후 정책 문구를 수정했다고 본문/후속 commit에서 확인. | 선행 spec/plan 없음. 후속 문서 인계 증거 미확인. | 선행 spec/plan 없음. 후속 문서 인계 증거 미확인. | 운영 가이드는 구현 이후 같은 PR에서 갱신. spec/plan 갱신 여부는 판정 불가. |
| 검증 보고·근거 | diff/gate 명령은 본문 주장. 제품 UI는 없음. GitHub status는 CodeRabbit 상태. | focused+full suite 결과는 본문 주장, 재수행 없음. CodeRabbit status pending. | origin-coherence·뮤테이션·unit 결과는 본문 주장, 재수행 없음. CodeRabbit status success. | red/green 시험과 재실행 결과는 본문 주장, 재수행 없음. CodeRabbit status success. |

가설 H1–H4는 위 증거로 자동 채점하지 않는다. H1은 모두 당시 spec/plan 부재로 중요한 근거 부족이다. H2는 네 사건 모두 UI가 아니어서 비적용이다. H3는 이 PR들이 외부 인터페이스가 여러 독립 PR 뒤늦게 합쳐져 실패했다는 계보를 보이지 않는다. #326의 여러 launch 경로는 통합 위험이 있는 경계였지만, PR 변경·시험 묶음 자체가 해당 문제를 입증하지 않는다. H4는 #363/#326/#301이 결과를 바꾸는 구체 test를 보고한 점이 우려에 반대되는 신호다. 그러나 계획 시점 문서가 없어 템플릿 원인이 아니라고 확정할 수 없다.

## 이전 PR 122건의 모집단 제외

2026-09-14 이전이며 30개 정규 intent entity에 제목·head-ref·명시적 본문 intent·diff 경로의 직접 연결이 없는 PR은 adopted-template 조사 모집단에서 제외하고 원 번호/제목/상태/변경 경로를 별도 JSON에 보존했다. 이는 영향이나 선행 인과관계가 없다는 판정이 아니라, 전 채택 이전 역사를 모두 복원하는 목표가 아닌 현재 조사 경계다. 나중 case와 직접 연결된 선행 흔적은 case inventory에 남겼다. PR별 전체 목록과 경로 root 그룹은 [curated-scope-adjudication.json](../../../../.local/research/openwebagent-template-history/20261003/collection/api/curated-scope-adjudication.json)의 `pre_adoption_unlinked_exclusions.groups`에 있다.

그룹 기준은 각 PR에서 변경된 경로 root 중 사전순 첫 항목이다. 이건 자료를 나누는 표식이고 같은 root가 같은 개발건이라는 뜻은 아니다.

| 경로 root | PR 수 | 제외 근거 |
|---|---:|---|
| `apps` | 38 | 채택 경계 이전이며 현재 intent entity를 가리키는 직접 근거 없음. |
| `docs` | 64 | 채택 경계 이전이며 현재 intent entity를 가리키는 직접 근거 없음. |
| `deploy` | 7 | 채택 경계 이전이며 현재 intent entity를 가리키는 직접 근거 없음. |
| `scripts` | 6 | 채택 경계 이전이며 현재 intent entity를 가리키는 직접 근거 없음. |
| `.github` | 4 | 채택 경계 이전이며 현재 intent entity를 가리키는 직접 근거 없음. |
| `.gitignore` | 2 | 채택 경계 이전이며 현재 intent entity를 가리키는 직접 근거 없음. |
| `CLAUDE.md` | 1 | 채택 경계 이전이며 현재 intent entity를 가리키는 직접 근거 없음. |

원 PR 본문, 변경 파일 목록, commit graph, issue-comment 원본, formal reviews, inline comments, check runs와 commit status는 private collection에 보존했다. 보고서 링크는 사건 원본과 자동 댓글을 열기 위한 것이며, 자동 댓글을 승인이나 사람의 판정으로 대신하지 않는다.
