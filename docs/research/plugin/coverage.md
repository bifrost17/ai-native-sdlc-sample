# plugin — 덮음 행렬

행 = 브리프 S8 의 과제 ①~④ (정책 파일 없음 · {POLICY} = 없음). 열 = 배포 골격 후보(candidates.md A~C). 칸 = 덮음 / 부분 / —.

| 조항 | A. 플러그인+마켓플레이스 | B. `--plugin-dir` | C. `.claude/skills/` 복사 | 근거(raw/) |
|---|---|---|---|---|
| ① 플러그인 규격을 공식 문서로 확인하고 이 레포를 플러그인으로 만드는 최소 파일 작성 | 덮음 — `.claude-plugin/plugin.json`(name·description·version·author·repository·keywords) + `.claude-plugin/marketplace.json`(name·description·owner·plugins[0].source `"./"`), `claude plugin validate . --strict` 통과 | 부분 — plugin.json 만 필요 | — | doc-plugins-reference.md · doc-plugin-marketplaces.md · 01~03 |
| ② 마켓플레이스 등록·설치 절차를 실제로 돌려 본다 | 덮음 — 로컬 경로 등록(30) · GitHub 브랜치 고정 등록 `bifrost17/intent-sdlc-skills@lane/S8-plugin`(50) · `--scope project` 설치(31·50) · uninstall/remove(50·60) 모두 rc 0 | — (등록·설치 없음) | — | 30 · 31 · 36 · 37 · 50 · 60 |
| ③ 헤드리스 `claude -p` 가 플러그인의 스킬·명령을 로드하는지 실측 | 덮음 — `system/init.plugins` 에 등재, `slash_commands` 에 `intent-sdlc-skills:_probe`·`:_probe-cmd`, Skill 도구 호출 기록, 결과 토큰 일치: 로컬 마켓 3/3+명령, GitHub 3/3+명령 | 덮음 — 3/3+명령(수정 후) | — | 20~23 · 32~35 · 51~54 |
| ④ 안 되면 `.claude/skills/` 복사 경로도 실측해 둘 다 기록 | — | — | 덮음 — 3/3+명령, 플러그인과 병존 시 충돌 없음 | 40~44 |

## 겹침
- ③ 을 A·B 가 함께 덮는다. 같은 플러그인을 `--plugin-dir` 와 마켓플레이스 설치로 동시에 주면 문서상 로컬이 우선(doc-plugins.md) — 실측은 서로 다른 임시 프로젝트로 분리했으므로 겹친 상태는 시험하지 않았다.
- ④ 의 C 와 A 를 한 프로젝트에 같이 두면 `_probe` 와 `intent-sdlc-skills:_probe` 둘 다 등재되고 모델은 접두 없는 쪽을 골랐다(44). 내용이 같아 모순은 없지만, 정책 스킬이 두 경로에 다른 판으로 놓이면 어느 쪽이 실행될지 보장 못 한다 → README 「정책 오너에게 묻는다」.

## 모순
- 없음. 단, 스킬 폴더 이름과 명령 파일 이름이 같으면(`skills/_probe` + `commands/_probe.md`) 슬래시 이름이 하나(`intent-sdlc-skills:_probe`)로 합쳐지고 명령 쪽 본문이 실행됐다(10·11: Skill 호출은 됐으나 결과 토큰이 COMMAND). 2.1.265 실측. 다른 세션 규칙: 스킬과 명령에 같은 이름을 쓰지 않는다.

## 빈칸과 이유
- ① 의 C 열: 복사 경로는 플러그인 파일이 필요 없으므로 해당 없음.
- ② 의 B·C 열: 등록·설치 단계가 없는 경로라 해당 없음.
- ④ 의 A·B 열: ④ 는 「플러그인이 안 될 때의 대체」로 정의돼 있어 A·B 로 덮을 대상이 아님. 결과적으로 A 가 되었으므로 ④ 는 대체 경로 기록으로만 남긴다.
- 관리 설정(`strictKnownMarketplaces`·`disableSideloadFlags`)의 실제 차단: 행에 없지만 브리프 근거 절이라 시도함. `--settings` 로 넣으면 둘 다 적용되지 않았다(46·60) — 문서대로 managed-settings.json 전용. MDM/관리 파일 배포 권한이 없어 **확인 못 함**.
