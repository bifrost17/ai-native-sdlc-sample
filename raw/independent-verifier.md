# 0017 R01 independent verifier report

Verified product: `/Users/jake/Projects/ai-native-sdlc-experiments/sync-r01`
Final product commit: `9f42449bc786535ceaa1d52df4fd34315a88c842`
Accepted revised spec: `5e6cdd68ed87a7dfdab76b823edafe09a10c9278`

## 1. What I ran

- `python3 -m unittest discover -s tests -v 2>&1 | tee /tmp/0017-r01-unittest.txt` — rc 0.
- A read-only Python subprocess harness, saved as output in `/tmp/0017-r01-cli.txt`, invoked:
  - `python3 tracker.py --data requests.json summary`
  - `python3 tracker.py --data requests.json summary --json`
  - `python3 tracker.py --data requests.json summary --owner hana --json`
  - `python3 tracker.py --data requests.json summary --owner nobody --json`
  - a temporary copy: `complete R-101`, then `summary --owner hana --json`
- `git show --name-status 5e6cdd68`, `git show --name-status 9f42449b`, `git diff --check 8dbf319..9f42449b`, plus AST comparison of every baseline test method and byte comparison of `requests.json`.

## 2. What I saw

- All 12 unittest cases passed in 0.571s. First failing line: none.
- Text summary was exactly `open\t3\ndone\t1\n`.
- JSON results parsed to integer objects `{"open":3,"done":1}`, owner hana `{"open":1,"done":1}`, and unknown owner `{"open":0,"done":0}`, all rc 0 with empty stderr.
- After completing R-101 in a temporary data copy, owner hana JSON became `{"open":0,"done":2}`.
- The source `requests.json` remained byte-identical to `8dbf319` with SHA-256 `c038196ad9f748e482a446e4025e4c6c0746b23942c39f5f457ad37dd9a53795`.
- All seven baseline test helpers/methods were AST-identical; seven summary methods were additions.
- `5e6cdd68` changes only the accepted spec. Its child `9f42449b` contains exactly `README.md`, `plan.md`, `tests/test_tracker.py`, and `tracker.py`; the worktree is clean.
- The plan identifies both the prior accepted base spec and the new exact `5e6cdd68` R8/AC9 acceptance. The new SHA and its scope are unambiguous.

## 3. What does not match plan.md

None. The dual historical/current SHA wording differs from a single-SHA Upstream style, but it explicitly links the accepted revised spec and does not leave the governing JSON requirement ambiguous.

## 4. What I could not check

I did not treat a future PR merge, remote publication, or archive record as product behavior. Those steps were outside this pinned local product verification.

Artifacts:
- `/tmp/0017-r01-unittest.txt` — SHA-256 `a5f0ca0f01d9752f329a46e6edf1cbf931ac9363e013697a559a86f416a32e29`
- `/tmp/0017-r01-cli.txt` — SHA-256 `6ca105ed02e25d43ec8fb91f575276849071b4f6b8df6a1b652ab06fb60725dc`
