# U7 — 선택 문서 포함 확인 훅 독립 구현 리뷰

2026-10-03, Asia/Seoul. 초기 검토는 `codex/plan-specificity-policy`의
`8d5175efddc6875ffe6613725110a5f78a3dc1c7` 위 U7 미커밋 변경을 대상으로 했다.
HEAD가 U7 구현을 포함한다는 뜻은 아니다. 최초 관측과 이후 수정 재검토를 구분해 보존한다.
리뷰자는 source를 수정하거나 커밋하지 않았고 이 보고서와 지정된 private 검토 자료만 작성했다.
사람의 수락·머지·배포를 부여하지 않는다.

## Initial findings

초기 구현에서 중요한 발견 2건을 재현했다. 훅의 표시 설정 의존성과 source 시험의 환경 격리 누락이다.
나머지 검사 범위에서는 별도 모델 실행·영구 receipt·자동 stage·기본 설치 활성화가 추가된 흔적을
찾지 못했다. 형식적인 문서 수정이나 매 커밋 fresh verifier도 요구하지 않는다.

### F1 / P2 / Bugs — 같은 staged 내용이 표시 설정과 작업 트리 attributes에 따라 다른 지문이 된다

초기 `tdd-optional/org-skills/examples/document-sync-hook/document_sync.py`의 `DIFF_FLAGS`
및 `staged()`(당시 51–78행)는 patch 출력에 SHA-256을 적용한다. `core.quotePath`와
`diff.algorithm`, 색상·rename·외부 diff·textconv 등의 일부 옵션은 고정했으나 canonicalization이
충분하지 않았다. SP08의 HEAD+canonical staged diff와 U7 설계의 표시 설정 독립 계약에 어긋난다.

독립 fixture에서 40줄 문서의 4번/20번 줄을 수정하고 `z.md`를 추가해 stage했다. HEAD와
`git ls-files --stage -z`의 경로·mode·object ID가 같은 상태에서 다음 입력만 바꿨다.

| 입력 | 초기 관측 |
|---|---|
| `git config diff.interHunkContext 30` | snapshot 변경 |
| `git config diff.orderFile <z.md를 먼저 나열한 임시 파일>` | snapshot 변경 |
| `GIT_DIFF_OPTS=--unified=0` | snapshot 변경 |
| stage하지 않은 `.gitattributes`의 `*.md binary` | snapshot 변경, staged entries 동일 |

설정 변경 전에 만든 신호를 유지하고 `diff.interHunkContext=30` 상태에서 실제 `git commit`을
실행하면 rc=1과 다음 오류가 발생했다.

```text
document-sync: HEAD 또는 staged index가 검토한 snapshot과 다릅니다. 현재 범위를 다시 검토하고 지문을 새로 만드세요.
```

내용은 그대로인데 커밋 대상이 달라졌다고 안내한다. settings를 매번 다시 맞추거나 지문을 단순히
재생성하게 만드는 불필요한 차단이며, 지문은 검토 인증이 아니라는 원래 경계와도 구분해야 한다.
최소 수정은 실제 staged 경로·mode·내용 정체성만으로 안정적으로 직렬화하거나, 채택한 patch
직렬화에 영향을 주는 설정·환경·attributes를 완전히 고정하는 것이다. 어떤 표현을 선택하든 설계와
README의 지문 설명을 맞추고 표시 설정 변경 전 신호로 실제 커밋하는 회귀를 남길 필요가 있다.
새 의미 검사기·모델 판정·승인 흐름은 필요하지 않다.

첫 probe는 index 파일의 raw 바이트를 비교해 `index_unchanged=false`를 기록했다. Git commit이
stat cache를 refresh할 수 있어 이 값만으로 훅이 stage를 변경했다고 판단하지 않았다. 두 번째
probe는 `ls-files --stage -z`를 함께 비교해 `staged_entries_unchanged=true`를 확인했다.
첫 출력은 삭제하지 않았다. 초기 r2에서 baseline은
`55c6635a55130560116d1668ce03b425a2ea679786a075123c64e11ae8618dbb`, interHunk 변경 후는
`649fa83c5a7dc5fd4fd623958c850cc9159413d6ff453a52e658121f81778810`이었다.
fixture HEAD가 매 실행 달라질 수 있으므로 digest의 절대 값보다 같은 실행 내 비교가 판별 기준이다.

### F2 / P2 / Bugs — disposable repo 시험이 실제 사용자 Git 설정과 환경을 상속한다

