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

## 후속 최종 검증 원문 — 2026-10-04

범위는 source commit `b579ebb3fa70ef6afffe6fcdf751a91f7e7f9ef2`, 실제 제품 제출
`921432a575fedf8a45f9f44bca9750846819e72b`와 현재 maker의 결과 기록이다.
원제품을 수정하지 않은 detached `final-checkout`의 문서·코드·시험을 읽고 공개 대화/도구 event,
단계별 snapshot, 최종 실행 로그와 비교했다. 추가 OpenCode/모델 호출·제품 변경·행동 검사·
전체 make 반복은 하지 않았다. maker의 다른 작업자 변경은 되돌리지 않았다.

### 실행·열람한 근거

이 검토자가 새로 실행한 것은 Git 상태/제출 내용 조회, JSON·문서 읽기와 기존 입력의 해시/판 대조다.
주요 조회는 `git rev-parse HEAD`, `git status --short`, `git log -4 --oneline`,
`git show --format=fuller --stat HEAD`이며 제출 clone에서 rc0, HEAD는 위 `921432a`, status는 비었다.
source 입력 고정과 named verifier 본문/metadata 대조를 저장한 실제 명령은 다음이고 rc0이었다.

```bash
python3 independent-review/inspect.py
```

cwd는 `/Users/jake/Projects/ai-native-sdlc-sample/.local/experiments/private/0039-intent-design-alignment-muse/`다.
`independent-review/inspect.py`, `inspect.stdout/.stderr`, `comparisons.json`, `public-tool-events.json`,
`inputs.json`에 수행 코드·결과·입력 경로/해시·공개 도구 event 전문을 남겼다.

source-validation의 **151개 파일**을 maker Git의 `git show b579ebb:<path>`와 직접 대조했고
불일치가 없었다. 제출판의 모든 팀/작성 skill·동반 자료·검증자와 설치 manifest의 해시도 같았다.
manifest에 포함된 로컬 `.opencode/.gitignore`는 커밋에 없는 runtime 보조 파일이며, source skill이나
검증자 누락이 아니다. 제출/설치판/fixture main의 별도 SHA와 149개 설치·fixture manifest를 읽었다.

root가 실제 실행한 `final-validation/product-unittest`는 제출 clone에서 rc0, 5시험 모두 통과했다.
`product-pycompile`는 임시 cfile을 사용해 tracker와 두 시험 모듈을 컴파일했고 rc0이었다.
`independent-cli.json/events.jsonl`의 11건은 표준 출력/오류/종료 코드와 바이트 보존을 기록한다.
이 검토자는 위 실행 전문과 독립 기대를 만드는 `oracle.py`를 읽었으며 재실행하지 않았다.
expectation은 HUMAN 결정과 비정렬 fixture에서 계산하고 구현 출력을 정답으로 복사하지 않았다.

### 실제 대화·판정 대조

첫 두 snapshot의 intent는 baseline `d3c23f3`와 같은 바이트이고 diff의 변경 경로는 spec·plan·색인뿐이다.
owner 필터는 기존 비교 목적을 이어받는 spec 근거를 남겼다. 이유 없는 정렬 제안은 파일 순서 제약과
충돌한다고 설명하고 Q2 미정으로 보존했으며 코드나 순서 계약에 먼저 편입하지 않았다.
HUMAN 3차 원문은 기본/owner 목록 모두 ID 오름차순과 그 이유, 구현·검증·로컬 커밋을 명확히 허가한다.
이 결정 뒤 추가 승인을 요구하지 않고 intent 제약과 하류 문서를 개정했다.

설계 개정의 선후는 같은 커밋만으로 추정하지 않았다. `03-accept-and-implement.jsonl`의 공개
tool event 행7(intent edit)→10(spec write)→13(plan write)→23/26(tracker edit)→29/30(시험)를
직접 읽었다. 기존 3시험 baseline은 개정 전 현재 baseline을 확인하는 실행이며 이후 코드 구현/
계약 개정 순서의 위반으로 세지 않는다. 구현 후 AST/5시험, native 검토 결과 반환, 로컬 commit,
commit 뒤 5시험 재실행과 CLEAN까지 실제 도구 출력이 있다. 시험의 ID 순서 기대 개정은 HUMAN
제약 변경에 근거하고 show/complete/반복 무쓰기 검증은 보존했다. non-TDD 선택 자체는 결함이 아니다.

parent의 실제 read/skill event는 `design-spec`, `plan`, `spec-policy-pass`, `brand`,
`data-compliance`와 제품 PROCESS/계약/정책을 보여준다. 첫 두 작성 스킬은 HUMAN이 명시 지정했다.
feedback 본문의 read/skill event는 없으므로 자연 선택·본문 실제 읽기·전체 feedback 효과는 미관측이다.
미관측을 스킬 미적용의 확정이나 기존 지침의 부재로 바꾸어 판정하지 않는다.

