# 결정 S8 — plugin: 이 레포를 플러그인 하나 + 마켓플레이스 하나로 배포한다

날짜 2026-09-09 · 세션 S8 · 브랜치 lane/S8-plugin · 상태: 오너 서명 대기

## 결정
1. 레포 루트가 플러그인 루트다: `.claude-plugin/plugin.json`(name `intent-sdlc-skills`, version 0.1.0) + `.claude-plugin/marketplace.json`(plugins[0].source `"./"`). 다른 세션의 `skills/<name>/`·`commands/` 는 그대로 플러그인 구성요소가 된다.
2. 팀 배포 경로는 마켓플레이스 설치(`extraKnownMarketplaces` + `enabledPlugins`, `--scope project`). `--plugin-dir` 는 개발·시험 전용, `.claude/skills/` 복사는 관리 설정이 없는 팀의 대체 경로.
3. 스킬과 명령에 같은 이름을 쓰지 않는다(충돌 실측).

## 근거
- 규격: docs/research/plugin/candidates.md A · raw/doc-plugins-reference.md · raw/doc-plugin-marketplaces.md.
- 실측: docs/research/plugin/trigger-tests.md — 등록·설치(raw/30·31·50), 헤드리스 로드 스킬 12/12·명령 4/4(raw/20~23·32~35·40~43·51~54), 충돌(raw/10·11·44).
- 덮음: docs/research/plugin/coverage.md ①~④ 모두 덮음.
- 레슨: skills-as-institutional-knowledge(플러그인 배포) · hooks-as-approval-gates(관리 설정) — raw/doc-lesson-*.txt.

## 기각·보류
- skills-dir 플러그인(D) 기각 — 홈 디렉터리 기준, 관리 설정이 차단 대상.
- claude.ai 조직 동기화(E) 보류 — 조직 관리자 권한 필요.

## 확인 못 한 것
관리 설정의 실제 차단, claude.ai 동기화, `--bare` 헤드리스, 템플릿 settings.json 과의 병합, 판 갱신 흐름. 자세히는 README 「남는 구멍」.

## 오너 결정 필요
README 「정책 오너에게 묻는다」 6개 — 라이선스, 플러그인 범위(레포 전체 복사), 명령 이름 공간, 관리 설정 배포 주체, version 범프 규칙, 등록 ref.
