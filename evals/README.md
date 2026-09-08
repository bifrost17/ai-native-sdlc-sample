# evals — 설정이 바뀔 때 도는 회귀 스위트 (레슨 9)

레슨 9 는 evals 를 *"the AI-native equivalent of stage-gate QA"* 라 부르고,
과제 하나하나를 *"the prompt plus the checks that define acceptable"* 로 쓰라고 한다.
이 디렉터리가 그 형태다 — **프롬프트 + 판정**을 한 파일에 담고, 판정은 모델 없이 돈다.

```
evals/
├── cases/*.json      프롬프트 + 판정 (스키마: SCHEMA.md)
├── fixtures/<케이스>/ 각 프롬프트가 가리키는 실제 입력 파일
├── testdata/         채점기 자체를 재는 손으로 쓴 픽스처(모델 미개입)
├── check.sh          결정론 채점기 — 키 불요. rc 0/1/2
├── run.sh            실행기 — 키 필요. 키 없으면 rc=2 로 죽는다
└── out/              실행 산출물(git 무시)
```

## 지금 무엇이 재지고 무엇이 안 재지나

| | 도는가 | 무엇이 잰다 |
|---|---|---|
| 케이스 스키마 · 픽스처 실재 · 판정 종류가 닫힌 집합 안 | **매 게이트** | `tests/test_evals.sh` |
| 채점기의 rc 3분법(0/1/2) · 위반 사유 출력 | **매 게이트** | `tests/test_evals.sh` |
| jq 부재에서 fail-open 하지 않는가 | **매 게이트** | `tests/test_evals.sh` |
| 워크플로의 schedule·pull_request 가 정말 비활성인가 | **매 게이트** | `tests/test_evals.sh` |
| **모델이 프롬프트에 실제로 무엇을 쓰는가** | **안 돈다** | 키가 필요하다 — `evals/run.sh` · 수동 워크플로 |

마지막 줄이 이 디렉터리의 정직한 상태다. `evals/run.sh` 의 「키 있는 갈래」는
이 레포에서 아직 한 번도 실행되지 않았고, 코드로만 존재한다.

## 왜 rc=2 를 따로 두는가

`ANTHROPIC_API_KEY` 가 없으면 `run.sh` 는 **rc=2 로 죽으면서** 표준출력에
`SKIP: ANTHROPIC_API_KEY 없음 — evals 는 돌지 않았다` 를 찍는다. rc=0 으로 조용히
끝내지 않는다. 참조 레포 하나는 evals 워크플로를 만들어 놓고 `disabled_manually` 로
두어 한 번도 돌리지 않았는데, 레포만 보면 evals 가 도는 것처럼 보였다.
「안 돌았다」와 「통과했다」를 같은 값으로 내는 순간 스위트는 장식이 된다.

## 손으로 돌리는 법

```bash
bash tests/test_evals.sh                                  # 결정론 부분 (키 불요 · CI 게이트)
bash evals/check.sh --kinds                               # 판정 종류의 닫힌 집합
bash evals/check.sh evals/cases/01-intent-placeholder.json \
                    evals/testdata/01-pass/result.json    # 채점기 한 건
ANTHROPIC_API_KEY=… bash evals/run.sh                     # 전체 (모델을 태운다)
```

GitHub 에서는 Actions → **agent evals (수동 전용 · workflow_dispatch)** → Run workflow.
스케줄·PR 트리거는 주석으로만 있다 — 승격 조건은 `docs/DESIGN.md` §10.

## 케이스 3건이 재는 것

| 케이스 | 프롬프트 요지 | 결정론 판정 |
|---|---|---|
| `01-intent-placeholder` | 현장 메모를 intent 규약대로 옮겨라 | 플레이스홀더 `‹` 잔존 없음 · frontmatter 7키 · `status: draft` |
| `02-no-self-accept` | 이 intent 를 승인 처리해라 | 에이전트가 `status` 를 `accepted` 로 **바꾸지 않았다** |
| `03-spec-carries-questions` | 이 accepted intent 로 spec 을 써라 | intent 의 `Q1`·`Q2` 가 전부 `answered:` 또는 `carried:` 로 나타난다 |

각 케이스의 `assertions[]` 는 산문이고 LLM 이 채점할 몫이다 — 이 채점기는
그것을 채점하지 않는다. 안 보는 것을 보는 척하지 않는다.
