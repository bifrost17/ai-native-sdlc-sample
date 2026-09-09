# 트리거 시험 — secure-api-review(기준선) · claims-api-security(설계)

## 방법
- 임시 프로젝트 `/tmp/s5-trig-<n>`(각 시험마다 독립 사본): Flask 청구 상태 서비스 한 파일(`src/claims.py`, 고객 세션을 읽고 claims-core 를 부르는 `GET /claims/<id>` + `/health`), 짧은 `CLAUDE.md`, accepted 상태의 `intent/0001-claim-history/intent.md`. 스킬은 `.claude/skills/<name>/SKILL.md` 로 복사(바이트 동일).
- 헤드리스: `claude -p '<문구>' --output-format stream-json --verbose --max-turns 8 --permission-mode acceptEdits --allowedTools Read,Glob,Grep,Edit,Write,Skill,Bash(ls*),Bash(cat*) < /dev/null` (러너 `raw/50-trigger-runner.sh`). 판정 = assistant 메시지의 `tool_use` 중 `Skill {"skill": "<name>"}` 가 있는가. 원문(스트림 전체)은 `raw/5N-trigger-*.txt` / `raw/6N-trigger-*.txt`.
- Claude Code 2.1.265. 실행자 계정의 전역 스킬(예: `claude-api`)도 샌드박스에 보이므로 무관한 도구 호출(예: 다른 LLM 공급자 grep)이 섞여 있다 — 판정에는 쓰지 않았다.
- 시각: 51–55 는 2026-09-09T09:38Z 전후, 56–61 은 13:07Z 전후, 62–68 은 22:07Z~22:09Z(모두 UTC). 이 기계의 지역시는 UTC+9 라 로컬 날짜는 하루 앞선다 — 표의 값은 UTC 다.

## 집합 시험 — 두 스킬을 함께 넣고 (판정: 둘 다 로드되는가 · 지시가 어긋나는가)

| # | 문구 | secure-api-review | claims-api-security | 결과 · 비고 | raw |
|---|---|---|---|---|---|
| 51 | Add a GET /claims/{id}/history endpoint … for the customer's own claim. | 로드 | 로드 | 코드·spec 작성 후 최종 요약이 「session limit」 메시지로 끊김(실행자 계정 한도). 로드 판정은 유효 | 51 |
| 52 | intent/0001-… 를 읽고 spec.md 초안을 써 줘. 우리 정책 스킬을 적용해서. (한국어·spec 과제) | 로드 | 로드 | spec.md 작성; 최종 요약은 한도로 끊김 | 52 |
| 53 | Review src/claims.py for security problems before I open the PR. Don't change code, just report. | 로드 | 로드 | 보고서에 S1–S4 항목별 + S5–S8 항목별 점검. 모순 없음 | 53 |
| 54 | Add a settings.py that holds the claims-core base URL and API key … | 로드 | 로드 | 값을 환경변수에서만 읽는 `settings.py` 작성, 리터럴 기본값 없음. S8 이 의도대로 작동; 4항목도 「해당 없음」으로 항목별 보고 | 54 |
| 55 | 사정인이 담당 청구를 청구번호로 조회하는 핸들러를 … 추가해 줘. (한국어·역할 과제) | 로드 | 로드 | 핸들러+spec 작성; 최종 요약은 한도로 끊김 | 55 |
| 56 | (51 재실행) | 로드 | 로드 | `--max-turns 8` 소진(error_max_turns)으로 요약 없이 끝남. 로드는 첫 턴에 확인 | 56 |
| 57 | (52 재실행) | 로드 | 로드 | 완주. 요약 표에 S1–S8 항목별 결과; S2(청구번호 패턴 근거 없음)·S4(`actor_role` 노출)를 「미결/판단 요청」으로 남김 — 스킬의 「모호하면 오너에게」 지시대로 | 57 |
| 58 | (55 재실행) | 로드 | 로드 | 완주. `GET /adjuster/claims/<id>` 를 사정인 세션 키만 읽게 작성(S7), 권한·존재 확인을 한 경로로(S6), 호출 수·캐시를 spec 에 적음(S5). S1 은 org note 대로 재지적 안 함 → 두 스킬 사이 모순 없음 | 58 |

집합 결과: 8/8 문구에서 두 스킬 모두 로드. 완주한 53·54·57·58 에서 두 스킬의 지시가 어긋난 곳 없음 — 특히 S1 재지적 금지(org note)와 S7(역할 키)이 같은 답 안에서 공존했다(58).

## 기준선 단독 시험 — secure-api-review 만 넣고

| # | 문구 | 로드 | 결과 · 비고 | raw |
|---|---|---|---|---|
| 59 | Create a POST /claims/{id}/notes endpoint … so an agent can attach a note to a claim. | 로드 | 4항목 항목별 보고(감사 이벤트 포함) | 59 |
| 60 | Generate an OpenAPI 3 spec (openapi.yaml) for the routes in src/claims.py. | 로드 | `openapi.yaml` 작성 + 4항목 보고; org note 대로 세션 인증은 지적하지 않음 | 60 |
| 61 | src/claims.py 의 API 코드를 리뷰해 줘. 고치지는 말고 문제만 알려 줘. (한국어) | 로드 | 4항목 항목별 리뷰 | 61 |

기준선 단독 결과: 3/3 로드. (예비 시험 — 최초 스모크 런 1회, 기준선만, 「Add a GET … history endpoint」: 로드. 원문은 남기지 않아 표에 넣지 않는다.)

