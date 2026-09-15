# 0013 — 플레이북 통제 보완 1·2·4 검증 기록

프로젝트 오너가 “3번 빼고 나머지 우선 보완”을 지시한 범위다. 기준은 [북극성 플레이북](north-star-playbook.html)의 해당 문단이며, 새 승인·문서 형식 검사기는 만들지 않았다.

- 구현 핀: `91727d2` (`codex/playbook-controls`).
- 비교 기준: `7aae55f` — 북극성 이름과 프로젝트 목표를 정리한 상태.
- 체인: [intent](../../intent/0013-playbook-controls/intent.md) → [spec](../../intent/0013-playbook-controls/spec.md) → [plan](../../intent/0013-playbook-controls/plan.md).
- 시점: 2026-09-10. 로컬 변경·검증만 수행했으며 PR·머지·배포는 실행하지 않았다.

## 무엇을 보완했는가

| 우선순위 | 수정 | 플레이북 주석 |
|---|---|---|
| 1 | 훅의 경로를 cwd·점 구간·심볼릭 링크·새 파일·파일시스템 별칭까지 해석한다. 논리적 보호 경로와 실제 대상을 함께 확인하고, 린트도 실제 파일에 실행한다. 오류는 차단한다. | V6-14, V8-10 |
| 2 | spec 지침이 로컬·로드된 플러그인 스킬을 함께 확인하며 실제 출처·판을 기록한다. 평가 실행기는 현재 조직 플러그인을 명시적으로 로드하고, 조직 스킬·정책·템플릿 변경도 CI 평가 대상에 넣는다. 정책 적용 사례를 추가한다. | V3-01, V3-14, V6-05, V9-07 |
| 4 | none/1σ는 기록, 2σ는 읽기 전용 진단, 3σ는 진단을 포함한 제안 초안으로 분기한다. 모델은 Read/Grep만 쓰고 스크립트가 결과를 저장한다. 미실행을 표시하고 실패를 비0으로 전파하며 탐지·실행 기록을 보존한다. | V13-02, V13-07, V13-09 |

2σ도 가이드의 intent 형식으로 진단 산출물을 남긴다. 이는 코드 수정이나 PR 제안 권한이 아니다. 3σ의 초안 역시 사람이 분류한 뒤 PR로 이어지는 기존 경계를 유지한다. 키 없는 3σ 초안에는 모델 진단 미실행을 명시한다.

`evals/check.sh`의 정규식 판정과 의미적 assertions 채점(우선순위 3)은 변경하지 않았다. 기존 테스트 파일도 수정하지 않고 새 회귀 시험 세 파일을 추가했다.

## 반례와 회귀 시험

작업자들은 구현 전에 새 시험을 실행했고, 독립 교차 검토에서 발견한 반례도 추가했다.

| 범위 | 수정 전 | 수정 후 |
|---|---|---|
| 경로 해석 | 16개 메서드, 37 subtest failures | 기본 경로 시험 통과 |
| macOS 대소문자 별칭 | `.GITHUB`·`TESTS`가 실제 보호 디렉터리와 같은데 허용됨. 확장한 20개 메서드에서 7 failures, 1 skipped | 20개 메서드, OK (skipped=1) |
| 조직 플러그인 실행 | 5개 메서드에서 11 subtest failures | 5개 메서드, OK |
| bands 실행 | 실행기 부재로 초기 8개 메서드에서 6 failures·3 errors | 오류 envelope·출력 저장 실패를 추가한 최종 11개 메서드, OK |

대소문자를 구분하는 파일시스템의 정상 대조 한 건만 이 Mac에서 생략된다. 실제 Mac의 대소문자 별칭, 보호 경로가 밖을 가리키는 링크, 새 파일, cwd, 잘못된 경로, 정상 파일은 시험했다. Linux에서 별개인 대문자 디렉터리를 무조건 소문자로 취급하지 않는다.

교차 검토에서 추가로 잡은 bands 반례는 rc=0이지만 `is_error=true`인 Claude 결과와 모델 출력 파일 저장 실패였다. 둘 다 실패로 처리하고 가능한 실행 기록에 원인을 남기도록 수정했다. verifier는 키 없는 2σ가 모델·초안 없이 `diagnosis_skipped/skipped_no_api_key`를 남기는 것도 별도로 확인했다.

## 실제 Sonnet 실행 — 프로세스 성공, 문자열 평가 실패

[정제된 실행 증거](0013-policy-evidence.json)는 실행 인자, 모델 이름, 파일 도구 호출 순서, 생성된 spec 전문과 채점 결과를 담는다. 계정 정보·세션 식별자·모델의 숨겨진 추론·관계없는 도구 반환값은 보존하지 않았다.

