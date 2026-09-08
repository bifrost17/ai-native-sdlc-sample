# CLAUDE.md

## Commands
- `make check` — 게이트 정본. healthy output 예: `6 passed, 0 failed`(rc=0). 지금은 W0 골격
  6검사만(§`scripts/check_all.sh`) — 아티팩트 검증기는 W1 이 `scripts/check_artifacts.py` 로 더한다.
- `make test` — W1 까지는 placeholder. healthy output: `no tests yet (W1)`.
- `bash scripts/gates/10-docs.sh` — 문서 게이트 단독 실행. healthy output 예: `5 passed, 0 failed`.

## Conventions
- 산문은 한국어, frontmatter 키·상태 어휘(`draft|accepted|rejected|superseded`)·절 제목 토큰은
  영문 고정 — 리터럴 검사가 언어를 타지 않게 한다.
- 구현 언어는 stdlib(Python) + bash/jq 만. 외부 패키지를 추가하지 않는다.
- 셸은 bash 3.2(macOS 기본) 호환: `mapfile`·연관 배열 금지, `wc -l` 뒤엔 `| tr -d ' '`.
- `git add -A` 금지 — 변경 파일을 이름으로 add 한다.
- 플레이스홀더 표기는 `‹…›`(홑화살괄호)다. `[…]`·`<…>` 는 정상 산문과 겹쳐 검증기 오탐을 낸다.

## Architecture
사슬은 `intent.md → spec.md → plan.md → 코드·시험 → PR·리뷰 → merge` 순서로만 흐르고,
각 단계는 이전 단계 커밋의 sha(`upstream: <file>@<sha>`)를 읽어야 다음으로 간다. 강제는
세 층(파일 편집을 막는 훅 → 머지를 막는 CI → 승인을 막는 브랜치 보호/CODEOWNERS)이 각자
독립적으로 겹쳐 잰다 — 한 층이 우회돼도 나머지가 남는다.

## Verifying your work
작업을 끝냈다고 보고하기 전에 `make check`(또는 해당 게이트 스크립트)를 직접 돌리고 그
원문 출력을 보고에 붙인다 — rc 값과 `N passed, N failed` 줄을 함께. 시험이 실패하면
**시험이 아니라 코드를 고친다("If a test fails, fix the code, not the test")**. 못 돌린
검사는 "확인 못 함"이라 적는다 — 안 돌리고 통과라 쓰지 않는다.

## Things Claude gets wrong
- `bash -n` 은 `[` 의 짝 `]` 누락 같은 런타임 오류를 못 잡는다 — 실제로 실행해서 확인한다.
- BSD `wc -l`(macOS) 은 출력 앞에 공백을 붙인다 — 수치 비교 전에 `| tr -d ' '`.
- macOS 기본 셸은 bash 3.2 다(연관 배열·`mapfile` 없음) — GNU bash 4+ 전용 문법을 쓰지 않는다.
- 플레이스홀더 표기는 `‹…›` 이지 `[…]` 가 아니다 — 대괄호는 정상 산문 문장과 안 갈린다.

같은 실수를 두 번 하면 이 파일에 등재한다.
