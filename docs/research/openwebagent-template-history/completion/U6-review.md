# U6 독립 source 완료 검토

## 범위와 판

- 저장소: `/Users/jake/Projects/ai-native-sdlc-sample`
- 제품 source HEAD: `df3ae99c3ba9bab5b656a0761aa52ba7a733bb79`
- 순차 제작 비교: `4a84596c37496deb1055bd528b94fb6abd5dea75..df3ae99`
- 원 후보 누적 비교: `ad98adec5c85ebb969fa394796d388df10303a1f..df3ae99`
- 현재 미커밋 maker plan SHA-256: `eb66aa1871b9b4de9c999638629e75cd65855c963a68c945c71887331aecd771`
- 검토 대상: AC03·AC05·AC06·AC07의 source와 인계, U1–U5 누적 회귀, T11 패키지 증거와 `make check`
- 제외: AC04 제품 효과, 실제 개발 사례 실험, 자연스러운 스킬 선택, 브라우저·실제 UI 관측, 전역 설치·배포·기존 설치 갱신

현재 수정판에는 **남은 중요한 source 또는 plan finding이 없다.** 다만 최초 plan 인계 누락은 실제 발견이었고 후속 개정으로 해결됐다. 이 결과는 사람의 수락, T11 완료 선언, main 통합 또는 배포를 대신하지 않는다.

## 발견과 해결 이력

### U6-F1 — 최초 plan의 실제 경로 인계 누락: 해결됨

최초 `Files that change`에는 연구 폴더, `tdd-optional` 개선, 북극성 연결을 설명하는 세 문장만 있었다. 실제 변경 경로, 수정 방법, T·SP 연결이 없어 다음 작업자가 최종 source diff를 plan과 양방향 대조하기 어려웠다. 이는 제품 source 의미의 결함이 아니라 V4-06과 verifier 인계 기준에 걸리는 계획 누락이었다.

수정 전 전문은 private `completion/plan-before-u6-findings.md`에 그대로 남아 있다. 현재 plan 13–57행은 다음과 같이 복구됐다.

- `ad98adec..df3ae99`의 `.claude-plugin`·`tdd-optional` 제품 경로 27개를 각각 명시했다.
- `4a84596..df3ae99`의 이번 순차 source 10개가 모두 같은 표에 포함됐다.
- 27개 모든 행에 수정·보존 방법과 T·SP 연결이 있다.
- `README.md`와 `docs/decisions/single-template.md`의 0.1.9 정정도 별도로 적었다.
- Codex patch·verifier, Claude 공통 verifier, tests·evals·Makefile을 T11의 읽기·임시 복사 입력으로 구분했다.
- 이 표가 최초부터 존재했다고 소급하지 않는다는 문장을 유지했다.

교정한 표 파서의 결과는 다음과 같다.

```text
expected_count=27
listed_count=27
expected_not_listed=[]
listed_not_expected=[]
empty_method=[]
missing_T_or_SP=[]
sequence_count=10
sequence_missing_from_rows=[]
```

`git diff --check -- intent/0028-openwebagent-history-feedback/plan.md`도 exit 0이다. 최초 지적은 현재 개정판에서 해결됐다.

### U4-F1 — 기존 제품에 두 번째 색인을 요구할 수 있던 충돌: 기존 해결 유지

이전 U4 최초판의 `GIT-WORKFLOW.md`는 기존 `intent/README.md`를 쓰는 제품에도 `changes/README.md` 갱신을 직접 지시할 수 있었다. 현재 source는 다음으로 구분한다.

- 새 템플릿은 `changes/README.md`를 기본으로 쓴다.
- 기존 제품은 실제 채택한 색인을 유지한다.
- 색인이 없으면 현재 plan과 기존 실행 기록에 상태를 남긴다.

현재 `PROCESS`, 세 작성 스킬, `sdlc-feedback`과 충돌하지 않는다. 최초 P2 finding과 후속 해결은 U4 기록에 함께 남아 있으며 최초판을 통과로 소급하지 않았다.

U4 리뷰 51행의 상대 링크는 source 위치에서 인용된 원문이어서 completion 폴더에서는 직접 해소되지 않았다. U6-validation 47–50행에 실제 source 링크를 추가했고 대상 파일의 존재를 확인했다. U4 전문과 raw diff를 고치지 않은 처리는 기록 보존 요구와 맞는다.

