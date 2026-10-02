# Claude Code 프로젝트별 설치

`intent-sdlc-skills-optional` **0.1.9**는 [팀 스킬 원본](../skills/) 13개와
[검증자](../agents/sdlc-verifier.md)를 플러그인으로 전달한다. 작성 스킬 3개는
같은 배포판의 `project/examples/skills/`에서 제품의 `.claude/skills/`로 따로 복사한다.
두 묶음 모두 선택 사항이다. 여기에는 Claude 전용 스킬 본문 복제본을 두지 않는다.
0.1.9의 개발건 색인과 PR·커밋 전달 기준은 같은 판의 `project/changes/README.md`와
`project/docs/CHANGE-DELIVERY.md`에서 읽는다. 플러그인은 채택한 `sdlc-feedback`의 정합성 안내를
전달하며 제품 문서나 기존 설치를 자동 갱신하지 않는다. 설치 확인은 실제 모델 행동의 검증과 구별한다.

## 준비와 설치 범위

Claude Code와 Git이 필요하다. `claude --version`, `claude plugin install --help`에서
프로젝트 설치 옵션을 확인한다. 아래 명령은 Claude Code 2.1.269의 CLI 형식을 기준으로 한다.
실제 PR 작업에는 인증된 `gh`와 해당 저장소 권한이 필요하며, 설치 확인에는 필요하지 않다.

`EDITION_SOURCE`는 `project/`, `org-skills/`, `.claude-plugin/`을 포함한 0.1.9 배포판의
절대 경로다. `PRODUCT_ROOT`는 그 `project/` 내용을 채택하고 Git을 초기화한 별도 제품이다.
설치 전에 제품의 `CLAUDE.md`, `PROJECT-POLICY.md`, `REVIEW.md`를 확인한다.
동명 프로젝트·개인 스킬이나 폐기된 기본형 플러그인이 있으면 실제 출처와 적용 범위를 살피고
제품 범위에서 충돌을 해결한다. 기존 전역 설치의 제거·갱신을 이 절차에 포함하지 않는다.

## 팀 스킬 13개

제품 루트에서 실행한다. `--scope project`는 프로젝트 활성화 설정을 저장한다.
플러그인 등록 정보와 캐시는 Claude의 사용자 설정 디렉터리에 놓일 수 있다.
임시 검증에서는 별도 `CLAUDE_CONFIG_DIR`을 지정해 실제 사용자 프로필과 분리한다.

```bash
EDITION_SOURCE=/absolute/path/to/tdd-optional
PRODUCT_ROOT=/absolute/path/to/adopted-product
(
  set -eu
  test -f "$PRODUCT_ROOT/CLAUDE.md"
  test -f "$PRODUCT_ROOT/PROJECT-POLICY.md"
  test -f "$PRODUCT_ROOT/REVIEW.md"
  cd "$PRODUCT_ROOT"
  claude plugin validate --strict "$EDITION_SOURCE/org-skills"
  claude plugin validate --strict "$EDITION_SOURCE/.claude-plugin/marketplace.json"
  claude plugin marketplace add "$EDITION_SOURCE" --scope project
  claude plugin install intent-sdlc-skills-optional@intent-sdlc-skills-optional --scope project
  claude plugin list --json
)
```

플러그인에는 `accessibility`, `brand`, `data-compliance`, `grilling`, `pr-loop`,
`sdlc-feedback`, `secrets-scan`, `secure-api-review`, `spec-policy-pass`, `stop-slop-ko`,
`tdd`, `to-questionnaire`, `ux-copy`가 있다. 검증자는 같은 플러그인의 `agents/`에 포함된다.
별도 `.claude/agents/` 복사가 필요하지 않다. 프로젝트의 기존 검증자를 쓰면
원본의 **Review criteria**와 동등한 기준을 인계한다.

## 작성 스킬 3개

채택하기로 한 경우 아래를 실행한다. 모든 입력·대상을 먼저 확인하고, 기존 설치가 있으면
복사 전에 중단한다. `SKILL.md`만 복사하면 `references/`와 `examples/`가 빠진다.

