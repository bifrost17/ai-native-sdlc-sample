# 0040 — 완료 인계 보완의 OpenCode 재실험

Status: running — 설치·baseline 확인 완료, 실제 대화와 완료 인계 관측 예정

사용자 요청 원문: “재실험해봐”.0039의 현재 plan 요약 누락 뒤 적용한 source
`e38477cdf4a6360c473bb76486d1e5e9baa1436e`/0.1.10 후보를 같은 작은 사례로 재시험한다.
root는 HUMAN(Codex simulated), OpenCode Muse Spark1.3/xhigh는 개발 에이전트다.
북극성 V4-09/V4-11의 plan·diff/관련 개정, V7-09의 보고 전용 검토자와 V8-02의 최종 새 문맥
검토를 기준으로 한다. 현재 요약·채택 색인·실행 근거의 같은 검토는 팀이 구체화한 절차다.
0038/0039 원 제출판과 partial, 전체 AC04 유예는 유지한다.

## 시작판과 실험 조건

제작 경로는 `.local/worktrees/intent-design-alignment`, branch는 `codex/intent-design-alignment`다.
정확한 source를 archive한 뒤 새 제품 저장소에 project·native11·작성3·자료2·검토자와 전체 동반
자료를 설치했다. 기존 OpenCode patch의 dry-run/적용을 확인했다. 전역 설정·원제품은 변경하지 않았다.

| 판 | branch·SHA | 역할 |
|---|---|---|
| 설치판 | `codex/0040-template` · `017eeb3f108844fe14fa57904d450dd8f1b6a64e` | source e38477c의 제품·팀 자산 |
| 제품 baseline | `main` · `862ba911f50fce59fa07b6bfbb94180f0d8ded64` | 0039 main의 업무 입력·문서·코드·시험과 설정 바이트 동일 |
| 작업판 | `codex/0040-completion-handoff` · 시작 시 위 baseline | 별도 실제 개발 branch |

0039의 `d3c23f3`에서 AGENTS·REQUEST·intent/spec/plan·색인·tracker·시험·fixture9파일과
opencode.json의 동일성을 직접 확인했다. 설치 정책/스킬은 후보 treatment이며 업무 baseline과
구분해 해시를 기록했다. 시작 unittest3개 통과. 제작 main을 제품 main으로 쓰지 않는다.

첫 두 대화는 owner 필터 설계와 이유 없는 정렬 제안이며 구현을 허용하지 않는다. 마지막은 실제
질문을 읽고 명확한 제약 변경의 이유·범위와 로컬 구현 인도를 결정한다. 처음 작성 스킬은0039처럼
명시 지정하고 feedback·최종 요약 갱신을 새로 지시하지 않는다. root는 실제 제출을 읽고 답하며
후속 결정과 oracle을 제품에 전달하지 않는다. [재사용 입력](datasets/v10/intent-alignment/public.md)과
[HUMAN 조건](datasets/v10/intent-alignment/human.md)의 기존 번호는 원본으로 보존한다.

기본 예산은 첫 dispatch부터15분, parent3회·native verifier 최대1회다. native verifier는 parent의
task 호출을 관측하며 root가 대신 실행하지 않는다. 중요한 누락/미완료는 예산 내 그대로 기록한다.
사소한 표현·도식 취향을 이유로 반복하지 않으며 이번 한 회를 원 문구의 개별 인과 효과로 해석하지 않는다.

[사전 설계 검토 전문](../research/openwebagent-template-history/intent-design-alignment/0040-retest-design-review.md)은
진행을 막을 중요한 모순이 없음을 보고했다. 실제 검토 요청 시점의 plan·색인과 근거, child의 대조·반환,
parent의 대기와 현재 인계를 관측한다. private runner는 plan·색인의 바이트 변화/관측 시각을 보존하며
모델이나 제품의 동작을 수정하지 않는다. 공개 도구 event의 편집·task 시각과 함께 대조한다.

## 판정과 원본 보존

의도 유지·충돌 확인·명시 변경과 문서 선개정·실제 구현/회귀·같은 commit·완료 검토와 현재 인계를
구분해 평가한다. 완료 요약은 실제 완료한 일/미검증/남은 의존성/다음 단계가 근거와 맞는지 판단한다.
구현·시험 성공을 사람 수락·main 통합·배포로 바꾸면 안 된다. parent/child의 실제 설치 본문 읽기와
metadata를 확인하고, 미관측은 그대로 남긴다. 본문 접근이 확인돼도 개별 문구의 효과를 입증하지 않는다.

제품은 `.local/experiments/workspaces/0040-completion-handoff-muse/product/`, 원본은
`.local/experiments/private/0040-completion-handoff-muse/`다. 설치 source·baseline 지문·실제 prompt·
전체 공개 응답/도구·실행 시간/rc·단계별 snapshot·검토 전 관측·independent CLI 기대/결과·
session export·Git refs/bundle을 보존한다. 인증 값·숨은 추론은 공개 기록/manifest에서 제외한다.
보고서는 실행 원문을 대신하지 않는다. 원격 PR·통합·배포·새 세션 인계·큰 개발건·다른 도구 행동은
이번 실행의 관측 범위 밖이다.
