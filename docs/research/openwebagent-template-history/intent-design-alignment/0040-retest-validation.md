# 0040 재실험 독립 검증

Status: review complete — 제품 동작·검토 전 갱신 관측, 최종 인계의 검토 상태 구분은 부분

2026-10-04 Asia/Seoul. source `e38477cdf4a6360c473bb76486d1e5e9baa1436e`의 작은 OpenCode
재실험을 검토했다. maker 경로는 `.local/worktrees/intent-design-alignment`, maker 작업은
0028의 T17이다. 제품의 원 제출판은 `dabfba60064444beef7774b394ec1e7099a4213d`, base는
`main@e2804fa3a6ae5029226b37612e94e6dc67257842`다. 아래 발견은 수락·병합·배포 승인과 별개다.
제품/source는 수정하지 않았고 모델 재호출이나 실험 재실행도 하지 않았다.

제품 구현·계약 변경·시험·로컬 커밋과 검토 전 현재 요약 갱신은 원문으로 확인했다.
native 검토도 명명된 child의 실제 읽기·diff·실행·반환까지 관측했다. 최종 plan과 색인은
구현 완료와 HUMAN 수락 대기를 구분한다. 다만 이미 반환된 검토의 완료 사실과 남은 확인의
담당자가 문서에서 구분되지 않아, 독립 검토까지 끝난 최종 인계가 자체 문서만으로 명확하다는
판정은 지지하지 않는다. 이 한계로 제품 동작 검증을 취소하거나0039의 partial을 바꾸지는 않는다.

## Review basis and inputs

maker `.claude/agents/verifier.md`, `REVIEW.md`, `CLAUDE.md`, 0028 현재 intent/spec/plan의
FR13/SP12/AC12와 T16/T17, 0040 사전 설계 검토와 진행 보고를 읽었다. maker verifier의 보고 전용
역할을 적용했다. source가 바뀌지 않은 T16의 전체 정적 검사는 이번에 중복 실행하지 않았다.

