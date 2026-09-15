# Codex 설치·세션·관측 설계

2026-09-13. [0032 본 설계](../../0032-codex-luna.md)의 기술 부록이다. 아래 설정/명령은 **실행할 후보**이며
설치·모델 실행 성공의 증거가 아니다. 현재 확인 범위는 CLI0.153.4 도움말, read-only 모델 목록,
공식 문서와 저장소 파일이다. 저장한 원문은 [evidence](evidence/official-manifest.json)에 있다.

## P0: 스킬과 프로젝트 진입

1. 선택형 소스의13개 team skill과3개 authoring example을 `.agents/skills/<name>/`에 전체 복사한다.
   `SKILL.md`만 복사하면 `references/`, `scripts/`, 작성 예시 참조가 끊길 수 있다.
   이동 가능한 상대 경로를 유지하고 source→target→hash→변환 사유 manifest를 남긴다.
2. Claude `disable-model-invocation: true`의 명시 사용 의미는 해당 스킬의 `agents/openai.yaml`에서
   `policy.allow_implicit_invocation: false`로 표현한다. 현재 대상은 작성 예시3개와 to-questionnaire다.
   나머지는 실제 원본 의미를 유지한다. 메타데이터 extra field 파싱을 사전에 확인하고,
   Codex가 무시하거나 오해하는 Claude 전용 값은 설치본에서 제거·번역한 diff를 남긴다.
3. plugin prefix와 Claude `Skill`/`Agent`/`AskUserQuestion` 같은 표현은 Codex에 맞는 스킬 파일 읽기,
   native agent, 일반 사용자 질문으로 변환한다. SDLC 판단 기준을 고치기 위한 patch와 섞지 않는다.
   정확한 파일별 범위는 [감사](skill-portability-audit.md)를 따른다.
4. 순수 사용판의 `CLAUDE.md`는 그대로 두고 선택 설치판의 `AGENTS.md`에 다음 진입 예시를 둔다.
   팀 채택 안내는0031 원문의 의미를 유지한다. 설치가 실제로 읽히는지는 P1에서 확인한다.

```markdown
# 프로젝트 작업 지침

이 프로젝트의 공통 작업 지침은 루트 CLAUDE.md다. 작업 전에 그 파일을 읽고 참조한
PROJECT-POLICY.md 및 현재 단계의 정책을 따른다.

## Adopted team workflow

계획한 구현이나 동작·요구·설계·계획에 영향을 주는 후속 요청을 처리할 때 채택한
`.agents/skills/sdlc-feedback/SKILL.md`를 읽고 현재 이벤트에 해당하는 절을 따른다.
구현 완료 보고 전에는 그 절차에 따라 최신 변경 범위를 검토하고 결과를 기다린다. 앞선 검토 이후
바뀐 동작을 이전 검토로 갈음하지 않는다. 현황 질문·단순 산문 정정에는 이 구현 검토를 실행하지 않는다.
```

작성 예시는 명시 사용 대상으로 보존한다. 자동 스킬 호출이 없어도 해당 문서 양식과 안내를 실제로
읽고 적용했다면 그 근거를 따로 인정한다. 모든16개를 호출하도록 prompt나 체크리스트를 만들지 않는다.
`pr-loop`는 hosted PR이 없는 사례에 맞지 않으므로 적절한 미사용을 기대하지만, 메타데이터를 임의로
막아 놓고 모델이 관련성을 잘 판단했다고 평가하지 않는다. 원격 Git 작업은 이번 위임 범위 밖이다.

