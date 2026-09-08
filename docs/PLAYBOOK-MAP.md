# PLAYBOOK-MAP.md — 플레이북 14 플레이 전수 판정

설계안(`docs/DESIGN.md`) §8 표를 정본 문서로 옮긴 것. 여기서부터 이 판정이 정본이고,
§8 은 그 시점(W1 착수 전)의 설계 의도로 남는다.

**판정 시점**: 이 문서는 W1-D 레인의 브랜치(`docs/0001-playbook-map`) 위에서, 그 커밋들이
만드는 실물만 보고 썼다. 형제 레인(W1-A/B/C)의 산출물은 이 시점에 origin 에 별도 브랜치로
푸시돼 있지 않아 **파일 존재를 확인할 수 없었다** — 그런 항목은 「이월(W1 진행 중 · 확인
못 함)」으로 적었다. 실물이 없는데 「구현」이라 쓰지 않는다.

판정 어휘: **구현**(실물이 이 브랜치에 있고 요구를 충족) · **부분**(실물 일부만 있음) ·
**해당없음**(서술형 레슨이라 산출물 판정 대상이 아님) · **이월**(§10 `PHASES.md` 로 영구
이월되었거나, 아직 다른 레인/웨이브 소관이라 이 시점엔 실물이 없음).

| # | 레슨(slug) | 판정 | 이 레포의 파일 | 근거 |
|---|---|---|---|---|
| 1 | introduction | 해당없음(서술) | `README.md` | 「사슬 = 감사 추적」 주장을 README 가 이미 인용하고 있다 — 레슨 1 자체는 산출물이 아니라 프레임 서술이라 구현/이월 판정 대상이 아니다 |
| 2 | capture-intent | 부분 | `.github/ISSUE_TEMPLATE/intent.yml` | 비엔지니어용 5절 폼 + 첫 대화 시각 입력은 이 브랜치에 있다. `templates/intent.md`·`intent/` 홈·`capture-intent` 스킬은 다른 레인 소유라 이 브랜치엔 없다(이월·W1 진행 중·확인 못 함) |
| 3 | requirements-and-design | 이월(W1 진행 중) | 없음 | `templates/spec.md`·`.claude/commands/spec.md`·flagged concerns 절은 W1-A/B 소관. 이 브랜치엔 실물 없음(확인 못 함) |
| 4 | plan-mode | 이월(W1 진행 중) | 없음 | `templates/plan.md`·`plan-sync` 훅·`docs/SOURCE-OF-TRUTH.md` 는 각각 다른 레인 소유. 이 브랜치엔 실물 없음(확인 못 함) |
| 5 | claude-md | 구현 | `CLAUDE.md` | ≤60줄(실측 35줄) · Commands(healthy output 포함) · Conventions · Architecture · Verifying your work · Things Claude gets wrong · 「두 번 틀리면 등재」 규칙까지 전부 포함 — `scripts/gates/10-docs.sh` 검사 ①이 줄 수를 강제 |
| 6 | skills-as-institutional-knowledge | 이월(W1 진행 중) | 없음 | `capture-intent`·`secure-api-review` 스킬(`.claude/skills/**`)·`check_endpoints.sh` 는 다른 레인 소유. 6b(hooks as build-time guardrails, 훅 5개)도 같은 이유로 이월 — `.claude/hooks/**` 는 이 브랜치에 없다(확인 못 함) |
| 7 | parallel-sessions-and-subagents | 이월 | 없음 | `.claude/agents/verifier.md` 는 다른 레인 소유. 설계상도 병렬 세션은 1인 레포라 문서화만 대상(`PHASES.md` 「auto mode · worktree 병렬 세션」 항) |
| 8 | give-claude-a-feedback-loop | 부분 | `Makefile`, `CLAUDE.md` | `make check`/`make test` 골격과 CLAUDE.md 의 healthy output 검증 블록은 있다. `make test` 는 아직 placeholder(`no tests yet (W1)`)이고, 레슨의 핵심 시연(0003 결함 사슬 — 실패 시험 먼저 → 훅 → green)은 W3 소관이라 이월 |
| 9 | continuous-evals-in-ci | 이월(W1 진행 중) | 없음 | `evals/cases/*.json`·`check.sh`·`agent-evals.yml` 은 다른 레인/웨이브 소관. 이 브랜치엔 실물 없음(확인 못 함) |
| 10 | ai-in-the-pr-review-loop | 부분 | `REVIEW.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/CODEOWNERS` | 패스 3(bugs·security·compliance) · Important 정의 · Nit 상한 · 보고 제외 목록 · PR 사슬 4문 · CODEOWNERS 전부 이 브랜치에 있다. `claude-code-action`·관리형 리뷰·`@claude` 픽스 루프·babysit 은 `PHASES.md` 로 이월 |
| 11 | hooks-as-approval-gates | 이월(W1 진행 중) | 없음 | `production-gate.sh`·`scripts/deploy.sh`·`org/managed-settings.example.json` 은 다른 레인 소관. 이 브랜치엔 실물 없음(확인 못 함) |
| 12 | ci-cd-integration-and-deployment | 이월 | `.github/workflows/check.yml` | PR·push 에서 `make check` 를 필수 상태 체크로 거는 것(W0 기존)만 실재. 브랜치 보호 실증·배포 흉내 스크립트·「에이전트는 게이트까지만」은 `PHASES.md` 「샌드박스 · MCP 배포 도구 · 롤백 리허설 · 환경별 티어」 항으로 이월 |
| 13 | closing-the-loop-on-metrics | 부분 | `docs/METRICS.md` | 플레이북 14쌍 전부의 정의·계산 가능성 판정과, 계산 가능한 3종의 git 계산식은 이 브랜치에 있다(실값은 비움). `ops/bands.yaml`·`detect_bands.py`·`emit_intent.py`·`scripts/metrics.py` 실행부는 W3 소관이라 이월 |
| 14 | closing-thoughts-and-resources | 해당없음(서술) | `docs/PLAYBOOK-MAP.md`(이 문서 말미) | 레슨 14 자체는 산출물이 아니라 요약·링크 레슨이라, 아래 리소스 목록으로 옮겨적는 것으로 충분하다 |

