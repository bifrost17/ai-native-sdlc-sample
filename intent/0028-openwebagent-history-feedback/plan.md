# Plan — openWebAgent 이력에서 개선과 재실험으로

Status: draft
Upstream: [spec](spec.md), [intent](intent.md), 사용자의 실행 요청.

현재 상태: T01의 340 PR·114 브랜치·30 번호 개발건과 4 무번호 개발건 수집 완료. T02 모든 건 보고서와 대형 후속 조사 작성 완료, 실행 원문·세부 감사의 한계는 coverage에 남긴다.
후속 사용자 지시에 따라 T04의 0037 실제 개발 비교를 중단했다. 실패·부분 수행을 보존하고 AC04의 전체 전후 비교는 유예한다.
현재 인계: T06–T12의 제작 보완·적대적 리뷰·중요 지적 해결을 완료했다. 새 사용자 요청으로 T13/0038을
별도 실행해 AC09의 관측/보존을 완료했다. 계약 갱신·같은 커밋·동작은 통과했으나 현재 plan 요약 누락으로
인계 상태 갱신은 부분이다. 이는 T04 재개나
전체 개발 비교 완료가 아니다. 전역 설치·원제품 변경·원격 인도는 범위 밖이다.
최신 인계: T14의 의도 없는 추가 요구/설계 개정을 줄이는 정본 설계·독립 제안·현재 지침 조사·적대적 리뷰를 완료했다. 활성 구현·새 실험은 진행하지 않았다.
초기 main은 a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e.
기존 제작 HEAD ad98ade와 미커밋 patch는 start/에 보존한다. 새 보고서를 제품 완료로 주장하지 않는다.

## Files that change
아래는 실제 저장소 상대 경로다. 원 후보부터의 source 범위는 `ad98adec..df3ae99`, 이번 순차 정리의
source 범위는 `4a84596..df3ae99`다. 후자의 10개 파일은 T06–T09 행에서 찾는다. T10은 기존 후보를
검토해 유지했으며 T11은 패키지 source를 새로 바꾸지 않고 현재판을 확인한다. 이 목록은 첫 계획에
이미 있었던 것으로 소급하지 않는다. U6가 발견한 경로 인계 누락을 후속 개정으로 정리한 것이다.

