# 두 배포판 분리의 검증 기록

2026-09-12. [승인된 구조](../../decisions/template-variants.md)를 구현한 작업 트리를 검증했다.
제품 채택 단위는 각 `project/`의 내용, 팀 스킬은 같은 판의 선택 설치 패키지다.

## 무엇을 확인했는가

| 확인 | 결과와 근거 | 이 결과가 다루는 범위 |
|---|---|---|
| 기본형 제품 보존 | 출발판 `84a77b3`의 71개 파일 모두 byte 일치. [해시 기록](baseline.json) | 제품의 누락·추가·내용 변경 없음 |
| 기본형 핵심 스킬 보존 | TDD·feedback·Claude/OpenCode 검증자 4개 본문이 `13376e8`의 원본과 byte 일치 | 패키지 위치·버전·설치 안내 개정과 실행 규칙 보존을 구분 |
| 제작 도구·배포판 회귀 | `make check`: Python 102개 중 101개 통과·1개 건너뜀, 훅 28개·eval shell 8개·managed settings 검사 통과. [실행 로그](checks.log) | 독립 제품 사본의 문서 연결, 패키지 식별자, 판별 생성/채점 경로, 기존 결정적 통제 |
| 배포 메타데이터·OpenCode 전달 | manifest 5건, 두 판 × patch 3개 × dry-run/실제 적용 12건 통과. [명령·출력](package-checks.json) | native CLI의 manifest 검사와 임시 사본에 patch 적용 가능 |
| 작은 실제 개발 3건 | 기본형 TDD, 선택형 구현 후 테스트, 선택형 TDD 각각 최종 7개 시험 통과. [별도 최종 검증](evidence/verification.json) | 선택한 지침을 읽은 새 에이전트의 제한된 함수 변경 |
| 독립 구현 검토 | 선택형 평가의 namespace 오류 P2 1건 발견·수정·재검토. 검토 범위 내 미해결 P1/P2 없음. [보고서](independent-review.md) | 정책·양식·스킬·검증자의 정합성, 경로·평가 격리 |

판별 보존·변경 내역은 [TDD 기본형](tdd-first.md)과 [TDD 선택형](tdd-optional.md)에 있다.
기존 북극성 주석·사용 브랜치의 실행 성공을 선택형의 성공으로 승계하지 않는다.

staged diff의 공백 검사는 경고 3건으로 종료 코드 2였다. 두 patch의 빈 context 행과 기존 upstream
HTML 예시의 공백이며 원본·patch 구문을 보존했다. [경고와 원본 대조](whitespace-check.json)
조사 원문 사본의 줄 끝·공백도 별도 연구 커밋에서 그대로 보존했다.

## 작은 실제 작업의 구성과 근거 수준

세 개의 별도 임시 제품 저장소에 동일한 `subtotal` 코드·기존 시험 3개·할인 계산 SPEC을 넣었다.
새 Codex 하위 에이전트 3개가 해당 판의 제품 지침과 동봉 스킬을 직접 읽고 계획·구현·검증을 수행했다.
작은 구현은 `gpt-5.6-sol/medium`, 전체 구조의 독립 검토는 `gpt-6-astra/high`로 나눴다.
기본형 요청은 TDD를 별도로 지시하지 않았고, 선택형 두 요청은 각각 구현 후 테스트와 TDD를 명시했다.
이는 선택형의 두 경로가 허용되는지 보는 작업이며, 자율 선택률 측정은 아니다.

| 작업 | 계획·실행 기록 | 관찰 |
|---|---|---|
| 기본형 | [PLAN](evidence/first/PLAN.md), [실행 기록](evidence/first/evidence.md) | 정책에 따라 선행 시험·실패 확인·구현을 진행. 두 RED→GREEN 단계 기록 |
| 선택형 구현 후 테스트 | [PLAN](evidence/optional-after/PLAN.md), [실행 기록](evidence/optional-after/evidence.md) | 작은 함수 구현 뒤 시험 추가·검증. TDD 미선택에 별도 승인 요구 없음 |
| 선택형 TDD | [PLAN](evidence/optional-tdd/PLAN.md), [실행 기록](evidence/optional-tdd/evidence.md) | 선행 시험이 아직 없는 public 함수 import에서 실패하고 구현 뒤 통과하는 한 주기 기록 |

작업자가 작성한 과거 실행·편집 순서 기록과 이후의 독립 검증을 구분한다. 별도 에이전트가 세 최종
사본에서 21개 시험을 다시 실행하고, 구현과 다른 식인 `(total * (100 - percent) + 99) // 100`으로
각 707개 유효 입력·2개 오류 경계와 기존 소계·입력 불변성을 확인했다.
최종 기능은 일치했다. `optional-after`의 PLAN에는 초기/현재 diff 비교라는 표현이 있으나,
실제 보관 기록은 `/dev/null`과 미추적 파일의 대조다. 이 문서 정밀도 문제는 원문을 고치지 않고
[검증 기록의 findings](evidence/verification.json)에 남겼다.

`evidence/`에는 각 작업의 SPEC·PLAN·구현·시험·자체 실행 기록만 보관했다. 전체 제품·스킬 사본이나
Git 이력은 포함하지 않는다. 따라서 발췌 PLAN 안의 제품 문서 경로는 해당 작업 당시의 사본을 뜻한다.
초기 저장소에는 커밋이 없어 SHA 기반 전후 diff가 없으며, 자체 검토를 별도 검증자 호출로 계산하지 않는다.

## 확인하지 않은 것

- Claude/OpenCode에 새 판을 설치한 뒤 자연어로 스킬을 발견·호출하고 native 검증자에 위임하는 실행.
  manifest·patch 성공과 수동으로 본문을 읽은 Codex 실행은 이 증거를 대신하지 않는다.
- 사용자 전역 설치와의 런타임 충돌·실제 업데이트. 기존 전역 설정·설치·인증은 변경하지 않았다.
- 유료 Claude 생성·의미 채점: 이 환경에 `ANTHROPIC_API_KEY`가 없어 실행하지 않았다.
  fake CLI 회귀검사는 호출 계약을 검증하며 실제 모델의 정책 적용을 채점하지 않는다.
- Codex skill-creator의 `quick_validate.py`: 로컬 Python에 PyYAML이 없어 실행하지 못했다.
  Claude 고유 메타데이터를 그 검사기에 맞추기 위해 변경하지 않았다.
- 개발 방식의 생산성 우열·TDD 사용률·웹앱 전반의 품질. 세 작업은 통제된 비교 실험이 아니다.
  연구상의 조건과 불확실성은 [조사 보고서](../../research/tdd-vs-test-after/README.md)에 있다.

새 승인 단계·상태 판정기·자동 동기화 생성기는 추가하지 않았다. 공통 양식과 팀 정책을 바꾸면
두 판의 영향을 함께 검토하고, 방식별 차이는 각 판에서 명시적으로 유지한다.
