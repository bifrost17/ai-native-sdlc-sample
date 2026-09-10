# evals — 설정이 바뀔 때 도는 회귀 스위트
<!-- TEAM: 20-50 real task cases + ANTHROPIC_API_KEY secret — docs/ADOPTING.md · L22 -->

L10 671행: "a suite that runs whenever the agent's configuration changes...
says whether the agent still does the work to the same standard."

```
evals/
├── cases/*.json      프롬프트 + 판정 (스키마: SCHEMA.md)
├── fixtures/<케이스>/ 각 프롬프트가 가리키는 입력 파일
├── testdata/         채점기 자체를 재는 손픽스처(모델 미개입)
├── check.sh          결정론 채점기 — 키 불요. rc 0/1/2
├── grade_assertions.py  별도 Sonnet·low 세션의 의미적 채점과 근거 검증
├── record.py         생성 결과 정규화·단계별 상태·실행 집계
└── run.sh            --semantic이 전체 평가. 기본 호출은 결정론 전용
```

키 없이 도는 부분(`bash tests/test_evals.sh`, `make test` 안)은 케이스 스키마·채점기
rc 계약과 「capture-intent 스킬대로 손으로 쓴 intent(`testdata/01-pass`)가 통과한다」를
잰다. 모델이 실제로 무엇을 쓰는지는 `ANTHROPIC_API_KEY` 가 있어야 돌고, CI 에서는
`.github/workflows/agent-evals.yml` 이 키와 함께 `make evals` 를 부른다(L10 689행).
케이스는 「레슨대로 쓴 에이전트가 통과한다」이지 아티팩트 형식 검사가 아니다.

현재 네 케이스 중 `04-org-policy-application` 은 조직 정책을 읽고 직원 연락처·로그·타임스탬프·인증·오류 문구에 적용해 spec 을 쓰게 한다. 실행기는 모든 케이스에 현재 체크아웃의 `org-skills` 를 `--plugin-dir` 로 명시하고, 케이스별 작업 디렉터리와 그 안의 `PROJECT-POLICY.md` 를 안내한다. CI 변경 경로에는 `org-skills/**`, `policies/**`, `templates/**`, `evals/**`, `.claude-plugin/**` 와 평가 워크플로 자체도 포함된다.

체인 0014부터 `make evals`는 생성 뒤 결정론 검사와 의미적 assertion을 모두 실행한다. 생성과 채점은 서로 다른 Sonnet·low 세션이며, 채점에는 도구를 제공하지 않는다. 실제 출력·입력·도구 기록·정책 원문을 근거로 판정하고 인용을 검증한다. 둘 중 하나라도 실패하거나 판정 불가이면 전체 평가가 통과하지 않는다. 실행마다 새 디렉터리의 `summary.json`과 상세 근거를 보존한다.

네 사례에는 현재 단계에 맞는 스킬의 선택·실제 읽기/호출·산출물 적용도 assertion으로 포함한다. 이름만 쓰거나 관련 없는 단계의 스킬을 호출한 것을 활용 성공으로 세지 않는다. 이들은 의도·검토·설계 단계의 부분 평가이며, 사람 역할과 여러 차례 주고받는 전체 SDLC 실험을 대신하지 않는다.

`tests/test_eval_plugin.py`는 기존 결정론 전용 호출의 플러그인 연결을, 새 `test_eval_regex.py`·`test_eval_assertions.py`·`test_eval_semantic_runner.py`는 오류·채점·전체 실행 연결을 시험한다. 가짜 CLI 시험은 실제 모델 품질을 증명하지 않는다. 실제 부분 실행 결과와 원래 실패는 검증 기록에 구분해 남긴다.

```bash
bash tests/test_evals.sh                                # 결정론 부분
bash evals/check.sh --kinds                              # 판정 종류 목록
ANTHROPIC_API_KEY=… make evals                           # 전체: 생성 + 두 종류 채점
bash evals/run.sh                                       # 키 필요; 결정론 전용, assertions 미채점
```

기존 산출물을 재채점할 때는 `python3 evals/grade_assertions.py --case <case.json> --result <result.json> --trace <generator.jsonl> --out <grade.json>`를 사용한다. CLI의 로그인 계정으로 이 부분 채점을 실행할 수 있지만, 키가 필요한 전체 CI 평가와 같은 실행이었다고 보고하지 않는다.
