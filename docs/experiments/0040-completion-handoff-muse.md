# 0040 — 완료 인계 보완의 OpenCode 재실험

Status: partial — 검토 전 요약 갱신·실제 대조·제품 동작 통과, 최종 인계의 검토 상태 구분에 한계

사용자 요청 원문: “재실험해봐”.0039의 현재 plan 요약 누락 뒤 적용한 source
`e38477cdf4a6360c473bb76486d1e5e9baa1436e`/0.1.10 미배포 후보를 같은 작은 사례로 재시험했다.
root는 HUMAN(Codex simulated), OpenCode Muse Spark1.3/xhigh는 개발 에이전트다.
북극성 V4-09/V4-11의 plan·diff/관련 개정, V7-09의 보고 전용 검토자와 V8-02의 최종 새 문맥
검토를 기준으로 한다. 현재 요약·채택 색인·실행 근거의 같은 검토는 팀이 구체화한 절차다.
0038/0039 원 제출판과 partial, 전체 AC04 유예는 유지한다.

## 시작판과 실험 조건

제작 경로는 `.local/worktrees/intent-design-alignment`, branch는 `codex/intent-design-alignment`다.
정확한 source를 archive한 뒤 새 제품 저장소에 project·native11·작성3·자료2·검토자와 전체 동반
자료를 설치했다. 기존 OpenCode patch의 dry-run/적용을 확인했다. 전역 설정·원제품은 변경하지 않았다.

아래 첫 시도는 시작 조건 오류로 판정에서 제외했다. 유효 실행은 뒤의 r2다.

| 첫 시도 판 | branch·SHA | 역할 |
|---|---|---|
| 설치판 | `codex/0040-template` · `017eeb3f108844fe14fa57904d450dd8f1b6a64e` | source e38477c의 제품·팀 자산 |
| 제품 baseline | `main` · `862ba911f50fce59fa07b6bfbb94180f0d8ded64` | 업무 입력·문서·코드·시험9파일+설정은 동일, customized CLAUDE/PROJECT-POLICY 누락 |
| 작업판 | `codex/0040-completion-handoff` · 시작 시 위 baseline | 별도 실제 개발 branch |

0039의 `d3c23f3`에서 AGENTS·REQUEST·intent/spec/plan·색인·tracker·시험·fixture9파일과
opencode.json의 동일성을 직접 확인했다. 설치 정책/스킬은 후보 treatment이며 업무 baseline과
구분해 해시를 기록했다. 시작 unittest3개 통과. 제작 main을 제품 main으로 쓰지 않는다.

첫 두 대화는 owner 필터 설계와 이유 없는 정렬 제안이며 구현을 허용하지 않는다. 마지막은 실제
질문을 읽고 명확한 제약 변경의 이유·범위와 로컬 구현 인도를 결정한다. 처음 작성 스킬은0039처럼
명시 지정하고 feedback·최종 요약 갱신을 새로 지시하지 않는다. root는 실제 제출을 읽고 답하며
후속 결정과 oracle을 제품에 전달하지 않는다. [재사용 입력](datasets/v10/intent-alignment/public.md)과
[HUMAN 조건](datasets/v10/intent-alignment/human.md)의 기존 번호는 원본으로 보존한다.

최초 예산은 첫 dispatch부터15분, parent3회·native verifier 최대1회였다. 아래 준비 오류로 최초2회를
보존하고 r2를 재시작해 전체 최대6회로 바꿨다. r2의 유효 실행은15분을 유지한다. 마지막 구현 dispatch 전,
root의 준비 오류·재시작으로 전체 시간 한도만20분으로 조정했다. 최초15분 계획의 변경과 두 실패 준비 턴을
함께 공개하며 추가 개발/검토 턴은 늘리지 않는다. native verifier는 parent의
task 호출을 관측하며 root가 대신 실행하지 않는다. 중요한 누락/미완료는 예산 내 그대로 기록한다.
사소한 표현·도식 취향을 이유로 반복하지 않으며 이번 한 회를 원 문구의 개별 인과 효과로 해석하지 않는다.

