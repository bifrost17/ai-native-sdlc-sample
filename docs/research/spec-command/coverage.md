# coverage — spec-command

행은 정책 조항이 아니라 **PO 프롬프트의 네 요구**다. S6 의 {POLICY} 는 「없음」이고, 이 레인이 덮어야 할
것은 `docs/work/baselines/spec.command.md` 가 나르는 L3 282 프롬프트의 네 요구이기 때문이다(S6 브리프
특별 지시). 조항 ID 대신 아래 P1~P4 를 고정 키로 쓴다.

| ID | 요구 (L3 282 축자에서) |
|---|---|
| **P1** | "Apply the skills available to you so the plan conforms to our brand guidelines, security policies and UX standards." — 조직 정책 스킬을 실제로 걸고, 어느 판을 걸었는지 남긴다(L3 279 "the skill versions in force"). |
| **P2** | "Document the spec fully as spec.md, ready to hand to the engineering team." — 요구와 설계가 한 파일에, 엔지니어링에 넘길 수 있는 꼴로. |
| **P3** | "Describe clearly any areas of concern" — 우려 지점을 제품 오너가 읽고 에스컬레이션할 수 있게 적는다. |
| **P4** | "especially where you cannot satisfy contradicting policies" — 지킬 수 없는 정책 모순을 명시하고, 스스로 해결하지 않는다. |

## 행렬

열은 **이 레인이 남기는 것**(설계분)과 **기준선**, 그리고 채택을 검토한 주요 후보다.
칸: 덮음 · 부분 · — (없음). 후보 전량과 판정 이유는 `candidates.md`.

| | 기준선 `/spec`+`design-spec` @016705e | **설계 `spec-policy-pass`** | bibutikoley `spec`@fb225c3 | jsnkle `spec`@4d2bd9e | shawn-sandy `spec-from-intent`@8f6b84a | gaberger `hex-spec-design`@247a0a7 | spec-kit @86b7a01 | claude-for-legal `escalation-flagger`@4a6c651 |
|---|---|---|---|---|---|---|---|---|
| **P1** | 부분 | **덮음** | 덮음 | 덮음 | 덮음 | 부분 | 부분 | 부분 |
| **P2** | 덮음 | 부분(기준선에 위임) | 덮음 | 덮음 | 덮음 | 부분 | 부분 | — |
| **P3** | 덮음 | 덮음 | 덮음 | 덮음 | 덮음 | 덮음 | 부분 | 덮음 |
| **P4** | 부분 | **덮음** | 덮음 | 덮음 | 덮음 | 부분 | 부분 | 덮음 |

기준선 P1·P4 를 「부분」으로 내린 근거는 추정이 아니라 실측이다 —
`raw/20-BASE-01-baseline-run.txt` 와 `raw/20-BASE-01-output-spec.md`:
- **P1 부분**: `Skills applied:` 에 네 스킬이 적혔으나 그중 `secure-api-review` 는 SKILL.md 를 연 적이
  없다(도구 호출 전량에 Read 없음, sha 를 얻는 `git log` 만 있음). 최종 응답은 "all opened before
  citing" 이라고 말했다. 「열고 적어라」는 경고문이 `design-spec` 본문에 이미 있는데도 4개 중 1개가 샜다.
- **P4 부분**: 우려 3건 중 1건에서 조항이 없는 사안(외부 단축 URL)을 "C1/C2(최소 노출)의 정신과 배치될
  수 있다"고 적어 **공백을 충돌로** 만들었다. 같은 문서 3번에서는 야간 발송을 두고 공백과 위반을 옳게
  갈랐다 — 가를 줄 알면서도 조항 ID 를 양쪽에 요구받지 않으니 갈리지 않았다.

## 겹침
- **P2·P3 는 기준선이 이미 덮는다.** `templates/spec.md` 의 일곱 절과 `Flagged concerns` 규칙이 그것이고,
  BASE-01 에서 실제로 다 채워졌다. 설계분은 이 둘을 다시 만들지 않고 기준선에 위임한다 —
  `spec-policy-pass` 본문 첫 문단이 "`design-spec` 을 대체하지 않는다"고 못박는 이유다.
