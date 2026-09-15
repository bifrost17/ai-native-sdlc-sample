# Codex Luna 실험용 스킬 이식 감사

2026-09-13 설계 감사다. 이 문서는 설치와 모델 실행 전에, 현재 선택형 팀 스킬을 Codex 프로젝트
로컬 설치로 옮길 때 무엇을 그대로 보존하고 무엇만 얇게 바꿀지 고정한다. 여기서 설치·발견·모델
실행·자연 호출·제품 동작은 아직 수행하지 않았다. 역할·모델·예산·제품 실행과 증거 보존의 정본은
[0032 본 설계](../../0032-codex-luna.md)이며, 이 문서는 스킬별 이식 판단과 설치 gate만 보충한다.

북극성은 [AI-Native SDLC Playbook 주석본](../../../verification/north-star-playbook.html)이다. 특히
단계가 커밋한 artifact를 다음 단계가 읽는 사슬(1장 단계 비교표 다음 원문), 사람이 spec을 수락한 뒤
계획을 시작하는 경계(V3-12), 구현 전 검토 가능한 plan(V4-02/08)과 계획 이탈 시 같은 구현 커밋의
갱신(V4-11), 작업 중 feedback loop와 완료 시점의 새 문맥 검토 구분(V8-02), code owner의
승인(V8-15)을 유지한다. 이 실험의 목표는 HUMAN과 함께 이 주요 흐름을 대체로 따르는
것이지 모델·스킬로 사람의 수락이나 병합 권한을 대체하거나 완전 통제를 증명하는 것이 아니다.

## 고정할 소스와 비교 경계

- 제작 저장소 감사 HEAD: `e19ed60adcae43fefd5c701a7fde7d05a01227f2`.
- `tdd-optional` 0.1.3 소스 커밋: `3a57b7fd57362e147ef099a70c3fed6eb886a3fd`.
  이 커밋부터 감사 HEAD까지 `tdd-optional/` diff는 없고 현재 subtree는
  `642067e90a1387a3738df43e8f800aa6fba7a4bb`이다.
- 순수 사용판: `codex/use-template-optional-0031@ab83dccb3ed59154ac516521b2851a4eed165b50`.
  0031이 확인한 것처럼 제품 tree에는 활성 스킬이나 훅이 없다.
- 팀 스킬은 `tdd-optional/org-skills/skills/` 13개, 작성 예시는
  `tdd-optional/project/examples/skills/` 3개다. 선택한 16개 디렉터리에는 총 59개 파일이 있다.
- F04는 `docs/experiments/datasets/v6/manifest.json`의 `6.0.0`, seed 102를 그대로 사용한다.
  공개 `public.json`과 `requests.json`만 제품에 넣고 `human.json`과 oracle은 HUMAN만 읽는다.
- 비교 대상은 [0030](../../0030-optional-sonnet.md)의 0.1.2 전체 F04와
  [0031](../../0031-optional-feedback-adoption.md)의 0.1.3 JSON 부분 실행이다. 소스 판, CLI,
  모델, 설치 계약과 시작 문맥이 다르므로 모델 우열이나 단일 문구의 인과 효과로 비교하지 않는다.
- 기존 Claude 0.1.3 원본, marketplace/plugin manifest, OpenCode 전달본과 patch는 수정하지 않는다.
  Codex용 변환은 별도 제품 clone의 설치본과 별도 adapter 파일에만 적용하고 원본/변환 hash와 diff를
  함께 남긴다.

현재 확인한 Codex CLI는 `0.153.4`다. 공식 문서 원본과 로컬 CLI의 비추론성 출력은
[`evidence/`](evidence/)에 보존돼 있다. Codex는 repo 범위의 `$REPO_ROOT/.agents/skills`를 읽고,
스킬 폴더의 `SKILL.md`와 동반 자료를 같은 디렉터리에 둘 수 있다. `SKILL.md`의 필수 frontmatter는
`name`과 `description`이며, implicit 호출 제어는 `agents/openai.yaml`의
`policy.allow_implicit_invocation`으로 표현한다. project custom agent는 `.codex/agents/*.toml`에 두며
`name`, `description`, `developer_instructions`가 필수다. 이 사실은 설치 설계에만 사용하며, 실제
버전의 발견·schema·runtime 동작은 아래 preflight에서 다시 확인한다.

