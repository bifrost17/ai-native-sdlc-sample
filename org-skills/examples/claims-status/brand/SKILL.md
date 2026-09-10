---
name: brand
description: >
  Apply our brand guidelines — policies/brand.md clauses B1-B7 — to every customer-facing
  Korean string. Use when writing or reviewing spec.md for a customer-visible change, when
  drafting a customer notice (SMS, email, push, letter, 상담 스크립트), and when reviewing UI
  copy: 화면 라벨, 버튼, 오류 메시지, 청구 상태 표시, 안내 문구. Also use when asked which
  organization skills apply to customer copy, or whether a draft is on-brand.
  Covers 어조(존댓말 · 한 문장 한 뜻 · 과장 금지), 확약 표현 금지, 사과 문구 꼴, 청구 상태
  5어휘(접수 · 심사중 · 보완요청 · 지급완료 · 종결), 공식 표기, 날짜 · 금액 · 시각 형식,
  이모지 · 느낌표 금지, 「○○○ 고객님」.
  Load this skill instead of inventing tone rules, instead of asking the user for a style guide,
  and instead of listing or reading files under .claude/skills to work out what the policy is —
  the transcribed policy is inside this skill.
---
<!-- 예시 — 팀 스킬이 아니다. 플러그인은 org-skills/skills/ 만 로드한다. 이 파일은 청구 상태 서비스를 한 프로젝트로 보고
     PROJECT-POLICY.md(같은 폴더)의 슬롯을 채웠을 때 스킬이 어떤 모습이 되는지 보여 준다. org-skills/examples/README.md -->
<!-- 정책 정본: bifrost17/intent-sdlc-skills 의 policies/brand.md (v0 draft, 오너 서명 대기).
     이 스킬은 그것을 옮긴 것이며 정책을 만들지 않는다. 아래 「정책 원문」 절이 전사본이므로
     정본 파일이 없는 레포에서도 이 스킬만으로 판정할 수 있다. -->
# Brand — 고객 문구의 어조 · 용어 · 표기

> L3 282: "Apply the skills available to you so the plan conforms to our brand guidelines,
> security policies and UX standards."
> 스킬 레슨(skills-as-institutional-knowledge): "write a skill for institutional knowledge that
> must be applied consistently"
> 같은 레슨: "A skill is a control, though an advisory one. It makes Claude likely to apply the
> policy while the code is written, and nothing forces a session to comply with it."

이 스킬은 **권고적 통제**다. 문구를 막지 않는다 — 문구를 쓰는 자리에서 정책을 적용하고,
적용할 수 없는 자리를 「Flagged concerns」로 드러낸다.