- **P1 의 「전량 로드」는 네 후보가 모두 같은 말을 한다**(bibutikoley "Load every policy skill available",
  jsnkle "Load every policy skill available", shawn-sandy "Load every one that is available"). 설계분은
  여기에 「연 것만 인용」과 「미적용에도 이유」를 더해 검증 가능하게 만든 것이지 새 원칙을 만든 것이 아니다.
- **P4 의 「스스로 해결하지 않는다」는 세 후보와 기준선이 함께 말한다.** 설계분이 더한 것은 우려의 네 갈래와
  조항 ID 요구뿐이다.

## 모순
- **후보 vs 기준선 (P2)**: SDD 프레임워크 6종(spec-kit · cc-sdd · OpenSpec · BMAD · Pimzino ·
  ai-dev-tasks)은 전부 요구와 설계를 **다른 파일**로 가르고 tasks 까지 쓴다. 프롬프트의 "requirements
  and design spec … as spec.md" 와 정면으로 어긋나 채택할 수 없다. `pdlc-design@de13cf7` 은 PRD 가
  없으면 설계를 거부하는 하드 가드까지 둔다.
- **후보 vs P4 (능동적 위배)**: `unlearndev/spec-generator@cea103a` 는 "Resolve ambiguity with a
  sensible default. … Don't leave blanks." 와 "Never include an 'Out of Scope' section." 을 지시한다.
  `superpowers/brainstorming@b36e082` 는 "Could any requirement be interpreted two different ways?
  If so, pick one and make it explicit." 라고 한다. `pdlc-design@de13cf7` 의 자기검사는 `自动修复`
  (자동 수정)로 끝난다. 셋 다 P4 가 금지하는 「스스로 해결」을 명시적으로 지시한다 — 기각의 근거다.
- **설계분 내부 모순 없음(시험함)**: `spec-policy-pass` 와 기준선 `design-spec` 을 한 프로젝트에 함께
  넣고 같은 과제를 돌린 집합 시험 결과는 `trigger-tests.md` 의 SET 절.

## 빈칸과 이유
- **P2 가 설계분에서 「부분」인 것은 의도다.** 한 파일 산출·절 구성·수락 확인은 기준선 `design-spec` 과
  `templates/spec.md` 의 몫이고, 그것을 복제하면 두 개의 정본이 생긴다. 설계분은 P2 에 두 줄만 더한다
  (관찰 가능한 말로 쓸 것, 수치 제약은 세어 볼 것).
- **P1 의 「판 기록」 형식은 열린 채 남는다.** 기준선은 `name@sha`, bibutikoley 는
  `name@last-reviewed`(정책 오너가 비엔지니어일 때 더 현실적)를 쓴다. 어느 쪽을 조직 표준으로 삼을지는
  정책 오너의 결정이라 이 레인이 정하지 않았다 — `README.md` 「정책 오너에게 묻는다」 2번.
- **P1·P4 의 강제는 이 레인이 덮지 않는다.** 스킬은 권고적 통제다(L6 "A skill is a control, though an
  advisory one"). 「연 스킬만 인용」이 반드시 지켜져야 한다면 훅이나 리뷰 패스가 필요하고, 그것은 S7
  (pr-loop)·템플릿의 `.claude/hooks/` 소관이지 여기가 아니다. BASE-01 이 보여 준 대로, 경고문은
  4개 중 1개를 놓쳤다 — 스킬을 고쳐도 0 이 되리라는 보장은 없고, 시험으로 측정할 뿐이다.
- **정책 4종의 v0 상태는 이 레인이 풀 수 없다.** `policies/*.md` 는 모두 `Status: draft v0 — 오너 서명
  대기`다. 서명 전 조항을 spec 이 인용해도 되는지는 정책 결정이므로 「정책 오너에게 묻는다」 1번으로 넘겼다.