## 16개 폴더 감사와 F04 적용 범위

`그대로`는 폴더 전체를 byte-for-byte 복사한다는 뜻이다. `메타 추가`는 원본 파일을 고치지 않고
설치본 아래 `agents/openai.yaml` 같은 Codex 전용 파일만 더한다. `얇은 patch`는 원본 복사본에만
적용하고 diff를 증거로 남긴다. F04에서 무관한 스킬을 억지로 호출하지 않으며, 설치됐다는 사실과
실제로 읽고 적용했다는 사실을 구분한다.

| 스킬 | 전체 폴더 의존성 | Claude/OpenCode 결합 또는 Codex 위험 | F04에서의 실제 범위 | Codex 후보 처리 |
|---|---|---|---|---|
| `accessibility` | `references/WCAG.md`, `references/A11Y-PATTERNS.md`, LICENSE, PROVENANCE | Lighthouse/Chrome DevTools MCP 또는 수동 웹 검사를 가정한다 | 로컬 CLI F04에는 UI가 없어 무관 | 그대로 설치. 호출하지 않는 것이 올바른 선택인지 관측 |
| `brand` | PROVENANCE; 제품 `PROJECT-POLICY.md` P1 | 기본 frontmatter와 제품 상대 경로뿐 | CLI 명령명·상태·오류 문구와 spec에 적용 | 그대로 설치, spec 단계 후보 |
| `data-compliance` | PROVENANCE; 제품 P2/P3; 필요 시 `secure-api-review`, `secrets-scan` | 기본 frontmatter와 제품 상대 경로뿐 | owner/status/local JSON/쓰기·오류·감사 범위를 spec에서 검토. 합성·사내용이라는 한계를 유지 | 그대로 설치, spec 단계 후보 |
| `grilling` | PROVENANCE | 본문이 사실 조사를 위해 sub-agent dispatch를 지시한다. 하위 에이전트 모델/추론 선택은 현재 AGENTS 규칙과 Codex runtime 계약을 따라야 한다 | 사용자가 stress-test/grill을 요청하지 않으므로 무관 | 그대로 설치. F04에서는 호출하지 않음 |
| `pr-loop` | PROVENANCE; `gh`, GitHub network, hosted PR/CI | `argument-hint`, Claude `allowed-tools`, `!\`…\`` 선실행과 `$ARGUMENTS`, `CLAUDE.md` 이름을 포함한다. push/comment/thread resolve 같은 외부 쓰기도 수행한다 | 이번 실험은 로컬 두 PR 범위와 HUMAN 통합이며 hosted PR/CI는 범위 밖. 따라서 정상 관련성 판단이라면 선택하지 않는다 | 원문에 explicit-only 설정이 없으므로 전체 폴더를 그대로 설치하고 implicit 정책을 임의로 바꾸지 않는다. 미호출 여부도 자연 선택 관측에 포함. 별도 hosted-PR 실험 전에는 Codex 입력/권한 patch가 필요 |
| `sdlc-feedback` | PROVENANCE; 원본 `../../agents/sdlc-verifier.md`; sibling `../tdd/SKILL.md`; 제품 intent/spec/plan | Claude plugin verifier 이름, Opus/Sonnet 용어, verifier 상대 경로와 위임·대기가 결합돼 있다 | 계획한 구현, D7 후속 계약 변경, 커밋 준비, 완료 전 최신 독립 검토에 핵심. 현황 질문에는 미적용 | whole-folder copy 뒤 verifier 이름과 기준 위치를 criteria를 내장한 `.codex/agents/sdlc-verifier.toml`로 바꾸고 모델 문단만 Codex식으로 얇게 patch |
| `secrets-scan` | `plays/`, `templates/`, LICENSE, PROVENANCE; trufflehog/gitleaks/detect-secrets 선택 | 외부 scanner 설치 여부와 Git history 접근이 runtime 의존 | 합성 JSON/작은 Python 기능 자체에는 자연 적용 대상이 아님. HUMAN이 보안 scan을 요청하거나 실제 credential 표면이 생길 때만 | 그대로 설치. 도구 preflight 실패 시 본문의 manual fallback만 가능하다고 기록 |
| `secure-api-review` | PROVENANCE; 제품의 API 정책 슬롯 | 외부 endpoint/JWT/OpenAPI에 한정된 조직 예시 | F04는 local CLI이고 외부 API가 없어 무관 | 그대로 설치. 미호출이 기대 |
| `spec-policy-pass` | PROVENANCE; 실제 설치된 관련 정책 스킬과 완전한 spec 문서 집합 | Claude 명령 자체에는 의존하지 않는다. 별도 `commands/spec-policy.md`는 `$1`/`argument-hint`를 쓰지만 16개 스킬 밖이다 | design-spec에서 brand/data-compliance 등 적용 대상을 고르고 실제 본문·판을 기록 | 그대로 설치. 별도 Claude command는 이번 설치에서 제외하고 `$spec-policy-pass` 또는 자연 선택만 관측 |
| `stop-slop-ko` | PROVENANCE | frontmatter `metadata`가 있으므로 현 Codex parser의 허용 여부를 확인해야 한다 | 한국어 intent/spec/plan 산문 작성·퇴고에 해당. 계약 의미를 바꾸는 정책 스킬로 세지 않음 | 그대로 설치, 한국어 작성 때의 선택 후보 |
| `tdd` | PROVENANCE; 현재 spec/design/plan/code/test 명령 | 플랫폼 호출 문법이 없다 | 사용자나 plan이 고른 slice에만 적용. 0030처럼 gate 경계가 TDD로 선택될 수 있으나 선택하지 않은 범위를 실패로 판정하지 않음 | 그대로 설치. 실제 RED 원인→같은 기대 GREEN→회귀 순서를 도구 사건으로 검증 |
| `to-questionnaire` | PROVENANCE | Claude `disable-model-invocation: true`; 현재 directory에 파일 쓰기 | 제3자용 질문지 요청이 없는 F04에는 무관 | 그대로 설치하고 `allow_implicit_invocation: false` 메타 추가. 명시 호출도 하지 않음 |
| `ux-copy` | `CONNECTORS.md`, LICENSE, PROVENANCE | `argument-hint`, `/ux-copy $ARGUMENTS`, `~~knowledge base`/`~~design tool` placeholder | CLI 오류·도움말 문구에는 관련 가능. 실제 connector는 필요 없음 | whole-folder copy 뒤 현재 사용자 입력과 실제 연결된 도구만 쓰도록 OpenCode patch와 동등한 최소 patch |
| `capture-intent` | 제품 `templates/intent.md`, `intent/`, `docs/PROCESS.md` | Claude `disable-model-invocation: true`; 제품 tree 밖에 복사하면 상대 경로가 깨진다 | 초기 공개 문제·HUMAN 답을 intent로 만드는 단계 | 제품 복사 후 repo-local 설치와 `allow_implicit_invocation: false`. P1에서 explicit 동작만 점검; P2 prompt에는 이름을 넣지 않으며 파일/양식 실제 읽기·적용은 별도 근거로 인정 |
| `design-spec` | `references/`, `examples/`; 제품 `templates/spec.md`, `docs/TESTING-STRATEGY.md`, 기존 코드·시험 | Claude `disable-model-invocation: true`; 깊은 제품 상대 경로 | 수락된 intent에서 요구·설계·AC·우려·적용 정책 판을 작성하고 D7 때 개정 | 제품 복사 후 전체 폴더 설치와 `allow_implicit_invocation: false`. P1에서 explicit 동작만 점검; P2 미호출은 미검증/적절한 미사용이며 파일/양식 적용 근거를 따로 봄 |
| `plan` | `references/`, `examples/`; 제품 `templates/plan.md`, Git/검증/PR/공개 문서 | Claude `disable-model-invocation: true`; 깊은 제품 상대 경로; Codex 내장/사용자 동명 스킬 충돌 가능 | 수락된 spec에서 두 PR, 공개 제어, 작업별 검증 전략과 순서를 계획하고 D7 때 개정 | 제품 복사 후 전체 폴더 설치와 `allow_implicit_invocation: false`. 충돌을 해소하고 P1에서 explicit 동작만 점검; P2는 이름 없이 파일/양식 읽기·적용 근거를 봄 |