Claude Code 2.1.265의 로그인된 로컬 계정으로 `04-org-policy-application`만 실행했다. 사용자가 비용 선호를 알려준 뒤 기본 설정으로 시작됐던 Opus 실행은 중단(rc=143)했고, `--model sonnet --effort low`로 다시 실행했다. 관측 모델은 `claude-sonnet-5`, 완료 시간은 136,666ms, 프로세스 rc=0, 결과 `success/is_error=false`다.

현재 플러그인을 `--plugin-dir <repo>/org-skills`로 로드했다. 도구는 `Read,Write,Glob,Grep,Skill`, Write 승인 경로는 사례의 임시 작업 디렉터리로 한정했다. Bash·커밋·PR 도구는 제공하지 않았다. API 키가 필요한 전체 `evals/run.sh`나 GitHub Actions를 실행한 것은 아니다.

기록에서 spec 작성 전에 다음 본문 Read를 확인했다.

- `org-skills/skills/spec-policy-pass/SKILL.md`
- `org-skills/skills/brand/SKILL.md`
- `org-skills/skills/data-compliance/SKILL.md`
- `org-skills/skills/secure-api-review/SKILL.md` 및 로컬 보안 스킬
- `org-skills/skills/ux-copy/SKILL.md`
- `org-skills/.claude-plugin/plugin.json`

생성 spec에는 절대 시각·KST, 직원 이메일/전화번호의 응답·로그 제외, 내부 ID와 UTC 접근 이력, 90일 보존 충돌의 정책 오너 이관, 인증된 포털 세션, 오류의 다음 행동이 반영됐다. plugin manifest 0.1.1은 기록하고 Git 판은 미확인으로 남겼다. 이는 실제 읽기와 일부 적용을 관측한 한 사례다. 모든 의미적 assertion의 충족이나 오너 수락을 증명하지 않는다.

기존 채점기를 그대로 실행한 결과:

```text
bash evals/check.sh evals/cases/04-org-policy-application.json evals/out/04-org-policy-application.sonnet.json
CASE 04-org-policy-application (11 판정 · evals/out/04-org-policy-application/ws)
  PASS  [0] file_exists spec.md
  PASS  [1] contains spec.md
  PASS  [2] contains spec.md
  PASS  [3] contains spec.md
  PASS  [4] contains spec.md
  PASS  [5] contains spec.md
  PASS  [6] contains spec.md
  PASS  [7] contains spec.md
  PASS  [8] contains spec.md
  FAIL  [9] contains spec.md — 없어야 할/있어야 할 문자열: gateway JWT
  PASS  [10] contains spec.md
04-org-policy-application: 10 passed, 1 failed
rc=1
```

실제 spec의 R5에는 `게이트웨이 JWT`가 있다. 이 실패를 없애려고 사례의 검사 문자열을 완화하거나 모델 산출물을 손으로 고치지 않았다. 정책 출처 인용과 충돌 처리 표현의 의미적 품질도 사람이 검토할 부분이다.

## 후속 요청 — Claude Code 영구 설치

실제 정책 사례 실행 후 사용자가 영구 설치를 허용했다. 현재 저장소를 로컬 마켓플레이스로 사용자 설정에 등록하고 `intent-sdlc-skills@intent-sdlc-skills` 0.1.1을 user 범위로 설치·활성화했다. 아래 명령은 모두 rc=0이다.

```text
claude plugin validate org-skills
claude plugin validate .claude-plugin/marketplace.json
claude plugin marketplace add /Users/jake/Projects/ai-native-sdlc-sample --scope user
claude plugin install intent-sdlc-skills@intent-sdlc-skills --scope user
claude plugin list --json
```

`--plugin-dir` 없이 새 Sonnet·low 세션을 실행했다(Read/Glob만 제공, 쓰기 없음). init 기록에는 `source: intent-sdlc-skills@intent-sdlc-skills`, `version: 0.1.1`이 나타났고, `spec-policy-pass/SKILL.md`와 해당 manifest를 읽은 뒤 rc=0으로 완료했다. 따라서 다음 세션의 자동 로드를 확인했다.

설치 메타데이터의 경로는 `/Users/jake/.claude/plugins/cache/intent-sdlc-skills/intent-sdlc-skills/0.1.1`이다. 다만 이 로컬 마켓플레이스에서는 실제 세션이 현재 저장소의 `org-skills`를 플러그인 경로로 해석했다. 독립된 설치 캐시에서의 전체 정책 평가나 업데이트 전파를 시험했다고 주장하지 않는다. 자세한 설치·새 세션 증거는 [증거 JSON](0013-policy-evidence.json)의 `permanent_installation`에 있다.

## 전체 로컬 검증 결과

`make check` rc=0. 출력의 종료 결과는 다음과 같다.

```text
python3 -m unittest discover -s tests
Ran 55 tests in 9.343s
OK (skipped=1)
test_hooks: 28 passed, 0 failed
8 passed, 0 failed
PASS  managed-settings 키·훅 계약
```

