# 완료 인계 보완 source·전달·maker 검증

Status: source and current-handoff verification complete; maker delivery commit pending

2026-10-04 Asia/Seoul. fresh Sol/high verifier가 직접 검증했다. 범위는 maker 0028의 T16,
spec@1872299 FR13/SP12/AC12와 intent@63bb3f6, 사용자 “보완해”의 source·현재 인계 보완이다.
소스의 의미·임시 전달·기존 회귀를 확인했으며 모델 행동 개선, 0038/0039 원 제출판 복구,
사람 수락·통합·배포를 판정하지 않는다. source·제품·다른 문서는 수정하지 않았다.

검증 경로:
`/Users/jake/Projects/ai-native-sdlc-sample/.local/worktrees/intent-design-alignment`.
branch `codex/intent-design-alignment`, HEAD
`18484793856036db3f21bb92b05b70468bdf6b5d`와 당시 dirty source다.
local main과 origin/main은 모두 `1d3ffd31a04ac10fc0ca4b59a5fa5da4cf4f3659`다.
T15의 main 대비 누적 변경, T16의 HEAD 대비 변경과 직전 0027 사슬의 자기 diff를 구분했다.

## What ran

maker `.claude/agents/verifier.md`, CLAUDE.md Commands/Verifying, REVIEW.md,
현재 intent/spec/plan, 북극성 V4-09/V4-11과 verifier/feedback source를 읽었다.
공통 검토 기준의 완료 주장·현재 plan·채택 색인·실행 근거 대조를 이 검토에 포함했다.
source 의미 반례 검토는 [기존 검토 원문](handoff-closure-review.md)의 후속 실제 source 절과 대조했다.

원본 경로는
`/Users/jake/Projects/ai-native-sdlc-sample/.local/research/openwebagent-template-history/handoff-closure-20261004/validation/`다.
이하 `R`은 그 절대 경로, `S`는 위 worktree다. 실행 스크립트는 새 private 경로에
apply_patch로 작성했다. 앞선 0039의 검증 스크립트를 읽어 이 범위에 맞게 복사·보완했고
원 경로에서 실행하거나 이전 원본을 덮어쓰지 않았다.

실제 시작 명령과 exit code:

```text
python3 R/run-source-validation.py
rc=0

/opt/homebrew/Caskroom/miniconda/base/bin/python3.13 R/inspect-delivery.py
rc=1 (최초 .orig 기대 오류; 아래에 보존)

python3 R/finish-validation.py delivery-inspection-initial /opt/homebrew/Caskroom/miniconda/base/bin/python3.13 R/inspect-delivery.py
wrapper rc=0; child rc=1 (동일 진단 실패 원문 보존)

python3 R/finish-validation.py delivery-inspection /opt/homebrew/Caskroom/miniconda/base/bin/python3.13 R/inspect-delivery.py
wrapper rc=0; child rc=0 (검증 코드의 .orig 기대만 수정)

python3 R/finish-validation.py supplement-validation /opt/homebrew/Caskroom/miniconda/base/bin/python3.13 R/supplement-validation.py
wrapper rc=0; child rc=0

python3 R/finish-validation.py final-inspection /opt/homebrew/Caskroom/miniconda/base/bin/python3.13 R/final-inspection.py
wrapper rc=0; child rc=0
```

위 표시의 R은 가독성을 위한 약칭이다. 정확한 절대 argv·cwd·각 child rc와 stdout/stderr
바이트 SHA-256은 `commands.json`에 있다. wrapper rc와 child rc를 혼동하지 않는다.
실제 핵심 child 명령은 다음과 같다.