## 언제 쓰나
- **spec 작성** — `spec.md` 의 요구사항·수용기준이 고객에게 보일 문구를 정할 때. 문구 예시를
  spec 에 적는다면 그 예시가 B1-B7 을 지켜야 한다. `Skills applied:` 줄에 `brand@<sha>` 를 남긴다
  (spec 레슨: "The spec, the prompt that produced it, and the skill versions in force are all logged
  in version control" — 줄 번호는 페이지에 보이지 않아 적지 않는다).
- **고객 통지 문구 작성** — 문자·이메일·푸시·안내장·상담 스크립트.
- **UI 문구 리뷰** — 화면 라벨, 버튼, 오류 메시지, 상태 표시, 빈 화면 문구.

대상은 **보험 청구 상태 조회 서비스(고객 포털 · 사정인 · 상담사 경로)와 그 고객 통지**다
(policies/brand.md 「대상」). 사내 문서·코드 주석·커밋 메시지는 대상이 아니다.

## 정책 원문 (policies/brand.md 에서 전사)

### 어조
- **B1** 고객 문구는 존댓말, 한 문장 한 뜻, 과장·감탄 없음("최고의", "완벽한" 금지).
- **B2** 회사가 확약할 수 없는 것을 약속하지 않는다("보장합니다", "무조건", "즉시" 는 근거 조항이 있을 때만).
- **B3** 사과는 사실 + 다음 행동으로 — "불편을 드려 죄송합니다" 단독 사용 금지.
### 용어
- **B4** 청구 상태 어휘는 다섯 개로 고정: 접수 · 심사중 · 보완요청 · 지급완료 · 종결. 동의어(처리중, 완료 등) 금지.
- **B5** 회사·상품·기관 이름은 공식 표기를 그대로(약칭·영문 혼용 금지).
### 표기
- **B6** 날짜는 `YYYY-MM-DD`, 금액은 천 단위 구분 + 「원」, 시각은 24시간제 · KST 표기.
- **B7** 이모지·느낌표 미사용. 고객 이름은 「○○○ 고객님」 꼴.

## 조항별로 이렇게 쓴다

**B1 — 존댓말 · 한 문장 한 뜻 · 과장 없음**
한 문장에 뜻이 둘이면 자른다. 부사로 부풀리지 않는다.
- 이렇게: `청구가 접수되었습니다. 심사 결과는 문자로 안내드립니다.`
- 이렇게 쓰지 않는다: `청구 접수 완료! 최고의 속도로 처리해 드릴게요.` (느낌표 · 과장 · 한 문장 두 뜻)
  — 어체(하십시오체 · 해요체)는 정책이 정하지 않았다. B1 이 요구하는 것은 존댓말이고 「해 드릴게요」도 존댓말이다.
  이 예가 걸리는 것은 어체 때문이 아니다.

**B2 — 확약하지 않는다**
「보장합니다 · 무조건 · 즉시」는 근거 조항(약관·법령·사내 규정)을 댈 수 있을 때만 쓰고, 쓸 때는
그 근거를 문구 옆에 남긴다. 근거가 없으면 사실만 적는다.
같은 꼴이어서 이 스킬이 함께 잡는 말: 「반드시 · 100% · 확실히」. **정책이 든 예는 앞의 셋뿐이다** —
뒤의 셋은 조항의 적용이지 조항이 아니다. 목록을 정책으로 만들려면 `policies/brand.md` 를 고쳐야 한다.
- 이렇게: `보완 서류를 받은 날부터 3영업일 이내에 심사 결과를 안내드립니다. (약관 제12조)`
- 이렇게 쓰지 않는다: `접수하시면 즉시 지급을 보장합니다.`
- 근거가 없을 때: `심사 소요 기간은 서류 확인 상황에 따라 달라집니다.`

**B3 — 사과는 사실 + 다음 행동**
「불편을 드려 죄송합니다」로 끝나는 문장은 그 자체로 위반이다. 무엇이 있었는지(사실)와
무엇을 할 것인지(다음 행동)를 붙인다.
- 이렇게: `2026-09-08 20:00부터 21:30까지 상태 조회가 되지 않았습니다. 원인을 고치고 재발 방지 점검을 마쳤습니다.`
- 이렇게 쓰지 않는다: `이용에 불편을 드려 죄송합니다.` (사실도 다음 행동도 없다)

**B4 — 청구 상태는 다섯 낱말만**

정책이 정한 것은 **다섯 낱말과, 동의어(처리중 · 완료 등)를 쓰지 않는다는 것**까지다.
아래 표의 「뜻」 열과 「쓰지 않는 말」 열은 **이 스킬의 읽기이지 정책 문언이 아니다** —
어느 상태가 어느 낱말인지는 정책이 정하지 않았고, 지급 없이 끝난 건과 지급이 끝난 건의
경계는 정책 오너에게 물어 둔 자리다(`docs/research/brand/README.md` 「정책 오너에게 묻는다」 3).
표와 실제 청구 시스템이 어긋나면 표를 고치지 말고 그 질문으로 올린다.

| 쓰는 말 | 뜻(이 스킬의 읽기) | 쓰지 않는 말(예 · 이 스킬이 모은 것) |
|---|---|---|
| 접수 | 청구가 들어와 등록된 상태 | 접수완료, 신청, 등록, 청구중 |
| 심사중 | 사정·심사가 진행 중인 상태 | 처리중, 검토중, 진행중, 확인중 |
| 보완요청 | 서류·정보 보완을 요청한 상태 | 서류미비, 반려, 추가요청, 보류 |
| 지급완료 | 보험금 지급이 끝난 상태 | 완료, 처리완료, 입금완료, 정산완료 |
| 종결 | 지급 없이 절차가 끝난 상태 | 마감, 취소, 끝, 종료 |

상태를 나타내는 자리(화면 라벨 · 문자 · API 응답 문구 · spec 의 상태 목록)에서는 이 다섯 낱말을
그대로 쓴다. 다섯으로 표현되지 않는 상태가 필요하면 새 낱말을 만들지 말고 「정책 오너에게 묻는다」로
올린다(B4 는 어휘를 다섯으로 **고정**한다).

**B5 — 이름은 공식 표기 그대로**
회사명·상품명·기관명은 등록된 표기를 쓴다. 약칭(예: 「우리손보」)·영문 혼용(예: 「OO Life」)·
띄어쓰기 변형을 만들지 않는다. 공식 표기를 모르면 지어내지 말고 확인될 때까지
`‹공식 표기 확인 필요: 기관명›` 으로 두고 그 자리를 spec 의 Open questions 로 올린다.

**B6 — 날짜 · 금액 · 시각**

| 무엇 | 꼴 | 예 | 쓰지 않는 꼴 |
|---|---|---|---|
| 날짜 | `YYYY-MM-DD` | `2026-09-10` | 26.9.10, 2026년 9월 10일, 09/10/2026 |
| 금액 | 천 단위 구분 + 「원」 | `1,250,000원` | 125만원, ₩1250000, 1250000 KRW |
| 시각 | 24시간제 · KST 표기 | `14:30 (KST)` | 오후 2시 30분, 2:30 PM |

**B7 — 이모지 · 느낌표 없음, 이름 꼴**
이모지와 느낌표는 쓰지 않는다(강조는 문장 순서로 한다). 고객 호칭은 「○○○ 고객님」 꼴 —
성명 뒤에 「고객님」, 「님」·「씨」·「고객」 단독은 쓰지 않는다.
- 이렇게: `홍길동 고객님, 청구가 접수되었습니다.`
- 이렇게 쓰지 않는다: `홍길동님 🎉 청구 접수됐어요!`

## 쓰기 전 · 쓴 뒤에 하는 일
1. **자리를 확인한다** — 고객에게 보이는 문구인가. 아니면 이 스킬은 적용하지 않는다.
2. **문구를 쓴다** — 위 조항을 적용해서. 조항끼리 부딪히면 스스로 풀지 말고 5로 간다.
3. **기계로 훑는다** — 이 스킬 폴더의 `check-brand-copy.sh` 를 문구 파일에 돌린다.
   설치 위치에 따라 경로가 다르다: 레포에 넣었으면 `.claude/skills/brand/check-brand-copy.sh`,
   플러그인으로 받았으면 `${CLAUDE_PLUGIN_ROOT}/skills/brand/check-brand-copy.sh`.
   B1·B2·B3·B4·B6·B7 중 낱말·기호로 잡히는 것만 잡는다 — **없다고 통과가 아니다.**
   알려진 사각: 점 찍은 날짜(`26.9.10`)는 IP·버전 번호와 구분할 수 없어 보지 않고, 인용문 안의 위반과
   존댓말·한 문장 한 뜻·B5(공식 표기)는 아예 보지 않는다. 검사가 실패하면 rc=2 로 멈춘다(초록으로 위장하지 않는다).
   판정은 이 스킬과 사람이 한다. 실행 원문: `docs/research/brand/raw/15-checker-run-v2.txt`.
4. **리뷰 결과를 낼 때는 조항 번호로 적는다** — 한 줄에 하나:

   | 조항 | 문제가 된 문구 | 왜 | 이렇게 |
   |---|---|---|---|
   | B4 | "처리중입니다" | 상태 어휘 밖 | "심사중입니다" |

5. **판정할 수 없으면 올린다** — 정책이 답하지 않는 자리, 조항끼리 모순되는 자리는
   spec.md 의 「Flagged concerns」에 무엇이 부딪히는지와 누가 정하는지를 적고 멈춘다
   (`design-spec` 스킬: "Do not resolve a policy conflict yourself").

## 정책이 바뀌면
정본은 `bifrost17/intent-sdlc-skills` 레포의 `policies/brand.md` 다(이 스킬을 쓰는 레포에는
그 파일이 없을 수 있다 — 그때도 위 「정책 원문」 절의 전사본이 판정 기준이다). 정책이 바뀌면 **정책을 먼저 고치고**(오너 서명 = 개정 PR 머지),
그 다음 이 스킬의 「정책 원문」 절을 다시 전사한다. 스킬 레슨: "When the policy changes, change
the skill and have the policy owner sign off on the change." 이 스킬 파일에서 정책을 고치는 것은
정책 변경이 아니다 — 두 파일이 어긋난 것이다.

## 이 스킬이 하지 않는 것
- 정책을 만들거나 고치지 않는다. `policies/brand.md` 를 수정하지 않는다.
- 조항끼리의 모순을 스스로 풀지 않는다 — 「Flagged concerns」로 올린다.
- 문구를 막지 않는다(권고적 통제). 차단은 훅·CI 의 일이지 이 스킬의 일이 아니다.
- 보안·규제·UX 판정을 하지 않는다 — `secure-api-review`, `compliance`, `ux` 스킬의 자리다.
- 사내 문서·코드 주석·커밋 메시지의 문체를 정하지 않는다.
