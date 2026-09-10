# S2 — brand 스킬: `stop-slop-ko` 채택 + `brand` 설계

결정일 2026-09-10 · 세션 S2 · 브랜치 `lane/S2-brand` · 정책 `policies/brand.md`(v0 draft, 오너 서명 대기).
근거 문서: `docs/research/brand/README.md` · `candidates.md` · `coverage.md` · `trigger-tests.md`.

## 결정
1. **`skills/brand/` 를 직접 설계한다** — 정책 B1~B7 을 전사하고, 조항마다 적용법·위반 예·표를 붙이고,
   낱말로 잡히는 것만 훑는 `check-brand-copy.sh` 를 딸려 보낸다.
2. **`skills/stop-slop-ko/` 를 원문 그대로 채택한다** — limleesol/stop-slop-ko `43313c9`, MIT.
   B1 보강. 수정 0건.
3. **나머지 30건은 채택하지 않는다** — 기각 27 · 보류 3(`candidates.md` 의 판정 열을 세면
   채택 1 + 기각 27 + 보류 3 = 열어 본 31건).

## 왜
- **찾는 것을 먼저 했다.** 8갈래로 86건을 찾고 31건을 열었다(`candidates.md`). 그런데 **B4(청구 상태
  다섯 어휘)와 B7(「○○○ 고객님」·이모지/느낌표)을 덮는 공개 스킬이 없었다.** 공개 스킬은 값이 빈 영어 틀이거나
  (`rampstack-brand-voice`, `0xelite-brand-voice`, `kwp-brand-review`), 우리 값과 정면으로 어긋나는 값을
  갖고 있었다(`Month DD, YYYY`, 느낌표 1개 허용, 「과도한 격식 금지」).
- **좋은 점은 가져왔다.** 대비 예시 꼴(cookbooks) · 리뷰 표 꼴(kwp-brand-review) · 오류 문구 3토막
  (uxwriting) · 근거 조항 인용 절차(korean-report-style) · 상태 낱말 승격 금지(localize-naturally).
  한 줄씩 `skills/brand/PROVENANCE.md` 「참고한 것」에 출처와 함께 적었다.
- **`stop-slop-ko` 만 채택한 이유**: 정책이 못박은 「최고의 · 완벽한」을 축자로 지목하는 유일한 후보이고
  (148행), 원문 레지스터를 보존해 존댓말을 깨지 않으며(102행), 정책과 모순이 없고, MIT 이며,
  런타임에 무엇을 받아오지 않는다.
- **`kwp-brand-review`(Apache-2.0, ★23,943)를 기각한 이유**: 시험에서 **우리 자리에 로드되지 않았다**.
  상태 배지·고객 문자 리뷰 2회 0/2, 마케팅 블로그 감사에서만 1회(`trigger-tests.md` S1·S2·S4).
  정책 대상 밖이고, 로드되지 않는 통제는 통제가 아니다.
- **`kskill-korean-humanizer`(★7,483)를 기각한 이유**: `npx -y @nomadamas/k-skill@0 …` 의 출력을
  본 지시로 삼는 스텁이다. `@0` 은 major 범위라 sha 를 박아도 실행 규칙이 고정되지 않는다.
  spec 에 「적용된 스킬 판」을 적어야 하는 우리 규칙(L3 279)과 양립하지 않는다.
- **`composio-qa-response` 를 보류한 이유**: 레포에 LICENSE 파일이 없고 README 가 스스로 Apache-2.0(배지)과
  MIT(본문)로 어긋난다. COMMON 「불명이면 보류」. 같은 레포의 `tone-rewriter`·`response-templates` 는
  라이선스와 무관하게 내용이 B1 과 반대(반말·느낌표 예시, 「과도한 격식 금지」)라 기각했다.

## 무엇을 바꿨나 (시험이 바꾼 것)
- 트리거 문장 1회 개정: 「우리 조직 스킬을 적용해서」 문구에 모델이 스킬 대신 파일을 뒤졌다(S8 이 본 것과 같은 꼴).
  description 에 「`.claude/skills` 를 뒤지지 말라」를 넣어 같은 문구로 재시험 통과.
- 체커 B4 정규식: 단독 `완료` 미탐을 집합 시험 S1 이 짚었다 → `(^|[^급])완료`·`종료`·`마감` 추가,
  `지급완료`·`종결` 오탐 없음 재확인.
- 스킬 안 경로 2곳: 배포 위치(`.claude/skills/…` · `${CLAUDE_PLUGIN_ROOT}/…`)와 정본 레포 이름을 밝히도록 고쳤다.

## 결정하지 않은 것 (정책 오너에게)
공식 표기 목록(B5) · 「근거 조항」의 범위(B2) · 다섯 어휘와 시스템 상태값의 대응(B4) · 마케팅 문구가
대상인지(B1·B7) · KST 표기 꼴(B6) · 성명 없는 고객의 호칭(B7). 여섯 건 전부
`docs/research/brand/README.md` 「정책 오너에게 묻는다」에 적었다. **정책 파일은 고치지 않았다.**

## 상태
정책이 `draft v0`(오너 서명 대기)이므로 이 스킬도 같은 상태다. 서명 = 개정 PR 머지.
정책이 바뀌면 정책을 먼저 고치고 `skills/brand/SKILL.md` 의 「정책 원문」 절을 다시 전사한다.
