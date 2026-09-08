# 상태 어휘 · 전이 · 증거

이 문서가 **상태 어휘의 유일한 정의처**다. `status:` 값의 뜻과 그 값이 바뀌는 조건을
여기 한 곳에서만 정의한다 — 참조 레포 한 곳은 상태 어휘가 다섯 벌 공존했고, 그러면
「accepted 가 무슨 뜻인가」를 사람마다 다르게 답하게 된다.

## 어휘 — 넷뿐이다

| 값 | 뜻 | 누가 쓰는가 |
|---|---|---|
| `draft` | 발의됐고 아직 승인되지 않았다. 자유롭게 고친다. | 발의자 |
| `accepted` | 승인됐다. **이후 내용 변경 금지** — 바뀌어야 하면 새 아티팩트가 supersede 한다. | product owner |
| `rejected` | 승인되지 않기로 결정됐다. 파일은 남는다(왜 안 했는지가 기록이다). | product owner |
| `superseded` | 뒤에 온 아티팩트가 대체했다. 대체한 쪽의 `supersedes:` 가 이 파일을 가리킨다. | 새 아티팩트 발의자 |

다섯 번째 값을 만들지 않는다. `in-review` · `wip` · `approved` 같은 동의어가 늘면
검사식이 언어를 타기 시작하고, 그 순간 리터럴 검사는 죽는다.

## 전이 · 증거 · 기계 검사

| 전이 | 누가 | 증거(사람이 보는 것) | 기계가 재는 것 |
|---|---|---|---|
| — → `draft` | 발의자(또는 이슈 폼) | 첫 커밋 | frontmatter 필수 키 전량 · `created` 가 오프셋 포함 ISO8601 · `id` == 디렉터리명 · `kind` == 파일명 |
| `draft` → `accepted` | product owner | `status:` 를 바꾼 커밋이 **머지된 PR** 안에 있다 | 기본 브랜치가 아닌 곳의 `accepted` 는 **바뀐 줄이 `status:` 하나뿐일 때만** 통과한다(D16 · 아래 절). 그 밖의 줄이 함께 바뀌면 red(`ACCEPTED_ON_BRANCH`) |
| `draft` → `rejected` | product owner | PR close | 위와 같다 |
| `accepted` → `superseded` | 새 아티팩트 발의자 | 새 아티팩트의 `supersedes:` 와 옛 파일의 상태 변경이 **같은 PR** 안에 | `supersedes:` 가 `none` 또는 `NNNN-slug` 형식(`SUPERSEDES_INVALID`) |

`accepted_at` 같은 시각 필드를 두지 않는다 — git 이 안다(`git log -S'status: accepted'`).
자기 신고 필드는 `created` 하나뿐이고, 그것이 git 이 모르는 유일한 값이라서 남긴다.

## 왜 「브랜치 위의 accepted」가 red 인가

승인은 **머지된 PR** 이라는 사건이다. 브랜치에서 스스로 `accepted` 로 바꾸고 그대로
일을 시작하면, 승인 없이 승인의 표시만 얻는다. 검증기는 이렇게 잰다:

1. HEAD 가 기본 브랜치(`main`, 없으면 `master`) **그 커밋**이면 검사하지 않는다 — 머지된
   뒤다. 브랜치 **이름**이 같은 것만으로는 건너뛰지 않는다: fork 의 PR 은 `head_ref` 가
   그 fork 의 브랜치 이름이라 `main` 일 수 있고, 이름만 보고 건너뛰면 PR 하나로 이 검사가
   통째로 꺼진다. detached HEAD 면 `INTENT_CHECK_BRANCH`·`INTENT_CHECK_DEFAULT_BRANCH` 를
   읽는다.
2. **base 에서 사라진 accepted 를 먼저 센다.** 기본 브랜치에서 `accepted` 였던 아티팩트가
   이 브랜치 트리에 `(형, 사슬 id)` 째로 없으면 `ACCEPTED_ARTIFACT_VANISHED` 다. 형을
   가리지 않고(intent 를 검사하는 회차도 사라진 spec 을 본다), 검사 중인 파일이
   `accepted` 인지도 가리지 않는다 — 「지우기만 하는 PR」을 먼저 머지시켜 base 에서 승인
   기록을 없애고 다음 PR 에서 자기 승인하는 2-PR 세탁을 그 자리에서 끊는다. 사라짐의
   유일한 출구는 head 에 그 id 를 `supersedes:` 로 가리키는 아티팩트가 있는 것이고, 그
   후속이 **같은 브랜치에서 스스로 accepted 가 된 것**이면 증인이 못 된다(그것이 세탁이다).
