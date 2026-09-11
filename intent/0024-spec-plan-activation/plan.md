# Plan: 활성화 → 설치 확인 → 실제 개발 실험
Upstream: spec.md@dc2cbcb. Status: draft.
사용자의 잔여 작업 진행 요청에 따라 순서대로 연속 수행한다. 이미 리뷰한 후보 2d3f2dc를 출발점으로 삼는다.

## Files that change
- templates/spec.md, plan.md, .claude/skills/{design-spec,plan}/와 해당 references: 실제 양식/작성 지침과 링크.
  기존 작은 examples에는 현행 교육 세트를 가리키는 README를 추가하고 원래 사례는 보존한다.
- docs/sdlc-authoring/** (new): 다섯 자체 예시·필수 교육 입력·갱신 예·색인. 이전 연구/예시는 보존.
- org-skills/skills/{spec-policy-pass,tdd,sdlc-feedback}/, org-skills/commands/spec-policy.md,
  org-skills/agents/sdlc-verifier.md, org-skills/README.md, org-skills/.claude-plugin/plugin.json,
  .claude-plugin/marketplace.json: 실제 팀 스킬/검토·설치 안내와 판.
- CLAUDE.md, docs/ADOPTING.md, README.md: 얇은 TDD 정책·선택 예시/사용판·완료 결과 안내.
- docs/GIT-WORKFLOW.md 및 후속 사용판의 동일 파일: 최초 단계별 커밋과 구현 시작 뒤 재계획의 같은 구현 커밋을 구별하는 기존 문구 정정.
- docs/research/sdlc-documentation/spec-plan-activation/** (new), docs/experiments/datasets/v6/** (new),
  docs/experiments/0024-spec-plan-activation.md (new), docs/experiments/README.md: 실행 입력·후속 사실·설치/리뷰/실험 근거.
- docs/verification/north-star-playbook.html: 통과한 실제 관측의 기존 관련 주석만 보강.
- 별도 codex/use-template-0024: 0023@787af77 기반의 core 양식/정책/선택 예시를 갱신. 실험 clone의 seed/main/작업 refs는 별도 보존.

## Order of work
### 1. 활성 템플릿·스킬 반영
root는 양식/작성 reference/예시·maker 정책·사용판을 반영한다. 독립 에이전트가 org-skills의 기존 기준과
TDD/정책 검토 소스를 병행 수정한다. 소유 파일은 겹치지 않는다. 서로 맞물리는 경로/정본·설명은 root가 조정한다.
Astra/ultra는 별도로 실제 실험의 최소 설계를 제안한다. 기존 연구를 재작성하거나 활성 검사기를 추가하지 않는다.
완료 관측: 후보→활성/사용판 대응, 설치 경로 참조·원문/기존 계약 보존, 스킬/플러그인 형식과 독립 검토.
이 변경은 문서/스킬 활성화이므로 제품 RED를 꾸미지 않는다. 관련 기존 회귀는 make check다.

### 2. 영구 설치와 새 세션 확인
실제 CLI와 설치 목록을 먼저 확인했다(2.1.265, 팀 플러그인 0.1.4, 로컬 marketplace).
활성 소스를 고정한 후 0.1.5로 validate/update/list를 수행하고 실제 소스/캐시와 새 세션의 판을 확인한다.
기존 외부 플러그인을 제거하지 않는다. 정상 세션의 설정/스킬 목록을 확인하며 safe-mode를 템플릿 실험에 사용하지 않는다.
작성 스킬은 자체 선택 예시를 제품의 .claude/skills에 설치한다. 이력/파일 존재와 실제 로드/적용을 구별한다.

### 3. 실제 작은 제품 개발
새 사용판에서 shallow clone, 제품 baseline/공개 문제 seed를 고정하고 짧은 작업 branch를 파생한다.
F04-release-json은 기존 CLI 4행 데이터를 재사용하는 작은 두 PR/한 공개 단위 사례다. 새 dataset은 따로 보존한다.
root는 PERSONA의 HUMAN으로 질문에 실제 답하고 산출물을 읽어 intent/spec/plan을 수락한다. 이후 Claude Code Sonnet/medium이
의미 있는 첫 RED→최소 GREEN·회귀를 수행한다. 중요한 설계/반복 오판에는 모델/추론을 적절히 높인다.
첫 PR을 로컬 검토/통합하고 최신 main을 검증한다. 둘째 PR의 실제 동작 리뷰에서 JSON 출력 후속 요청을 전달하되
문서 갱신을 별도 상기하지 않는다. 실제로 이미 커밋했다면 되돌려 재연출하지 않고 열린 PR의 후속 변경으로 관측한다.
새 spec 수락 요청이 오면 실제 판을 읽고 수락한다. 관련 구현·영향 spec/plan 동시 기록, 전체 회귀·일반 OFF/시험 ON,
완성 코드의 공개/중단을 확인한다. cleanup은 모의 조건과 범위를 구분해 필요하면 같은 실행의 짧은 후속으로 확인한다.
제품 코드는 root가 대신 구현하지 않는다. 중요한 자발적 동기화 실패는 복구와 새 시험을 구분한다.
기본 60분/12 HUMAN 턴의 한 실행을 기준으로, 초과나 재실험이 필요하면 실제 사유·범위와 모델 조건을 기록한다.

실행 중 조정: 첫 JSON 변경은 spec/plan을 자발적으로 갱신했지만 plan을 별도 커밋했고 intent의 절대 출력 표현도
남겼다. 현재 제품은 HUMAN 리뷰 후 정정·통합하고 최초 실패는 보존한다. 새 Opus/high 부분 실행에서도 계획을
먼저 별도 커밋하는 관측이 반복되어, 독립 Astra 검토로 최초 단계별 커밋과 후속 변경 규칙의 적용 범위 중첩을 확인했다.
새 절·검사기·필수 스킬을 만들지 않고 Git 정책의 기존 두 문장을 명확히 한다. 원래 use0024는 고정한 채 후속
use0024-r2를 파생하고, 기존 텍스트 요약 경계의 새 clone·업무 요청으로 해당 조건만 확인한다. 설치 플러그인
소스/판은 바꾸지 않는다. 최종 판정은 각 원 실행·복구·부분 재시험을 구분하며 전체 재실행을 하지 않는다.

### 4. 검증·반영·기록
독립 verifier가 .claude/agents/verifier.md에 따라 make check와 해당 사슬·두 인접 흐름을 확인한다.
실제 제품 검증은 Claude의 개발 결과와 별도로 root/검증자가 다시 실행해 검토한다. 관련 모순을 고친 뒤 영향을 재검증한다.
원문/기존 실패·고정 평가 근거를 보존하고 관측한 주석만 갱신한다. 완료 범위를 로컬 main에 통합하고 근거 refs와 문서를 보존한다.
원격 PR·CI·조직 권한 분리·운영 배포를 실제 수행한 것으로 표현하지 않는다.

## Risks
경로를 단순 복사하면 선택 예시/설치 뒤 링크가 깨질 수 있어 배치 후 직접 확인한다. 로컬 marketplace의 설치 metadata만으로
새 소스 로드를 판정하지 않는다. 초기 실행에서 다른 스킬·maker 이력이 보이면 오염 범위를 숨기지 않는다.
코드 성공이 문서 동기화/TDD를 증명하지 않으며, HUMAN의 정답 유도·사후 RED 재현은 자발적 성공으로 세지 않는다.

## Proof
| 대상 | 실제 증거 |
|---|---|
| AC1 | 활성/사용판 파일 대응·스킬/플러그인 검증, 독립 리뷰, 기존 make check·보존 대조 |
| AC2 | CLI 버전·설치 전후 목록/경로/내용, 새 세션 공개 Skill/Read/Agent trace와 적용 결과 |
| AC3 | use/seed/단계/main SHA, 파일 tree·shallow/비공개 미노출 확인, 보존 refs |
| AC4/5 | 실제 대화/수락·첫 RED와 후속 Write/시험·커밋 diff·회귀/공개 상태·관련 문서 갱신 |
| AC6 | 독립 verifier 원문, 전체 흐름 평가/고정 근거 재사용/미관측 표, 주석 diff·원문/이력 보존 |

실행·리뷰·개선 발견에 따라 실제 파일/순서/증명과 이 plan을 관련 변경 커밋에서 갱신한다.

## Execution outcome

활성화 0f0f3ce, 후속 정책 정정 e0657c9와 사용판 d4d2153을 기준으로 설치·제품 개발까지 수행했다.
플러그인 0.1.5는 user 범위에 영구 설치했고 정상 새 세션의 실제 로드/본문 적용을 확인했다.
전체 원 실행에서 두 local PR 범위를 통합하고 14시험·50관측 및 별도 공개/중단 12관측을 수행했다.
plan 커밋 분리·intent 잔류는 최초 실패로 보존했다. 부분 r01도 같은 커밋 기준을 실패했다.
정책 적용 범위만 명확히 한 r02는 dc05fc0에 plan과 구현을 함께 커밋했다. native 리뷰 보완 뒤
HUMAN 최종 참조 정정·수락을 거쳐 merge c5ea850에서 17시험·50관측을 통과했다.
이는 사람 리뷰를 포함한 관측 범위의 통과이며 자동 무결성·UI/운영 배포·cleanup까지 증명하지 않는다.

최초 60분/12턴 기준은 부분 재시험이 필요해 도달 전 90분/16턴으로 연장했다. 실제 개발 대화는
14턴·약 82분에 종료했다. 이후 기록 아카이브·문서 마감·제작 main 통합은 별도의 마감 작업이다.
관련 12개 북극성 주석만 추가하고 원문·기존 판정·179 ID를 보존한다.
최종 소스 검증은 독립 verifier의 make check(96시험, hook28, eval fixture8, managed settings),
격리 hook bad input과 실제 제품 실행/역사적 trace 대조다. 고정된 이웃 근거는 이전 판 diff로 재사용했다.

[0024 결과·보존 색인](../../docs/experiments/0024-spec-plan-activation.md)과
[독립 마감 검토](../../docs/research/sdlc-documentation/spec-plan-activation/closing-review.md)에
실행별 수락 SHA·기능/과정 판정·한계를 둔다. 전체 공개 raw는 세 개의 고정 실험 기록 branch에 보존하고
제작 main에는 색인과 판단만 둔다. 이력 재작성·제품 코드의 제작 main 병합·원격 작업은 하지 않는다.
