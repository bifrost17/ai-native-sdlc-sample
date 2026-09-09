## 무엇
사슬 0002(청구 상태 셀프서비스)의 spec → plan → 실패 시험 → 구현. base = `chain/0002-intent`(PR #17). **PR #17 이 머지되면 이 PR 의 base 를 `main` 으로 옮긴다.**

## 착수 근거
`design-spec` 스킬은 「intent 가 accepted(머지)가 아니면 쓰지 않는다」고 말한다. intent 는 아직 draft(PR #17 미머지)다. 엔지니어(부모 세션)가 2026-09-09 착수를 지시했고 그 사실을 spec.md 머리 한 줄에 남겼다 — 다인 조직이면 PR #17 머지를 기다렸을 자리다.

## 커밋 ↔ 단계
| 커밋 | 단계 | 산출물 |
|---|---|---|
| e257572 | 2 spec | `intent/0002-claims-status/spec.md` (36줄) — Upstream intent.md@d9d55ff · secure-api-review 항목별 점검 · 미결 3건 answered/carried |
| 1a7e4d1 | 3 plan | `plan.md` (29줄) — Upstream spec.md@e257572 · Proof 에 실재 시험 이름 |
| 23b2a56 | 4 실패 시험 | `tests/test_claims_status.py` (127줄) + 스텁 `src/claims_status/` — **red 실측 FAILED (failures=7)**, 0 ERROR(임포트 실패 아님) |
| (HEAD) | 5 구현 | `src/claims_status/{records,response,routes}.py` 합계 102줄 — 시험 미편집 |

## red → green 원문
- red(스텁 위): `Ran 10 tests` / `FAILED (failures=7)` / RC 1 — 단정 실패 7(예 `{} != {'error': 'unauthenticated'}`, `0 != 1`), 양성 대조 2 + 공허 통과 1(`pii_values_never_appear` 는 `{}` 위에서 참).
- green(구현 후): `Ran 10 tests` / `OK` / RC 0. 시험 파일 sha256 커밋 시점 = 작업 트리(`1e7b01bf751b5849`).
- `make check`: `Ran 29 tests … OK` · `test_hooks: 28 passed, 0 failed` · `8 passed, 0 failed` · `PASS  managed-settings` · RC 0.

## 훅 반응 (protect-tests · stdin JSON 직접 투입)
- `INTENT_TASK=fix` + Edit `tests/test_claims_status.py` → **rc=2** `[protect-tests.sh] BLOCKED: … Route: fix the code, not the test.`
- `INTENT_TASK=fix` + Edit `src/claims_status/routes.py` → rc=0 · INTENT_TASK 미설정 + tests/ → rc=0.
- 라이브 Claude Code 세션에서의 PreToolUse 발화는 **확인 못 함**(이 세션의 프로젝트 디렉터리가 이 레포가 아니라 훅이 물려 있지 않다).

## 뮤테이션 1건
`routes.py` 소유 판정을 `False and …` 로 침묵 살해(문자열 보존) → `test_ac4_foreign_and_unknown_claim_share_one_body` FAIL(`{'claim_id': 'C-1002', …} != {'error': 'not_found'}`) → 원복 sha256 `d9be501e…` 동일 → OK.

## secure-api-review 점검 요약
① 인증: 익명 경로 없음, 세션 없이는 값 없음 ② 입력: GET, 경로 인자 `C-<숫자>` 만, 오류 문구에 입력 되비춤 없음 ③ 감사: 읽기 전용이라 이벤트 없음 ④ pii: 응답·오류·로그에 없음(모듈이 로그를 남기지 않음). 상세는 spec.md Design.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01NzhLB6C1oHJHu7uAVDe54w