[사전 설계 검토 전문](../research/openwebagent-template-history/intent-design-alignment/0040-retest-design-review.md)은
진행을 막을 중요한 모순이 없음을 보고했다. 실제 검토 요청 시점의 plan·색인과 근거, child의 대조·반환,
parent의 대기와 현재 인계를 관측한다. private runner는 plan·색인의 바이트 변화/관측 시각을 보존하며
모델이나 제품의 동작을 수정하지 않는다. 공개 도구 event의 편집·task 시각과 함께 대조한다.

## 시작 조건 오류와 r2 재시작

root는 처음 baseline9파일+config를 복사했지만0039에서 채운 CLAUDE.md/PROJECT-POLICY.md를
기본 template 상태로 남겼다. 첫 설계119.518초·둘째54.871초 뒤 treatment 지문 대조에서 발견했다.
작업 권한·정책·채택 안내의 차이이므로 이 두 턴은 후보 보완 효과의 유효 관측에서 제외한다.
첫 시도는 구현을 요청하지 않았고 두 설계 응답·snapshot·dirty diff·bundle을 원본 그대로 보존한다.
원 모델 실패나 source 결함으로 분류하지 않으며 실험 준비의 오류다.

새 `0040-completion-handoff-muse-r2` private/workspace를 만들고 원0039의11개 baseline파일+
config 바이트 동일성과 기존3시험을 확인했다. 후보에 의한 차이는 feedback·plan 작성본2개·
verifier·REVIEW·PROCESS의6파일이며, 자동 로드되지 않는 이전 patch `.orig` 백업1개가 없다.
r2는 새 세션에서 동일한 첫 요청으로 시작한다. r2의 parent3/native최대1과 wall time은 별도로 기록하며
처음2회를 숨기거나 전체 예산에서 빼지 않는다.

| r2 판 | branch·SHA |
|---|---|
| 설치판 | `codex/0040-r2-template` · `d7b5b40b2fa66a2d141b4839eff22c2436dfe10e` |
| baseline | `main` · `e2804fa3a6ae5029226b37612e94e6dc67257842` |
| 작업판 | `codex/0040-r2-completion-handoff` · 시작 시 위 baseline |

## 실제 실행

r2 parent는121.094초·86.962초·226.840초로 세 번 실행했고 같은 세션을 이어갔다.
native `sdlc-verifier`는 parent의 task가 호출한 별도 세션1개이며85.574초가 마지막 parent 시간에
포함된다. r2 첫 dispatch부터 마지막 종료는545.239초(약9분5초), 최초 준비 시도부터는1020.975초
(약17분1초)다. 최초15분 전체 한도는 변경됐으며 최종20분/r2 15분 한도 안이다.
무효 준비2+유효parent3/native1=총6 product dispatch다. 모델 내부 round-trip 수는 이 숫자가 아니다.

실제 metadata의 parent/child 모두 `opencode-go/muse-spark-1.3-contributor`, variant `xhigh`,
OpenCode1.18.30을 확인했다. 첫 두 유효 단계는 spec/plan만 바꿨고 intent·코드·시험·fixture는
보존했다. 정렬 제안의 제약 충돌을 미정 Q4로 남긴 뒤 마지막 HUMAN의 이유·범위를 받고 intent→
spec→plan→구현/시험을 개정했다. `sdlc-feedback`는 마지막 단계에서 실제 skill 도구로 읽었다.
처음 design-spec/plan은 명시 지정했고 이 사실을 자연 선택의 근거로 세지 않는다.
parent는 세 단계 모두 feedback 본문을 실제 skill 도구로 받았다. 설치 목록만 보고 사용을 추정하지 않았다.