## source 의미와 북극성 회귀

북극성 V3-11/14, V4-06/08/11, V7-05, V8-02와 실제 source를 대조했다.

- **U1 검증 설계:** 중요한 AC의 기대를 구현 결과와 분리하고, 실제 경계·입력·환경·실패·후속 상태 관측을 plan으로 넘긴다. 작은 F01에는 기존 좁은 검증을 재사용할 수 있고 별도 HTTP·DB 표를 강요하지 않는다. TDD는 선택된 범위에서 유지되며 모든 작업의 의무로 확대되지 않는다.
- **U2 UI:** 정적 HTML은 배치 탐색에 계속 유효하다. 상호작용·앱 셸·상태가 위험일 때는 실제 컴포넌트를 선택하고, 시각 기준·스크린샷·행동 관측·사람 피드백과 제품 편입을 별도로 확인한다. 탐색 결과를 제품 완료로 올리지 않는다.
- **U3 초기 통합:** 첫 위험 경계를 통과하는 작은 실제 경로를 먼저 만들고 후속 확장과 독립 병렬 작업을 허용한다. 연결을 늦출 때는 가정·가상 경계·시점·위험을 명시한다. health check나 mock을 사용자 흐름 증거로 취급하지 않으며 독립 PR, main 통합, 배포 가능성을 구분한다.
- **U4 정본·역사:** 현재 계약과 역사 자료를 구분하고 실제 채택 색인을 우선한다. 기존 `intent/` 구조를 강제 이사하지 않으며 색인 없는 제품에는 plan·실행 기록 fallback이 있다.
- **U5 전달:** PR은 최종 diff, 실제 시험 대상 판, 관련 spec·plan 개정, 남은 범위와 후속 근거를 연결한다. 시험 통과와 사람의 수락·병합·배포·전체 제품 완료를 구분한다. 작은 수정은 같은 수준의 문서 묶음을 새로 만들 필요가 없다.

U1·U2·U3·U5에서 새로 해결해야 할 중요 누락은 찾지 못했다. U4의 위 finding만 실제 수정 후 해결된 상태다.

## 실제 실행과 출력

### `make check`

이번 완료판에서 직접 한 번 실행했다.

```sh
make check
```

- exit: `0`
- 첫 실패 행: 없음
- 전체 stdout: 이번 verifier의 native tool record에 보존됨
- 결과:
  - `python3 -m unittest discover -s tests`: 103 tests, 38.787s, `OK (skipped=1)`
  - `bash tests/test_hooks.sh`: 28 passed, 0 failed
  - `bash tests/test_evals.sh`: 8 passed, 0 failed
  - `bash tests/test_managed_settings.sh`: 11개 공식 key 확인, `PASS managed-settings 키·훅 계약`

이 결과는 현재 작업 트리의 maker 회귀다. 제품 효과나 사람의 시각 수락 증거는 아니다.

### diff 공백 검사

```sh
git diff --check ad98adec5c85ebb969fa394796d388df10303a1f..HEAD -- .claude-plugin tdd-optional
```

exit `0`, 출력 없음.

```sh
git diff --check 4a84596c37496deb1055bd528b94fb6abd5dea75..HEAD -- tdd-optional/project/templates/spec.md tdd-optional/project/examples/skills/design-spec/references/design-depth.md tdd-optional/project/examples/skills/plan/examples/disposable-ui-exploration.md tdd-optional/project/examples/skills/plan/references/execution-depth.md tdd-optional/project/changes/README.md tdd-optional/project/docs/PROCESS.md tdd-optional/project/docs/GIT-WORKFLOW.md tdd-optional/project/examples/skills/capture-intent/SKILL.md tdd-optional/project/examples/skills/design-spec/SKILL.md tdd-optional/project/examples/skills/plan/SKILL.md
```

exit `0`, 출력 없음.

전체 기록 범위 검사는 통과하지 않았다.

```sh
git diff --check 4a84596c37496deb1055bd528b94fb6abd5dea75..HEAD
```

- exit: `2`
- 첫 실패 행:

```text
docs/research/openwebagent-template-history/completion/U4-review.md:161: trailing whitespace.
```