| 실제 명령·대상 | rc·관측 |
|---|---|
| `make check`, cwd S | 0; 전체 stdout와 stderr를 읽음 |
| `claude plugin validate --strict R/source-snapshot/tdd-optional/org-skills` | 0 |
| `claude plugin validate --strict R/source-snapshot/tdd-optional/.claude-plugin/marketplace.json` | 0 |
| `claude plugin validate --strict R/source-snapshot/.claude-plugin/marketplace.json` | 0 |
| `patch --batch --dry-run -d R/codex-product -p1`, stdin Codex explicit-only/sdlc-feedback/ux-copy/pr-loop patch | 네 개 모두 0 |
| 같은 네 patch의 `patch --batch -d R/codex-product -p1` 실제 적용 | 네 개 모두 0 |
| `patch --batch --dry-run -d R/opencode-product/.opencode/skills/{sdlc-feedback,ux-copy} -p1` | 두 개 모두 0 |
| 같은 두 patch 실제 적용 | 두 개 모두 0 |
| `patch --batch --dry-run -d R/opencode-product/.claude/skills -p1`, stdin authoring-native patch | 0 |
| 같은 authoring-native patch 실제 적용 | 0 |
| Ruby `YAML.safe_load`로 각 플랫폼 16개 SKILL frontmatter 파싱 | 모두 0 |
| Ruby로 verifier 2판·Codex openai.yaml 4개 파싱 | 0 |
| Python3.13 `tomllib.load`로 설치 Codex verifier 파싱 | 0 |
| `python3 /Users/jake/.codex/skills/.system/skill-creator/scripts/quick_validate.py R/codex-product/.agents/skills/sdlc-feedback` | 1; PyYAML 부재 |
| `bash .claude/hooks/protect-paths.sh`, stdin `{"tool_name":"Edit","tool_input":{"file_path":"Makefile"}}` | 2; 예상한 frozen-path 차단 |
| `git diff --check`, cwd S | 0 |
| `opencode debug agent sdlc-verifier`, cwd R/opencode-product | 0; JSON·본문 대조 |
| `opencode debug skill`, cwd R/opencode-product | 0; 첫 PIPE 출력 불완전, 직접 파일 출력의 bounded 재실행 JSON 완전 |
| `git diff --name-status b9af49a 46908f4`, 자기 0027 범위 | 0 |
| `git diff b9af49a 46908f4`, `git show 46908f4:intent/0027-single-template-skill-parity/plan.md` | 0 |
| `git diff 46908f4 -- intent/0027-single-template-skill-parity/` | 0; 후속 역사 정정과 로컬 통합 기록 구분 |
| `git merge-base --is-ancestor origin/main HEAD` | 0; 로컬 ref의 ancestry만 확인 |

명령별 stdin patch는 source snapshot의 해당 파일과 연결된다. 각 label의
`*.stdout`·`*.stderr`가 전문이다. 실제 make 출력 전문은
`make-check.stdout`·`make-check.stderr`에 있으며, `make build`·`make lint`는
이 repo에 target이 없어 실행 성공으로 기록하지 않았다. 실제 회귀는 make check다.
semantic API evals와 실제 모델 CLI 턴은 실행하지 않았다.

## What was observed

make check의 모든 출력에서 실패는 없었다.

```text
Ran 116 tests in 41.134s

OK (skipped=1)
test_hooks: 28 passed, 0 failed
8 passed, 0 failed
org/managed-settings.example.json 키 11개 전부 공식 목록 안
PASS  managed-settings 키·훅 계약
```

이는 기존 Python 회귀·hook·fake eval harness·설정 검사의 결과다. T16 문구를 모델이 실제로
준수하는 시험은 아니다. T16은 새 문구와 동일한 기대를 고정하는 테스트를 만들지 않는다고
선택했고, 의미 반례 검토와 설치/기준 대조를 별도 Proof로 두었다. 실제 `proof-search.stdout`와
Makefile 실행 경로를 읽어 기존 회귀가 실제 make 출력에 들어 있는지 확인했다.

세 strict 검사 모두 `✔ Validation passed`였고 stderr는 비었다.
Codex/OpenCode의 dry-run과 실제 적용에 reject/fuzz/offset 실패가 없었다.
각 임시 제품은 같은 snapshot의 project 전체와 13개 팀·3개 작성 skill의 전체 폴더를 복사했다.
Codex 16개는 source 59파일→target 63파일이며 추가 4개는 explicit-only openai.yaml이다.
OpenCode 16개는 source/target 59파일이다. 누락 파일 0, 동반 자료의 선언되지 않은 변경 0이다.
OpenCode ux-copy PROVENANCE.md의 변경은 기존 플랫폼 patch의 선언된 변환이다.
검증자·AGENTS/색인도 해당 adapter source에서 복사했고 전체 설치 manifest에 hash를 보존했다.

