# evals 케이스 스키마

## 0. 공식 스키마를 먼저 찾았다 — 그리고 무엇이 있고 무엇이 없는지

공식 문서(`code.claude.com/docs`)를 2026-09-08 에 받아 확인한 결과:

| 물음 | 답 | 근거 |
|---|---|---|
| 비대화형 실행 플래그가 공식인가 | **그렇다** — `-p`/`--print` · `--allowedTools`(별칭 `--allowed-tools`) · `--output-format`(`text`\|`json`\|`stream-json`) | `docs/en/headless.md` · `docs/en/cli-reference.md` |
| `--output-format json` 의 텍스트 결과는 어디 있나 | `.result` 필드 | `docs/en/headless.md` 의 `jq -r '.result'` 예시 |
| **CI evals 케이스 스키마가 공식으로 정의돼 있나** | **없다** — 문서 색인(`docs/llms.txt`)에 `eval` 이 한 번도 나오지 않는다 | 색인 전문 검색 |
| 그래도 문서가 가리키는 eval 파일 형식이 있나 | **있다** — `skill-creator` 플러그인의 `evals/evals.json`. 공식 `docs/en/skills.md` 가 형식 전문을 agentskills.io 로 넘긴다 | `docs/en/skills.md` 「Evaluate and iterate on a skill」 |

`skill-creator` 의 `evals/evals.json` 필드(agentskills.io 「Evaluating skill output quality」):

```
{ "skill_name": …, "evals": [ { "id", "prompt", "expected_output", "files", "assertions" } ] }
채점 산출 grading.json: { "assertion_results": [ { "text", "passed", … } ] }
```

**우리가 한 것.** 우리 케이스는 위 필드명을 **그대로** 쓴다 — `id` · `prompt` ·
`expected_output` · `files` · `assertions`. 한 글자 다르게 쓰면 그 필드는 조용히
무시된다(honghu 는 `assertions` 를 `expectations` 로 써서 21케이스가 채점기에
안 잡힐 개연이 있었다). 다만 두 가지를 의도적으로 다르게 하고, 이유를 적는다:

1. **케이스 1건 = 파일 1개**(`evals/cases/<id>.json`). 공식은 배열 하나에 모아 둔다.
   우리 케이스는 사슬 단계마다 소유자가 다르고 CODEOWNERS 로 나눌 것이라 파일을 가른다.
   그래서 `skill_name` 대신 `id` 가 파일명과 같아야 한다(시험이 대조한다).
2. **`assertions` 는 산문 그대로 두고 채점하지 않는다.** 공식 `assertions` 는
   LLM 이 채점하는 자연어 문장이다. 우리 채점기 `check.sh` 는 결정론이라 산문을
   판정할 수 없다. 산문을 결정론인 척 채점하면 그 자리가 거짓 그린이 된다 —
   그래서 결정론 판정은 **`checks`** 라는 다른 이름의 필드에 둔다. 같은 이름 아래
   다른 의미를 넣지 않는 것이 요점이다.

`checks` 는 **우리 정의**다(공식 스키마 없음). 아래가 그 정의다.

## 1. 케이스 파일 `evals/cases/<id>.json`

| 키 | 필수 | 뜻 |
|---|---|---|
| `schema_version` | ✓ | `1` 고정. 다른 값이면 채점기가 rc=2 |
| `id` | ✓ | 파일명(확장자 제외)과 같아야 한다 |
| `prompt` | ✓ | 에이전트에게 그대로 넘길 프롬프트 |
| `expected_output` | ✓ | 사람이 읽는 기대 서술(채점되지 않는다) |
| `files` | ✓ | 입력 픽스처의 레포 상대경로. `run.sh` 가 워크스페이스 루트로 basename 그대로 복사한다. 없는 파일을 가리키면 판정 불가 |
| `allowed_tools` | — | `--allowedTools` 에 넘길 값. 없으면 `Read,Write,Glob,Grep` |
| `measures` | — | 이 케이스가 무엇을 재는지 한 문단(사람이 읽는다) |
| `assertions` | ✓ | **산문 · LLM 채점용 · `check.sh` 는 채점하지 않는다.** 키가 붙어 심사자가 생기는 날 쓴다 |
| `checks` | ✓ | 결정론 판정 목록. 0건이면 통과가 아니라 판정 불가다 |

