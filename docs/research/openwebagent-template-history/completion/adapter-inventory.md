# 0.1.9 작성·feedback 스킬 경로와 패키지 검사 목록

검사 기준은 `4a84596c37496deb1055bd528b94fb6abd5dea75`의 추적 파일이다. `ec47695` 이후 `tdd-optional/`의 변경은 `git diff --name-status ec47695..4a84596 -- tdd-optional`에서 없었다. 현재 루트에는 별도 미커밋 WIP가 있으므로 이 목록은 이를 배포판 변경으로 간주하지 않는다. 아래 경로는 저장소 루트 상대 경로다.

## 유지하는 정본과 경로

| 의미 | 정본·동반 자료 | 설치 시 경로 |
|---|---|---|
| spec 문서 양식 | `tdd-optional/project/templates/spec.md`; 작성 깊이·추적·예시는 `project/examples/skills/design-spec/references/`, `project/docs/sdlc-authoring/`, `project/docs/sdlc-authoring/traceability.md` | 채택 제품의 `templates/spec.md` 등 `project/` 전체 내용 |
| plan 문서 양식 | `tdd-optional/project/templates/plan.md`; 실행 상세·예시는 `project/examples/skills/plan/references/`, `project/examples/skills/plan/examples/`, `project/docs/sdlc-authoring/` | 채택 제품의 `templates/plan.md` 등 |
| `design-spec` 작성 스킬 | `tdd-optional/project/examples/skills/design-spec/SKILL.md`와 전체 `references/`, `examples/` 폴더 | Claude: 제품 `.claude/skills/design-spec/`; Codex: 제품 `.agents/skills/design-spec/` |
| `plan` 작성 스킬 | `tdd-optional/project/examples/skills/plan/SKILL.md`와 전체 `references/`, `examples/` 폴더 | Claude: 제품 `.claude/skills/plan/`; Codex: 제품 `.agents/skills/plan/` |
| `sdlc-feedback` 팀 스킬 | `tdd-optional/org-skills/skills/sdlc-feedback/SKILL.md`, `PROVENANCE.md`; 공통 검토 기준은 `tdd-optional/org-skills/agents/sdlc-verifier.md` | Claude: `intent-sdlc-skills-optional` 플러그인의 `skills/sdlc-feedback/`·`agents/sdlc-verifier.md`; Codex: 제품 `.agents/skills/sdlc-feedback/`와 `.codex/agents/sdlc-verifier.toml` |

`spec`은 별도 제품 스킬명이 아니라 `design-spec`이 `templates/spec.md`를 읽어 작성하는 산출물이다. 제품 `project/`는 `examples/skills/`를 포함하지만 활성 `.claude/skills`, `.agents/skills`, 훅을 설치하지 않는다. 세 작성 스킬 중 `capture-intent`도 같은 복사 절차의 구성원이다.

제작 저장소의 `.claude/skills/design-spec/SKILL.md`와 `.claude/skills/plan/SKILL.md`는 위 제품 정본으로 보내는 얇은 maker 라우터다. `.claude/commands/spec.md`는 maker의 spec 명령이다. 제품 패키지에 이 루트 명령·라우터를 복사하지 않는다. 루트 `.claude-plugin/marketplace.json`과 `tdd-optional/.claude-plugin/marketplace.json`은 모두 0.1.9의 `tdd-optional/org-skills`를 가리키며, `tdd-optional/org-skills/.claude-plugin/plugin.json`이 실제 플러그인 manifest다.

## 도구별 설치·변환

Claude 설치 안내의 정확한 위치는 `tdd-optional/org-skills/claude/README.md`다. 제품 `CLAUDE.md`, `PROJECT-POLICY.md`, `REVIEW.md`를 확인한 뒤 `claude plugin validate --strict`를 플러그인 폴더와 배포판 marketplace에 수행한다. 프로젝트 범위 marketplace 추가와 플러그인 설치 후 `claude plugin list --json`으로 범위와 판을 확인한다. 작성 스킬은 `product/examples/skills/{capture-intent,design-spec,plan}` 전체를 각각 `product/.claude/skills/`에 복사하며 이미 있으면 멈춘다. 명시 호출은 `/design-spec`, `/plan`, `/intent-sdlc-skills-optional:sdlc-feedback`이다. 플러그인의 verifier는 별도 `.claude/agents/` 복사를 요구하지 않는다. 팀이 feedback을 채택했다는 프로젝트 지침 예시는 `tdd-optional/org-skills/examples/sdlc-feedback-adoption.md`에 있으며 자동 적용을 뜻하지 않는다.

