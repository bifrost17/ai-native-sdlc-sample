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
| `draft` → `accepted` | product owner | `status:` 를 바꾼 커밋이 **머지된 PR** 안에 있다 | 기본 브랜치가 아닌 곳에서 기본 브랜치와 다른 내용으로 `accepted` 이면 red(`ACCEPTED_ON_BRANCH`) |
| `draft` → `rejected` | product owner | PR close | 위와 같다 |
| `accepted` → `superseded` | 새 아티팩트 발의자 | 새 아티팩트의 `supersedes:` 와 옛 파일의 상태 변경이 **같은 PR** 안에 | `supersedes:` 가 `none` 또는 `NNNN-slug` 형식(`SUPERSEDES_INVALID`) |

`accepted_at` 같은 시각 필드를 두지 않는다 — git 이 안다(`git log -S'status: accepted'`).
자기 신고 필드는 `created` 하나뿐이고, 그것이 git 이 모르는 유일한 값이라서 남긴다.

## 왜 「브랜치 위의 accepted」가 red 인가

승인은 **머지된 PR** 이라는 사건이다. 브랜치에서 스스로 `accepted` 로 바꾸고 그대로
일을 시작하면, 승인 없이 승인의 표시만 얻는다. 검증기는 이렇게 잰다:

1. 현재 HEAD 가 기본 브랜치(`main`, 없으면 `master`)면 검사하지 않는다 — 머지된 뒤다.
2. 기본 브랜치가 아니면 그 브랜치의 같은 경로 파일을 `git show` 로 꺼내 지금 파일과
   바이트로 대조한다. 다르면(또는 기본 브랜치에 아직 없으면) `ACCEPTED_ON_BRANCH`.

**이 검사가 안 도는 경우가 있고, 그때는 그렇다고 말한다.** 기본 브랜치 참조가 로컬에
없거나(얕은 클론) HEAD 가 detached 이면(CI 의 PR 체크아웃이 대표적) 검증기는 판정을
포기하고 `ACCEPTED_BRANCH_CHECK_SKIPPED` 를 **note 로 출력**한다. note 는 rc 를 올리지
않는다 — 못 잰 것을 잰 척하지 않기 위해서다. 그 자리는 브랜치 보호(리뷰 필수 · 상태
체크 필수)가 대신 막는다. 두 장치는 겹치는 게 아니라 서로의 사각을 맡는다.

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