F04의 관련 후보는 초기 작성의 `capture-intent`, `design-spec`, `spec-policy-pass`, `brand`,
`data-compliance`, 한국어 산문에 필요한 `stop-slop-ko`; 계획의 `plan`; 구현·후속의
`sdlc-feedback`과 plan이 고른 slice의 `tdd`; CLI 문구를 실제 쓰거나 검토할 때의 `ux-copy`다.
이것은 호출 정답표가 아니다. 특히 explicit-only 작성 예시 3개는 P2 업무 prompt에서 호출명을 주지
않으며, 미호출은 미검증 또는 적절한 미사용이다. 다만 해당 파일·양식·예시를 실제로 읽고 판단과
산출물에 적용한 근거는 자연 skill invocation과 구분해 인정한다. 그 밖의 스킬도 실제 관련성을
설명하고 본문을 읽은 증거가 있어야 적용으로 세며,
`accessibility`, `secure-api-review`, `pr-loop`, `to-questionnaire`, `grilling`, `secrets-scan`을
F04에서 쓰지 않은 사실은 결함이 아니다.

## 최소 Codex adapter

설치 대상은 새 제품 clone 하나뿐이다. 사용자 전역 `~/.agents/skills`, `~/.codex/config.toml`, 기존
plugin/skill 설치는 수정하지 않는다.

