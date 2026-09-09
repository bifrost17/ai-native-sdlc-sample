#!/usr/bin/env bash
# tests/test_no_scratch_paths.sh — 레인 스크래치 경로가 레포로 새어 들어오지 않는가.
#
# 왜 있는가: 이 레포의 문서·시험은 격리 워크트리(레포 밖 스크래치 디렉터리)에서
# 쓰인다. 그래서 「재현: 아래 경로에서 …」 같은 문장에 그 기계에만 있는 절대경로가
# 그대로 실려 커밋된 적이 있고, 직전 라운드가 2건을 손으로 지웠다. 손으로 지운 것은
# 다음에 또 들어온다 — 그때 쓴 grep 을 게이트로 설치하는 것이 이 파일이다.
#
# 무엇을 재는가: 레포 전체(.git 제외 · 이 파일 포함)에서 아래 P1~P3 이 0건인가.
#   P1  레인 원문 디렉터리 이름(W1-K 레인이 남긴 것)
#   P2  macOS 스크래치 절대경로 접두
#   P3  세션 스크래치 디렉터리 이름
# 세 패턴의 실제 문자열은 아래 P1/P2/P3 대입에 조각으로 들어 있다 — 주석에
# 완성형으로 적으면 이 파일이 자기 검사에 걸린다(실측: 그렇게 적었다가 FAIL 3자리).
# 패턴은 실행 시각에 조각으로 이어 붙인다 — 그래야 이 파일 자신이 자기 검사에
# 걸리지 않고, 그러면서도 「자기 자신만 제외」라는 구멍을 만들지 않는다.
#
# 부재 PASS 는 「살아 있음」 계약과 짝이어야 한다: 이 시험은 매 회차 자기 계기를
# 먼저 증명한다 — 레포 안에 탐침 파일을 만들어 세 패턴이 전부 잡히는지 보고,
# 잡히면 지운 뒤에야 본 검사를 돌린다. 탐침이 안 잡히면 「0건」은 결함 없음이
# 아니라 못 잰 것이므로 FAIL 한다. 탐침 삭제는 trap 이 보장한다.
#
# 이 계기가 증언하지 못하는 것: 패턴 목록 자체의 정당성. 양성 대조는 grep 이
# 살아 있다는 것만 보이고, P1~P3 이 옳은 세 패턴인지는 사람이 정한다 — 패턴을
# 조용히 좁히는 변경은 이 시험이 아니라 리뷰가 잡는다.
#
# 무엇을 재지 않는가: 다른 기계의 스크래치 관례(`/tmp/…`·`C:\…`) · 존재하지만
# 레포 밖인 상대경로 · 커밋 메시지(작업 트리만 본다) · git 이 무시하는 파일과
# `.git` 자신(디렉터리든 연결 워크트리의 파일이든 둘 다 검사 대상 밖이다).
#
# rc: 0 = PASS · 1 = FAIL. 호환: macOS 기본 bash 3.2(배열·mapfile 안 쓴다).
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"

# 조각 이어 붙이기 — 이 파일에 완성된 패턴 문자열이 남지 않게 한다.
P1="raw-""w1k"
P2="/private""/tmp"
P3="scratch""pad"
PATTERN="$P1|$P2|$P3"

PROBE="$ROOT/.scratch-path-probe.tmp"
trap 'rm -f "$PROBE"' EXIT INT TERM

scan() {
  # 판정할 명령을 파이프 왼쪽에 두지 않는다 — 파일로 받고 rc 를 직접 읽는다.
  #
  # --exclude=.git 이 왜 필요한가: 연결 워크트리(git worktree add · detached
  # 측정에서 쓴다)에서는 `.git` 이 디렉터리가 아니라 **파일**이고 그 안에
  # 「gitdir: <절대경로>」 한 줄이 들어 있다. --exclude-dir 만으로는 그 파일이
  # 걸러지지 않아 계기가 자기 워크트리 배치를 결함으로 보고한다(실측:
  # detached 회차에서 이 한 자리로 FAIL rc=1 · raw-r2B/33).
  grep -rIn -E "$PATTERN" "$ROOT" --exclude-dir=.git --exclude=.git > "$1" 2>/dev/null
  return 0
}

HITS="$(mktemp)"
trap 'rm -f "$PROBE" "$HITS"' EXIT INT TERM

# --- 계기 양성 대조(매 회차) ------------------------------------------------
{
  echo "probe $P1"
  echo "probe $P2/foo"
  echo "probe $P3/bar"
} > "$PROBE"
scan "$HITS"
FOUND=0
grep -q -- "$P1" "$HITS" && FOUND=$((FOUND + 1))
grep -qF -- "$P2" "$HITS" && FOUND=$((FOUND + 1))
grep -q -- "$P3" "$HITS" && FOUND=$((FOUND + 1))
rm -f "$PROBE"
if [ "$FOUND" -ne 3 ]; then
  echo "FAIL  계기 양성 대조 — 탐침 3종 중 ${FOUND}종만 잡혔다. 이 회차의 「0건」은 판정이 아니다"
  echo "      탐침: $PROBE · 패턴: $PATTERN"
  exit 1
fi
echo "PASS  계기 양성 대조 — 레포 안에 심은 탐침 3종을 전부 잡았다(패턴이 살아 있다)"

# --- 본 검사 ---------------------------------------------------------------
scan "$HITS"
N="$(wc -l < "$HITS" | tr -d ' ')"
if [ "$N" -ne 0 ]; then
  echo "FAIL  레포 밖 스크래치 경로가 ${N}자리 남아 있다 — 지우고 다시 돌려라"
  sed 's/^/      /' "$HITS"
  exit 1
fi
echo "PASS  레포 밖 스크래치 경로 0건(패턴 3종 · .git 제외 · 이 파일 포함 전수)"
exit 0
