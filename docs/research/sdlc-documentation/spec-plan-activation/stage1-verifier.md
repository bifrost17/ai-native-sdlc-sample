# 단계 1 독립 verifier 보고

2026-09-11. 검증자 `activation_verifier`, 모델·추론 `Sol/high`.
검증 범위는 `185dd5e`에서 활성 소스 고정 커밋 `0f0f3ce`까지의 단계 1
활성 템플릿·스킬·사용판, 전체 `make check`, 이전 0023 이웃 사슬과 설정 훅의
의도적 bad input이다. 단계 2 설치, 단계 3 제품 실험과 단계 4 최종 주석은 진행 중인
후속 범위로 구분하며 이 보고에서 불합격으로 판정하지 않는다.

검증 판정: **단계 1 PASS. 중요한 plan 불일치 없음.** 소스 수정은 하지 않았습니다.

## 1. 실행한 명령

- `make check` — `0f0f3ce` 고정 후 재실행, `rc=0`

```text
python3 -m unittest discover -s tests
..............................................................s.................................
----------------------------------------------------------------------
Ran 96 tests in 30.412s

OK (skipped=1)
bash tests/test_hooks.sh
ok   protect-paths: .github blocked (rc=2)
ok   protect-paths: Makefile blocked (rc=2)
ok   protect-paths: .claude/hooks blocked (rc=2)
ok   protect-paths: settings.json blocked (rc=2)
ok   protect-paths: accepted intent passes (PO reviews it, not the hook) (rc=0)
ok   protect-paths: src file passes (rc=0)
ok   protect-tests: fix task, test file blocked (rc=2)
ok   protect-tests: fix task, src passes (rc=0)
ok   protect-tests: no fix task, test passes (rc=0)
ok   no-secrets: AWS key blocked (rc=2)
ok   no-secrets: password literal blocked (rc=2)
ok   no-secrets: plain edit passes (rc=0)
ok   format-lint: broken .py reported (rc=2)
ok   format-lint: broken .sh reported (rc=2)
ok   format-lint: valid .py passes (rc=0)
ok   format-lint: valid .sh passes (rc=0)
ok   production-gate: unapproved prod deploy blocked (rc=2)
ok   production-gate: approved prod deploy passes (rc=0)
ok   production-gate: staging deploy passes (rc=0)
ok   fail-closed: broken JSON blocks (rc=2)
ok   fail-closed: no jq blocks (rc=2)
ok   wiring: settings.json is valid JSON
ok   wiring: protect-paths.sh wired and executable
ok   wiring: protect-tests.sh wired and executable
ok   wiring: no-secrets.sh wired and executable
ok   wiring: format-lint.sh wired and executable
ok   wiring: production-gate.sh wired and executable
ok   decision log: block appended (2026-09-11T10:45:38Z protect-paths.sh block Makefile)
test_hooks: 28 passed, 0 failed
bash tests/test_evals.sh
PASS  1. 케이스 전량 스키마
PASS  2. 통과 픽스처 rc=0 (01-pass = capture-intent 스킬대로 손으로 쓴 intent)
PASS  3. 위반 픽스처 rc=1+FAIL
PASS  4. 없는 파일/워크스페이스 → rc=2
PASS  5. 닫힌 집합 밖 kind → rc=2
PASS  6. run.sh 키 없음 → rc=2+SKIP
PASS  7. jq 없는 PATH → rc=2
PASS  8. 셸 구문

8 passed, 0 failed
bash tests/test_managed_settings.sh
org/managed-settings.example.json 키 11개 전부 공식 목록 안
PASS  managed-settings 키·훅 계약
```

- `git diff --check 185dd5e..0f0f3ce` — `rc=0`
- `git diff --name-only 185dd5e..0f0f3ce` — 65개 경로, 계획 경로군 밖 출력 없음.
- `claude plugin validate --strict --json ./org-skills` — `rc=0`, `success: true`, errors/warnings 없음.
- `claude plugin validate --strict --json .claude-plugin/marketplace.json` — `rc=0`, `success: true`, errors/warnings 없음.
- 활성판과 사용판의 작성 문서/양식 로컬 링크 검사 — 각각 104개 확인, 누락 0.
- 사용판 `787af77..fbc23c0` — 45개 파일, worktree clean.
- 기존 작은 examples 15개를 `185dd5e`와 대조 — 변경 0.
- 이전 0023 이웃 사슬:

