# Claude Code sonnet result

Filtered CLI export; private reasoning omitted. Final result below is verbatim.

## 요약

PR2(요약)를 구현했습니다: `tracker.py`에 `_owner_matches(request, owner)` helper를 추가해 `list`와 공유하고, `summary [--owner ID]`를 `open\t{n}\ndone\t{n}\n` 형식으로 추가했습니다(쓰기 없음). `USAGE.md`에 사용법 한 줄을 더했습니다.

리뷰에서 지적된 검증 공백도 보강했습니다: `tests/test_summary.py`의 `ExistingErrorPathRegressionTests`에서
- `complete R-999`(없는 ID)가 `show R-999`와 동일한 rc=1·stderr(`Request not found: R-999`)를 내고 데이터를 바꾸지 않음
- 존재하지 않는 `--data` 경로가 기존 rc=2·`Cannot read or update requests: ` 접두사를 유지함

을 실제 subprocess 실행으로 확인했습니다. 이 두 확인은 AC3가 이미 요구하던 "기존 show/complete 오류 유지" 범위이므로 spec 변경은 없고, 검증 공백을 메운 경위만 `plan.md`에 남겼습니다.

**실행 결과**: `python3 -m unittest discover -s tests -v` → 16개 시험 전부 통과, rc=0 (기존 `test_tracker.py` 3개, `test_owner_list.py` 5개, 신규 `test_summary.py` 8개). `list`/`summary`/`summary --owner hana`를 수동으로도 실행해 출력을 확인했습니다.

**커밋**: `ee972b0 feat: add summary --owner status counts (F02 PR2)` — `tracker.py`, `tests/test_summary.py`, `USAGE.md`, `intent/0001-owner-list-summary/plan.md`.

**미확인/범위 밖**: hosted PR·CI·원격 머지는 수행하지 않았습니다(로컬 실험 지시에 따름). PR1→PR2 통합 절차(사람 리뷰 후 main 머지)는 아직 진행되지 않았습니다.
