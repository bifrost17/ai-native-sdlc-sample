# intent-template (S1) — 요약

**조사 시각(UTC): 2026-09-09T09:32Z ~ 2026-09-10T05:30Z.** 모든 수치(별·forks·갱신일)는 그 시각의 값이다.

## 결론

**기준선 `capture-intent` 는 유지한다. 대체 후보는 없었다. 그 옆에 두 개를 곁들인다.**

| | 이름 | 무엇을 메우나 | 출처·판·라이선스 |
|---|---|---|---|
| 유지 | `capture-intent` | 다섯 절 전부 | 템플릿 `bifrost17/intent-sdlc-sample@016705e`, MIT — **한 글자도 고치지 않는다** |
| 채택 | `to-questionnaire` | **Q**: 답할 사람에게 실제로 묻는 수단 | `mattpocock/skills@3cca18b`, MIT |
| 채택 | `grilling` | **P·O·U·C**: 「답이 얇은 곳을 판다」의 *방법* | `mattpocock/skills@3cca18b`, MIT |

- **직접 설계: 없음.** 다섯 절 중 덮이지 않은 절이 없어 새로 쓸 이유가 없었다(`coverage.md`).
- **기각: 40여 후보.** 표와 이유는 `candidates.md`. 가장 아까운 둘은 `github/spec-kit` 의 `speckit.assess.define`(다섯 절 중 넷을 가장 가깝게 덮지만 `.specify/` 파이프라인과 `problem.md` 산출을 요구)과 `ideate`(다섯 절을 다 덮지만 14절짜리 spec 을 내고 OpenCode 배포물이다).
- **트리거: 9/9 통과** + 집합 충돌 시험 4건 통과(`trigger-tests.md`).

### 왜 대체가 아니라 병렬인가

마켓의 이 부류는 거의 전부 **PRD/spec 생성기**다. user story·acceptance criteria·기술 고려사항·우선순위를 만든다 — 기준선이 명시적으로 금지한 것들이다("Does not propose solutions … does not write spec.md or plan.md"). 다섯 절을 그 이름대로 쓰는 스킬도, 「승인은 PR 머지이고 별도 승인 파일은 없다」를 규칙으로 적은 스킬도 없었다(`candidates.md` §4). 그래서 기준선을 바꿀 근거가 없다.

두 채택분은 기준선이 **말은 하되 수단을 주지 않은 두 자리**에만 들어간다:

- 기준선: "An open question you cannot answer stays in Open questions with the name of who can — do not invent an answer." → 그 사람에게 보낼 문서를 만드는 수단이 없다. → `to-questionnaire`.
- 기준선: "Four things, then **dig where answers are thin**" → 어떻게 파는지가 없다. → `grilling`(design tree · frontier · 라운드).

`to-questionnaire` 는 `disable-model-invocation: true` 라 사람이 `/to-questionnaire` 로만 부른다 — 구조적으로 intent 를 쓰는 자리를 뺏을 수 없다. `grilling` 은 모델이 부를 수 있으나, 실측에서 「intent 로 써 달라」에는 기준선이, 「grill/stress-test/interrogate」에는 grilling 이 떴다.

## 남는 구멍

1. **묻는 항목과 쓰는 절이 1:1 이 아니다.** 기준선은 Scope·Users·Constraints·Success 넷을 묻는데 템플릿 절은 다섯이고, `Problem`(관측된 사실)과 `Open questions` 는 묻는 목록에 없다. 실측에서 모델은 두 절을 알아서 물었지만(`raw/40`), 그것은 본문의 다른 문단(관측 사실·지어내지 말라)이 받쳐 준 결과다.
2. **`to-questionnaire` 의 산출 경로**가 현재 디렉터리(`to-questionnaire-<slug>.md`)라 `intent/<NNNN>-<slug>/` 규약 밖이다.
3. **`to-questionnaire` 가 파일을 쓰는 것까지는 확인 못 했다** — 헤드리스라 1단계 질문에서 멈췄다(`trigger-tests.md` §5).
4. **동시 시작 `<NNNN>` 충돌**은 스킬이 아니라 사람의 조정에 맡겨져 있다(기준선 본문에 그렇게 적혀 있다).
5. **비엔지니어 유입 경로**(claude.ai/Cowork → `intent/` 커밋)는 스킬의 문제가 아니다. 템플릿 `docs/ADOPTING.md` 가 플랫폼 엔지니어의 몫으로 이미 못박아 두었다.

## 정책 오너에게 묻는다

이 레인은 정책 파일이 없고(`{POLICY} = 없음`) intent 템플릿은 **리드 서명 사항**이다(L2 202 "encoded as a skill … signed off by a lead", ADOPTING "a technical team member writes it, a lead signs off"). 아래는 결정하지 않고 남긴다.

1. **묻는 넷 ↔ 쓰는 다섯의 어긋남을 맞출 것인가?** 기준선 "What to ask" 를 `Problem`(관측된 사실)·`Open questions` 를 포함한 다섯으로 고칠지, 지금처럼 본문이 받치게 둘지. **템플릿 변경이라 오너 서명이 필요하다 — 이 레인은 손대지 않았다.**
2. **동시 체인의 번호 배정**을 사람의 조정에 계속 맡길 것인가, `intent/` 에 번호 예약 규약을 둘 것인가?
3. **`to-questionnaire` 산출물의 자리.** `intent/<NNNN>-<slug>/` 안에 둘 것인가, PR 에 첨부할 것인가, 아니면 지금처럼 세션 작업 디렉터리에 둘 것인가? 지금 답은 「원문을 고치지 않으므로 현재 디렉터리」다.
4. **`grilling` 을 모델이 스스로 부르게 둘 것인가?** 지금은 그렇다. 「사람이 요청할 때만」으로 좁히려면 `disable-model-invocation: true` 를 더해야 하는데, 그것은 원문 수정이라 PROVENANCE 에 기록될 변경이 된다.
5. **spec-kit `assess.define` 의 두 항목**(`## Cost of Inaction`, `## Non-Goals`)을 다섯 절에 들일 것인가? 기각한 후보 중 유일하게 다섯 절과 같은 층에서 값을 더하는 항목이었다. **템플릿 변경이라 역시 오너 서명 사항.**

## 파일

| 파일 | 무엇 |
|---|---|
| `candidates.md` | 본 후보 전부 — 출처·판·라이선스·사용 신호·트리거 문장·덮는 절·판정과 이유 |
| `coverage.md` | 다섯 절 × 스킬 행렬, 겹침·모순·빈칸 |
| `trigger-tests.md` | 문구별 결과(9건) + 집합 충돌 시험(4건) + 확인 못 한 것 |
| `raw/` | 레슨·템플릿 사본, 후보 SKILL.md 사본(`<name>@<sha>.SKILL.md`), 검색·메타 출력, 트리거 시험 원문(`.jsonl`/`.txt`), 실행기 `run-trigger.sh` |
| `../../decisions/S1-intent-template.md` | 결정 1쪽 |
| `../../../skills/to-questionnaire/`, `../../../skills/grilling/` | 채택분 SKILL.md(원문 그대로) + PROVENANCE.md |
