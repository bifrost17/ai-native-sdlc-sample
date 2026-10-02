# 현재 템플릿 비교 기준

조사 기준 시각: 2026-10-03 01:25:11 KST. 이 문서는 당시 배포 원본과 기존 WIP를 고정한다.
openWebAgent 사건의 원인 판정이나 새 템플릿 변경은 포함하지 않는다.

사용자가 허용한 범위는 **실사용 이력 분석 → 소수의 얇은 템플릿 개선 → 실제 개발 재실험 5회**다.
에이전트가 합의한 범위 안에서 설계·구현 방법을 판단하고 탐색할 여지를 보존한다. 개별 모델 실수를
모두 신규 정책·검사기·승인 단계로 바꾸지 않으며, 현재 지침으로 설명되는 문제는 중복 보완하지 않는다.

## 고정한 판과 근거

| 대상 | 실제 확인한 판·범위 |
|---|---|
| 제작 저장소 | `/Users/jake/Projects/ai-native-sdlc-sample`, `codex/plan-specificity-policy` |
| 조사 시작 HEAD | `ad98adec5c85ebb969fa394796d388df10303a1f` |
| 스냅샷 수집 HEAD | `d5e2e7bc3b0f70f80a04f0e45abedab898b360a8`; 새 0028 intent만 추가, 제품 원본 차이 없음 |
| 원격 main | `gh api repos/bifrost17/ai-native-sdlc-sample/branches/main`에서 `67739c8fe8f3a7c3159b480ebd95270888b05074` 확인 |
| 제품 원본 | `tdd-optional/project/` 75개 추적 파일. 위 세 커밋에서 내용 동일 |
| 조직 스킬 원본 | `tdd-optional/org-skills/` 68개 추적 파일, manifest `intent-sdlc-skills-optional` 0.1.8. 세 커밋과 WIP에서 내용 동일 |
| 기존 WIP 후보 | 제품의 5개 정책 파일, 32행 추가·3행 삭제. 아래 의미 차이와 원문 patch 보존 |

원문·파일별 SHA-256·초기 Git 상태·patch는 저장소의
[로컬 기준 디렉터리](../../../.local/research/openwebagent-template-history/20261003/baseline/)에 있다.
`initial-head/`, `head/`, `remote-main/`, `candidate-wip/`를 분리했다. 각 트리는 제품·조직 스킬과
maker 진입·검증자·북극성 참고를 합친 154개 파일이며, 선택한 154개 전체에서 remote main과 수집 HEAD의 차이는 0이다.
수집 중 원본 파일 변경도 0이었다. 다른 WIP는 초기 상태에 기록했고 수정하지 않았다.

`manifest.json` SHA-256은 `e9601c95b1904dd284aec52ba91f53add9558b8ae82c33c13d75d73203f3b117`이다.
초기 HEAD는 `initial-head-manifest.json`에서 별도로 검증한다. 집계 해시는 경로순으로
`path + NUL + file_sha256 + LF`를 이어 SHA-256한 값이다.

| 범위 | 기준 원본 집계 SHA-256 | 기존 WIP 집계 SHA-256 |
|---|---|---|
| project | `d57e40cf1e0c65791b4ad3f7d50bce6f62adace51114d002244ebc8354fdd16f` | `ebfa8e6e3f09c3dc70f8a2ea5a6ee1a7686ae0a03efc9d726addd2173d1e7d84` |
| org-skills | `3dd17b3f8ddefc70172bbe3cbeb249bd32971546618f932bf6f95ba8125d4351` | 기준과 동일 |

처음 잘못된 소유자 경로의 gh 조회는 404였다. Git remote의 `bifrost17`으로 바로잡아 위 성공 응답을 보존했다.
이는 원격 접근 불가나 원격 main 부재의 증거가 아니다.

## 실제 적용과 배포 원본의 구분

maker의 `.claude/skills/{capture-intent,design-spec,plan}/SKILL.md`는 제품 양식·작성 예시로 연결한다.
제품 `examples/skills/`는 명시적으로 선택하는 예시이고 그 위치만으로 자동 로드되지 않는다.
스킬의 존재·manifest 버전·파일 해시가 같다는 사실만으로 특정 개발 세션에 설치되거나 읽혀 적용됐다고 판단하지 않는다.

이 조사 세션의 `/Users/jake/.agents/skills/sdlc-feedback/SKILL.md`에는 설치 참고판 0.1.7이 표기돼 있다.
배포 원본 0.1.8과 구별하여 `installed-reference/`에 보존했다. 설치된
`/Users/jake/.codex/agents/sdlc-verifier.toml`은 비교한 배포 TOML과 원문이 같았지만, 이것도 과거 세션의
실제 verifier 선택·실행 증거는 아니다. maker의 `.claude/agents/verifier.md`는 `make check`와
maker 사슬 대조가 중심이며 제품용 공통 verifier와 역할이 다르다.

