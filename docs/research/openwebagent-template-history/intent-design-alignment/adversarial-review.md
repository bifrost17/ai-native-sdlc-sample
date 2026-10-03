# 의도·설계 정합성 보완안 독립 적대적 리뷰

Status: draft. 검토일: 2026-10-03, Asia/Seoul.

이번 설계 범위에서 수정이 필요한 중요한 누락·모순·목적 불합치·과잉 부담을 찾지 못했다. 기존 작성·feedback의 변경 진입을 보완하고 중요한 선택의 이유를 실제 spec에 남기는 방향은 사용자가 요청한 얇은 보완과 맞는다. 이는 문서 설계에 대한 검토 결과다. 실제 누락 방지, 토큰 절감, 설치·자동 선택·모델 행동의 효과는 판단하지 않았다. 이 리뷰는 사람의 수락이나 활성 적용 권한을 부여하지 않는다.

## 기준판과 검토 범위

작업 디렉터리는 `/Users/jake/Projects/ai-native-sdlc-sample`, 브랜치는 `codex/plan-specificity-policy`, HEAD는 `c724213a7e4dc9233198df8b57eff523c4dbdb89`였다. 선택형 source의 plugin 표시는 0.1.9다. 검토 당시 `git diff --name-only c724213 -- tdd-optional docs/verification/north-star-playbook.html`에는 변경이 없었다. 새 연구 문서는 untracked, 제작 intent/spec/plan에는 WIP가 있었다. HEAD가 이 설계 초안의 커밋이라고 해석하지 않는다.

대상은 [정본 설계](README.md), [현행 안내 조사](current-guidance.md), [독립 제안](astra-proposal.md) 전문이다. 제작 사슬의 intent와 이번 FR11·AC10·SP10·T14 및 관련 제약을 대조했다. U1–U7 구현 전체, 0038 실험의 원본 감사, 전체 0028 완료 판정은 범위 밖이다. 현행 조사와 독립 제안이 적은 `52a5678`은 작성 당시 판으로 보존하며, 이번 리뷰의 현재판은 위 HEAD와 아래 파일 해시다.

북극성 Lesson 2·3·8의 본문과 관련 주석, 현재 intent/spec 양식, capture-intent/design-spec, sdlc-feedback, PROCESS/GIT-WORKFLOW/REVIEW, Codex verifier의 공통 기준, U7 사용·검사 계약을 직접 읽었다. F01의 intent/spec/plan은 작은 변경의 문서 부담을 대조하는 데 사용했다. F01 제품 코드·고정 입력 전체와 실행 결과를 다시 감사한 것은 아니다.

설계 검토에는 설치된 `sdlc-feedback`(기재판 0.1.7), `spec-policy-pass`(기재판 0.1.6)를 읽고 프로젝트 source와 검토 기준을 우선했다. 작성에는 `stop-slop-ko`, `brand`(각 기재판 0.1.6)를 적용했다. 실제 경로는 `/Users/jake/.agents/skills/{sdlc-feedback,spec-policy-pass,stop-slop-ko,brand}/SKILL.md`이며 설치 manifest를 독립 검증하지는 않았다. maker 루트에는 PROJECT-POLICY.md가 없어 제품 예시의 빈 P1을 새 승인 의무로 적용하지 않았다. 제품 endpoint·민감 필드·로그·UI를 설계하지 않아 API·데이터·UX 정책 변경은 검토 범위에 넣지 않았다.

## 북극성과 현행 규칙 대조

Lesson 2의 V2-03·08·09·10·11은 요청자의 무엇·왜·제약, 해결 제안과 확정 제약, 질문과 원저자 정정을 구분한다. 정본의 출처·이유 확인과 intent 부분 정정은 이 목적을 유지한다. 모든 FR/NFR를 intent에 역기입하거나 모든 후속 발화를 새 의도 문서로 만드는 규칙은 도입하지 않았다.

Lesson 3의 V3-09·10·11은 실제 문제 해결 여부, 미결 질문 처리, 우려의 책임자, 요청과 결정의 기록을 연결한다. 정본은 설계 위임 안의 선택을 진행하면서도 중요한 목표 충돌을 숨기지 않도록 한다. V3-09의 0024 관측에는 목표가 같아도 낡은 “항상 세 줄” 제약이 남았다가 HUMAN이 복구한 사례가 있다. 정본의 “목표가 같아도 낡은 제약은 남기지 않는다”는 경계가 이 반례를 다룬다. 이 과거 관측을 새 보완 효과의 실증으로 확대하지 않았다.

