# 독립 verifier 초기 스냅샷

2026-09-11T03:41:38Z. Reviewer: spec_final_verifier, gpt-5.6-sol / high.
Maker HEAD ac0963b, 기준 a734b29. 아래는 반환한 네 부분 보고를 root가 정리한 기록이다.
검증자는 프로젝트를 고치지 않았고 로그는 /tmp에서 이 폴더로 복사했다.

당시 판정은 **FAIL**이었다. make check와 명시 Proof는 통과했으나 사용판 선택 스킬에 적용한
Codex quick_validate가 실패했고, 아직 리뷰/실험 중이라 계획의 색인·주석 3파일이 반영 전이었다.
이를 검사 전체가 통과한 것으로 바꾸지 않는다. 후속 확인은 별도 최종 보고에 남긴다.

## 1. 실행 명령과 종료 코드

- `make check`: rc=0. [전체 출력](make-check.log).
- `python3 -m unittest -v tests/test_eval_plugin.py tests/test_team_harness.py`: rc=0, 20 tests.
  [Proof 이름·출력](proof-python-v.log).
- `bash -v tests/test_evals.sh`: rc=0. [출력](test-evals-v.log).
- `bash evals/check.sh evals/cases/03-spec-carries-questions.json evals/testdata/03-pass/result.json`:
  rc=0, 5/5. 같은 case의 `03-fail-carry/result.json`: 예상 rc=1. [대조 출력](proof-03.log).
- `/tmp/intent-form-validation-venv/bin/python /Users/jake/.codex/skills/.system/skill-creator/scripts/quick_validate.py`
  뒤에 maker `.claude/skills/design-spec`을 준 검사: rc=0. adopter의
  `examples/skills/capture-intent`와 `examples/skills/design-spec`을 준 검사: 각각 rc=1.
  [출력](quick-validate.log), [adopter design 출력](quick-validate-adopter-design.log).
- `printf deliberately-not-json | .claude/hooks/production-gate.sh`: 예상 rc=2.
  [차단 출력](hook-bad-input.log).
- `env -u ANTHROPIC_API_KEY make evals`: 예상 rc=2, SKIP. [출력](make-evals-no-key.log).
- `git diff --name-status main...HEAD`, `git diff --name-status a734b29`, untracked와
  adopter add296d 기준 diff, 이전 `540ce05..a734b29` diff와 0020 plan 대조.
  [범위 로그](scope.log).
- R1 31개 해시와 결합 해시 재계산, HTML의 해시와 a734b29 대비 무변경 확인: 모두 일치.

## 2. 관측

make check는 Python 96개 중 1 skip, hooks 28/28, deterministic evals 8/8,
managed settings PASS였다. 첫 비의도 실패는 아래 Codex validator 출력이다.

```text
Unexpected key(s) in SKILL.md frontmatter: disable-model-invocation. Allowed properties are: allowed-tools, description, license, metadata, name
```

의도한 Q1 누락 음성은 다음대로 실패해 기준이 유지됐다.

```text
FAIL  [2] regex_present spec.md — 패턴 불일치: /^- Q1 (answered|carried forward):/
```

skip은 대소문자를 구별하지 않는 파일시스템 때문에 해당 구별 사례를 실행할 수 없어서다.
[skip 상세](skip-detail-v.log). 31개 후보·11개 parity는 당시 영수증과 일치했다.

## 3. 계획 대조

현재 수정에 계획 밖 파일은 없었다. 당시 반영 전인 예정 파일은 README.md,
docs/research/sdlc-documentation/README.md, docs/verification/north-star-playbook.html 세 개였다.
adopter의 15개 변경은 계획 범위와 맞고 제품 코드·제작 검증 자산이 없었다.
이전 0020의 540ce05..a734b29 범위도 당시 plan과 양방향으로 일치했다.

## 4. 미확인과 검사 적용 범위

API key 없는 semantic eval, 진행 중인 모델 리뷰·대화 실험, 후속 수정은 미확인이다.
이 기계 검증은 문서 의미 리뷰와 조직 승인을 대신하지 않는다.

Root 후속 조사: 이 quick_validate는 Codex용으로 허용 키 다섯 개만 검사한다. 사용판은 기존부터
Claude Code 선택 예시로 `disable-model-invocation: true`를 둔다. Claude Code 공식
[frontmatter 설명](https://code.claude.com/docs/en/skills#frontmatter-reference)을 2026-09-11에
열어 이 옵션이 지원됨을 확인했다. 따라서 사용판 실패는 도구의 플랫폼 범위 불일치이며,
선택성을 지키는 키를 지우거나 검사 코드를 수정해 숨기지 않는다. 최종 verifier가 유효 YAML과
해당 옵션·자료 범위를 별도로 대조한다. 이는 Claude 런타임의 자동 발견/호출 시험은 아니다.