## 2. 판정 종류 — 닫힌 집합 7종

정본은 `evals/check.sh` 의 `CHECK_KINDS` 하나이고 `bash evals/check.sh --kinds` 로
읽는다. `tests/test_evals.sh` 1번이 케이스의 모든 `kind` 가 이 목록 안인지 대조한다.

| kind | 필수 필드 | 판정 |
|---|---|---|
| `file_exists` | `path` | 파일 또는 디렉터리가 있다 |
| `contains` | `path` `value` | 파일 내용에 `value` 가 부분문자열로 있다 |
| `not_contains` | `path` `value` | 없다 |
| `regex_present` | `path` `pattern` | ERE 가 **한 줄이라도** 맞는다(`^`·`$` 는 줄 단위) |
| `regex_absent` | `path` `pattern` | 한 줄도 안 맞는다 |
| `frontmatter_has_keys` | `path` `keys[]` | YAML frontmatter 최상위에 그 키들이 전부 있다 |
| `frontmatter_equals` | `path` `key` `value` | frontmatter 의 그 키 값이 `value` 와 같다 |

- `path` 는 **워크스페이스 상대**다. 절대경로와 `..` 는 판정 불가로 거절한다.
- frontmatter 는 첫 줄이 `---` 여야 하고, 최상위(들여쓰지 않은) `키: 값` 줄만 읽는다.
  값 끝의 ` #주석` 은 떼어낸다 — 우리 템플릿이 `status:` 줄에 어휘 목록을 주석으로 달기 때문이다.
- **임의 셸 조각을 실행하는 판정은 두지 않는다.** 그 순간 판정 어휘의 소유자가
  채점기에서 케이스 작성자로 넘어가고, 닫힌 집합이라는 성질이 사라진다.
- 목록에 없는 `kind` 를 만나면 **건너뛰지 않고 rc=2 로 죽는다.**

## 3. 결과 파일 (채점기의 두 번째 인자) — 우리 정의

```json
{
  "schema_version": 1,
  "case_id": "01-intent-placeholder",
  "workspace": "01-intent-placeholder/ws",
  "result": "모델의 최종 텍스트(--output-format json 의 .result)",
  "claude_raw": { "…": "--output-format json 원문 전량 — 감사 추적용" }
}
```

- `workspace` 가 상대경로면 **결과 파일이 있는 디렉터리** 기준으로 푼다.
  그래야 픽스처가 어느 CWD 에서 돌아도 같은 것을 가리킨다.
- 워크스페이스 디렉터리가 없으면 rc=2 다. 「대상이 없다」는 통과가 아니다.
- `result` 는 감사용으로 보관만 하고 `checks` 는 이 문자열을 판정하지 않는다.
  판정 대상은 전부 워크스페이스 안의 **파일**이다.

## 4. 반환값 — 「안 돌았다」와 「통과했다」는 다른 값이다

| rc | `check.sh` | `run.sh` |
|---|---|---|
| 0 | 판정 전부 통과 | 전 케이스 통과(모델을 실제로 태웠다) |
| 1 | 판정 하나 이상 실패 | 케이스 하나 이상 판정 실패 |
| 2 | 판정 불가 — jq 없음 · 파일 없음 · 스키마 위반 · 닫힌 집합 밖 kind · 워크스페이스 없음 | 키 없음 · `claude` 없음 · 픽스처 없음 · 채점기 rc=2 |

`rc=2` 를 `rc=0` 으로 접는 코드는 이 레포에 없다. 워크플로도 rc=2 를 「skip」으로
**표시만** 하고 통과로 바꾸지 않는다.