Lesson 8의 V8-02는 작업 중 피드백과 끝의 새 문맥 검토를 구분한다. 정본이 편입 전 의미 대조를 기존 세션에 두고 기존 설계 검토를 재사용하는 방식은 이에 어긋나지 않는다. 별도 모델을 매번 호출하지 않는다고 마지막 검토를 없애는 내용도 아니다. 북극성의 파일 쌍·검토·피드백 설명에서 새 형식 hook이나 전수 매핑 의무를 도출하지 않았다.

현행 design-spec의 요구 근거·인과 설명과 feedback의 현재 intent 제약 대조·영향 정본 갱신은 이미 충분한 규칙이다. 현재안은 이를 “새로 발명한 의도 검토”로 소개하지 않고, 제안이 요구로 굳기 전의 이유·전제 판단 시점을 보완 대상으로 좁혔다. 작성 예시가 기본 자동 로드되지 않는다는 한계를 고려해 feedback과 PROCESS에도 진입 책임을 연결한다. 자동 선택 성공은 아직 확인하지 않았다.

## 반례별 판단

아래는 문구와 경계를 대조한 설계 리뷰다. 모델에 입력해 실행한 시나리오나 시험 결과가 아니다.

| 반례 또는 위험 | 대조한 근거 | 판단 |
|---|---|---|
| 목적은 그대로인데 모든 spec 편집에 intent 동반 수정을 요구 | 정본의 짧은 대조 4, 상황 표, hook 대안; 현행 feedback Change or acceptance | 의미가 바뀐 문서만 고친다. 형식적인 intent 개정을 요구하지 않는다. |
| 오래된 intent가 명확한 새 사용자 목표를 막음 | 정본 역할 구분·상황 표·카드 UI 예시 | 최신의 명시적 목표 변경을 사용하고 재승인 없이 하류를 맞춘다. |
| “설계는 맡긴다”를 목적 교체 허가로 확대 | 정본 짧은 대조 3·충돌 상황 행 | 위임 내 기술 선택은 진행하지만 불명확한 목적·고정 제약 변경은 드러낸다. |
| “좋다”라는 추천 채택을 성능·보안 전제 검증으로 취급 | 정본 역할 구분·전제 반증 행; 독립 제안 지식과 결정의 구분 | 채택 범위와 전제의 사실성을 분리하고 틀린 추천을 정정한다. |
| 사람이 틀린 전제를 계속 주장하므로 그대로 계약화 | 정본 전제 확인·반증·권한 문단; 독립 제안 질문과 반론 | 근거·영향·대안을 제시한다. 사실과 선호, 목적 결정과 정책 예외를 구분한다. |
| 모든 이유가 부족하다고 질문하고 가역적인 내부 선택까지 중단 | 정본 중요성 기준·정상 선택 행; 독립 제안 작은 가역적 선택 | 결과를 크게 바꾸는 미정만 질문한다. 독립 작업과 위임 안의 선택은 계속한다. |
| 원래 intent 자체가 오해됐는데 “목적 불변”으로 정정 거부 | 정본 짧은 대조 4; 독립 제안 의도를 바꾸는 경계 | 핵심 배경·잘못 기록한 의도와 낡은 제약을 부분 정정한다. |
| 새 목적에 맞춰 intent를 먼저 바꿔 충돌이 없었던 것처럼 만듦 | 정본 출처 구분·왜 발명 금지·현재/과거 구분; 독립 제안 의도 개정 경계 | 사용자 결정의 출처와 개정 이유를 보존한다. 구현 결함에 맞춘 사후 정당화도 허용하지 않는다. |
| 여러 작은 선택은 각각 정합하지만 누적으로 대상·성공·비용이 바뀜 | 정본 큰 설계와 새 세션; 독립 제안 큰 설계와 비용 관리 | 기존 묶음 인계에서 누적 효과를 대조한다. 매 턴 승인이나 새 주기 검사를 추가하지 않는다. |
| 한 spec만 읽어 다른 정본의 공유 제약을 놓침 | 정본 전체 설계 인계; 현행 spec 양식·design-spec 전체 선언 집합 | 영향 부분 검토와 전체 인계를 구분하고 전체 준비 완료 주장에는 전체 선언 집합을 유지한다. |
| 새 세션이 과거 승인판·현재 WIP·대화의 이유를 섞음 | 정본 새 세션 문단; 현행 design-spec/feedback/PROCESS | 현재 문서·판·미결·실제 색인을 읽는다. 없는 이유를 추측하거나 구판 수락을 새 내용에 소급하지 않는다. |
| 직접 사용자 요청이 없는 기술·정책 설계를 억지로 intent에서 도출 | 정본 정책/기술 제약 문단; 현행 Requirements 근거 | 정책·관측·현재 계약도 정당한 근거다. 사용자 발언과 연결되지 않는다는 이유만으로 필요한 설계를 금지하지 않는다. |
| 모든 결정에 ID·짝 표·별도 장부가 필요해 F01도 비대해짐 | 정본 실제 spec 근거·후속 구현 부담 제한; F01 기존 R/SP/T | 경로·절과 기존 인과 설명을 사용한다. 새 필수 열·전수 매핑·모델 호출을 완료 조건으로 삼지 않는다. |
| U7가 intent 경로를 받았으므로 의미 일치가 인증됨 | 정본 hook 절; U7 README 커밋 전 사용·검사 계약 | 선언 문서 포함과 의미 판단을 분리한다. 거짓 빈 목록·재계산·본문 누락의 한계를 숨기지 않는다. |