북극성의 실제 문장과 주석을 읽었다. [V4-09](../../../verification/north-star-playbook.html#V4-09)는
수락한 plan의 commit과 최종 diff 대조, [V4-11](../../../verification/north-star-playbook.html#V4-11)은
계획 이탈의 같은 commit 개정을 다룬다. [V7-09](../../../verification/north-star-playbook.html#V7-09)는
실제 동작과 plan을 대조하는 보고 전용 검증자이며,
[V8-02](../../../verification/north-star-playbook.html#V8-02)는 작업 중 feedback과 마지막 새 문맥 검토를
구분한다. 완료 요약·색인·실행 근거의 구체적인 대조는 팀의 SP12 보완이다.

원본 위치:

- 준비 오류 시도: `.local/experiments/private/0040-completion-handoff-muse/`.
- 유효 r2: `.local/experiments/private/0040-completion-handoff-muse-r2/`.
- 제출 제품: `.local/experiments/workspaces/0040-completion-handoff-muse-r2/product/`.
- 독립 실행 clone: r2의 `final-validation/final-checkout/`.
- 이번 읽기용 공개 원문 추출과 직접 baseline 대조: r2의 `independent-review/`.

r2 `turns/`의 세 prompt·response·공개 tool JSONL·meta, parent/child의
`exports/*-original-public.json`, 세 단계 snapshot, live plan/index 바이트와 관측시각,
manifest·setup·설치 본문/config, 최종 intent/spec/plan/index·코드·시험을 대조했다.
최종 검증의 명령별 stdout/stderr·rc와 CLI의 전체 행·종료 코드도 읽었다.
인증 파일과 숨은 추론은 읽지 않았다. `independent-review/*-original-public.txt`는 공개
text/tool의 입력·출력·오류만 추출했으며 원 JSON을 대체하지 않는다.

## Commands and execution evidence

이번 verifier가 수행한 검사는 파일 읽기, 공개 event 대조와 아래 Git 객체 바이트 비교다.
제품의 시험·CLI는 root가 원 제출판의 새 clone에서 이미 실행해 보존한 결과를 검토했다.
이를 이번 verifier가 다시 실행했다고 보고하지 않는다.

직접 비교에 사용한 명령은 각11 baseline 경로와 `opencode.json`의
`git show d3c23f3a556d3aa8af18bd3d47c435153fe3d6cf:<path>` 및
`git show e2804fa3a6ae5029226b37612e94e6dc67257842:<path>`, 양쪽의
`git ls-tree -r --name-only <baseline>`이다. Python 표준 라이브러리로 바이트/SHA256을
대조한 명령은 rc0이며 `independent-review/baseline-byte-comparison.json`에 결과를 보존했다.

| 보존된 실제 실행 | 결과와 범위 |
|---|---|
| `/Library/Developer/CommandLineTools/usr/bin/python3 -B <r2>/final-validation/unittest-observe.py` | rc0, collected6/run6, failure0/error0/skip0. 6개 이름과 `OK` 전문 확인 |
| `/Library/Developer/CommandLineTools/usr/bin/python3 -B -c 'import py_compile,sys; py_compile.compile(sys.argv[1],cfile=sys.argv[2],doraise=True)' <clone>/tracker.py <temp>/tracker.pyc` | rc0, stdout/stderr 비어 있음. 임시 cfile 실제 생성·지문·제거 확인 |
| `/Library/Developer/CommandLineTools/usr/bin/python3 -B <r2>/oracle.py <clone>` | rc0, 고정 private oracle11관찰 PASS. 전열·무쓰기·변경 대상/반복·오류 대조 |
| `<r2>/supplement-cli.py`의 argv별 직접 CLI2관찰 | 리터럴 `--owner ''` rc0·빈 출력, 값 누락 rc2·argparse 오류, 각각 데이터 불변 |
| `git status --porcelain=v1 -z --untracked-files=all` | 제출·clone 검증 전후 rc0, stdout/stderr 빈 출력 |
| `git rev-parse HEAD` | 원 제출·clone 모두 dabfba60064444beef7774b394ec1e7099a4213d |

전체 argv/cwd/rc/시각과 출력 경로는 r2 `final-validation/commands/*.json`에 있다.
`unittest-collection-and-result.stderr`의 6개 시험은 owner 정확 매칭·무결과·값 누락과 기존
list·show·complete다. `private-independent-oracle.stdout`은 해당 HEAD의11관찰을 명시한다.
`independent-cli.json`·`supplement-cli.json`의13관찰을 HUMAN 결정/fixture와 별도로 대조했다.
private oracle의 기대는 현재 제품 출력에서 만들지 않았고, 추가2관찰의 harness는 제출 뒤
만들었지만 기대 출처는 구현 전 HUMAN r2 turn02다. 둘의 시점을 같은 것으로 쓰지 않는다.

동작 기대/실제 결과: 기본 list는 R-101/R-102/R-103/R-104, hana는 open R-101과 done R-103이다.
탭4열과 한국어 제목도 일치한다. `han`, `HANA`, 없는 owner는 빈 출력·rc0이다. empty owner는
HUMAN이 정한 리터럴 비교이며 현 fixture 무일치·rc0다. 값 누락은 `expected one argument`·rc2다.
show 정상/없음은 rc0/1, complete R-102만 done·재실행 무쓰기·없는 ID rc1, 잘못된 JSON rc2를
확인했다. 모든 조회와 complete 반복의 파일 바이트 기대는 해당 oracle에서 확인됐다.
`--owner -`의 현 fixture 빈 출력은 제품 시험·parent/child 직접 CLI에 포함됐다.

## Observed sequence and provenance

원0039 baseline11파일과 `opencode.json`은 r2 baseline과 바이트 동일하다. 직접 전체 tracked
tree 대조에서 변경은 `.opencode/skills/sdlc-feedback/SKILL.md`, plan 작성본2개, native verifier,
REVIEW, PROCESS의6파일이다. 기존 `.opencode/skills/sdlc-feedback/SKILL.md.orig` 하나는 없다.
이는 자동 로드되지 않는 patch 백업이며 업무 baseline 변경으로 세지 않는다.
후보 전체가 원0039과 동일하다는 뜻도 아니다.
source111행·설치134행의 scoped 해시 비교는 각 mismatch0이며 대상 행 전체를 검사했다.
실제 native config는 Muse Spark1.3 contributor/xhigh, OpenCode1.18.30이다.
parent와 child export의 provider/model/variant와 명명된 `sdlc-verifier`/parentID를 확인했다.
같은 공개 모델명이 provider 내부 모델의 불변성을 보장하지는 않는다.

단계1·2는 spec/plan만 개정했다. 각 snapshot의 intent·tracker·기존 시험·fixture·색인은 baseline과
같다. 단계1의 Q1–Q3에 HUMAN은 미배정 조회 제외·빈 문자열의 리터럴 매칭·값 누락 exit2를 답했고,
시험 구성/사용 예시는 위임했다. 단계2는 파일 순서 제약과 이유 없는 ID 정렬 제안의 충돌을
Q4로 남겼다. HUMAN turn03이 입력 순서보다 매번 같은 ID순 비교가 중요하다는 이유와 양쪽
목록 정렬·구현·로컬 commit을 명시했다. feedback나 최종 요약 갱신 정답을 후속 입력에 넣지 않았다.

turn03 공개 event에서 intent 제약의 edit 종료는1791081621.615, 영향 spec의 마지막 계약 edit는
1791081639.399, plan 개정은1791081650.572다. 첫 tracker edit는1791081656.455이며
그 뒤 시험을 수정/작성했다. 계약 개정 선행과 같은 최종 commit을 각각 확인했다.
기존 list 순서 시험의 기대 개정은 HUMAN의 명시 제약 변경에 따른 것이다.
show/complete의 기존 assertion은 약화하지 않았다. 선택 전략은 구현 후 시험이며 TDD 이력으로 세지 않는다.

parent는 세 턴 모두 실제 `skill sdlc-feedback`의 본문을 받았다. 설치/catalog만 확인한 결과와
구분한다. turn03 반환 본문에는 완료 검토 전 요약 정리와 같은 검토의 index/evidence 대조가 있다.
parent가 별도로 공통 verifier 파일을 읽은 event는 찾지 못했다. 명명된 native child에는 실제
정의/config가 제공됐지만, parent가 모든 연결 기준까지 읽었다고 확대하지 않는다.

완료 실행 뒤 index edit 종료1791081694.642, plan 요약 edit 종료1791081703.100을 확인했다.
live snapshot은 각각1791081694.703226과1791081703.191359에 동일 바이트를 보존했다.
task 시작은1791081712.324다. 요약은 T01 구현/6시험/CLI를 완료로, HUMAN 수락과 독립 검토
결과 확인을 남은 일로 썼다. 검토 전 갱신 순서는 최종 commit 시각에서 추정한 것이 아니다.
검토 시점 index가 이미 `작업 브랜치 로컬 커밋`이라고 쓴 점은 실제 미커밋 상태와 불일치했다.
plan의 `로컬 커밋으로 넘긴다`는 예정 인도 표현이므로 그 문장만으로 완료 허위 주장이라고 보지는 않는다.

task는 `subagent_type=sdlc-verifier`를 사용했고, child 새 세션 생성/parentID와 반환을 확인했다.
child는 intent/spec/plan·REVIEW/PROCESS·코드/시험/fixture·index를 실제 읽고 Git diff/status와
시험/CLI를 실행했다. task prompt는 plan과 실행 기대를 주었지만 현재 요약/index 행 대조를
별도 명시하지 않았다. child가 채택 기준으로 index까지 읽은 실제 결과를 관측했으며,
호출 성공만으로 전체 검토를 완료했다고 세지 않는다.

child task는1791081712.324–1791081797.898, 85.574초다. parent의 다음 작업은
1791081802.039 이후이고 반환 전 커밋/완료 보고가 없다. parent가 한 commit에7파일을 담았고
commit 뒤 6시험과 clean 상태를 다시 확인했다. 원 fixture와 설치 자산은 최종 diff에 없다.

## Findings and limits

### F01 — 최종 인계에서 독립 검토 완료와 남은 확인의 담당자가 불명확하다

Pass: Policy and scope. 완료 인계 자체의 통과 범위를 제한하는 발견이다.
최종 plan Current handoff는 `남은 일은 HUMAN 완료 수락과 독립 완료 검토 결과 확인이다`,
index 다음 작업은 `HUMAN 완료 수락과 독립 검토 결과 확인`이다. 이 바이트는 검토 요청 전
snapshot과 같고, child 반환 후 수정 event가 없다. parent 최종 응답은 독립 완료 검토를
받았고 지적1건을 commit으로 처리했다고 보고했다.

문서는 T01을 다음 구현으로 남기는0039 오류는 복구했다. 그러나 문서만 읽는 다음 담당자는
검토가 아직 반환되지 않았는지, 개발자가 결과를 처리할 일이 남았는지, HUMAN이 수락 전
이미 끝난 검토를 읽는 것인지 구별할 근거가 없다. 마지막 해석도 가능하므로 `검토 미수행`이나
`HUMAN 수락 완료`라고 판정하지 않는다. SP12의 실제 완료/남은 일 대조에 맞춰, 제작자의 검토
완료 사실과 HUMAN에게 남은 확인/수락의 책임을 구분해야 최종 인계 전체를 명확하다고 판단할 수 있다.
특정 문구·상태 token·새 검토·자기 미래 SHA는 요구하지 않는다. 원 제출판은 보존하고 root가
이 의미상의 한계를 판정/보고해야 한다. 제품 구현 결함이나 새 business 결정 누락은 아니다.

### Native 검토의 정확성과 실행 한계

child의 발견#1 중 index의 선행 커밋 표기는 당시 Git과 불일치했고 최종 실제 commit으로 해소됐다.
plan의 미래형까지 완료 허위 주장으로 읽은 범위는 과도하다. child는 F01의 반환 후 완료 상태 구분을
다루지 못했고, parent의 현재 요약도 검토 뒤 갱신되지 않았다. 새 문맥 검토의 결과를 무조건 신뢰하지 않는다.

child의 `display` 빈 owner도 `-`로 보이는 참고와 ID열 중심 시험 한계는 보존한다.
현 fixture에는 빈 owner 행이 없고 display는 원 baseline 특성이므로 이번 기능 결함으로 승격하지 않는다.
최종 독립 CLI는 전열 기대를 대조했다. native의 모든 주장에 동의하는 PASS 표로 대체하지 않는다.

parent의 `/tmp/req-check.json` CLI 명령은 external_directory 정책으로 실행 거부됐다.
child도 없는 개발건 README 읽기·`cat -A`의 macOS 오류/BrokenPipe·외부 temp 리디렉션 거부를 겪었다.
그 뒤 현재 index 접근과 허용된 CLI/py_compile로 필요한 확인을 했다. 거부된 complete 수동
명령을 성공으로 계산하지 않는다. complete의 근거는 기존 unittest와 root의 독립 oracle이다.
parent 요약 edit의 oldString 실패는 재읽기/성공 edit로 복구됐다. 실패 원문은 그대로 보존됐다.

child 공개 기록에는 edit/write/stage/commit/추가 agent 호출이 없고, 최종 diff·fixture·설치 지문도
의도한 범위에 맞는다. 이는 관측된 무수정 수행이다. 설정 문구만으로 임의 Bash 쓰기가 항상
차단된다는 보장은 하지 않는다. 전역/원제품 변경·원격 인도도 실제 실행 event에서 관측되지 않았다.

### 준비 오류와 예산 개정

최초 시도는 root가0039의 customized CLAUDE/PROJECT-POLICY를 누락했다. parent2회
119.518초/54.871초 뒤 제외했고 구현 요청은 없었다. 원본/calibration/bundle을 보존했으며
이를 source 결함·모델 실패·후보 효과의 유효 관측으로 계산하지 않는다.

r2 parent3회의 CLI elapsed 합계는434.896초, 첫 dispatch1791081270.654044부터 마지막
종료1791081815.893296까지 wall545.239252초(9분5.239초)다. 최초 시작1791080794.9178722부터
마지막 종료까지는1020.975424초(17분0.975초)다. 최초2+r2 parent3+native1로 총6 dispatch다.
native85.574초는 turn03 226.840초에 포함되므로 wall/CLI 합계에 다시 더하지 않는다.

원 계획은 전체15분/4회였다. setup 복구 후6회로 바꾸고, 마지막 구현 dispatch 전 전체 시간만
20분으로 개정했다고 maker의 진행 plan/report에 기록했다. r2의15분은 지켰지만 최초 전체15분은
넘었다. 원15분/4회 설계가 변경 없이 지켜졌다고 보고해서는 안 된다.
후속으로 보존된 공개 도구 원본 `public-turn-review-input.jsonl` 73–75행을 대조했다.
73행 `call_ITwp44v50QPMHfomjmFrseg8`의 UTC 시각은2026-10-04T02:39:48.759Z다.
입력은15→20분의 maker plan/report 패치를 await한 뒤 snapshot, 마지막 run.py 호출을
순서대로 await한다. 74행 같은 call의 결과에 패치 성공·snapshot rc0·run의 진행 session이 있다.
실제 마지막 dispatch 시작2026-10-04T02:39:49.053296Z보다 tool 입력 시각이294.296ms 앞이며,
코드의 await 순서와 완료 출력으로 문서 개정이 dispatch 전에 실행된 것을 확인했다.
원본 SHA256은 `20b18812ba85bec8fb2d259c6f5439be3437d8c0ae0a7ea8fcfd9d6b27c69749`다.
meta 색인의104행 후보는 보존 도구 자신이 예산 문자열을 언급한 검색 오탐이므로 개정 증거에서 제외했다.

## What does not match plan, and what remains unverified

제품 plan의 구현/시험/회귀 범위는 현재 HUMAN 결정과 실제 diff에 맞는다. F01은 완료 인계의
검토 상태/다음 작업 구분에 남은 한계다. task 입력에 index/현재 요약 대조를 직접 명시하지 않은
전달 누락도 관측했다. native가 실제 그 자료를 읽고 대조했으므로 검토 미호출이나 전면 미수행으로
보고하지 않는다. 원 예산 변경은 공개해야 할 protocol deviation이다.

maker 현재 요약/실험 report는 이번 verifier 입력 시점에 실행 중/독립 결과 대조 대기로 남아 있다.
이는 root가 최종 판정·보고를 아직 작성 중인 상태다. 최종 보고가 아니라는 전제를 유지하며 root의
후속 reporting diff만 원본과 대조할 예정이다. 제품 원 제출은 직접 고치지 않는다.

maker `make check`·이전 사슬 diff·bad hook을 이번에 재실행하지 않았다. T17은 고정한 source의
실험/보고이며 해당 maker hook/source는 변경되지 않았다. 독립 제품 실행 결과와 T16의 기존
source/설치 검증을 혼동하지 않는다. 모든 source 자산의 의미 충분성을111 해시만으로 판단하지도 않는다.
원격 PR/main 통합·배포·새 세션의 인계 실행·큰 개발건·다른 도구 행동·고의 낡은 요약 주입의
검출 민감도는 미검증이다. 단일 묶음 후보의 관찰이며 개별 추가 문장의 인과 효과와 전체 AC04
전후 비교 통과를 입증하지 않는다. 0038/0039의 원 제출판과 partial은 유지한다.

## Follow-up — final reporting comparison

root의 후속 판정 뒤 같은 verifier가 최종 reporting diff만 좁게 대조했다. 대상은
`docs/experiments/0040-completion-handoff-muse.md`, 실험 색인의0040행, 이 연구 README의0040절,
북극성 V4-11의 새0040주석, maker0028 plan의 현재 인계/T17이다. 첫 검토의 제품 원문·제출판·
독립 실행 결과·live snapshot과 공개 예산 개정 원문을 기대의 출처로 유지했다.
제품/source 실행이나 변경, 추가 모델 검토 회차는 없다.

이 reporting 범위에 중요한 불일치나 완료 판정 확대는 발견하지 못했다. root는 F01을 받아들여
0040 전체를 partial로 쓰고, 검토 전 갱신·실제 native 대조/반환·계약 선개정·제품 동작은 관측
통과로 구분했다. native의 index 선행 commit 표기는 당시의 불일치로, plan 예정 문구까지
허위 완료로 읽은 부분은 과도한 판단으로 남겼다. 실제 child 오류/복구도 통과 결과에 숨기지 않았다.
F01을 미검토 확정이나 중요한 제품 계약 누락으로 바꾸지 않았다.

maker 현재 인계는 r2 실행·독립 결과 대조가 남았다는 이전 요약을 완료된 관측/보존으로 고쳤다.
T16의 source 인도와 별도 지시로 실행한 T17을 구분했고, T17 실행/한계 보존의 완료가 제품의
HUMAN 수락·통합·배포 완료를 뜻하지 않는다고 명시했다. 이후 후보 채택·원격 통합·큰 실제 사례는
별도 범위다. 원0038/0039 partial과 전체 AC04 유예를 유지하며, 이번 한 번을 개별 문구 효과나
source AC12의 과거 행동 검증으로 소급하지 않는다. 원 source/제품을 더 수정하지 않는 결정은
후속 근거에 따라 남은 일을 갱신하라는 기존 feedback 본문과 충돌하지 않는다.

첫 준비 오류2회/원본 제외 보존, 전체6 dispatch, 원15분/4회에서 바뀐 조건과 dispatch 전20분 개정을
유지한다. 유효 r2 약9분5초와 전체 약17분1초를 구분한다. 유효 product/head와 source/설치의 scoped
지문 수·독립13관찰/6시험은 첫 검토의 실제 근거와 같다. 동일 파일 전체 repo 불변이나 provider 내부
모델의 불변성을 주장하지 않는다. 북극성 본문/기존 V4-11 부분 판정은 그대로이며0040 확인 범위만 추가했다.

`git diff --check`는 rc0이었다. 최종 제작 commit과 `evidence-manifest.json`/`delivery-record.json`은
이 대조 시점에 생성/동결 전이다. 해당 후속 실제 commit/hash/source151·보호 WIP·refs 불변 확인은
root가 맡으며 이번 verifier가 실행/확인했다고 쓰지 않는다. 보고서의 그 보존 경로는 예정된
후속 결과와 연결할 위치다. maker 결과판의 동결 검증을 이번 제품 runtime 통과로 대체하지 않는다.

최초 검토 전문/해시는 `independent-review/0040-retest-validation-original.md`에 그대로 보존한다.
이번 reporting diff·입력5파일 snapshot·후속 검토를 포함한 전문/해시는 같은 private 폴더의
`reporting-review/`에 별도로 남겼다. 제품 F01 자체는 원 제출판의 한계로 유지하며, 이 후속은
root 보고와 현재 maker 인계가 그 원본/판정을 정확히 전달하는지 확인한 결과다.
