# OpenCode 스킬 설치 호환성 검토

검토일: 2026-09-11. 대상은 설치된 **OpenCode 1.18.30**과 팀 Claude 플러그인 **0.1.5**다.
팀 소스는 `9b7772f0fe0704b98bd00467525cf42f0a58f1a1`,
실사용 템플릿은 `codex/use-template-0024-r2@d4d2153188743eb4f1bb30693b5c17afdaa0f999`로 고정했다.

**스킬 본문은 대부분 재사용할 수 있다. Claude 플러그인 전체를 그대로 설치하는 방식은 실패한다.**
스킬 13개 복사본의 발견·본문 반환은 성공했지만, Claude용 검증자 파일까지 그대로 복사하면
OpenCode 설정 오류가 발생했다. 검증자의 설정 형식과 호출 이름을 바꾼 임시본은 등록에 성공했다.

이번 범위는 설치 검토다. 임시 프로젝트에서 CLI의 설정·발견 명령만 실행했다.
영구 설치, 활성 스킬/템플릿 수정, 모델 호출, 제품 구현 실험은 하지 않았다.
등록 성공은 실제 에이전트의 스킬 선택·수행 또는 검증자 위임 성공을 뜻하지 않는다.

2026-09-12 후속: [OpenCode 템플릿 실험 설계](experiment/README.md)를 작성했다.
native 14개와 파일 참조 2개를 제공하는 전체 F04 1회 및 필요한 부분 재시험 계획이며 아직 시작하지 않았다.

## 판단 기준

[북극성](../../verification/north-star-playbook.html)의 L3·L6·L8·L9를 기준으로,
팀 정책을 필요한 단계에서 읽고 적용하며, 현재 합의·설계·계획·실행을 대조하는 역할을 유지한다.
도구를 바꾼다고 별도 SDLC나 문서 검사 프로그램을 추가하지 않는다.
사람의 판단과 가벼운 정책을 유지하고, 플랫폼별 설치·호출 계약만 조정하는 방향이다.

## 현재 설치 상태와 실제 확인

| 확인 대상 | 결과 | 의미 |
|---|---|---|
| 현재 maker 프로젝트의 정상 `opencode debug skill` | 6개: 내장 1, 전역 aside-browser 1, 프로젝트 4 | `.claude/skills`는 읽는다. Claude 마켓플레이스에 설치한 `org-skills`는 이 목록에 없다 |
| 팀 `skills/` 전체 → 임시 `.opencode/skills/` | 팀 13개 모두 발견, 반환 본문과 소스 본문 일치 | Markdown 로딩 호환성 확인. frontmatter 실행 의미까지 확인한 것은 아니다 |
| 위 구성 + 원본 `agents/sdlc-verifier.md` | 종료 코드 1 | `tools: Read, Glob, Grep, Bash` 문자열을 OpenCode가 거부 |
| OpenCode 형식의 임시 검증자 + 호출 이름 수정 | 팀 13개 발견, 검증자 `mode: subagent`, `steps: 20`으로 등록 | 얇은 설정 변환으로 구성 오류 해결 가능 |
| 원본 `commands/spec-policy.md` → 임시 `.opencode/commands/` | 명령 등록 성공, `$1`이 template에 보존됨 | 실제 인자 치환·모델 실행은 아직 시험하지 않음 |

현재 프로젝트의 4개는 `capture-intent`, `design-spec`, `plan`, `secure-api-review`다.
여기의 마지막 스킬은 프로젝트 복사본이며, 팀 플러그인 설치 경로가 발견됐다는 뜻은 아니다.
임시 디렉터리는 독립 Git 프로젝트지만 사용자 전역 설정은 계속 적용된다.
전역 aside-browser가 보였으므로 완전히 격리된 사용자 환경으로 표현하지 않는다.

원본 검증자 복사의 실제 오류:

```text
Configuration is invalid at .../.opencode/agents/sdlc-verifier.md
↳ Expected object | undefined, got "Read, Glob, Grep, Bash" tools
```

증거: [현재 상태](evidence/current.json), [복사 실험](evidence/discovery.json),
[임시 변환본](evidence/native-draft.json), [명령 등록](evidence/command.json).
초기 PIPE 출력 수집은 UTF-8 해독 오류로 실패했다. stdout을 파일로 직접 받은 재실행 결과를 사용했다.
실패한 수집에서 호환성 결과를 추정하지 않았다.

## 필요한 조정

### 스킬과 플러그인 구분