**집계(이 시점)**: 구현 1 · 부분 4 · 해당없음 2 · 이월 7. 설계안 §8 의 최종 목표(구현 8 · 부분
4 · 해당없음 2)와 차이가 나는 것은 이 문서가 **지금 시점**(W1 착수 직후)을 재기 때문이다 —
다음 웨이브가 착지할 때마다 이 표를 갱신한다.

---

## 레슨 14 리소스 — 우리 말로 한 줄씩

플레이북 원문(레슨 14)이 가리키는 플랫폼 문서 14개를, 이 레포의 문맥에 맞춰 한 줄씩 옮긴다
(D13 인용 정책 — 축자 인용 대신 짧은 요지 + 무엇을 위해 참고하는지).

1. **Claude Code 개요 문서** — 이 레포의 모든 강제 장치(훅·서브에이전트·설정)가 어떤 도구
   위에서 도는지의 기준.
2. **CLAUDE.md 작성 가이드** — 이 레포 `CLAUDE.md` 의 절 구성(Commands·Conventions 등)의 근거.
3. **훅(hooks) 레퍼런스** — `.claude/hooks/**`(다른 레인 소관)가 구현할 이벤트·matcher·exit
   코드 규약.
4. **서브에이전트 레퍼런스** — `.claude/agents/verifier.md`(다른 레인 소관)가 따를 정의 형식.
5. **스킬(skills) 레퍼런스** — `.claude/skills/**`(다른 레인 소관)의 `SKILL.md` 형식·트리거 규약.
6. **슬래시 커맨드 레퍼런스** — `.claude/commands/spec.md`(다른 레인 소관)가 따를 프롬프트→
   커맨드 변환 규약.
7. **관리형 설정(managed settings) 문서** — `org/managed-settings.example.json`(다른 레인
   소관)이 인용하는 키 전체 목록의 출처.
8. **권한(permissions)·샌드박스 문서** — `allowUnsandboxedCommands`·`failIfUnavailable` 등
   §6.3 이 인용하는 값의 정의처.
9. **GitHub Actions 연동 가이드** — `.github/workflows/check.yml`·`agent-evals.yml` 이 따르는
   워크플로 문법.
10. **브랜치 보호·CODEOWNERS 가이드(GitHub)** — `.github/CODEOWNERS`·§6.4 브랜치 보호 실증의
    근거.
11. **평가(evals) 하네스 가이드** — `evals/cases/*.json`·`check.sh`(다른 레인/웨이브 소관)의
    케이스 형식.
12. **모델 컨텍스트 프로토콜(MCP) 문서** — §10 「샌드박스 · MCP 배포 도구」 이월 항목이
    가리키는 확장 지점.
13. **Claude Tag(Claude in Slack) 문서** — §10 「Claude Tag 온콜」 이월 항목이 가리키는 채널.
14. **Claude Academy 코스 페이지 자체** — 이 설계안의 정본(§0 결정 요약의 출처), 레슨 slug
    좌표의 1차 자료.