위 `8 passed`는 모델을 쓰지 않는 기존 채점기·스키마 시험이다. 앞의 실제 Sonnet 사례가 평가를 통과했다는 뜻은 아니다. `git diff --check`도 rc=0이었다.

## verifier 보고

`.claude/agents/verifier.md`를 읽은 별도 작업자가 다음을 수행했다. 이 작업자는 훅 작성자이므로 훅 작성과 완전히 독립된 검증자는 아니다. 훅은 다른 정책 작업자가 독립 검토해 Mac 별칭 반례를 찾았고, 수정 후 이 verifier가 전체 시험과 이웃 흐름을 실행했다. bands도 다른 작업자의 독립 검토에서 오류 반례를 찾아 수정했다.

### 1. 실행한 명령과 종료 코드

```text
make check
rc=0 — Ran 55 tests in 9.302s; OK (skipped=1)
test_hooks: 28 passed, 0 failed
8 passed, 0 failed
PASS  managed-settings 키·훅 계약

python3 -m unittest discover -s tests -p test_hook_paths.py -v
rc=0 — Ran 20 tests in 5.249s; OK (skipped=1)

python3 -m unittest discover -s tests -p test_eval_plugin.py -v
rc=0 — Ran 5 tests in 2.740s; OK

python3 -m unittest discover -s tests -p test_bands_workflow.py -v
rc=0 — Ran 11 tests in 2.032s; OK

git diff --check
rc=0

git diff --name-only main...HEAD
git diff HEAD --name-only
git ls-files --others --exclude-standard
git diff --name-only main -- tests
git diff --exit-code main -- evals/check.sh
모두 rc=0

git diff --name-status 76d4c4c^1 76d4c4c
rc=0

printf '%s' '{broken' | bash .claude/hooks/protect-paths.sh
rc=2 — 의도한 차단

bash evals/check.sh evals/cases/04-org-policy-application.json evals/out/04-org-policy-application.sonnet.json
rc=1 — 10 passed, 1 failed
```

세 Proof 시험 파일의 이름을 `-v` 출력과 대조했고, 임시 디렉터리에서 키 없는 2σ도 확인했다.

### 2. 관측 결과와 첫 실패

로컬 `make check`에는 실패가 없다. 실제 모델 평가의 첫 실패는 위의 `gateway JWT` 문자열이다. 잘못된 훅 JSON은 다음 설명으로 차단됐다.

```text
[protect-paths.sh] BLOCKED: hook input is not valid JSON; refused. Route: run the hook with a Claude Code PreToolUse/PostToolUse JSON on stdin.
```

### 3. 계획과 대조

구현 파일은 계획과 일치하며, 기존 테스트·채점기는 변경하지 않았다. 초기 북극성 이름 변경과 프로젝트 목표 문서는 앞선 수정 보존 항목으로 구분했다.

verifier의 중간 스냅샷에는 증거 JSON의 계획 기재와 보고서·색인 작성이 남아 있었다. 이후 `91727d2`의 plan에 `0013-policy-evidence.json`을 명시했고 이 보고서와 README·CHAPTERS·INDEX 및 주석의 핀을 갱신했다. verifier의 최종 문서 확인에서 이 대기 항목은 모두 해소됐다. 계획 기재·파일 존재·로컬 링크 13개·원문 보존·지정한 주석 9개·집계와 `git diff --check`가 모두 통과했다. 그 뒤의 영구 설치는 root가 별도로 위와 같이 확인했다.

이웃 흐름인 체인 0012는 당시 계획에 `README.md`, brand 출처 문서 변경, brand 예시·검사 스크립트와 예시 프로젝트 정책 추출이 명시되지 않았다. 핵심 정책 분리·스킬 이동은 일치했다. 이는 이전 체인의 기록상 차이며 이번 수정 범위에 포함하지 않았다.

### 4. 확인하지 못한 범위

- 대소문자를 구분하는 실제 파일시스템 대조 한 건.
- 전체 실제 모델 평가, 운영 bands의 실제 Claude 진단, 호스티드 CI.
- 설치 캐시의 갱신과 판 추적, 사람이 정책 충돌을 검토하고 수락하는 전체 개발 사슬.
- 제외된 3번의 의미적 assertions·정규식 채점 보완.

## 북극성 반영

구현 근거와 위 관측 범위를 아홉 주석에 반영했다. V3-01·V3-14는 부분을 유지한다. 다른 해당 판정도 유지하므로 전체 집계는 **179블록 · 충실139 · 부분23 · 팀몫17**이다. 플레이북 원문에는 손대지 않았다. 비교에서 제외하는 것은 `details.verify` 평가 블록과 핀을 알리는 기존 검증 머리말 한 문단뿐이다.
