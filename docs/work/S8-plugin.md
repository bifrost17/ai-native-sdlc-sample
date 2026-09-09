# 변수 블록 — S8 · plugin

- {N} = 8 · {SKILL} = plugin · {POLICY} = 없음
- 브랜치 lane/S8-plugin · 산출 폴더 docs/research/plugin/ · 결정 docs/decisions/S8-plugin.md
- 해당 레슨: https://academy.claude.com/courses/ai-native-sdlc-playbook/skills-as-institutional-knowledge

## 특별 지시
스킬이 아니라 골격. 레슨의 「distribute it organization-wide through a plugin」과 managed settings 절(https://academy.claude.com/courses/ai-native-sdlc-playbook/hooks-as-approval-gates 의 strictKnownMarketplaces · disableSideloadFlags)이 근거.
과제: ① Claude Code 플러그인 규격(`.claude-plugin/` · skills/ · commands/ 배치, marketplace 등록 파일)을 공식 문서로 확인하고 이 레포를 플러그인으로 만드는 최소 파일을 작성 ② 마켓플레이스 등록·설치 절차를 실제로 돌려 본다(임시 프로젝트) ③ **헤드리스 `claude -p` 가 플러그인의 스킬·명령을 로드하는지** 실측(도구 호출 기록) ④ 안 되면 `.claude/skills/` 복사 경로도 실측해 둘 다 기록.
다른 세션의 skills/ 는 아직 비어 있으므로 시험용 더미 스킬 하나를 `skills/_probe/` 에 두고 끝나면 지운다. coverage 는 ①~④ 를 행으로.
