#!/bin/bash
# reviewer script — local merges only, no push
set -u
export PYTHONDONTWRITEBYTECODE=1
cd "$(dirname "$0")/.."
for tag in 0005 0006; do
  git -C chain56R worktree remove --force ../chain56R-wt-merge-$tag 2>/dev/null
  git -C chain56R branch -D review/merge-$tag 2>/dev/null
done
for order in "0005-intent 0005-build 0006-intent 0006-build" "0006-intent 0006-build 0005-intent 0005-build"; do
  tag=${order:0:4}; wt=chain56R-wt-merge-$tag
  git -C chain56R worktree add -q -b review/merge-$tag ../$wt origin/main
  echo "##### order: $order  wt=$wt start=$(git -C $wt rev-parse --short HEAD) branch=$(git -C $wt branch --show-current)"
  for b in $order; do
    git -C $wt merge --no-edit origin/chain/$b > /tmp/rv56-merge.log 2>&1; rc=$?
    echo "merge $b rc=$rc: $(grep -E 'CONFLICT|Fast-forward|Merge made|Already' /tmp/rv56-merge.log | head -2 | tr '\n' ' ')"
    git -C $wt status --short | head -5
  done
  echo "--- combined tree: routes.py owner line / records.py guard"
  grep -n "owner" $wt/src/claims_status/routes.py
  grep -n "record is not None" $wt/src/claims_status/records.py
  echo "--- make test"
  ( cd $wt && find . -name __pycache__ -prune -exec rm -rf {} + ; PATH=/opt/homebrew/bin:$PATH make test > /tmp/rv56-mt.log 2>&1; echo "make test rc=$?"; grep -E "^Ran|^OK|FAILED|passed, |^PASS  managed" /tmp/rv56-mt.log )
  echo "--- both new suites + 0002 suite verbose tail"
  ( cd $wt && python3 -m unittest -v tests.test_claims_status_defect tests.test_claims_status_incident tests.test_claims_status > /tmp/rv56-nv.log 2>&1; echo "rc=$?"; grep -cE "\.\.\. ok$" /tmp/rv56-nv.log | sed 's/^/ok lines: /'; tail -3 /tmp/rv56-nv.log )
  echo "--- cross-interaction: 0005 defect repro + 0006 stale repro on combined tree"
  ( cd $wt && python3 -c 'import sys;sys.path.insert(0,"src");from claims_status import records,routes;del records._UPSTREAM["C-1001"]["subscriber_id"];print("0005 repro:",routes.get_claim_status("C-1001",{},now=0))'; python3 -c 'import sys;sys.path.insert(0,"src");from claims_status import records,routes;S={"subscriber_id":"S-77"};print("t0",routes.get_claim_status("C-1003",S,now=0));records._UPSTREAM["C-1003"]={"claim_id":"C-1003","subscriber_id":"S-77","status":"접수","next_step":"서류 검토","due_date":"2026-09-20"};print("t30",routes.get_claim_status("C-1003",S,now=30),"upstream=",records.upstream_calls())' )
done
