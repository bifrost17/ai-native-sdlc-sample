# Codex 프로젝트별 설치 — tdd-optional

현재 선택판 **intent-sdlc-skills-optional 0.1.9**의 13개 팀 스킬, 제품 작성 예시 3개와 독립
검토 기준을 한 제품 repo에 설치하는 Codex adapter다. 전체 skill 폴더는 원 source에서
복사하고, 이 디렉터리는 Codex에 필요한 patch와 완성된 verifier TOML, 얇은 `AGENTS.md` 예시만 둔다.
사용자 전역 설정·설치와 maker source는 바꾸지 않는다.
0.1.9의 개발건 색인과 PR·커밋 전달 기준은 같은 판의 `project/changes/README.md`와
`project/docs/CHANGE-DELIVERY.md`에서 읽는다. 팀의 `sdlc-feedback`은 Claude 배포판과 같은
변경 정합성 기준을 전달하되 verifier 호출과 명시 호출 문법은 아래 Codex 경로를 따른다.
파일 설치 확인은 실제 모델 행동의 검증과 구별한다.

## 파일과 변환 범위

- `patches/explicit-only.patch`: `capture-intent`, `design-spec`, `plan`, `to-questionnaire`의 Claude 전용
  `disable-model-invocation`을 제거하고 각 폴더에 `agents/openai.yaml`을 추가한다.
- `patches/sdlc-feedback.patch`: verifier criteria 경로, Codex native 위임과 0.153.4의 file-read fallback,
  결과 대기·보존·child close 및 Codex model/reasoning 표현만 바꾼다.
- `patches/ux-copy.patch`: Claude command 입력과 connector placeholder를 Codex 현재 요청/실제 연결 문맥으로
  바꾸고 지원되지 않는 `argument-hint`를 제거한다.
- `patches/pr-loop.patch`: Claude의 `argument-hint`·도구 허용 목록과 명령 선실행을
  Codex의 현재 요청·실제 도구 호출로 바꾼다. PR 작업 순서·종료 조건은 유지하며 권한은 세션 설정을 따른다.
- `agents/sdlc-verifier.toml`: 원 `org-skills/agents/sdlc-verifier.md`의 Review criteria 전문을
  `developer_instructions`에 직접 넣은 Codex 파일이다. 프로젝트 진입 목록에 `AGENTS.md`만 추가한다.
- `templates/AGENTS.md`: `CLAUDE.md`와 그 참조 정책을 먼저 읽게 하고 채택한 feedback 절차만 연결한다.

Claude plugin/marketplace manifest와 command는 Codex 설치 파일이 아니다. 16개 skill은 모두
`.agents/skills/`에 놓으며 별도 `team-resources` wrapper를 만들지 않는다. 이 adapter는 제품의
`.codex/config.toml`이나 parent model, approval, sandbox, memory, plugin/MCP 설정을 정하지 않는다.

## 새 제품 repo에 설치

