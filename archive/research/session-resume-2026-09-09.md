# 재개 노트 — intent-sdlc-sample (2026-09-08 소프트 중지 시점)

레포: https://github.com/bifrost17/intent-sdlc-sample (public · MIT)

## main 현재 상태
- 머지 완료: #13(CI fetch-depth 0) · #7(검증기+게이트 확장점) · #4(밴드 검출) · #5(스킬2·verifier·/spec·엔드포인트 백스톱, 머지 SHA 2d45f105)
- 게이트: `15 passed, 0 failed, 1 skipped` · `Ran 57 tests ... OK`
- 게이트 성장 실측: 6 → 10 → 11 → 15

## 열린 PR 9건
| PR | 상태 | 남은 일 |
|---|---|---|
| #3 docs/0001-playbook-map | check SUCCESS | 머지 전 CLAUDE.md 「healthy output」 문구 정정(CD-3: `6 passed`·`no tests yet` 둘 다 거짓) |
| #6 hooks | check **FAILURE** | 레인 P 수정 중 중지 — F6-1 경로해석 · bash3.2 성능(64KB 126초) · CD-1 백틱 |
| #8 metrics | SUCCESS | 리뷰 R3 조건부 — 펜스 안 `status: accepted` 위조 차단 + 50-metrics.sh SKIP 3분법. 레인 S 수정 중 중지 |
| #9 evals | SUCCESS | **머지 가능**(R3) · 등재: `regex_absent` 깨진 ERE 침묵 no-op |
| #10 docs/plays | SUCCESS | 스테일 13행 + 산문 3자리. 레인 T 수정 중 중지 |
| #11 managed-settings | SUCCESS | **머지 가능**(R3) · 레포 밖 스크래치 경로 참조 제거는 레인 T 미완 |
| #12 chain 0001 + D16 | SUCCESS | R4 리뷰 중 중지 — 판정 미도착 |
| #14 설계 정정 | SUCCESS | R4 리뷰 중 중지 |
| #15 chain 0002 | **CONFLICTING** + check FAILURE | 리베이스 필요 · D16 착지 후 승인 전이 커밋 필요 |

## 머지 순서(W1-M 통합 드라이런 권고)
#6 · #8 · #9 · #11 → #3(정정 후) → #10(갱신 후) → #12 → #14 → #15

## 웨이브 경계 지면 정정 대기열
CD-3 CLAUDE.md 건강출력 · CD-4 verifier.md 의 pytest(stdlib 규약 위반) · CD-6 check7 침묵 통과 ·
CD-5/F-X1 게이트 조각 단독 실행 rc 규약 3~4가지로 갈림 · README「W0 골격」 · secure-api-review SKILL.md 신규 규약 누락 ·
F11-1 레포 파일이 레인 스크래치 경로 참조

## 미해결 설계 물음
- E-6/E-7: D16 기준점 — 「새 파일일 때 `git diff main` = 45 0」이라 승인 커밋 자신의 디프(1 1)를 봐야 한다. W2-I 변형과의 조정은 R4 판정 대기 중이었다.

