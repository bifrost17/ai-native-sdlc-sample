# spec-command — 조사 요약

**과제**(S6 브리프): 기준선 `/spec` — L3 282 축자 PO 프롬프트 + 배선 두 줄 — 이 나르는 **네 요구**를
남의 스킬·명령이 더 잘하는지 보고, 남으면 설계한다. 네 요구는 `coverage.md` 의 P1~P4:
정책 스킬 적용 · spec.md 산출 · 우려 지점 기술 · 모순되는 정책 명시.

조사 시각(UTC): 발굴 2026-09-09T09:35Z~09:41Z(1회차, 세션 한도로 중단) · 정독 2026-09-10T07:19Z~07:26Z ·
실측 2026-09-09T22:20Z~23:27Z. 별 수·갱신일은 정독 시각의 값이다.

## 결론

**채택 0건 · 설계 2건.** 후보 30건을 열어 봤고(`candidates.md`), 원문 유지로 채택할 것은 없었다.

- `skills/spec-policy-pass/` — 설계. 기준선 `design-spec` 을 **대체하지 않고 겹친다**. 정책 스킬 전량
  열거(미적용에도 이유) · **연 스킬만 인용**(sha 만 얻는 것은 적용이 아니다) · 우려를 표로 쓰고 종류를
  **충돌 / 공백 / 미확인 / 추정** 넷으로 가르며 충돌은 **양쪽 조항 ID**를 요구 · 결정자는 구체적으로 ·
  결정 칸은 비움 · 수치 제약은 세어 봄.
- `commands/spec-policy.md` — 설계. L3 282 축자 프롬프트를 **byte 동일**로 유지하고(기준선과 `diff` 0,
  `raw/02-baseline-vs-template-diff.txt`) 앞뒤로 절차만 감쌌다. 스킬 폴더명과 파일명을 다르게 두었다
  (NOTES.md 1 — 같으면 플러그인에서 한 이름으로 합쳐진다).

### 왜 채택이 아닌가
1. **네 요구를 다 덮는 셋은 별 0개다.** bibutikoley `spec`@fb225c3 · jsnkle `spec`@4d2bd9e ·
   shawn-sandy `spec-from-intent`@8f6b84a — 셋 다 이 플레이북 공개 뒤 2주 안에 만들어진 동료 구현이라
   「이미 있고 사람들이 쓰는」이라 부를 사용 신호가 없다. 게다가 자기 저장소의 경로·명령·상태 규약
   (`sdlc/changes/_template/spec.md` · `/sdlc:spec` · `tracker-sync`)에 묶여 원문 채택은 곧 깨진 참조가 된다.
2. **사용 신호가 큰 것들은 P2 를 어긴다.** spec-kit(134k★) · OpenSpec(67.8k★) · BMAD(52.8k★) ·
   ai-dev-tasks(7.8k★) · Pimzino(3.9k★) · cc-sdd(3.7k★)는 전부 요구와 설계를 **다른 파일**로 가르고
   tasks 까지 쓴다. "requirements and design spec … as spec.md" 와 정면으로 어긋난다.
3. **셋은 P4 를 능동적으로 위배한다.** `unlearndev/spec-generator` 는 "Resolve ambiguity with a sensible
   default. … Don't leave blanks.", `superpowers/brainstorming` 은 "pick one and make it explicit.",
   `pdlc-design` 의 자기검사는 `自动修复`(자동 수정)로 끝난다.
4. **가장 좋은 것은 계약 법무용이다.** Anthropic 이 배포한 `claude-for-legal` 의
   `escalation-flagger`@4a6c651(Apache-2.0, 9,413★)은 P4 가 요구하는 꼴의 정본이지만, 본문이 법무 실무
   설정 파일의 에스컬레이션 매트릭스를 읽고 트리거가 "does this need GC sign-off" 같은 법무 발화다.
   우리 저장소에 원문 그대로 넣으면 첫 단계에서 멈추고 spec 과제에는 트리거되지 않는다.

문장은 빌려 왔다 — 출처는 `skills/spec-policy-pass/PROVENANCE.md` 의 표(전부 MIT 또는 Apache-2.0).

### 기준선의 어디가 비었나 — 추정이 아니라 실측
기준선을 임시 프로젝트에서 돌려 쟀다(`raw/20-BASE-01-*`). P2·P3 는 잘 됐다. 둘이 샜다.
- **P1**: `Skills applied:` 에 네 스킬이 적혔는데 `secure-api-review` 는 SKILL.md 를 연 적이 없다
  (Read 없음, sha 를 얻는 `git log` 만). 최종 응답은 "all opened before citing" 이라고 말했다.
  「열고 적어라」는 경고문이 `design-spec` 본문에 이미 있는데도 넷 중 하나가 샜다.
- **P4**: 조항이 없는 사안(외부 단축 URL)을 "C1/C2 의 **정신**과 배치될 수 있다"고 적어 공백을 충돌로
  만들었다. 같은 문서 다른 항목에서는 옳게 갈랐다.

### 트리거 시험
**트리거 4/4 · 집합 1/1 · 배포 경로 1/1**(`trigger-tests.md`). 서로 다른 네 문구(한국어 셋·영어 하나)에서 매번 로드됐고,
명령·두 스킬을 함께 넣은 집합 시험에서 어긋난 지시가 나타나지 않았다. 여기까지 트리거 문장을 두 번
고쳤다(v1 에서 1건, v2 에서 1건 실패 → v3). 실패와 무효까지 모두 같은 파일에 적었다.

