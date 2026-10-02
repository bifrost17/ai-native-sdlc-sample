# 0001 project-structure — 정책 전환과 선택·재사용 실행기

조사 상태: **evidence-limited**. 최초 문서·보관 구현, T2 검증 조건 변경, T4의 사용자 변경 보호·재사용 결함, T5 측정과 T6 인계를 주요 사건별로 검토했다. 51개 연결 PR 전체의 코드·시험을 모두 재검증한 상태는 아니다.

0001은 신규 템플릿 설치 이후에도 남아 있던 과거 정책의 실행 경로를 정리하고, 작은 변경마다 전체 검사를 반복하던 비용을 줄이는 작업이다. 상세 설계와 검증 계획은 있었다. 그 뒤 모듈별 구현·검토를 거쳤지만, 실제 두 회차를 연결하는 보고서 전달 경로와 재사용 활성화에서 결함이 발견됐다. 한편 측정에서 이득이 작은 최적화는 구현하지 않았다. 절차가 길었다는 사실과 제품 효과가 입증됐다는 판단을 분리해야 하는 사례다.

## 조사 기준

- **M** = 동결 main `a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e`.
- **A** = 최초 I 경로 추가 commit `7e0c41b87cd4f157922ece4786d07bcf60c2fb0a`.
- **I** = `intent/0001-project-structure/`. `SHA:path:line`은 해당 Git 객체의 경로와 줄을 뜻한다.
- `.local/research/openwebagent-template-history/20261003/analysis/0001/`에 최초/동결 문서, 주요 코드 전후판, PR body, commit index, `source-manifest.json`을 보존했다. branch/title 필터로 50개 PR을 찾고 관련 #270을 추가해 51개를 연결했다.
- Git 객체·시험 코드·수집 PR API를 읽었다. 이 조사에서 제품 시험, Docker, 기존 full, 성능 측정을 재실행하지 않았다. 아래 PASS·FAIL·시간은 **당시 기록**이며 원 /tmp 로그 전체의 현재 존재·해시를 확인한 독립 재실행 증거가 아니다.
- 최초 commit에 이미 문서·측정·선행 구현 보관본과 제품 수정이 함께 있다. commit에서 문서가 처음 보인다는 이유만으로 그 문서가 실제 편집보다 먼저 작성됐다고 추정하지 않는다.

