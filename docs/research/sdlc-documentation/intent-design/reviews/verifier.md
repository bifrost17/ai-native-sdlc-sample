# 독립 verifier 보고

2026-09-11. Reviewer: `intent_final_verifier`, `gpt-5.6-sol` / `high`.
아래는 독립 검증자의 결과와 후속 명령 확인을 root가 네 부분으로 정리한 기록이다.
검증자는 프로젝트 파일을 고치지 않았고 검사 로그는 /tmp에 저장했다. root가 같은 로그를 이 폴더에 복사했다.

## 1. 실행한 명령과 종료 코드

전체 검사, rc=0. 로그 SHA256: `32612c4b61f92d1ce79d9be60a5c408e969ffac956145b55aa1ee0647e356877`.

```sh
make check > /tmp/intent-0020-make-check.log 2>&1; check_rc=$?; printf '\nMAKE_CHECK_EXIT=%s\n' "$check_rc" >> /tmp/intent-0020-make-check.log; cat /tmp/intent-0020-make-check.log; exit "$check_rc"
```

명시한 proof의 실행 이름 확인, rc=0, 30개 통과:

```sh
python3 -m unittest -v tests/test_skill_template.py tests/test_detect_bands.py tests/test_bands_workflow.py
```

건너뛴 검사의 이름과 환경 이유 확인, rc=0:

```sh
python3 -m unittest -v tests.test_hook_paths.HookPathTests.test_filesystem_case_aliases_protect_future_paths tests.test_hook_paths.HookPathTests.test_case_sensitive_distinct_directories_remain_unprotected tests.test_eval_regex.EvalRegexTests.test_unreadable_regular_file_is_undecidable
```

스킬 검사 rc=0, 잘못된 훅 입력 rc=2(예상된 차단):

```sh
/tmp/intent-form-validation-venv/bin/python /Users/jake/.codex/skills/.system/skill-creator/scripts/quick_validate.py .claude/skills/capture-intent
printf %s deliberately-not-json | .claude/hooks/production-gate.sh
```

범위 대조 명령은 모두 rc=0:

```sh
git diff --name-status main...HEAD
git show --name-status 540ce05
git diff --name-status 540ce05
git ls-files --others --exclude-standard
git diff --name-status c190fc7^..5d67b0f
git diff --check 540ce05 --
git diff --cached --name-status 540ce05
git diff --name-only
```

R2 다섯 파일의 개별·합산 SHA256을 작업 트리와 index에서 각각 재계산했다. 두 결과 모두
`4d8431b42d872243d71ac727eef2086ed474be53856da1d2eb4a3d78bdd3a118`로 영수증과 일치했다.

## 2. 관측 결과

make check: unittest 96개 중 1 skip, hooks 28 passed, eval fixtures 8 passed,
managed settings PASS. 실패 행 없음. [전체 로그](make-check.log).

건너뛴 검사는 파일시스템의 대소문자 별칭 특성 때문이다:

```text
test_case_sensitive_distinct_directories_remain_unprotected ... skipped 'this filesystem aliases differently-cased directories'
```

훅의 잘못된 JSON 입력은 다음과 같이 차단됐다. 실행 전후 git status는 같았다:

```text
[production-gate.sh] BLOCKED: hook input is not valid JSON; refused. Route: run the hook with a Claude Code PreToolUse/PostToolUse JSON on stdin.
```

emit_intent.py는 현재 템플릿의 다섯 `##` 제목을 순서대로 읽고 출력 2행에 작성자/draft를 쓴다.
자동 intent 생성과 2σ 진단 인계·3σ 제안 생성, 스킬 펜스와 템플릿의 바이트 동일성을 포함한
[30개 proof 검사](proof-tests.log)가 통과했다. [스킬 검사 출력](skill-validate.log)은 `Skill is valid!`이다.

## 3. plan.md 불일치

없음. main부터 540ce05까지 201개 경로는 사전 조사 보존분이다. 이를 구분한 0020 변경은
plan의 Files that change 안에 들어간다. 이전 0019의 `c190fc7^..5d67b0f` 자체 diff 20개
경로도 당시 plan과 양방향으로 일치하며, 시작 커밋의 ancestry를 확인했다.

후속 staged 점검 시 기준 540ce05 이후 38개 경로가 있었다. 현재 staged 36개와 이미 커밋한
0020 intent/spec 2개이며, 모두 선언된 범위다. 그 시점의 unstaged·untracked는 없었다.
이는 root가 이 보고서와 추가 완료 문구·CLI 내보내기 기록을 더하기 전의 스냅샷이다.

## 4. 확인하지 못한 것

- 검증 이후 root가 추가한 이 보고서·완료 문구·CLI 내보내기 기록 및 최종 커밋 자체는 당시 없었다.
  해당 후속 산출물은 root가 같은 선언 범위, 링크, diff와 R2 해시로 최종 확인한다.
- 실제 요청자 대화에서의 스킬 동작, 호스티드 PR·CI, 조직 승인·merge는 이번 범위 밖이다.
- 문서 의미 평가는 Astra/Fable의 독립 리뷰에 맡겼으며 이 verifier가 그 결론을 새로 판단하지 않았다.