## 집합 시험 2회차 — 채택분을 넣은 세 스킬(secure-api-review · claims-api-security · secrets-scan)

`secrets-scan` 을 채택한 뒤 같은 샌드박스에 셋을 함께 넣고 다시 돌렸다(2026-09-09T22:07Z ~ 22:09Z).
`secrets-scan/` 은 `SKILL.md` 와 그것이 가리키는 `plays/secrets-scan.md` · `templates/finding.md` 까지 함께 넣었다.
66–68 의 샌드박스에는 훑을 것이 있도록 `src/settings.py`(자리표시자 값, 비밀값 모양이 아님)를 하나 더 뒀다.

| # | 문구 | secure-api-review | claims-api-security | secrets-scan | 결과 · 비고 | raw |
|---|---|---|---|---|---|---|
| 62 | Add a settings.py that holds the claims-core base URL and API key … | 로드 안 됨 | 로드 | **로드 안 됨** | 값을 환경에서만 읽고 리터럴 기본값 없는 `settings.py` 작성 — S8 은 지켜졌다. 다만 셋 중 하나만 떴다(아래 「빈 곳」) | 62 |
| 63 | intent/0001-… 를 읽고 spec.md 초안을 써 줘. 우리 정책 스킬을 적용해서. | 로드 | 로드 | 로드 안 됨 | S1–S4 · S5–S8 을 항목별로 보고. S5 의 rps 환산 입력값이 없어 「닫히지 않음」으로 남김 — 스킬의 지시대로 | 63 |
| 64 | Review src/claims.py for security problems before I open the PR. … | 로드 | 로드 | 로드 | **셋 다 로드.** 답 하나 안에서 S1–S4 → S5–S8 → 비밀값 순으로 이어지고 서로 부딪히지 않았다. S1 은 org note 대로 재지적하지 않는다고 명시 | 64 |
| 65 | 사정인이 담당 청구를 … 핸들러를 하나 추가해 줘. | 로드 | 로드 | 로드 안 됨 | 턴 한도(`--max-turns 8`)로 요약 없이 끝남. 로드는 첫 턴에 확인 | 65 |
| 66 | Before I merge this, check the repo for leaked secrets or hardcoded credentials. | 로드 안 됨 | 로드 안 됨 | 로드 | 채택분이 자기 자리에서 뜬다 | 66 |
| 67 | 커밋하기 전에 코드랑 설정에 자격증명이 하드코딩돼 있는지 훑어봐 줘. (한국어) | 로드 안 됨 | 로드 안 됨 | 로드 | 같음 | 67 |
| 68 | Audit this repository for credential exposure and tell me what to rotate. | 로드 안 됨 | 로드 안 됨 | 로드 | 같음 | 68 |

채택분 `secrets-scan` 의 트리거: **4/4**(64 · 66 · 67 · 68), 서로 다른 네 문구.
집합 충돌: 셋이 함께 뜬 64 에서 지시가 어긋난 곳 없음. `secrets-scan` 의 발견 보고 형식(`templates/finding.md`)과
기준선의 「항목별로 요약에 적어라」가 한 답에 같이 있었지만 충돌 없이 절을 나눠 썼다.

### 빈 곳 — 62 에서 드러난 것
`secrets-scan` 의 트리거 문장은 **검토·감사** 쪽이다(`Use when reviewing code for leaked secrets before commit/merge,
auditing a repository for credential exposure, or setting up secret detection`). 그래서 62 처럼 **자격증명을 담는 설정 파일을
새로 쓰는** 과제에는 뜨지 않았다 — 정작 S8 이 가장 필요한 순간이다. 그 자리는 설계분 `claims-api-security` 의 S8 절이
메웠고(62 에서 로드됨), 실제로 환경변수만 읽는 파일이 나왔다. 채택분의 트리거 문장은 원문 유지 원칙 때문에 고치지 않았다
(`skills/secrets-scan/PROVENANCE.md`). 62 에서 `secure-api-review` 까지 뜨지 않은 것은 2 스킬 집합의 같은 문구(54)에서는
떴던 것이라 — 트리거는 결정적이지 않다. 「권고적 통제」(플레이북 L6 503)의 실물이다.

## 설계 스킬(claims-api-security) 트리거 근거
집합 시험 2 스킬 8/8(51–58) · 3 스킬 4문구 중 4/4(62–65) 에서 매번 로드. 문구는 엔드포인트 추가(영·한), spec 작성(한), 리뷰(영), 설정/비밀값(영), 역할별 핸들러(한)의 다섯 갈래. 트리거 문장을 고쳐야 했던 경우: 없음(초안 그대로 8/8).

## 확인 못 한 것
- 설계 스킬을 **단독**으로 넣은 시험은 하지 않았다(집합에서 매번 로드됐고, description 은 단독일 때와 같다).
- 51·52·55·56 은 로드는 확인됐으나 최종 요약이 계정 한도 또는 턴 한도로 끊겼다 — 지시 준수 여부는 57·58 재실행으로 확인했다.
- 대화형(비헤드리스) 세션에서의 로드는 시험하지 않았다.
- 65 는 턴 한도로 요약이 없어 세 스킬의 지시가 한 답에서 어떻게 만나는지 못 봤다 — 그 확인은 64 로 했다.
- 트리거는 시행마다 같지 않다: 같은 문구(설정 파일에 API 키)가 2 스킬 집합(54)에서는 `secure-api-review` 를 띄웠고 3 스킬 집합(62)에서는 띄우지 않았다. 각 칸은 그 1회의 관측이지 확률이 아니다.
