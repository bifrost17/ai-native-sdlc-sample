# 최종 보고서 독립 비판 검토

검토일: 2026-09-12. 대상은 같은 디렉터리의 주보고서 초안과 그 근거 자료다. 신규 에이전트 실험, 벤치마크, 대상 프로젝트 테스트, 보관한 연구 코드 실행은 수행하지 않았다. 공개 JSONL을 읽어 비용과 표본 수만 독립 재계산했다. 주보고서는 직접 수정하지 않았다.

## 판정

**초안에서 P1 0건, P2 3건을 확인했다. 아래 재검토에서 P2 3건 모두 해결을 확인했으며, 검토 범위 내 미해결 P1/P2는 없다.** “엄격 TDD의 일괄 강제 근거가 부족하고, 작업에 따라 짧은 구현 후 검증을 허용한다”는 조건부 결론을 뒤집을 문제는 확인하지 못했다. 아래 지적은 수정 전 상태를 보존한 검토 기록이다.

### P2-1. Finster의 비용을 재시도·중단을 포함한 총 API 비용으로 읽지 않도록 제한해야 한다

- **대상:** `practitioner-evidence.md:7–13`, `README.md` Finster 행과 효율성 해석.
- **현재 표현:** “구현+후속 변경의 평균 비용/회”, “비용은 실행 중 보고된 API 비용”. 숫자는 맞지만 비용 수집기의 구체적인 누락 가능성이 드러나지 않는다.
- **원문 근거:** 보관한 `originals/practitioner/B3-run_refactor_experiment.py:369–381`의 `dispatch`는 재시도할 때 앞선 응답을 `last`로 덮어쓰고 마지막 응답만 반환한다. `620–624`의 `_cost`는 이 마지막 응답들만 합산하고 `retries`도 남기지 않는다. `343–351`에서는 timeout 때 비용이 `None`이고, `_cost`는 이를 0으로 바꾼다. `798–807`은 `run_cell`의 4단계가 끝난 뒤에만 JSONL을 기록한다. 저자의 결과 문서 `originals/practitioner/B3-finster-05-final-results.md:364–368`도 환경 회수로 진행 중 실행이 반복 종료되었다고 명시한다.
- **영향:** 보관 JSONL의 완료 cell 비용과 캠페인에 실제 소비된 전체 비용은 다를 수 있다. 앞선 실패가 과금되었는지, 방식별 누락액이 얼마인지 이 자료로는 알 수 없다. 누락 때문에 순위가 바뀌었다고 주장할 근거도 없다. “실행 로그 재현성 미확인”이라는 일반 문구보다 이 구체적인 비용 회계 한계가 사용자의 총비용 질문에 중요하다.
- **수정안:** 열 제목을 “완료 cell에 기록된 API 비용 평균(초기 구현+변경 3회)”으로 바꾸고, “보관한 수집기는 재시도 전 응답의 비용을 누적하지 않으며 중단 cell 비용도 결과 파일에서 빠질 수 있다. 따라서 이 값은 중단·재시도를 포함한 총소비비용으로 확인되지 않았다”를 추가한다. README 비용 행에는 “완료 기록 기준”이라고 짧게 붙인다.
- **독립 계산:** 각 핵심 방식은 4과제×6회=24 cell, cell당 4행이었다. 평균은 continuous-single `$0.9934522083`, tdd-refactor `$1.5886820042`, one-shot-single `$2.0888303938`로 주보고서와 일치했다. 완료 행의 `is_error`는 모두 false지만, 앞선 재시도 기록이 집계 구조에서 사라지므로 이 사실이 누락액 0의 증거는 아니다. 보관 스크립트가 당시 실행본과 완전히 같았다는 검증은 하지 않았다.

### P2-2. Finster에도 ‘TDD 지시’와 ‘엄격 TDD 실행 준수’를 구분해야 한다

- **대상:** `practitioner-evidence.md:9–13`, `README.md` Finster 행 및 “직접 비교에 가까운 공개 실험” 분류.
- **현재 표현:** “동작별 TDD” 대 “동작별 구현 → 테스트 → 정리”가 실제 실행 순서를 확인한 비교처럼 읽힌다. Dan Luu 행에는 지시와 충실한 실행의 차이가 명시되지만 Finster에는 없다.
- **원문 근거:** `originals/practitioner/B3-run_refactor_experiment.py:148–171`은 test-first/test-after 프롬프트를 설정한다. `634–637`에서는 단일 에이전트의 구현·테스트를 한 dispatch 안에서 수행한다. `406–426`의 `refactor_process`는 커밋 메시지와 refactor 커밋의 테스트 변경량을 센다. JSONL의 process 필드도 `granularity`, `first_green`, `test_loc_churn_in_refactor`, `commits`뿐이며 의미 있는 RED 실행과 구현 선행 관계를 기록하지 않는다. 결과 문서 `157–168`의 “0 violations”는 리팩터링 중 테스트 동작을 바꾸지 않는 규칙에 관한 것이다.
- **영향:** 이 비교는 서로 다른 절차를 지시한 비용 사례로 유효하지만, 엄격한 RED–GREEN 순서만의 준수 효과를 입증하지 않는다. 반대 방향의 실험에만 준수 한계를 붙이면 증거 평가 기준이 비대칭이 된다.
- **수정안:** 표를 “동작별 TDD 지시”, “동작별 구현 후 테스트 지시”로 표기하고, “프롬프트와 최종 산출물 집계는 확인했으나 동작별 RED 실행·순서 준수는 보관 자료로 검증하지 못했다. 0 violations는 refactor 중 테스트 변경 검사다”를 덧붙인다. 기존 비용 사례 자체를 삭제하거나 무효 처리할 필요는 없다.

