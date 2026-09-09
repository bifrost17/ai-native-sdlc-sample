# plugin — 트리거·로드 시험

방법: 임시 프로젝트(`/tmp/s8/proj-*`, 빈 git 저장소, `.claude/` 없음)에서
`claude -p "<문구>" --output-format stream-json --verbose --max-turns 3 [경로 옵션]` 을 돌리고
(1) `system/init.plugins` 에 플러그인 등재, (2) `system/init.slash_commands` 에 `_probe` 항목, (3) `assistant` 메시지의 `tool_use` 가 `Skill {"skill": …}`,
(4) 결과 텍스트가 스킬 본문의 고정 토큰 `S8-PROBE-SKILL-LOADED`(명령은 `S8-PROBE-COMMAND-LOADED`)인지 본다.
원문·rc·시각은 raw/NN-*.txt (머리 세 줄 CMD/AT_UTC/RC, stderr, stream-json 전체). 실행기: /tmp/s8/run.sh (raw 파일 머리의 CMD 줄이 실제 명령).
시험 스킬: `skills/_probe/SKILL.md`(raw/_probe@44f5f66.SKILL.md 사본) · 명령 `commands/_probe-cmd.md`. 둘 다 끝나고 삭제(마지막 커밋).
Claude Code 2.1.265 · 2026-09-09 (UTC 09:36~13:06).

문구 세 개(모두 스킬 description 의 낱말을 그대로 쓰지 않도록 골랐다):
- P1 `Give me the probe token.`
- P2 `Run a plugin load check for this session.`
- P3 `Can you verify that our organization skills are loaded in this session?`
- CMD `/intent-sdlc-skills:_probe-cmd` (복사 경로는 `/_probe-cmd`)

## 1차 (수정 전) — `--plugin-dir`
| raw | 문구 | init.plugins | slash | Skill 호출 | 결과 | 판정 |
|---|---|---|---|---|---|---|
| 10 | P1 | 등재 | `intent-sdlc-skills:_probe` 하나 | `intent-sdlc-skills:_probe` | `S8-PROBE-COMMAND-LOADED` | **실패(이름 충돌)** — `skills/_probe` 와 `commands/_probe.md` 가 한 이름으로 합쳐져 명령 본문이 실행됨 |
| 11 | P2 | 등재 | 같음 | 같음 | `S8-PROBE-COMMAND-LOADED` | 실패(같은 이유) |
| 12 | P3 | 등재 | 같음 | 없음 — Bash 로 `~/.claude/plugins` 를 뒤짐, max-turns 초과(rc 1) | 빈 결과 | **실패(트리거 안 됨)** |
| 13 | CMD `/intent-sdlc-skills:_probe` | 등재 | 같음 | (명령 직접 호출) | `S8-PROBE-COMMAND-LOADED` | 성공 |
| 14 | P1, 플러그인 없음(대조군) | 미등재 | 없음 | 없음 — 파일 탐색 후 "I don't have one" | — | 대조군: 토큰 없음 = 스킬이 없으면 못 낸다 |

고친 것: 명령 파일을 `commands/_probe-cmd.md` 로 개명; 스킬 description 에 「instead of inspecting files or settings」와 「organization skills / org skills / policy skills are loaded or available」을 추가(커밋 44f5f66).

## 2차 — `--plugin-dir` (B)
| raw | 문구 | init.plugins | slash | Skill 호출 | 결과 | 판정 |
|---|---|---|---|---|---|---|
| 20 | P1 | 등재(`@inline`) | `:_probe`, `:_probe-cmd` | `intent-sdlc-skills:_probe` | `S8-PROBE-SKILL-LOADED` | 성공 |
| 21 | P2 | 등재 | 같음 | 같음 | 같음 | 성공 |
| 22 | P3 | 등재 | 같음 | 같음 | 같음 | 성공 |
| 23 | CMD | 등재 | 같음 | — | `S8-PROBE-COMMAND-LOADED` | 성공 |
→ 스킬 3/3, 명령 1/1.

## 3차 — 로컬 경로 마켓플레이스 등록 + `--scope project` 설치 (A)
등록·설치: raw/30·31 (rc 0; `.claude/settings.json` 에 `extraKnownMarketplaces{source:directory}` + `enabledPlugins`; 캐시 `~/.claude/plugins/cache/intent-sdlc-skills/intent-sdlc-skills/0.1.0` 에 레포 전체 45파일 784K 복사, `.git` 제외 — raw/36).
| raw | 문구 | init.plugins | slash | Skill 호출 | 결과 | 판정 |
|---|---|---|---|---|---|---|
| 32 | P1 | 등재(`@intent-sdlc-skills`, path = 레포 경로) | `:_probe`, `:_probe-cmd` | `intent-sdlc-skills:_probe` | `S8-PROBE-SKILL-LOADED` | 성공 |
| 33 | P2 | 등재 | 같음 | 같음 | 같음 | 성공 |
| 34 | P3 | 등재 | 같음 | 같음 | 같음 | 성공 |
| 35 | CMD | 등재 | 같음 | — | `S8-PROBE-COMMAND-LOADED` | 성공 |
→ 스킬 3/3, 명령 1/1. `claude plugin details` 는 스킬 2개, 상시 ~160 토큰(raw/37).