## 평가축과 이미 문서화된 대응

북극성의 본문과 해당 주석을 함께 읽었다. 주석의 과거 경로·PASS·부분 판정은 당시 범위에 남긴다.
V4-08의 새 문맥 구현 관측, V4-11의 갱신 실패·사람 복구, V8-02의 미호출·대기 구분을 현재 전체 성공으로 확대하지 않는다.
아래의 “있음”은 문서 기준의 존재이며 실제 개발에서 충분히 작동했다는 판정은 아니다.

| 평가축 | 북극성 본문·주석 | 현재 원본에 이미 있는 판단 기준 | 실제 이력에서 확인할 것 |
|---|---|---|---|
| intent 보존 | [V2-03/08/11](../../verification/north-star-playbook.html#V2-08): 요청자의 말·목표·제약과 정정 | `templates/intent.md`, `examples/skills/capture-intent/SKILL.md`: 해결 제안과 필수 제약 구분, 없는 수치 금지, 후속 요청을 기존 건에 연결 | 원 요청·사람 정정과 문서 의미가 같은가. 바뀌지 않은 intent를 형식적으로 재작성했는가 |
| spec 충분성 | [V3-04/09/14](../../verification/north-star-playbook.html#V3-09): 요구·설계, 질문 처리, 실제 정책 적용 | `templates/spec.md`, `design-spec`와 `references/design-depth.md`, `REVIEW.md`: 전체 정본 집합, 정확한 경계·실패·복구, 다른 구현자가 호환되지 않게 해석할 여지, 이월의 영향·시점 | 당시 착수에 필요한 공유 의미가 있었는가. 새 요구와 빠진 결정을 뒤늦게 발견한 일을 구분 |
| plan 실행성 | [V4-06/07/08](../../verification/north-star-playbook.html#V4-08): 파일·순서·증명, 위험·대안, 대화 없이 구현 | `templates/plan.md`, `examples/skills/plan/SKILL.md`, `references/execution-depth.md`: SP 의미→실제 코드 지점·Method→기대·검증·Done, 첫 인도, 착수 입력 | 링크/파일 목록만 있는가, 구현 방법이 연결되는가. 새 문맥 독자가 시작하고 실제 결과에 도달했는가 |
| PR 분할·통합 | [V7-05/06](../../verification/north-star-playbook.html#V7-05): 독립성·공유 파일과 작업 분할 | `docs/PR-SIZE.md`, `GIT-WORKFLOW.md`, plan: 응집된 인도, 의존 PR, 공유 계약·소유권, 최신 main 결합과 머지 후 검증; LOC 상한 없음 | 모듈별 통과를 전체 흐름 통과로 바꾸었는가. 단계별 main·일반/시험 노출·남은 범위를 확인했는가 |
| 변경·갱신 | [V4-11](../../verification/north-star-playbook.html#V4-11): 이탈한 plan을 같은 구현 커밋에서 갱신 | 제품 `CLAUDE.md`, `PROCESS.md`, `GIT-WORKFLOW.md`, `sdlc-feedback`: 실제 diff→T→SP→요구/AC→intent 제약, 다음 의존 작업 전 영향 문서 갱신, 현재 요약·재개 대조 | 최종 문서 일치와 실제 갱신 순서를 구분. 같은 커밋만으로 선행 갱신을 증명하지 않음 |
| 검증·보고 | [V8-01/02/13](../../verification/north-star-playbook.html#V8-02), [V10-05/06](../../verification/north-star-playbook.html#V10-05): 작업 중 피드백, 끝의 별도 검토, 원문 출력·사람 판단 | `TESTING-STRATEGY.md`, `REVIEW.md`, `sdlc-feedback`, 공통 verifier: 독립 기대, 선택한 검증 순서, 실제 판·명령·결과, 미실행·한계, 설계 준비/실행/수락 구분 | 문서·단위시험·모의 입력·실서버/화면·통합 근거의 범위를 구별. 실패와 사람이 복구한 결과를 보존 |

조직 스킬 비교 범위는 `skills/sdlc-feedback/SKILL.md`, `agents/sdlc-verifier.md`,
`codex/agents/sdlc-verifier.toml`이다. 세 문서는 현재 합의와 정본의 충분성, 선행 갱신과 같은 커밋의
차이, 통합 판, 독립 기대·검토 한계를 이미 다룬다. 스킬 이름이나 검토자 수를 추가하는 것으로 이 평가축을 대체하지 않는다.

## 기존 5개 WIP가 추가하는 것

| 파일 (`tdd-optional/project/` 아래) | 기준 원본 대비 의미 |
|---|---|
| `docs/PROCESS.md` | “구현계획의 구체성”을 공통 기준으로 추가. 현재 착수 범위의 구현·검증·PR 인도, 내부 선택의 재량, 후속 작업 상세화와 선행 공유 계약을 구분 |
| `CLAUDE.md`, `PROJECT-POLICY.md` | 위 공통 기준을 진입 지침·인계 기준에서 연결 |
| `REVIEW.md` | 첫 작업 시작 가능성에서 현재 착수 범위의 PR 인도 가능성으로 검토를 명확히 하고, 필요한 결정을 후속 상세화로 미루는지 확인 |
| `templates/plan.md` | 공통 기준 링크와 Input의 착수 조건 추가 |

이미 작성 예시·실행 상세에 있던 의미를 제품 정책 진입점에서 찾기 쉽게 하는 후보다.
새 클래스 목록·UML 의무·형식 검사기·승인 단계는 추가하지 않는다. 아직 이 후보의 실제 실행 효과는 측정하지 않았다.

## 사용자가 제시한 네 가설과 남은 관측

| 가설 | 현재 기준으로 설명되는 부분 | 아직 확인할 부분 |
|---|---|---|
| 설계가 부족해 변경과 plan 이탈이 잦다 | 설계 정본·공유 의미·중요 실패와 이월 제한, plan의 실제 구현 방법이 이미 있음 | 당시 읽은 판/참조가 충분했는지, 요구 변화·학습에 따른 정당한 개정인지, 빠진 결정 때문에 재작업했는지 사건별 판정 |
| HTML 시안의 심미성·기존 UI 통일성이 부족하며 설계 중 실제 UI 구현을 선호한다 | `design-depth.md`는 mock의 판·구속 범위와 화면 상태를 다룸. `PROCESS.md`·`TESTING-STRATEGY.md`는 허용된 UI 탐색·실제 관찰과 제품 편입을 허용 | W01은 정확 px/색상을 기존 포털에 맡기고 픽셀 디자인을 범위에서 제외한 합성 예시다. 실제 디자인 시스템·비교 화면·사람의 시각 판단 근거는 없음. 사용자의 실제 UI 선호를 적용할 관측 범위와 보존할 스타일을 구체 사건에서 확인 |
| 모듈 구현 후 통합이 실패하므로 전체 인터페이스·시퀀스를 먼저 정해야 한다 | 공유 계약·순서·상태·책임의 충분성과 최신 결합 판 검증이 이미 있음. W01은 사용자→UI→API→저장소 시퀀스, API/화면 상태와 실서버 e2e를 연결 | 원인과 관련된 전체 경계가 설계/첫 인도에 빠졌는지 확인. 모든 내부 메서드·도식 종류를 일괄 강제할 근거는 아직 없음 |
| 검증 방법을 설계에서 충분히 구체화하지 않는다 | spec은 대표 입력·독립 기대·실패/보존 계약, plan은 구체 시험·명령·관측·한계를 연결. W01은 모의 UI 시험과 실제 서버 흐름을 분리 | 설계에서 검증 가능성·필요 환경·독립 기준이 누락되어 이후 검증이 막혔는지 확인. 상세 명령을 모든 spec에 중복할 필요가 있는지는 미확정 |

네 가설은 조사 질문이다. 현재 문구가 있다는 이유로 현장 문제를 부정하거나, 사용자 관측만으로
원인을 템플릿 결함으로 확정하지 않는다. UI 탐색·공유 인터페이스·검증 설계의 구체 사건을 여섯 평가축에 연결한다.

## 판정 경계

템플릿 구현 결함, 북극성 원문 충실도, 당시 제작·실행 프로세스 준수는 따로 판단한다.
선택형의 버그 test-first·시험 동결 조정은 `TESTING-STRATEGY.md`가 명시한 팀 선택이며 원문과 같은 절차로 계산하지 않는다.
주석의 과거 성공 수치·합성 문서 리뷰는 이번 기준의 실험 결과가 아니다. 이 기준 작성에서는 제품 실행·UI 렌더링·설치·자동 활성화를 검증하지 않았다.

원인이 확인된 반복 사건도 현재 지침에 이미 답이 있으면 적용·전달·모델 판단·검증 범위를 먼저 대조한다.
수정 후보를 남길 때에는 아직 없는 일반 판단 기준과 중복을 지운 최소 변경을 설명한다. 실제 실행에서
줄어든 재작업과 남은 실패, 과도한 선행 확정·문서 중복으로 탐색과 구현을 방해했는지도 함께 본다.