`delivery-inspection.json`의 상대 링크 확인 대상은 두 플랫폼의 16개 SKILL.md와
source의 루트/판별 안내·org README·PROCESS/REVIEW다. 그 범위의 누락 링크는 0이다.
모든 역사 Markdown의 링크나 외부 웹 주소를 전수 확인한 결과로 확대하지 않는다.
root catalog·선택판 catalog·plugin의 버전은 모두 0.1.10이다.

검토 기준 본문은 Claude=OpenCode 바이트 동일이다. Codex는 프로젝트 입력 목록의
`AGENTS.md, CLAUDE.md` 한 줄만 다르고 이를 정규화하면 동일하다.
`criteria-comparison.stdout`, `codex-feedback-comparison.stdout`,
`opencode-feedback-comparison.stdout`의 실제 diff를 읽었다. 플랫폼 patch는 완료 요약 갱신·
같은 검토의 요약/색인/근거 입력을 보존한다. Codex의 호출/기준 경로·모델 표현과 OpenCode의
검증자 이름/설정 책임 변환을 해당 adapter 범위로 구분했다.

OpenCode debug agent의 실제 JSON prompt는 설치 검증자 본문과 같았다.
`steps: 20`, edit/write/task/skill false를 확인했다. 이 값은 설정 파싱이며 권한의 실제
런타임 집행을 검증한 것은 아니다. debug skill의 첫 stdout PIPE 캡처는 rc0인데 약65KiB에서
JSON이 잘렸다. `opencode-debug-skill.stdout`의 불완전 원본을 그대로 보존하고, 모델을
시작하지 않는 동일 명령을 stdout 파일로 직접 연결해 한 번 더 실행했다.
`opencode-debug-skill-file.stdout`는 완전한 32항목 JSON이었다. 기대한 임시 local native11개와
작성3개 모두 실제 설치 경로·본문이 일치했다. 나머지 global/built-in 항목도 있어 완전한 전역
격리를 주장하지 않는다. 자료용 to-questionnaire/pr-loop 2개는 설치 inventory에 있고,
catalog의 동명 global 항목을 임시 자료 설치판의 발견 성공으로 세지 않았다.
관측 CLI는 Claude2.1.285, Codex0.159.2, OpenCode1.18.30, Ruby2.6.10이다.

의도적 잘못된 hook 입력의 정확한 stderr:

```text
[protect-paths.sh] BLOCKED: Makefile is a frozen path (.github/* Makefile .claude/hooks/* .claude/settings.json). Reason: CI wiring, the make targets and the hooks are the feedback loop itself; an agent must not loosen them mid-task. Route: a human changes it in its own PR, or edits PROTECTED in this hook in that PR.
```

실제 Edit나 Makefile 쓰기는 수행하지 않았다. 기존 hook 범위에서 rc2가 기대한 결과다.
그 외 최초 실행 불가 줄은 다음이며 PASS로 세지 않는다.

```text
ModuleNotFoundError: No module named 'yaml'
```

quick_validate를 위해 패키지를 설치하지 않았다. Ruby YAML 파싱은 별도 검사다.

검증 도구의 최초 delivery-inspection은 patch가 반드시 .orig를 생성한다고 가정해 rc1로
끝났다. 실제 실패 경로는 `codex-product/.agents/skills/sdlc-feedback/SKILL.md.orig`이며
`delivery-inspection-initial.stdout`·`.stderr`에 보존했다. source나 patch를 고치지 않고
.orig가 없으면 source/설치 본문 직접 diff를 읽도록 private 검사만 보정해 rc0을 확인했다.
추가 recorder의 outer wrapper가 inner 메타데이터를 덮은 오류도 private 검사에서 발견했다.
실제 명령 원문/rc 출력·실행 script·stdout/stderr hash로 11행을 복구하고 wrapper가 child 완료 뒤
최신 commands를 읽게 보정했다. `final-inspection.stdout`에 이 보정과 근거를 남겼다.

### 실제 대상 지문