3. 기준점을 정한다. 조회는 **합집합**이다 — 같은 사슬 id 의 같은 형(여럿이면 같은 경로를
   먼저) ∪ base 의 그 경로 ∪ base 에서 **본문 바이트가 같은** 같은 형 아티팩트. 셋 다
   0건이면 사슬이 이 브랜치에서 태어난 경우이고, 이 브랜치 커밋 중 **아직 `accepted` 가
   아니었던 가장 최근 판**이 기준점이다 — 도장을 찍을 원본이다.
4. 기준점 blob 과 지금 판을 **바이트로** 꺼내 견준다. 「지금 판」은 워크트리 파일이 아니라
   **HEAD 의 blob** 이다 — 워크트리는 `core.autocrlf`·`.gitattributes` 의 `eol`·`ident` 를
   거친 바이트라, 그것을 기준점 blob 과 견주면 같은 커밋이 **읽는 사람의 git 설정에 따라**
   빨갛고 초록이다. 워크트리가 HEAD 와 다를 때만(그 판정도 `git diff` 가 한다) 그 바이트를
   하나 더 얹어 **엄한 쪽**으로 판정한다 — 미커밋 편집의 포착은 그대로다. `git diff` 의
   출력 **모양**은 판정에 들어오지 않는다: 무엇을 binary 로 볼지·diff 드라이버·`+++`/`---`
   접두·rename 탐지는 전부 git 이 소유하는 어휘라, 그것을 읽는 축은 git 이 형식을 바꾸는
   날 죽는다. 실제로 그 축은 8종의 우회에 뚫렸다.
5. frontmatter 의 `status` **값 하나만** 다르고 나머지 키의 줄과 본문이 바이트까지 같으면
   도장이다. 그 밖은 `ACCEPTED_ON_BRANCH`. 도장이어도 전이가 허용 표 밖이면
   `ACCEPT_TRANSITION_NOT_ALLOWED`.

**축이 세 번 바뀌었고, 바뀐 것은 「누가 그 어휘를 쓰는가」다.** 축 1 은 `git diff` 출력의
텍스트 모양을 읽었고 그 어휘의 주인은 git 이었다. 축 2 는 사슬 id 로 기준점을 찾았는데,
그 어휘의 주인은 **승인 PR 작성자**였다 — 디렉터리를 개명하면 `ID_DIRNAME_MISMATCH` 가
id 개명을 강제하고, id 가 바뀌면 기준점 조회가 0건이 되어 브랜치 자기 커밋으로 후퇴한다.
축 3 의 물음(2번)은 **base 브랜치 이력**이 소유한다. PR 작성자는 base 에서 id 를 없앨 수
없다.

### D16 — 「도장만 찍는 커밋」은 브랜치에서도 통과한다

전이 표가 요구하는 승인 행위 자체가 「PR 안에서 `status:` 를 고치고 머지」다. 브랜치 위의
`accepted` 를 예외 없이 막으면 **승인 PR 자체가 CI 에서 빨개져** 사슬이 한 칸도 전진하지
못한다. 그래서 예외를 하나 둔다. 폭은 정확히 한 줄이다:

> 기준점과 견줘 frontmatter 의 `status` **값 하나만** 바뀌었으면 통과. 그 밖의 내용이
> 한 바이트라도 함께 바뀌면 red.

근거는 승인의 뜻이다. 승인은 **이미 검토된 문서에 도장을 찍는 행위**이지 「고치면서 승인」이
아니다. 내용을 바꾸려면 draft 로 되돌려 다시 검토받는다 — 그래야 도장이 무엇을 승인한
것인지가 한 가지로 읽힌다. 예외가 열어 두지 **않는** 자리:

| 상황 | 판정 | 왜 |
|---|---|---|
| 기본 브랜치의 draft 를 `status` 값만 바꿔 승인 | 통과 | 도장 |
| `status:` 와 본문(또는 `author` 같은 다른 frontmatter 키)을 같은 커밋에서 함께 변경 | red | 고치면서 승인 |
| draft 단계 없이 처음부터 `accepted` 로 태어난 파일 | red | 도장 찍을 원본(승인 전 판)이 없다 |
| 승인 커밋을 아직 만들지 않았고 작업 트리 변경이 `status` 값뿐 | 통과 | 승인 커밋을 만들 수 있어야 한다 |
| 승인 커밋 뒤에 내용을 다시 편집(커밋했든 작업 트리에 남았든) | red | `accepted` 이후 불변 |
| 기본 브랜치에서 이미 `accepted` 인 파일을 브랜치에서 편집 | red | 같음 |
| `status:` 값 뒤에 인라인 주석(`# PO 승인 …`)을 붙여 승인 | red | 승인 커밋에 함께 들어온 산문은 아무도 검토하지 않았다 |
| NUL 바이트·`.gitattributes` 로 git 이 diff 를 못 내게 만들고 전면 개작 | red | 판정이 diff 텍스트가 아니라 바이트다 |
| 본문 줄이 `---`/`++` 로 시작해 diff 접두 필터에 걸리는 개작 | red | 같음 |
| 바뀐 줄이 **펜스 안** pseudo-`status:` 또는 본문의 `status:` 모양 1줄 | red | 도장은 frontmatter 의 `status` 키에서만 일어난다 |
| accepted 정본을 개명(파일·디렉터리)하고 브랜치가 심은 draft 위에 재도장 | red | 기준점 조회가 합집합이다 — id 로도, base 의 그 경로로도, 본문 바이트로도 찾는다 |
| accepted 정본을 지우고 **새 id 로 갈아타** 자기 승인 | red | `ACCEPTED_ARTIFACT_VANISHED` — base 의 accepted 집합에서 사라진 것은 PR 작성자가 지울 수 없는 어휘다 |
| accepted **spec** 을 지우고 intent 만 도장(형을 넘는 사라짐) | red | 사라짐 검사는 형을 가리지 않는다 |
| 아무것도 도장하지 않고 accepted 를 지우기만 하는 PR(2-PR 세탁의 1단계) | red | 사라짐 검사는 검사 대상의 `status` 도 가리지 않는다 |
| 지운 accepted 를 `supersedes:` 로 가리키는 후속을 **같은 브랜치에서** accepted 로 | red | 자기 도장한 후속은 대체의 증인이 못 된다 |
| `core.autocrlf`·`eol=crlf` 클론에서의 순수 도장 | 통과 | 견주는 것이 워크트리가 아니라 머지되는 blob 이다 |
| 워크트리는 같아 보이는데 **머지되는 blob 의 본문**이 갈린 커밋 | red | 같음(반대 방향) |
| base 에 같은 사슬 id 가 두 경로인데 같은 경로에서 도장 | 통과 | 아카이브 사본 하나로 정상 승인이 영구 봉쇄되지 않는다 |
| `rejected` → `accepted` · `superseded` → `accepted` | red | 되살리기다. 대체하려면 새 아티팩트를 만들고 `supersedes:` 로 가리킨다 |

허용 전이는 한 곳에 데이터(`ACCEPT_TRANSITIONS`)로 있다 —
`draft`→`accepted` · `draft`→`rejected` · `draft`→`superseded` · `accepted`→`superseded`.
🔴 **이 표가 다스리는 것은 `accepted` 로 들어오는 전이뿐이다.** 이 검사 전체가 「지금 파일이
`accepted` 일 때」만 도므로 도착 상태는 언제나 `accepted` 이고, 나머지 세 줄은 도달하지
않는다. 「표에 없는 전이는 전부 거부한다」는 예전 문면은 거짓이었다 — 표 밖 전이
(`accepted`→`draft` · `accepted`→`rejected` · `superseded`→`draft`)는 이 축의 사정거리
밖이라 그냥 지나간다. 특히 **`accepted`→`draft` 를 표에 넣어 거부하면 안 된다**: 그것은 이
검사가 스스로 처방하는 경로다(내용을 바꾸려면 draft 로 되돌려 다시 검토받는다). 표를
「완성」하려는 다음 사람이 그 줄을 막으면 승인된 문서를 고칠 방법이 사라진다.
그래서 남는 구멍이 하나 있다 — **`accepted` 를 `draft` 로 내리면서 같은 커밋에서 본문을
통째로 가는 것**은 이 검사가 보지 않는다(등재). 그 판은 더 이상 승인을 주장하지 않고
이력은 git 이 갖고 있으므로 red 로 만들지 않았다.
되살리기 두 갈래(`rejected`→`accepted` · `superseded`→`accepted`)를 막은 것은 부모 세션의
잠정 결정이고 product owner 확인을 기다린다(spec 의 F2). 되돌리려면 그 표에 한 줄을 더한다.