named native 검토는 `subagent_type: sdlc-verifier`로 한 번 dispatch됐다. 공개 child metadata는
parentID와 `agent: sdlc-verifier`, `opencode-go/muse-spark-1.3-contributor`/`xhigh`를 확인하며
parent/child가 같은 모델/variant라는 사실을 보존한다. `verifier.stdout`의 실제 debug prompt는
설치된 verifier body와 동일하다. 즉 기준이 구성된 named agent 선택과 공개 보고 반환을 확인했다.
숨은 model prompt나 내부 추론을 추가 열람한 것은 아니며, 구성/선택 증거를 모든 기준 준수 보장으로
확대하지 않는다. child는 코드·시험·미커밋 diff·정책·intent/spec/plan을 실제 읽고 임시 fixture를
검사해 동작 영향 발견 없음으로 보고했다. task는 completed 결과 전문을 parent에 반환했다.
이 검토는 commit 전의 동작 중심 범위이며 HUMAN 원문/실제 편집 선후/commit 후 상태를 직접
확인하지 못했다고 스스로 남겼다. 이 검토자가 후속 공개 원문과 제출판으로 그 사실을 보강했다.

실제 parent는 3회, native child는 1회이며 모두 Muse Spark/xhigh다. 세 dispatch 합계393.420초,
첫 dispatch부터 마지막 종료까지621.758초(약10분22초)는 meta timestamp/elapsed와 일치한다.
런 rc0·timeout 없음과 도구 실패를 구별했다. 첫 read의 `docs/REVIEW.md` 부재는 같은 턴의 실제
`REVIEW.md` 읽기로 복구했다. parent/child의 기본 py_compile 캐시 권한 실패·AST 대체와 root의
임시 cfile 컴파일은 다른 실행이다. tar filter 미지원·catalog 총수 assertion·export database lock의
최초 실패와 복구도 보존되어 있다. 공개 original-public 도구 본문에는 truncation marker가 없었다.

### 발견 목록

**[Compliance / Important — 제품 인계] 최종 plan의 현재 요약은 실제 제출 상태와 불일치한다.**
제품 `changes/0001-request-comparison/plan.md`의 현재 요약은 `완료(예정)`,
`미검증: T01 실행 전체`, `다음 한 단계: T01을 실행한다`를 그대로 남겼다. 실제 `921432a`는
intent/spec/plan·색인·tracker·시험7파일을 커밋했고 5시험/독립 CLI는 통과했으며 색인도 로컬
인도·HUMAN 수락 대기로 개정됐다. 새 담당자가 끝난 T01을 다시 실행하거나 완료 근거를 잃을 수
있으므로 표현 취향 수준의 nit가 아니다. 원 제출판은 수정하지 않아 최초 누락을 보존했다.
후속 제품 인계를 실제로 진행한다면 개발자가 plan의 실제 판·완료/미검증·다음 일을 갱신해야 한다.
이번 실험 관측과 원본 보존을 마치기 위해 모델을 추가 실행하거나 제품 제출을 사후 수정할 이유는 없다.

source feedback의 `When later test or review evidence changes what remains`, PROCESS의 인계 절,
명시 사용한 plan skill의 `Rewrite the current summary and next work`와 verifier의 pause/handoff
criteria에 이미 같은 요구가 있다. source의 중요한 계약 누락보다는 이번 적용/검토의 누락이다.
native 검토는 이를 발견하지 않았지만 commit 전/동작 중심 검토의 반환을 최종 인계 전체 통과로
취급해서는 안 된다. 한 사례를 이유로 새 강제 hook·인계 장부·항상 묻는 단계·모델 호출을 추가할
근거는 없다. Bugs/Security 관점에서는 합성 fixture와 선언된 CLI 범위 안에서 추가 중요한 발견이 없다.

### maker 결과 기록과 남은 한계

현재 maker의 6개 변경을 읽었다: 0039 보고서, 실험 README의0039 색인, 정본 README의 후속
활성 적용 절, maker T15 현재 인계, OpenCode README의0039 근거, North Star V3-09의0039 주석이다.
새 실험 색인 행은 T15 실제 경로 목록에도 연결했고 같은 partial 범위를 유지한다. 핵심 세 사건의
관측·제품 동작 통과·최초 plan 인계 누락/전체 partial·명시 스킬/feedback 읽기 미관측·정확한
source/제출판·3+1/시간·실패/복구를 실제 공개 원문과 일치하게 기록했다. 중요한 새 보고 과장은 없다.
0038의 최초 부분 판정과 전체 AC04 유예, source 설치와 도구 행동의 차이를 유지한다.

이번 후속 대조가 원 제품 plan 누락을 해소하거나 인계 새 세션을 실행한 것은 아니다. 정확한 현재
요약의 복구, 추천 전제 반증의 다른 분기, 큰 설계 누적, 다른 도구/모델, 자연 feedback 선택,
개별 인과 효과, 전체 SDLC/AC04는 미입증이다. 원격 PR/main 통합·배포·전역 설치는 이번 범위 밖이다.
maker의 마지막 기록 commit과 그 resulting content/공개 보존 hashmanifest는 root의 후속 인도 작업이다.
검토자는 발견을 보고하며 승인·병합·전체 SDLC 통과를 선언하지 않는다.
