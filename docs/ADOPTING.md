# 템플릿 채택과 팀이 정할 내용

유일한 현행 템플릿은 [TDD 선택형](../tdd-optional/README.md)이다.
`tdd-optional/project/`의 내용을 별도 제품 저장소 루트로 복사한다. 그 안의 `PROJECT-POLICY.md`를 실제
제품·팀 기준으로 채운다. 배포판 폴더나 설치한 스킬 자체가 조직의 승인·정책을 대신하지 않는다.

## 채택하는 사람이 채울 사항

| 항목 | 기록할 것 |
|---|---|
| 프로젝트 맥락 | 제품 이름·사용자·범위, 민감 데이터, 실제 외부 전송과 의존성 |
| 역할·수락 | 제품 책임자, 계획·검토·통합·운영 결정자, 대상 SHA와 결정 근거를 보관할 위치 |
| 검증 | 실제 빌드·테스트·린트·실행 명령과 성공 기준. 없는 명령은 미정으로 남긴다. |
| 개발 방식 | 작업별 TDD·구현 후 테스트·기존 테스트 활용·혼합의 선택과 이유 |
| 정책 | [policies](../policies/README.md)의 예제를 참고해 보안·규정·브랜드·UX를 실제 기준으로 채운다. |
| Git·공개 | 제품 docs의 GitHub Flow·PR 범위·공개 제어. 배포·공개 결정자와 필요한 실제 통제 |
| 선택 도구 | Claude Code 또는 Codex의 팀 스킬·작성 예시·검증자, 실제 모델과 권한·설치 범위 |

문서 양식은 `intent→spec→plan`과 개정의 연결을 제공한다. 선택형은 TDD 미사용만으로 별도 예외 승인을
요구하지 않지만, 합의된 계약·독립 기대·회귀 보호·실행 증거를 유지한다. 팀이 이미 정한 사람 승인과
운영 권한을 무시하는 선택지는 아니다.

## 제작 예제와 제품 설정의 차이

루트 `.claude/hooks/`, `org/managed-settings.example.json`, `ops/`, `scripts/`, `evals/`는 제작·검증
예제다. 현재 제품 사용판은 이 도구를 자동 설치하지 않는다. 조직이 채택할 때 보호 경로·시크릿 규칙·
formatter·테스트 보호·배포 gate·CI 명령을 실제 환경에 맞추고 동작을 확인한다.
스킬은 권고이고, 훅/CI의 결정적 통제와 사람의 병합 권한은 별개다. 값이나 담당자를 템플릿이 발명하지 않는다.

[팀 패키지](../tdd-optional/org-skills/README.md)에서 [Claude Code](../tdd-optional/org-skills/claude/README.md)와
[Codex](../tdd-optional/org-skills/codex/README.md)의 설치·갱신 안내를 제공한다. 패키지의 LICENSE·PROVENANCE·동반 자료와
검증자를 함께 보존한다. 폐기한 기본형이나 사용자 전역 설치와 충돌하는지 실제 로드 출처를 확인하고,
소스 발견·설정 파싱·실제 모델 실행을 구분한다.

[분리 전 상세 제작 예제 표](https://github.com/bifrost17/ai-native-sdlc-sample/blob/13376e8049c5650c0fe3a8a258a6595f8d3ada8f/docs/ADOPTING.md)는
당시 구성과 레슨별 역할을 기록한다. 옛 경로를 현행 제품의 필수 파일로 오해하지 않는다.
[책임 경계](BOUNDARY.md) · [현재 구조](decisions/single-template.md)