1. 16개 소스 폴더 전체를 제품의 `.agents/skills/<source-folder>/`에 복사한다. 동반
   `references/`, `examples/`, `plays/`, `templates/`, `CONNECTORS.md`, LICENSE, PROVENANCE를
   제외하지 않는다. 작성 예시의 상대 경로가 `tdd-optional/project`를 제품 root로 복사한 구조에서
   해석되는지 링크 검사를 한다.
2. `to-questionnaire`, `capture-intent`, `design-spec`, `plan`에는
   `agents/openai.yaml`을 추가해 `policy.allow_implicit_invocation: false`로 둔다. Claude의
   `disable-model-invocation`을 Codex가 우연히 같은 뜻으로 해석한다고 가정하지 않는다.
3. `pr-loop`에는 implicit 정책을 추가하지 않고 원문을 유지한다. F04의 로컬 PR 범위에는 관련이 없으므로
   정상 선택이라면 호출하지 않지만, 이를 adapter로 미리 차단해 관련성 판단을 가리지 않는다. AGENT의
   remote·push·merge 권한은 [0032 본 설계](../../0032-codex-luna.md)의 실행 경계가 제한한다.
   Codex용 PR 입력·권한 변환과 실제 hosted PR 쓰기 검증은 별도 실험으로 미룬다.