```bash
(
  set -eu
  test -f "$PRODUCT_ROOT/CLAUDE.md"
  test -f "$PRODUCT_ROOT/PROJECT-POLICY.md"
  test -f "$PRODUCT_ROOT/REVIEW.md"
  for skill in capture-intent design-spec plan; do
    test -f "$PRODUCT_ROOT/examples/skills/$skill/SKILL.md"
    test ! -e "$PRODUCT_ROOT/.claude/skills/$skill"
  done
  mkdir -p "$PRODUCT_ROOT/.claude/skills"
  for skill in capture-intent design-spec plan; do
    cp -R "$PRODUCT_ROOT/examples/skills/$skill" "$PRODUCT_ROOT/.claude/skills/$skill"
  done
)
```

작성 스킬 3개와 팀의 `to-questionnaire`는 `disable-model-invocation: true`를 유지한다.
다른 팀 스킬은 설명에 맞는 업무에서 선택되며, TDD는 사용자나 현재 plan이 선택한 범위에만 적용한다.

## 명시 호출과 출처 확인

제품 루트에서 새 Claude 세션을 열어 다음 이름으로 호출한다. 작성 스킬의 인자는 현재 의도·설계나
작업 경로를 문장으로 전달한다. 팀 스킬은 플러그인 이름을 붙여 동명 개인 스킬과 구별한다.

| 대상 | Claude Code | Codex의 같은 스킬 |
|---|---|---|
| 의도 기록 | `/capture-intent` | `$capture-intent` |
| 요구·설계 | `/design-spec` | `$design-spec` |
| 구현 계획 | `/plan` | `$plan` |
| 팀 스킬 | `/intent-sdlc-skills-optional:<skill-name>` | `$<skill-name>` |
| 예: 명시 질문지 | `/intent-sdlc-skills-optional:to-questionnaire` | `$to-questionnaire` |
| 예: PR 후속 작업 | `/intent-sdlc-skills-optional:pr-loop 123` | `$pr-loop`와 PR 번호 `123`을 요청에 명시 |

독립 검토는 `sdlc-feedback`이 채택된 업무에서 플러그인의 `sdlc-verifier`에 맡긴다.
새 문맥·실제 기준 읽기·보고 반환과 주 세션의 결과 수신을 확인한다. 검증자는 보고만 하며
인수나 병합을 대신하지 않는다. 모델·권한 설정은 도구별로 다르다.
[Codex 안내](../codex/README.md)는 같은 기준의 TOML 전달과 버전별 위임 한계를 설명한다.

설치 목록의 판·범위와 원본 경로, 설치본 파일 해시를 확인한다. 작성 스킬은 제품 경로,
팀 스킬·검증자는 실제 플러그인 로드 경로를 기준으로 비교한다. 목록에 이름이 보이는 것,
명시 호출로 본문·참고 자료를 읽은 것, 실제 업무에서 지침을 적용한 것은 각각 별도 근거다.
네 명시 전용 스킬은 자연 선택을 통과 조건으로 삼지 않는다. 파일·manifest 검사만 했다면
모델 호출·검토 행동은 미검증으로 남긴다.

## 기존 설치 갱신

설치 당시 소스 판·Git SHA 또는 파일 해시, 현재 설치본의 로컬 변경을 먼저 보존한다.
새 배포판은 별도 위치에서 검증하고, 작성 스킬 전체 폴더와 팀 플러그인의 이전 소스→새 소스
변경을 비교한다. 작성 스킬은 그 변경만 제품의 `examples/skills/`와 `.claude/skills/`에 병합한다.
로컬 참고 자료·프로젝트 정책과 팀이 선택한 호출 정책도 함께 보존한다.
제품 루트·`.claude/` 전체를 새 템플릿으로 덮어쓰지 않는다.

팀 플러그인의 로컬 수정이 있으면 먼저 관리하는 플러그인 소스에 병합한다. 캐시 편집만으로
유지되는 변경은 update가 보존하지 않는다. 검증된 로컬 marketplace source를 갱신한 뒤 제품에서
`claude plugin update intent-sdlc-skills-optional@intent-sdlc-skills-optional --scope project`를 실행한다.
프로젝트 정책·권한·기존 검증자 설정은 별도로 비교·병합한다. 새 세션에서 판·실제 출처를 다시 확인한다.

호출과 폴더 규칙은 [Claude 스킬 문서](https://code.claude.com/docs/en/skills),
설정·캐시 범위는 [설정 문서](https://code.claude.com/docs/en/settings)를 참고한다.