이후 경고도 U4에 보존된 raw patch의 한 칸 context 행, 원본 hunk 제목의 후행 공백, EOF 빈 줄이다. 따라서 “전체 diff 공백 검사 통과”로 보고하지 않는다. 배포 source 경로의 통과와 원문 기록의 nonzero를 구분한다.

### 의도적 hook bad input

`.claude/settings.json`의 `PreToolUse`에 연결된 `protect-paths.sh`를 하나 직접 확인했다.

```sh
printf '%s\n' '{"tool_name":"Edit","cwd":"/Users/jake/Projects/ai-native-sdlc-sample","tool_input":{"file_path":"Makefile","old_string":"never-applied","new_string":"never-applied-2"}}' | bash .claude/hooks/protect-paths.sh
```

- exit: `2`
- 첫 출력 행:

```text
[protect-paths.sh] BLOCKED: Makefile is a frozen path (.github/* Makefile .claude/hooks/* .claude/settings.json). Reason: CI wiring, the make targets and the hooks are the feedback loop itself; an agent must not loosen them mid-task. Route: a human changes it in its own PR, or edits PROTECTED in this hook in that PR.
```

예상된 차단이며 제품 결함이 아니다.

## 패키지 증거

`source-hashes.json`과 최종 package 자료를 현재 파일에서 다시 해시했다.

```text
source_head=df3ae99c3ba9bab5b656a0761aa52ba7a733bb79
source_count=147
source_hash_mismatches=[]
package_source_head=df3ae99c3ba9bab5b656a0761aa52ba7a733bb79
package_result_count=15
package_nonzero=[]
package_log_hash_mismatches=[]
codex_skills=16
claude_authors=3
authoring_links_checked=128
common_verifier_criteria_equal=True
asset_hash_rows=59
```

세 버전은 모두 `0.1.9`다.

```text
.claude-plugin/marketplace.json
tdd-optional/.claude-plugin/marketplace.json
tdd-optional/org-skills/.claude-plugin/plugin.json
```

최종 package가 기록한 실제 명령은 다음과 같다.

```text
claude plugin validate --strict tdd-optional/org-skills
claude plugin validate --strict tdd-optional/.claude-plugin/marketplace.json
claude plugin validate --strict .claude-plugin/marketplace.json
```

모두 rc 0이다.

Codex 격리 복사본에서는 다음 두 argv를 explicit-only, sdlc-feedback, ux-copy, pr-loop 네 patch에 각각 실행했다.

```text
patch --batch -p1 --dry-run
patch --batch -p1
```

8건 모두 rc 0이다. capture-intent, design-spec, plan, sdlc-feedback에는 격리 validator 환경의 `quick_validate.py <설치 스킬 경로>`를 실행했고 4건 모두 rc 0이다. 이번 verifier는 strict나 adapter를 다시 실행하지 않고, `results.json`의 argv·rc와 15개 log SHA-256 및 격리 결과 바이트를 확인했다.

첫 private 시도는 그대로 실패 기록으로 남아 있다.

```text
ModuleNotFoundError: No module named 'yaml'
```

그 시도에서는 strict 3건과 네 patch가 이미 통과했지만 quick validation 환경에 PyYAML이 없었고, 비교 절차가 문서화된 Codex `AGENTS.md` 진입 안내 차이를 정규화하지 못했다. 격리 validator 환경과 비교 절차를 고쳐 같은 source로 재실행한 최종 package가 통과했다. 이는 private 실행 환경·비교 절차의 실패이며 제품 source 결함으로 바꾸지 않았다.

`root-package-originals/manifest.json`에는 root 실행의 tool-call/output 기록 13건이 남아 있다.

## 인접 0027 흐름

다음 실제 diff를 `intent/0027-single-template-skill-parity/plan.md`와 대조했다.

```sh
git diff --name-only 79dedb88..46908f43
git diff --name-only 46908f43..ad98adec
```

- `79dedb88..46908f43`: 184개 파일. tdd-first 제거, root 문서·catalog·route, `tdd-optional`의 Claude/Codex 전달, scripts·evals·tests·GitHub workflow, 실행 기록이 plan의 파일군과 맞는다.
- `46908f43..ad98adec`: `intent/0027-single-template-skill-parity/execution/README.md`와 `plan.md` 두 파일뿐이다.

인접 chain에서 현재 0028 완료 판단을 깨는 경로 또는 순서 불일치는 찾지 못했다.

