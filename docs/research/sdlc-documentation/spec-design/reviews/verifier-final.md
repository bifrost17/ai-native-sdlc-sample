# 최종 독립 verifier 보고

Reviewer: spec_final_verifier, gpt-5.6-sol / high. 아래는 반환 보고 원문이며 로그만 이 폴더의
final-*.log로 복사했다. 검사 후 root가 이 보고서·로그와 완료 링크를 추가한다. 핵심 33파일은 그대로다.

최종 기계 검증 결론: 요청된 최종 불변조건은 모두 일치합니다. 단, adopter 두 skill의 Codex `quick_validate.py`는 rc=1 그대로이며 이를 PASS로 바꾸지 않았습니다. Claude Code 전용 필드에 대한 검사 도구 범위 차이입니다.

## 1. 무엇을 실행했는가

검사 스냅샷: `2026-09-11T04:03:00Z`

- maker HEAD `efc65d9e82639eefc35e93c89bcc693cfa408cd4`
- adopter HEAD `ca87cdb0fca215787b37bc9b981415427511c4e5`
- `make check` → rc=0
  - Python 96 tests, `OK (skipped=1)`
  - hooks 28/28
  - deterministic evals 8/8
  - managed settings PASS
- 03 양성 checker → rc=0, 5/5
- dropped-Q1 음성 checker → 예상 rc=1, Q1 패턴만 FAIL
- `candidate-r2.json`의 33개 파일 SHA와 combined SHA 재계산
- R1/R2 receipt 차이와 12개 maker/adopter parity 독립 재계산
- `a734b29` 이후 maker diff 및 untracked, `add296d` 이후 adopter diff 및 untracked 양방향 scope 검사
- north-star baseline/current HTML을 verify block과 외부 원문으로 분리해 SHA, ID, class, 변경 block 검사
- adopter 두 `SKILL.md`를 PyYAML `safe_load`로 읽고 필드 타입 확인
- maker/adopter 세 skill에 Codex `quick_validate.py` 실행
- probe receipt의 branch/path/HEAD, 보호 파일, artifact SHA, 최종 guidance 대응 검사
- API key를 제거하고 `make evals` 실행 → 예상 rc=2 SKIP

로그:

- `/tmp/spec0021-final-make-check.log`
- `/tmp/spec0021-final-proof-03.log`
- `/tmp/spec0021-final-receipt.log`
- `/tmp/spec0021-final-maker-scope.log`
- `/tmp/spec0021-final-adopter-scope.log`
- `/tmp/spec0021-final-scope-check.log`
- `/tmp/spec0021-final-north-star.log`
- `/tmp/spec0021-final-frontmatter-yaml.log`
- `/tmp/spec0021-final-quick-validate.log`
- `/tmp/spec0021-final-probe.log`
- `/tmp/spec0021-final-make-evals-no-key.log`
- `/tmp/spec0021-final-snapshot.log`

## 2. 무엇을 보았는가

R2 receipt는 정확히 33개 파일이며 개별 SHA 불일치가 0개였습니다. combined SHA도 다음 값과 일치했습니다.

```text
f4b37b76c06a28360bdf6bce56f2ebd3289b905b88d5135011ac6c43e337de02
```

R1→R2 변경은 receipt에 적힌 13개와 정확히 일치하며 삭제된 core 파일은 없습니다. 예시·template·design-depth의 12개 parity를 직접 비교해 모두 true였습니다.

north-star는 baseline HTML SHA와 receipt가 일치했고, verify 밖 원문 SHA는 전후 모두 다음 값입니다.

```text
31c395a2b617e4ca0b06c8ebb7d7a9d3c9aaa69c4afa46ac5338c53e1963ffdf
```

179개 verify ID와 class가 순서까지 동일하며 실제 변경 block은 정확히 `V3-02`, `V3-09`, `V3-10`뿐입니다.

Codex validator의 첫 실패 줄은 그대로 다음과 같습니다.

```text
Unexpected key(s) in SKILL.md frontmatter: disable-model-invocation. Allowed properties are: allowed-tools, description, license, metadata, name
```

maker `design-spec`은 validator rc=0입니다. adopter `capture-intent`와 `design-spec`은 각각 rc=1입니다. 두 파일 모두 PyYAML에서 유효한 dict로 읽혔고 `disable-model-invocation` 값은 실제 boolean `True`였습니다. 보존된 공식 문서와 현재 [Claude Code 공식 frontmatter reference](https://code.claude.com/docs/en/skills#frontmatter-reference)는 이 키를 optional 필드로 명시합니다. 따라서 이는 유효하지 않은 YAML이나 Claude Code 미지원 필드가 아니라 Codex validator의 허용 키 집합과 Claude Code 확장 필드 사이의 범위 차이입니다.

## 3. plan.md와 맞지 않는 점

없음.

maker 범위는 총 112개 경로이며 plan 밖 경로와 필수 경로 누락이 모두 0개입니다. 최종 시점에는 전부 tracked/staged 상태이고 untracked가 없습니다.

adopter 범위는 총 15개 경로이며 모두 `templates/`, `examples/README.md`, 선택형 `examples/skills/` 아래입니다. 제품 코드, tests, evals, intent, 제작 연구·검증 자산은 없습니다. 원본 `codex/use-template-0017`과 remote branch는 모두 `add296d3875fb5555b583fdb5fce9ca4696b424c`로 보존됐습니다.

probe receipt도 실제 경로, `codex/exp-0021-spec-handoff`, HEAD `a2908b1…`과 일치합니다. 초기 `2dd4386` 이후 `tracker.py`, `tests/test_tracker.py`, `requests.json`, 입력 intent는 변경되지 않았습니다. 변경은 spec/plan과 최종 guidance에 한정되며, adopter와 비교한 14개 guidance 파일은 모두 동일합니다. 세 artifact SHA도 receipt와 일치했고 probe worktree는 clean입니다.

## 4. 확인하지 못한 것과 이유

- `make evals`는 API key 없음으로 rc=2 SKIP입니다. semantic eval은 실제 실행되지 않았고 PASS로 판정하지 않았습니다.
- probe의 저장 로그에는 기존 3개 시험 rc=0이 있지만, 이번 verifier는 해당 시험을 새로 실행하지 않았습니다. 제품 기능은 구현되지 않았으며 새 기능·손상 JSON 경로는 plan에만 있습니다.
- 두 모델의 PASS는 현재 R2 의미 리뷰 결과입니다. 이번 검증은 모델 보고서의 의미 판단을 재수행하거나 대신하지 않았습니다.
- Python suite의 1개 skip은 같은 환경에서 앞서 확인한 대소문자 경로 alias 관련 플랫폼 조건입니다.
- 초기 adopter validator rc=1은 계속 실제 결과입니다. 공식 Claude Code 지원과 YAML 유효성 확인은 그 결과를 삭제하거나 validator 자체를 PASS로 바꾸지 않습니다.

Root의 보존 로그 링크: [make check](final-make-check.log), [03 양성·음성](final-proof-03.log),
[해시](final-receipt.log), [scope](final-scope-check.log), [북극성](final-north-star.log),
[YAML](final-frontmatter-yaml.log), [validator 원문](final-quick-validate.log), [probe](final-probe.log).