Codex CLI, Git, `patch`가 필요하다. 실제 PR 작업에는 인증된 `gh`와 저장소 권한이 필요하다.
`codex --version`으로 실제 판을 확인한다. [공식 스킬 문서](https://developers.openai.com/codex/skills/)의
프로젝트 경로와 명시 호출 정책을 사용한다. 동명 개인·상위 프로젝트 스킬이 있으면 실제 출처와
현재 프로젝트의 선택을 확인한다. 설치가 전역 동명 스킬을 제거하지는 않는다.

`SDLC_PACKAGE`는 선택한 0.1.9의 `tdd-optional/org-skills` 절대 경로이고, `CODEX_ADAPTER`는
그 package의 `codex/` 경로다. `CODEX_TARGET`에는 같은 판의 `project/` 내용이 이미
복사돼 있어야 한다. 다음 명령은 깨끗한 대상용이며 기존 설치가 있으면 중단한다.

```bash
SDLC_PACKAGE=/absolute/path/to/tdd-optional/org-skills
CODEX_ADAPTER="$SDLC_PACKAGE/codex"
CODEX_TARGET=/absolute/path/to/adopted-product
(
  set -eu
  test -f "$SDLC_PACKAGE/.claude-plugin/plugin.json"
  test -f "$CODEX_TARGET/CLAUDE.md"
  test -f "$CODEX_TARGET/PROJECT-POLICY.md"
  test -f "$CODEX_TARGET/REVIEW.md"
  test ! -e "$CODEX_TARGET/.agents/skills"
  test ! -e "$CODEX_TARGET/.codex/agents/sdlc-verifier.toml"
  test ! -e "$CODEX_TARGET/AGENTS.md"
  for skill in accessibility brand data-compliance grilling pr-loop sdlc-feedback \
    secrets-scan secure-api-review spec-policy-pass stop-slop-ko tdd to-questionnaire ux-copy; do
    test -f "$SDLC_PACKAGE/skills/$skill/SKILL.md"
  done
  for skill in capture-intent design-spec plan; do
    test -f "$CODEX_TARGET/examples/skills/$skill/SKILL.md"
  done
  mkdir -p "$CODEX_TARGET/.agents/skills" "$CODEX_TARGET/.codex/agents"
  for skill in accessibility brand data-compliance grilling pr-loop sdlc-feedback \
    secrets-scan secure-api-review spec-policy-pass stop-slop-ko tdd to-questionnaire ux-copy; do
    cp -R "$SDLC_PACKAGE/skills/$skill" "$CODEX_TARGET/.agents/skills/$skill"
  done
  for skill in capture-intent design-spec plan; do
    test -f "$CODEX_TARGET/examples/skills/$skill/SKILL.md"
    cp -R "$CODEX_TARGET/examples/skills/$skill" "$CODEX_TARGET/.agents/skills/$skill"
  done
  patch --batch -d "$CODEX_TARGET" -p1 < "$CODEX_ADAPTER/patches/explicit-only.patch"
  patch --batch -d "$CODEX_TARGET" -p1 < "$CODEX_ADAPTER/patches/sdlc-feedback.patch"
  patch --batch -d "$CODEX_TARGET" -p1 < "$CODEX_ADAPTER/patches/ux-copy.patch"
  patch --batch -d "$CODEX_TARGET" -p1 < "$CODEX_ADAPTER/patches/pr-loop.patch"
  cp "$CODEX_ADAPTER/agents/sdlc-verifier.toml" "$CODEX_TARGET/.codex/agents/sdlc-verifier.toml"
  cp "$CODEX_ADAPTER/templates/AGENTS.md" "$CODEX_TARGET/AGENTS.md"
)
```

기존 `AGENTS.md`가 있는 제품은 덮어쓰지 말고 `templates/AGENTS.md`의 두 의미를 기존 지침에 합친다.
갱신할 때는 이전 소스 판·설치 해시와 로컬 변경을 먼저 보존한다. 새 소스를 임시 제품에 복사해
patch 적용을 확인하고, 이전→새 소스의 변경만 기존 설치에 병합한다. `references/`·`examples/` 등
전체 폴더를 비교하며 로컬 참고 자료와 선택한 호출 정책을 유지한다. `CLAUDE.md`, `PROJECT-POLICY.md`,
기존 `AGENTS.md`·검증자 설정을 새 템플릿으로 통째로 덮어쓰지 않는다. 출처·판·대상 해시를 갱신한다.

## 명시 호출

제품에서 `$capture-intent`, `$design-spec`, `$plan` 뒤에 현재 작업과 문서 경로를 적는다.
팀 스킬도 `$sdlc-feedback`, `$to-questionnaire`처럼 `$<skill-name>`으로 지정한다.
`$pr-loop`에는 PR 번호·URL·브랜치를 요청에 적으며, 생략하면 현재 브랜치 PR을 사용한다.
네 명시 전용 스킬의 `agents/openai.yaml`은 `allow_implicit_invocation: false`를 유지한다.
TDD는 사용자나 현재 plan이 선택한 부분에만 적용한다.
[Claude 대응 호출표](../claude/README.md#명시-호출과-출처-확인)는 같은 16개 스킬의 이름을 비교한다.

## native verifier 사용과 확인

Codex 0.153.4에서 0032 P1이 관측한 native spawn 입력은 `message`, `model`, `reasoning_effort`,
`fork_context`, `items`였고 named custom-agent selector는 없었다. 따라서 이 판에서는 fresh native child를
`gpt-5.6-sol`/`high`, `fork_context=false`로 열고, 최소 인계와 함께
`.codex/agents/sdlc-verifier.toml`을 읽어 그
`developer_instructions`를 적용하라고 명시한다. 결과를 기다려 받아 보존한 뒤 child를 닫고 이력은
지우지 않는다. 0032의 첫째·둘째 child는 이 방식으로 파일을 읽고 보고했으나 role metadata는 `null`이었다.

이 fallback은 criteria 본문 전달을 확인하는 방법이다. TOML의 named custom-agent 설정이 선택됐거나
role이 적용됐다는 증거는 아니다. 현재 runtime이 named selector를 제공하면 실제 schema와 반환 metadata를
확인한 뒤 그 경로를 사용할 수 있다. 다른 Codex 판·호스트에서는 다시 검증한다.

진행 상태와 결과는 native wait로 확인한다. `send_input`은 새 메시지를 보내는 동작이므로 이미 끝난
child를 다시 시작할 수 있다. 0032의 JSON 검토에서는 완료 보고를 받은 뒤 불필요한 재개와 close 뒤
조회가 겹쳤다. 반환된 검토 보고와 후속 도구 상태를 구별하며, 완료한 child를 닫은 뒤 추가 대기는 필요 없다.

설치 후에는 16개 source/target 경로와 파일 hash, 네 patch, verifier/AGENTS hash를 보존한다.
네 explicit-only skill은 기본 자연 catalog에 없을 수 있으므로 설치 inventory와 명시 호출로 확인한다.
나머지 catalog 이름만으로 본문 읽기·자연 선택·검토 수행을 통과 처리하지 않는다. 실제 작은 작업에서
fresh child, criteria 읽기, 보고 반환, parent 대기, close와 프로젝트 무변경을 따로 관측한다.

Codex CLI 0.153.4의 위 전달 방식은 source 0.1.3으로 관측했고, 현재 전달판은 같은 방식으로
source 0.1.9의 설계·계획 검토와 추적·커밋·인계 기준을 제공한다. 0.1.8에서 `pr-loop`의 Claude 전용
입력·선실행 문법 변환과 임시 설치를 확인했다. 0.1.9의 새 지침에 대한 실제 모델 행동은 확인하지 않았다.
실제 hosted PR 수정·push·댓글, 다른 Codex 버전,
조직 전역 설치와 장기 운영은 이번 확인에 포함하지 않았다.

실제 설치판과 공개 실행 범위·실패·HUMAN의 보완은 maker의
[0032 실행 기록](../../../docs/experiments/0032-codex-luna-run.md)에 보존한다. 이 링크는 maker 내
참고이며 선택판 폴더만 복사한 설치에서는 필요하지 않다. 제품 정책은 그대로이며 원 스킬 기준의
0.1.4 변경은 intent 제약과 상위 문서 참조의 비교를 명확히 한 것이다.
