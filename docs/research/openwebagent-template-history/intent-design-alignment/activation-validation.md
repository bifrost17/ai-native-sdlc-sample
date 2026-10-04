# 활성 source 실행·설치 검증

2026-10-04. T15 / FR12 / SP11 / AC11의 **source 전달 범위**를 검증했다. 별도 OpenCode
제품 대화·구현 실험과 fresh final 검토는 이 기록의 통과 범위에 포함하지 않는다.
활성 source·maker 문서는 수정하지 않았고, 임시 source snapshot·제품은 private 경로만 사용했다.

## 실행 입력과 원본

- cwd: `/Users/jake/Projects/ai-native-sdlc-sample/.local/worktrees/intent-design-alignment`
- branch: `codex/intent-design-alignment`; base: `1d3ffd31a04ac10fc0ca4b59a5fa5da4cf4f3659`.
- 실제 HEAD: `d921985cd50f1094d726a468bcee0171313a5b24`, source `0.1.10`은 실행 당시 미커밋.
- before/after dirty hash: `737a68d1fa595694350262b363992dc238bcb8be193619836fa8bd4b795d3b3f`.
  status 전문·binary diff·추적/미추적 파일별 해시를 함께 고정한 지문이다. 실행 전후 동일했다.
- source snapshot의 `tdd-optional/` 전체와 root marketplace manifest를 고정했다.
  `source-tree-manifest.json` SHA256:
  `e1fd1bf6ecb41f7f8763fd3114209245b2449209887f412ab161526274d5f256`.
  source는 suite 실행 전후 동일했다. 후속 source commit은 이 파일별 지문과 대조해야 한다.
- 원본: `/Users/jake/Projects/ai-native-sdlc-sample/.local/experiments/private/0039-intent-design-alignment-muse/source-validation/`.
  `commands.json`은 각 실행의 실제 argv·cwd·rc·stdout/stderr 해시를 보존한다.
  각 `<label>.stdout/.stderr`는 전문이며 `run-source-validation.py`, `inspect-delivery.py`,
  `source-snapshot/`, `codex-product/`, `opencode-product/`, 설치 전후 hashmanifest도 보존했다.

## 무엇을 실행했나

실제 CLI는 Claude Code `2.1.285`, Codex CLI `0.159.2`, OpenCode `1.18.30`이었다.
suite 명령은 다음이며 전체 하위 명령은 private `commands.json`과 실행 스크립트에 있다.

```bash
python3 /Users/jake/Projects/ai-native-sdlc-sample/.local/experiments/private/0039-intent-design-alignment-muse/source-validation/run-source-validation.py
```

| 실제 실행 | rc | 확인 범위 |
|---|---:|---|
| `make check` | 0 | 현재 maker cwd의 기존 전체 회귀 |
| `claude plugin validate --strict <snapshot>/tdd-optional/org-skills` | 0 | plugin manifest |
| `claude plugin validate --strict <snapshot>/tdd-optional/.claude-plugin/marketplace.json` | 0 | 선택판 marketplace |
| `claude plugin validate --strict <snapshot>/.claude-plugin/marketplace.json` | 0 | root marketplace |
| Codex `explicit-only`, `sdlc-feedback`, `ux-copy`, `pr-loop`: `patch --batch --dry-run -d <codex-product> -p1`, 이어서 같은 명령의 `--dry-run` 없는 적용 | 각 0 | 16개 전체 skill 폴더 복사 뒤 4개 patch |
| OpenCode `sdlc-feedback`, `ux-copy`, `authoring-native`: 안내된 대상 디렉터리에서 같은 dry-run/적용 | 각 0 | native 11개·직접 읽는 2개·선택 작성 3개와 3개 patch |
| Ruby 2.6의 기존 `YAML.safe_load`로 설치된 두 도구의 16개 SKILL frontmatter 파싱 | 각 0 | YAML dictionary와 name/description string |
| Python 3.13 `tomllib.load` | 0 | Codex verifier TOML 전체 파싱 |
| `python3 .../skill-creator/scripts/quick_validate.py <codex-product>/.agents/skills/sdlc-feedback` | 1 | PyYAML 부재로 validator 시작 불가 |
| `bash .claude/hooks/protect-paths.sh`에 Makefile Edit JSON 입력 | 2 | 의도한 frozen path 차단 |