```text
git diff --name-status 65a509a..abd6b28
core_changed_count=116
계획 경로군 밖 출력 없음

git diff --name-status 82d7ad2..787af77
use_changed_count=12
계획 경로군 밖 출력 없음
```

`main`은 현재 base `185dd5e`와 0023 base `65a509a` 양쪽의 조상이므로, 각각 최신 로컬 main을 포함한 결과에서 검사했습니다.

- `.claude/settings.json`에 연결된 `protect-paths.sh`를 격리된 임시 복사본에서 의도적 bad input인 `Makefile` Edit로 실행 — 예상한 `rc=2`

```text
[protect-paths.sh] BLOCKED: Makefile is a frozen path (.github/* Makefile .claude/hooks/* .claude/settings.json). Reason: CI wiring, the make targets and the hooks are the feedback loop itself; an agent must not loosen them mid-task. Route: a human changes it in its own PR, or edits PROTECTED in this hook in that PR.
HOOK_EXIT_CODE:2
```

## 2. 관측 결과

`make check`의 첫 실패 줄은 **없습니다**. 전체 결과는 96 tests OK, hooks 28/28, deterministic eval fixtures 8/8, managed settings PASS입니다. `skipped=1`은 테스트 러너가 명시한 기존 skip입니다.

한 번 잘못 호출한 명령은 보존합니다.

```text
claude plugin marketplace validate --strict --json .
error: unknown command 'validate'
rc=1
```

이는 제품 검증 실패가 아니라 존재하지 않는 하위 명령 호출이었습니다. 올바른 `claude plugin validate --strict --json .claude-plugin/marketplace.json`으로 바로잡아 `rc=0`을 확인했습니다.

후보→활성→사용판의 byte 차이는 배치에 따른 상대 링크와 명시된 사용판 포장 차이였습니다. `spec-policy-pass`, `tdd`, `PROVENANCE`, `spec-policy` 명령은 후보와 활성판이 byte-identical입니다. 사용판의 추가 차이는 자동 로드를 막는 `disable-model-invocation`, 사용판 안내, maker 전용 `INTENT_TASK=fix` 문구의 일반화입니다.

## 3. plan.md와 맞지 않는 점

**없음.**

- `185dd5e..0f0f3ce`의 65개 파일은 단계 1 활성 양식·스킬·교육 자료·팀 플러그인·사용 안내 및 계획에 선언된 연구/실험 입력 경로 안에 있습니다.
- 별도 사용판은 선언한 base `787af77`에서 `fbc23c0`으로 갱신됐고 깨끗합니다.
- 활성판/사용판의 필수 로컬 링크 누락이 없습니다.
- 현재 보이는 `docs/research/sdlc-documentation/spec-plan-activation/runtime/` untracked 경로는 소스 고정 뒤 시작된 단계 2 실행 증거이므로 단계 1 diff에 포함하거나 불일치로 세지 않았습니다.

## 4. 확인하지 못한 것

계획상 아직 진행 중인 후속 작업이므로 불합격으로 판정하지 않았습니다.

- 단계 2: 실제 0.1.5 설치/update/list, 캐시·소스 판, 새 정상 세션의 실제 로드와 적용.
- 단계 3: F04 제품 CLI 실험, 실제 RED→GREEN, PR1/PR2 통합, 공개 ON/OFF 및 문서 동기화.
- 단계 4: 최종 제품 독립 재검증, `docs/experiments/0024-spec-plan-activation.md`, 실험 색인과 북극성 주석 갱신.
- `make evals`의 외부 모델 semantic 실행은 `make check` 구성에 포함되지 않으며 현재 단계 1 Proof가 요구하는 기존 회귀도 아닙니다.
