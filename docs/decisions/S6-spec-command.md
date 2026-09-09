# S6 결정 — spec-command

**결정: 채택 없음 · 설계 1건(`skills/spec-policy-pass/`) + 명령 1건(`commands/spec-policy.md`).**
날짜 2026-09-10. 근거는 `docs/research/spec-command/{README,candidates,coverage,trigger-tests}.md`.

## 무엇을 물었나
기준선 `/spec`(= L3 282 축자 프롬프트 + 배선 두 줄) + `design-spec` 스킬이 프롬프트의 네 요구를
얼마나 하고 있고, 남의 것으로 더 잘할 수 있는가. 네 요구는 `coverage.md` 의 P1~P4 다.

## 무엇을 봤나
후보 30건을 열어 봤다(`candidates.md`) — 같은 플레이북을 구현한 동료 저장소 9, SDD 프레임워크 9,
PRD·우려 갈래 12. 채택 후보로 끝까지 검토한 것은 여섯: bibutikoley `spec`@fb225c3,
jsnkle `spec`@4d2bd9e, shawn-sandy `spec-from-intent`@8f6b84a, gaberger `hex-spec-design`@247a0a7,
그리고 Anthropic 이 배포한 `claude-for-legal` 의 `escalation-flagger`·`launch-review`@4a6c651.

## 왜 채택이 아닌가
1. **네 요구를 다 덮는 셋(bibutikoley · jsnkle · shawn-sandy)은 별 0개다.** 셋 다 이 플레이북이 공개된
   뒤 2주 안에 만들어진 동료 구현이라 「이미 있고 사람들이 쓰는」이라 부를 사용 신호가 없다. 게다가
   자기 저장소의 경로·명령·상태 규약(`sdlc/changes/_template/spec.md`·`/sdlc:spec`·`tracker-sync`)에
   묶여 있어 원문 유지 채택은 곧 깨진 참조가 된다.
2. **사용 신호가 큰 것들은 P2 를 어긴다.** spec-kit(별 134k) · OpenSpec(67.8k) · BMAD(52.8k) ·
   cc-sdd(3.7k) · Pimzino(3.9k) · ai-dev-tasks(7.8k)는 전부 요구와 설계를 다른 파일로 가르고 tasks
   까지 쓴다. 프롬프트의 "requirements and design spec … as spec.md" 와 정면으로 어긋난다.
3. **셋은 P4 를 능동적으로 위배한다.** `unlearndev/spec-generator` 는 "Resolve ambiguity with a
   sensible default. … Don't leave blanks.", `superpowers/brainstorming` 은 "pick one and make it
   explicit.", `pdlc-design` 의 자기검사는 `自动修复`(자동 수정)로 끝난다.
4. **가장 좋은 것(`escalation-flagger`, Apache-2.0, 별 9,413, Anthropic 배포)은 계약 법무용이다.**
   P4 가 요구하는 꼴의 정본이지만 본문이 법무 실무 설정 파일의 에스컬레이션 매트릭스를 읽고 트리거가
   "does this need GC sign-off" 같은 법무 발화다. 우리 저장소에 원문 그대로 넣으면 첫 단계에서 멈춘다.

그래서 **원문 채택 0건**, 대신 위 여섯의 문장을 근거로 직접 설계했다. 문장별 출처는
`skills/spec-policy-pass/PROVENANCE.md` 의 표에 있다(전부 MIT 또는 Apache-2.0).

## 기준선의 어디가 비었나 — 추정이 아니라 실측
기준선을 임시 프로젝트에서 한 번 돌려 재 봤다(`raw/20-BASE-01-*`). P2·P3 는 잘 됐다. 둘이 샜다.
- **P1**: `Skills applied:` 에 네 스킬이 적혔는데 그중 `secure-api-review` 는 SKILL.md 를 연 적이 없다
  (도구 호출 전량에 Read 없음, sha 를 얻는 `git log` 만 있음). 최종 응답은 "all opened before citing"
  이라고 말했다. 「열고 적어라」는 경고문이 `design-spec` 본문에 이미 있는데도 4개 중 1개가 샜다.