실제 배포 경로(플러그인)로도 따로 쟀다 — 산출물을 프로젝트에서 빼고 `--plugin-dir` 로만 얹었을 때
`intent-sdlc-skills:spec-policy-pass` 로 로드돼 끝까지 갔고, 그 세션에 함께 올라온 다른 레인 스킬 7종과
어긋난 지시가 없었다.

산출물 품질도 같이 쟀다: 기준선이 틀렸던 항목(외부 단축 URL)을 4회차 5회 **5/5 모두** 「공백 · 조항 없음」
으로 옳게 갈랐고, 충돌 행에는 양쪽 조항 ID 가 붙었으며, 결정 칸은 5/5 비어 있었다. 90자 제약을 실제로
센 실행이 3회다.

## 남는 구멍
1. **강제는 덮지 않는다.** 스킬은 권고적 통제다(L6 "a control, though an advisory one"). 실측이 보여 준
   대로 경고문은 넷 중 하나를 놓쳤다. 「연 스킬만 인용」이 반드시 지켜져야 한다면 훅이나 리뷰 패스가
   뒤를 받쳐야 하고, 그것은 S7(pr-loop)·템플릿 `.claude/hooks/` 소관이다.
2. **「연 스킬만 인용」이 0 이 되지 않았다.** 최종 4회차에서도 T1d 는 스킬 본문 대신 저장소 뿌리의
   `policies/*.md` 를 열고 스킬 이름을 적었다. 이 시험 판에 `policies/` 가 함께 있어서 열린 길이며,
   실제 배포 프로젝트에는 `.claude/skills/` 만 간다 — **`policies/` 가 없는 판에서도 같은 일이 생기는지는
   돌려 보지 않았다(확인 못 함).**
3. **판 기록 형식이 열려 있다.** 기준선은 `name@sha`, bibutikoley 는 `name@last-reviewed`. 어느 쪽을
   조직 표준으로 삼을지는 정책 오너의 결정이라 이 레인이 정하지 않았다(아래 2번).
4. **`templates/spec.md` 는 손대지 않았다.** `awesome-copilot/create-specification` 의 안정 ID 체계
   (`REQ-`/`SEC-`/`CON-`/`AC-`)는 우리 템플릿에 없는 장점이지만, 템플릿은 이 레인의 파일이 아니다(아래 3번).
5. **코드 검색 커버리지가 부분적이다.** 1회차 `gh search code` 가 대부분 HTTP 403(rate limit)으로
   실패했다(`raw/05`·`06`·`09` 의 `RC: 1`). `.claude/commands/` 아래에만 있는 소규모 spec 명령 중 못 본
   것이 있을 수 있다 — **확인 못 함**.
6. **정독하지 않은 것**: `claude-for-legal` 의 `feature-risk-assessment`·`gap-surfacer` 는 존재만 확인하고
   사본을 남겼다 — **확인 못 함**.

## 정책 오너에게 묻는다
1. **정책 4종이 모두 `Status: draft v0 — 오너 서명 대기`다.** 서명 전 조항(B1·C4·U2·S5 …)을 spec 이
   확정 제약으로 인용해도 되는가, 아니면 spec 의 우려 표에 「미서명」으로 함께 적어야 하는가.
   이 레인은 정하지 않고 조항 ID 를 그대로 인용하게 두었다.
2. **적용한 정책의 판을 무엇으로 적을 것인가.** `name@sha`(기준선, git 커밋)인가
   `name@last-reviewed`(정책 파일 머리의 검토일, 비엔지니어 오너에게 더 현실적)인가. 둘 다 L3 279 의
   "the skill versions in force" 를 만족하지만 감사 대상이 다르다.
3. **`templates/spec.md` 에 요구 ID 를 넣을 것인가.** 지금은 절만 있고 번호가 없어 다른 문서가 특정
   요구를 인용할 수 없다. 넣는다면 템플릿 소유자(템플릿 저장소)의 결정이다.
4. **수락된 intent 가 본문에 영원히 `Status: draft` 로 남는 문제.** `capture-intent` 는 "Approval is
   the merge" 라 손대지 말라 하고, `design-spec` 은 "must be accepted — merged to main. If it is still
   a draft … stop" 이라 한다. 시험에서 두 실행이 이 때문에 과제를 시작조차 하지 않았다
   (`trigger-tests.md` 2절). 둘 중 하나가 바뀌어야 한다 — 어느 쪽인가는 이 레인이 정할 일이 아니다.

## 파일
| 파일 | 무엇 |
|---|---|
| `candidates.md` | 후보 30건 — 출처·판·라이선스·사용 신호·트리거 문장·덮는 조항·판정과 이유 |
| `coverage.md` | P1~P4 × 스킬 행렬, 겹침·모순·빈칸 |
| `trigger-tests.md` | 실행 16회(기준선 1 + 트리거 14 + 집합 1), 실패·무효·고침 이력 포함 |
| `raw/` | 사본(sha)·명령 출력 원문·시험 실행 원문·산출 spec |
| `../../decisions/S6-spec-command.md` | 결정 1쪽 |
| `../../../skills/spec-policy-pass/` | 설계 스킬 + PROVENANCE |
| `../../../commands/spec-policy.md` | 설계 명령(축자 프롬프트 유지) |
