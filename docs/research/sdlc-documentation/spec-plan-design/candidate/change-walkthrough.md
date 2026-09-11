# 구현 중 발견을 문서에 반영하는 예

아래는 문서/커밋 설계 예시다. 제품 코드를 구현·시험·커밋했다는 실행 기록이 아니다.
각 시나리오는 기준 후보에서 독립적으로 시작하며 네 예시의 기본 계약을 실제로 변경하지 않는다.

## 경로 변경만 있는 경우
F01 실행 중 기존 저장소 관례가 tests/cli/test_owner.py라는 사실을 확인했다면:

```diff
--- plan.md (설명용 발췌)
+++ plan.md (관련 구현 커밋)
-| tests/test_owner.py (new) | 정확 비교·순서·미배정·기존/I/O 회귀 시험 | AC1–4 |
+| tests/cli/test_owner.py (new) | 기존 CLI 시험 배치 관례에 맞춰 AC1–4 추가 | AC1–4 |
```

Order의 경로와 Proof의 명령도 실제 발견 방식에 맞게 함께 고친다. 예를 들어 재귀 discover가
패키지 구성상 탐색하지 못한다면 기존 프로젝트의 실행 타깃을 확인해 기록한다. 이 변경은 정확 일치
계약을 바꾸지 않으므로 spec은 유지한다. 경로 이동과 plan 갱신을 같은 커밋에 포함한다.

## 중요한 설계 변경은 연결된 spec 문서도 수정
M01 구현 중 새 환경에서 SQLite 연결을 호출 사이에 공유하자는 제안이 나오면 단순 내부 선택이 아니다.
현재 architecture는 호출 단위 연결을 정하고 storage는 그 경계의 원자성을 설명한다. 먼저 근거·동시성
영향을 검토한다. 변경을 선택했다면 architecture의 연결 계약과 storage의 트랜잭션/실패 책임을 실제로
수정하고 plan의 파일·시험/Proof 영향도 같은 구현 커밋에서 반영한다. 이때 spec.md 정본 목록은 파일이
늘지 않으면 그대로여도 되지만 전체 spec 집합이 리뷰 대상이다. 논의 메모만 추가해서는 반영된 것이 아니다.

현재 후보는 이 변경을 선택하지 않았으므로 대안 코드/결과를 발명하지 않는다.

## 공개 제어의 정상 퇴역은 테스트 약화와 다르다
F03의 오너가 조건 충족 근거를 확인하고 cleanup을 요청한 경우:

```diff
--- tests/test_release_control.py (설명용 시험 목록)
+++ tests/test_release_control.py (cleanup 의도)
-test_off_rejects_new_commands  # 제어가 있는 판의 계약
+test_final_features_without_environment  # cleanup 판 AC7
```

설정 없는 최종 기능을 기대하는 시험의 RED를 먼저 관측한 뒤 제어를 제거한다. 정확 비교·집계·원순서·
읽기 전용·기존 명령 시험은 유지한다. 폐기한 OFF 기대의 이유와 최종 phase를 spec/plan/PR에 남긴다.
필요한 조건이 아직 미충족이면 이 전환을 수행하지 않는다.

## 실패를 고치려다 기대값을 바꾸려는 경우
F01의 HANA 시험이 hana 행을 반환해 실패하면 새 합의 없이 AC2를 바꾸지 않는다. 구현을 수정한다.
반대로 fixture의 오타가 독립 입력과 대조해 입증되면 시험 데이터를 바로잡고 이유를 기록한다.
실행 후 만든 시험을 test-first로 꾸미거나 모든 사례를 실패시키는 의식은 하지 않는다.

동시 문서 개정의 SHA 참조 방식은 [실행 지침](guidance/execution-blocks.md)의 Current change 규칙을 따른다.