제출은 `dabfba60064444beef7774b394ec1e7099a4213d`의7파일 로컬 commit이며 작업트리는 clean이다.
template/main은 위 판을 유지한다. root가 새 clone에서 collected/run6·실패/skip0, 임시 cfile
py_compile, 기존 독립 CLI11건과 HUMAN의 빈 문자열/값 누락 결정2건을 직접 실행해 통과했다.
추가2건의 기대는 구현 전 HUMAN turn02에서 확정됐으며 실행 도구 작성은 제출 뒤다. 기존 oracle11의
작성 시점과 구분한다. source111·설치134 scoped 지문은 초기/정본과 같으며 전체 repo 불변을 주장하지 않는다.

task 시작 시각1791081712324ms보다 앞선 plan/색인 관측(1791081703191ms/1791081694703ms)에
T01 구현·6시험 완료가 적혀 있다. 원문 편집/tool 시각과 실제 snapshot을 함께 대조하며 같은 commit만으로
편집 순서를 추정하지 않는다. native는 plan·색인·Git 상태·실행 근거를 읽고 검사했다. 커밋 전 실제
작업트리와 색인의 선행 커밋 표기 불일치를 발견했고 parent는 결과를 받은 뒤 로컬 commit했다.
plan의 `로컬 커밋으로 넘긴다`는 예정 표현이므로 그 문장까지 허위 완료로 읽은 child 판단은 과도하다.
native 발견을 무조건 채택한 통과표로 바꾸지 않는다.

마지막 parent의 임시 외부 경로 CLI 호출은 권한으로 차단됐고 plan 편집1회는 oldString 불일치로
실패한 뒤 성공했다. 각 tool error와 복구를 보존하며 top-level rc0을 모든 도구 성공으로 바꾸지 않는다.
child도 없는 개발건 README 읽기·macOS `cat -A`/BrokenPipe·외부 temp 접근 실패 뒤 필요한 자료/실행을
확인했다. 전체 stdout/stderr·실패·복구 원문은 보존한다. 원 계획의15→20분 개정은 마지막 dispatch 전
공개 도구 입력/패치 성공/실행 시작 epoch로 대조했다. 최종 파일 시각을 선행 결정의 증거로 쓰지 않는다.

## 판정

[새 Sol/high의 독립 검증 전문](../research/openwebagent-template-history/intent-design-alignment/0040-retest-validation.md)은
제품 원 제출·공개 대화/도구·검토 전 snapshot·실제 실행·인계 문서를 읽고 아래 관측과 F01을 확인했다.
제품을 수정하거나 새 모델을 호출하지 않았다. root는 원문과 이 결과를 대조해 **전체 부분 통과**로 판단한다.

| 평가한 행동 | 판정·근거 |
|---|---|
| 기존 의도 유지·제약 충돌 확인 | 통과. 첫 두 단계는 설계만 개정하고 정렬 충돌은 Q4로 남김 |
| 이유 있는 제약 변경·문서 선개정 | 통과. HUMAN turn03 뒤 intent→spec→plan→구현/시험 순서와 같은7파일 commit 확인 |
| 실제 구현·회귀 | 통과. 제출 dabfba6의 새 clone에서6시험·독립 CLI13관찰·컴파일 확인 |
| 완료 검토 전 현재 인계 갱신 | 통과. T01 구현/시험 완료와 HUMAN 수락 대기를 plan/채택 색인에 기록한 실제 관측 시각이 task보다 앞섬 |
| 같은 검토의 실제 자료 대조·결과 대기 | 통과. native child의 문서/index/Git/실행 확인·반환 후 parent commit 확인 |
| 최종 인계의 완료 검토 상태와 다음 책임 | 부분. 반환된 검토와 남은 결과 확인의 담당자를 문서 자체로 구분하기 어려움 |

