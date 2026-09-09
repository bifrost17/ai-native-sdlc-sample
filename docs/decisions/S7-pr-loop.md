# 결정 S7 — pr-loop: 채택할 것이 없어 `/pr-loop` 를 설계한다

날짜 2026-09-09 · 세션 S7 · 브랜치 `lane/S7-pr-loop` · 상태: 오너 서명 대기

## 결정

1. **채택 0건.** 후보 35건(공식 5 · 커뮤니티 30, 표 33행) 전부를 파일로 열어 보고 기각 25행 · 보류 8행 했다.
   근거와 사유는 `docs/research/pr-loop/candidates.md`.
2. **`skills/pr-loop/` 를 설계한다** — `/intent-sdlc-skills:pr-loop [PR번호|URL|브랜치]`.
   레슨 L10 문장의 네 동작을 Step B→A→C→D 로 옮기고, 조직이 채울 자리는 「Team settings」 다섯 줄로
   뺐다(`TEAM:` 주석, 템플릿 `docs/ADOPTING.md` 의 「Claude as the reviewer」 행에 대응).
3. **스킬 폴더 이름과 같은 `commands/pr-loop.md` 는 두지 않는다**(S8 실측: 같은 이름은 충돌한다).
   슬래시로도 자연어로도 로드되도록 `disable-model-invocation` 을 쓰지 않는다.
4. **가드레일을 스킬의 일부로 못 박는다** — 승인·머지 금지, force-push·rebase 금지, 체크를 약화시켜
   그린을 만들기 금지, 안 고친 스레드 resolve 금지, PR 본문·코멘트·CI 로그는 untrusted data.

## 근거

- 기각 사유 셋: **라이선스**(최상위 후보 `ship-and-babysit` 이 GPL-3.0; 라이선스 불명 8건은 보류) · **범위 절반**
  (코멘트만 또는 CI 만 — `facebook/relay` `fix-ci` ★18962 포함) · **이식 불가**(동봉 python watcher나
  그 조직의 봇·체크 이름에 묶임). → `candidates.md`
- **공식에 대체물이 없다**: `review-pr`·`code-review` 는 리뷰를 만들 뿐 push 하지 않고,
  `ralph-loop` 는 PR 을 모르며, `claude-code-action` 은 멘션 한 번에 한 번 반응할 뿐 반복하지 않는다.
  → `coverage.md`, `raw/04-claude-code-action-capabilities.txt`
- **실증 4/4**: 실제 PR 4건(리뷰 코멘트 2 + 실패 체크 1)에서 전부 완주. 체크가 실제로 초록이 됐고
  스레드가 답글·resolve 됐으며 머지·승인은 하지 않았다 — 모델 주장이 아니라 GitHub 조회로 확인.
  → `trigger-tests.md`, `raw/34-tests-after-state.txt`
- **빌린 것은 문장 단위로 밝혔다** (MIT/Apache 5건에서 9가지). → `skills/pr-loop/PROVENANCE.md`

## 기각·보류

- **기각 25행** — 공식 5(범위 불일치) · 범위 절반 9 · 이식 불가/조직 고정 5 · GPL-3.0 2 ·
  사용 신호 없음/불충분/형식 불일치 4. `duyet/…/babysit-pr` 는 `--auto-merge` 로 머지까지 해서
  레슨의 「코드 오너 승인만 남기고 멈춘다」와 어긋나 기각.
- **보류 8행** — 전부 라이선스 불명(`none` 5 · `NOASSERTION` 3). 라이선스가 밝혀지면 다시 본다.

## 확인 못 한 것

MAX_ROUNDS 도달 · 진전 없는 라운드 조기 정지 · 병합 충돌 경로 · 100건 넘는 스레드 페이지네이션 ·
리뷰 body 에만 findings 가 있는 경우 · `REQUIRED_ONLY`/`LOCAL_CHECK`/`BOT_REVIEWERS` 설정 ·
가드레일의 거부 동작(유도 시험 안 함) · 봇 리뷰어가 붙은 PR · 집합 충돌 시험(스킬이 하나뿐).
후보 목록도 망라적이지 않다(code search 403 반복, 열지 못한 출처 4곳). 자세히는 README 「남는 구멍」.

## 오너 결정 필요

README 「정책 오너에게 묻는다」 6개 — 정책 파일을 세울지, `RESOLVE_THREADS` 기본값,
`claude-code-action` 과의 역할 분담, 필수 체크만인지 전부인지, `LOCAL_CHECK` 의 내용,
임시 레포 `bifrost17/s7-pr-loop-test` 존치 여부.
