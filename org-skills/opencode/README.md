# OpenCode 실험용 팀 자료 전달

이 디렉터리는 팀의 Claude용 원본을 바꾸지 않고 OpenCode 프로젝트에 전달하기 위한 얇은
어댑터다. 설치 스크립트, 의미 검사기, 전역 설정은 포함하지 않는다. 원본 폴더를 판이 고정된
Git 객체에서 통째로 복사하고, 플랫폼 계약이 다른 두 스킬과 세 작성 예시에 작은 patch만 적용한다.

## 원본 판과 배포 범위

| 구분 | 고정 판 | 사용 내용 |
|---|---|---|
| 팀 스킬 | `9b7772f0fe0704b98bd00467525cf42f0a58f1a1`, Claude plugin `0.1.5` | `org-skills/skills/`의 13개 폴더와 원본 verifier |
| 사용 템플릿 | `d4d2153188743eb4f1bb30693b5c17afdaa0f999` | `examples/skills/`의 작성 예시 3개 |
| OpenCode 어댑터 | 이 디렉터리를 포함하는 배포 커밋 | verifier 전체 변환본, patch 3개, 자료 색인 |

조건 A는 native skill 14개와 직접 읽는 파일 자료 2개를 제공한다.

- `.opencode/skills/`: `brand`, `data-compliance`, `secure-api-review`,
  `spec-policy-pass`, `tdd`, `stop-slop-ko`, `accessibility`, `secrets-scan`,
  `grilling`, `sdlc-feedback`, `ux-copy`
- `.claude/skills/`: 사용판 작성 예시 `capture-intent`, `design-spec`, `plan`.
  OpenCode가 발견할 프로젝트 경로로 명시 채택하되 기존 프로젝트 상대 링크를 유지한다.
- `team-resources/skills/`: 자동 발견 경로에서 뺀 `to-questionnaire`, `pr-loop`.
  전자는 사용자가 질문지를 명시적으로 원할 때, 후자는 실제 hosted PR 업무일 때 직접 읽는다.
- `.opencode/agents/sdlc-verifier.md`: `sdlc-feedback`이 사용하는 독립 보고 전용 검증자.
- `team-resources/INDEX.md`: 자료 위치와 용도만 알려 주는 온보딩 색인.

폴더 복사는 `SKILL.md`만 떼어 내지 않는다. `references/`, `examples/`, `plays/`,
`templates/`, `LICENSE*`, `PROVENANCE.md`, `CONNECTORS.md`를 포함한 모든 동반 자원을 보존한다.
보조 스캐너, MCP, 외부 서비스와 Claude hook은 이 전달 자료가 설치하지 않는다.

## OpenCode 변환 내역

| 파일 | 원본 | 변환 |
|---|---|---|
| `agents/sdlc-verifier.md` | 팀 verifier, SHA-256 `dc01c7a33f89da0863e1f1441430975dc9247039f9725cbc94d1b075ba6c91e3` | Review criteria 본문 보존. `mode: subagent`, `steps: 20`; `edit/write/task/skill` 비활성화와 `edit/task` 거부; 검사 Bash 허용 |
| `patches/sdlc-feedback.patch` | 팀 `sdlc-feedback/SKILL.md`, SHA-256 `a0096145d0263a1e2edf8bb6d4e838ee3039608e5bcb7eb338740a3a7d1cfd35` | Claude plugin 한정 agent 이름을 `sdlc-verifier`로 바꾸고 OpenCode 모델 선택 책임을 프로젝트로 돌림 |
| `patches/ux-copy.patch` | Anthropic 채택 원문, SHA-256 `d46a00a62ec637e9ca9d5f7823ea3e0a4ec26dffc53bb5035f59b48ebfcdcde7` | `$ARGUMENTS` 대신 현재 요청을 읽고, 동반 `CONNECTORS.md` 링크와 실제 연결 여부를 사용하도록 조정; 원본 provenance에 변환 사실 추가 |
| `patches/authoring-native.patch` | 사용판 `examples/skills/` 3개 | `disable-model-invocation: true` 세 줄 제거 |

`disable-model-invocation`은 이 세 예시가 원래 발견 경로 밖의 수동 선택 자료였다는 Claude용
표시다. 이번 실험은 세 예시를 native 경로에 명시 채택하므로 OpenCode가 지원하지 않는 필드를
그대로 남겨 제어가 유지된 것처럼 보이지 않게 제거한다. `to-questionnaire`는 수동 사용 의도를
유지하기 위해 native 경로로 옮기지 않으며 원본 frontmatter도 바꾸지 않는다.

검증자의 `model`과 variant/reasoning 항목은 의도적으로 비웠다. 설치 대상 프로젝트가 실제로
연결된 provider/model ID와 지원 옵션을 확인해 프로젝트 설정과 실행 기록에서 확정한다.
특정 `github-copilot/...` 또는 Claude 모델 이름을 이 배포물이 추측하지 않는다.

검증자에는 `read: allow` 같은 와일드카드 권한을 추가하지 않았다. 프로젝트의 기존 `.env`와
비밀 파일 읽기 제한을 상속해야 하며, agent 뒤쪽의 넓은 allow가 이를 덮을 수 있기 때문이다.
`bash: allow`는 시험과 조회를 가능하게 할 뿐 셸을 기계적으로 읽기 전용으로 만들지 않는다.
본문의 보고 전용 지침과 프로젝트 권한을 함께 적용한다.

## 수동 설치

