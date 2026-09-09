# 커버리지 — intent-template (S1)

정책 파일이 없는 레인이다(`docs/work/S1-intent-template.md`). 행은 기준선 `capture-intent` 가 쓰는 **intent.md 다섯 절**을 쓴다. 조항 ID 는 이 문서 안에서만 쓰는 국소 ID(P/O/U/C/Q)이며 `policies/*.md` 의 ID 가 아니다.

열 = 이 레인이 내놓는 집합. 칸: **덮음** = 그 절을 직접 묻거나 쓴다 · **부분** = 그 절을 강화하지만 절 자체를 쓰지는 않는다 · **—** = 관여하지 않는다.

| 조항 | 절(템플릿 원문) | capture-intent (기준선·유지) | grilling (채택) | to-questionnaire (채택) |
|---|---|---|---|---|
| **P** | `## Problem` — ‹observed facts — counts, time, frequency. Not a cause, not a fix› | 덮음 | 부분 | — |
| **O** | `## Proposed outcome` — ‹what is different when this is done, in a sentence the author can verify› | 덮음 | 부분 | — |
| **U** | `## Affected users and systems` — ‹people (which team, which customers) and systems (which service, which data)› | 덮음 | 부분 | — |
| **C** | `## Constraints` — ‹lines that must hold — existing auth only, no new PII, what is out of scope› | 덮음 | 부분 | — |
| **Q** | `## Open questions` — ‹what nobody could answer yet, and who can — one per line› | 덮음 | 부분 | 부분 |

## 겹침

- **P·O·U·C 에서 `capture-intent` 와 `grilling`.** 둘 다 캐묻는다. 겹치지만 층이 다르다 — `capture-intent` 는 *무엇을 물어 어디에 적을지*(네 가지를 묻고 다섯 절에 originator 의 말로 적는다), `grilling` 은 *어떻게 파고들지*(선행 결정이 끝난 질문만 한 라운드로, 각 질문에 권고안을 달고, 사실은 서브에이전트가 찾고 결정은 사람이 한다). 실측으로도 자리가 갈렸다: 「intent 로 써 달라」 → `capture-intent`, 「grill / stress-test / interrogate 해 달라」 → `grilling`(`trigger-tests.md` §3).
- **Q 에서 `capture-intent` 와 `to-questionnaire`.** `capture-intent` 는 답 없는 질문을 *답할 사람 이름과 함께 남기고* 끝난다. `to-questionnaire` 는 그 다음 동작 — 그 사람에게 보낼 문서를 만든다. 같은 절을 두 번 쓰지 않는다: 산출 파일이 다르다(`intent/<NNNN>-<slug>/intent.md` vs `to-questionnaire-<slug>.md`).

## 모순

- **없음.** 세 스킬을 한 프로젝트에 함께 넣고 같은 과제를 시킨 집합 시험에서 지시가 어긋난 곳은 없었다(`raw/53-set-idea.txt`: `capture-intent` 가 로드되고 그 규칙대로 질문). 구조적으로도 `to-questionnaire` 는 `disable-model-invocation: true` 라 모델이 스스로 부를 수 없어 intent 를 쓰는 자리를 뺏지 못한다(`raw/52-tq-natural.txt` 로 확인).
- 채택하지 않은 후보 중에는 모순이 있다. superpowers `brainstorming` 은 "You MUST use this before any creative work" 로 모든 창작 앞을 막고 산출을 design doc 으로 몰아가며, 승인을 대화 중 승인으로 본다 — 기준선의 「해법을 쓰지 않는다」·「승인은 머지다」와 충돌한다. 함께 넣어 본 실측에서는 intent 문구에서 `capture-intent` 가 이겼지만(`raw/60-bs-collision.txt`), 이는 충돌이 없다는 뜻이 아니라 이 문구에서 드러나지 않았다는 뜻이다 — 그래서 기각했다.

## 빈칸과 이유

행렬에 **덮이지 않은 절은 없다**. 기준선이 다섯 절을 모두 쓴다. 대신 「덮이지만 얇은」 자리와, 이 레인이 메우지 *않기로* 한 자리를 적는다.

| 자리 | 상태 | 왜 이 레인이 메우지 않았나 |
|---|---|---|
| 묻는 항목과 쓰는 절이 1:1 이 아니다 — 기준선은 **Scope · Users · Constraints · Success** 넷을 묻는데 템플릿 절은 **Problem · Proposed outcome · Users+Systems · Constraints · Open questions** 다섯이다. `Problem`(관측된 사실)과 `Open questions` 는 묻는 목록에 없다 | 부분 | 이 어긋남을 없애려면 기준선 SKILL.md 의 "What to ask" 를 고쳐야 한다. 템플릿 변경은 **정책 오너/리드 서명 사항**(L2 202, ADOPTING 「a lead signs off」)이라 조사 레인이 손대지 않는다 → README Q1 |
| `to-questionnaire` 의 산출이 현재 디렉터리에 떨어진다(`to-questionnaire-<slug>.md`) — intent 폴더 규약 밖 | 부분 | 원문을 고치면 「채택분은 원문 유지」 규칙을 깨고 상류 갱신을 따라가기 어려워진다. 경로 한 줄은 오너가 정할 문제 → README Q3 |
| 비엔지니어 유입 경로(claude.ai/Cowork 커넥터로 `intent/` 에 커밋) | 없음 | 스킬로 풀 수 있는 문제가 아니다. 템플릿 `docs/ADOPTING.md` 가 「no file — non-engineer contributor's commit path」로 이미 플랫폼 엔지니어의 몫이라고 못박아 두었다 |
| 선행지표(첫 대화 → 커밋까지의 시간) 자동 측정 | 부분 | 기준선이 PR 본문 첫 줄에 첫 대화 시각(ISO, UTC)을 적게 해 *기록*은 남는다. 그 값을 모아 재는 것은 스킬이 아니라 계측의 몫(L14) |
| 여러 체인이 동시에 시작될 때의 `<NNNN>` 충돌 | 부분 | 기준선이 「동시 시작을 지시한 사람이 번호를 배정하고 PR 본문에 적는다」로 사람에게 넘겼다. 스킬이 강제할 수 없는 조정 문제 → README Q2 |