## 중요한 발견과 수정 권고

**Bugs:** 이번 설계 경계에서 중요한 모순을 찾지 못했다. 전제의 실제 확인 방법은 현행 design-spec의 탐색·미결 영향·의존 인계 규칙과 결합해 읽었다. 설계를 무효화하는 미정을 표기만 하고 하류를 준비 완료로 넘길 수 있다는 해석은 그 기존 규칙과 맞지 않는다.

**Security:** 새로운 실행·데이터·권한 경계를 만들지 않는다. 정책 예외를 일반 설계 위임에서 추론하지 않는 방향을 확인했다. 실제 제품 보안이나 U7 구현의 우회 가능성을 다시 검증하지 않았다.

**Policy and scope:** 새 의미 검사 hook, 새 승인 단계, 전수 의도 ID 장부, 매번 독립 검토를 도입하지 않는 범위가 FR11·AC10·SP10·T14와 맞는다. 연구 제안의 현행 source 반영은 후속 작업으로 남아 있다. 이 리뷰를 해결하기 위한 활성 source 수정 권고는 없다.

구현 시에는 정본이 이미 정한 부담 제한을 유지해야 한다. 특히 긴 연구 전문을 여러 스킬에 그대로 복제하거나, 중요한 선택의 근거가 이미 충분한 사례에 새 문장·양식을 추가하면 이번 설계의 채택 목적에서 벗어난다. 이는 현재 발견의 수정 요구가 아니라 후속 구현에서 대조할 조건이다.

## 남은 한계

현재안은 의미 판단의 성공을 보장하지 않는다. 작성자·사람·독립 검토자가 동일한 잘못된 전제를 공유할 수 있다. 중요한 선택을 작다고 오판하거나 누적 전환을 놓칠 가능성도 남으며, 새 세션에서 기록이 불충분하면 필요한 질문이 다시 생긴다. 이를 전수 검사와 영구 장부로 없애는 것은 이번 목표가 아니다.

정본의 후속 검증 표는 정상 개정의 부담, 명확한 목적 변경, 중요한 전제 반증, 새 세션과 실제 정본 갱신을 다룬다. 후속 실행에서는 문서 최종 형태 외에 질문·충돌 발견과 의존 작업의 순서를 관찰해야 한다는 독립 제안도 보존돼 있다. 반복 수·모델·예산과 개선 효과는 미정이며 설계 검토 결과로 채우지 않았다.

제품 실험·시험·추가 모델 호출·설치·버전 갱신은 실행하지 않았다. 이 리뷰에서 수정한 파일은 본 파일 하나다. 최초 검토 결과는 유지하며 이후 설계가 바뀌어 재확인하면 해당 범위와 새 해시를 아래에 추가한다.

## 읽은 파일의 SHA-256

해시는 열람판 식별용이다. 파일 전체 주장의 독립 실증이나 모든 과거 이력의 감사를 뜻하지 않는다. spec/plan은 이번 설계 범위와 관련 제약을 읽었다.