## Git 상태와 WIP 보존

순차 commit은 다음과 같다.

```text
e1f6f6f docs(plan): complete template improvements in adversarially reviewed slices
bcb501f docs(spec): finish validation design guidance after adversarial review
b814ec2 docs(ui): finish real-component exploration guidance after review
e7ed3fa docs(plan): finish early integration guidance after adversarial review
c3c5a3a docs(workflow): finish adopted-index compatibility and contract authority guidance
df3ae99 docs(delivery): record final adversarial review of PR and commit guidance
```

보호된 tracked WIP는 시작 patch와 동일하다.

```text
2348d9437e25c43e12e75bbd9f349e777233ee82a8811f1d7f2252272a5501aa
```

대상은 `.gitignore`, `CLAUDE.md`, `README.md`, `docs/experiments/README.md`다. 0036·datasets/v8·local-workspaces, 별도 실행계획 연구, plan-skill-design, graft도 이번 source 완료 범위에 넣거나 되돌리지 않았다. 현재 `make check`는 이 작업 트리에서 통과했으므로 이 WIP가 maker gate를 깨지는 않았지만, 그 내용 자체를 U6에서 검토하거나 승인한 것은 아니다.

## 검토 보조 명령의 교정

검토 중 첫 table parser가 경로에 backtick이 있을 것으로 잘못 가정해 `listed_product_path_count=0`을 출력했다. 실제 표는 backtick 없는 첫 cell이었다. cell 파서를 고쳐 27/27, 누락·초과 0을 확인했다.

package metadata 첫 inspector도 실제 key `sha256` 대신 `log_sha256`을 읽어 exit 1, 첫 실패 `KeyError: 'log_sha256'`이었다. 실제 schema로 고친 inspector는 exit 0이며 위 15개 log 불일치 0을 냈다.

보호 patch도 한 번 `.../20261003/start/protected-wip.patch`로 잘못 조회해 exit 1이었다. `find`로 실제 `.../20261003/completion/start/protected-wip.patch`를 확인한 뒤 양쪽 SHA-256이 일치했다. 세 건 모두 reviewer 보조 절차의 경로·schema 오류이며 source 또는 package 실패로 해석하지 않았다.

## 확인하지 못한 범위

- 로컬 `origin/main`은 `67739c8fe8f3a7c3159b480ebd95270888b05074`, HEAD와의 merge-base는 `ad98adec5c85ebb969fa394796d388df10303a1f`다.
- 이번 검토에서 원격을 fetch하지 않았고 최신 원격 main과의 merge-tree, 실제 통합 결과를 실행하지 않았다. 로컬 ref가 최신이라고 단정할 수 없다.
- 제품 CLI·모델 호출·실제 사례 개발, 자연 스킬 선택, 실제 UI·브라우저·사람의 시각 수락을 실행하지 않았다.
- AC04 전후 효과, 완료율 개선, 실제 adoption은 계속 미입증이다.
- 전역 설치, plugin 등록, 기존 설치 업그레이드, PR 생성·병합, main 배포는 하지 않았다.
- 34건 연구 사건 전체를 재감사하지 않았다. 이번 판단은 제작 source, 선언된 누적 리뷰, 인접 흐름 및 package 증거에 한정된다.
- `make check`, strict, patch, 링크·hash 검사는 해당 gate와 전달 형태의 증거다. 사람의 수락·통합·제품 전체 완료를 입증하지 않는다.

현재 plan은 검토 시점에 T11을 진행 중으로 유지하고 있다. 이 보고서를 보존하고 U6/T11 인계를 갱신하는 책임은 root에 있으며, 이 독립 검토는 그 완료 선언이나 사람의 승인 자체가 아니다.

<oai-mem-citation>
<citation_entries>
MEMORY.md:517-527|note=[north star scope and deferred experiment boundaries]
rollout_summaries/2026-09-10T12-17-01-KSiV-ai_native_sdlc_playbook_north_star_history_research.md:9-27|note=[playbook first template review context]
rollout_summaries/2026-09-10T12-17-01-KSiV-ai_native_sdlc_playbook_north_star_history_research.md:65-79|note=[experiment deferral and provenance boundary]
</citation_entries>
<rollout_ids>
01a08b3f-fad6-7e43-8064-cc5b1a3511cd
</rollout_ids>
</oai-mem-citation>