- **P4**: 조항이 없는 사안(외부 단축 URL)을 "C1/C2(최소 노출)의 정신과 배치될 수 있다"고 적어 **공백을
  충돌로** 만들었다. 같은 문서 다른 항목에서는 공백과 위반을 옳게 갈랐다 — 가를 줄 알면서도 조항 ID 를
  양쪽에 요구받지 않으니 갈리지 않았다.

## 무엇을 만들었나
- `skills/spec-policy-pass/SKILL.md` — 기준선을 대체하지 않고 겹친다. 정책 스킬 전량 열거(미적용에도
  이유) · **연 스킬만 인용**(sha 만 얻는 것은 적용이 아니다) · 우려를 표로, 종류를 **충돌/공백/미확인/추정**
  넷으로 가르고 충돌은 **양쪽 조항 ID**를 요구 · 결정자는 구체적으로 · 결정 칸은 비움 · 수치 제약은 세어 봄.
- `commands/spec-policy.md` — L3 282 축자 프롬프트를 **byte 동일**로 유지하고(기준선과 `diff` 0) 앞뒤로
  절차만 감쌌다. 이름은 스킬 폴더명과 다르게 두었다(NOTES.md 1 — 같으면 플러그인에서 합쳐진다).

## 시험 (`trigger-tests.md`, 실행 원문 `raw/21-run-*.txt`)
**트리거 4/4 + 집합 1/1.** 서로 다른 네 문구(한국어 셋·영어 하나)에서 매번 로드됐고, 명령과 두 스킬을
한 프로젝트에 함께 넣은 집합 시험에서 어긋난 지시가 없었다. 여기까지 트리거 문장을 두 번 고쳤다 —
v1 에서 1건(T1), v2 에서 1건(T4c)이 `design-spec` 만 골랐다. 실패와 무효까지 모두 적었다.

## 무엇이 나아졌나 (같은 과제, 같은 모델, 최종 5회)
- **P4**: 기준선이 틀렸던 항목(외부 단축 URL)을 **5/5 모두** 「공백 · 조항 없음」으로 옳게 갈랐다.
  「정신」으로 논증한 실행은 없었다. 충돌 행에는 양쪽 조항 ID 가 붙었고(예: "brand B4 · ux U2 ·
  compliance C5 · intent 의 「문자 90자 제한」"), 결정 칸은 5/5 비어 있었다.
- **수치 제약**: 5회 중 3회가 90자를 실제로 셌다("약 95자", "링크(85자)", "90byte≈한글 45자").
  기준선은 우려로 적기만 하고 세지 않았다.
- **P1**: 5회 중 4회가 인용한 정책의 본문을 모두 열었다. 기준선처럼 **내용을 못 본 채 이름만 적은
  실행은 없었다.**

## 남는 것 (정직하게)
1. **「연 스킬만 인용」이 0 이 되지 않았다.** 최종 회차의 T1d 는 스킬 본문 대신 저장소 뿌리의
   `policies/*.md` 를 열고 스킬 이름을 적었다. 내용은 같지만(시험 판에서 스킬은 정책의 축자 사본)
   연 것과 적은 것이 다르다. `policies/` 없는 판에서도 같은 일이 생기는지는 **확인 못 했다.**
2. **강제는 이 레인이 덮지 않는다.** 스킬은 권고적 통제이고(L6 "an advisory one"), 기준선 실측대로
   경고문은 넷 중 하나를 놓쳤다. 반드시 지켜져야 한다면 훅이나 리뷰 패스가 받쳐야 한다 —
   S7(pr-loop)·템플릿 `.claude/hooks/` 소관이다.
3. **템플릿의 실재하는 모순을 발견했다.** `capture-intent` 는 수락돼도 `Status: draft` 를 손대지 말라
   하고, `design-spec` 은 draft 면 멈추라 한다. 그래서 정상적으로 수락된 intent 가 영원히 draft 로
   보이고, 시험에서 두 실행이 이 때문에 과제를 시작조차 하지 않았다. 이 레인이 정할 일이 아니라
   정책 오너에게 넘겼다(README 4번). 정책 오너 질문은 모두 4건.
