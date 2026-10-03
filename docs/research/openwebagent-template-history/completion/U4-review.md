# U4 적대적 리뷰 — 개발건과 현재 정본

2026-10-03 Asia/Seoul. 검토 대상은 미배포 0.1.9 후보의 개발건/현재 정본 안내와 이번 U4 diff다.
최초 검토에서 중요한 지적 1건(P2)을 발견했고, root 수정 후 해당 경계를 다시 읽어 해결을 확인했다.
최종 검토 범위에 남은 중요한 지적은 없다. 제품 실험·전체 패키지 통과·사람의 수락을 뜻하지 않는다.

## 대상과 권한

작업 위치는 `/Users/jake/Projects/ai-native-sdlc-sample`이며 실제 diff base와 검토 시작 HEAD는
`e7ed3fad46fd76bcbf5ce0438a034432be1ec4bf`다. 최초 범위는 다음 다섯 파일의 현재 전문과 base 대비
미커밋 변경이다. 기존 0.1.9 후보에 이미 있던 개발건·정본 문장도 함께 검토했다.

- `tdd-optional/project/changes/README.md`
- `tdd-optional/project/docs/PROCESS.md`
- `tdd-optional/project/examples/skills/capture-intent/SKILL.md`
- `tdd-optional/project/examples/skills/design-spec/SKILL.md`
- `tdd-optional/project/examples/skills/plan/SKILL.md`

필수 인접 참조로 `GIT-WORKFLOW.md`, `traceability.md`, `REVIEW.md`, 조직 `sdlc-feedback`와 그
verifier 기준을 실제 읽었다. root의 수정 후 재검토에는 `GIT-WORKFLOW.md`의 세 변경부를 추가했다.
다른 WIP는 `git status --short`로 구분했고 수정·정리·stage하지 않았다. 리뷰자의 유일한 작성 파일은 이 보고서다.

루트 `AGENTS.md` 파일은 없었으며 대화로 주어진 모델/추론 수준 지침과 `CLAUDE.md`를 확인했다.
프로젝트 `.claude/agents/verifier.md`도 읽었다. 사용자에게서 전달된 U4 범위에 따라 전체
`make check`, strict/adapter 검사와 인접 hook 실행은 U6에 남겼다. 이 제한 때문에 전체 verifier 실행
완료로 보고하지 않는다. 모델 CLI·브라우저·개발 실험·전역 설치·푸시·병합은 실행하지 않았다.

## 북극성과 요구 추적

북극성 `docs/verification/north-star-playbook.html`의 다음 본문과 주석을 먼저 읽어 판단 기준으로 삼았다.

| 기준 | 실제 의미와 U4 적용 |
|---|---|
| V3-11, 532–537행 | spec을 intent 옆에 기록해 요청과 결정을 함께 찾게 한다. 디렉터리 이름을 changes로 정하는 것은 팀 선택이며 기존 intent 이사를 요구할 근거가 아니다. |
| V3-14, 554–559행 | 살아 있는 정책과 실제 스킬 판을 읽고 사람의 수락을 보존한다. 과거 승인·문서 번호로 현재 계약을 자동 결정하지 않는다. |
| V4-06, 616–623행 | 현재 구현 계획이 실제 파일·순서·증명을 연결해야 한다. 총괄 표는 그 plan을 찾는 색인이며 계획이나 증거를 대신하지 않는다. |
| V4-08, 630–645행 | 대화를 못 본 담당자가 선언된 입력으로 이어갈 수 있어야 한다. 주석의 제한된 새 문맥 관측을 모든 제품의 성공 근거로 확대하지 않았다. |
| V4-11, 658행 이하 해당 주석 | 이탈한 계획은 구현과 같은 commit에서 갱신한다. hook은 선택이고, 후속 복구를 처음부터 자발적 성공이었다고 소급하지 않는다. 색인 유무는 현재 plan 갱신을 면제하지 않는다. |
| V8-02, 1130–1137행 | 작업 중 feedback과 새 문맥 최종 검토의 역할을 구분한다. 이번 문서 리뷰가 실제 구현 효과나 사람의 결정을 대신하지 않는다. |