**이 검사가 안 도는 경우가 있고, 그때는 그렇다고 말한다.** 브랜치나 기본 브랜치를 못
정하면 검증기는 판정을 포기하고 `ACCEPTED_BRANCH_CHECK_SKIPPED` 를 **note 로 출력**한다.
**D16 판정이 못 도는 경우도 같은 note 로 묶는다** — 기준점을 세우는 `git rev-list` 나
`git ls-tree` 가 실패하면 통과시키지 않고 사유를 그 note 에 적는다. note 는 rc 를 올리지
않는다 — 못 잰 것을 잰 척하지 않기 위해서다.

그 note 는 **게이트 출력으로 흘러나온다**. `run_gate` 는 PASS 일 때 함수 출력을 통째로
버리므로, 예전에는 「검사가 안 돌았다」가 CI 로그에 한 줄도 남지 않았다 — 셀 수 있다는
주장만 있고 셀 것이 없었다. 지금은 `check11_intent_chain` 이 rc=0 이어도 note 줄을 그대로
흘려보내므로 `grep -c ACCEPTED_BRANCH_CHECK_SKIPPED` 한 번으로 「그 자리가 조용히 비었는지」를
센다. 브랜치를 풀 수 있는 회차의 답은 0 이고, detached 체크아웃에서 env 도 없으면 0 이
아니다 — 같은 커밋이 attached 에서 0, detached 에서 2 다. 그러니 **「0 이면 건강」은 전제가
선 회차에서만 뜻이 있다**. 그 부재 PASS 는 살아 있음 계약과 짝이어야 하므로, 시험은 ①
브랜치를 풀 수 없으면 PASS 도 FAIL 도 아닌 SKIP 이고 ② 풀 수 있을 때는 임시 클론에 위반을
심어 게이트가 실제로 죽는지 잰다.

**CI 에서도 이 검사는 돈다.** `actions/checkout` 은 PR 을 detached HEAD 로 두어 검사가
통째로 빠졌었다(집행력 0). 지금은 워크플로가 `github.head_ref`/`github.base_ref` 를
`INTENT_CHECK_BRANCH`·`INTENT_CHECK_DEFAULT_BRANCH` 로 넘기고 기준 브랜치를
`refs/remotes/origin/<base>` 로 확보한다. 「안 돌았다」는 「통과」가 아니므로, 그 배선이
살아 있는지는 시험이 **위반을 심어 red 가 나는 것**으로 확인한다. 이 검사와 브랜치 보호는
겹치는 게 아니라 서로의 사각을 맡는다.

## `accepted` 이후 불변

`accepted` 인 파일의 내용을 고치는 것은 승인 기록을 소급 변조하는 일이다. 고쳐야 할
이유가 생기면 새 아티팩트를 만들고 `supersedes:` 로 옛 것을 가리킨다. 옛 파일의 상태는
같은 PR 에서 `superseded` 로 바꾼다 — 두 변경이 한 PR 에 있어야 「무엇이 무엇을
대체했는지」가 한 커밋 범위로 읽힌다.

로컬 편집 차단(훅)은 이 규칙의 **빠른 되먹임**이고, 정본 판정은 PR·리뷰다. 훅이 없거나
꺼진 환경에서도 규칙 자체는 살아 있다.

## 상류 승인 — spec·plan 이 무엇을 읽었는가

`spec` 은 `upstream: intent.md@<sha>` 를, `plan` 은 `upstream: spec.md@<sha>` 를 갖는다.
검증기는 그 sha 를 `git show` 로 **실제로 열어** ① 그 판의 `status` 가 `accepted` 인지
② `id` 가 자기와 같은지 본다. 파일명만 적고 sha 를 비우면 「어느 판을 읽었는지」가
사라지고, 그러면 상류가 바뀌어도 하류는 낡았다는 것을 아무도 모른다.

sha 를 못 열면 rc=2(판정 불가)다. **rc 2 는 통과가 아니다** — 얕은 클론이나 rebase 로
객체가 사라진 상태를 「문제 없음」으로 넘기지 않는다.