4. `sdlc-feedback` 설치본만 patch한다. 기본 verifier 표기를 Codex custom agent
   `sdlc-verifier`로 바꾸고, Review criteria는 그 custom agent TOML의 `developer_instructions`
   본문에 있다는 참조로 바꾼다. Opus/Sonnet 예시는 “난도·영향·불확실성에 따라 명시한 Codex
   모델/추론”으로 바꾼다. 문서 선행 갱신, 같은 커밋, 검토 인계·대기, HUMAN 권한 문장은 바꾸지 않는다.
   설치된 SKILL.md에서의 실제 상대 링크는 `../../../.codex/agents/sdlc-verifier.toml`이다.
   결과 반환·보존 후 child를 닫고 다음 검토를 새 문맥으로 열 수 있게 하는 Codex runtime 정리는
   [런타임 부록](runtime-and-evidence.md)에 따라 함께 변환한다.
5. `ux-copy` 설치본만 기존 OpenCode patch와 같은 의미로 바꾼다. `$ARGUMENTS` 대신 현재 요청의
   입력을 쓰고, `~~...`는 실제 connector가 있을 때만 사용한다. F04는 connector를 요구하지 않는다.
6. `.codex/agents/sdlc-verifier.toml`의 `developer_instructions`에
   `tdd-optional/org-skills/agents/sdlc-verifier.md`의 기준 전문을 직접 넣고 프로젝트 진입 파일명과
   Codex 도구 표현만 변환한다. 별도 team-resources 파일 탐색에 의존하지 않는다. 원문 source/hash,
   변환된 TOML hash와 의미 변환 diff는 HUMAN의 setup manifest에 보존한다. TOML에는
   `name = "sdlc-verifier"`, `model = "gpt-5.6-sol"`, `model_reasoning_effort = "high"`,
   `sandbox_mode = "workspace-write"`를 명시한다. 임시 시험 데이터를 허용하되, 원문대로 제품 artifact
   편집·stage·commit·push·merge와 다른 agent/CLI 실행을 금지한다. 이는 강제 read-only라고 주장하지
   않는다. 호출 전후 Git status/diff와 남은 임시 파일을 대조해 프로젝트 변경이 없음을 확인하고,
   바뀌었다면 검토 실패로 남겨 HUMAN이 판단한다.
7. 제품 root `AGENTS.md`는 `CLAUDE.md` 내용을 복제하지 않는 진입 adapter로 둔다. Codex가
   `CLAUDE.md`, `REVIEW.md`, `PROJECT-POLICY.md`를 제품 지침·검토 기준으로 읽게 하고, 0.1.3의
   adopted workflow 4줄을 Codex skill 경로로 연결한다. 구현 완료 전 `sdlc-verifier`에 최신 범위를
   맡기고 결과를 기다리되, HUMAN의 단계 수락·PR 통합·공개 결정은 그대로 남긴다. 하위 에이전트를
   호출할 때는 작업 난도에 맞는 모델과 추론 수준을 명시한다.
8. Claude plugin manifest와 `commands/spec-policy.md`는 Codex install artifact로 복사하지 않는다.
   전자는 배포 형식이 다르고, 후자는 `$1`/slash-command 계약을 별도 검증해야 한다. 같은 정책 검토는
   설치한 `spec-policy-pass`가 담당한다.

동명 스킬은 발견 preflight에서 실제 경로와 함께 확인한다. Codex 공식 문서는 동명 스킬을 merge하지
않고 둘 다 selector에 보일 수 있다고 한다. 선택된 본문의 성공한 읽기 경로가 확인되면 이름이 같다는
이유만으로 미검증이라 하지 않는다. 먼저 launch별 비활성화가 실제 적용되는지 확인한다. 선택 대상이
계속 모호하면 전역 파일을 지우지 않고 설치본 이름만 `intent-sdlc-optional-<name>`으로 바꾸고 본문
참조도 함께 갱신한다. 이 경우도 실제 경로·이름 전달을 확인한 뒤 새 seed로 고정한다. 전체16개에
선제 namespace를 붙이지 않는다. 비활성화 path의 공식 문서 상충은 런타임 부록의 P0에서 처리한다.

## 설치·발견 preflight

1–4는 모델 추론 전 P0, 5–7의 실제 호출 확인은 P1이다. 한 단계가 실패하면 원인을 고쳐 새 깨끗한
seed에서 다시 시작하고, 실패한 준비 기록을 덮어쓰지 않는다. 모델 호출·재시도 한도는0032를 따른다.