## 4차 — GitHub 등록(`bifrost17/intent-sdlc-skills@lane/S8-plugin`) + `--scope project` 설치 (A, 실제 배포 꼴)
등록·설치: raw/50 (HTTPS clone, ref lane/S8-plugin, sha 44f5f66; `.claude/settings.json` 에 `{source:github, repo, ref}`). 51·52 첫 시도는 세션 한도(`You've hit your session limit`)로 API 실패 → 재실행이 아래.
| raw | 문구 | init.plugins | slash | Skill 호출 | 결과 | 판정 |
|---|---|---|---|---|---|---|
| 51 | P1 | 등재(path = 캐시 경로) | `:_probe`, `:_probe-cmd` | `intent-sdlc-skills:_probe` | `S8-PROBE-SKILL-LOADED` | 성공 |
| 53 | P2 | 등재 | 같음 | 같음 | 같음 | 성공 |
| 54 | P3 | 등재 | 같음 | 같음 | 같음 | 성공 |
| 52 | CMD | 등재 | 같음 | — | `S8-PROBE-COMMAND-LOADED` | 성공 |
→ 스킬 3/3, 명령 1/1.

## 5차 — `.claude/skills/` · `.claude/commands/` 복사 (C)
| raw | 문구 | init.plugins | slash | Skill 호출 | 결과 | 판정 |
|---|---|---|---|---|---|---|
| 40 | P1 | 미등재(플러그인 아님) | `_probe`, `_probe-cmd` | `_probe` | `S8-PROBE-SKILL-LOADED` | 성공 |
| 41 | P2 | — | 같음 | 같음 | 같음 | 성공 |
| 42 | P3 | — | 같음 | 같음 | 같음 | 성공 |
| 43 | `/_probe-cmd` | — | 같음 | — | `S8-PROBE-COMMAND-LOADED` | 성공 |
→ 스킬 3/3, 명령 1/1.

## 집합 충돌 시험
| raw | 조건 | slash | Skill 호출 | 결과 | 판정 |
|---|---|---|---|---|---|
| 44 | C 복사본 + `--plugin-dir` 플러그인 동시, P1 | `_probe`, `_probe-cmd`, `intent-sdlc-skills:_probe-cmd`, `intent-sdlc-skills:_probe` 넷 다 | `_probe`(접두 없는 쪽) | `S8-PROBE-SKILL-LOADED` | 지시 어긋남 없음(내용 동일). 어느 쪽을 고를지는 보장 없음 |

## 통제 실험
| raw | 조건 | 관측 | 판정 |
|---|---|---|---|
| 45 | `--plugin-dir` + `--bare` (2회) | init.plugins 에는 등재됐으나 API 응답 `Not logged in · Please run /login`, rc 1 | **확인 못 함** — `--bare` 가 사용자 설정을 건너뛰어 이 머신의 인증을 못 찾는 것으로 보이나 원인 미확인. 모델 로드 여부 판정 불가 |
| 46 | `--plugin-dir` + `--settings '{"disableSideloadFlags":true}'` | 그대로 로드·트리거(3/3 과 동일) | `--settings` 로는 적용 안 됨 — 문서대로 managed-settings 전용. 관리 파일 배포 권한 없어 **확인 못 함** |
| 60 | `--settings '{"strictKnownMarketplaces":[]}' plugin marketplace add …` | 등록 성공(rc 0) | 같음 — managed-settings 전용, **확인 못 함** |

## 합계
수정 후 스킬 트리거 12/12 (경로 4 × 문구 3), 명령 4/4, 집합 충돌 0, 대조군 0/1(기대대로). 수정 전 1차는 0/3(이름 충돌 2, 미트리거 1).

## 뒷정리 (raw/60)
proj-mp·proj-gh 의 설치 해제와 마켓플레이스 제거 rc 0. `~/.claude/plugins/known_marketplaces.json`·`installed_plugins.json`·`~/.claude/settings.json` 에 intent-sdlc 항목 0. 캐시 폴더 `~/.claude/plugins/cache/intent-sdlc-skills` 는 uninstall 이 남겨서 수동 삭제.