| 실제 경로 | 수정/보존할 의미와 방법 | 작업·설계 |
|---|---|---|
| tdd-optional/project/templates/spec.md | AC의 독립 기대·검증 경계·미정 입력을 plan으로 연결 | T03c/T06, SP06/07 |
| tdd-optional/project/examples/skills/design-spec/references/design-depth.md | 기존 설계 블록에서 검증 접근·실제 UI 선택과 편입 조건 설명 | T03c/T06/T07, SP06/07 |
| tdd-optional/project/examples/skills/plan/examples/disposable-ui-exploration.md | 정적 예시와 실제 컴포넌트 선택·제품 편입을 구별 | T03c/T07, SP06/07 |
| tdd-optional/project/examples/skills/plan/references/execution-depth.md | 첫 위험 경계의 실제 연결·늦는 연결과 독립 병렬 작업 설명 | T03c/T08, SP06/07 |
| tdd-optional/project/changes/README.md | 개발건 색인·명명·후속 계약과 역사 구분. 기존 project/intent/README.md를 신규 배포에서 대체하며 기존 제품은 이사하지 않음 | T03b/T09, SP05/07 |
| tdd-optional/project/docs/PROCESS.md | 실제 채택 색인·현재 plan 인계·작업 크기와 검증 경계 연결 | T03b/T09, SP05/07 |
| tdd-optional/project/docs/GIT-WORKFLOW.md | 실제 색인 갱신 fallback, 계약/계획 개정·PR 최종판·통합 연결 | T03b/T09/T10, SP05/07 |
| tdd-optional/project/examples/skills/capture-intent/SKILL.md | 실제 채택 색인/경로로 기존·신규 건 찾기 | T03b/T09, SP05/07 |
| tdd-optional/project/examples/skills/design-spec/SKILL.md | 현재 계약/역사 대조·실제 색인 fallback·관련 설계 정본 찾기 | T03b/T09, SP05/07 |
| tdd-optional/project/examples/skills/plan/SKILL.md | 현재 설계에서 실행·검증을 연결하고 기존 경로 유지 | T03b/T09, SP05/07 |
| tdd-optional/project/docs/CHANGE-DELIVERY.md | 목적/범위/실제 검증판/인계의 PR 안내와 의미 있는 커밋 본문 | T03b/T10, SP05/07 |
| tdd-optional/project/.github/pull_request_template.md | 네 부분의 기본 PR 양식, 작은 정리 예외 | T03b/T10, SP05/07 |
| tdd-optional/org-skills/skills/sdlc-feedback/SKILL.md | 최종 diff·시험판·영향 문서·기존 색인 갱신을 작업 사건에 연결 | T03b/T03c/T10, SP05/06/07 |
| tdd-optional/project/CLAUDE.md | 채택 제품의 활성 경로와 기존 얇은 규칙 연결 | T03b, SP05 |
| tdd-optional/project/PROJECT-POLICY.md | 실제 역할/기록 위치를 제공하는 슬롯과 새 색인 안내 | T03b, SP05 |
| tdd-optional/project/README.md | 제품 진입점·색인·전달 기준 연결 | T03b, SP05 |
| tdd-optional/project/REVIEW.md | 계획 구체성·현재 계약·검증 의미 대조 | T03b/T03c, SP05/06 |
| tdd-optional/project/templates/plan.md | 원 WIP5의 실행 구체성 보완을 보존하고 적용 안내 연결 | T03c, SP06 |
| .claude-plugin/marketplace.json | 단일 선택판의 source·0.1.9 일치 | T03c/T11, SP07 |
| tdd-optional/.claude-plugin/marketplace.json | 배포판 catalog의 source·0.1.9 일치 | T03c/T11, SP07 |
| tdd-optional/org-skills/.claude-plugin/plugin.json | 실제 팀 플러그인 0.1.9 | T03c/T11, SP07 |
| tdd-optional/README.md | 같은 판의 채택/설치 시작점 | T03c/T11, SP07 |
| tdd-optional/org-skills/README.md | 공통 스킬·배포판/제품 정책 경계 | T03c/T11, SP07 |
| tdd-optional/org-skills/claude/README.md | 공통 source 전체를 Claude에 전달·갱신·검증 | T03c/T11, SP07 |
| tdd-optional/org-skills/codex/README.md | Codex 네 patch와 verifier/동반 자료·설치/행동 한계 | T03c/T11, SP07 |
| tdd-optional/org-skills/opencode/README.md | T03c의 기존 전달 안내를 유지하고 T13의 선택 hook·0038 관측 범위와 설치/행동 근거 차이를 연결 | T03c/T13, SP07/09, FR10/AC09 |
| tdd-optional/org-skills/commands/spec-policy.md | 기존 정책 검토 예시의 같은 판 유지 | T03c, SP07 |
| README.md, docs/decisions/single-template.md | 74e1148의 현재 0.1.9 표기 정정. README의 별도 미커밋 WIP는 그대로 보존 | T05, SP07 |
| docs/research/openwebagent-template-history/ | T01–03의 방법·coverage/cases·조사/검토 전문과 원본색인. 하위 실제 보고서 목록은 coverage.md·originals-index.json, 이번 완료 자료는 completion/README.md에서 연결 | T01–03/T05–11, SP01/02/04/05/06/07 |
| intent/0028-openwebagent-history-feedback/ | 실제 변경된 의도·설계·계획·현재 인계. 자기 문서 경로는 산출 lineage | T01–13, 전체 |
| docs/experiments/0037-openwebagent-history-feedback.md | 이미 중단된 부분 실행·실패·후속 유예 기록 보존 | T04/T05, SP03 |
| docs/verification/north-star-playbook.html | T05/T11의 source만으로는 승격하지 않음. T13의 실제 문서 갱신·같은 커밋·새 인계 범위만 V4-11에 추가하며 기존 부분·실패를 유지 | T05/T11/T13, SP07/09, FR10/AC09 |
| tdd-optional/org-skills/examples/document-sync-hook/ | opt-in pre-commit·표준 라이브러리 검사와 설치/실행/한계 예시 | T12, SP08 |
| tdd-optional/org-skills/skills/sdlc-feedback/SKILL.md, tdd-optional/org-skills/claude/README.md, tdd-optional/org-skills/codex/README.md, tdd-optional/org-skills/README.md | 같은 예시·신호 계약을 선택한 커밋 절차에 연결. 원 스킬의 의미·최종 검토 경계 유지 | T12, SP08 |
| tdd-optional/project/docs/CHANGE-DELIVERY.md, tdd-optional/project/docs/GIT-WORKFLOW.md | 메시지 검사와 선택 동기화 hook의 경계·확인 가능한 조건 연결 | T12, SP08 |
| tests/test_document_sync_hook.py | 격리 Git repo에서 신호/포함/실제 index/부분stage·무관WIP·기존설치 보존 동작 시험 | T12, SP08 |
| docs/BOUNDARY.md | 기존 미구현 plan-sync 설명과 사용자 후속 opt-in 예시·의미 판단 경계 정합성 | T12, SP08 |
| docs/experiments/0038-document-sync-muse.md, docs/experiments/datasets/v9/broker-replay/ | 0018의 ACK/최종 구분에서 파생한 합성 원본 fixture·입력·HUMAN 조건·실제 실행 전문의 경로/결과/한계 | T13, SP09, FR10/AC09 |
| docs/research/openwebagent-template-history/originals.md, docs/research/openwebagent-template-history/originals-index.json, docs/research/openwebagent-template-history/README.md, docs/research/openwebagent-template-history/recommendations.md | U1–U7 source 완료와 새 0038 실험 범위·전문/원문 색인·보존 감사 연결 | T13, SP03/07/08, FR10/AC09 |
| docs/research/openwebagent-template-history/intent-design-alignment/ | 현행 지침 전문 조사·독립 제안·root 정본 설계·적대적 리뷰를 역할별 파일로 보존. 선언된 참조와 원문/해시 연결 | T14, SP10, FR11/AC10 |
| intent/0028-openwebagent-history-feedback/intent.md, spec.md, plan.md, docs/research/openwebagent-template-history/README.md, originals.md, originals-index.json | 새 설계 요청의 이유·범위·근거·현재 인계와 전문 색인 갱신. 활성 스킬/정책과 제품은 그대로 유지 | T14, SP10, FR11/AC10 |