| 기록 | SHA-256 |
|---|---|
| before dirty hash: HEAD+status+binary diff+worktree file manifest | 4c7383d67bcdf2aff92770da12d3795e3707022310e741620e0ffb11c0ff1fe4 |
| after dirty hash | 52da13106259a55275e3b7786663a60edd3d34d04c69c2ef76092ef24ac85327 |
| source-tree-manifest.json | 219707106e8709572e1fb7bea6b7a9661745d8497cd8ba40f804ae8b7dc76caf |
| codex-installed-manifest.json | 4a4c5537c33c968c621ba9c87d3cd9831804679e07ceaf1bb7700bdfcbe42de4 |
| opencode-installed-manifest.json | 9fff475cf1741a2b619882a2504d8d6c73753059229144cd12cc21619fb61000 |
| first updated maker plan | 18c28a5af1fb76729735495d285f031fa4c1196f58e255972e4393b1cd50d68f |

source snapshot에는 tdd-optional 전체와 루트 marketplace를 고정했다.
make/설치 전후 그 source 바이트는 같았고 최종 추가 관측 시점에도 manifest의 모든 파일이 같았다.
full worktree manifest의 초기/후기 차이는 병렬 의미 검토자가 보완한
`handoff-closure-review.md`뿐이었다. 전체 작업트리가 동일했다고 쓰지 않는다.
현재 maker 문서 판은 initial/updated artifact snapshot·manifest에 별도로 연결했다.

## What does not match plan.md

T16 source/전달 범위에는 중요한 불일치가 없다. 실제 변경은 feedback·plan 작성 예시·
PROCESS/REVIEW, verifier3판, feedback patch2판, org README와 제작 연구/북극성 기록이다.
모두 T16의 실제 경로 목록에 있다. 이전 T15의 design-spec·제품0039 범위를 현재 작업의
미수행으로 세지 않았고, 현재 사슬 문서의 후속 판은 lineage로 확인했다.

FR13/SP12/AC12는 완료 주장 전에 현재 요약을 정리하고 같은 최종 검토에 요약·채택 색인·근거를
포함한다. 현재 source는 그 시점을 기존 completion 절에 연결하고 채택하지 않은 색인,
미래 자기 SHA·전체 로그 복제·새 장부·매 commit 검토·문서-only의 새 구현 검토를 요구하지 않는다.
source가 전달하는 기준과 별도 의미 reviewer의 실제9파일 지문이 이 snapshot과 맞는다.

이 maker는 제품의 changes/ 색인을 채택한 제품 repo가 아니다. 현재 작업은 maker plan과
이 연구 README, 기존 docs/experiments/README의0038/0039 상태와 실제 검증/검토 근거를 대조했다.
제품용 changes 색인을 새로 만들거나 표본 행을 완료로 바꾸지 않았다.0038/0039 partial은
현재 plan·연구 안내·실험 색인·V4-11에 보존된다.

최초 실행 당시 maker plan은 T16 source수정/검증을 다음 일로 두었다. 검증이 진행 중이었으므로
그 시점의 미완료 표기는 적절했다. 실제 결과를 받은 뒤 root는 상단과 T16현재인계에
source·의미검토·make/strict/patch/16자산 완료, catalog bounded 확인·최신 요약 대조·제작 commit
대기를 나눠 기록했다. 이 중간판을 읽고 실제 완료 결과와 맞음을 확인했다.
catalog 확인은 이제 끝났으므로 root가 최종 요약과 인도 경계를 갱신하면 그 changed scope를
같은 기존 검토에서 마지막으로 대조한다. 이미 확인한 source를 새 모델 실험으로 재검증하지 않는다.

인접 흐름인0027은 자기 기준 `b9af49a..46908f4`의186경로를 plan과 대조했다.
133개 tdd-first 삭제, root/활성 안내·package adapter·scripts/evals/tests/CI·사슬근거라는
계획 범위에 들어 있었다. 현재0027의 plan/실행 README에 후속 ad98ade의 실제 로컬 통합 기록과
초기 실패 원본 JSON 결손 정정이 있음을 구분했다. 이를 T16 변경이나 현재 설치 완료로 승계하지 않았다.

