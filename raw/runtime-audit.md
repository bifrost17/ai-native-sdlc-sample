# 0017 Claude runtime instruction audit

## 확정 사실

- 실험 첫 턴은 `/Users/jake/Projects/ai-native-sdlc-experiments/f02-plan-sync`의 clean `d22a9fe`에서 시작했다. 당시 루트 `CLAUDE.md`에는 구현이 계획에서 벗어나면 `plan.md`와 이유를 해당 구현과 같은 커밋에 담고, 요구·설계 변경은 개정 절차를 따르라는 지침이 있었다.
- `run_turn.py`는 Claude Code 2.1.265를 `--restricted --setting-sources project,local --settings <inline JSON> --tools Read,Write,Edit,Glob,Grep,Bash,Skill`로 실행했다. 다섯 턴의 init 기록에서 실제 도구 목록은 `Bash, Edit, Glob, Grep, Read, Skill, Write`였다.
- 현재 셸에서 `CLAUDE_CODE_SIMPLE`, `CLAUDE_CODE_SAFE_MODE`, `CLAUDE_CODE_DISABLE_AUTO_MEMORY`는 모두 unset이었다.
- 다섯 턴의 공개 stream 기록과 로컬 보존 세션에서 `CLAUDE.md`를 대상으로 한 명시적 `Read`는 없었다. turn 1은 intent/spec/plan/code/tests를 읽었고 turn 2는 `tracker.py`를 읽었다. HUMAN이 누락을 지적한 turn 3에서야 `docs/PROCESS.md`와 `docs/GIT-WORKFLOW.md`를 읽었다.
- 같은 커밋 절차의 정확한 문구는 turn 3의 `docs/PROCESS.md` Read 결과에서 처음 관측됐다.
- `run_turn.py`는 `system/init` 이벤트를 선택 필드로 축약하므로 원래 init의 전체 내용을 보존하지 않는다. 로컬 세션 JSONL의 첫 assistant 전 이벤트와 전체 텍스트에도 프로젝트 지침 원문이 보이지 않는다.

## 판정과 한계

- 지침 파일이 작업트리에 존재했다는 사실은 확정이다.
- turn 2 전에 자동 주입 원문이 모델 컨텍스트에 실제 전달됐는지는 보존 기록으로 확정할 수 없다. 자동 컨텍스트가 세션 JSONL에 완전히 직렬화된다는 근거가 없으므로 원문 부재를 미전달의 증명으로 사용할 수 없다.
- Claude Code 도움말은 `--restricted`가 user/project/local “settings files”를 무시한다고 설명한다. 공식 문서는 `CLAUDE.md` memory files와 JSON settings files를 구분하며, `--bare`와 `--safe-mode`만 CLAUDE.md 비활성화를 명시한다. 따라서 `--restricted`가 CLAUDE.md를 억제했다는 결론은 근거가 없다.
- 공식 동작 계약상 `project` setting source는 루트 `CLAUDE.md`를 세션 시작 컨텍스트에 로드해야 한다. 이는 기본 동작 기대이며 이번 실행의 직접 관측 결과는 아니다.
- `CLAUDE.md`를 명시적으로 읽지 않았다는 것은 관측 사실이지만, 자동 주입이 이뤄졌다면 별도 Read 없이도 지침을 확인할 수 있으므로 그 자체를 규칙 위반으로 판정하지 않는다. 확정 가능한 실패는 turn 2 요구 변경에서 spec/plan 갱신을 누락했다는 것이다. HUMAN 리뷰 이후에만 관련 절차를 명시적으로 읽고 복구했다.
- 후속 R01/R02는 초기 온보딩에서 `CLAUDE.md` 확인을 요구했고, T1의 Bash `cat` 성공 결과가 당시 파일 전문과 일치함을 별도 exposure 기록으로 확인했다. 이는 도구 결과를 통한 지침 전달 관측이며 원래 실행의 자동 주입 여부를 소급해 증명하지 않는다. 초기 프롬프트 조건도 달라졌으므로 템플릿 문구 효과만을 단독 입증하지 않는다.

## 공식 출처

- Claude Code CLI reference: https://code.claude.com/docs/en/cli-usage
- Claude Code settings and the distinction between memory and JSON settings files: https://code.claude.com/docs/en/settings
- Project `CLAUDE.md` loading through the project setting source: https://code.claude.com/docs/en/agent-sdk/claude-code-features
- CLAUDE.md is injected into conversation context rather than the system prompt: https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts
- CLAUDE.md troubleshooting and delivery model: https://code.claude.com/docs/en/memory
