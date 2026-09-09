# evals — 설정이 바뀔 때 도는 회귀 스위트

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

```bash
bash tests/test_evals.sh                                # 결정론 부분
bash evals/check.sh --kinds                              # 판정 종류 목록
ANTHROPIC_API_KEY=… bash evals/run.sh                    # 전체(모델 태움)
```