공식 근거: [skills와 progressive loading](https://learn.chatgpt.com/docs/build-skills),
[AGENTS.md 탐색 순서](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
Codex가 catalog에서 보여준 이름은 본문 전달·적용 증거가 아니다. shell read 등 성공한 본문 읽기도
유효하며 특정 `Skill` 도구 이름만 찾지 않는다.

## P0: native verifier 변환

기본 경로는 `.codex/agents/sdlc-verifier.toml`이다. 이름·설명·developer_instructions를 갖춘
standalone custom agent가 현재 공식 형식이다. 아래의 대괄호 설명은 작성 지시이며 최종 설치 파일에
문자 그대로 넣지 않는다.

```toml
name = "sdlc-verifier"
description = "Independently check a completed implementation or important branch/PR change against current human agreements, spec, plan and actual verification evidence. Report findings before completion; do not use for status questions or perform implementation."
model = "gpt-5.6-sol"
model_reasoning_effort = "high"
sandbox_mode = "workspace-write"
developer_instructions = '''
[tdd-optional/org-skills/agents/sdlc-verifier.md 본문 전체를 복사하고
프로젝트 진입 AGENTS.md/CLAUDE.md와 Codex 도구 표현만 변환한다.]
'''
```

원문의 기준을 wrapper가 별도 파일 링크만 제공하는 방식보다 agent 본문에 직접 담는 방식을 기본으로
선택한다. 따라서 criteria의 전달을 다시 파일 탐색 성공에 의존하지 않는다. 원문 출처·hash와 변환 diff는
setup manifest에 남긴다. Codex agent 파일의 model/effort가 호출 override보다 우선하므로 둘 다 고정한다.
sdlc-feedback의 criteria 참조는 이 TOML로 바꾼다. 제품 root 기준 경로는
`.codex/agents/sdlc-verifier.toml`, 설치된 `.agents/skills/sdlc-feedback/SKILL.md`에서 해석할
Markdown 상대 링크는 `../../../.codex/agents/sdlc-verifier.toml`이며 P0에서 실제 도달을 확인한다.

검증자는 원문처럼 **보고 전용**이며 문서·제품·시험 수정, stage/commit/merge/push, 추가 agent/CLI를
실행하지 않는다. 시험용 임시 데이터 생성은 허용한다. 단위 시험의 임시 파일·관측 때문에 이번에는
workspace-write sandbox를 쓴다. 이것은 수정이 기술적으로 차단된 read-only agent라는 뜻이 아니다.
검토 전후 tracked/untracked/staged diff를 확인하고 시험 임시 파일 외 변경이 있으면 권한 준수 발견으로
기록한다. 원문의 Bash도 본질적으로 읽기 전용 도구는 아니었다.

Claude `tools`, `disallowedTools`, `maxTurns: 20`를 같은 이름의 TOML key로 복사하지 않는다.
이 설정들이 Codex에서 같은 강제를 만든다는 근거가 없다. 동시 자식 수를1로 두고 root 시간·호출
예산과 agent의 보고 전용 지침으로 이번 실행을 제한한다. 이는 자식의 도구 turn 수20과 동등하지 않다.
완료한 child가 아직 열린 thread라면 슬롯을 차지할 수 있다. 개발자는 결과를 보존하고 반환을 기다린 뒤
Codex가 제공하는 종료 동작으로 child를 닫아 다음 검토에 새 문맥을 사용할 수 있게 한다. 이 정리는
검토 기준 변경이 아니라 플랫폼 인계 표현의 일부로 sdlc-feedback 설치본에 기록한다. 이력은 지우지 않는다.
P1에서 자식의 이름/설정 전달·실제 호출·결과 반환·부모 대기·종료 후 두 번째 fresh 호출을 확인해야 한다.
[공식 custom agent 형식과 우선순위](https://learn.chatgpt.com/docs/agent-configuration/subagents).

## P0: 실제 환경과 격리의 한계

고정 후보 설정은 다음과 같다. CLI 인자와 프로젝트 파일의 실제 적용·우선순위는 P1에서 확인한다.

```toml
model = "gpt-5.6-luna"
model_reasoning_effort = "high"
approval_policy = "never"
sandbox_mode = "workspace-write"

[agents]
enabled = true
max_concurrent_threads_per_session = 1
default_subagent_model = "gpt-5.6-sol"
default_subagent_reasoning_effort = "high"

[memories]
use_memories = false
generate_memories = false
```

`--ignore-user-config`는 사용자 config.toml을 제외하지만 인증은 기존 CODEX_HOME을 사용한다.
이 옵션만으로 전역 스킬·AGENTS·plugins·MCP·관리 정책·메모리가 모두 사라졌다고 쓰지 않는다.
개인 폴더를 이름만 바꾸거나 auth 파일을 복사하지 않는다. 관련 경로·이름·활성 상태만 기록하며
토큰·계정 비밀·다른 작업의 원문을 실험 자료로 수집하지 않는다.

- 공식 경로의 `.agents/skills`, 사용자·관리 스킬, 현재 런타임의 추가/legacy 경로, project ancestry와
  사용자 `AGENTS.override.md`/`AGENTS.md` 적용 여부를 확인한다. 사용자가 가진 다른 작업을 건드리지 않는다.
- 선택하지 않은 동명/동등 스킬은 launch별 `skills.config`와 `enabled=false`로 비활성화 가능한지
  실제 catalog와 대조한다. 공식 config-reference는 folder path, skills 예시는 `SKILL.md` path를
  보여주므로 두 후보 중 현 CLI에서 실제 적용되는 형식을 확인해 고정한다. 파일 존재나 설정 parse만으로
  비활성화 성공을 단정하지 않는다. 모든 bundled 도구를 지우는 작업은 하지 않는다.
  남는 공통 시스템 지침·도구는 목록과 한계를 기록한다. 관련 외부 스킬이 제공되면 clean team-only
  조건으로 해석하지 않고 혼합 조건 또는 환경 오염으로 구분한다.
- 메모리 사용/생성은 실험에서 끈다. 외부 MCP·네트워크 작업은 이 작은 로컬 사례에 필요 없으므로
  세션에 제공되는 구성을 확인하고 지원되는 launch/project 설정으로 제외한다. 관리 정책을 우회하지 않는다.
- `workspace-write`는 HUMAN-only 파일의 읽기를 모두 차단하는 비밀 경계라고 가정하지 않는다.
  HUMAN 입력은 repo·Git refs·prompt에 주지 않고 읽기 trace를 확인한다. 실제 비공개 접근/답안 유출이
  있으면 오염으로 분류한다. 더 강한 격리가 필요하면 별도 홈/컨테이너 설계를 먼저 수정한다.
- `.git` 등 보호 경로 때문에 agent의 commit이 막힐 수 있다. smoke에서 로컬 작은 commit을 확인한다.
  막히면 첫 본실험 전에 **HUMAN Git 대행 조건**으로 명시 고정할 수 있다. Luna가 선택한 변경 묶음·diff를
  수락해 root가 commit하고 명령·actor를 남긴다. 이 경우 “Luna의 Git commit 성공”은 미검증이다.
  `danger-full-access`, `--ignore-rules`, sandbox/approval bypass로 조용히 바꾸지 않는다.

[공식 설정 참조](https://learn.chatgpt.com/docs/config-file/config-reference)의 `skills.config`,
`agents`, `memories`, `approval_policy`와 저장한 실제 [exec 도움말](evidence/exec-help.txt)을 함께 본다.
기술적인 샌드박스 조건 변경은 방법론 보완 효과와 분리해 기록한다.

## P1: transport와 smoke

새 실행은 argv 배열과 stdin으로 prompt 파일의 실제 UTF-8 본문을 전달한다. 아래는 인자 구성을
보여주는 예시이며 이 문서 작성 과정에서 실행한 명령이 아니다. 경로는 실제 실행 때 확정한다.

```text
codex exec --ignore-user-config --strict-config --json
  -C <product-directory> --sandbox workspace-write
  -m gpt-5.6-luna
  -c model_reasoning_effort="high" -c approval_policy="never"
  -c agents.enabled=true -c agents.max_concurrent_threads_per_session=1
  -c agents.default_subagent_model="gpt-5.6-sol"
  -c agents.default_subagent_reasoning_effort="high"
  -c memories.use_memories=false -c memories.generate_memories=false
  --output-last-message <human-record-directory>/turns/01.result.md -
```

실제 실행기는 프로젝트 cwd, stderr 파일, 프로세스 종료 코드, 시작/종료 시각을 따로 받는다.
prompt를 shell에 문자열 삽입하지 않는다. 출력 `tail`의 rc를 Codex/시험 rc로 쓰지 않는다.
`--output-last-message`는 CLI transport가 HUMAN 경로에 쓰는 출력이며 agent에 그 경로의 작업 권한이나
oracle 읽기 권한을 준다는 의미가 아니다. 실행 시 이 옵션이 적절하지 않으면 stdout 최종 메시지로 저장한다.

계속 대화할 때는 **관측한 session ID**를 사용해 같은 제품 cwd에서 실행한다.

```text
codex exec resume <observed-session-id>
  --ignore-user-config --strict-config --json -m gpt-5.6-luna
  -c model_reasoning_effort="high" -c approval_policy="never"
  -c sandbox_mode="workspace-write"
  -c agents.enabled=true -c agents.max_concurrent_threads_per_session=1
  -c agents.default_subagent_model="gpt-5.6-sol"
  -c agents.default_subagent_reasoning_effort="high"
  -c memories.use_memories=false -c memories.generate_memories=false
  --output-last-message <human-record-directory>/turns/02.result.md -
```

これは [resume 도움말](evidence/resume-help.txt)의 인자를 기준으로 한 후보다. resume에는 exec의
`-C`/`--sandbox`가 동일하게 노출되지 않아 cwd와 설정 override로 유지한다. prompt/설정 누적 의미와
실제 applied settings는 smoke에서 확인한다. 세션에 잘못된 최초 설정이 있으면 그대로 본실험에 쓰지 않는다.
`--ephemeral`은 continuation·이력 보존 목적과 맞지 않아 사용하지 않는다.
[공식 비대화형 모드](https://learn.chatgpt.com/docs/non-interactive-mode).

smoke는 별도 초기 clone에서 다음을 최대3회에 나누어 확인한다. 한 호출에 모두 지시해 완료해도
이어지는 짧은 질문을 resume하여 세션 연속성은 확인한다.

1. `AGENTS.md`→공통 지침 읽기, 선택한 skill 하나와 명시 사용 skill 하나의 본문/참조 열기. 출력은
   발견한 path·name·간단한 적용 범위만 요청한다. 전체16개 본문을 context에 억지로 올리지 않는다.
2. 별도 smoke 파일의 작은 변경·관련 실행을 하고 native verifier에 현재 범위·기대·base를 넘긴다.
   child의 결과 반환·보존 후 종료하게 명시한다. 이 호출은 자연 이벤트 감지 점수가 아니다.
3. 같은 ID의 후속 질문에서 이전 범위/결과 유지와 짧은 두 번째 fresh native 검토를 확인한다.
   두 child ID가 다르고 첫 종료 뒤 새 슬롯을 사용했는지, 실제 Luna/Sol metadata, 파일 무변경 조건과
   Git 수행/대행 조건, 공개 event의 도구 순서·성공 결과·부모 대기를 확인한다. 다음 검토를 시작할 수
   없으면 runtime 준비 실패로 처리하며 조용히 기존 child를 재사용해 새 문맥이라고 쓰지 않는다.

고의 제품 결함을 본 데이터에 심거나 규칙 거부 게임을 추가하지 않는다. 설치 오류가 나오면 실패
출력을 남기고 adapter만 보정한 새 smoke를1회 허용한다. 그 후에도 핵심 증거를 얻지 못하면 본실험은 시작하지 않는다.

예산·timeout 중단은 최종 답변을 기다리는 일을 멈추는 것과 실행 중인 작업을 멈추는 것을 구별한다.
실행기가 기록한 대상 process/session/child만 종료·중단하고, 남은 자식과 파일 변경이 없는지 확인한 뒤
중단 당시 diff·rc·미완료 범위를 저장한다. 관련 없는 Codex 프로세스를 일괄 종료하지 않는다.
현재 버전의 정확한 종료·이력 보존 동작은 P1에서 확인하며 미확인 상태를 정상 종료라고 기록하지 않는다.

## 공개 사건과 시간 순서 근거

`--json` 형식이 Claude/OpenCode 원본과 같다고 가정하지 않는다. P1에서 실제 이벤트 schema와
session/turn/native 관련 key를 작은 표에 고정한다. thread.started 등의 이름도 관측한 값으로 기록한다.
각 호출의 JSON 공개 응답·tool 입력/결과·최종 요약·usage를 보존하되 숨겨진 reasoning 이벤트와
인증 비밀은 제외한다. 공개 event 번호는 원본 위치와 정제본 위치의 대응을 유지한다.

도구 호출 요청만으로 쓰기 성공을 판단하지 않는다. 적용 성공 결과와 당시 파일/diff를 대조한다.
복합 shell에서 문서와 코드가 함께 바뀌면 명령 내부 순서·성공 결과로 확인 가능한 범위만 쓰고,
모호하면 순서 미검증이다. 리뷰어가 최신 문서를 읽었다는 말은 실제 읽기/전달 증거와 분리한다.

CLI JSON이 native 사건이나 모델·문서 쓰기 결과를 충분히 주지 않으면 대상 session/child만의
공식 이력 읽기 또는 app-server session 조회로 **공개 메시지·도구 결과만** 보충한다. 이 방식의
가용성과 정확한 호출은 P1에서 검증한 후 기록한다. 전체 개인 session 저장소 덤프나 숨겨진 추론
보존은 하지 않는다. body 전달·중요 문서 순서·native 반환/대기 등 핵심 증거가 끝내 불가능하면
실험 범위를 축소해 평가 미검증을 명시하고 정식 본실험 조건을 먼저 재설계한다.

통계는 설치 수·관련 기회·본문 읽기·적용 사례·native 호출/반환/실패·HUMAN 복구·root 호출·시간·usage를
구분한다. 자식이 background로 시작하고 같은 호출의 끝에서 반환한 것을 두 독립 실행으로 세지 않는다.
실패/재시작·요청 모델과 관측 모델 차이·관측할 수 없는 effort·알 수 없는 비용은 빠짐없이 남긴다.

## 공식 원문과 현장 조회 보존

| 파일 | 의미 |
|---|---|
| [official-manifest.json](evidence/official-manifest.json) | 공식 Markdown 원문의 URL·조회 시각·byte/hash. 원문 그대로 보존 |
| [skills.md](evidence/skills.md), [agents-md.md](evidence/agents-md.md) | 설치/발견·명시 사용 정책·프로젝트 진입 |
| [subagents.md](evidence/subagents.md) | native custom agent·model/effort 우선순위 |
| [non-interactive.md](evidence/non-interactive.md), [config-reference.md](evidence/config-reference.md) | CLI·resume·설정·권한 관련 정의 |
| [cli-version.txt](evidence/cli-version.txt), [exec-help.txt](evidence/exec-help.txt), [resume-help.txt](evidence/resume-help.txt) | 현재 설치0.153.4에서 조회한 실제 도움말 |
| [prompt-input-help.txt](evidence/prompt-input-help.txt) | read-only prompt inspection 도움말만 조회. 실제 개인 prompt 덤프 미실행 |
| [selected-model-catalog.json](evidence/selected-model-catalog.json) | read-only catalog 중 Luna/Sol/Astra 공개 필드만 발췌. 실제 모델 실행 증거 아님 |

공식 문서와 설치 버전의 동작이 다르면 실제 실행 증거와 차이를 기록하며 조용히 호환을 가정하지 않는다.
API 모델 페이지의 단가/context 수치를 Codex 구독 계정의 실제 비용/세션 한도로 대체하지 않는다.
