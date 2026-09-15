# TDD 선택형 SDLC 설계·검증 기록

2026-09-12. 기준 commit: `e6b16db8278f6a8d81397ca0a0d26f3c7dba8bb9`.
대상은 선택형 문서와 팀 패키지 `intent-sdlc-skills-optional` 0.1.1이다.

**테스트 작성 순서를 작업별로 선택하고, 요구의 근거·회귀 보호·실제 실행과 사람의 결정을 유지하는
SDLC를 문서에 반영했다.** [전체 설계](../../decisions/tdd-optional-sdlc.md)는 조사 근거와 북극성 연결,
의도부터 운영까지의 인계, 선택·탐색·검토·전략 변경의 판단을 설명한다.
제품에서 사용할 정본은 [검증 방식 가이드](../../../tdd-optional/project/docs/TESTING-STRATEGY.md)다.

## 설계와 반영

- 현재 연구의 주보고서·방법론·에이전트 11건/사람 5건 카드·실무 실험·프로젝트별 정책과 공개 이력·
  비판 검토를 읽었다. 플레이북의 관련 원문과 주석을 대조했다. 추가 웹 검색이나 비교 실험은 하지 않았다.
- A5 원문의 비교 조건을 다시 읽고 ‘구현 뒤 별도 대화에서 시험 생성은 직접 검증되지 않았다’는
  카드의 표현을 정정했다. 같은 대화와 요구사항만 제공하는 새 대화는 직접 비교했으며, 그 결과를
  전체 제품 개발이나 최종 리뷰 효과로 확대하지 않는다. [정정 기록](../../research/tdd-vs-test-after/review.md)
- PROJECT-POLICY·CLAUDE·PROCESS·REVIEW·plan·작성 스킬을 가이드에 연결했다. 조건별 상세 기준을
  각 문서에 반복하지 않고, 이번 작업의 방식·이유·기대 출처·검증 순서를 plan에 남기게 했다.
- [기존 시험 활용 리팩터링](../../../tdd-optional/project/examples/skills/plan/examples/refactor-existing-tests.md)과
  [폐기 가능한 UI 탐색](../../../tdd-optional/project/examples/skills/plan/examples/disposable-ui-exploration.md)을 추가했다.
  두 문서는 계획 예시다. 탐색으로 배운 것과 제품 완료의 증거를 구분하며, 새 시험·가짜 RED·출시 절차를 일괄 요구하지 않는다.
- feedback·두 verifier는 독립 기대를 먼저 파악하고 현재 구현·시험·실행을 대조한다. 새 문맥이라는
  사실만으로 정답을 보장하지 않는다. 구현 비노출 시험 생성과 실제 구현을 읽는 최종 리뷰를 구분했다.
- 북극성이 버그 수정에 제시한 test-first와 수정 중 시험 동결은 **사용자가 요청한 선택 정책으로
  조정한 부분**이다. 그 절차와 문자적으로 같거나 효과가 동등하다고 주장하지 않는다. 이미 채택된
  프로젝트의 실제 보호 통제와 사람 권한은 유지한다.

## 확인 결과

| 확인 | 관찰한 결과 | 근거와 범위 |
|---|---|---|
| 기존 전체 회귀 | `make check` 종료 코드 0. Python 102건 중 101 통과·1 건너뜀, 훅 28 통과, eval shell 8 통과, managed settings 계약 통과 | [전체 출력](optional-sdlc-checks.log). 제품 사본의 링크·격리 및 기존 도구의 결정적 검사 포함 |
| native manifest | 루트 marketplace, 선택형 marketplace/plugin 3건 strict 검사 통과 | [명령·출력](optional-sdlc-package-checks.json). 실제 설치나 모델 실행은 아님 |
| OpenCode 전달 | feedback·ux-copy·작성 예시 patch 각각 임시 사본에서 dry-run과 실제 적용: 6건 통과 | 같은 JSON. 원본 SKILL이나 사용자 설치를 patch하지 않음 |
| YAML·검증 기준 | 변경 관련 SKILL/verifier 5개 frontmatter Ruby YAML 파싱 통과. 두 verifier의 Review criteria 동일 | 같은 JSON. Claude/OpenCode의 자연어 발견·권한 집행 증거는 아님 |
| 기본형·공통 양식 | `tdd-first/`의 추적 파일 diff와 미추적 추가 없음. 선택형 intent/spec 양식은 기준 commit에서 변경 없고 기본형과 byte 일치 | 같은 JSON. 테스트 방식 변경을 기본형으로 전파하지 않음 |
| 독립 의미 검토 | 7개 시나리오의 핵심 판단 일치. 최초 P3 2건은 수정·재검토 완료, 검토 범위의 미해결 P1/P2/P3 없음 | [독립 보고서](optional-sdlc-independent-review.md). 연구·북극성·정책·스킬·양식의 문서 검토 |
| 최종 링크·공백 | 변경·추가 Markdown 31개, 로컬 링크 225개와 그중 fragment 24개 통과. 최종 공백 검사 결과도 같은 기록에 보존 | [파일 검증](optional-sdlc-artifact-checks.json). 온라인 URL의 현재 상태는 재조회하지 않음 |

검토의 P3는 탐색 계획에도 제품 spec/Proof가 고정된 것처럼 보이던 양식·참조 문구와,
플레이북의 리뷰 기준·사람 승인 문단을 묶었던 링크였다. 각각 적용 범위와 원문 연결을 명확히 했다.
기존 분리판의 실제 함수 개발 3건은 [이전 검증](README.md)의 역사적 근거이며 이번 개정판의 실행 결과로 승계하지 않는다.

중요한 근거·북극성 해석·최종 독립 검토에는 `gpt-6-astra/high`, 구체 작성 스킬·예시 보완에는
`gpt-5.6-sol/high`를 사용했다. 작성 파일 소유 범위를 나눴고 최종 검토자는 자신의 보고서만 편집했다.

## 확인하지 않은 범위

이번 작업은 문서와 배포 메타데이터 설계다. 새 리팩터링/UI 예시를 제품에서 실행하거나, 브라우저로
동작·접근성을 확인하거나, 방식별 품질·시간·비용을 비교하지 않았다. Claude/OpenCode 새 설치,
자연어 스킬 선택·실제 위임·대기·권한의 런타임 집행, 유료 모델 평가는 수행하지 않았다.
정적 검사와 별도 에이전트의 문서 검토는 그 증거를 대신하지 않는다.

작성 담당자가 시도한 skill-creator `quick_validate.py`는 호스트에 PyYAML이 없어 실행되지 않았다.
의존성을 설치하거나 Claude 메타데이터를 바꾸지 않고 Ruby YAML 파싱과 실제 파일 연결을 확인했다.
이는 원래 검사기의 전체 규칙 통과를 의미하지 않는다.

공개 연구는 조건부 선택의 근거다. 실제 TDD 사용률·어떤 방식의 보편 우월성·전체 비용 절감률은
확정하지 않는다. 새 승인 단계·상태 판정기·의무 측정 장부·자동 설치를 추가하지 않았다.