Codex 설치 안내는 `tdd-optional/org-skills/codex/README.md`다. 같은 제품 `project/` 내용이 먼저 있어야 한다. 13개 팀 스킬 전체를 `product/.agents/skills/`로, 세 작성 스킬 전체를 `product/examples/skills/`에서 `product/.agents/skills/`로 복사한 다음 루트 상대 `patch -p1`로 `explicit-only.patch`, `sdlc-feedback.patch`, `ux-copy.patch`, `pr-loop.patch`를 적용한다. 관련 두 패치는 `tdd-optional/org-skills/codex/patches/`에 있다. `explicit-only.patch`는 `design-spec`과 `plan`의 Claude 전용 `disable-model-invocation`을 제거하고 각 `agents/openai.yaml`에 `allow_implicit_invocation: false`를 추가한다. `sdlc-feedback.patch`는 검토 기준 참조를 Codex TOML 경로로 바꾸고 native child 위임·파일 읽기 fallback·결과 대기/보존 및 모델 표현을 바꾼다. `tdd-optional/org-skills/codex/agents/sdlc-verifier.toml`을 제품 `.codex/agents/`에, `codex/templates/AGENTS.md`를 제품 루트에 복사한다. 기존 `AGENTS.md`는 덮지 않고 의미를 병합한다. 명시 호출은 `$design-spec`, `$plan`, `$sdlc-feedback`이다.

Codex README의 0.153.4 검증은 named custom-agent role 선택을 입증하지 않는다. 이 판의 fallback은 fresh child가 `.codex/agents/sdlc-verifier.toml`의 `developer_instructions`를 직접 읽게 하는 절차다. TOML의 `gpt-5.6-sol`/`high` 값과 역할 메타데이터 적용은 구분해야 한다. Claude 플러그인/marketplace manifest와 command 파일은 Codex 설치 대상이 아니다.

## 기존 검사 명령과 범위

| 검사 | 현재 명령·위치 | 확인 가능한 것 |
|---|---|---|
| 저장소 결정론 gate | 저장소 루트 `make check` (`Makefile`: `python3 -m unittest discover -s tests`, `bash tests/test_hooks.sh`, `bash tests/test_evals.sh`, `bash tests/test_managed_settings.sh`) | 패키지 경로·링크·manifest의 일부는 `tests/test_template_editions.py`가 확인. 스킬 모델 행동은 확인하지 않음. |
| Claude 패키지 파싱 | `claude plugin validate --strict tdd-optional/org-skills`; `claude plugin validate --strict tdd-optional/.claude-plugin/marketplace.json`; 루트 catalog를 바꾼 경우 `claude plugin validate --strict .claude-plugin/marketplace.json` | 플러그인/marketplace 구조. 실제 설치·명시 호출·자연 선택과 별개. 임시 검증 시 별도 `CLAUDE_CONFIG_DIR` 사용. |
| Codex patch 적용성 | 임시로 복사한 제품에 `patch --batch --dry-run -d "$CODEX_TARGET" -p1 < "$CODEX_ADAPTER/patches/explicit-only.patch"` 등 네 패치를 순서대로 검사한 다음, 설치 안내의 `patch --batch -d ... -p1` 순서로 적용하고 설치본을 비교 | patch 충돌과 최종 파일 내용. 같은 대상에 각 patch를 적용한 뒤 다음 patch를 확인해야 하며, 설치본의 전체 폴더·해시·상대 참조를 검사해야 함. 실제 모델 행동과 별개. |
| diff 위생 | `git diff --check <base>..<candidate>` 및 실제 미커밋 diff가 있으면 `git diff --check` | 공백 오류. 기능/의미 동등성은 확인하지 않음. |
| 모델 eval | `make evals` (`ANTHROPIC_API_KEY` 필요, 없으면 rc=2 SKIP); `bash evals/run.sh`는 결정론 부분만 | 별도 실행 근거. 이번 read-only 목록 작성에서 실행하지 않음. |

`docs/research/openwebagent-template-history/source-review.md`는 정확한 `ec47695` archive에서 `make check`(Python 103건 중 1 skip, hook 28, eval shell 8, managed settings PASS), Claude strict 3개, Codex patch 네 개의 dry-run·임시 적용을 기록한다. 이는 그 SHA의 과거 검사 근거다. `4a84596`에서 `tdd-optional/`은 동일하지만 현재 미커밋 WIP와 새 변경의 통과 근거로 자동 승계하지 않는다. 이 보고서 작성 중 설치·patch·모델·eval 명령은 실행하지 않았다.

## parity가 깨지기 쉬운 지점

1. `design-spec`/`plan` 본문·`references/`·`examples/`·제품 양식 중 하나만 고치면 Claude와 Codex에 같은 의미가 전달되지 않는다. 제품 내 상대 링크는 전체 `project/` 복사를 전제한다.
2. 작성 스킬의 front matter가 바뀌면 Codex `explicit-only.patch` hunk가 실패하거나 명시 전용 정책이 달라질 수 있다. Claude source의 `disable-model-invocation: true`와 Codex의 `allow_implicit_invocation: false`를 각각 확인한다.
3. 공통 `sdlc-feedback` 또는 verifier 기준을 바꾸면 Codex `sdlc-feedback.patch`와 `sdlc-verifier.toml`의 복제 전문도 함께 검토해야 한다. TOML이 공통 Markdown 기준보다 오래된 상태일 수 있다.
4. 설치 안내·manifest 판·루트와 배포판 marketplace·실제 설치본 해시가 어긋나기 쉽다. 목록에 이름이 보이는 것과 파일 읽기, 실제 업무 적용은 다른 근거다.
5. 루트 maker 라우터와 제품 배포본은 역할이 다르다. root WIP를 무심코 제품 스킬로 복사하거나 maker `intent/` 경로를 채택 제품의 `changes/` 경로로 치환하면 의미가 바뀐다.
