CMD: Agent(owa-investigate, opus) — 공개 저장소의 PR fix-loop 명령/스킬 발굴. 아래는 서브에이전트 보고 원문(부모가 인용한 항목은 raw/21-* 에서 부모가 직접 재확인함).
AT_UTC: 2026-09-09T09:33:31Z ~ 2026-09-09T09:45:00Z
RC: 0
(보고 본문은 다음 커밋 단계에서 이어붙임)

주: 아래 보고의 **모든 후보 30건은 부모 세션이 `raw/21-candidates-verified.tsv` 에서 직접 재확인**했다
(존재 · file sha · 라이선스 · 별 · pushed_at 전부 일치). 허용 라이선스(MIT/Apache-2.0) 14건은
부모가 원문 사본을 `raw/<name>@<sha>.SKILL.md` 로 다시 받아 인용 문장을 대조했다.

---

(서브에이전트 보고 요약 — 전문은 세션 기록. 부모가 채택 판단에 쓴 것은 아래 넷.)

1. 장르는 포화 상태다. `babysit-pr` 가 사실상 표준 이름이고, a/b/c/d 네 동작을 한 파일에
   담은 완전체가 최소 12건 실재한다. 신규 설계의 여지는 루프 구조가 아니라
   (가) 정지조건의 근거 (나) 리뷰 findings 신뢰 규칙 (다) prompt injection 가드 셋에 있다 —
   셋을 다 갖춘 후보는 없었다.
2. 도구는 `gh` CLI + GraphQL `reviewThreads` 로 수렴. REST `pulls/N/comments` 로는 resolve
   상태를 알 수 없고, `gh pr view --comments` 는 `COMMENTED` 리뷰 안의 인라인 코멘트를 못 본다.
3. 반복(d)의 구현은 셋으로 갈린다 — 문서 내 자연어 루프 · 하네스 스케줄러(ScheduleWakeup·
   /loop·CronCreate) · 외부 python watcher. 이식 가능한 단일 방법이 없다.
4. 답글 엔드포인트가 문서마다 세 갈래로 달랐다(§확인 못 함) → 부모가 실 PR 에서 실측해
   `pulls/<n>/comments/<id>/replies` 가 동작함을 확인(raw/10, raw/11).

열지 못한 것: michael-denyer/pstack-plugins(repo 404) · claudepluginhub 페이지(403) ·
solberg.is 글의 명령 본문(미공개) · nakamasato Medium(403) · `.agents/skills/babysit-pr` 계열의
upstream 원본. GitHub code_search 가 403 을 반복해 목록은 망라적이지 않다.