OpenCode는 프로젝트 `.opencode/skills/`뿐 아니라 `.claude/skills/`, `.agents/skills/`와
대응 전역 경로를 지원한다. 다만 Claude의 marketplace/plugin manifest가 OpenCode 설치 파일이 되는 것은 아니다.
OpenCode의 plugin은 별도의 JS/TS 또는 npm 확장 방식이다. 이번 용도에는 새 실행 플러그인까지 만들 필요가 없다.
[Skills](https://opencode.ai/docs/skills/), [Plugins](https://opencode.ai/docs/plugins/).

폴더 전체를 복사해 `references/`, `plays/`, `templates/`, LICENSE와 PROVENANCE를 보존한다.
소스 0.1.5에서 변환했다면 원본 SHA와 변환 내역도 기록한다. 수정된 복사본을 원본과 동일한 판이라고만 표시하지 않는다.

### 완료 검증자와 sdlc-feedback

`sdlc-feedback`은 `../../agents/sdlc-verifier.md`를 읽는다.
스킬만 설치하면 이 기준 파일이 빠진다. `.opencode/skills/sdlc-feedback/`와
`.opencode/agents/sdlc-verifier.md`를 함께 배치하면 상대 경로를 유지할 수 있다.

검증자에는 OpenCode의 `mode: subagent`, `steps`, `permission` 형식을 사용하고,
스킬의 Claude 한정 이름 `intent-sdlc-skills:sdlc-verifier`를 실제 등록명 `sdlc-verifier`로 맞춘다.
원본의 검토 기준과 보고 전용 역할은 유지한다. 모델은 실제 제공자의 모델 ID와 지원 추론 옵션으로 지정해야 한다.
Claude의 `model: opus`, `effort: high`, `maxTurns`가 그대로 적용된다고 가정하지 않는다.
[Agents](https://opencode.ai/docs/agents/).

[임시 변환 diff](probes/native-draft.patch)는 **설정 파싱 확인용**이다.
모델·추론은 지정하지 않아 부모 설정 상속 상태만 확인했다. Bash 허용은 셸의 쓰기를 차단하지 않으며,
이 초안의 read 허용도 기존 세부 권한과 합쳐지는 결과를 검토해야 한다.
실제 배포 설정으로 승인된 파일이 아니다. 최종 설치 시 프로젝트 권한을 존중하고,
개발은 적정 비용, 중요한 교차 문서 검토는 더 높은 역량을 선택한다는 기존 원칙을 구체화한다.

### 명령 인자와 호출 제한

OpenCode가 인정하는 스킬 frontmatter는 `name`, `description`, `license`,
`compatibility`, `metadata`다. 다른 필드는 무시하므로
`disable-model-invocation` 또는 `allowed-tools`를 복사해도 Claude의 제어 의미가 보존되지 않는다.
특히 `to-questionnaire`와 사용판 작성 예시 3개에는 명시 선택용 설정이 있다.
의도적으로 스킬로 활성화할지, 수동 명령으로 제공할지 설치 시 구분해야 한다.
[Skills](https://opencode.ai/docs/skills/).

`$ARGUMENTS`, `$1` 및 느낌표 뒤 backtick으로 감싼 셸 명령은 OpenCode의 **명령 템플릿**에서도 지원한다.
이 구문 자체를 Claude 전용으로 판단하면 안 된다.
다만 `pr-loop`·`ux-copy`를 일반 스킬로 복사했을 때 명령과 같은 전처리가 일어난다고 보장할 수 없다.
명령 진입점으로 옮기거나 본문에서 실제 입력과 실행 절차를 읽도록 조정한다.
`spec-policy`는 원문 그대로 명령 등록에 성공했고, `argument-hint`는 해석된 설정에 남지 않았다.
[Commands](https://opencode.ai/docs/commands/).

### 작성 스킬은 실사용 템플릿의 예시에서 선택

실제 제품 실험에는 maker의 `.claude/skills/`를 복사하지 않는다.
maker 전용 시험·수정 관행이 들어 있기 때문이다. 사용판의 다음 예시를 명시적으로 선택한다.

- `examples/skills/capture-intent/`
- `examples/skills/design-spec/`
- `examples/skills/plan/`

선택한 폴더를 실험 프로젝트의 `.claude/skills/`에 두면 기존 프로젝트 상대 링크를 유지하면서
OpenCode도 발견할 수 있다. `.opencode/skills/`도 깊이가 같지만 기존 다른 문서의 경로 인용까지 확인해야 한다.
전역으로 옮기면 `../../../templates/` 등의 프로젝트 연결이 깨지므로 작성 예시는 프로젝트 범위가 적합하다.
세 예시의 `disable-model-invocation: true`를 OpenCode가 강제한다고 표시하지 않는다.

현재 사용판에는 활성 스킬이 없다. 선택 설치는 파생 실험 브랜치에서 하고, 깨끗한 사용판에는
기존대로 예시만 남긴다. OpenCode 1.18 계열의 프로젝트 지침은 AGENTS.md 우선, CLAUDE.md 대체 읽기를
지원하므로 이번 설치 때문에 지침 전체를 일괄 개명할 필요도 없다.
[Rules](https://opencode.ai/docs/rules/).
버전 2 문서와 이번에 설치된 1.18.30의 동작은 섞어 해석하지 않았다.

## 권장 첫 설치 범위

1. 실험에서 선택한 작성 예시 3개를 프로젝트 범위에 활성화한다.
2. `spec-policy-pass`, `tdd`, `sdlc-feedback`과 OpenCode용 검증자를 묶고,
   개발건에 해당하는 `brand`, `data-compliance`, `secure-api-review` 등을 함께 선택한다.
   정책 스킬이 읽는 프로젝트 정책 파일도 실제 값으로 준비한다.
3. `pr-loop`, `ux-copy`, `to-questionnaire`는 위 호출 차이를 정리한 뒤 포함한다.
   나머지 일반 도구도 개발건에 필요할 때 선택한다. 모든 스킬 사용을 요구하지 않는다.
4. 설치를 구현할 때는 소스·변환 파일·설치/갱신/제거 안내와 실제 설치 경로·판을 저장소에 함께 제공한다.
   우선 프로젝트 범위에서 검증하면 서로 다른 에이전트 실험을 비교하기 쉽다.
   사용자 전역 설정을 변경해야만 하는 구조나 별도 검증 프로그램은 필요하지 않다.

이는 후속 작업 권고이며 이번 턴에서 설치 패키지를 완성하거나 영구 설치한 것은 아니다.

## 기존 자료의 제한과 독립 리뷰 보정

[독립 소스 리뷰](reviews/source-review.md)는 gpt-5.6-sol/high로 수행한 읽기 전용 검토 원문이다.
실제 CLI 결과와 원본 출처를 대조해 다음과 같이 보정했다.

- 리뷰의 작성 스킬 분석은 maker 파일 대상이었다. 제품에는 위 사용판 예시를 적용한다.
- `spec-policy`의 `$1`과 OpenCode 명령의 인자·셸 구문은 지원된다. 바꿔야 할 것은
  스킬/명령의 실행 문맥이며, 모든 변수 구문을 새로 만드는 것이 아니다.
- OpenCode는 서브에이전트를 지원한다. `grilling`의 환경 조사 위임을 이유 없이 약화하지 않고,
  실제 위임은 후속 실행에서 확인한다.
- `ux-copy`의 `../../CONNECTORS.md` 연결 문제와 `accessibility`의 미포함
  `web-quality-audit` 연결은 기존 PROVENANCE에 이미 기록돼 있다. 새 OpenCode 회귀가 아니다.
  필요한 경우 수정 출처를 남긴 복사본에서 상대 경로를 바로잡고 선택 리소스의 부재를 명시한다.
- `secrets-scan`의 `data/opencre/README.md` 안내도 현재 패키지에 없는 보조 자료다.
  기본 스캔에 필요한 plays/templates는 존재한다. 설치 과정에서 외부 스캐너를 자동 설치하지 않는다.
- 원본에서 예시로만 둔 brand 검사기나 의도적으로 제거한 secure-api-review 검사기를 새로 만들지 않는다.

## 후속 실행에서 확인할 것

설치 구성 검토는 완료했다. 실제 사용 호환성 판정은 다음 증거가 있어야 한다.

- 새 OpenCode 세션이 선택한 스킬 본문과 판을 실제로 읽고, 관련 단계의 결과물에 적용하는가.
- 구현 전에 의미 있는 RED를 확인하고 GREEN과 회귀 근거를 남기는가.
- 변경·커밋 준비 때 연결 설계와 plan을 갱신하고 같은 관련 커밋에 포함하는가.
- 완료 전 독립 검증자를 실제 호출하고 기다리며, 최신 합의·변경·시험을 전달하고 발견을 보완하는가.

이때 기존 소규모 데이터셋과 HUMAN↔AGENT 대화를 사용한다.
발견 목록이나 이번 설정 성공만으로 북극성 주석을 통과로 올리지 않는다.

## 이번 문서 변경 검증

근거 JSON 4개 파싱, 보고서 내부 파일 링크, Git 공백 검사를 확인했다.
저장소 기본 검사 [make check 출력](evidence/make-check.txt)은 종료 코드 0이다.
Python 96개 중 1개 skip, 나머지 통과; hook 28개, eval 도구 검사 8개, 관리형 설정 검사 통과.
이 검사는 OpenCode의 실제 모델 동작을 검증하지 않는다.