```text
d073af17408007f8097b6e592b9831d30f13b04bf4b788c35a1659cef509385a  docs/research/openwebagent-template-history/intent-design-alignment/README.md
478d551e871940567c8d0222ad39d8b1128d6afbb8bce61cb81463eee1cd3bdd  docs/research/openwebagent-template-history/intent-design-alignment/current-guidance.md
b761b51d7402757f65cae111e1c5be1e35053582b9bc527ab9fd5dd9f22db971  docs/research/openwebagent-template-history/intent-design-alignment/astra-proposal.md
d6469aee8f3646dad8b1f578d78baa983d17f3ff5499a72ca7538b0ef19dfb35  docs/verification/north-star-playbook.html
d89951d382047eb7b8b4157297a43e2c3409487791d3fea6a140c835a8a32ddf  intent/0028-openwebagent-history-feedback/intent.md
977df6283d85214a43749ee2b8d367c808204230ad3f7f6dfe2368217c5e1733  intent/0028-openwebagent-history-feedback/spec.md
9a68a15b349e049dab4be2b6595defcf90ec8cd7b9b28dbda69b01c520940f5f  intent/0028-openwebagent-history-feedback/plan.md
ed0a1cc1307daa7c03c72a48b988e87d4b3c4d614987eaa9783c6f955ecbddb7  tdd-optional/project/templates/intent.md
d52f4293f164399b6724f37acedc40bc720fa96ac81104112e05d4fd7f18a6ed  tdd-optional/project/templates/spec.md
9ae45ab728a0206b5852fe15aad0439344069e8effe84588e791afcd9cd80655  tdd-optional/project/examples/skills/capture-intent/SKILL.md
ee0af34532bb55367a0cc9907c1e9c8ddcf783dc8b9990b84fa6b9bda9dddfa3  tdd-optional/project/examples/skills/design-spec/SKILL.md
6aa27117d46060122b9aa58a3918b73a76200d4f9053481ad3c6d0b3178d955d  tdd-optional/org-skills/skills/sdlc-feedback/SKILL.md
dd811217033a866c3d6502d7dae2d5a68a775a090cf8b8e43ec56792cd586da1  tdd-optional/project/docs/PROCESS.md
71e5f69c80504434d53f396ab3b34917f2f8522fa57ba67bb60089b6a0c93fcf  tdd-optional/project/docs/GIT-WORKFLOW.md
7587cae2849954087a28da9d5258373416e27075041d06d7c5ee1bca1180f2a2  tdd-optional/project/REVIEW.md
c34eb0d9970546dd8855d9068fde2f6fb6c770c535fcc73f384de0e298ef593c  tdd-optional/org-skills/codex/agents/sdlc-verifier.toml
a40542cbed6b40f17be3ed53da35df23401d8113e2d55c50a45015029162db0f  tdd-optional/org-skills/examples/document-sync-hook/README.md
ca5a6758b93491b6407eb5a7d6da6bc6ccc1819897653e4cbe767d42a1c08f0b  CLAUDE.md
bfd4554f2f753bca5374d732f4733fe48cd3f4a97d94a491d7cda1dc88aae696  REVIEW.md
0fd99a19650beba4b2789ce38e42b7af83db5cc1e859e35e82a63e8231245c3b  tdd-optional/project/docs/sdlc-authoring/examples/F01/intent.md
ed2f3c2bd8bf6f1719f909dad34b74b2cb019799eb8e53c949d2de10f56d3b63  tdd-optional/project/docs/sdlc-authoring/examples/F01/spec.md
cc5c7cf18104ad499863675ddcf7859cb5f45296a612d568471d5b1ee56cef81  tdd-optional/project/docs/sdlc-authoring/examples/F01/plan.md
```

## 후속 문구 재확인

2026-10-03, Asia/Seoul. root가 알려 준 정본의 두 개정을 직접 다시 읽었다. 기존 문맥 재사용은 같은 판과 관련 결정이 바뀌지 않은 경우로 한정하며, 판·결정 변경 또는 문맥 상실 때 현재 내용을 확인하도록 명확히 했다. 이는 이미 검토한 현재판 대조의 조건을 드러낸 것으로, 반복 전체 읽기나 새 장부를 요구하지 않는다. 중요한 발견이 없다는 최초 판단은 유지한다.

사용자 요청 원문과 `request-manifest.json`의 보존 경로를 정본 끝에 추가한 것도 확인했다. 해당 private 원본·manifest의 바이트와 원 세션을 이번 리뷰에서 독립 대조하지는 않았다. 보존했다는 정본 설명과 실제 원본 감사는 구분한다.

재확인한 정본 SHA-256은 `ba61fd64c2d22439ff4ea31141390126e018bfc1fcbf921a1b7b6e76b367d1a9`다. 위의 `d073af…`는 최초 열람판으로 남긴다. 이 재확인은 변경된 문구 두 곳에 한정하며 추가 제품 시험·모델 실행은 하지 않았다.