F01: 최종 plan은 `남은 일은 HUMAN 완료 수락과 독립 완료 검토 결과 확인이다`, 색인은
`HUMAN 완료 수락과 독립 검토 결과 확인`이라고 적었다. 검토 요청 전 snapshot과 같은 바이트이며
검토 반환 후 문서 edit는 없다. 최종 대화 응답은 검토를 받았고 커밋 지적을 처리했다고 설명한다.
다음 사람이 문서만 읽으면 검토가 아직 진행 중인지, 개발자의 결과 처리가 남았는지, HUMAN이
수락 전에 결과를 읽으면 되는지 확정하기 어렵다. HUMAN의 확인을 뜻할 수도 있으므로 `검토 미수행`이나
끝난 T01을 미구현으로 둔0039와 같은 실패로 판정하지 않는다. 제품 동작이나 중요한 계약 변경 누락도 아니다.
그러나 이번 대상인 최종 인계 전체가 분명해졌다는 주장에는 이 의미상의 한계가 남는다.

검토 전 갱신과 기존 검토의 실제 대조라는 핵심 보완은 동작했다. 후속 결과가 남은 일을 바꾸면 현재
요약/다음 작업도 맞추라는 지침은 이미 feedback에 있다. 한 관측으로 새 source 규칙·훅·상태 장부를
추가하거나 완벽한 문구를 얻기 위해 제품을 반복 수정하지 않는다. 원 제출과 부분 판정을 보존한다.
전체 AC04 전후 비교,0038/0039의 과거 부분 판정, source AC12의 검증 범위는 바꾸지 않는다.

## 원본 보존과 한계

프로젝트 아래 `.local/experiments/`에 원문을 보존했다. 이 보고서는 원 실행을 대신하지 않는다.

- 준비 오류 시도: `workspaces/0040-completion-handoff-muse/product/`, `private/0040-completion-handoff-muse/`.
  두 설계 턴·snapshot·calibration.json·dirty diff·전체 Git bundle을 보존하며 판정에서 제외한다.
- 유효 제출: `workspaces/0040-completion-handoff-muse-r2/product/`, `private/0040-completion-handoff-muse-r2/`.
  `turns/`의 실제 prompt/response/공개 tool JSONL/meta, `snapshots/`와 `live-snapshots/`의 각 문서판을 보존한다.
- parent `ses_efb3cae5dfferwr1FuZE6uV3Ng`, native `ses_efb35f53fffeprNFkE9Gk51Lv4`의
  `exports/*-original-public.json`은 전체 공개 text/tool 입력·출력이다. sanitize export도 구분해 유지한다.
- source.tar·설치 manifest·baseline11파일+config 직접 대조·권한 probe·debug skill/agent·설치 본문을 보존한다.
  `final-validation/`은 제출 bundle·독립 clone·명령별 argv/cwd/시각/rc/stdout/stderr·6시험과13관찰의 전문이다.
- `independent-review/`은 fresh verifier의 공개 원문 추출·baseline 직접 비교·검토 전문과 SHA다.
  `public-turn-review-input.jsonl`73–75행은 root의 예산 개정과 dispatch 순서의 원문이다.
  meta 색인의104행 후보는 보존 도구 자체 문자열의 검색 오탐이며 선행 개정 근거에서 제외했다.
- `evidence-manifest.json`과 `delivery-record.json`에 보존 대상의 개별 SHA256, 실제 제작 결과판,
  제품 refs·source/WIP 불변 대조를 연결한다. 인증 파일·숨은 추론·runtime 상태·Git 내부 파일은 제외한다.

시험 통과는 HUMAN 수락·main 통합·배포가 아니다. native 호출 성공만으로 모든 기준을 확인했다고
판정하지 않았다. 실제 body 읽기/행동을 관측해도 한 묶음 후보의 개별 문구 효과나 provider 내부 모델
불변성을 입증하지 않는다. source/임시 설치의 전체 정적 검사는 source가 변하지 않은 T16 근거를
재사용했으며 이번에 다시 실행했다고 쓰지 않는다. 원격 PR·통합·배포·새 세션 인계 실행·큰 개발건·
다른 도구 행동·고의 낡은 요약 검출 민감도와 전체 SDLC는 이번 관측 범위 밖이다.
