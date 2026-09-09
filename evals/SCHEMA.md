# evals 케이스 스키마 (레슨 9)

L10 687행: "Write each task as an eval, meaning the prompt plus the checks
that define acceptable (tests pass, lint clean, behavior unchanged, policy
followed)."

## 케이스 파일 `evals/cases/<id>.json`

| 키 | 필수 | 뜻 |
|---|---|---|
| `schema_version` | ✓ | `1` 고정 |
| `id` | ✓ | 파일명(확장자 제외)과 같아야 한다 |
| `prompt` | ✓ | 에이전트에게 넘길 프롬프트 |
| `expected_output` | ✓ | 사람이 읽는 기대 서술(채점 안 함) |
| `files` | ✓ | 입력 픽스처 경로. `run.sh` 가 워크스페이스로 복사한다 |
| `assertions` | ✓ | 산문 — LLM 채점용, `check.sh` 는 채점하지 않는다 |
| `checks` | ✓ | 결정론 판정 목록(0건이면 판정 불가) |

## 판정 종류 — 닫힌 집합 5종 (정본: `evals/check.sh --kinds`)

`file_exists` `contains` `not_contains` `regex_present` `regex_absent`. 아티팩트의
형식(frontmatter·절 목록)을 재는 kind 는 없다 — 형식은 스킬이 말하고 PO 가 읽는다
(docs/BOUNDARY.md). `path` 는 워크스페이스 상대이고
절대경로·`..` 는 판정 불가. 목록 밖 kind 를 만나면 건너뛰지 않고 rc=2 로 죽는다.

## 결과 파일 (check.sh 의 두 번째 인자)

`{"schema_version": 1, "case_id": "...", "workspace": "<상대경로>", "result": "...", "claude_raw": {...}}`
— `workspace` 는 결과 파일 위치 기준 상대경로다.
