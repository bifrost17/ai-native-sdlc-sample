# plugin — 조사 요약 (S8)

스킬이 아니라 **골격**: 이 레포(`intent-sdlc-skills`)를 Claude Code 플러그인 하나 + 마켓플레이스 하나로 만들어, 템플릿(`bifrost17/intent-sdlc-sample`)을 채택한 팀이 `.claude/settings.json` 두 줄로 조직 스킬 세트를 받게 하는 것.
근거: 레슨 skills-as-institutional-knowledge 「distribute it organization-wide through a plugin」, hooks-as-approval-gates 의 관리 설정 절(`strictKnownMarketplaces` · `disableSideloadFlags` — 「any skill … came through the organization's approved plugin marketplace and not from a home directory」). 원문 사본 raw/doc-lesson-*.txt.
조사·실측 2026-09-09 (UTC 09:33~13:06), Claude Code 2.1.265, macOS.

## 결론 — 채택 집합: A(플러그인+마켓플레이스), 대체 C(`.claude/skills/` 복사)
- **① 규격·최소 파일** — 공식 문서(plugins-reference · plugin-marketplaces · plugins, raw/doc-*.md)로 확인. 만든 파일 둘:
  - `.claude-plugin/plugin.json` — `name: intent-sdlc-skills`(= 슬래시 접두), description, `version: 0.1.0`(갱신 캐시 키), author, repository, keywords. `skills/`·`commands/` 는 기본 자리라 선언 불필요.
  - `.claude-plugin/marketplace.json` — `name: intent-sdlc-skills`, description, `owner`, `plugins[0] = {name, source: "./"}` (레포 루트 = 플러그인 루트). `claude plugin validate . --strict` 통과(raw/02·03).
- **② 등록·설치** — 로컬 경로와 GitHub(`bifrost17/intent-sdlc-skills@lane/S8-plugin`) 두 방식 모두 `--scope project` 로 성공(raw/30·31·50). 결과는 임시 프로젝트의 `.claude/settings.json`:
  ```json
  { "extraKnownMarketplaces": { "intent-sdlc-skills": { "source": { "source": "github", "repo": "bifrost17/intent-sdlc-skills", "ref": "lane/S8-plugin" } } },
    "enabledPlugins": { "intent-sdlc-skills@intent-sdlc-skills": true } }
  ```
  머지 뒤 팀은 `ref` 없이(=기본 브랜치) 이 두 키를 템플릿의 `.claude/settings.json` 에 넣거나 아래 두 명령을 친다:
  ```
  claude plugin marketplace add bifrost17/intent-sdlc-skills --scope project
  claude plugin install intent-sdlc-skills@intent-sdlc-skills --scope project
  ```
- **③ 헤드리스 로드** — `claude -p … --output-format stream-json --verbose` 에서 `system/init.plugins` 등재, `slash_commands` 에 `intent-sdlc-skills:_probe`, `Skill` 도구 호출, 고정 토큰 응답까지 확인. 마켓플레이스(로컬) 3/3, GitHub 3/3, `--plugin-dir` 3/3, 명령 각 1/1 (trigger-tests.md, raw/20~23·32~35·51~54).
- **④ 복사 경로** — 플러그인이 됐지만 브리프대로 실측: `.claude/skills/_probe` + `.claude/commands/_probe-cmd.md` 3/3+명령(raw/40~43). 플러그인과 병존 시 넷 다 등재되고 모순 없음(raw/44).

## 설계 근거(무엇을 참고했고 왜 그렇게 갈랐나)
- 「레포 = 마켓플레이스 = 플러그인 하나」— Understand-Anything(MIT, 5feed1f) 의 최소 꼴을 따르되, 그쪽은 하위 폴더인데 우리는 `source: "./"` 로 루트를 썼다. 다른 세션이 이미 `skills/<name>/`·`commands/` 를 루트에 만들기로 돼 있어서(README·COMMON) 경로를 바꾸지 않기 위해서다. 공식 문서가 `source: "./"` 를 명시적으로 지원(raw/doc-plugin-marketplaces.md 722행).
- `commands/` 는 문서가 「flat .md, 새 플러그인은 skills/ 권장」이라 하지만 S6 의 spec 명령 자리가 `commands/` 이므로 유지.
- 관리 설정 통제와 맞물리는 것은 마켓플레이스 경로(A)뿐 — `--plugin-dir`(B)는 `disableSideloadFlags` 가, skills-dir(D)는 `strictKnownMarketplaces` 가 막는 대상. 그래서 A 를 배포 경로, B 를 개발·시험 경로, C 를 관리 설정 없는 팀의 대체 경로로 갈랐다.

## 발견(다른 세션에 알릴 것)
1. **스킬 폴더 이름 = 명령 파일 이름이면 충돌** — `skills/_probe` + `commands/_probe.md` 가 `intent-sdlc-skills:_probe` 하나로 합쳐지고 명령 본문이 실행됐다(raw/10·11). 스킬과 명령에 같은 이름을 쓰지 말 것.
2. **플러그인은 레포 전체를 복사한다** — 캐시에 `docs/`·`policies/`·`CLAUDE.md` 포함 45파일 784K(raw/36). 로드되는 것은 `skills/`·`commands/` 뿐이지만 용량과 `CLAUDE.md` 노출은 오너 판단(아래 질문 2).
3. **플러그인 스킬은 항상 접두** — `/intent-sdlc-skills:spec` 꼴. 템플릿의 `/spec` 과 이름이 다르므로 둘이 공존 가능하나, 플레이북 프롬프트가 `/spec` 을 부른다면 S6 와 맞춰야 한다(질문 3).
4. **트리거 문장 1차 실패** — 「organization skills are loaded?」 문구에 모델이 스킬 대신 파일을 뒤졌다(raw/12). description 에 「instead of inspecting files or settings」를 넣어 3/3. 정책 스킬도 「무엇을 하지 말고 이 스킬을 쓰라」를 description 에 넣는 편이 안전.
5. `--settings` 로 넣은 `disableSideloadFlags`·`strictKnownMarketplaces` 는 적용되지 않는다(raw/46·60) — 문서대로 managed-settings.json 전용.

## 남는 구멍
- 관리 설정의 실제 차단(`strictKnownMarketplaces`·`disableSideloadFlags`)은 MDM/관리 파일 배포 권한이 없어 **확인 못 함**.
- claude.ai 조직 설정 동기화 배포(E) — Team/Enterprise 관리자 권한 필요, **확인 못 함**.
- `--bare` 헤드리스는 이 머신에서 `Not logged in` 이라 모델 로드 판정 불가(raw/45).
- 템플릿에 이미 있는 `.claude/settings.json`(훅 포함)과 두 키의 병합은 실제 템플릿 레포에서 돌려 보지 않았다.
- 판 갱신 흐름(`claude plugin update`, version 범프 뒤 캐시 갱신), 비공개 레포 인증, Windows — 실행 안 함.
- 스킬 산출물 없음: S8 은 `skills/<name>/` 를 만들지 않는다. 시험용 `skills/_probe`·`commands/_probe-cmd.md` 는 삭제(사본 raw/_probe@44f5f66.SKILL.md).

## 정책 오너에게 묻는다
1. **라이선스** — 이 레포에 LICENSE 가 없다(GitHub API `license: null`). plugin.json 의 `license` 를 비워 두었다. 어떤 라이선스로 배포하나.
2. **플러그인 범위** — 레포 전체가 캐시에 복사된다. 그대로 두나, 아니면 플러그인을 `plugin/` 하위로 옮기고 `source: "./plugin"` 로 바꾸나(그러면 모든 세션의 `skills/`·`commands/` 경로가 바뀐다).
3. **명령 이름 공간** — 플러그인의 spec 명령은 `/intent-sdlc-skills:spec` 이 된다. 템플릿 `.claude/commands/spec.md`(`/spec`)를 남기고 플러그인은 스킬만 실을지, 명령도 실을지.
4. **관리 설정 배포** — `strictKnownMarketplaces: [{source: github, repo: bifrost17/intent-sdlc-skills}]` + `disableSideloadFlags: true` 를 누가 어떤 경로(MDM·관리 콘솔)로 배포하나. 브리프 근거 절이지만 이 세션은 검증 못 했다.
5. **판 범프 규칙** — `version: 0.1.0` 이 갱신 캐시 키다. 정책 변경 → 스킬 변경 → 오너 서명 때 누가 version 을 올리나(안 올리면 팀에 갱신이 안 간다).
6. **등록 ref** — 마켓플레이스 등록을 기본 브랜치로 할지 태그(`@v0.1.0`)로 고정할지.