고정판의 주요 원문: [최초 보관 구현](https://github.com/bifrost17/openwebagent/blob/7e0c41b87cd4f157922ece4786d07bcf60c2fb0a/intent/0001-project-structure/implementation/README.md#L3), [최초 PR/검증 계획](https://github.com/bifrost17/openwebagent/blob/7e0c41b87cd4f157922ece4786d07bcf60c2fb0a/intent/0001-project-structure/plan.md#L48), [T4 활성화](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0001-project-structure/plan.md#L1322), [T6 남은 검증](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0001-project-structure/plan.md#L2209).

## 주요 사건 사슬

| 사건 | 당시 결정·계획 | 실제 변경·시험·인계 | 근거 |
|---|---|---|---|
| 9/14 의도 수립 | CLAUDE의 문구뿐 아니라 참조·실행 경로에 남은 과거 정책을 제거. 작은 변경 선택, 성공 보존, 실패 후 재개, 배포 전 full을 함께 요구 | “30~40분”은 사용자 경험으로 기록하고 실측으로 부르지 않음. 템플릿 설치 사실만으로 완료하지 않는다고 명시 | `A:I/intent.md:6-38,46-53` |
| 설계 중 선행 구현 | 설계 마무리가 요청된 시점에 시험 정리 일부를 이미 작성 | 기존39+신규4, 총43경로를 원복·패치 보관. 93 gate는 중간 집합. 패치 재구성 검증과 제품 테스트 통과를 구별; 새 catalog/verify/cache/resume은 미구현 | `A:I/implementation/README.md:3-38`; `A:I/plan.md:13-17`; [#259](https://github.com/bifrost17/openwebagent/pull/259) |
| 초기 비용 측정 | 기존 full 비용을 먼저 관측 | baseline-01 중단, baseline-02 68 OK/29 FAIL/1 NEVER-RAN·85분48초. recordFinalized/runCompleted/runPassed를 분리. 85분을 성공 full 기준이나 최적화 전후 개선율로 사용하지 않음 | `M:I/measurements/findings.md:27-57` |
| 초기 설계 리뷰 | 기대효과와 intent를 별도 검토. 일반 run과 resume 목표 집합의 모호성을 발견 | 독립 리뷰 gpt-5.6-sol/high 기록. 광역 입력·reuse none이 남으면 효과가 작을 수 있다고 초기부터 경고. 이전 “material finding 없음”을 현재 증명으로 사용하지 않음 | `A:I/reviews/expected-outcomes-and-intent.md:22-28,50-57,79-101,136-143` |
| 첫 plan/PR1 전달 | PR1 정책·시험 정리 → PR2 공통 정의 → PR3 선택/재개 → PR4 비용 → PR5 기본 전환. 기존 회귀·구현 후 시험·직접 관찰의 혼합 | T0/T1는 보관본 재사용과 현재 운영 계약 이관, T2~4는 fixture 계약, T5~6은 실제 어댑터·결합 관측으로 구분. PR1 집중 결과를 전체 완료로 확대하지 않음 | `A:I/plan.md:48-63,303-316`; [#259](https://github.com/bifrost17/openwebagent/pull/259) |
| T2 공통 정의 전환 | 최초 plan은 clean 결합판의 실제 adapter/full/capture를 main 전환 조건으로 요구 | #260의 옛 판을 #263이 대체. 지원 환경 문제 뒤 요청자가 이 Mac에서는 가능한 검증으로 merge하고 full/capture는 지원 환경, 늦어도 T6에 수행하도록 변경 | `A:I/plan.md:150-160`; `M:I/plan.md:23-26,169-182`; [#260](https://github.com/bifrost17/openwebagent/pull/260), [#263](https://github.com/bifrost17/openwebagent/pull/263) |
| spec/plan 갱신 정책과 template delta | 9/15 요구·동작·범위·AC 변경은 요청자와 조정, 그 밖의 보완은 구현 바로 다음 commit에 기록 | #261 규칙 정정, #262 TDD optional 0.1.7 delta 적용. 이를 모든 사소한 편집에 재승인이 필요하다는 규칙으로 확대하지 않음 | `M:I/plan.md:13-18,175`; [#261](https://github.com/bifrost17/openwebagent/pull/261), [#262](https://github.com/bifrost17/openwebagent/pull/262) |
| T3 선택·입력 지문 | 입력/도구/비교 범위와 소비자 전파를 구현 | 완료 후 일부 lane의 doc-next-commit 이탈을 소급하지 않고 기록. G의 여러 행동 commit 뒤 문서가 마지막 `d6b703172`에 몰린 사실을 명시 | `M:I/plan.md:1788-1797`; [#265](https://github.com/bifrost17/openwebagent/pull/265) |
| R9·T4 선행 유지 체계 | 요청자가 gate 선언 유지와 정적 표류·reuse 자격을 채택 | R9·AC25~27, `docs/GATES.md`, drift 검사·자격 검사와 인계 작업. 작은 선언 유지가 별도 작업으로 확장된 이유는 기록된 요구 변경 | `M:I/plan.md:174,1817-1818`; [#266](https://github.com/bifrost17/openwebagent/pull/266), [#270](https://github.com/bifrost17/openwebagent/pull/270) |
| PR-A #272 사용자 변경 보호 | R8의 기존 제약을 이미 어기던 i18n HEAD 복원, unfrozen uv, 배포 루트 상속을 먼저 수정 | 첫 snapshot 수정 뒤 비정상 종료 손실, 다음 EXIT trap 수정 뒤 미완성 snapshot 복원 손실을 리뷰가 재현. cp 성공 후 trap 무장으로 수정하고 SIGTERM fuzz40회 삭제0 기록. 남은 회귀 생존 mutant·정리 잔재도 기록 | `M:I/plan.md:230-287`; [#272](https://github.com/bifrost17/openwebagent/pull/272); `af276a1900e:scripts/ci/gates/commands.sh` |
| 반복 리뷰 뒤 전제 재검토 | 사용자가 custom 실행기 전제와 개발 기간을 우려, 서드파티 대체를 조사 | 요청자는 현 plan 유지와 gate 근거의 독립 필요성 재확인(R10·AC28)을 선택. 94→93 gate 감사를 별도 새 의무로 중복시키지 않고 reuse 감사와 병행 | `M:I/plan.md:76-87,1805-1809`; [#274](https://github.com/bifrost17/openwebagent/pull/274), [#275](https://github.com/bifrost17/openwebagent/pull/275), [#280](https://github.com/bifrost17/openwebagent/pull/280) |
| T4 3a/3b 순서 재설계 | 요청자가 읽기 전용 조사 결론을 채택. 선언/감사3a → 상태·resume1/2 → 활성화3b | 엔진이 아직 없는데 readiness만 true로 바꾸면 거짓 신호가 되므로 미룸. 반대로 선언이 비어 있으면 실제 경로를 못 밟는다는 위험도 이미 인지 | `4fcbcc6d70d:I/plan.md`; `M:I/plan.md:1910-1924`; [#281](https://github.com/bifrost17/openwebagent/pull/281) |
| T4 모듈별 구현 | mutation 관측/선언, SQLite state, argv capture, run, resume, 수명, 잠금, redaction을 순차 전달 | #284~295에서 각각의 시험·부분 완료를 기록. 실제 catalog는 모두 reuse none이어서 제품 catalog의 CACHED 경로는 아직 열리지 않음 | `M:I/plan.md:88-100,1324-1327`; [#288](https://github.com/bifrost17/openwebagent/pull/288), [#291](https://github.com/bifrost17/openwebagent/pull/291), [#295](https://github.com/bifrost17/openwebagent/pull/295) |
| 3b 직전 N1/N2/N3 발견 | #296 독립 리뷰가 활성화를 차단 | N1 임시 run_root에 쓴 보고가 삭제되고 reader는 장부 디렉터리를 읽음. N2 artifact identity 미구현인데 outputs gate의 reuse 설정을 기계적으로 막지 않음. N3 CACHED가 이번 회차 producer FAIL의 BLOCKED보다 먼저 판정됨 | `465144ab28d:scripts/ci/verification/reuse.py:69-105`; `465144ab28d:scripts/ci/verify.py:637-673`; [#296](https://github.com/bifrost17/openwebagent/pull/296) |
| #297 결합 경로 수정 | 새 요구 없이 기존 AC9/20/26의 구현 결함을 고침 | N3 test `83ce1f2267a`→`b093ecdb0d0`, N2 `58f850a443f`→`56dc28f1bfa`, N1 `3323953898a`→`d219e219b11`. 정리 전 보고를 원자 저장·gate별 병합. 실제 다음 회차, 부분 실패·SIGKILL을 시험 | `d219e219b11:scripts/ci/verify.py:541-591,692-739`; `d219e219b11:scripts/tests/verification/test_resume.py:897-987`; `56dc28f1bfa:scripts/ci/gate-definition.mjs:471-478`; [#297](https://github.com/bifrost17/openwebagent/pull/297) |
| #298 추가 보정 | N4 redaction, N5 잠금 probe 경쟁, N6 문서 불일치 | 잠금 probe가 실제 LOCK_EX를 잡아 새 회차를 거짓 거부하는 경합을 2000회 중293회 재현했다고 기록. 유한 재시도 뒤0/2000. “입력 안 바뀜” 설계 설명은 실제 5gate 입력 확대와 맞게 정정 | `M:I/plan.md:1244-1313`; [#298](https://github.com/bifrost17/openwebagent/pull/298) |
| #299 실제 재사용 첫 활성화 | 93개 중8개만 result, 나머지85 none. outputs/resources/mutations와 숨은 host 분기 확인 | `96a17f44b` test→`2875eadbb` 9줄 설정 변경. 실제 catalog·실제 input archive를 가져와 두 회차 OK→CACHED, 파일 변경 재실행, 대조군을 시험. 명령은 exit0 대역이므로 gate 본문 실환경 검증은 아님 | `M:I/plan.md:1322-1398`; `2875eadbbf4:scripts/tests/verification/test_reuse_live.py`; [#299](https://github.com/bifrost17/openwebagent/pull/299) |
| PR-C 잘못된 전제 철회 | docker-volume 과선언 제거와 정적 resources 대조를 조사 | 실제 호출을 끝까지 추적하니 과선언이 아니었음. 정적 prototype의 오탐·미탐으로 새 동적 계기가 필요해졌고 요청자가 문서화만 선택. 원 catalog를 불필요하게 바꾸지 않음 | `M:I/plan.md:218`; [#300](https://github.com/bifrost17/openwebagent/pull/300) |
| PR-B 거짓 성공 보정 | 수집0·LOCAL_ONLY 보류를 성공 cache에 섞지 않음 | frontend 판정을 gate 명령 안으로 옮기고 candidate 장부에 사유 추가. 상태 어휘를 임의 확장하지 않음. fake Vitest 검증과 실물 미실행을 구별 | `M:I/plan.md:1500-1543`; [#302](https://github.com/bifrost17/openwebagent/pull/302) |
| T5 비용 가설 측정 | 공유 prepare·fixture seed 재사용·저비용 검사 선행·제한 병렬을 검토 | uv4회 합0.137s/58.1s=0.24%, 선행 sync는 같거나 느려 공유 prepare 안 만듦. artifact fixture 재구조의 안전한 몫은1.4%라 안 만듦. 저비용 검사 재배열은 시간 단축이 아닌 진단 복구로 기록 | `M:I/plan.md:1945-1973,2052-2064,2134,2189-2192`; [#303](https://github.com/bifrost17/openwebagent/pull/303), [#304](https://github.com/bifrost17/openwebagent/pull/304), [#305](https://github.com/bifrost17/openwebagent/pull/305), [#306](https://github.com/bifrost17/openwebagent/pull/306) |
| T5 “사실상 종결” | Docker stage 최적화는 지원 환경, 제한 병렬은 요청자가 설계만 선택 | #307 제목만 보면 전체 완료로 읽힐 여지가 있으나 body는 두 미구현 항목을 명시. 성능 예산·개선폭·허용 변동 미합의여서 전체 R6 효과 수락은 아님 | `M:I/plan.md:156-164,1951-1956,2052-2053`; [#307](https://github.com/bifrost17/openwebagent/pull/307) |
| T6 부분 인계 | 전체 결합·기본 전환·trusted full/capture 의무가 남음 | unownedInputs21개, 정책 소비자 재검증, PATH tool observation 계기·두 회차 자격 배선 구현. PATH 재설정·보고 파일 부재의 관측 사각을 명시. 500시험 기록을95개 current gate full로 읽지 않음 | `M:I/plan.md:2209-2295`; `M:I/execution/policy-inventory.md:47-92`; [#308](https://github.com/bifrost17/openwebagent/pull/308), [#309](https://github.com/bifrost17/openwebagent/pull/309), [#310](https://github.com/bifrost17/openwebagent/pull/310) |

## 이 사례에서 실제로 빠진 연결

N1은 모듈마다 있어야 할 기능이 전혀 없던 문제가 아니다. 작성 모듈은 임시 `run_root`에 관측을 남겼고 읽기 모듈은 장부 옆 보고를 확인했다. 없는 보고는 자격 축을 적용하지 않는 정책이어서 실패가 겉으로 드러나지 않았다. `465144ab28d`에서 writer 종료 뒤 `shutil.rmtree`는 있지만 두 위치를 잇는 publish는 없다. `d219e219b11`이 정리 직전 publish를 추가했고, `test_the_run_observation_report_lands_where_the_next_run_reads_it`가 두 회차의 연결을 직접 검증했다.

N2는 artifact cache를 구현한 수정이 아니다. 산출물 identity를 아직 확인하지 못하므로 outputs가 있는 gate는 reuse를 켤 수 없도록 거부한 수정이다. #299에서 실제로 켠 여덟 gate에는 outputs가 없다. “T4 재사용 완료”를 “artifact 재사용 구현 완료”로 읽으면 틀린다. N3 역시 새 성공 정의를 만든 것이 아니라 기존 실패 의존성 계약이 CACHED보다 먼저 적용되게 했다.

이 셋은 기능 분할의 완료를 실제 사용자 경로의 완료로 묶기 전에 최소 수직 시험이 필요한 근거다. 다만 활성화 전 리뷰에서 막았고 당시 catalog는 전부 none이었으므로, 이 자료만으로 사용자에게 잘못된 CACHED가 이미 제공됐다고 주장할 수는 없다.

## PR body·commit message·최신 문서의 정확성

| 확인한 표현 | 대조 결과 | 판단 |
|---|---|---|
| #272 body의 “모든 뮤테이션이 새 회귀에 재킬됨” | `M:I/plan.md:274-279`는 trap을 cp 앞으로 옮긴 mutant 하나가 새 회귀를 통과했고 SIGTERM 중단 갈래를 별도로 재지 않는다고 명시 | **표현 과장 확인.** 최종 제품의 tracked-file 손실을 입증한 것은 아니지만 “모든” mutation 검출 주장은 상세 기록과 충돌한다. PR body를 수정본의 실제 proof와 대조해야 함 |
| #272 “3라운드 리뷰 뒤 보호” | 같은 plan이 첫 snapshot→EXIT trap→cp 뒤 무장으로 새 손실 경로를 순차 발견한 과정을 남김 | 리뷰 횟수는 결함 부재 증명이 아님. 반대로 최종3차 이후에도 같은 데이터 손실이 남았다고 단정할 근거는 없음. 남은 것은 기록상 회귀 강도·제한된 잔재 문제 |
| #297 N1/N2/N3 수정 설명 | 수정 전 reader 경로·분기·cleanup과 수정 후 publisher·schema guard·BLOCKED 순서를 Git 코드에서 확인 | 핵심 동작 설명은 대조 범위에서 일치. body의437시험 통과는 당시 주장으로 보존하며 이번 조사에서 재실행하지 않음 |
| #299 “실제 재사용 경로” | 실제 catalog와 inputs를 쓰지만 실행 명령은 exit0 대역(`M:I/plan.md:1347-1365`) | 실제 **조정기/선언 두 회차**를 뜻한다. 실제 Docker/npm gate 본문 통과로 확대하면 안 됨. PR body에는 이 대역 경계가 상세 plan만큼 드러나지 않음 |
| `docs: T5 사실상 종결`과 #307 제목 | body·plan은 Docker 미실행, 병렬 설계만, 성능 예산 미정이라고 명시 | title만으로 전체 효과 완료를 오인할 수 있으나 본문이 한계를 숨긴 사례는 아님 |
| M plan의 “열린 #260” | `M:I/plan.md:167`은 옛 판이 열린 채 남았다고 서술. 수집 PR API는 closed, closed_at `2026-09-17T12:01:06Z`, merged_at null | **현재 상태 표류 확인.** 역사 인계 문장을 10/3 현재 PR 상태로 사용하면 틀림 |
| M plan의 catalog93개/8 result/85 none | 당시 `2875eadbbf4` catalog는 실제93/8/85. 동결 M catalog는95/8/87, 이후 `sqllab-port-license`·`sqllab-release-docs` 추가 | **역사 설계/실행판을 현재 정본으로 오인할 위험이 실재.** 초기 수치는 당시 사실로 유지하되 현재 운영 수치는 실제 catalog를 읽어야 함 |
| PR1 정책 소비자 표 | T6 재검증은 15행 중2행이 더 이상 유효하지 않다고 명시. composer gate 제거·sqlexec SHA 보호 판단 변경을 따로 기록 | 과거 표를 덮어쓰지 않고 시점과 변경 이유를 보존한 좋은 사례. `M:I/execution/policy-inventory.md:47-73` |

#272 body의 대조 출처는 수집 `collection/api/pulls-pages.json`의 PR272 `body`이며, 분석용 `pr-272.md:26-28`에도 보존했다. API는 현재 body snapshot이므로 그 문장이 언제 수정됐는지까지는 확정하지 않는다. commit message에 적힌 RED/GREEN 역시 시험 코드 commit 순서는 확인할 수 있지만, 메시지만으로 당시 명령 실행을 입증하지 않는다.

## 여섯 축 판정

| 축 | 판정과 근거 | 귀속 |
|---|---|---|
| 의도 보존 | 사용자 경험30~40분과 실측85분 실패를 분리. 과거 정책 제거·선택·resume·배포 full 요구를 유지. Mac full 유예·R9/R10·병렬 설계만 결정은 문서로 추적 가능 | 요구 변경 자체를 template 과도 통제로 분류하지 않음. 원 사용자 대화 전체는 미확인 |
| 설계 충실성 | 상세 execution/gate-policy, 상태·지문·자원·출력 계약이 초기에 존재. 이후 N1 저장/소비, N2 산출물 자격, N3 판정 순서 누락 | product design/agent implementation. 문서 양과 인터페이스 실행 완전성은 별개 |
| 계획 실행 가능성 | 최초5PR/T0~T6·검증 전략·실환경 전환 조건이 구체적. 환경 제약으로 full 조건을 사용자가 바꾸고, gate 감사/선언/활성화 순서를 조정 | tool-environment와 user scope. 처음의 필요 전제를 더 일찍 실행 확인할 여지는 있으나 검증 방법 부재로 일반화 불가 |
| PR·병렬 분할 | 작은 PR로 실패 경계를 확인하고 일부 위험을 활성화 전에 차단. 51PR로 확대돼 실제 reuse 첫 성공은 #299 | 실행기 모듈별 완료와 두 회차 경로 완료의 연결이 늦음. T4 세분화는 요청자 채택 결정이라 템플릿이 강제한 분할로 단정 불가 |
| 변경 피드백 | 과선언 가설 철회, N6 문서 불일치 정정, doc-next-commit 편차 기록, 작은 최적화 미구현 결정 | 좋은 피드백 사례. 최신 plan의 역사 인계와 current 상태가 섞이는 표류는 doc maintenance 문제 |
| 검증·보고 정확성 | baseline 실패 보존, setup/fixture/full 구별, two-run test, mutation·signal 검토가 존재 | #272 body의 전량 mutation 검출 과장, full 미실행·시간예산 미정, 관측 report fail-open 범위가 한계. 전체 검증 완료로 합산 불가 |

## 네 가설 판정

**H1 설계 부족이 잦은 변경을 만들었다 — 부분 지지.** N1/N2/N3과 i18n cleanup 단계의 불변식 누락은 구체적이다. 그러나 초기 설계와 독립 검토가 없지는 않았고, 일부 변경은 사용자 요구(R9/R10)와 실행 환경 제한으로 발생했다. 설계 중 구현43경로가 이미 생긴 사실은 문서 선행 순서를 Git 최초 추가로 판단할 수 없다는 추가 한계다.

**H2 실제 UI 대신 HTML mock을 봤다 — 이 사례의 직접 판정 대상 아님.** 주 제품은 CLI와 gate 실행기다. 이에 대응하는 검증 차이는 fake Docker/Vitest/exit0 command와 실제 Linux full/capture다. #299의 조정기·catalog 검증은 유효하지만 실제 gate 본문이 도는 지원 환경 증명을 대신하지 않는다.

**H3 모듈의 늦은 통합이 실패를 만들었다 — 구체적 지지.** N1의 producer/report/consumer 경로는 모듈 단위 시험과 실제 두 회차 사이의 단절이다. 3a/1/2/3b 계획은 그 위험을 이미 언급했는데도 활성화 직전까지 빠졌다. 처음부터 작은 gate 하나로 관측 생성→보존→다음 회차 거부/재사용까지 실행하는 전달 기준이 유효한 개선 실험이다. 모든 모듈 내부 설계를 먼저 끝내는 처방까지 입증한 것은 아니다.

**H4 초기 검증 방식 고려가 부족했다 — 일부 반증, 실환경 준비 공백은 지지.** 첫 plan은 방법·fixture·full·증거 경계가 상세했다. 실제 Mac/Linux·Rosetta·BuildKit·공유 Docker 제약, 지원 환경 full의 미완료, 실사용 catalog가 전부 none이던 상태가 효용 입증을 늦췄다. “시험 수”보다 first usable slice와 환경 전제의 실행 증거를 앞당길 근거다.

## 현재 템플릿 대조에 넘길 입력

0.1.8·WIP5의 문장별 비교는 기준판 조사와 결합 전 **미판정**이다. 당시에도 요구/AC 변경 조정, 설계·plan 동기화, 검증 전략 선정, 독립 리뷰와 실패 보존 규칙이 있었다. 아래 사건을 자동으로 새 규칙 부족으로 귀속하지 않는다.

- 첫 runnable slice가 실제 producer→consumer 경로를 끝까지 확인하는지: N1 report 전달과 #299 실제 catalog 활성화를 평가 입력으로 사용.
- PR 설명이 상세 proof와 같은 범위를 말하는지: #272의 “모든 mutation”과 #299의 명령 대역 경계를 대조.
- 역사 spec/plan의 상태표와 현재 catalog/API를 구분하는지: #260 상태와93→95gate 변화, T6의 옛 소비자 표 정정 사례를 함께 사용.
- 필요 전제가 없는 검증을 막아 둔 상태에서 어떤 부분을 완료라 부르는지: T2 사용자 결정, T5 미구현 선택, T6 미완료를 구분.

## T2·T3 후속 심층 보완

앞선 조사에서 미검토로 남긴 T2/T3의 주요 통합·선택 경계를 추가로 읽었다. 아래 기록은 `M:I/execution/shared-definition-transition.md`와 `selection-coordinator.md` 및 선택한 실제 생산/시험 diff를 대조한 결과다. 94개 gate의 모든 본문과 모든 시험을 전수 검토한 것은 아니다.

| 사건 | 실제 원인·수정·검증 | 판단·근거 |
|---|---|---|
| T2 초반 구조 리뷰와 실제 실행의 차이 | 초기 독립 검토는94개 순서·registry·private definitionRoot·4단계 ABI·24catalog/8artifact 집중 통과를 확인했으나 trusted full/capture는 미확인. 이후 실제 실행은 text2sql17번, root-node23번, artifact26번에서 차례로 실패. | 독립 리뷰 범위를 전체 동등성으로 확대할 수 없다. `M:I/reviews/pr2-implementation.md:3-23`; shared-definition-transition148-163 |
| 잘못된 진행 범위 보고 | 앞선 문서는 artifact-manifest를 “마지막 gate”라 했지만 실제26/94였다.27~94의68개 gate는 당시 한 번도 실행되지 않았다고 후속이 정정했다. | PR 본문 외에도 인계 요약 정확성을 대조해야 하는 실제 사례. 과거 full 실패를 완료로 읽으면 안 된다. `M:I/execution/shared-definition-transition.md:148-163` |
| adapter cwd 통합 회귀 | 공통 adapter가 원 셸 cwd 대신 subjectRoot로 이동해 Vitest455 suites 수집 실패·$lib 해석 실패. `6aa9ed4b5`는 caller의 PWD를 별도 NUL종결 `.cwd`로 전달; `55c11c1dd`는 prepare/execute가 같은 검증 helper를 사용. | 실제 adapter 경유 About.test가 root cwd에서는FAIL, apps/open-webui에서는PASS. fake 명령 순서 일치로 잡지 못한 integration contract. 생산 diff와 기록을 확인. `M:I/execution/shared-definition-transition.md:180-218,268-289` |
| 실행 정의의 의존 전파 | 이동한 run_gate 위치를 가정한 diagnostics시험, 새 import가 fixture에 없는 rollback, artifact-manifest의 definition 입력 누락을 수정. browser timeout과 hardening 원인은 별도 미확정. | 구조 추출은 동작 보존 의도였어도 실제 consumer·fixture·입력 계약 변경을 동반했다. `M:I/execution/shared-definition-transition.md:188-201,268-289` |
| 사람의 범위 결정·잘못 넓힌 해석 | 최초 사용자 문장은 “이 맥 환경에서 full은 포기…지원 가능 환경에만 적용”. 완료 전 검토가 이를 PR2 merge 허용으로 넓힌 점을 지적했고 사용자가 별도로 “머지 허용, full은 T6까지” 선택. PR263의 옛 merge금지 본문도 갱신. | 사용자 결정과 agent 해석을 분리한 좋은 복구. OS 제약을 임의 면책으로 만들지 않았다. `M:I/execution/shared-definition-transition.md:294-301,326-347`; [PR263](https://github.com/bifrost17/openwebagent/pull/263) |
| T3 첫 runnable slice | `07edfa7a5` 기대표/stub RED→`f6fdc33ea`68GREEN; CLI는 구현 후 시험으로 별도 표시. readiness 전환 전 실제 catalog의 list/run은 rc2였고 실행/resume 저장은 T4로 남겼다. | 계산·표시 인도와 실제 효용을 구분했다. early strategy 부재 주장은 반증. `M:I/execution/selection-coordinator.md:3-55` |
| 선언/명령 변경 비선택 | R1에서 adapter·명령·catalog 비선택 필드가 바뀌어도 gate를 선택하지 않음. `fa0b33199` RED→`294a76b1b`: whole gate canonical JSON·tool/resource registry diff와 shared definition 확대를 추가. | 선택기 내부 그래프가 맞아도 실행 정의와 연결이 빠지면 필요한 gate를 놓친다. 생산 diff 및 동일 Python별 RED/GREEN 기록 확인. `M:I/execution/selection-coordinator.md:152-175`; [PR265](https://github.com/bifrost17/openwebagent/pull/265) |
| read-only 조회가 index를 변경 | stat-dirty에서 list/dry-run이 사용자 index를 다시 씀. `970234bc1` private index로 고쳤으나 copyfile의 새 mtime 때문에 같은 초/같은 크기 dirty를 clean으로 보는 racy-Git 회귀. `fccc75a48`은 copy2로 mtime 보존. R3 `c30ca8583`는 오래된 sharedindex 파일 존재가 아닌 actual shared-index-path를 검사. | “읽기 전용”의 실제 부작용·mtime 의미·환경 경계를 반복 review가 찾았다. 생산 diff와 deterministic mtime RED→GREEN/3.9반복15회 기록 대조. `M:I/execution/selection-coordinator.md:161-173,214-216` |
| 입력 지문 불완전성 | `61bfd734a`는 중첩 repo 내용을 재귀 해시하고 directory symlink를 opaqueInputs로 전파, T4 reuse none 조건으로 인계. `632221b77`는 GIT_CONFIG_COUNT/PARAMETERS 등 환경 주입과 node 호출 상속을 제거. | repo 밖 file symlink, fsmonitor/untracked-cache 조합·sha256 repo·잘못된UTF8 출력 등은 미검증으로 남았다. `M:I/execution/selection-coordinator.md:163-167,197-205`; 생산 diff 대조. |
| R3 추가 review와 검증 비용 | origin/main 없는 clone readiness 실패, Cf제어문자 출력, Python/JS 목록 동기화, profile밖 consumer·basename 오인 공백을 보완.185시험100~122초, 실제 list/dry-run 도구 호출0 및 index hash/mtime 불변 확인. | 이미GREEN인 구현은 mutation으로 판별력만 확인했고 억지 RED를 만들지 않음. trusted full/capture는 여전히 미완료. `M:I/execution/selection-coordinator.md:207-243` |

이 보완은 H3의 adapter→실제 command cwd, selection→실행정의 전파 사례를 추가한다. H4는 시험방법 자체보다 **실제 caller/consumer를 거치는 첫 인도와 지원 환경 확보**에 공백이 있었다는 쪽으로 좁혀진다. PR263 문구 정정과 사용자 원문/해석 분리는 이미 수행된 좋은 행동이며 템플릿에 새 규칙이 없었다는 증거가 아니다.

## OS·모델·남은 조사

당시 baseline 환경은 Linux amd64/Rosetta·CPU6·실제8GiB였고 생성 요청12GiB와 달랐다(`M:I/measurements/findings.md:34-38`). 이후 Mac의 Bash5.3, Python3.13/시스템3.9, BuildKit overlay 제한과 shared Docker 보호가 기록돼 있다(`M:I/plan.md:177-193`). Windows에서 이 동작을 검증한 근거는 이 조사에서 확인하지 못했다.

초기 설계·계획 독립 검토는 `gpt-5.6-sol/high`를 명시한다(`M:I/reviews/intent-spec-plan.md:11-12`, `expected-outcomes-and-intent.md:22`). 후속 PR의 Claude Code 표시와 `claude/` branch만으로 실제 모델을 특정하지 않는다. T4 각 lane의 모델·추론 수준·교체 이유와 다른 모델을 썼을 때의 비용은 모른다.

| 범위 | 조사 상태 | 남은 근거 |
|---|---|---|
| 최초 intent·보관 구현·설계/계획·실패 baseline | reviewed / 실행은 evidence-limited | 최초 commit 이전 설계·편집 순서의 원대화, 개별 측정 원로그 전체 |
| #272 반복 수정·#296~299 재사용 연결 | reviewed / 실행은 evidence-limited | PR272 최종 모든 코드 경로의 재실행, 원 리뷰/퍼즈 로그, PR body 편집 이력 |
| R9/R10·T4 분할 결정·T5 효과 부정·T6 인계 | reviewed / 실행은 evidence-limited | 사용자 원대화, 성능 원시 자료와 현재 지원 환경 full/capture |
| T2 실제 adapter 주요 회귀·T3 R1/R2/R3 핵심 선택/지문 수정 | reviewed / 실행은 evidence-limited | 본문 보완의 실제 code/test diff·실행기록 확인. 원 로그와 전체94 gate 실행은 재검증하지 않음 |
| T2 adapter 모든 소비자·T3 남은 모든 선택/지문 경계·94 gate 감사 전량 | not-reviewed | 51PR 전체 세부 코드·시험과 audit 원자료. 주요 사건 추가 검토를 전량 검토 완료로 확대하지 않음 |
| current M 전체 효과·기본 전환·T6 수락 | evidence-limited | I 경로 마지막 변경은9/17. `execution/acceptance.md`·`execution/performance.md`는 M에 없음. 다른 경로의 후속 증거 여부와 최신 main의 실제 full은 별도 조사 필요 |

원대화가 필요하면 root 조사에서 **2026-09-14 설계 중 구현/원복**, **9/16 custom 실행기·R9/R10·T4 순서 채택**, **9/17 병렬 설계만·T5 종결과 T6 인계**에 해당하는 세션을 좁혀 찾아야 한다. 세션 ID는 현재 Git/API 자료에서 확정하지 못했다. 전체 채팅을 읽지는 않았다.
