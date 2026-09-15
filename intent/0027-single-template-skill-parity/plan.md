# Plan — 단일 템플릿과 스킬 전달 동등성

Status: draft
Upstream: [spec](spec.md), [intent](intent.md), 현재 변경. 기준 `b9af49a`.

현재 인계: T01–T04 완료. 구현 커밋 `46908f4`를 깨끗한 로컬 main에 fast-forward했고
동일 Git 판·기본형 삭제·0.1.8을 확인했다. 이 후속 기록은 실제 통합 결과를 담는다.
중요한 미해결 발견은 없다. 검증자는 실제 모델 행동을 이번 결과로 판정하지 않았다.
브랜치 `codex/single-template-skill-parity`. 실제 근거는 [실행 기록](execution/README.md)에 있다.
기존 미추적 `docs/research/003-execution-plan-audit/`, `docs/research/plan-skill-design/`는 범위 밖이다.

## Files that change
| 경로 | 구현 | 설계 |
|---|---|---|
| tdd-first/ | 추적 배포 소스 삭제 | SP01 |
| README, CLAUDE, .claude-plugin, .claude/skills, docs의 활성 안내·역사 색인, policies의 README·양식 안내, team-harness/README | 단일 정본·설치 시작점·폐기 판 경계 | SP01 |
| tdd-optional/의 설치 안내·카탈로그·어댑터 | 공통 16개 스킬의 도구별 전달과 0.1.8 | SP02/03 |
| scripts, evals, tests, .github | 기본 실행/허용 판을 선택형으로 전환하고 관련 회귀 확인 | SP01/03 |
| intent/0027-single-template-skill-parity/ | 설계·실제 검증·검토·인계 기록 | 전체 |

## Order of work
- T01 (root, SP01): 기본형 삭제, 활성 문서·루트 카탈로그·작성 라우터 정리. Done: AC01의 채택 경로가 하나이고 역사 기록과 구분된다.
- T02 (worker, SP01/03): scripts/evals/tests/.github의 실행 경로와 기존 시험 수정. 기본값 선택형, 폐기 판 거부를 시험한다. T01과 병렬. Done: 관련 시험과 `make check`가 삭제된 파일을 요구하지 않으며 기존 검증을 유지한다.
- T03 (worker, SP02/03): tdd-optional 내부의 Claude 설치 절차와 Codex 전달을 비교·보완하고 0.1.8로 맞춘다. 전체 폴더·명시 호출·업데이트·확인 지침을 제공한다. T01/02와 파일 소유가 달라 병렬. Done: AC02를 임시 제품 복사본에서 확인하고 결과를 root에 넘긴다.
  실제 Codex `pr-loop` 입력·명령 선실행 변환 누락을 발견해 네 번째 patch로 보완했다.
  공유 작업·보호·종료 규칙은 그대로다. 두 도구 설치·자료 대조와 기존 OpenCode patch도 확인했다.
- T04 (root + fresh reviewer, 전체): 통합 diff·전체 검사·패키지/설치 확인 후 Astra/high의 새 문맥 검토를 받는다. 중요한 발견만 보완해 관련 시험을 다시 확인한다. 완료 문서와 관련 변경을 커밋하고 깨끗한 로컬 main에 안전한 fast-forward로 반영한다. 원격 push와 전역 설치는 하지 않는다.

이번 범위는 한 번의 템플릿 배포 변경이다. 폴더 삭제·실행 경로·카탈로그를 따로 인도하면 중간판이 깨지므로
동일 구현 커밋에 묶는다. 작업자는 결과를 병렬로 준비하며 통합 책임은 root가 갖는다.

## Risks
폐기 경로가 시험·평가 기본값에 남는 것이 가장 큰 위험이다. 단순 검색 일치 건을 전부 바꾸면
역사 증거를 훼손하므로 활성 실행과 당시 기록을 구분한다. 도구별 설정은 동일 바이트가 아니라
같은 스킬 의미와 자료를 전달하는 것으로 판단한다. 새로운 installer 프로그램이나 SDLC 승인 검사는 만들지 않는다.

## Proof
`make check`, 폐기 판 거부·기본 평가 경로 시험, root/단일판 manifest strict,
임시 제품의 Claude 작성 폴더와 Codex 패치 적용·16개 자산·동반 검토 기준 비교,
기존 OpenCode 패치 회귀, 독립 최종 리뷰. 원본 출력은 execution/에 보존한다.
정적 설치 확인을 새 모델 호출·전체 개발 통과로 확대하지 않는다.