`.local/research/openwebagent-template-history/20261003/`는 원본/실행/해시의 private 산출 위치다.
Codex의 `org-skills/codex/patches/`와 `agents/sdlc-verifier.toml`, Claude 공통 `org-skills/agents/`는
T11의 **읽기·임시 복사 검증 입력**이며 이번 변경 파일이 아니다. T12는 위 새 Git fixture 시험을
추가하며 기존 `tests/`·`evals/`·Makefile의 실행 방식은 보존한다.
원제품·전역 설치·별도 미커밋 WIP는 범위 밖이다.

## Order of work
- T01 / SP01 (Luna medium + root): 원격 API 전수 페이지와 bare Git를 수집한다. main/ref SHA와 원본 hash를 고정한다. intent 이력, PR의 head/title/body/diff에서 개발건을 정규화한다. 당시 지침·현재 HEAD·후보를 서로 구분한다. Done: AC01의 조사 모집단과 담당 목록.
- T02 / SP02 (Sol medium, 큰 계약 Astra high): 0018/0021/0028을 먼저 읽어 사건 기준을 맞춘다. 모든 개발건을 4~5개 묶음으로 병렬 분석한다. 승인·최초 문서·관련 구현·리뷰·후속 갱신의 실제 Git 판을 대조한다. 중요한 원인이 불명확할 때만 필요한 대화 구간을 수집한다. Done: AC02의 전체 건별 보고서와 coverage.
- T03 / SP02 (root + Astra high): 공통 원인을 중복 제거하고 반증·성공 대조·현행 지침을 읽는다. 후보가 두 독립 사건 또는 중대한 현재 재현에 근거하는지 확인한다. 개선할 실제 지침과 바뀔 판단을 이 spec/plan에 추가한다. Done: AC03의 최대 2~3개 작은 변경 또는 근거 있는 보류.
- T03a / SP04 (Astra high, T02와 병렬): 사용자 추가 네 가설을 원전 연구와 대조한다. 실제 UI/공유 시퀀스의 조기 검증과 설계 검증의 구체화를 현행 지침에 대조하고 역사 증거와 결합한다. 일반 방법의 효과를 해당 실사용 실패의 원인 증명으로 대신하지 않는다.
- T03b / SP05 (root 설계, Sol medium 구현, Astra high 검토): 사용자 추가 PR·커밋·총괄/정본 요구를 배포판의 기존 정책과 대조한다. changes 경로와 총괄 README, .github PR 양식과 commit 작성 문서를 제공한다. 기존 intent 경로·maker 이력은 자동 이동하지 않으며 source 작성 스킬/도구 전달의 참조를 맞춘다.
- T03c / SP06 (root 구현, Astra high 설계 검토): templates/spec.md의 AC 안내에 검증 경계·입력/환경·독립 기대·관측/한계를 연결한다. design-spec/references/design-depth.md의 기존 설계 블록에 실제 UI/앱 셸과 검증 예시를, plan/references/execution-depth.md에 첫 실제 수직 경로와 늦는 경우의 대안을 보강한다. disposable-ui-exploration 예시는 정적 배치 탐색과 실제 컴포넌트 결합 탐색의 선택을 설명한다. 공통 feedback은 최종 PR본문·현재판·개발건색인/과거spec대조를 짧게 연결한다. source package를 0.1.9로 맞추고 Codex patch/Claude strict검증, 작은 사례 부담 검토를 거친다. Done: AC03/06의 실제 diff·검토 기록 및 T04의 현재판/수정판 경계 비교.
- T04 / SP03 (root HUMAN + 실제 CLI): 원래 도구의 두 사례 전후 네 실행, 다른 도구의 별도 한 실행을 수행한다. 각 제품은 독립 repo와 고정 template ref/파생 branch를 갖는다. 설치 자산·실제 model/effort·질문/답변·실행·commit을 보존한다. 새 문맥 인계와 후속 변경을 관측한다. Done: AC04; 부족하면 최대 두 차례 수정과 전체 9실행 안에서 재검증.
  현재 유예: Claude 조직 차단·OpenCode 공급자 인증 오류와 B의 부분 수행/사용자 중단을 보존한다. 완성 전후 쌍이 없으며 효과를 판정하지 않는다. 후속 지시가 있으면 그때 기준·권한·예산을 다시 고정한다.
