---
name: claims-ux-copy
description: Apply the org's UX wording policy (U1 error messages · U2 the five claim status labels and their next step · U3 waiting notices) to any Korean customer-facing text of the claims status service — error and empty states, status screens, loading and delay notices, SMS/email notifications for the customer portal, adjuster and agent paths. Use whenever writing or reviewing spec.md, UI strings, screen copy or a customer notification, and whenever a change adds a failure path, a status display or a wait, instead of inventing wording or looking up the policy files yourself.
---
<!-- 예시 — 팀 스킬이 아니다. 플러그인은 org-skills/skills/ 만 로드한다. 이 파일은 청구 상태 서비스를 한 프로젝트로 보고
     PROJECT-POLICY.md(같은 폴더)의 슬롯을 채웠을 때 스킬이 어떤 모습이 되는지 보여 준다. org-skills/examples/README.md -->
# Claims UX — wording (U1 · U2 · U3)

`policies/ux.md` v0 is the source of truth. Each clause below is quoted verbatim (Korean); the lines
after it say what to do when you write or review copy. Wording rules that are about tone and
notation (존댓말, 금칙어, 날짜·금액 표기) belong to `policies/brand.md` (B1~B7) — this skill does not
repeat them, but every string you write must satisfy both. If no skill in this repo carries the brand
clauses yet, read `policies/brand.md` itself before you write customer-facing words.

The five status words themselves are brand **B4**; U2 is what the screen must show around them.

## U1 Error messages
> **U1** 오류 메시지는 세 요소: 무엇이 안 됐는지 · (알 수 있으면) 왜 · 다음에 할 행동. 내부 코드·스택은 금지.

Every message a customer, adjuster or agent can see on a failure carries the three elements. The
order below and the one-or-two-sentence length are this skill's default, not policy text — U1 fixes
the three elements, not their order:
- **무엇이 안 됐는지** — name the action that failed in the user's words ("청구 내역을 불러오지 못했습니다"),
  not the component that threw ("claims-core 호출 실패").
- **왜** — only when the system actually knows and the customer can act on it (세션 만료, 첨부 용량
  초과, 조회 조건 불일치). If the cause is unknown or internal, leave it out. Do not guess a cause.
- **다음에 할 행동** — one concrete action: 다시 시도, 다시 로그인, 파일 크기를 줄여 다시 첨부,
  고객센터 문의(전화번호·운영시간은 정책 오너가 정한 값을 그대로). If the action is "wait", U3 applies —
  give the time, not "잠시 후".
- **금지**: U1 의 문면은 「내부 코드·스택」이다. 이 스킬은 예외 이름 · 스택 · 상태 코드 · 상관관계 ID ·
  SQL · 내부 시스템 이름을 그 범주로 읽는다(내부 URL 도 같이 본다 — 이것은 조항을 **넓혀 읽은 것**이므로
  다투는 자리가 생기면 정책 오너에게 묻는다). 그런 값은 로그·감사 기록에 남기고 화면 문구에는 넣지 않는다.
  "오류가 발생했습니다" 단독도 U1 위반이다 — 세 요소 중 둘이 빠졌다.

Write the strings for **every** failure branch the change introduces: 조회 실패, 권한 없음, 없음,
타임아웃, 첨부 실패, 세션 만료. A spec that lists a failure path without its message is not done.

## U2 Status display
> **U2** 상태 표시는 brand B4 의 다섯 어휘 그대로, 각 상태에 「다음 예정」 한 줄을 붙인다(예: 보완요청 → 무엇을 보내야 하는지).

- The label is exactly one of **접수 · 심사중 · 보완요청 · 지급완료 · 종결**. No synonym (처리중, 완료,
  진행중, 대기), no English (In Review, Paid), no invented sixth state. If a screen needs a state the
  five do not cover, that is a policy question — write it under 「정책 오너에게 묻는다」, do not coin a word.
- Each displayed status carries **one 「다음 예정」 line** saying what happens next and, where the next
  step belongs to the customer, what they must do. U2 gives one worked example(보완요청 → 무엇을
  보내야 하는지); the list below is **this skill's reading of the other four**, not policy text. Use it as
  the shape of the line, and get the actual content from the business process or the policy owner —
  what a 「다음 예정」 line may say about 계좌, 이의 절차 or 지급 시점 is their decision, not the spec writer's.
  - 접수 → 심사가 언제 시작되는지.
  - 심사중 → 심사 결과가 언제 나오는지(U3 의 확인 시점과 같은 값).
  - 보완요청 → **무엇을** 보내야 하는지(서류 이름) 와 **언제까지** — 이 한 줄만 U2 원문의 예시다.
  - 지급완료 → 지급이 언제 반영되는지.
  - 종결 → 왜 종결인지와, 그다음 경로가 있다면 무엇인지.
- The status word and its 「다음 예정」 line are one unit — a list, a card, a notification and a
  detail screen all show both. Never a bare badge.
- Do not show the status only as a colour or an icon (that is U6).

## U3 Waiting
> **U3** 기다리게 할 때(조회 지연·심사 소요)는 예상 시간 또는 확인 시점을 적는다. 「잠시만 기다려 주세요」 단독 금지.

- Anything that makes a person wait — 조회 스피너, 대기 화면, 심사 소요 안내, 재시도 안내 — states
  either an **예상 시간**("보통 1~2분 걸립니다") or a **확인 시점**("심사 결과는 접수일로부터 영업일
  기준 3일 이내에 알려 드립니다").
- Where the number comes from must be traceable: an SLA in the spec, a measured value, or a value
  the policy owner gave. Do not invent a number, and do not write a range you cannot defend. If no
  number exists yet, the spec records it as an open question — that is not a licence to write
  「잠시만 기다려 주세요」.
- 「잠시만 기다려 주세요」 alone is what U3 names, and any bare synonym of it is the same thing with
  different words — 「처리 중입니다」 is additionally a B4 문제(「처리중」은 금지된 동의어). Whatever the
  wording, a wait line without a time or a checkpoint does not satisfy U3.
- If the wait ends in a notification instead of on screen, say which channel and when
  ("결과는 알림톡으로 보내 드립니다").

## When the copy is for a destructive action
Writing the words for 취소 · 철회 · 삭제 pulls in **U4**, which this skill does not carry: the policy wants a
confirmation step **and** a way back. Do not end such copy at 「되돌릴 수 없습니다」 — that satisfies the
warning half and misses the other half. Load `claims-ux-interaction` and write the confirmation copy and
the way-back copy together.

## What this skill does not do
- It does not decide policy. A case the five status words or the three error elements cannot express
  goes into the spec's open questions with the name of who can answer — the policy owner decides.
- It does not set tone, honorifics, forbidden words, date/amount notation — `policies/brand.md` B1~B7 은
  그 자리의 정본이다(그 조항을 지는 스킬이 이 레포에 아직 없다면 정책 원문을 직접 읽는다).
- It does not cover destructive actions, duplication or accessibility — `claims-ux-interaction`.

## In your summary
List U1, U2 and U3 one by one with the strings you wrote or checked, and say which failure paths,
which statuses and which waits the change touches. If a clause cannot be satisfied for this change,
say so under "areas of concern" instead of choosing an interpretation.
