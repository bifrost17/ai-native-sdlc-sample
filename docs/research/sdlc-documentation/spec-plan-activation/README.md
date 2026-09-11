# spec·plan 활성화와 실제 개발 검증

0024의 허가 범위는 활성 양식·작성/팀 스킬 → 사용 템플릿 → 영구 설치 → 실제 제품 개발 실험의 순차 진행이다.
기존 후보와 재평가 기록은 보존하고, 설치·코드 실행을 하지 않았던 이전 설계 패키지의 범위를 바꾸지 않는다.

- [실행 계획](../../../../intent/0024-spec-plan-activation/plan.md)
- [활성화 독립 리뷰·사용판 조정](activation-review.md)
- [팀 스킬 반영](team-skill-notes.md), [구체적 예시 반영](examples-notes.md)
- [실험 설계](experiment-design.md), [고정 데이터 v6](../../../experiments/datasets/v6/README.md)

활성 양식·스킬 반영, 팀 플러그인 **0.1.5 영구 설치**, 실제 작은 제품의 개발·검토·로컬 통합을 수행했다.
현재 사용판은 `codex/use-template-0024-r2@d4d2153188743eb4f1bb30693b5c17afdaa0f999`다.
원 사용판 `fbc23c0`과 동일한 71파일이며 Git 정책 한 파일의 최초 작성/후속 개정 범위만 명확히 했다.
자동 로드 스킬·제작 연구는 사용 tree에 없고 자체 예시는 선택 설치용이다. 원 사용판과 실패 실행은 보존한다.

- [전체 결과·설치 환경·실패와 재시험·기록 refs](../../../experiments/0024-spec-plan-activation.md)
- [초기 활성화 verifier](stage1-verifier.md)
- [커밋 경계 독립 판단과 작은 정책 보완](commit-boundary-assessment.md)
- [마감 독립 검토](closing-review.md)

실제 제품은 별도 shallow clone에서 기존 CLI와 4행 합성 데이터로 시작했다. UI/서버 인증·DB 동시성·
실제 배포 환경을 구현한 것으로 확대 해석하지 않는다. 전체 공개 대화와 출력은 실험 기록 branch에 보존한다.