아래 명령은 이 Git 저장소와 깨끗한 실험 제품 디렉터리가 로컬에 있고, 나열한 대상 경로가
아직 없다는 전제다. 기존 파일이 있다면 먼저 출처와 로컬 변경을 대조하고 별도로 보존한다.

```bash
export OC_SOURCE=/absolute/path/to/ai-native-sdlc-sample
export OC_TARGET=/absolute/path/to/experiment-product
export OC_TEAM_REV=9b7772f0fe0704b98bd00467525cf42f0a58f1a1
export OC_TEMPLATE_REV=d4d2153188743eb4f1bb30693b5c17afdaa0f999

git -C "$OC_SOURCE" cat-file -e "$OC_TEAM_REV^{commit}"
git -C "$OC_SOURCE" cat-file -e "$OC_TEMPLATE_REV^{commit}"

mkdir -p "$OC_TARGET/.opencode/skills" "$OC_TARGET/.opencode/agents"
mkdir -p "$OC_TARGET/.claude/skills" "$OC_TARGET/team-resources/skills"

git -C "$OC_SOURCE" archive "$OC_TEAM_REV" \
  org-skills/skills/brand \
  org-skills/skills/data-compliance \
  org-skills/skills/secure-api-review \
  org-skills/skills/spec-policy-pass \
  org-skills/skills/tdd \
  org-skills/skills/stop-slop-ko \
  org-skills/skills/accessibility \
  org-skills/skills/secrets-scan \
  org-skills/skills/grilling \
  org-skills/skills/sdlc-feedback \
  org-skills/skills/ux-copy \
  | tar -x -C "$OC_TARGET/.opencode/skills" --strip-components=2

git -C "$OC_SOURCE" archive "$OC_TEMPLATE_REV" \
  examples/skills/capture-intent \
  examples/skills/design-spec \
  examples/skills/plan \
  | tar -x -C "$OC_TARGET/.claude/skills" --strip-components=2

git -C "$OC_SOURCE" archive "$OC_TEAM_REV" \
  org-skills/skills/to-questionnaire \
  org-skills/skills/pr-loop \
  | tar -x -C "$OC_TARGET/team-resources/skills" --strip-components=2

cp "$OC_SOURCE/org-skills/opencode/agents/sdlc-verifier.md" \
  "$OC_TARGET/.opencode/agents/sdlc-verifier.md"
cp "$OC_SOURCE/org-skills/opencode/team-resources/INDEX.md" \
  "$OC_TARGET/team-resources/INDEX.md"

patch -d "$OC_TARGET/.opencode/skills/sdlc-feedback" -p4 \
  < "$OC_SOURCE/org-skills/opencode/patches/sdlc-feedback.patch"
patch -d "$OC_TARGET/.opencode/skills/ux-copy" -p4 \
  < "$OC_SOURCE/org-skills/opencode/patches/ux-copy.patch"
patch -d "$OC_TARGET/.claude/skills" -p3 \
  < "$OC_SOURCE/org-skills/opencode/patches/authoring-native.patch"
```

설치 뒤 OpenCode 판, 실제 provider/model/variant, `debug skill`의 14개 발견, verifier 구성 파싱,
동반 파일과 중복 이름을 기록한다. 이 확인은 설정·발견 근거다. 실제 모델이 자연어 업무에서
스킬을 선택·읽고 적용했는지, 검증자를 호출하고 기다렸는지는 작은 pilot과 본 실험에서 별도로
관측한다. 명시 호출 probe를 자연 선택 성공으로 기록하지 않는다.

## 갱신

갱신은 원본 팀 판, 사용 템플릿 판, 어댑터 판을 각각 기록한 뒤 수행한다. 기존 설치에 직접
덮어써서 로컬 수정과 출처를 섞지 않는다.

1. 설치된 16개 폴더와 verifier, INDEX의 로컬 변경을 대조하고 필요한 변경을 별도로 보존한다.
2. 새 원본 commit에서 세 patch를 dry-run한다. hunk가 맞지 않으면 원문 변화와 플랫폼 차이를
   읽고 patch와 이 문서의 SHA·변환 내역을 함께 갱신한다.
3. 세 작성 예시의 `disable-model-invocation` 상태와 프로젝트 상대 링크를 새 사용판에서 확인한다.
4. 아래 제거 범위만 비운 깨끗한 대상에 수동 설치 절차를 다시 적용한다.
5. 새 session에서 실제 로드 경로·판·중복 노출을 다시 확인한다. 기존 session이 자동으로
   새 본문을 읽었다고 가정하지 않는다.

## 제거

다음 경로만 이 배포물의 소유 범위다. 제거 전 로컬 변경을 확인하고, 팀 자료 외 다른 파일이
들어 있는 상위 `.opencode/`, `.claude/`, `team-resources/` 디렉터리는 삭제하지 않는다.

- `.opencode/skills/` 아래의 위 11개 이름
- `.claude/skills/capture-intent`, `design-spec`, `plan` — 이 배포로 설치한 경우만
- `.opencode/agents/sdlc-verifier.md`
- `team-resources/skills/to-questionnaire`, `team-resources/skills/pr-loop`
- `team-resources/INDEX.md` — 이 배포의 색인인 경우만

이 전달본 자체는 OpenCode 모델 실행, 자연어 trigger, 위임·대기, `.env` 제한의 런타임 합성,
hosted PR, 전역 사용자 설정 격리를 증명하지 않는다. 설치·파싱과 실제 수행 결과를 분리해 기록한다.