- T05 / 전체 (root + fresh verifier): 현재 diff와 coverage·실험·회귀 결과를 독립 검토한다. make check와 필요한 패키지/adapter 확인을 수행한다. 확인 범위만 주석·최종 보고·인계에 반영하고 관련 파일만 커밋한다. Done: AC05 및 실제 결과/잔여 한계.
- T06 / SP06–07: spec AC 안내와 design-depth의 검증 접근을 구체화한다. 중요한 AC의 독립 기대·경계·환경·실패/관측·미정이 plan에 전달되는지 Astra/high 적대적 리뷰를 받는다. 작은 F01과 선택형 TDD의 부담을 대조한다. Done: AC03/07, U1 기록과 scoped commit.
- T07 / SP06–07 (T06 후): 실제 기존 컴포넌트·앱 셸·시각 기준·핵심 상태와 초기 UI 코드의 편입 조건을 design-depth와 기존 UI 탐색 예시에서 정리한다. Astra/high가 정적 시안의 유효성, 사람 피드백, 제품 완료 오인을 적대적으로 검토한다. Done: U2 기록과 중요한 지적 해결.
- T08 / SP06–07 (T07 후): plan execution-depth에서 첫 위험 경계를 통과하는 작은 경로·후속 확장/병렬·늦는 연결의 가정을 정리한다. Astra/high가 공유 계약/PR 독립성·배포 가능성과 초기 연결의 실질성을 검토한다. Done: U3 기록과 중요한 지적 해결.
- T09 / SP05/07 (T08 후): changes 색인·현재 계약과 과거 spec의 구분·기존 intent 호환·작성 스킬 발견 경로를 대조한다. Astra/high가 정본 중복과 과거 수락 오인·업데이트 누락을 검토한다. Done: U4 기록과 중요한 지적 해결.
- T10 / SP05/07 (T09 후): PR/커밋 양식과 기존 feedback에서 최종 diff·문서 개정·현재 인계/색인을 연결한다. Sol/high가 작은 수정의 부담·권한/수락 혼동·대상판·검증 한계를 적대적으로 검토한다. Done: U5 기록과 중요한 지적 해결.
- T11 / SP07 (T10 후): Claude/Codex 패키지와 patch 참조·버전·링크를 확인하고 기존 make check/strict 검증을 실행한다. 새 verifier가 실제 전체 diff와 판별 근거를 검토한다. Done: AC05/07의 source 완료. AC04 제품 실험은 미입증으로 유지한다.
- T12 / SP08 (T11 완료 후): [U7 설계](../../docs/research/openwebagent-template-history/completion/U7-hook-design.md)를 적용한다. root는 기존 feedback·정책/Claude·Codex 전달을, Sol/medium worker는 선택 hook/격리 Git 시험을 소유한다. 단계 승인이나 별도 모델 CLI는 추가하지 않는다. Astra/high 적대적 리뷰에서 대상 지문·문서 선택·부분stage·설치 범위·자기선언/우회 한계를 확인하고 중요한 지적만 수정한다. make check와 필요한 adapter 적용·설치판 참조를 확인한다. Done: AC08의 실제 source 시험/리뷰·대상판/한계 보존. 모델 개발 실험·전역 설치는 진행하지 않는다.
  검증 방식은 실제 Git 저장소의 시나리오 시험이다. 메타데이터 모킹으로 실제 commit 대상/부분 stage를
  입증할 수 없어 첫 commit·오류·alternate index·설치 보존을 확인한 뒤 전체 make check로 회귀를 확인한다.
  리뷰의 P2 복구는 재현 실패 후 같은 기대의 통과를 확인한다. 지문은 SP08의 HEAD+index 엔트리+변경 경로 방식으로
  개정한다. 초기 시험/지적/복구를 소급해 첫 구현부터 TDD였다고 보고하지 않는다.

