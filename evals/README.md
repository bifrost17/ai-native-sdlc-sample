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
└── run.sh            실행기 — 키 필요. 키 없으면 rc=2
```

키 없이 도는 부분(`bash tests/test_evals.sh`, `make test` 안)은 케이스 스키마·채점기
rc 계약과 「capture-intent 스킬대로 손으로 쓴 intent(`testdata/01-pass`)가 통과한다」를
잰다. 모델이 실제로 무엇을 쓰는지는 `ANTHROPIC_API_KEY` 가 있어야 돌고, CI 에서는
`.github/workflows/agent-evals.yml` 이 키와 함께 `make evals` 를 부른다(L10 689행).
케이스는 「레슨대로 쓴 에이전트가 통과한다」이지 아티팩트 형식 검사가 아니다.

현재 네 케이스 중 `04-org-policy-application` 은 조직 정책을 읽고 직원 연락처·로그·타임스탬프·인증·오류 문구에 적용해 spec 을 쓰게 한다. 실행기는 모든 케이스에 현재 체크아웃의 `org-skills` 를 `--plugin-dir` 로 명시하고, 케이스별 작업 디렉터리와 그 안의 `PROJECT-POLICY.md` 를 안내한다. CI 변경 경로에는 `org-skills/**`, `policies/**`, `templates/**`, `evals/**`, `.claude-plugin/**` 와 평가 워크플로 자체도 포함된다.

`tests/test_eval_plugin.py` 는 가짜 Claude CLI로 플러그인 인자·작업 디렉터리·오류 전파를 시험한다. 정책 이름만 나열한 결과가 실패하는지도 확인한다. 이는 실제 모델이 스킬을 읽었다는 증거가 아니다. 새 케이스도 기존 `file_exists`/`contains` 채점만 쓰며, `assertions` 의 의미적 채점과 정규식 채점 문제는 체인 0013의 범위에서 제외했다. 실제 정책 적용은 모델의 도구 기록과 spec 내용을 함께 읽어 확인해야 한다.

```bash
bash tests/test_evals.sh                                # 결정론 부분
bash evals/check.sh --kinds                              # 판정 종류 목록
ANTHROPIC_API_KEY=… bash evals/run.sh                    # 전체(모델 태움)
```