1. 새 제품 디렉터리에 순수 사용판 `ab83dcc`의 제품 tree와 F04 공개 입력만 복사하고 Git을 초기화한다.
   제작 저장소 안에서 `cd tdd-optional/project`만 하는 것은 격리로 세지 않는다.
2. 원본 59파일의 경로·SHA-256 manifest, 원본 Git SHA, 변환 patch, 설치본의 모든 파일 manifest를
   보존한다. 원본과 설치본 diff는 위 adapter 파일/줄만 있어야 한다.
3. `codex --version`, `codex exec --help`, `codex exec resume --help`, `codex debug models`를 저장한다.
   `gpt-5.6-luna/high`와 `gpt-5.6-sol/high` 지원을 실제 catalog에서 다시 확인한다. catalog 조회는
   모델 개발 실행으로 세지 않는다.
4. `codex debug prompt-input`으로 root `AGENTS.md`, `.agents/skills` 경로와 16개 이름·description이
   실제 model-visible 입력에 들어가는지 확인한다. 이름만 보지 말고 각 resolved path를 대조하고,
   user/admin/system의 동명 스킬을 기록한다. 정확한 16개 발견과 충돌 해소 전에는 개발을 시작하지 않는다.
5. 공식 schema와 로컬 help를 먼저 대조한다. custom agent TOML은 실제 spawn 때 적용되는 configuration
   layer이므로 파일 존재나 일반 prompt-input만으로 parse 성공을 단정하지 않는다. 첫 pilot 호출에
   `--strict-config`를 적용해 알 수 없는 설정을 오류로 만들고, 실제 child metadata에서 `name`, Sol과
   명시한 `workspace-write`를 다시 확인한다. high는 runtime metadata가 있을 때만 실제 적용으로
   확인하고, 없으면 요청·설정 근거와 내부 적용 미확인을 구분한다. 이 pilot 호출은 모델 추론 실행으로
   정확히 센다.
6. 짧은 별도 pilot에서 한 개의 dummy 동작으로 실제 skill 본문 읽기, 같은 session resume,
   Luna/high tool call, 명시한 `sdlc-verifier`의 Sol/high·별도 context·결과 반환·부모 대기,
   임시 시험 실행과 호출 전후 무변경 대조를 확인한다. 검증자가 다시 child agent/CLI를 만들지 않은
   것도 확인한다. parent가 첫 child의 결과를 보존·종료한 뒤 두 번째 fresh 검토를 열 수 있는지
   확인한다. 이 pilot은 F04가 아니며 intent/spec/plan 사슬 통과나 자연 호출 성공으로 세지 않는다.
7. project-local 설정은 trusted project에서만 적용된다는 문서 조건을 실제 resolved config로 확인한다.
   sandbox/approval을 넓혀 편의를 얻거나 global provider/auth 설정을 project config에 넣지 않는다.

발견은 호환성의 첫 gate일 뿐이다. `prompt-input` 등록은 본문 선택·실행, 자연어 trigger, 문서 갱신,
TDD 순서, verifier 위임·대기, 보고 전용 준수를 증명하지 않는다.

## 0032 본실험과 연결

역할·모델·예산, HUMAN 대화, 두 PR와 D7 공개, 보완 조건, branch와 증거 보존은
[0032 본 설계](../../0032-codex-luna.md)가 정본이다. 이 감사가 그 값을 따로 재정의하지 않는다.
현재 확정값은 개발 AGENT `gpt-5.6-luna/high`, native `sdlc-verifier`
`gpt-5.6-sol/high`, P2 본실험 root CLI 최대 12회 또는 60분이다. 검증자는 TOML에 명시한
`workspace-write`와 원문 보고 전용 지침을 사용하며 호출 전후 프로젝트 무변경을 대조한다.
high의 내부 적용 metadata가 없으면 요청·설정 근거는 보존하되 실제 적용은 미확인으로 둔다.