## What could not be checked

기존 Python1skip은 남아 있다. PyYAML quick_validate는 실행 불가이며 Ruby 파싱으로 대체
통과라고 쓰지 않는다. source·임시 파일·설정 파싱은 자연 스킬 선택/읽기, 새 문구 준수,
검증자 위임·대기·권한 집행, 모델 행동 개선·0038/0039 원 제출판 복구를 입증하지 않는다.

실제 모델/semantic API evals·새 제품 실험·전역 설치·원제품 변경·원격/Git stage/commit·push/merge는
수행하지 않았다. local main/origin/main ancestry는 확인했지만 remote refresh와 dirty source의
통합 실행·후속 resulting commit은 아직 없다. root의 제작 인도 뒤 결과판 확인은 별도 실제 사건이다.
이 보고서가 그 commit이나 사람 수락·통합·배포를 미리 승인하지 않는다.

## 최종 현재 요약·근거 대조 — 2026-10-04 KST

root가 catalog 결과를 반영한 maker plan 상단·T16현재인계와 연구 README를 같은 verifier가
다시 읽었다. 기존 원문/실행 결과와 갱신 diff를 대조했으며 중요한 불일치는 없다.
이 확인은 source나 제품을 추가 수정하지 않은 changed-scope 대조다. 회귀·설치·모델 실행을
반복하지 않았고 다음 세 파일의 현재 바이트를 별도 snapshot에 보존했다.

| 마지막 대조 입력 | SHA-256 |
|---|---|
| maker plan.md | 6d6c6f3196d42e7e3dc410f124dc3d1bef8a1251669fa70524cc5bd2913a8edb |
| 연구 README.md | 3a7384eb37a297b8d381e8dc014f0150f2a7fb5f237edc0f85582339e33e5038 |
| 기존 방향·source 검토 원문 | 61b0ff5eed19ff00a86250b5bba2be08186a5d9d0443db43715c94cb4a9cc2bf |

정확한 HEAD+현재 diff+status·입력 파일 hash는 `closure-binding.json`,
`artifact-snapshot-closure-manifest.json`과 `artifact-snapshot-closure/`에 있다.
closure binding hash는 `22fc031ffb83cffc15d4ffa00106121132cc90079ee5aaf74c07016885d04a4f`이며,
`close-handoff.stdout`·`.stderr`와 명령 메타데이터가 그 기록에 연결된다. 이 snapshot의
검증 보고서 바이트는 본 최종 문단을 추가하기 직전 판이며, 자기 미래 hash를 요구하지 않았다.
해당 명령은 rc0였고 실행 때 source manifest의 모든 package 파일이 기존 시험판과 같았다.

갱신 요약은 실제로 완료한 source·의미 검토·make/strict/patch·16자산·기준/버전·catalog 확인을
완료로 구분한다. quick_validate의 PyYAML 한계, 최초 진단 코드 오류와 메타데이터 복구,
첫 catalog 출력 절단·직접 파일 출력 재확인도 실제 원문과 맞는다. OpenCode의 자료용2개를
자동 catalog 발견으로 세지 않았고, debug agent 설정 파싱을 런타임 권한 집행으로 확대하지 않았다.
여기서 읽기 전용 설정 확인은 edit/write/task/skill 비활성화의 파싱 범위다.

plan과 연구 README는 최신 요약의 이 대조와 제작 commit을 아직 남은 일로 표시했다.
본 대조가 끝났으므로 root는 그 사실을 현재 요약에 반영하고 source·결과 기록을 같은 제작
commit으로 인도할 수 있다. 그 commit 생성·resulting content 확인은 아직 수행되지 않았다.
미래 자기 SHA나 새 검토 회차를 요구하지 않는다. 기존 실험 색인·0038/0039 원 보고서는
partial을 유지하며 이 source 보완을 원 제출 인계 복구·모델 행동 개선으로 승격하지 않았다.

T16의 source·전달·maker 현재 인계 대조 범위에서 중요한 미해결 발견은 없다.
전역 설치·원제품·새 runtime 실험·push/merge·전체 AC04 비교는 계속 이번 범위 밖이다.
