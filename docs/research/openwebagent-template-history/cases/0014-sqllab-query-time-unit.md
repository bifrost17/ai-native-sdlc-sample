# 0014 — SQL Lab 쿼리 시각 단위

판정: **이력 검토 완료, 운영 관측은 문서 증언.** 원본 Superset의 에폭 밀리초 계약을 이식 코드가 초로 바꾼 결함이다. 생산 함수만 고치면 기존 초 단위 행과 새 행이 섞이므로, 생산·저장 행 이행·프런트 계약을 한 PR로 인도했다. 머지·재배포 후 화면 관측은 별도 문서 PR로 남겼다.

## 사건 사슬

고정 원본은 `.local/research/openwebagent-template-history/20261003/collection/`의 inventory·API와 bare Git, 기준 main은 `a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e`다. [PR #341](https://github.com/bifrost17/openwebagent/pull/341), [PR #342](https://github.com/bifrost17/openwebagent/pull/342)의 본문은 보고자의 진술이며 원시 실행 출력은 아니다.

| 순서 | 확인한 사실·근거 |
|---|---|
| 문제·최초 문서 | [`102e2be`](https://github.com/bifrost17/openwebagent/commit/102e2be1ff1)는 intent·spec·plan을 제품 변경 전에 추가했다. intent `:4-74`는 2초 이상 쿼리 결과 소실과 초/ms 불일치를 분리했고, spec `:26-58,72-166,201-223`은 생산 ms·기존 행 이행·프런트 소비·재배포 화면 4회 기대를 연결했다. 원본 `dates.py`와 이식 `utils/sqllab/utils.py`, `sql_json_executer.py` 비교는 PR #341과 spec SP01에 있다. |
| 설계 인계 | [`d8c67ca`](https://github.com/bifrost17/openwebagent/commit/d8c67cad0a6)가 구현 전 계획 인계 검토를 반영했다. plan `:75-99,117-128,201-260,319-402`는 T01 생산, T02 이행, T03 프런트 모양, T04 이전 0003 문서 정정과 V5 재배포 검증을 구분한다. PR을 한 개로 묶은 이유는 혼합 단위 판을 main에 만들지 않기 위해서다. |
| 구현·변경 | [`aefa8ab`](https://github.com/bifrost17/openwebagent/commit/aefa8ab27b5) T01, [`6b70910`](https://github.com/bifrost17/openwebagent/commit/6b709102906) T02, [`9c180d7`](https://github.com/bifrost17/openwebagent/commit/9c180d737f9) T03, [`35592e4`](https://github.com/bifrost17/openwebagent/commit/35592e458d8) T04가 순서대로 있다. 사이의 `8e2c302`, `7af8b54`, `f3eb411`, `ded0dcf`는 각 실행 기록·계획 이탈을 문서화했다. T02는 downgrade 제수를 `1000.0`으로 바꾸었고, `f8e85b1`은 이행 시험에서 누락됐던 네 번째 시간 열도 채웠다. 코드·시험 변경은 이 커밋 diff에서 확인된다. |
| 검토·통합 | [`b832d59`](https://github.com/bifrost17/openwebagent/commit/b832d593daf)가 V3 게이트와 V4 검토, AC07 문구 정정을 기록했다. PR #341은 집중 시험 30 passed, 변이 M8 생존, PostgreSQL 이행 미검증을 보고한다. [`849a2d5`](https://github.com/bifrost17/openwebagent/commit/849a2d565c)가 #341을 2026-09-25 06:26 KST 머지했다. 시험 원출력·변이 로그를 독립 수집하지 못했다. |
| 사후 검증 | #342의 [`4acb644`](https://github.com/bifrost17/openwebagent/commit/4acb644be)는 plan `:570-625`에 배포 백업, 이행, 브라우저 AC01·07·08을 더했다. 4/4 E1 결과 행과 4/4 GET, 오래된 행의 ms 이행을 보고한다. 첫 빈 결과는 7초 캡처 창이 콜드스타트를 못 따라간 계측 한계로 기록했다. `/home/nara/openwebagent-briefs/0014-deploy/` 원본은 이 수집에 없으므로 운영 PASS는 **문서·PR 진술**이다. V5-6과 PostgreSQL 이행은 여전히 미실행이다. |

## 여섯 축과 가설

| 축 | 판정 |
|---|---|
| 의도 보존 | **충족.** 원 요청의 결과 소실을 단위 계약으로 좁히고 E1 4회 화면 기대를 보존했다. 0015의 별개 execute 500은 범위에서 분리했다. |
| 설계 충실성 | **정적 확인.** 생산 함수·이행 네 열·프런트 ms 소비를 관련 diff와 시험에서 확인했다. 0003의 과거 “에폭 초” 두 줄을 T04에서 정정했으므로 **0003 문서를 현재 정본으로 인용하면 틀린다**. |
| 계획 실행 가능성 | **강함.** 구현 지점·순서·혼합 단위 위험·사후 검증 전제가 명확하다. 커밋은 문서 선행과 각 변경 후 기록을 보여 주지만 RED 명령의 실제 시각은 Git만으로 증명하지 않는다. |
| PR·병렬 분할 | **적절.** 생산과 이행을 묶고 운영 배포 관측을 #342로 분리했다. 병렬 레인 원시 핸드오프는 미수집이다. |
| 변경 피드백 | **기록 있음.** 인계 리뷰, downgrade 제수, 네 번째 이행 열, AC07 기대 수정이 커밋으로 남았다. |
| 검증·보고 | **경계 명시.** #341은 집중 시험과 미검증을, #342는 재배포 실증과 남은 한계를 구분한다. 수치·스크린샷은 문서 진술이며 이번 조사에서 재실행하지 않았다. |

H1: 초기 초/ms 계약 누락은 0003 이식 설계의 결함을 지지한다. 0014 내부 재작업은 주로 시험·표현 보완이며 전체 계획 실패로 일반화할 수 없다. H2: UI 외형 시안 사건이 아니므로 판단 불가. H3: 서버 생산·저장 행·프런트 소비의 전체 계약을 함께 다뤄 지지보다 반례에 가깝다. H4: 재배포 뒤 화면 검증이 최초 plan에 특정돼 있었고 별도 PR로 실행을 보고했다. 원본 로그 부재로 독립 증명은 아니다.

당시 지침의 적용 여부는 세션 원문 부재로 미확인이다. 현행 배포 0.1.8의 plan·검증·선행 갱신 기준과 기존 5파일 WIP의 계획 구체성 문구는 [baseline](../baseline.md)에 이미 구분돼 있다. 이 사례만으로 새 템플릿 규칙을 추가할 근거는 없다.