현재 chain의 `intent.md` 19–28, 33–40행은 제작 보완의 순차 검토와 제품 실험 유예, 얇은 보완을 정한다.
`spec.md` FR07·FR08, SP05·SP07, AC03·AC06·AC07 및 `plan.md` T09를 대조했다.
이번 diff의 기존 경로 선택과 현재 계약 대조는 SP05/FR07/AC06에, 발견·수정·재검토 보존은
SP07/FR08/AC07에 해당한다. U1–U3 완료 표기나 과거 PASS는 U4 수락 근거로 사용하지 않았다.

## 최초 발견

### U4-F1 — P2: 인계·머지 단계가 기존 제품에 두 번째 색인을 요구할 수 있음

최초 읽은 `tdd-optional/project/docs/GIT-WORKFLOW.md` 64–66행은 PROCESS를 따른 뒤
“[개발건 총괄 표](../changes/README.md#현재-개발건)의 관련 행도 갱신한다”고 했고,
83–84행은 머지 후 같은 파일의 “대상 판·PR·남은 범위” 갱신을 명령했다.

반례는 기존 `intent/<NNNN>-<slug>/`와 `intent/README.md`만 쓰는 제품이다.
이번 PROCESS 8–10, 50–51행과 세 작성 스킬을 따라 기존 색인에서 작업을 시작할 수 있다.
그러나 인계·머지 때 GitHub Flow의 직접 지시까지 수행하면 `changes/README.md`를 새로 만들거나
기존 표와 새 표를 함께 갱신해야 한다. 색인이 전혀 없는 제품도 해당 경로를 만들라는 요구로 읽을 수 있다.
실제 에이전트가 그렇게 행동했다는 실행 관측은 없으며, 동시에 적용할 문장 사이의 충돌을 지적한 것이다.

changes 안내 서두의 “기존 경로 유지”와 PROCESS의 “두 번째 색인을 요구하지 않는다”는 반증도 고려했다.
시작 13행의 규칙 링크만 있었다면 기존 경로를 보존하는 일반 참조로 해석할 여지가 충분했다.
하지만 두 갱신 문장은 파일과 표를 직접 지정하므로 현재색인 선택 안내만으로 갱신 대상이 하나로 정해지지 않는다.
FR07/SP05/AC06의 호환 참조와 복제 없는 색인, T09의 업데이트 누락·정본 중복 점검에 걸리는 실제 인계 문제다.

필요한 수정은 GitHub Flow의 갱신 대상을 실제 채택한 색인으로 맞추고, 색인이 없는 경우 현재
plan·기존 실행 기록을 갱신하도록 연결하는 것이다. 새 장부·검사기·승인 단계나 강제 마이그레이션은 필요 없다.
수정 책임은 root이며 리뷰자는 source를 고치지 않았다.

## 수정 후 좁은 재검토

root가 위 발견을 수용해 `GIT-WORKFLOW.md` 시작·중단/인계·머지 세 곳을 고쳤다.
현재 파일의 13–16, 65–68, 85–88행과 실제 base diff를 다시 읽었다.

- 시작: 실제 채택한 색인·규칙을 따른다. changes 안내는 새 템플릿의 기본이라고 한정한다.
- 인계: 실제 색인의 행을 갱신한다. 색인이 없으면 plan·기존 실행 기록에 인계 상태를 남기며 새 색인을 요구하지 않는다.
- 머지: 실제 색인, 없으면 plan·기존 실행 기록의 대상 판·PR·남은 범위를 갱신한다.

기존 intent 색인이 있는 제품은 같은 표를 계속 쓰고, 색인이 없는 제품도 현재 상태를 갱신한다.
새 제품은 changes 표로 이어진다. PROCESS 45–51행 및 feedback 66–75, 133–136행과 충돌하지 않는다.
U4-F1은 이 수정판에서 해결됐다. 최초 문제와 수정은 별도 기록으로 유지하며 최초판을 통과로 소급하지 않는다.

최초 GIT-WORKFLOW 본문은 base와 같았다. 해시 수집 중 root 수정이 반영됐으므로 최종 입력 표의 해당
해시는 수정판이다. 최초판은 Git 객체에서 다시 계산했다.

- 최초판 SHA-256: `82831f2d6c03e148a372f917ee74172e2cf5abf53f11b4398945ae4d4b40d93c`
- 수정판 SHA-256: `e2bb249d930ffef7a187c67210b1b0e6ac22ff25f0390a189ce7faa74da60e7d`

## 나머지 반례와 판정 근거

| 반례 | 대조한 실제 문장과 판단 |
|---|---|
| 색인 없는 구제품이 상태 갱신을 계속 생략 | PROCESS 45–49행과 feedback 66–75행은 색인 유무와 별개로 현재 plan·실행 기록을 갱신한다. 수정된 GitHub Flow는 merge 뒤에도 같은 fallback을 명시한다. 추가 결함 없음. |
| 과거 spec·더 큰 번호·과거 승인으로 현행 설계 결정 | changes 82–87, 92–97행, design-spec 13–23행은 현재 코드/설정·정책·적용할 수락 계약을 대조하고 보존·대체·미확인을 기록한다. 번호·옛 수락 자동 승계를 금지한다. |
| 실제 코드의 버그에 맞춰 spec 개정 | changes 89–90행은 구현 결함을 계약에 맞춰 수정하고 의도된 계약 개정만 별도로 다룬다. plan 84–89행, feedback 52–64·135–136행과 REVIEW 38–40행도 같은 구분이다. |
| 공통 계약을 새 spec에 복사해 정본 두 개 생성 | changes 92–95행은 공통 정본을 실제 갱신하고 대체 범위를 밝힌다. design-spec 39–41행과 traceability 18–26행은 결정별 한 정본 및 참조를 정한다. 과거 수락 판은 Git에 보존하므로 현재 계약을 낡게 둘 필요가 없다. |
| 진행 중·부분 통합·전체 완료 혼동 | changes 19–21·74–76행은 전체 합의 범위의 실제 결과와 수락 근거를 요구한다. GitHub Flow 54–55행의 부분 PR 제한, REVIEW 31–34행의 공개 수락 구분과 일치한다. 표의 상태 예시는 강제 상태 기계가 아니다. |
| 동시 신규 건 번호 충돌 | changes 47–51행은 main과 알려진 진행 작업 양쪽 경로 확인, 조율자의 배정, 충돌 시 통합 전 번호·참조 조정을 둔다. 중앙 등록 도구를 요구하지 않고 남은 경쟁의 복구도 설명한다. |
| 작은 수정마다 새 문서 세트·승인 요구 | changes 67·71–72행과 capture-intent 18–19행은 같은 건 갱신 및 오탈자·링크 정리를 구분한다. PROCESS 98–102행은 중요한 결정·위험·검증·인계만 남기도록 한다. 형식 부담을 더할 지적 없음. |
| 같은 기능의 독립 후속건을 첫 폴더에 무한 누적 | changes 62–76행은 독립 목표·수락·완료 범위로 나누며, 완료 후 기능 추가·결함·유지보수와 미완료 재개를 구별한다. 과거 개발건 진행 상태를 새 건으로 덮지 않는 80–81행과도 일치한다. |
| 기존 ID를 새 번호 체계로 전수 변경 | traceability 13–14·18–29행은 기존 R/AC/P ID를 유지하고 개발건 번호·작업 T·PR의 범위를 분리한다. 이번 diff는 이를 바꾸지 않는다. |

위 판단은 문장 의미와 참조의 정합성 검토다. 자동 스킬 선택, 실제 사용자 응답, 실제 개발 결과를 실행해
관측한 판정이 아니다. 모든 경우의 절차를 추가하거나 어휘 선호만으로 수정을 요구하지 않았다.

## 실행한 확인과 한계

명령은 작업 저장소에서 실행했고 완료된 읽기·diff·hash 명령의 exit code는 0이었다.

```text
pwd
git status --short
git rev-parse HEAD
git diff --stat e7ed3fad46fd76bcbf5ce0438a034432be1ec4bf
git diff e7ed3fad46fd76bcbf5ce0438a034432be1ec4bf -- <최초 다섯 source 경로>
git diff e7ed3fad46fd76bcbf5ce0438a034432be1ec4bf -- tdd-optional/project/docs/GIT-WORKFLOW.md
git diff --check e7ed3fad46fd76bcbf5ce0438a034432be1ec4bf -- <최종 여섯 source 경로>
git show e7ed3fad46fd76bcbf5ce0438a034432be1ec4bf:tdd-optional/project/docs/GIT-WORKFLOW.md | shasum -a 256
shasum -a 256 <아래 입력 파일>
```

`nl -ba`와 `sed -n`으로 위 입력 전문·북극성 해당 구간을 읽었다. 큰 배치 출력에서 잘린 구간은
작게 나눠 다시 읽었다. diff 공백 검사는 출력 없이 exit 0이었다. 이 검사는 링크·의미·제품 동작을 증명하지 않는다.
최초 다섯 source diff는 +19/-9, root의 해결 수정은 GIT-WORKFLOW +6/-4다.

과거 실험 원문·원제품 코드·원격 main을 새로 조사하지 않았다. 현재 지침 검토에 북극성의 과거 주석을
기준으로 사용했으며 주석에 연결된 모든 실험을 재감사했다는 뜻이 아니다. 새 통합 판·패키지 전달본·전체
회귀는 U6가 확인해야 한다. source의 변경 순서 전체나 실제 사용 시 에이전트 준수율을 추정하지 않았다.

## 읽은 입력의 SHA-256

다음 값은 이 리뷰 중 수집한 파일 바이트 해시다. GIT-WORKFLOW는 수정판이며 최초판 해시는 위에 별도 보존했다.
해시 일치 자체를 의미 검토 근거로 사용하지 않았다.

```text
ca5a6758b93491b6407eb5a7d6da6bc6ccc1819897653e4cbe767d42a1c08f0b  CLAUDE.md
de01e577a0cdaacda538c0197adff6e11eaaec32561011f13717911ac3a1b395  .claude/agents/verifier.md
56c380d188c3eeff0b6c30951d831159fc32db27f781680caa13200235cd9106  intent/0028-openwebagent-history-feedback/intent.md
ff36f8b563e39326cc161fee680b7bbdeb728eb8659cf0943618229209ab0905  intent/0028-openwebagent-history-feedback/spec.md
16e20b67481a60eca32061c69bae8a34b4ca166db6267f8c4d684712ae46ac4a  intent/0028-openwebagent-history-feedback/plan.md
baafed96eb52e3243c78cfd48f9de2f25a7d15a9276b28e54a9edcf6130d6335  docs/research/openwebagent-template-history/completion/README.md
e11f73355e5b2ec329f6d485487341ebc6d15aa7a54c4d4a5a7ef4f17329ca50  docs/verification/north-star-playbook.html
47237bcd01ebcfe6dcd2d23bf8e940011cb575eb776464a8c90c9274cbf6d1f6  tdd-optional/project/changes/README.md
dd811217033a866c3d6502d7dae2d5a68a775a090cf8b8e43ec56792cd586da1  tdd-optional/project/docs/PROCESS.md
9ae45ab728a0206b5852fe15aad0439344069e8effe84588e791afcd9cd80655  tdd-optional/project/examples/skills/capture-intent/SKILL.md
ee0af34532bb55367a0cc9907c1e9c8ddcf783dc8b9990b84fa6b9bda9dddfa3  tdd-optional/project/examples/skills/design-spec/SKILL.md
991046cef4e122f711f1c3cdcf4afa3169bcf6cbc86ac78a5264089c4e64ec0f  tdd-optional/project/examples/skills/plan/SKILL.md
e2bb249d930ffef7a187c67210b1b0e6ac22ff25f0390a189ce7faa74da60e7d  tdd-optional/project/docs/GIT-WORKFLOW.md
2d8f3493dc90199b7ccabd002a5ca862fce33e36b3510ab77707a527d8ec7ab6  tdd-optional/project/docs/sdlc-authoring/traceability.md
7587cae2849954087a28da9d5258373416e27075041d06d7c5ee1bca1180f2a2  tdd-optional/project/REVIEW.md
f9f3c509c95196b1b349242d9dd29c3957020eeb3c0113a7686a659ad8342bfb  tdd-optional/org-skills/skills/sdlc-feedback/SKILL.md
6011efd7c8de0ad092db19751364d890dafbca6d390560aaeae3c1855e1e617a  tdd-optional/org-skills/agents/sdlc-verifier.md
```

## 최초 U4 실제 diff 전문

```diff
diff --git a/tdd-optional/project/changes/README.md b/tdd-optional/project/changes/README.md
index 75acba8..3223fe3 100644
--- a/tdd-optional/project/changes/README.md
+++ b/tdd-optional/project/changes/README.md
@@ -86,6 +86,9 @@ spec.md는 설계의 진입점이며 필요한 상세 문서를 연결한다. 
 앞선 설계 전체를 복제하지 않아도 되지만, 새 spec과 선언된 참조만으로 이번 계약을 이해할 수 있어야 한다.
 새 plan은 그 spec을 기준으로 실제 변경 파일·작업·검증과 이전 기능의 회귀를 연결한다.
 
+현재 코드와 수락된 계약이 다르면 차이를 먼저 확인한다. 구현 결함은 계약에 맞춰 고치며, 실제 코드가
+다르다는 이유만으로 spec을 바꾸지 않는다. 의도된 계약 개정이면 관련 결정과 영향받는 설계를 갱신한다.
+
 현재도 사용하는 공통 설계 정본이 있으면 그것을 확인하고, 영향받는 파일은 함께 갱신해 새 spec에서 연결한다.
 과거 기록을 보존한다는 이유로 현재 적용할 계약을 낡은 상태로 두지 않는다. 이전 수락 판과 근거는 Git에 보존하며,
 같은 결정의 정본이 둘이 되지 않도록 새 spec에 대체하는 범위를 밝힌다. 번호가 더 크다는 사실만으로 계약을 덮어쓰지 않는다.
diff --git a/tdd-optional/project/docs/PROCESS.md b/tdd-optional/project/docs/PROCESS.md
index ee1b498..2804cff 100644
--- a/tdd-optional/project/docs/PROCESS.md
+++ b/tdd-optional/project/docs/PROCESS.md
@@ -5,7 +5,9 @@
 책임자가 읽고 결정할 수 있도록 작성한다. 문서 형식과 승인 상태를 판정하는 자동 검사는 이 템플릿에
 포함하지 않는다. 실제 코드와 동작의 검증 방법은 프로젝트가 정한다.
 
-착수할 때 [개발건 규칙](../changes/README.md)으로 기존 개발건과 이번 목표를 확인한다.
+착수할 때 실제 채택한 색인·규칙으로 기존 개발건과 이번 목표를 확인한다. 새 템플릿의 기본은
+[개발건 규칙](../changes/README.md)이며, 기존 `intent/` 제품은 기존 색인·경로를 사용한다.
+색인이 없으면 현재 개발건·plan과 프로젝트 규칙을 먼저 확인한다. 경로 이사나 두 번째 색인을 요구하지 않는다.
 진행 중인 같은 목표의 수정은 기존 문서를 갱신하고, 독립된 후속 개발·유지보수는 새 개발건으로 연결한다.
 폴더 이름을 정하거나 PR을 나누는 일은 별도의 승인 단계가 아니다.
 
@@ -45,8 +47,8 @@
 Git의 staged·unstaged·untracked 상태, 실행 근거를 대조한 뒤 의존 작업을 잇는다. 충돌하거나 빠진 결정은
 드러내고 영향받는 후속 작업을 준비 완료로 단정하지 않는다. 강제 종료를 막았다고 주장하지 않으며,
 단순 상태 질문은 이 개정·실행 사건을 시작하지 않는다.
-개발건의 현재 상태·대상 판·다음 작업은 [총괄 표](../changes/README.md#현재-개발건)의 관련 행에도
-연결하되 plan과 시험 출력을 복제하지 않는다.
+개발건의 현재 상태·대상 판·다음 작업은 실제 채택한 색인의 관련 행에도 연결하되 plan과 시험 출력을
+복제하지 않는다. 새 템플릿에서는 [총괄 표](../changes/README.md#현재-개발건)를 사용한다.
 
 ## 구현계획의 구체성
 
diff --git a/tdd-optional/project/examples/skills/capture-intent/SKILL.md b/tdd-optional/project/examples/skills/capture-intent/SKILL.md
index 8977dd6..f96ee7a 100644
--- a/tdd-optional/project/examples/skills/capture-intent/SKILL.md
+++ b/tdd-optional/project/examples/skills/capture-intent/SKILL.md
@@ -12,8 +12,9 @@ disable-model-invocation: true
 해결책부터 제안받았다면 바라는 개선을 확인하고 제안 자체도 Proposed outcome에 보존한다.
 제안자가 필수라고 확인한 것만 제약으로 기록한다. 관측 사실과 원인 추정을 구별한다.
 
-먼저 프로젝트의 `changes/README.md`에서 기존 개발건을 이어갈지와 번호·이름 규칙을 확인한다.
-이미 `intent/`를 채택한 제품은 그 경로를 자동으로 옮기지 않고 기존 기록과 참조를 확인한다.
+먼저 프로젝트가 실제로 사용하는 개발건 색인·규칙에서 기존 건을 이어갈지와 번호·이름을 확인한다.
+새 템플릿의 기본 색인은 `changes/README.md`다. 이미 `intent/`를 채택한 제품은 기존 색인과 경로를
+사용한다. 색인이 없다면 현재 개발건·plan과 프로젝트 규칙을 확인하며 경로 이사나 두 번째 색인을 요구하지 않는다.
 프로젝트의 `templates/intent.md`를 사용해 해당 변경 폴더의 `intent.md`를 작성하거나 필요한 부분만 갱신한다.
 후속 요청이라고 매번 새 폴더를 만들거나, 의도가 그대로인데 형식적으로 다시 쓰지 않는다.
 제안자의 사실을 대신 만들지 않으며, 양식의 빈칸은 실제 내용이나 답을 기다리는 질문으로 바꾼다.
diff --git a/tdd-optional/project/examples/skills/design-spec/SKILL.md b/tdd-optional/project/examples/skills/design-spec/SKILL.md
index 3e76fe4..ee1d916 100644
--- a/tdd-optional/project/examples/skills/design-spec/SKILL.md
+++ b/tdd-optional/project/examples/skills/design-spec/SKILL.md
@@ -12,8 +12,10 @@ Human acceptance starts planning (L3 276). These source principles remain separa
 
 Confirm the actual intent revision and recorded human acceptance, or the already-authorized draft scope.
 Keep Upstream with the actual input revision and Status draft. An old accepted version does not approve new edits.
-Find the active change through [the project's change index](../../../changes/README.md), including a retained
-`intent/` path in an already-adopted product. Treat older specs as evidence of decisions made then: compare their
+Find the active change through the project's actual index and naming rules; [changes/README.md](../../../changes/README.md)
+is the new template's default. An adopted product may retain its `intent/` path and existing index. If no index exists,
+locate the current change/plan through its actual records and project rules; do not require relocation or a second index.
+Treat older specs as evidence of decisions made then: compare their
 relevant contracts with current code/configuration, policy and currently applicable accepted agreements. State in
 the new spec what is preserved, superseded or still unverified; a higher number or past acceptance is not current authority.
 Do not ask twice when authorization already covers this work; do not invent acceptance.
diff --git a/tdd-optional/project/examples/skills/plan/SKILL.md b/tdd-optional/project/examples/skills/plan/SKILL.md
index 8845f92..7e08e47 100644
--- a/tdd-optional/project/examples/skills/plan/SKILL.md
+++ b/tdd-optional/project/examples/skills/plan/SKILL.md
@@ -10,8 +10,10 @@ disable-model-invocation: true
 North star L4 317–321: name changed files, work order and proving tests; support an engineer without the conversation.
 L4 329: update plan.md in the same implementation commit when work departs from it.
 
-Find the active change through [the project's change index](../../../changes/README.md); an adopted product may
-retain its existing `intent/` path. Read the current intent. For product planning, read the current spec.md and
+Find the active change through the project's actual index and naming rules; [changes/README.md](../../../changes/README.md)
+is the new template's default. An adopted product may retain its `intent/` path and existing index. If no index exists,
+locate the current change/plan through its actual records and project rules; do not require relocation or a second index.
+Read the current intent. For product planning, read the current spec.md and
 every declared required design document, actual
 code/tests and applicable project policies. Confirm the spec revision and human acceptance or already-authorized draft scope.
 For a bounded exploration before design acceptance, instead read the current intent/draft question, relevant product
```

## U4-F1 해결의 실제 diff 전문

```diff
diff --git a/tdd-optional/project/docs/GIT-WORKFLOW.md b/tdd-optional/project/docs/GIT-WORKFLOW.md
index ba07f32..d5bc3f1 100644
--- a/tdd-optional/project/docs/GIT-WORKFLOW.md
+++ b/tdd-optional/project/docs/GIT-WORKFLOW.md
@@ -10,7 +10,8 @@
 아닌 최신 제품 `main`에서 만든다. 브랜치 이름은 짧게 목적을 드러내며 Codex 작업은 기본적으로
 `codex/<작업명>`을 쓴다. 긴급 수정도 같은 흐름에서 필요한 검증을 거쳐 통합한다.
 
-문서 폴더의 번호·이름은 [개발건 규칙](../changes/README.md)을 따른다. 브랜치에도 변경 번호를
+문서 폴더의 번호·이름은 실제 채택한 색인·규칙을 따른다. 새 템플릿의 기본은
+[개발건 규칙](../changes/README.md)이며 기존 제품의 색인·경로는 유지할 수 있다. 브랜치에도 변경 번호를
 넣으면 연결하기 쉽다. 예를 들어 `codex/0001-export-query`와 `codex/0001-export-csv`는 같은
 `changes/0001-request-export/` 계획의 서로 다른 PR일 수 있다. 문서 폴더와 브랜치를 1:1로 만들지는 않는다.
 
@@ -62,8 +63,9 @@ PR 본문·커밋 메시지는 [전달 정책과 양식](CHANGE-DELIVERY.md)을
 의존 브랜치를 장기 통합 브랜치로 유지하지 않는다.
 
 중단·인계·재개는 별도 브랜치 규칙이 아니라 작업 사건이다. [절차](PROCESS.md)에 정한 현재 plan 요약과
-실행 근거를 실제 Git 상태와 대조하고 다음 의존 작업을 정한다. [개발건 총괄 표](../changes/README.md#현재-개발건)의
-관련 행도 갱신한다. 모든 작업의 준비 완료 판정을 새로 만들지 않는다.
+실행 근거를 실제 Git 상태와 대조하고 다음 의존 작업을 정한다. 실제 채택한 색인의 관련 행도 갱신한다.
+새 템플릿의 기본은 [개발건 총괄 표](../changes/README.md#현재-개발건)다. 색인이 없으면 현재 plan·기존
+실행 기록에서 인계 상태를 갱신하며 별도 색인 생성을 요구하지 않는다. 모든 작업의 준비 완료 판정을 새로 만들지 않는다.
 
 ## 검토와 통합
 
@@ -80,7 +82,7 @@ PR이 만들어졌다는 사실도 승인이 아니다. 기록을 남기는 위
 원본과 통합 후 커밋의 대응 및 문서 내용이 같은지 확인한 근거를 남긴다. 내용이 바뀌었다면 승인을
 자동 승계하지 않는다. 공유된 브랜치의 이력 재작성은 협의하고, `main`을 force push하지 않는다.
 
-머지 후 통합 결과를 확인하고 [개발건 총괄 표](../changes/README.md#현재-개발건)의 대상 판·PR·남은 범위를
+머지 후 통합 결과를 확인하고 실제 채택한 색인(없으면 현재 plan·기존 실행 기록)의 대상 판·PR·남은 범위를
 갱신한 뒤 완료된 작업 브랜치와 worktree를 정리한다. PR·커밋·결정 기록은 남긴다.
 문제가 발견되면 영향과 의존성을 보고 수정 PR 또는 revert PR로 대응하며, 데이터·외부 효과는 별도로
 복구한다. 머지는 배포나 기능 공개와 같지 않다. 배포·노출·되돌리기는 프로젝트의 실제 운영 방식에
```

## 다음 인계

root는 U4-F1의 최초 발견·해결판을 단위 기록에 연결하고 해당 여섯 source만 U4 범위로 다룰 수 있다.
현재 검토 범위에는 남은 중요한 지적이 없다. U5는 전달/갱신의 자체 책임 범위를 실제 파일로 검토하고,
U6는 여섯 단위의 최종 source·패키지·참조와 make check/strict/adapter를 검증한다.
제품 개발 실험은 별도 사용자 지시를 기다린다. 이 보고서는 사용자 수락·커밋·푸시·머지 권한을 추가하지 않는다.