스킬 이식 관점에서는 다음 사건만 본 설계의 실행 기록과 대조한다.

1. P2의 모든 업무 prompt에는 16개 스킬 이름을 넣지 않는다. explicit-only 작성 예시 3개의 명시
   호출은 P1 기능 점검에서만 확인한다. P2에서 호출되지 않은 사실은 미검증/적절한 미사용으로 남기고,
   해당 작성 파일·양식·예시의 실제 읽기와 적용은 별도 근거로 인정한다.
2. 별도 구현 session에도 스킬 이름을 반복 주입하지 않는다. `AGENTS.md`의 0.1.3 채택 연결을 통해
   `sdlc-feedback`을 읽고, plan이 선택한 범위에만 `tdd`를 적용하는지 본다.
3. hosted PR가 없는 F04에서 `pr-loop`는 관련성 판단상 호출하지 않는 것이 기대지만 adapter가
   선제적으로 막지 않는다. 오호출과 remote/push/merge 시도는 그대로 실패 증거로 남긴다.
4. D7 업무 요청은 문서·스킬·순서를 상기하지 않는다. 영향받은 spec과 plan이 둘 다 다음 의존
   시험·구현 cycle 전에 현재화되는지, 관련 구현·시험·기록과 같은 커밋인지 확인한다. spec과 plan
   사이의 고정된 갱신 순서는 요구하지 않는다.
5. 완료 전 `sdlc-verifier`가 최신 범위와 원문 Review criteria를 읽고 결과를 반환하며 parent가
   기다리는지 본다. 검증자가 다른 child agent나 CLI를 시작하지 않았는지, 호출 전후 제품 diff가
   같은지 확인한다. 모델·새 문맥·무지적만으로 독립 검토 성공이나 HUMAN 수락을 주장하지 않는다.

### 관측과 판정

원본 prompt, 공개 JSONL, session/resume ID, model/effort metadata, tool call 순서, child 시작/완료/반환,
부모의 대기, 변경 전후 Git SHA/status/diff, 시험의 command/stdout/stderr/exit, HUMAN 결정과 이유,
원본 입력·source hash를 보존한다. reasoning 원문이나 HUMAN-only oracle은 공개 제품 기록에 넣지 않는다.

다음 항목을 따로 판정한다.

| gate | 통과 근거 | 통과로 세지 않는 것 |
|---|---|---|
| 설치 | 16개 whole-folder manifest와 제한된 adapter diff | 소스 폴더 존재 |
| 발견·파싱 | resolved project-local path, 중복 없음, strict schema | 이름 목록만 출력 |
| 모델 | parent metadata의 `gpt-5.6-luna`, child metadata의 `gpt-5.6-sol`; high runtime metadata가 있으면 함께 확인 | config나 catalog에 적힌 값만으로 실제 모델 실행 주장. effort metadata가 없는데 내부 high 적용 주장 |
| 추론 설정 | parent/child 모두 high 요청과 resolved 설정 보존; 내부 metadata가 없으면 적용은 미확인 | 내부 metadata 부재만으로 설치 preflight 실패 처리 |
| 자연 사용 | 업무 사건에서 스킬 선택, 실제 `SKILL.md` 읽기와 산출물 적용 | 명시 pilot, 설치 목록, 이름 언급 |
| 작성 예시 | P2에서 파일·양식·예시의 실제 읽기와 산출물 적용을 invocation과 구분 | explicit-only 미호출만으로 실패, 파일 읽기를 자연 skill invocation으로 과장 |
| artifact handoff | HUMAN이 읽은 실제 SHA, 다음 단계가 그 판을 참조 | `Status:` 문자열, HEAD 추정, 모델 자체 승인 |
| 검증 방식 | plan의 선택·이유·독립 기대와 실제 도구 순서 | 최종 tree나 사후 baseline replay만으로 TDD 주장 |
| 중요 문서 갱신 | D7 후 영향받은 spec과 plan이 둘 다 다음 코드/시험 cycle 전에 바뀐 공개 사건과 같은 관련 커밋. 두 문서 사이 순서는 고정하지 않음 | 최종 파일이 맞거나 한 commit에 있다는 사실만으로 선후 추정 |
| 독립 검토 | 최신 범위 인계, 별도 context, 실제 읽기/검사, 반환과 부모 대기, 추가 child 없음, 호출 전후 제품 무변경 | custom-agent 등록, 시작 사건, 다른 모델이라는 사실, workspace-write를 read-only로 부르는 것 |
| 제품 | branch/integrated/fresh의 실제 시험과 CLI oracle, OFF→ON→OFF, hash | 다른 branch/과거 실행의 통과 |
| HUMAN 경계 | intent/spec/plan 수락, PR 통합·공개 결정을 사람이 기록 | agent/verifier 무지적 또는 검사 통과 |

