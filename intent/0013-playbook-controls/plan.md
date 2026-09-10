# Plan: 플레이북 통제 보완 1·2·4
Upstream: spec.md@e152f50. Status: draft.
프로젝트 오너가 대화에서 보완 1·2·4번의 우선 구현을 지시해 draft 체인에서 진행한다. 승인은 PR 머지로 기록한다.
## Files that change
- `.claude/hooks/_lib.sh`, 필요 시 `protect-paths.sh`·`protect-tests.sh`·`format-lint.sh`: 경로 정규화와 오류 전파.
- `tests/test_hook_paths.py` (new): 경로·심볼릭 링크·새 파일·정상 대조 회귀 시험.
- `.claude/skills/design-spec/SKILL.md`, `org-skills/skills/spec-policy-pass/SKILL.md`, `org-skills/commands/spec-policy.md`, `org-skills/.claude-plugin/plugin.json`, 관련 PROVENANCE: 배포 위치와 판 기록 안내.
- `templates/spec.md`: 설치 캐시에서도 실제 출처·판을 기록할 수 있도록 스킬 인용 안내를 맞춘다.
- `.github/workflows/agent-evals.yml`, `evals/run.sh`, `evals/cases/04-org-policy-application.json` (new), 대응 fixtures (new), `tests/test_eval_plugin.py` (new): 조직 스킬 평가 연결.
- `.github/workflows/bands.yml`, `scripts/run_bands.py` (new), 필요 시 `scripts/emit_intent.py`, `tests/test_bands_workflow.py` (new): 등급별 실행·오류 전파.
- `docs/verification/north-star-playbook.html`, `docs/verification/README.md`, `docs/verification/CHAPTERS.md`, `docs/verification/INDEX.md`, `docs/verification/0013-controls.md`·`0013-policy-evidence.json` (new): 반례·수정·검증 근거, 실제 모델의 정책 읽기·출력과 해당 판정 갱신.
- `evals/README.md`, `docs/BOUNDARY.md`, `docs/ADOPTING.md`, `policies/README.md`: 네 번째 평가 케이스, 플러그인 연결, 출처·판 기록 안내를 동기화.
## Order of work
1. intent·spec·plan을 각각 기록한다. 기존 목표 문서의 미커밋 수정은 유지한다.
2. 서로 다른 파일을 맡은 작업으로 훅, 조직 스킬, bands를 병렬 구현한다. 각 작업은 새 회귀 시험으로 기존 실패를 확인한 뒤 구현한다.
3. 변경을 합쳐 `make check`를 실행한다. 필요할 때만 관련 추가 시험을 돌린다.
4. 실행 증거와 실제 모델·호스티드 CI 미검증을 분리해 북극성 주석에 반영한다.
5. 별도 verifier가 결과와 계획을 대조한다. 발견을 해결하고 영향받은 검증을 다시 실행한다.
## Risks
- 경로 정규화가 정상 파일이나 macOS의 심볼릭 링크 경로까지 차단할 수 있다. 실제 대상과 논리적 보호 경로를 모두 시험한다.
- 플러그인 로드 인자와 버전 표기가 설치 캐시·로컬 체크아웃에서 다를 수 있다. 가짜 CLI 통합과 가능한 실제 실행을 분리한다.
- 2σ에 쓰기 권한을 주거나 모델 오류를 성공으로 숨길 수 있다. 도구 인자·산출물·종료 코드를 등급별로 시험한다.
- 3번 채점 문제는 남아 있다. 이번 회귀 시험이나 주석에서 의미적 검증을 끝냈다고 주장하지 않는다.
## Proof
- `python3 -m unittest discover -s tests -p test_hook_paths.py -v`
- `python3 -m unittest discover -s tests -p test_eval_plugin.py -v`
- `python3 -m unittest discover -s tests -p test_bands_workflow.py -v`
- `make check`, `git diff --check`.
- 변경 전 북극성과 비교해 플레이북 원문은 동일하고 평가 주석만 해당 근거로 갱신됐음을 확인한다.
- `.claude/agents/verifier.md`를 읽은 독립 에이전트의 실행·관측·계획 대조·한계 보고를 남긴다.
