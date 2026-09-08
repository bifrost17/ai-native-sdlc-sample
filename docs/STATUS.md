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

1. 현재 HEAD 가 기본 브랜치(`main`, 없으면 `master`)면 검사하지 않는다 — 머지된 뒤다.
   detached HEAD 면 `INTENT_CHECK_BRANCH`·`INTENT_CHECK_DEFAULT_BRANCH` 를 읽는다.
2. 기본 브랜치가 아니면 기준점을 정한다. 기준점은 **기본 브랜치에 같은 사슬 id 의 같은 형
   아티팩트가 있으면 그것**이고(경로가 아니라 id 로 찾는다 — 경로로 찾으면 개명 한 번에
   기준점이 브랜치 자기 커밋으로 후퇴한다), 없으면(사슬이 이 브랜치에서 태어났다) 이
   브랜치 커밋 중 **아직 `accepted` 가 아니었던 가장 최근 판** — 도장을 찍을 원본이다.
3. 기준점 blob 과 지금 파일을 **바이트로** 꺼내 견준다. `git diff` 의 출력 모양은 판정에
   들어오지 않는다 — 무엇을 binary 로 볼지·`.gitattributes` 의 diff 드라이버·`+++`/`---`
   접두·rename 탐지는 전부 git 이 소유하는 어휘라, 그것을 읽는 축은 git 이 형식을 바꾸는
   날 죽는다. 실제로 그 축은 8종의 우회에 뚫렸다.
4. frontmatter 의 `status` **값 하나만** 다르고 나머지 키의 줄과 본문이 바이트까지 같으면
   도장이다. 그 밖은 `ACCEPTED_ON_BRANCH`. 도장이어도 전이가 허용 표 밖이면
   `ACCEPT_TRANSITION_NOT_ALLOWED`.

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
| accepted 정본을 개명(파일·디렉터리)하고 브랜치가 심은 draft 위에 재도장 | red | 기준점을 경로가 아니라 사슬 id 로 찾는다 |
| accepted 정본을 지우고 **새 id 로 갈아타** 자기 승인 | red | `ACCEPTED_ARTIFACT_VANISHED` — 승인 기록의 사라짐은 id 로 셀 수 있다 |
| `rejected` → `accepted` · `superseded` → `accepted` | red | 되살리기다. 대체하려면 새 아티팩트를 만들고 `supersedes:` 로 가리킨다 |

허용 전이는 한 곳에 데이터(`ACCEPT_TRANSITIONS`)로 있고 **그 밖은 전부 거부**한다 —
`draft`→`accepted` · `draft`→`rejected` · `draft`→`superseded` · `accepted`→`superseded`.
되살리기 두 갈래를 막은 것은 부모 세션의 잠정 결정이고 product owner 확인을 기다린다
(spec 의 F2). 되돌리려면 그 표에 한 줄을 더한다.

**이 검사가 안 도는 경우가 있고, 그때는 그렇다고 말한다.** 브랜치나 기본 브랜치를 못
정하면 검증기는 판정을 포기하고 `ACCEPTED_BRANCH_CHECK_SKIPPED` 를 **note 로 출력**한다.
**D16 판정이 못 도는 경우도 같은 note 로 묶는다** — 기준점을 세우는 `git rev-list` 나
`git ls-tree` 가 실패하면 통과시키지 않고 사유를 그 note 에 적는다. note 는 rc 를 올리지
않는다 — 못 잰 것을 잰 척하지 않기 위해서다.

그 note 는 **게이트 출력으로 흘러나온다**. `run_gate` 는 PASS 일 때 함수 출력을 통째로
버리므로, 예전에는 「검사가 안 돌았다」가 CI 로그에 한 줄도 남지 않았다 — 셀 수 있다는
주장만 있고 셀 것이 없었다. 지금은 `check11_intent_chain` 이 rc=0 이어도 note 줄을 그대로
흘려보내므로 `grep -c ACCEPTED_BRANCH_CHECK_SKIPPED` 한 번으로 「그 자리가 조용히 비었는지」를
센다. 건강한 회차의 답은 0 이다.

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
