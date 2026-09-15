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
| `expected_output` | ✓ | assertion 채점에 제공할 기대 서술. 자체 점수는 없고 assertions의 판단 맥락이다 |
| `files` | ✓ | 입력 픽스처 경로. `run.sh` 가 워크스페이스로 복사한다 |
| `assertions` | ✓ | 비어 있지 않은 산문 배열. 전체 평가에서 별도 LLM 세션이 항목별로 채점한다. `check.sh` 단독은 채점하지 않는다 |
| `checks` | ✓ | 결정론 판정 목록(0건이면 판정 불가) |
| `grading_context` | | 의미적 채점에 필요한 정책·지침 원문 경로 배열. 저장소 상대 경로이며 기본값은 빈 배열. `SDLC_PROJECT`와 `SDLC_ORG_SKILLS`는 실행기가 선택한 에디션 경로로 치환한다 |

공유 prompt의 `SDLC_PLUGIN_NAME`은 선택한 `org-skills/.claude-plugin/plugin.json`의 `name`이다.
생성과 의미 채점에 같은 이름을 사용하므로 특정 배포판의 스킬 namespace를 케이스에 고정하지 않는다.

## 판정 종류 — 닫힌 집합 5종 (정본: `evals/check.sh --kinds`)

`file_exists` `contains` `not_contains` `regex_present` `regex_absent`. 아티팩트의
형식(frontmatter·절 목록)을 재는 kind 는 없다 — 형식은 스킬이 말하고 PO 가 읽는다
(docs/BOUNDARY.md). `path` 는 워크스페이스 상대이고
절대경로·`..` 는 판정 불가. 목록 밖 kind 를 만나면 건너뛰지 않고 rc=2 로 죽는다.
정규식은 시스템 grep의 ERE다. grep 종료 코드 0은 일치, 1은 불일치이고 그 외는
구문·읽기·실행 오류이므로 rc=2다. 오류를 `regex_absent`의 통과로 계산하지 않는다.

## 결과 파일 (check.sh 의 두 번째 인자)

`{"schema_version": 1, "case_id": "...", "workspace": "<상대경로>", "result": "...", "claude_raw": {...}}`
— `workspace` 는 결과 파일 위치 기준 상대경로다.

## 전체 평가 결과

`run.sh --semantic`은 실행마다 `evals/out/<edition>/semantic-*/`를 새로 만들고 다음을 남긴다. `<edition>`은 `SDLC_EDITION`의 엄격한 허용 목록에 남은 `tdd-optional`이고 기본값도 같다. 폐기한 판이나 다른 값은 판정 불가로 거부한다.

- `<id>.claude.jsonl`·`.claude.stderr`: 생성기의 실행 기록. 성공한 최종 result가 있어야 채점한다.
- `<id>.json`: 생성 결과 wrapper. `record.py normalize`가 trace에서 만든다.
- `<id>.checks.log`: 결정론 검사 출력.
- `<id>.assertions.json`: 항목별 `index`, `assertion`, `result`(pass/fail/undecidable), `reason`, `evidence`(source/excerpt), 집계와 rc.
- `<id>.assertions.packet.json`·`.assertions.raw.json`: 선택한 에디션, 근거 원문 전체와 source별 SHA-256을 포함한 채점 입력과 채점 프로세스 결과.
- `<id>.status.json`: 생성·결정론·의미적 단계의 종료 코드와 최종 상태.
- `summary.json`: 모든 케이스의 결과, pass/fail/undecidable 수, 전체 케이스를 분모로 한 pass_rate.

의미적 채점은 새 Sonnet·low 세션에서 수행한다. 채점 모델에는 도구를 제공하지 않고,
Python이 입력 픽스처·실제 산출물·선택한 정책 원문·정규화한 도구 기록을 전달한다.
모델의 주장만으로 실제 스킬 읽기를 인정하지 않는다. 단계와 스킬 역할의 적합성, 읽기/호출,
산출물의 적용을 함께 평가하며 제공되지 않은 스킬을 활용 성공으로 표시하지 않는다.

모든 assertion의 번호가 빠짐없이 한 번씩 있어야 하며, 근거 인용은 제공된 source의 실제
부분 문자열이어야 한다. 잘못된 응답·인용·trace·모델 실패·판정 근거 부족은 rc=2다.
항목별 실패는 rc=1이며 모두 통과해야 rc=0이다. 전체 평가는 2 > 1 > 0 순으로 합친다.
판정 불가를 pass-rate 분모에서 제외하지 않는다.