### P2-3. Superpowers #2275의 작성자 보고를 독립 실행 artifact로 승격하지 않아야 한다

- **대상:** `working/agent-projects.md:57,77`, `data/agent-projects/pr-evidence.json`의 `visible_test_first_with_failure_execution`, README의 Superpowers 사례 요약.
- **현재 표현:** “제한된 test-first + 실패 실행”, “이 기록은 명명된 feasibility/probe 사이클만 입증”이라고 한다. 주보고서에는 “공개 보고 artifact”라는 단서가 있으나 구조화 분류와 ‘입증’은 실제 실행 로그까지 확인한 것으로 읽힐 수 있다.
- **원문 근거:** `originals/projects-agent/superpowers-pr-2275-task1-report@49bc293.md:11`은 큰 실행 artifact가 Git에서 무시되며 로컬·원격에만 남고 source와 report만 커밋되었다고 명시한다. `86–88`은 `red-unimplemented.txt`, `red-outcomes.txt`라는 파일명과 KeyError 결과를 요약하는 작성자 보고다. 검토 자료에는 이 두 원시 로그가 없고 중간 CI도 0건이다. 같은 상세 보고서는 #1720의 RED–GREEN 요약을 작성자 보고로 제한하고 있어 등급의 일관성이 필요하다.
- **영향:** 공개 테스트 커밋 선행이라는 관찰은 유지할 수 있다. 그러나 당시 의미 있는 실패 실행을 확인한 정도는 작성자 보고 수준이다. 특히 `assert_outcomes({})`의 KeyError는 보고 schema 누락에 관한 실패여서, 이것만으로 실제 recorder 동작의 실패부터 검증했다고 확대할 수 없다.
- **수정안:** “일부 probe 테스트 커밋 선행, 실패 실행은 작성자 보고(원시 로그·중간 CI 미확보)”로 분류하고, “입증”을 “작성자 보고가 뒷받침한다”로 낮춘다. 구조화 데이터에도 `test_first_commit_visible: true`, `red_execution_evidence: author_report`처럼 두 축을 분리하거나 별도 분류명을 사용한다. #2275가 TDD를 하지 않았다는 결론은 내리지 않는다.

## 여섯 검토 축에서 추가 실질 지적을 하지 않은 이유

| 검토 축 | 확인 결과와 범위 |
|---|---|
| 반대 근거 누락 | README와 11개 연구 카드는 TENET·ClassEval-TDD·TGen 등 개선 결과, TDAD의 악화, 새 테스트 생성의 무효 결과를 함께 다룬다. Finster 표도 큰 일괄 테스트의 높은 mutation score를 숨기지 않는다. 보관 자료 내부에서 결론을 바꿀 정도의 반대 결과 누락은 확인하지 못했다. 문헌 검색 전체의 완전성을 새로 검증한 것은 아니다. |
| 정책·관행·작성자 보고 | 전체 구조는 세 층을 구분한다. OpenHands의 “TDD tests”와 명시적 RED-first의 차이, SWE-agent 기본 프롬프트와 저장소 기여 규칙의 차이도 적절히 설명한다. 예외는 P2-3이다. |
| 사람 연구의 과잉일반화 | `human-studies.md`는 사람 연구를 배경 근거로 제한하고 비용 구조 외삽을 금지한다. Fucci 원문의 단일집단 상관 설계 설명과 Santos의 비유의 신뢰구간을 대조했으며 보고서의 해석은 이에 부합한다. |
| 수치·분모·비용·비유의성 | Finster 핵심 3방식 비용과 분모는 직접 재계산했다. TENET Table VI의 42.65→49.18과 토큰 표, TDAD 9,245/8,040/8,536의 다른 분모, Santos 본문 −7.06 및 CI −14.47~0.35를 원문과 대조했다. 비유의성을 동등성으로 해석하지 않는 경계는 명시돼 있다. 비용 범위의 남은 문제는 P2-1이다. |
| 순서와 독립성 | 구현 노출 연구의 어려운 의미 오류 선정 조건을 원문과 확인했다. 요구사항만 본 테스트 생성의 이점을 엄격 TDD 순서의 효과로 등치하지 않은 것은 타당하다. Finster 준수 문제는 P2-2이다. |
| 최신성과 대표성 | README는 72건을 독립 실험·채택률로 취급하지 않고 API 상한, squash, 같은 병합 커밋, 오래된 SWE-agent 사례, 현재 OpenHands 저장소의 Agent Canvas 범위를 공개한다. 다만 전체 최신 적격 PR을 독립적으로 재검색한 것은 아니므로 표본 선정의 완전성을 인증하지 않는다. |