초기 `tests/test_document_sync_hook.py`의 `setUp()` 및 Git/Python subprocess helper는 사용자
환경을 그대로 상속한다. fixture는 `.git/hooks/pre-commit`에 파일을 복사하지만 실제 Git이 그
경로를 쓰게 고정하지 않는다. `init.defaultBranch`도 명시하지 않은 채 conflict 시험은 master가
없으면 main이라고 가정한다. Git signing, inherited `GIT_DIR`/`GIT_INDEX_FILE`도 격리하지 않는다.

실제 사용자 설정을 바꾸지 않고 private fixture 안의 `GIT_CONFIG_GLOBAL` 파일로 재현했다.

```text
[core]
 hooksPath = <빈 임시 디렉터리>
```

이 환경에서 source의 `test_first_commit_requires_signal_and_accepts_valid_empty_declaration`
하나를 실행하면 신호 없는 커밋이 rc=0이어서 `AssertionError: 0 == 0`으로 실패했다. 설치한 훅이
실행되지 않은 것이다. 전체 시험이 잘못 PASS했다는 뜻은 아니다. 기존 부정 검사가 이 환경 문제를
검출했지만 시험하려던 훅의 동작까지 도달하지 못한다.

별도 임시 global config의 `[init] defaultBranch = trunk`에서
`test_unresolved_index_fails_snapshot`을 실행하면 `git checkout -q main`의
`error: pathspec 'main' did not match any file(s) known to git`로 실패했다.
최소 수정은 fixture 전용 Git 환경·설정을 사용하고 초기 브랜치를 명시하며, snapshot·commit에도
같은 환경을 넘기는 것이다. 실제 사용자 전역 설정을 수정해 시험을 통과시키면 안 된다.
inherited Git 환경은 fixture 밖을 가리킬 수 있으므로 제거하거나 명시한 fixture 경로로 제한한다.

## Scope, contracts and routing

검토 기대는 현재 구현에서 추출하지 않고 사용자 인계, 0028의 FR09/SP08/AC08/T12,
U7-hook-design.md, 북극성 V4-11과 실제 staged Git 의미에서 먼저 정했다. V4-11 본문은 계획을
벗어나면 같은 commit에서 plan을 갱신하고 hook을 **고려**하라고 한다. 해당 주석의 `부분` 판정과
0017/0018/0019 등의 최초 누락·사람 복구 이력은 이번 결정론적 fixture로 승격하지 않는다.

현재 maker plan의 Files that change에는 새 `org-skills/examples/document-sync-hook/`,
`tests/test_document_sync_hook.py`, 공통 feedback, Claude/Codex/org-skills README,
제품 CHANGE-DELIVERY/GIT-WORKFLOW의 변경 경로가 있다. 각 행은 T12/SP08로 연결되고,
SP08은 FR09/AC08을 명시한다. 새 helper·시험·전달 문서가 계획 밖에 빠졌던 U6식 경로 누락은
이번 현재판에서 재현되지 않았다. U1–U6의 기존 수락/검토 결과를 U7에 자동 승계하지도 않는다.

초기 T12에는 source 시험과 독립 리뷰가 있었지만 선택 검증 방식·이유·구현/검증 순서를 짧게
명시하지 않았다. 다음 담당자가 TDD 이력으로 오인하지 않도록 실제 방식을 현재 인계에 기록하는
것이 맞다. 이는 non-TDD 자체에 대한 결함 지적이나 새 승인 요청이 아니다.

maker `docs/BOUNDARY.md`의 현재 “Not here: a plan-sync hook … this repo does not have one”은
새 optional example의 존재와 기본 비활성 범위를 구분해 정정할 필요가 있다. 과거 playbook 주석의
원문·판정은 역사로 유지한다. 새 시험 파일 첫 문장에도 maker CLAUDE가 요구한 spec clause가
없었다. 이 둘은 주 결함 2건과 별개인 작은 현재 문서/출처 정정이며 새로운 일반 규칙을 요구하지 않는다.