## 중지 시점 레인 상태
### RD1-T (#10 스테일 · #11 스크래치 경로) — 커밋 0 · 트리 깨끗
- raw: `design/raw-rd1t/` 14개. **경로 대조는 끝났고 편집만 안 했다** — 재개하면 바로 고칠 수 있다.
- 실측: 8장 표의 고유 경로 36개 중 HEAD 실재 19개(= 「착지」로 바꿀 행) · 나머지 16개는 열린 PR 9개에 전수 대조.
- 추가 발견: 「없음」으로 적힌 4행이 이제 열린 PR 에 실재 → 「대기(PR #N)」로 바꿔야 한다
  (`intent/0002-claims-status/{intent,spec,plan}.md` → #15 · `org/managed-settings.example.json` → #11).
- `check_all.sh` 확장 지점은 실측상 이미 살아 `scripts/gates/*.sh` 를 자동 source — `claude-md.md` · `skills-as-institutional-knowledge.md` 의 「아직 source 안 함」 산문은 지금 거짓.
- 작업 B(#11)는 착수 전 — `gh pr checkout 11` 부터.

### RD1-S (#8 펜스 위조 · 50-metrics SKIP 오계상) — 커밋 0 · sha256 로 무변조 확인
- raw: `design/raw-rd1s/` 5개 · 클론 `design/rd1s` · 브랜치 `feat/0001-metrics` HEAD `ca7f3dc0`.
- 기준선(#8 브랜치): `unittest tests.test_metrics` 15 OK · `gates/50-metrics.sh` 단독 2 passed · `check_all.sh` **17 passed, 0 failed, 1 skipped**.
- 진단 확정: `metrics.py` 의 `git_accepted_commit()` 이 `git log -S'status: accepted' -- <path>` 의 **가장 오래된 줄을 교차 확인 없이** 승인 커밋으로 쓴다.
- 재사용 가능 확인: `check_artifacts.py` 의 `strip_code_spans()`·`extract_frontmatter()` 는 `__main__` 가드가 있어 **임포트 부작용 없음** → 중복 구현 불필요.
- `50-metrics.sh` 단독 대역(78~103행)은 `SKIP_COUNT` 자체가 없고 rc≠0 을 전부 FAIL 로 접는다.
- **비침습 red 하네스(설계 완료 · 재개하면 그대로 쓸 것)**: 임시 디렉터리에 `<tmp>/scripts/gates/50-metrics.sh` 로 실파일 복사 → `GATE50_ROOT` 가 `<tmp>` 가 된다.
  PATH 앞에 `exit 3` 만 하는 `python3` 셰임 → 실대역을 수정 없이 태운다. 지금 `FAIL`(0 passed, 2 failed), 고친 뒤 기대 `SKIP`(0 passed, 1 failed, 1 skipped). 양성 대조는 `exit 0` 셰임(2 passed).
- **PR 본문에 실을 알려진 한계**: `-S` 픽스액스는 같은 커밋에서 펜스 예시를 지우고 진짜 accepted 를 넣으면 등장 횟수 1→1 이라 후보를 아예 못 낸다 — 교차 확인으로도 그 갈래는 안 보인다.

### W2-R4 (#12 사슬+D16 · #14 설계 정정) — 리뷰 대부분 완료 · 원복 sha256 확인
raw: `design/raw-w2r4/` 40개 · 하네스 `design/_w2r4/*.py|sh` (재사용 가능한 D16 벡터 하네스)
🔴 **측정 기준판 = #12 head `9df1da4c` · #14 head `f170912f`. #12 는 그 뒤 `fa2bec49` 로 두 번 전진했고 그 두 커밋은 안 봤다.**

**#12 — 주장 9건 전수 재현(TDD red 2회 · 게이트 11 passed · 뮤테이션 4종 양방향).**
벡터 22종 중 **8종 뚫림**, 그리고 전부 **한 결함 부류**에서 나온다:
> `classify_accept_diff` 가 **git diff 의 텍스트 모양**을 어휘로 삼는다 — 그 어휘의 소유자는 우리가 아니라 git 이다
> (binary 판정 · `.gitattributes -diff` · `+++`/`---` 접두 충돌 · rename 탐지). ORCHESTRATION §10.3 「열린 어휘를 열거하는 축」.
- 뚫린 것: ⑦d(NUL → binary diff 로 1539B→3036B 전면 개작 통과) · ⑦e(`.gitattributes` `*.md -diff`) · ⑦a/⑦c/⑦a3(`---`/`++` 접두) · ⑥c(디렉터리 개명 → 기준점이 브랜치 자기 커밋으로 후퇴) · ③ rejected→accepted(spec F2 에 등재됨) · ④ superseded→accepted(**지면 어디에도 없음**)
- **막힌 것**: ⑥ 기준점 조작 본형 · ⑤b · ② 주석 위장 · ①b/①c 공백
- **축 전환 처방(R4 권고)**: 질문을 「diff 가 무엇처럼 보이는가」 → **「두 blob 의 frontmatter 를 파싱해 `status` 키 하나만 달라졌고 나머지 바이트가 같은가」**.
  그 어휘(frontmatter 키·상태 enum)는 이미 `SCHEMA` 에 열거돼 우리 소유다. **라운드가 아니라 태스크 분리.**
- 등재 E1~E9. 그중 굵은 것:
  - **E4/E5 — CI 에서 D16·브랜치 검사가 아예 안 돈다**(detached HEAD · CI 로그가 축자로 `기본 브랜치(None) 또는 현재 브랜치(None)`). 게다가 `check11_intent_chain` 이 rc=0 일 때 출력을 버려 **「안 돌았다」를 CI 로그에서 셀 수도 없다**(STATUS.md 는 셀 수 있다고 적었다 — 거짓).
  - **E8 — 사슬↔지표 오염 실측 확정**: `intent/0001-*/intent.md` **L17 의 인라인 코드**(펜스 아님) `` `status: accepted` `` 를 #8 `metrics.py` 픽스액스가 승인으로 센다 → `l1_accepted` 가 draft 생성 커밋 `4accbd1` 을 승인 커밋으로 보고 `l1`(6045초)과 값이 붕괴. 🔴 **#12 의 문장을 고쳐 통과시키지 말 것** — 계기를 고치는 게 아니라 소재를 검열하는 일이 된다. 결함 소유자는 #8.
  - E6 — plan Proof 의 AC2·AC4 가 어디에도 없는 시험을 가리킨다(#6·#8 브랜치에만) · `check_plan_proof` 는 시험 실재를 안 잰다.
  - E7 — 게이트 사정거리 `find intent -mindepth 2 -maxdepth 2` 가 깊은 경로를 안 고른다.
- 축 D: intent 제목은 문제문(합격) · spec 이 C1~C3·Q1·Q2 를 **내용까지** 이어받음(합격) · 사슬은 **사후 재구성이되 위조 아님**(9분 8개 서로 다른 초).

**#14 — 정정 3건 중 E-3(spec 8절)·E-5(ruleset 7/7) 실측 완전 일치. 차단 1건:**
> **E-4 D16 기준점 문면이 실물과 어긋난다.** DESIGN.md 는 「`git diff <기본브랜치> -- <파일>`」이라 적었으나 구현 `accept_baseline` 은 2갈래다
> (기본 브랜치에 파일이 **있으면** 기본 브랜치 · **없으면** 이 브랜치의 「아직 accepted 가 아니었던 가장 최근 판」). #12 의 STATUS.md 는 2갈래를 정확히 적었다.
> 그대로 머지하면 DESIGN.md ↔ STATUS.md 가 D16 기준점을 서로 다르게 말한다. **한 문장 교체 + 근거 칸 완화**로 닫힌다(등급 C).
등재 2: §5 「Files that change 경로 실재」는 미구현 축 · §6.4 CODEOWNERS 는 아직 main 에 없다(#3).

**R4 가 안 본 것(재개 브리프가 그대로 쓸 목록)**: #12 현재 head `fa2bec49` 두 커밋 · #14 최신 CI · 심볼릭링크/gitlink/CRLF/rename 벡터 · 얕은 클론 갈래 · spec/plan 에 대한 D16(전부 intent.md 로만 쟀다) · 착지 후 plan Proof 재판정.

### RD1-P (#6 훅 수정) — 커밋 0 · 미커밋 1파일(의도적) · sha256 11/11 확인
raw: `design/raw-rd1p/` 6개(`04-*` 는 성능 계측 2회를 중지로 죽여 비어 있음) · PR #6 은 클론 당시 그대로(HEAD `f651dc1`)
- **미커밋으로 남긴 것**: `tests/test_hooks.sh` +27/−0(순수 추가) — 픽스처에 파일 심링크 `dep.sh → scripts/deploy.sh` + 케이스 7건.
  **red 실측 완료**: `79 → 86 케이스, 82 passed / 4 failed`. 새 차단 4건이 전부 `rc=0 (기대 2)` — PG17 `/./` · PG18 파일 심링크 · PG19 `cd &&` · PG20 대문자.
  **음성 대조 3건(PG21~23)은 그린** = `cd` 섞인 명령·심링크 픽스처가 거짓 양성을 안 만든다는 기준선 확보. 기존 79건 전부 그린.
- **부모 재결 1줄**: 시험 커밋만 올리면 PR #6 게이트가 빨간 채로 남는다 → 레인이 「올리지 않는 쪽」을 택했다. 재개 시 이 판단을 확인할 것.
- 원복: sha256 11파일 중 10파일 HEAD 와 바이트 동일(다른 하나가 위 `test_hooks.sh`) · 배경 프로세스 kill · 임시 트리 삭제.
- **재개 순서(레인 권고)**:
  (a) CD-1 — `.claude/hooks/production-gate.sh` 13행의 백틱 친 `docs/production-notes.md` 하나만 벗기면 된다(전수 조사 raw 07: 백틱 친 비실재 경로는 그 한 자리뿐. `_lib.sh:75` 의 `` `//` `` 는 `[ -e "//" ]` 가 참이라 무해 — 미실측)
  (b) F6-4 성능 — `_lib.sh:53` · `production-gate.sh:104` 의 `${…//[[:space:]]/}` 두 자리를 `case … in *[![:space:]]*)` 로. 두 형태 동치는 bash 3.2/5.3 양쪽 확인했으나 **원문이 raw 에 없다(트랜스크립트에만)** — 재개 시 다시 남길 것
  (c) 🔴 **성능 계기를 다시 짜라** — 리뷰어의 「32KB 31.9초」와 달리 이 맥북에서 32KB 한 칸이 **CPU 9분 52초**(`ps` TIME)를 먹고 안 끝났다. 페이로드 공백 밀도 차로 보이나 **미확정**. 64KB 버리고 1·2·4·8·16KB 곡선 + 칸마다 timeout. 하네스 `design/_perf-rd1p.sh`·`_idiom-rd1p.sh` 는 그대로 있다
  (d) 그 다음에야 F6-1 경로 해석 구현
- **`cd` 처방 설계 판단(코드는 없음)**: fail-closed 전면 차단이 아니라 **후보 기준 디렉터리 집합을 넓히는 쪽** — `BASES` 에 `cd`/`pushd` 목적지를 더하되 기존 base 는 지우지 않는다(탐지를 넓히기만 하므로 `cd X || …` 실패 갈래에서도 안 놓친다). 해석 불가한 `cd $VAR` 는 `production` 토큰이 함께 있을 때만 차단.

---

# RD1 결과 (2026-09-08~09 · 워크플로 wf_8557b35e-0f1 · 15에이전트 0에러)

## 판정: 다섯 레인 전부 **조건부** (차단 7 · 등재 34)
| 레인 | 차단 |
|---|---|
| A #8 | 출하 docstring/PR본문이 「not_applicable」이라 적는데 실측은 `unavailable` + 사유 + candidates 1건 |
| B #10 | 표 28행만 고치고 **산문 20줄을 남겨 없던 자기모순을 만들었다**(정정 전엔 일치했다) |
| C #6 | `production-gate.sh` **250행 이중 백슬래시**가 주 차단 메시지 경로를 죽였다(94/94 그린이었다 — 부분 문자열 단언이 bash exec 실패 진단문을 먹는다) |
| D #14 | PR 본문이 브랜치 실물과 다르다(E-4 「후:」가 옛 문면 · 게이트 수치 6 vs 실측 15) |
| E #12 | ① `check_all.sh <오타>` = 0/0/0 rc=0 거짓 그린 ② 「표 밖 전이 전부 거부」가 거짓(표 4행 중 3행 도달 불가, 표 밖 3종 통과) ③ PR 본문에 자기가 거짓 판정한 문장 4개 생존 |

## 적대 검증 4렌즈 — 새 축도 뚫렸다
- **id 세탁**(차단): `git mv` → `ID_DIRNAME_MISMATCH` 가 id 개명을 **강제** → 기준점 조회 0건 → 브랜치 자기 커밋으로 후퇴 → 전면 개작 자기승인, 정본 게이트 `16 passed rc=0`
- **2-PR 세탁**(차단): accepted spec 삭제 PR 이 초록(VANISHED 가 형에 매여 안 돎) → 다음 PR 에서 재도장. 한 PR 안에서 하면 막힌다
- **거짓 빨강 3종 신설**: base≠main → **D16 자신의 음성 대조 2개 사망** · 중복 id → 정상 승인 영구 봉쇄 · `core.autocrlf` → 순수 도장 빨강
- **거짓 그린**: fork PR head_ref=main → D16 꺼지고 **E5 계기가 함께 초록**(계기가 우회를 인증)
- 뿌리 하나 더: 「두 blob 바이트 비교」가 거짓 — 기준점만 blob, 지금 파일은 **워크트리**(필터 적용)

## 완결성 비평이 직접 잰 것 (가장 큰 발견)
- 🔴 **N1**: 같은 SHA 7289140 이 attached `16/0/0 rc=0` · **detached `15 passed 1 failed rc=1`**. 죽는 시험이 #12 자신의 계기.
  리뷰어 5 + 적대 4 **전원이 attached 로만 재서** 그 바닥 위에 판정을 쌓았다. 머지되면 이후 모든 격리 트리 리뷰 기준선이 1 failed.
- **N2**: 여섯 브랜치 결합 **충돌 0건** · SHA `870ed50` · attached `21 passed` · detached `20/1 rc=1`
- **N9**: 반례 5건이 전부 단일 렌즈 결과이고 셋은 서로 충돌 → 계기 다원화 필요
- 브랜치별 detached: #8 `54c1d00` 17/0/1 · #6 `bf63424` 17/0/1 · #10 `f6d2115` 15/0/1 · #11 `968bce1` 15/0/2 · #12 `7289140` **15/1/0 rc=1** · #14 `cb20a67` 15/0/1
- CD-1 전제가 틀렸다: 그 게이트는 `origin/main`·#6 head·결합에서 **이미 PASS**

## 부모 결정
1. **§10.3 투 스트라이크 성립** — 축1(diff 모양 · git 소유) 사망, 축2(사슬 id · **승인 PR 작성자가 쓴다**) 사망.
   → 축3 의 어휘 소유자 = **base 브랜치 이력**: 「base 의 accepted id 집합에서 사라진 것 + head 가 `supersedes:` 로 가리키는가」. PR 작성자는 base 에서 id 를 없앨 수 없다. id 세탁·2-PR 세탁을 동시에 닫는다.
2. **N1 은 머지 전에 닫는다** — 시험 삭제가 아니라 **계기가 자기 전제를 세우게** 한다(브랜치를 못 풀면 PASS 도 FAIL 도 아닌 SKIP) + 짝이 되는 살아있음 시험.
3. 머지 순서(비평 권고 · 채택): **#8 → #6 → #11 → #12 → #14 → #10**
   (#10 은 #6·#11 뒤라야 라벨이 참 · #14 는 #12 뒤라야 main 문서가 없는 동작을 서술하지 않는다)
4. 머지는 RD2 착지 후 일괄. #9 는 머지 가능이나 base 를 흔들지 않기 위해 대기.

## RD2 (워크플로 wf_1c52353b-df4) — 진행 중
5레인(차단 7 + 적대 반례 8종 + detached 기준선) → 독립 리뷰 → 적대 재검증 4렌즈(3개는 RD1 반례 전량 재현 · 1개는 **렌즈 간 교차 재현**) → 결합 트리 attached/detached 양모드 판정.
