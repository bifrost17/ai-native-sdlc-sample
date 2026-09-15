# 보완 설계 대조 검토 — Sol

2026-09-14. `README.md`와 `analysis.md`의 이벤트, 입력, 두 TDD 판의 판별, 제공 adapter와
부분 평가 계획을 현재 파일에 대조했다. 이 기록은 앞선 범위 분석에 이어 설계 초안을 보조 검토한 결과이며,
새 문맥의 독립 최종 심사나 보완 절차의 실제 효력 검증이 아니다. 제품, 활성 지침, 설치와 `inputs/` 원문은
수정하지 않았다.

## 결론

검토한 범위에서 남은 중대한 설계 발견은 없다. 기존 `sdlc-feedback`/`sdlc-verifier` 안에 설계 인계
범위를 나누고 사소한 변경에는 새 독립 검토를 요구하지 않는 선택은 구현 가능하다. 설계만 검토할 때
없는 plan·diff·시험·배포 값을 요구하지 않는 입력 경계와 설계 준비·실제 AC 실행·사람 수락의 구분도
서로 맞는다.

기본형의 test-first/RED→GREEN 요구와 선택형의 작업별 검증 전략·독립 기대·coverage 판단은 구현
범위에 그대로 남는다. 기존 구현 완료 fresh verifier와 결과 대기 의무도 유지되며, 설계 PASS가 이를
대체하지 않는다. 설계와 구현이 섞이면 이름이 아니라 실제 변경과 완료 주장으로 범위를 정한다는 보완도
design-only 예외가 구현 검증으로 번지는 것을 막는다.

네 기본 호출과 필요할 때의 최대 두 보완 호출은 동일 원본의 현행/개선 대조, 작은 충분한 spec,
정당한 이월 합성 사례를 포함하므로 제한된 부분 평가로 실행 가능하다. 시간 초과와 미완료를 실패 없이
보존하고 시간 자체를 충분성 판정에 쓰지 않는 조건도 적절하다. 이 네 호출은 명시적 설계 검토 시험이며
자연 선택과 실제 구현 완료 호출을 검증하지 않는다고 현재 문서가 한정하므로, 자연 trigger의 실증까지
이 실험에 추가할 의무는 없다.

## 설치·동기화 대조

설계가 적은 동기화 경로는 실제 배포 구조와 맞는다. 양 판에는 Claude 정본과 OpenCode verifier 사본 및
feedback patch가 있고, 선택형에만 Codex verifier TOML과 feedback patch가 있다. 기본형 Codex adapter를
새로 만들거나 존재한다고 가정하지 않는 경계도 정확하다.

구현 시 `design-spec` 본문과 `design-depth.md`의 설치 사본도 확인해야 한다. OpenCode는 양 판의
`org-skills/opencode/patches/authoring-native.patch`, 선택형 Codex는
`org-skills/codex/patches/explicit-only.patch`를 거쳐 작성 스킬을 설치한다. 현재 patch는 주로 Claude 전용
frontmatter를 제거하므로 본문 보완만으로 반드시 수정될 파일은 아니지만, 문서가 예정한 “모든 제공 adapter의
적용·설치본 기준/해시 일치” 확인에 hunk 적용과 동반 reference 복사를 포함하면 된다. 별도 설계 변경은 필요 없다.

## 실제 확인 범위와 한계

- 두 판의 `sdlc-feedback`, Claude/OpenCode verifier, 선택형 Codex verifier와 관련 patch·설치 안내
- 두 판의 `project/docs/PROCESS.md`, `project/REVIEW.md`, `project/examples/skills/design-spec/`와
  `references/design-depth.md`
- `inputs/manifest.json`의 9개 보존 원본과 외부 `final-design-r1/files` 210파일 경로의 존재
- 북극성의 요구·설계 인계, 코드 전 설계 review, feedback loop와 작은 변경 비례 원칙
- root가 추가한 구현 완료 fresh 의무의 정적/adapter 확인, 혼합 범위 판별, 과거 리뷰 노출 한계

210파일 전체 의미는 재검토하지 않았다. 실험, 설치, patch 적용과 제품 실행도 수행하지 않았으므로 새
기준의 탐지율·자연 호출·설치 성공·패키지 검증 결과는 아직 확인되지 않았다.