공통 feedback의 추가 문단은 기존 세션에서 의미를 검토하고 필요한 것만 stage하며, companion
문서 개정이 없으면 빈 목록을 사용하게 한다. 훅이 스킬을 호출하거나 검토를 인증하지 않는다는
경계도 유지한다. Codex의 기존 `sdlc-feedback.patch`를 임시 사본에 실제 적용해 rc=0과 U7 공통
문단의 보존을 확인했다. Claude/Codex README는 같은 example로 연결하고 설치 자동 활성화를
주장하지 않는다. example README는 실행 파일 2개와 Python 3.8 이상을 요구하며 README도 기존
개발 안내에서 접근 가능하게 보존하도록 한다. companion을 설치한 실제 채택 제품은 이번 범위에 없다.

제품 CHANGE-DELIVERY의 새 hook 금지는 메시지 형식 검사의 범위로 좁혀졌고, Git 정책은 opt-in
문서 포함 확인을 허용하되 의미·검토 진위·우회 방지는 보장하지 않는다. 별도 receipt/상태 장부,
모든 commit의 spec/plan 수정, 매번 fresh verifier를 추가하지 않아 현재 intent 제약과 맞는다.

## Executed evidence

환경은 macOS의 `git version 2.39.5 (Apple Git-154)`, Python 3.9.6이다. 최초 9개 source 시험은
이 머신의 현재 환경에서 모두 통과했다. 명령과 결과는 다음과 같다.

```sh
python3 -m unittest discover -s tests -p test_document_sync_hook.py -v
```

```text
test_alternate_index_and_path_limited_commit ... ok
test_bad_signals_and_required_path ... ok
test_binary_diff_ignores_display_and_external_diff_configuration ... ok
test_deletion_and_rename_accept_actual_staged_old_and_new_paths ... ok
test_first_commit_requires_signal_and_accepts_valid_empty_declaration ... ok
test_partial_stage_and_unrelated_worktree_changes ... ok
test_stale_head_and_index_fail ... ok
test_unresolved_index_fails_snapshot ... ok
test_unstaged_required_path_does_not_count ... ok
Ran 9 tests in 11.337s
OK
```

독립 재현 코드와 전문 결과는 아래 private 경로에 보존했다. 임시 repo는 그 하위에 만들고
시험 뒤 정리했다. root의 사용자/제품 저장소, 전역 설정, 기존 설치를 수정하지 않았다.

```text
.local/research/openwebagent-template-history/20261003/completion/U7-review/probe.py
.local/research/openwebagent-template-history/20261003/completion/U7-review/probe-results.json
.local/research/openwebagent-template-history/20261003/completion/U7-review/probe-results-r2.json
```

