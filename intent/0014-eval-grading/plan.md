# Plan: 평가 채점기의 의미·오류·실행 증거 연결
Upstream: spec.md@5307151. Status: draft.
프로젝트 오너가 우선순위 3의 구현을 지시해 draft 체인에서 진행한다. 승인 기록은 머지다.
## Files that change
- `evals/check.sh`, `tests/test_eval_regex.py` (new): grep 종료 코드와 반례.
- `evals/grade_assertions.py`, `tests/test_eval_assertions.py` (new): 증거 수집·격리 채점·결과 검증.
- `evals/record.py`, `tests/test_eval_semantic_runner.py` (new): 생성 trace 정규화·케이스 상태·실행 집계.
- `evals/run.sh`, `Makefile`, `CLAUDE.md`: 전체 채점 모드와 canonical 실행 명령·종료 문구.
- `evals/cases/01-intent-placeholder.json`, `02-no-self-accept.json`, `03-spec-carries-questions.json`, `04-org-policy-application.json`: 단계에 맞는 스킬 활용을 assertion에 추가하고 관련 정책 원문을 채점 입력에 연결한다. 04의 번역 가능한 인증 요구는 의미적으로 검사한다.
- `evals/SCHEMA.md`, `evals/README.md`, `docs/BOUNDARY.md`: 채점 형식과 결정론 전용 경로·전체 평가 경로의 차이를 설명한다.
- `docs/verification/north-star-playbook.html`, `README.md`, `docs/verification/{README,CHAPTERS,INDEX}.md`, `docs/verification/0014-eval-grading.md` (new), 필요한 정제 실행 증거: 범위·근거·핀·미검증 기록.
- 별도 `codex/use-template` 작업 폴더: 제작 자료를 제외한 실제 사용 템플릿과 선택적 자체 제작 스킬 예시. 제작 브랜치에는 사용 브랜치 위치·기준과 전체 프로세스/부분 실험 구분만 기록한다.
## Order of work
1. intent·spec·plan을 각각 커밋한다.
2. 정규식과 의미적 채점기를 서로 다른 파일에서 병렬 구현한다. 새 시험으로 실패를 먼저 확인한다.
3. 같은 생성 루프에 trace 기록·전체 채점·집계를 연결하고 기존 호출 호환을 검증한다.
4. 실제 Sonnet·low로 부분 채점 검증을 수행한다. 원래의 모델 출력은 손대지 않는다.
5. `make check`, 별도 verifier, 원문 보존·근거 링크 확인 후 문서를 정리한다.
6. 별도 사용 브랜치의 선택적 예시와 제작 자료 제거를 검토하고 기준 커밋을 남긴다. 전체 프로세스 실험을 실행했다고 주장하지 않는다.
## Risks
- 잘못된 정규식을 정상 불일치로 취급하면 금지 패턴 검사가 통과한다. 양쪽 kind와 읽기 오류를 시험한다.
- 생성 결과가 채점 지시로 작동하거나 grader가 답을 자기 승인할 수 있다. 독립 세션·도구 없음·출처 인용 검증으로 범위를 제한한다.
- 누락된 판정, 잘못된 모델 envelope, 오래된 결과 파일이 통과처럼 보일 수 있다. 새 실행 기록과 0/1/2 계약을 확인한다.
- 기존 가짜 CLI는 실제 모델 품질을 증명하지 못한다. 실제 부분 채점과 생성기 통합 시험의 근거를 분리한다.
## Proof
- `python3 -m unittest discover -s tests -p test_eval_regex.py -v`
- `python3 -m unittest discover -s tests -p test_eval_assertions.py -v`
- `python3 -m unittest discover -s tests -p test_eval_semantic_runner.py -v`
- `make check`, `git diff --check`, `.claude/agents/verifier.md`의 별도 보고.
- 0013 실제 출력 및 인증 부재 반례의 Sonnet·low 부분 채점 기록. 실패를 숨기지 않는다.
- 사용 브랜치에 자동 로드되는 스킬·플러그인·필수 특정 스킬 지시·제작 이력이 없는지 검토한다. 선택적 예시는 자체 제작 출처를 확인한다.
