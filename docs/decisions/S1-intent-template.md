# 결정 — S1 · intent-template

- **날짜(UTC)**: 2026-09-10
- **레인**: `lane/S1-intent-template` · 조사: [`docs/research/intent-template/`](../research/intent-template/README.md)
- **정책 파일**: 없음. 기준선은 `docs/work/baselines/capture-intent.SKILL.md`

## 결정

1. **`capture-intent` 를 유지한다.** 고치지 않고, 이 레포에 사본도 두지 않는다(정본은 템플릿 레포 `.claude/skills/capture-intent/SKILL.md`).
2. **`to-questionnaire` 와 `grilling` 을 원문 그대로 채택해 곁에 둔다** — `skills/to-questionnaire/`, `skills/grilling/`.
3. **직접 설계한 스킬은 없다.**

## 왜

**대체 후보가 없어서.** 40여 후보를 봤고 그중 20여 개를 정독했다([`candidates.md`](../research/intent-template/candidates.md)). 이 부류는 거의 전부 PRD/spec 생성기여서, 기준선이 금지한 것(해법·기술 선택·user story·acceptance criteria)을 정확히 생산한다. 다섯 절을 그 이름대로 쓰는 스킬도, 「승인 = PR 머지」를 규칙으로 적은 스킬도 **없었다**(`candidates.md` §4). 가장 가까웠던 둘도 기각했다 — `speckit.assess.define` 은 `.specify/` 파이프라인과 `problem.md` 산출을 요구하고, `ideate` 는 14절 spec 을 내는 OpenCode 배포물이다.

**보완 후보가 있어서.** 기준선이 *말은 하되 수단을 주지 않은* 두 자리에만 들어가는 것을 골랐다([`coverage.md`](../research/intent-template/coverage.md)):

- `to-questionnaire` → **Q**. 기준선의 "do not invent an answer … with the name of who can" 다음 동작. 주제가 아니라 *보내는 일*만 인터뷰한다(누구에게 · 무엇을 돌려받아야 하나).
- `grilling` → **P·O·U·C**. 기준선의 "dig where answers are thin" 의 방법. design tree 의 frontier 를 한 라운드씩 소진하고, 사실은 서브에이전트가 찾고 결정은 사람이 한다.

**실측으로 자리가 갈려서.** 트리거 9/9, 집합 충돌 4/4 통과([`trigger-tests.md`](../research/intent-template/trigger-tests.md)). 「intent 로 써 달라」 → `capture-intent`(집합 상태에서도), 「grill/stress-test/interrogate」 → `grilling`, 질문지는 `disable-model-invocation` 때문에 사람이 슬래시로만. superpowers `brainstorming` 을 같이 넣은 충돌 시험에서도 `capture-intent` 가 이겼다.

**라이선스가 깨끗해서.** 둘 다 `mattpocock/skills` MIT(원문 사본 `raw/70-source-paths-and-license.txt`), Anthropic 공식 플러그인 마켓플레이스가 같은 sha 로 고정 배포한다(`raw/12-official-marketplace-entries.txt`). GPL-2.0(`digoal/blog`)·AGPL-3.0(`ainalyst`)·라이선스 불명(richtabor·pmYangKun·Nate's·PM Copilot·loki-mode·use-case-writer·problem-solver) 후보는 규칙대로 배제했다.

## 하지 않은 것

- **템플릿 다섯 절을 고치지 않았다.** 묻는 넷과 쓰는 다섯이 1:1 이 아닌 것을 발견했지만(README 「남는 구멍」1), intent 템플릿 변경은 리드 서명 사항(L2 202)이라 조사 레인이 결정하지 않는다.
- **채택분 원문을 고치지 않았다.** `to-questionnaire` 의 산출 경로가 `intent/` 규약 밖이지만 원문 유지 규칙을 지켰다 — 경로는 오너 질문 3으로 남겼다.
- **`policies/*.md` 와 다른 세션의 폴더를 건드리지 않았다.** `docs/research/README.md` 의 색인 행도 8개 레인이 공유하는 파일이라 손대지 않았다(부모 세션이 묶는다).

## 오너에게 넘긴 질문

다섯 건. [`README.md` 「정책 오너에게 묻는다」](../research/intent-template/README.md#정책-오너에게-묻는다) — 요지는 (1) 묻는 넷 ↔ 쓰는 다섯 정렬, (2) 동시 체인 번호 배정, (3) 질문지 산출물의 자리, (4) `grilling` 의 모델 자동 호출 허용 여부, (5) `Cost of Inaction`·`Non-Goals` 를 다섯 절에 들일지.

## 확인 못 한 것

- `to-questionnaire` 가 `to-questionnaire-<slug>.md` 를 실제로 쓰는 것(헤드리스라 1단계 질문에서 멈춤).
- 슬래시 확장의 직접 도구 호출 증거(스트림에 남지 않는다 — 행동 증거로 판정).
- `candidates.md` §3 의 후보들은 정독하지 않았다(프런트매터 + 절 키워드까지만 확인).