재현 명령은 `python3 .local/research/openwebagent-template-history/20261003/completion/U7-review/probe.py`다.
최초/두 번째 실행의 출력은 각각 따로 보존했고 스크립트는 두 번째 실행 내용이다. Git subprocess는
`GIT_*`와 SDLC 신호를 제거한 복사 환경, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`을
기본으로 사용한다. 환경 상속 결함 확인 때만 fixture용 global 설정 파일을 전달했다.

독립 실행에서 실제 확인한 결과는 다음과 같다.

- README 첫 shell block을 그대로 추출해 별도 repo에 설치했다. 신호 없는 실제 commit은 rc=1로
  차단되어 설치한 hook의 실행을 확인했다. 올바른 첫 commit은 통과했다.
- `git commit -a`가 worktree에서 만든 실제 대상과 일반 index의 snapshot이 다르면 rc=1이었다.
  HEAD에서 만든 별도 index에 `git add -u`한 snapshot으로 동일 `-a` 대상 commit은 rc=0이고
  `HEAD:text.md` 내용도 기대한 `commit all change`였다.
- 내용 변경이 없는 `--amend`를 새 신호와 함께 실행하면 rc=0이고 HEAD가 바뀌었다.
- 하위 디렉터리에서 상대 `GIT_INDEX_FILE=../alternate`로 얻은 snapshot은 동일한 절대 alternate
  index의 snapshot과 같았다. 실제 path-limited 실패·복구, 일반 index의 무관 staged 보존은
  source 시험에서도 실행했다.
- 기존 hook이 있는 repo에 README 설치를 다시 실행하면 rc=1이었다. 로컬 hooksPath와 임시 global
  hooksPath가 있는 경우도 rc=1이며 다른 경로를 만들지 않았다. 임시 global 파일은 바뀌지 않았다.
- linked worktree의 실제 hooks 경로가 primary repo의 공통 디렉터리임을 확인했다. 기존 설치가
  있는 linked worktree에서 재설치는 거절됐다. 문서의 저장소 전체 영향 경고와 맞는다.
- 공백·한글 경로, rename의 old/new 경로와 deletion, malformed JSON/duplicate key/extra field/
  glob/escape/duplicate path, 선언 문서가 worktree에만 존재하는 경우, 부분 stage와 무관한
  untracked WIP, unborn HEAD, stale HEAD/index, unresolved index는 source 시험의 실제 Git 경계를 확인했다.

root가 제공한 `completion/package-u7/results.json` 및 `completion/U7-install-fixtures/results.json`도
읽었다. root의 Claude strict 3건, Codex 4 patch의 dry/apply, frontmatter 4건, authoring links 128개와
공통 기준 일치, 설치 fixture 4건은 제공된 별도 실행 근거다. 본 리뷰자의 직접 실행으로 바꾸어
기록하지 않는다. 전체 `make check`는 root 담당이라 중복 실행하지 않았다.

## Limits and disposition

Security 관점에서 새 network/model 호출·credential 저장·영구 신호 기록은 보지 못했다. 훅은
Git 조회와 JSON 검사를 수행하고 경로 문자열을 shell 명령이나 pathspec으로 실행하지 않는다.
거짓 빈 목록, 형식적 문서 수정, 신호만 재생성, `--no-verify`, 훅 제거/설정 우회는 명시한 협조적
신뢰 경계 안의 한계다. 이를 보안 강제 실패로 재분류하거나 새 인증 서버를 요구하지 않는다.

실제 Claude/Codex 모델이 자연스럽게 스킬을 선택했는지, 실패를 읽고 의미 있는 문서 개정을 했는지,
실사용 누락률이 줄었는지는 미검증이다. 제품 개발 실험 AC04는 유예돼 있다. Windows/Linux 실행,
Python 3.8 최소 버전 실행, 모든 custom hook 관리자와의 수동 병합, 동시 index 수정 경쟁,
non-UTF-8 경로의 실제 fixture는 실행하지 않았다. 미관측을 PASS 또는 실패로 바꾸지 않는다.

이 독립 리뷰는 적용한 프로젝트 verifier의 기준을 읽고 source와 실제 Git을 대조한 결과다.
별도 subagent를 호출하지 않았다. `/Users/jake/.agents/skills/sdlc-feedback/SKILL.md`와 한국어
보고서의 stop-slop-ko 지침을 적용했다. CodeRabbit 지침도 읽었지만 parent가 금지한 외부 모델/설치를
실행하지 않았으므로 CodeRabbit 결과로 부르지 않는다. 기억 파일은 북극성 우선·원문 보존·실험 유예의
탐색 방향에만 썼고 모든 현재 source 판단은 현 checkout에서 확인했다.

초기 F1/F2는 root에 전달했다. 수정 사실만으로 해결됐다고 표시하지 않으며 후속 재검토 결과를
아래에 추가한다. 검토 보고는 사람의 수락이나 전체 제품 완료 판정이 아니다.

## Follow-up review — F1/F2 복구와 intent-to-add

root가 F1/F2를 수용한 뒤 scoped 재검토를 요청했다. 표시 옵션을 계속 추가하는 중간 수정을 거쳐,
현재 SP08/README는 HEAD와 canonical index 엔트리, 실제 cached 변경 경로 집합의 지문으로
계약을 개정했다. 초기 U7-hook-design.md와 이 보고서의 첫 발견은 보존했다.

개정 도중 `ls-files --stage -z`만 사용하는 제안에 추가 반례를 제시했다. 빈 `empty.md`에
`git add -N empty.md`를 한 뒤의 엔트리와 `git add empty.md` 뒤의 엔트리는 모두 다음과 같다.

```text
100644 e69de29bb2d1d6434b8b29ae775ad8c2e48c5391 0\tempty.md\0
```

하지만 실제 `git diff --cached --name-only -z`는 전자에서 빈 출력, 후자에서 `empty.md\0`이다.
엔트리만 hash하면 실제 커밋 대상이 바뀌어도 이전 신호를 재사용할 수 있다. 이 반례는
`U7-review/ita-probe.py`와 `ita-results.json`에 보존했다. root는 실제 cached 변경 경로도 정렬하고
길이로 경계를 나누어 지문에 넣도록 SP08/README와 구현을 함께 보완했다. 그 결과 intent-to-add가
선언 문서 포함으로 잘못 계산되지 않으면서, 빈 파일의 실제 추가 전환도 지문에 반영된다.

재검토 source는 같은 HEAD 위 미커밋 변경이며 해시는
`.local/research/openwebagent-template-history/20261003/completion/U7-review/rereview-source-hashes.json`에
보존했다. 검사 시작과 종료 때 같은 해시인지 비교했다. 핵심 파일은 다음과 같다.

| 파일 | SHA-256 |
|---|---|
| `document-sync-hook/document_sync.py` | `76c6792021582112c650c1656f4a3887686b8a600ea9bd731d5b720771b09038` |
| `document-sync-hook/README.md` | `a40542cbed6b40f17be3ed53da35df23401d8113e2d55c50a45015029162db0f` |
| `tests/test_document_sync_hook.py` | `71925381bde00d0a1599ebb2d6093f4b42a3151c6574b5f0845e1e00cbb5d1d6` |

수정 helper는 충돌 index를 먼저 거절하고 `HEAD`, `ls-files --stage -z` 바이트, 정렬한 실제 변경
경로를 각각 길이와 함께 `sdlc-doc-sync-v2` SHA-256 입력으로 사용한다. required-document 검사도
같은 실제 변경 경로 집합을 쓴다. 표시 patch, 작업 트리 본문, index stat cache는 hash에 넣지 않는다.
test fixture는 inherited Git 변수를 제거한 전용 환경, global/system 설정 격리, 초기 main 브랜치,
같은 Python 실행 파일을 사용한다. alternate/path-limited 하위 환경도 이 전용 환경에서 파생한다.

독립 재검증 명령은 다음과 같다. 초기 probe와 별도 코드/결과로 보존했다.

```sh
python3 .local/research/openwebagent-template-history/20261003/completion/U7-review/rereview.py
```

| 독립 입력/행동 | 기대 | 관측 |
|---|---|---|
| snapshot 후 interHunkContext/orderFile/GIT_DIFF_OPTS와 unstaged binary attributes를 함께 변경 | 같은 지문, 기존 신호로 커밋 허용 | 지문 동일, staged entries 동일, commit rc=0 |
| 위 commit 뒤 attributes 확인 | 작업 트리에만 남음 | 내용 보존, HEAD에는 없음 |
| 빈 문서를 intent-to-add만 하고 필수 문서로 선언 | 포함 거절 | rc=1, 필수 문서 오류 |
| 빈 문서를 실제 add한 뒤 ITA 시점 신호로 commit | 지문 불일치 거절 | entries는 동일, 지문 변경, rc=1 |
| 같은 실제 추가에 새 신호와 필수 경로로 commit | 허용, 빈 문서 포함 | rc=0, `HEAD:empty.md`는 빈 내용 |
| fake global hooksPath·trunk·gpgSign과 잘못된 inherited index 아래 첫 commit source 시험 | fixture가 환경을 격리하고 통과 | 1 test, rc=0, OK |
| 같은 오염 환경 아래 unresolved-index source 시험 | main에서 실제 충돌을 만들고 snapshot 거절을 검증 | 1 test, rc=0, OK |

전문 결과는 `U7-review/rereview-results.json`에 있다. 마지막 두 항목은 새 source 시험 전체를
반복한 것이 아니라 최초 F2 실패 입력에서 해당 시험 2개를 재실행한 결과다. root가 실행하는
전체 회귀와 이 독립 반례 재검증을 구분한다.

maker plan T12에는 실제 Git 시나리오를 선택한 이유, 첫 commit/오류/alternate index/설치 확인 뒤
전체 회귀로 이어가는 순서, 리뷰 실패 재현과 복구, 처음부터 TDD였다고 소급하지 않는다는 설명이
추가됐다. `docs/BOUNDARY.md`도 선택 예시의 존재와 제품/maker 기본 비활성 범위를 구분한다.
helper/시험 헤더에 SP08(FR09/AC08) 연결을 확인했다. 새 `docs/BOUNDARY.md` 경로도 maker plan의
T12/SP08 행에 반영돼 있다. 이전 현재 문서/출처 정정 항목은 이 판에서 해결됐다.

현재 수정 범위에서 F1, F2와 ITA 후속 반례는 해결된 것으로 판단한다. 이 독립 검토에서 중요한
미해결 발견은 남지 않았다. 이는 위 source와 실제 Git 경계에 대한 판단이며 전체 make check,
실제 모델 행동, 새 실험, 제품 채택, 사람의 수락을 대신하지 않는다. 이후 모델 실험을 진행한다면
별도 실행판·근거와 연결해야 한다.