Claude strict는 private `CLAUDE_CONFIG_DIR`을 사용했다. marketplace 등록·plugin 설치나
전역 설치·설정 변경, 모델 호출, `make evals`, 모델 CI는 실행하지 않았다.

## 무엇을 보았나

`make check` stdout/stderr의 모든 줄을 읽었다. Python `Ran 116 tests` / `OK (skipped=1)`,
hook `28 passed, 0 failed`, eval harness `8 passed, 0 failed`, managed-settings의 11개 공식
키·훅 계약 PASS였다. harness의 의도한 위반 입력 rc=1, 없는 파일/키/jq 등의 rc=2와
`SKIP` 검사는 기존 시험의 기대 동작이며 실제 agent eval 실행 통과가 아니다.
첫 회귀 실패 줄은 없다. 별도 bad-input hook의 stderr는
`[protect-paths.sh] BLOCKED: Makefile is a frozen path ...`이며 rc=2로 차단됐다.

세 manifest의 현재 plugin version은 모두 `0.1.10`, source 경로는 root에서
`./tdd-optional/org-skills`, 선택판에서 `./org-skills`였다. 세 strict 검사는 모두
`Validation passed`였다. source/adapter 안내와 설치된 skill의 상대 링크 172개에서 누락은 없었다.

Codex/OpenCode 각각 16개 skill의 원 source 파일 59개가 모두 존재했다. 전체 폴더 복사로
references·examples·templates·LICENSE·PROVENANCE 등 동반 자료를 보존했다. 변경 파일은 안내된
SKILL 변환과 OpenCode ux-copy PROVENANCE 변환이며, Codex는 네 `agents/openai.yaml`을 추가했다.
네 YAML은 모두 `allow_implicit_invocation: false`다. 원본 폴더를 patch하지 않았다.

모든 patch dry-run/적용 rc=0이며 stdout/stderr에 offset 또는 fuzz 메시지가 없었다.
macOS `patch`는 두 설치판의 sdlc-feedback에 `SKILL.md.orig`를 한 개씩 생성했다.
이는 source와 같은 바이트이며 SHA256은
`c339dfea38c67d96b7daeccaac752a08d5e196a29a75477463130d74bd0ac92f`다.
원본 설치 재현을 그대로 보존했다. 따라서 Codex target 파일 수 64는 원본 59 + YAML 4 + backup 1,
OpenCode target 60은 원본 59 + backup 1이다. backup 생성을 offset/fuzz 관측으로 바꾸어 쓰지 않는다.

Claude 원 검증자의 **Review criteria**와 설치판을 전문 diff했다. OpenCode는 완전 동일했고
Codex는 프로젝트 입력 목록에 `AGENTS.md`를 추가한 한 줄만 달랐다. 설치된 feedback diff도 읽었으며
Codex는 criteria 경로·native 호출/fallback·model/effort, OpenCode는 verifier 이름·provider 책임만
변환했다. 새 편입 전 의미 대조는 그대로 남았다. 해당 전문은 `criteria-comparison.stdout`,
`codex-feedback-comparison.stdout`, `opencode-feedback-comparison.stdout`에 보존했다.

## plan과 다른 점

이 source 검증 범위에서 중요한 불일치는 없다. 이전 0027 plan의 실제 전달 계약은 전체
16개 자산·동반 자료·선택 호출·기존 patch/manifest 회귀였다. 이번 source는 그 전달 경로를 유지한다.
새 지침 문자열을 고정하는 테스트를 추가하지 않았고 기존 hook 동작/신호를 수정하지 않았다.

## 확인하지 못한 것과 다음 단계

skill-creator validator는 `ModuleNotFoundError: No module named 'yaml'`로 실행 불가였다.
기존 Ruby YAML parser를 사용했지만 이것은 quick_validate의 모든 skill 규칙 통과를 대신하지 않는다.
Codex/OpenCode catalog 발견·자연 선택·모델의 기준 읽기/판단·native 검증자 위임/대기·권한의
런타임 집행은 이번 파일/파싱 검증으로 확인하지 않았다. Claude도 manifest 검증까지만 수행했다.

root가 source commit을 파일 지문과 대조한 뒤 별도 0039 제품 실험을 수행한다.
실험·문서·인계의 fresh final 검증은 그 실행 완료 후 별도 후속으로 남긴다.
이번 source 확인을 AC11 전체 완료나 제품 행동 효과·다른 두 도구의 행동 통과로 부르지 않는다.
