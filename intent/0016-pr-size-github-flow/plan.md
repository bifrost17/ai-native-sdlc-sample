# Plan: PR 크기 조사와 GitHub Flow 정책을 실험으로 검증
Upstream: spec.md@77a91de. Status: draft.
오너의 조사·반영·실험 지시에 따라 진행한다. 조사/정책 설계는 구현 전에 독립 검토하며, 실제 조직 승인과 실험 HUMAN의 수락을 구분한다.
## Files that change
- 제작 docs/research/pr-size/README.md(new), docs/research/README.md: 일차 근거·사례·반례·한계와 채택 이유.
- 제작 docs/PR-SIZE.md, docs/GIT-WORKFLOW.md(new): 사용 템플릿에 배포하는 정책 원문. 같은 두 파일을 사용판 docs/에 동일하게 둔다.
- 사용 후보 codex/use-template-0016: CLAUDE.md, docs/PROCESS.md, PROJECT-POLICY.md, REVIEW.md, README.md, templates/plan.md와 새 정책 두 문서. 선택 예시 스킬은 기존 양식/단계 지침과 충돌하지 않는지 확인하며 불필요한 변경은 하지 않는다.
- 제작 docs/experiments/datasets/v2/{manifest.json,F02/public.json,F02/human.json,F02/requests.json}(new): 이전 CLI baseline을 고정 참조하는 새 합성 개발건. 기존 v1은 불변.
- 제작 docs/experiments/README.md, docs/experiments/0016-flow-pilot.md(new): PR 단위 실험 방식·결과·판정. root README.md와 docs/verification/{north-star-playbook.html,README.md,INDEX.md,CHAPTERS.md}: 사용 후보·조사·실행 색인과 해당 주석의 한정된 근거.
- intent/0016-pr-size-github-flow의 사슬 문서. 실제 제품 코드·대화·PR/실행 근거는 별도 실험 복제본/브랜치에만 보존한다.
- 후속 요청: 사용 후보 codex/use-template-0016-r2에서 CLAUDE.md, docs/PROCESS.md, REVIEW.md, docs/GIT-WORKFLOW.md의 '같은 변경'을 '해당 구현과 같은 커밋'으로 명확히 한다. 설계 개정과 수락 판의 Upstream 연결을 짧게 안내한다. 최초 후보와 F02 전체 실행은 고정 보존하고 같은 결과 문서에 부분 실험을 구분해 남긴다.
## Order of work
1. 플레이북 plan/parallel/review와 기존 평가를 읽고, 연구·공식 운영·공개 PR 사례를 교차 확인한다. 설계 검토로 단계 수락/PR merge와 Upstream SHA의 충돌을 해소한다.
2. 보고서와 작은 정책 두 문서를 쓴 뒤 진입점과 수락 규칙을 연결한다. 원래 기준선은 고정하고 사용 후보를 새 커밋으로 보존한다. 코드/형식 집행 장치는 추가하지 않는다.
3. F02 두 업무 결과의 문제를 새 데이터로 고정한다. 별도 얕은 사용 복제본에서 제작 자료·HUMAN 비공개 사실을 배제하고 Sonnet·low를 같은 세션으로 이어간다. HUMAN은 실제 응답/산출물에 따라 사실 공개·리뷰·수정을 결정한다.
4. 실험 복제본의 main을 기존 GitHub 저장소의 전용 실험 통합 브랜치에 대응시킨다. 실제 Draft PR을 그 대상으로 열고, 구현/시험/설명을 합리적으로 묶은 둘 이상의 통합을 관측한다. 같은 파일을 공유하면 순차 실행하는 선택도 정상이다. 각 통합 후 기존/새 동작을 확인하고 마지막에는 새 디렉터리 인도와 두 번째 변경 되돌리기를 검증한다.
5. 중요한 편차는 피드백 후 수정·재확인한다. 실행·세션·입력·커밋·PR·비용·범위를 보존하고 전체 흐름 회귀를 판단한다. 변하지 않은 가이드 근거는 재사용하며 원문과 역사적 실패를 유지한 채 주석에 이번 범위만 추가한다.
6. 독립 verifier가 제작 make check, 변경/계획/링크/배포 정책 동일성, 실험 PR·합성 동작·참조 SHA와 인접 흐름을 확인한다. 결과를 기록하고 제작 main에 변경을 반영한다. 실험 제품을 제작 main에 통합하지 않는다.
7. 사용자 후속 요청으로 기존 cff4c2b의 계획·구현 동시 커밋을 대조하고, 후속 후보에서 구현 중 요구·설계 변경을 주는 부분 실험을 한다. 수정 spec의 수락 판과 코드·시험·plan의 같은 커밋, 기존 동작 회귀를 관측한다. 새 전체 프로세스 성공 표본으로 세지 않는다.
## Risks
작업마다 PR을 강제해 과도 분할, 문서 승인과 구현 머지를 혼동해 형식 증가, 파일 분리만으로 병렬성을 판단, 승인 커밋을 squash로 유실하는 회귀를 확인한다. 같은 계정의 GitHub 댓글/merge는 조직 권한 분리를 검증하지 못한다. 작은 CLI 실험은 대형 PR 성능이나 실제 배포 호환성 실험이 아니다.
## Proof
출처와 주장 대조, 사용판 진입점에서 두 정책을 읽을 수 있는지와 상충 문구 검사, 기존 v1 해시 보존, 실제 세션 도구/스킬/모델 기록, 둘 이상의 GitHub PR과 HUMAN 수락/merge 이력, 각 통합의 python3 -m unittest discover -s tests -v 및 독립 CLI 관측, 새 복제본 인도와 두 번째 기능 revert 대조. 제작 make check와 .claude/agents/verifier.md의 네 부분 보고를 남긴다. 실험 예산은 60분/12 HUMAN 턴을 기본으로 하며 독립 검증/기록은 별도다.
