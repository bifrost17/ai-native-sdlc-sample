# 선택형 OpenCode 실험 전 직접 리뷰

2026-09-12. 검토한 소스 `4f7d1b0f5d8dc8cefa6aea7f9c57d8251c6bef76`, 선택형 팀 패키지 0.1.1.
작성·판단: Codex root. 독립 보조 검토: Astra/ultra. 모델 개발 실험 전에 수행했다.

## 판단

선택형 템플릿의 정책·양식·실행 스킬·두 검증자·설치 연결에서 수정이 필요한 확정 결함은 찾지 못했다.
이는 문서·배포 경로 리뷰 결과이며 실제 에이전트의 방법 선택·적용·검토 성공은 아직 증명하지 않는다.

- `project/PROJECT-POLICY.md` 42–46행과 `docs/TESTING-STRATEGY.md`는 방법 선택·독립 기대·
  동작별 검증·탐색의 편입 경계를 구별한다. non-TDD 선택에 새 승인을 요구하지 않는다.
- `templates/plan.md`와 계획 작성 스킬은 선택 이유·실제 파일·순서·PR·검증을 연결한다.
  F01의 구현 후 테스트, W01의 혼합, 기존 시험 재사용과 폐기 가능한 탐색 예시는 선택 규칙과 맞는다.
  B01의 선행 시험·보호 단계는 그 합성 입력의 명시 조건이며 모든 결함에 확대하지 않는다.
- `org-skills/skills/tdd/SKILL.md`의 자동 적용은 TDD를 선택한 범위다. feedback은 비TDD 리뷰
  수정을 선택한 방식으로 연결하고, 두 verifier는 non-TDD 자체가 아닌 계약·증거·회귀 부족을 평가한다.
- spec/plan 선행 현재화·관련 구현과 같은 커밋·사람 수락·GitHub Flow·공개 제어를 유지한다.
  방법 변경은 기술적 선택이며 계약/권한 변경과 구별한다. 시험 정정에 대한 사람 판단은 기존 정책이다.
- 북극성의 일반 피드백 루프와 새 문맥 검토를 유지하며, 버그의 test-first·시험 동결 처방을 조정한
  팀 정책임을 명시한다. 과거 판의 TDD 성공이나 문서 검토를 선택형의 실행 성공으로 승계하지 않는다.

## 실험 기준에서 발견한 문제

선택형 제품 결함과 별개의 **실험 평가 기준 충돌**을 확인했다.

1. 기존 `docs/experiments/PERSONA.md:63–64`는 결함마다 수정 전 재현 시험 실패를 확인하도록 했다.
   선택한 판과 전략에 따라 평가하도록 공통 현행 페르소나를 고친다. 과거 소스는 Git에 보존한다.
2. `datasets/v6/F04-release-json/human.json`의 `process_observations[1]`은 모든 새 계약에 RED를
   요구하며, v6 README는 과거 사용판을 고정한다. v6 원문은 수정하지 않는다. 0029는 같은 업무
   사실·fixture·oracle을 재사용하되 현재 선택형 출발판과 방식별 평가 기준을 별도 프로토콜에 명시한다.

또한 이미 설치한 기본형 패키지나 전역 스킬이 실험에 섞이는지 실제 발견 경로·본문을 확인해야 한다.
이는 현재 선택형의 확인된 결함이 아니라 실험의 노출 조건이다. 두 판을 함께 로드한 결과를 선택형
독립 실행으로 기록하지 않는다.

## 직접 확인한 범위

- 기존 `tests/test_template_editions.py` **3개 통과**: 제품 복사본 내부 문서 연결·격리,
  marketplace의 패키지 연결, 두 판의 intent/spec 양식 일치.
- 임시 제품 복사본에 선택형 팀 폴더 전체와 작성 예시를 배치했다. feedback·ux-copy·authoring의
  patch dry-run/실제 적용 **6개 통과**. 두 verifier의 Review criteria 본문 동일.
- 로컬 Claude CLI help에서 문서의 marketplace/install/update `--scope project` 옵션을 확인했다.
  실제 플러그인 설치나 사용자 전역 설정 변경은 하지 않았다.
- source 정책·가이드·작성 스킬·예시·feedback/TDD·검증자·북극성 관련 원문을 직접 대조했다.
  연구 논문의 효과 재평가, 제품 구현, 자연 호출·권한 집행·품질 비교는 이번 사전 리뷰 범위 밖이다.

보조 리뷰·복사 검사 코드·결과는
`/Users/jake/Projects/ai-native-sdlc-experiment-private/0029-optional-opencode/`에 보존한다.
이 결과를 먼저 보고한 뒤 [0029 프로토콜](../../experiments/0029-optional-opencode.md)로 실행한다.