## 실제 검증 범위와 미검증 범위

**읽은 보고서:** README, methodology, practitioner-evidence, human-studies, working/agent-studies, working/web-projects, working/agent-projects 및 Finster 재집계 스크립트·JSON, Dan 차트 추출 JSON. 에이전트 프로젝트 구조화 JSON의 분류 기준도 확인했다.

**핵심 원문 대조:** Finster 결과 문서·workflow matrix 및 refactor harness의 관련 함수 정적 열람, 공개 JSONL 672행의 핵심 3방식 재계산, Superpowers #2275의 공개 Task 1 보고서, TENET·TDAD·coding-before-testing PDF 추출 텍스트의 관련 표·방법, Fucci·Santos 원문 추출 텍스트의 설계·주요 수치. 정책 원문은 OpenHands AGENTS와 Rails·Next.js 테스트 가이드의 관련 부분을 표적 확인했다.

**하지 않은 검증:** 11개 논문의 모든 표·부록 전수 재계산, 5개 사람 연구 전체 수치의 전수 대조, 72개 PR의 전체 diff·커밋 그래프·CI 재확인, 출처 최신성의 새 웹 검색, 공개되어 있지 않은 실행 로그·청구 비용 확인, 논문/프로젝트 코드 실행, 논문 결과의 독립 재현. 그러므로 “모든 원문이 완전히 검증됐다”는 인증으로 사용할 수 없다.

`originals/README.md`, `originals/manifest.json`, `review.md`는 다른 작업에서 작성 중인 것으로 전달받아 존재 여부를 결함으로 평가하지 않았다. 위 P2를 수정하면 현재 조건부 결론의 신뢰 범위가 더 명확해지며, 추가 실험 없이 조사 결과를 전달할 수 있다.

## 수정 후 재검토 — 3건 해결

같은 날 보고서 작성자가 수정한 파일을 다시 읽어 다음을 확인했다. 최초 지적의 원문과 수치는 위에 보존한다.

| 지적 | 재확인한 수정 | 상태 |
|---|---|---|
| P2-1 비용 회계 | README의 Finster 행이 완료 cell 기록 비용과 중단·재시도 누락 가능성을 명시한다. `practitioner-evidence.md` 표 제목은 “완료 cell의 기록 API 비용 평균(구현+변경 3회)”이며 본문은 누락 메커니즘과 전체 지출로 읽을 수 없음을 설명한다. | 해결 |
| P2-2 실행 준수 | README와 상세 표가 세 방식을 모두 “지시”로 표기하고, 의도한 RED 실행 준수는 확인되지 않았다고 명시한다. | 해결 |
| P2-3 자기보고 등급 | README, `working/agent-projects.md`, `data/agent-projects/pr-evidence.json`이 테스트 커밋 선행과 실패 실행의 작성자 보고를 분리한다. JSON 분류는 `test_commits_first_failure_author_report`이며 evidence에서도 실행을 독립 검증하지 않았다고 명시한다. 원시 artifact가 Git-ignored라는 한계도 포함됐다. | 해결 |

재검토 중 별도 표본 검토에서 변경된 Next.js 표도 문서·manifest 사이 동기화를 확인했다. #98504는 성능 개선이라는 제외 사유가 기록되고 #97988로 교체됐다. JSON을 세어 웹 전체 45건은 same-commit 37건, 관련 테스트 변경 없음 7건, 구현 커밋 후 테스트 1건이며 Next.js는 각각 7·1·1건이다. README·상세 표가 이에 일치한다. 이는 변경된 분류의 문서 정합성 검사이며 새 PR 전체 diff를 독립 검토한 것은 아니다.

또한 Superpowers 정책은 main에서 확인했지만 최근 일부 PR은 dev·기능 브랜치에 병합됐다는 범위 제한이 README와 상세 문서에 추가됐음을 확인했다. 이 재검토에서 새 벤치마크나 원본 코드 실행은 수행하지 않았다. 현재 조건부 결론을 전달하는 데 남은 P1/P2는 확인하지 못했다.