- T13 / SP09 (T12 완료 후): 사용자 새 OpenCode Muse Spark/xhigh 요청을 [0038](../../docs/experiments/0038-document-sync-muse.md) 한 실행으로 수행한다. source a23a1ce의 선택판·전체 동반 스킬·hook을 별도 repo에 먼저 적용한다. HUMAN(root)는 실제 intent/spec/plan 초안을 검토해 구현을 요청하고 첫 구현 뒤 역할별 final 결과 가시성 변경을 전달한다. 초기 변경에는 갱신을 상기하지 않는다. 새 Muse 세션의 문서 인계와 실제 HTTP/SQLite·회귀·커밋 내용을 root가 확인한다. 실제 Git/HTTP 시나리오 검증을 사용하며 검증 방식은 에이전트의 선택을 관측한다. 총30분·parent6/child2, 사전1호출5분. Done: AC09의 실제 결과/미완료/한계 보존; AC04의 전체 전후 비교는 유예. 추가 source 변경은 일반 문제일 때만 최소로 검토한다.

- T14 / SP10 (T13 기록 후): root가 북극성 intent/design 절을 정독한다. Sol/medium explorer가 현행 작성·feedback/전달본의 공백을 좁게 조사하고 Astra/high가 독립 설계 전문을 작성한다. root는 현재 intent에 맞는 중요한 변경 진입·근거/충돌·추천 전제 확인을 정본으로 통합한다. 새 Astra/high 검토자는 정본·원문의 의도와 현재 source를 대조해 적대적 리뷰를 전문에 남긴다. 중요한 지적만 수정·재확인한다. Done: AC10의 설계/수정 이유·실제 수정 경로·후속 검증안·리뷰·원문/해시 보존. 새 실행·활성 source/전역 설치·버전 변경은 하지 않는다.

## Risks

PR title·최종 문서·version 문자열만으로 실제 사건과 설치를 판단하지 않는다.
사람의 복구는 초기 자발적 수행 성공과 구별한다. 원격 body는 수집 시점의 mutable 자료다.
큰 개발건의 반복 수정이 전체 실패율을 부풀리지 않도록 같은 사건을 dedupe한다.
기록 결손으로 템플릿 결함을 추정하거나, 단일 프로젝트의 검사 정책을 일반 템플릿에 편입하지 않는다.

## Proof
원본/API/Git manifest, 전체 개발건 coverage와 보고서, 원문·발췌 대조, 후보 검토,
실제 CLI 설치·전후 실행·독립 동작 확인·회귀·새 문맥 리뷰, maker make check와 필요한 배포 검사.
전문은 .local/의 실행 자료에 보존하고 연구 문서에서 경로·hash·SHA·결론을 연결한다.

현재 인계(후속 범위): 연구 폴더에 개발건별 분석·원전 조사·설계/전달/source/결론 리뷰 전문을 보존한다.
`originals.md`와 `collection-originals.md`에서 로컬 원문·공개 보고 응답·바이트 스냅샷·manifest를 연결한다.
과거 미검토·실패와 후속 정정은 같은 원문을 덮어쓰지 않고 함께 보존한다. Git partial clone과 초기 pack
목록의 변화는 원문 보존 감사에서 드러내며 추가 실험 없이 링크·스냅샷 해시·scoped Git 인도를 확인한다.
위 Proof의 실제 개발 비교 항목은 유예돼 있으며 이번 조사 인도의 완료 조건으로 세지 않는다.

