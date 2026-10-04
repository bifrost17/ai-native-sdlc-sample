# 현재 인계 요약 보완의 방향 검토

Status: review complete — 방향 검토, 행동 효과 미검증

2026-10-04 Asia/Seoul. Sol/high가 제작 branch `codex/intent-design-alignment`의
HEAD `ab504d85173f8f53ef03ddb913de9ca186f76515`과 root의 후속 보완 제안을 읽었다.
최초 확인 당시 작업트리는 깨끗했다. 이 문서만 작성하며 활성 source의 후속 diff는 검토 대상에
포함하지 않는다. 제품 실행·설치·시험·원 제출판 수정은 하지 않았다.

완료보고 전에 현재 plan 요약을 실제 결과로 정리하고, 기존 완료 검토의 입력에 plan 요약·채택한
개발건 색인·실행 근거의 대조를 포함하는 방향에서 중요한 모순을 발견하지 못했다. 아래 경계를
실제 문구에도 유지해야 한다. 이 판단은 구현 source의 완료나 새 모델의 행동 개선을 입증하지 않는다.

## 읽은 기준과 사건

북극성 [V4-09와 V4-11](../../../verification/north-star-playbook.html#V4-09)은 수락한 plan을
최종 diff와 대조하고, 계획 이탈을 관련 구현과 같은 커밋에 남긴다. V4-11의 0038·0034·0022 등
주석은 후속 근거에 따른 현재 인계와 사후 복구를 자발적 갱신 성공에서 구분한다.
[V7-09](../../../verification/north-star-playbook.html#V7-09)의 검증자는 실행과 plan을 대조해
발견을 보고하며 수정·승인하지 않는다. [V8-02](../../../verification/north-star-playbook.html#V8-02)는
작업 중 feedback loop와 끝의 새 문맥 검토를 구분한다. 기존 마지막 검토의 대조 범위를 구체화하는
이번 안은 이 구분과 맞는다. 모든 커밋에서 새 모델 검토를 요구할 근거는 없다.

제작 [REVIEW](../../../../REVIEW.md), maker 0028의 현재 intent/spec/plan,
팀 source의 `sdlc-feedback`과 세 플랫폼 `sdlc-verifier`, 제품 예시 PROCESS,
plan 양식과 `execution-depth.md`를 읽었다. 현재 source에는 후속 근거·중단·인계에서 실제 판과
완료/미검증/다음 일을 정리하라는 안내가 이미 있다. 다음 담당자가 현재 파일과 근거를 대조하도록
하는 기준도 있다. 이번 안은 완료보고 사건과 그 기존 검토 입력을 연결하는 보완으로 해석한다.

[0038 보고](../../../experiments/0038-document-sync-muse.md)와
[독립 대조 전문](../completion/0038-review.md)은 제품 `78ab6d5`의 plan에 이미 끝난 T03 RED가
다음 일로 남고, 원격 PR/main 절차와 로컬 인도 범위가 충돌했음을 보존한다. 새 독자가 코드·Git·
색인에서 실제 남은 일을 맞혔어도 현재 plan 전체의 정합성은 부분으로 정정했다. 기존 설치판에도
현재 요약 갱신 지침이 있었으므로 이 사례를 지침 부재의 확정 증거로 쓰면 안 된다.

[0039 보고](../../../experiments/0039-intent-design-alignment-muse.md)는 제품 `921432a`의
동작·같은 커밋·현재 색인 관측과 낡은 plan 요약을 구분한다. `완료(예정)`, `미검증: T01 실행 전체`,
`다음 한 단계: T01을 실행한다`가 실제 인도·시험 결과와 어긋났다. parent는 최종 검토 질문을
동작 영향으로 좁혔고 verifier는 이 누락을 놓쳤다. 기존 기준의 입력과 질문 범위를 연결할 이유가
있다. parent의 feedback 본문 읽기는 미관측이므로 이번 문구만의 효과나 자연 사용을 추정하지 않는다.

## 문구에 필요한 경계

완료보고 대상은 의미 있는 구현 작업 또는 인도다. 해당 완료 검토를 시작하기 전에 개발자가
현재 plan 요약을 실제 결과로 갱신하고, 그 요약과 기존 실행 기록을 검토 입력으로 준다.
기존 기록의 전문을 plan이나 색인에 복사할 필요는 없다. 아직 검토가 진행 중이면 그 상태를
완료로 적지 않는다. 검토 뒤 발견이 남은 일을 바꾸면 현재 요약을 다시 맞춘다.

plan의 현재 요약은 이 인도의 완료·미검증·다음 일을 설명한다. 하위 T의 구현과 회귀가 끝났지만
통합이나 공개가 남았다면 각각 구분한다. 현재 scope 밖의 후속 작업까지 끝내거나 매번 전체
릴리스 검토를 요구하지 않는다. 실제 완료와 사람의 수락·원격 통합·배포는 별도 사실이다.
시험 통과나 검토의 무지적 결과로 `Status: accepted`를 만들지 않는다.

검토 입력의 색인은 프로젝트가 실제 채택한 개발건 색인이다. 색인이 없는 프로젝트에 새 파일을
강제하지 않는다. 이미 채택한 색인이 현재 상태·판·다음 일을 기록한다면 그 관련 행을 plan과
근거에 대조한다. 같은 내용을 별도 완료 장부로 늘리지 않는다. 충돌을 단순 표현 취향으로 넘기지
않되, 역사적 원문이나 보존된 이전판을 현재 상태처럼 고쳐 쓰지도 않는다.

실제 대상판은 이미 존재하는 코드/시험 commit과 현재 working tree의 필요한 변경으로 식별할 수
있다. staged·unstaged·untracked 범위를 구분하고 실행 근거의 대상과 같은지 확인한다. plan이
자기 자신을 포함할 미래 commit SHA를 먼저 쓰게 하면 순환이 생긴다. 기존 baseline과 현재 변경을
연결하는 안내를 유지하고, 다음 갱신에서 확정 SHA를 참조할 수 있게 한다. SHA만 맞추기 위한
반복 commit이나 새 검토를 요구하지 않는다.

문서만 고치는 인계도 실제 요약 갱신은 할 수 있다. 그 사건에 구현 완료 검토를 새로 강제하지
않는다. 단순 현황 질문이나 prose 정정은 개정·실행 사건으로 취급하지 않는다. 설계 handoff는
아직 없는 구현·실행 성공을 요구하지 않는 기존 검토 기준을 유지한다.

## 기존 위치에 넣을 최소 표현

`sdlc-feedback`의 기존 Completion and review 진입에서 다음 뜻을 연결하면 충분하다.

> Before this completion review, update the current plan summary from actual results:
> completed and unverified work, pending dependencies and the next step. Give the verifier
> that summary, the relevant development-case index entry when the project uses one, and
> the existing execution evidence; include their consistency in the current delivery scope.

실제 구현 완료보고 전에 요약을 갱신한다는 뜻이 첫 문장에서 분명해야 한다. 기존의 meaningful
delivery boundary, pending review, prose/status 예외, helper/commit마다 반복하지 않는 문장은 유지한다.
Completion 절과 전달 입력에 같은 의무를 장문으로 중복할 필요는 없다.

plan 작성 예시의 마지막 현재 요약 안내에는 다음 사건을 추가할 수 있다.

> 재계획·중단·인계 및 구현 완료보고 전에 현재 요약을 실제 결과로 고친다. 완료·미검증·다음 일을
> 실제 대상판과 기존 실행 근거에 연결하고, 상세 출력과 이전 판단은 기존 기록에 보존한다.

PROCESS의 기존 중단·인계 문장에는 `구현 완료보고 전`을 포함하고, 기존 실제 대상 revision과
현재 작업트리/근거 대조를 재사용한다. 전달본 세 플랫폼의 기존 pause/handoff/resume 항목에는
`implementation-completion or delivery claim`을 포함하고, 프로젝트가 쓰는 색인의 관련 행과
현재 요약·실행 근거를 함께 대조한다고 쓰면 된다. 별도 review 회차나 approval 항목은 필요하지 않다.

## 반례 대조

| 상황 | 기존 검토에 포함할 판단 |
|---|---|
| T01 구현·시험이 끝났지만 plan이 T01 착수를 지시함 | 완료 요약의 중요한 불일치로 보고한다. 제품 시험 PASS로 상쇄하지 않는다. |
| 코드·색인은 현재지만 plan만 낡음 | 세 자료를 대조한다. 색인의 최신 결과로 plan을 자동 통과시키지 않는다. |
| T01 완료, 다음 T02 또는 통합이 남음 | 현재 인도 완료와 후속 미검증을 구분한다. 전체 작업 완료로 확대하지 않는다. |
| 로컬 인도만 허용됐는데 현재 요약은 PR/main을 지시함 | 최신 사람의 범위와 충돌하는 현재 인계로 보고한다. 원격 실행으로 해결하지 않는다. |
| 제품은 끝났으나 사람의 수락 대기 | 구현/검증 결과와 수락 대기를 함께 남긴다. 수락을 만들어 내지 않는다. |
| 문서와 구현을 같은 미커밋 변경에서 검토함 | 실제 base와 현재 변경·근거 범위를 식별한다. 미래 SHA를 요구하지 않는다. |
| 검토 후 요약 문구만 근거에 맞게 정정함 | changed scope를 확인한다. 모든 helper/commit의 fresh review로 확대하지 않는다. |
| 실제 code fix가 추가돼 앞 시험판과 달라짐 | 바뀐 동작의 검증·문서와 근거를 다시 맞춘다. 예전 결과를 현재판의 실행 성공으로 세지 않는다. |
| 프로젝트가 개발건 색인을 채택하지 않음 | 실제 plan과 기존 기록만 대조한다. 새 색인·장부를 요구하지 않는다. |
| 설계-only handoff 또는 단순 현황 질문 | 기존 설계 검토/질문 범위를 따른다. 구현 완료 검토·새 제품 실행을 강제하지 않는다. |
| 0038/0039의 후속 보완 source가 정적 확인을 통과함 | 새 source 확인 범위만 보고한다. 원 제출판 복구나 모델 행동 개선으로 소급하지 않는다. |

위 반례는 문서 의미 대조이며 새 실험이나 runtime 검증이 아니다. 중요 미해결 방향 지적은 없다.
실제 source가 완성되면 기존 최종 검토에서 위 경계·플랫폼 동등성·maker의 현재 요약과 실제 근거를
대조해야 한다. 0038/0039의 원 제출판과 부분 판정은 유지한다. 행동 효과를 확인할 실험은 별도 지시
범위로 남는다.

## 후속 실제 source 검토 — 2026-10-04 Asia/Seoul

최초 방향 검토를 보존한 채 root의 후속 요청으로 실제 수정판을 다시 읽었다. 이번 입력은
HEAD `18484793856036db3f21bb92b05b70468bdf6b5d`의 `git diff 1848479`와 현재 파일이다.
maker 0028의 spec FR13/SP12/AC12와 plan T16이 선언한 source·플랫폼 전달을 대조했다.
같은0.1.10 미배포 후보의 source 의미와 반례를 검토하며 수락·제작 완료·행동 개선을 판정하지 않는다.

현재 source의 의미에서 중요한 미해결 발견은 없다. `sdlc-feedback` Completion and review의
115–120행은 meaningful implementation delivery의 기존 검토 요청 전에 plan 요약을 실제 결과로
갱신하고 채택한 색인의 관련 행을 맞춘다. 135–137행은 그 요약·색인·기존 실행 근거를 같은 검토
scope에 포함한다. 동작만 확인하도록 검토를 좁히지 않는다는 문장도 있다. 이는0039 parent의
좁은 질문 때문에 인계 누락을 놓친 경우를 판단할 수 있는 입력과 범위다.

plan 작성 스킬의 마지막 갱신 안내, PROCESS의 기존 중단·인계 절, REVIEW의 구현 정합성 절도
같은 시점과 대조를 전달한다. REVIEW는 완료된 작업을 다음 일로 남긴 중요한 요약 불일치를
발견으로 보고하도록 한다. 제품의 동작·회귀 성공만으로 plan 요약의 중요한 누락을 통과시키지 않는다.
문서 전문 복제나 새로운 상태 장부는 필요하지 않다.

### 검토 후 결과 변화의 기존 연결

새 진입 문구만 보면 검토 요청 전 요약을 정리하는 시점이 명시돼 있다. 그 뒤의 결과 변화는
같은 스킬의 기존 Change or acceptance 83–86행에서 다룬다. 후속 시험이나 검토 근거가 남은
일을 바꾸면 현재 plan/handoff 요약과 다음 일을 실제 시험판·기존 근거에 연결해 다시 갱신한다.
151–158행의 Address concrete findings는 영향 artifact를 갱신하고 바뀐 근거를 완료 전에
재확인하게 한다. 기존 검토 재사용은 scope와 evidence가 유지될 때로 제한한다.

요약만 실제 근거에 맞게 정정했다면 그 changed scope를 확인할 수 있다. 코드 결함까지 고쳤다면
선택한 검증 방식으로 해당 동작·인접 회귀를 확인하고 실제 현재판과 요약을 맞춰야 한다.
검토 전 실행 성공을 바뀐 코드판의 실행 성공으로 쓰거나, 발견이 남았는데 완료를 선언하는 경우는
현재 규칙에 맞지 않는다. 기존 인도/인계의 색인 갱신 안내와 affected artifacts에는 의미가 바뀐
관련 색인 행도 포함된다. 이 연결을 위해 검토 회차를 늘리거나 같은 지시를 새 절로 반복할 필요는 없다.

### 실제 문구에 적용한 반례

| 반례 | 현재 source의 판단과 근거 |
|---|---|
| 검토 요청 전에 plan이 끝난 T01 착수를 지시함 | feedback115–120과 plan 작성 갱신 안내를 충족하지 못한다. REVIEW의 중요한 요약 불일치로 보고한다. |
| 색인이 최신이지만 plan은 낡고 제품 시험은 통과함 | feedback135–137과 verifier의 같은 review scope가 세 자료를 대조한다. code/test PASS는 대조를 대신하지 않는다. |
| 검토에서 새로운 실패나 미검증 경계가 발견됨 | feedback83–86과151–158에 따라 현재 요약·영향 artifact·근거를 다시 맞춘다. 이전 review를 무조건 재사용하지 않는다. |
| 프로젝트가 개발건 색인을 쓰지 않음 | feedback과 verifier가 미채택 색인을 요구하지 않는다고 명시한다. 새 파일을 만들어 적용할 이유가 없다. |
| 같은 commit에서 spec/plan을 개정하며 아직 SHA가 없음 | checked commit/base와 current amendments로 식별한다. plan의 기존 current-change 안내를 유지하며 자기 미래 SHA를 요구하지 않는다. |
| 구현만 끝났고 사람 수락·main 통합·배포가 남음 | feedback과 PROCESS/REVIEW가 이 사실을 구분한다. 현재 구현 인도 밖의 후속 일을 완료로 바꾸지 않는다. |
| document-only 인계 또는 단순 prose/status 작업 | 기존 handoff 요약 갱신은 유지하지만 새 implementation review를 만들지 않는다. status 질문은 실행·완료 검토 밖이다. |
| 매 commit마다 상태가 조금 달라짐 | helper/commit마다 fresh review를 반복하지 않는 기존 예외와 이번 verifier 항목을 유지한다. 바뀐 실제 범위에 맞게 확인한다. |
|0038/0039의 후속 source 확인이 통과함 | 원 제출판 복구·모델의 자발적 갱신 성공으로 소급할 수 없다. 연구 안내와 V4-11도 이 경계를 명시한다. |

### 플랫폼 전달과 보존 범위

세 verifier의 수정된 pause/handoff/completion 항목은 동일하다. 의미 있는 implementation-completion
또는 delivery claim에서 현재 plan·실제 채택 색인의 관련 항목·기존 실행 근거를 같은 검토에 넣는다.
실제 revision과 working tree·Git 상태에 대조하며, 미채택 색인·미래 자기 SHA·실행 로그 복제·새
장부·매 commit review·document-only delivery의 새 implementation review를 요구하지 않는다.
기존 앞부분의 design-only 적용 범위와 마지막 human approval/merge 구분도 유지됐다.

전체 Review criteria는 Claude와 OpenCode가 같고, Codex에는 프로젝트 `AGENTS.md`도 읽는
기존 플랫폼 차이가 있다. TOML의 문자열 종료 표기는 전달 형식이다. 이 차이를 의미 불일치로
판정하지 않는다. 이번 수정 항목의 플랫폼 동등성은 현재 본문 대조로 확인했다. patch 변경은 공통
본문 이동에 따른 hunk 위치 조정이며 별도 정책·모델 검토 회차를 추가하지 않는다. 실제 patch
적용과 임시 설치·정적 검사 결과는 다른 최종 검토의 확인 범위로 남긴다.

0038/0039 보고서와 세 버전 manifest에는 이번 base 대비 diff가 없다.0038의 현재 plan/인계
부분 판정과0039의 partial·최초 실패를 유지한다. 후속 연구 안내·팀 README·V4-11은 같은0.1.10
미배포 후보의 source 보완과 실제 행동 재시험/원 제출판 복구를 구분한다. 새 제품 실행이나
제품/전역 설치를 확인한 것으로 쓰지 않는다.

### 읽은 현재 source 지문

| 파일 | SHA-256 |
|---|---|
| tdd-optional/org-skills/skills/sdlc-feedback/SKILL.md | 9c10d4ca34cff66741512fef893029c5e6012e095ff7ed6cc5726e2ba5c3afe9 |
| tdd-optional/org-skills/agents/sdlc-verifier.md | d7c7b3023af3d20ecae60b7829cfa899ade49580f17776b30dd50834cf5c3481 |
| tdd-optional/org-skills/codex/agents/sdlc-verifier.toml | 8a014b9b4221b67cffe9f1757b1dc0d8f8467bbde63e95beba161b6da43dc2cc |
| tdd-optional/org-skills/opencode/agents/sdlc-verifier.md | f4535e4d2bb76bafdbd28136541cbf1fbcb92b9bf029714e03abbbe34ee61bc5 |
| tdd-optional/project/examples/skills/plan/SKILL.md | e155e2204f04fb885aae25dd4914f578154fe6181ec46eeafee7223ba59e3115 |
| tdd-optional/project/docs/PROCESS.md | 6761293539a07cffd4b6c06809e8780b202941402c6f5362047ef7299617727d |
| tdd-optional/project/REVIEW.md | f2c1a8fbd346cd97e24596f593deac78c7bd6ebb48e41cf1935f2371b127fdda |
| tdd-optional/org-skills/codex/patches/sdlc-feedback.patch | 9c12d3d09fc85b74bc91d3cce614dffce082a23854c3ecf452cda979706225a8 |
| tdd-optional/org-skills/opencode/patches/sdlc-feedback.patch | 2fc115b42e666792b0dc905b17ddd49bc15182da02ade35417c6cb29eb8c76ca |

지문은 위 판단에 사용한 바이트를 식별한다. 실행이나 스킬의 실제 사용 증거는 아니다.
이번 의미 검토에서 추가 source 수정은 요구하지 않는다. 완료보고 직전 maker plan·검증 기록의
현재 결과 정리와 기존 최종 검토는 T16의 다음 작업으로 남는다. 최초 방향 검토와 이번 source
검토만으로 AC12 전체 완료·사람 수락·설치 성공·모델 행동 개선을 선언하지 않는다.
