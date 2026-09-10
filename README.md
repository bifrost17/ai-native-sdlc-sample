# 소프트웨어 개발 절차 템플릿

제품의 문제를 기록하고, 요구사항과 설계를 검토하고, 구현 계획과 검증 근거를 이어 가기 위한 시작점이다.
팀은 자기 제품의 정책·도구·실행 환경을 정한 뒤 이 구조를 사용한다.

## 시작하기

1. [프로젝트 정책](PROJECT-POLICY.md)에 역할, 기록 위치, 적용할 정책과 실제 검증 방법을 적는다.
   아직 정하지 못한 것은 미정으로 남기고 결정할 사람을 적는다.
   브랜치는 [GitHub Flow](docs/GIT-WORKFLOW.md), 변경 묶음은 [PR 크기 가이드](docs/PR-SIZE.md)를 따른다.
2. [개발 절차](docs/PROCESS.md)를 읽고 문제 하나를 [intent/](intent/README.md)에 기록한다.
3. 승인된 의도에서 요구·설계를, 승인된 요구·설계에서 구현 계획을 만든다.
   [문서 양식](templates/)을 사용하고 사람의 결정과 근거를 다음 단계로 넘긴다.
4. 구현한 결과를 실제 프로젝트의 방법으로 검증하고 [리뷰 지침](REVIEW.md)에 따라 검토한다.

## 들어 있는 것

| 경로 | 쓰임 |
|---|---|
| [CLAUDE.md](CLAUDE.md) | 에이전트가 따를 프로젝트 작업 원칙 |
| [docs/PROCESS.md](docs/PROCESS.md) | 역할, 단계별 인계, 승인과 검증 근거 |
| [docs/GIT-WORKFLOW.md](docs/GIT-WORKFLOW.md) | main·작업 브랜치·PR·단계 수락·통합과 정리 |
| [docs/PR-SIZE.md](docs/PR-SIZE.md) | 변경을 나누거나 함께 두는 유연한 판단 기준 |
| [PROJECT-POLICY.md](PROJECT-POLICY.md) | 팀과 프로젝트가 채울 정책·도구·책임자 |
| [templates/](templates/) | intent, spec, plan의 빈 양식 |
| [intent/](intent/README.md) | 앞으로 진행할 제품 변경의 기록 |
| [examples/](examples/README.md) | 팀이 선택해서 수정할 수 있는 작업 방식 예시 |

현재 tracker.py, requests.json, tests/에 작은 CLI와 시험 기준선이 있다. 별도 빌드·호스티드 CI는 없다.
이 파일들이 있다는 사실이나 문서를 읽었다는 사실을 실행·검증 완료로 보고하지 않는다.
팀의 스킬과 도구는 필요에 따라 선택할 수 있으며, 이 템플릿을 사용하기 위한 필수 구성은 아니다.

## 제품 시작과 작업 브랜치

템플릿의 판을 기록해 제품 저장소를 초기화하고 제품의 `main`을 통합 기준으로 삼는다.
이후 작업은 최신 제품 `main`에서 짧은 브랜치를 만들어 PR로 통합한다. 매 작업을 초기 템플릿
커밋에서 다시 시작하지 않는다. 큰 요구는 계획의 작업·의존성에 따라 여러 PR로 이어갈 수 있다.
이 템플릿을 배포하는 저장소의 브랜치와 채택한 제품의 브랜치는 서로 다른 역할이다.

템플릿의 출처와 라이선스는 [NOTICE](NOTICE)와 [LICENSE](LICENSE)에 있다.