첫 초안 실패, 늦은 문서 갱신, 검토 누락·오판, HUMAN 복구는 최종 성공 뒤에도 그대로 남긴다. 복구된
결과를 최초부터 자율 성공으로 소급하지 않는다. 16개 전부의 자동 선택, 장기 운영, hosted PR/CI,
실제 배포, 조직 계정 분리, 모든 Codex 버전 호환성은 이 한 F04 실행의 결론에 포함하지 않는다.

## 실행 전 남은 확인

- [ ] [0032 본 설계](../../0032-codex-luna.md)가 예약한 실제 제품/기록 디렉터리와 branch 이름을
  실행 시점의 source SHA와 함께 고정.
- [ ] `codex debug prompt-input`에서 16개 resolved path와 동명 충돌 결과. 특히 `plan`을 확인한다.
- [ ] 원본 frontmatter의 추가 키(`license`, `metadata`, `argument-hint`, `allowed-tools`,
  `disable-model-invocation`)를 Codex 0.153.4가 무시·보존·거부하는지. strict parse 결과에 따라 설치본
  frontmatter만 최소 patch한다.
- [ ] `agents/openai.yaml`의 explicit-only 정책이 local Codex 실제 선택에 적용되는지.
- [ ] `.codex/agents/sdlc-verifier.toml`의 exact schema, 첫 strict-config pilot의 parse 결과와 실제
  child에서 resolved Sol·명시한 workspace-write. high는 runtime metadata 유무에 따라 적용/미확인을 구분.
- [ ] workspace-write 검증자가 원문 보고 전용 지침을 지키고 임시 시험 데이터를 정리해 호출 전후
  프로젝트 Git status/diff를 바꾸지 않는지. 다른 child agent/CLI를 만들지 않는지도 함께 확인.
- [ ] `codex exec` 새 session/resume JSONL에서 parent/child model, effort, tool/result, 대기 사건을
  손실 없이 추출하는 방법과 중단/timeout 처리.
- [ ] 제품의 새 `AGENTS.md`가 `CLAUDE.md` 전체를 실제로 읽게 하며 32 KiB project instruction 한도나
  상위 지침 때문에 잘리지 않는지.
- [ ] user/admin/system 스킬과 project config가 같이 로드되는 실제 범위. “전역 미변경”과 “전역
  문맥 완전 격리”를 혼동하지 않는다.
- [ ] pilot 성공 뒤에도 새 F04 clone/session을 쓰고, pilot 명시 호출을 자연 호출 성공으로 세지 않는지.

이 확인이 끝나기 전에는 “Codex 호환”, “Luna가 0.1.3을 사용”, “Sol 검증자가 보고 전용 지침을
준수함” 또는 “북극성을 통과”라고 기록하지 않는다. 이번 설정의 명시적 workspace-write를 강제
read-only라고 기록하지 않는다. 조직 차원의 권한 강제를 확립하는 것은 이 실험의 목표가 아니다.