단위별 완료 기록: [completion](../../docs/research/openwebagent-template-history/completion/README.md).
현재 제작 인계: T06–T10의 source 검토를 완료했다. U4의 색인 충돌 P2는 수정·재검토했고 다른 단위에
중요 미해결 지적은 없다. 단위 기록은 `bcb501f`, `b814ec2`, `e7ed3fa`, `c3c5a3a`, `df3ae99`다.
T11의 임시 Claude/Codex 복사·strict·patch·공통 기준/자료 확인은 현재 source `df3ae99`에서 통과했다.
T11은 make check와 새 verifier의 전체 정합성 검토·지적 복구/재검토 후 root가 source 완료로 판정했다.
실제 경로 목록이 부족했던 maker plan은 후속 복구이며 처음부터 충분했다고 소급하지 않는다.
근거와 최초 지적은 completion/U6-review.md·U6-validation.md에 보존했다. 제품 source는 df3ae99와 동일하다.
AC04의 실제 제품 효과·자연 스킬 선택·전후 비교는 유예 상태다. 미배포 0.1.9, 기존 설치·main·원제품은 갱신하지 않았다.
root가 source를 소유하며 참조/검사 경로 조사는 Sol/medium에게 병렬 위임한다. 리뷰자는 source를 고치지 않는다.
각 리뷰에는 다른 단위가 이미 완료됐다는 주장보다 실제 해당 파일과 필요한 정본을 제공한다. 중요 지적만
수정하고 changed scope를 재검토한다. 보완 source는 미배포 0.1.9 후보를 유지하며 버전을 단위마다 올리지 않는다.

후속 T12/U7: 선택 Git 예시·기존 feedback 연결의 source를 완료했다. fresh Astra/high의 P2 두 건과
intent-to-add 반례를 복구·재검토했다. 실제 Git 시험13건, make check116건(1skip)과 기존 shell 검사,
Claude/Codex 전달·선택 설치 확인이 통과했다. 앞선 T06–T11과 구별해 AC08만 완료로 판정한다.
근거·최초 결함·복구는 completion/U7-review.md·U7-validation.md에 남긴다. T12 자체는 모델 행동을 입증하지 않는다.

후속 T13/0038: source `a23a1ce`/0.1.9를 먼저 설치한 별도 제품에서 실제 OpenCode1.18.30의
Muse Spark1.3/xhigh를 확인했다. HUMAN의 초안 피드백을 받은 첫 인도 뒤 문서 갱신을 상기하지 않은
가시성 변경에서 spec→plan→RED→코드 GREEN을 관측했고 `d302942`에 코드·시험·spec/plan을 함께
담았다. 새 세션의 현재 문서 인계, 새 clone `78ab6d5`의9시험·독립 HTTP/SQLite·별도 프로세스 재시작
확인이 통과했다. AC09의 한 사례 관측/보존은 완료했지만 최종 독립 리뷰에서 제품 plan의 낡은
다음 작업/원격 절차를 발견해 현재 인계 상태 갱신은 부분으로 정정했다. root의 최초 통과 보고와
제품 원 제출판을 보존하며 새 실행이나 개별 실수에 대응한 정책을 추가하지 않는다. 초기 HUMAN 수정·자연 hook 실패 복구
미관측·알림 외 상태조회 결과 가시성의 미결·전체 AC04 유예는 유지한다. 제품 main은 baseline `ab3d230`다.
전체 응답·실행 결과·refs/bundle·설치 해시는 0038의 원본 경로에 보존하며 별도 모델 실행을 추가하지 않는다.

후속 T14/SP10: [정본 설계](../../docs/research/openwebagent-template-history/intent-design-alignment/README.md)와
독립 제안·현재 안내 조사·적대적 리뷰를 전문으로 보존했다. 변경 입력의 이유/현재 의도/전제/충돌을
기존 feedback·작성 진입에서 대조하고 중요한 근거는 실제 spec에 남기는 안을 선택했다. 기본 의미 검사
hook·전수 의도 ID·모든 변경의 intent 편집·반복 질문/모델 검토를 추가하지 않는다. 새 Astra/high의14반례
검토에 중요한 지적은 없고 root는 AC10의 설계 범위를 완료로 판단한다. 사용자 요청 원문·세션 공개 응답/
도구 값·판/해시도 보존했다. 후속 구현 위치와 미실행 효과 검증은 정본에 남긴다. 현재0.1.9 source·설치판·버전,
원제품·전역 설치는 그대로다. 다음 단계는 후속 범위에서 활성 자산에 짧게 반영하는 작업이며 이번에는 실행하지 않는다.
