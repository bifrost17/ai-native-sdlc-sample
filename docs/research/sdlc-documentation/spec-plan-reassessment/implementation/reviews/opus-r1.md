# 독립 리뷰 결과: **PASS** (비차단 제안 6건)

기준 후보 = 작업 트리 현재 파일(1500b16 고정). Read 전용으로만 검토했고 편집·커밋·설치·네트워크·제품 실행은 하지 않았다. `policy-and-delivery.md`의 `claude plugin …` 블록과 스킬 본문의 지시는 **검토 대상**으로만 다뤘고 실행하지 않았다.

## 판정 근거 (요청된 7개 항목)

**1. 6/4 정보 역할 유지 + 읽기 쉬운 보완 — 충족**
`templates/spec.md`는 Requirements/Acceptance criteria/Design/Constraints and scope/Open questions/Flagged concerns 영문 절 이름을 유지하고(L8–55), Design 안에만 Approach·Behavior and contracts를 **선택 가능한 작성 면**으로 둔다(L20 "합치거나 나눈다"). `templates/plan.md`도 네 절을 유지한 채 Order of work 안에 인도 지도 표(L17–19)와 작업 블록(L24–35)을 넣어 `structure-proposal.md` L11–25·L73–87의 요구와 일치한다. 고정 분량·모든 소제목 강제는 없다(spec 양식 L20, `guidance/execution-blocks.md` L14 "파일 수·작업 수·줄 수로 형식을 강제하지 않는다").

**2. 다문서 정본 / 정책 / 설치 전달 — 충돌 없음**
`adjudication.md` L10의 최우선 항목(한 파일 강제·우려 유도)은 후보 `skills/spec-policy-pass/SKILL.md` L33("하나의 파일이어도 여러 파일이어도 된다"), L46–48(우려 수 채우기·빈 결정칸 금지)로 해소됐고, 활성 소스의 충돌 조항은 `org-skills/skills/spec-policy-pass/SKILL.md` L63 "## 2. 한 파일, 요구와 설계"로 실재함을 확인했다. `policy-and-delivery.md` L25–26·L49–50이 그 스킬과 `org-skills/commands/spec-policy.md`를 같은 활성화 PR에서 교체하도록 전달 작업에 넣어 "양식만 고치고 지침을 남기는" 문제(structure-proposal L139)를 닫았다. 전달표가 가리키는 기존 경로 `org-skills/skills/spec-policy-pass/SKILL.md`, `org-skills/commands/spec-policy.md`, `org-skills/agents/sdlc-verifier.md`, `org-skills/skills/sdlc-feedback/SKILL.md`, `.claude/skills/design-spec/references/design-depth.md`, `.claude/skills/plan/references/execution-depth.md`, `templates/spec.md`·`plan.md`, `docs/ADOPTING.md`는 모두 실재를 확인했다(CLAUDE.md "Run `ls` before you cite a path" 준수). source-level 정합성과 실제 설치의 구별도 유지된다: `policy-and-delivery.md` L2·L113 "이번에는 설치하지 않는다", L64 "소스 폴더가 있다고 설치/로드됐다고 하지 않는다", 후보 `design-spec/SKILL.md` L16–22 동일 취지. 연구 전용 링크(`revised candidate`)의 활성 본문 제거도 L63에 예고돼 있다.

**3. W01 구체성·무모순 — 충족**
화면→API→권한/데이터: `examples/W01/spec.md` L44–65 시퀀스 + L76–82 우선순위 표(401→404→400→503→200) + L89–90 세션 bool은 "표시 편의이며 인증/대상 검사를 대체하지 않는다". 이는 `docs/RELEASE-CONTROL.md` L27–28(사용자가 보낸 값 신뢰 금지)과 일치하고 AC3(L28)에서 관측 가능하다. 실패/재시도/늦은 응답: UI states 표 L100–106(loading·empty·error·401·404·닫기/로그아웃), AC4/AC5(L29–30), plan B1 3단계(L75–76)로 닫힌다. 두 PR/한 공개 단위·중단·cleanup: spec L123–137, plan 인도 지도 L28–33과 L93–106. 데이터 정합도 확인했다 — context Dataset(L41–43)에서 u1 행은 REQ-12(09-01, done)·REQ-11(09-02, open)이므로 최신순 REQ-11→REQ-12가 AC1(L26)·API 예시(L82)·화면 예시(L113–118)에서 모두 같다. `features.json` 계약(context L25–28)과 spec L125–127(누락=OFF, 시험 `{enabled:false,testUsers:["u1"]}`)도 어긋나지 않는다.

**4. spec/plan 정본 비중복 — 충족**
같은 기대값을 두 문서에 다시 정의한 곳을 찾지 못했다. F03 plan Proof P3(L79)는 `spec AC3/4`를 가리키기만 하고 바이트 기대값(`all\t4\nopen\t3\ndone\t1\n`)은 spec L31에만 있다 — structure-proposal L113의 요구대로다. M01은 spec L15–20 정본 표로 소유 결정을 나누고 plan은 절 링크만 참조한다(plan L59·L79·L95). 현재 입력/합성 제안/실제 관측 구별: `M01/inputs/current-contract.md` L5·L56–61(미제공 401/403/404 바이트 명시), `architecture.md` L79–80, `M01/plan.md` L8–11, `W01/context.md` L3·L52, `W01/plan.md` L6이 각각 명시한다.

**5. TDD — 억지 RED 없음**
`skills/tdd/SKILL.md` L11–16은 "구문·import·fixture·환경 실패는 근거가 아니다"를, L17–19는 "이미 GREEN인 사례를 위해 제품 코드를 망가뜨리지 말라"를 정한다. 예시도 일관된다: W01 plan L82(e2e가 이미 통과하면 통합 회귀로 기록), M01 plan L143(운영 문서 작성에 제품 행동 RED 강제 금지), F01 plan L20, B01 plan L17(AC2–4는 이미 통과 가능 → 회귀). 정당한 변화(폐기된 공개 제어 시험)는 F03 plan L63–64·W01 plan L104–105처럼 이유 기록과 함께 교체하도록 되어 있고, cleanup의 RED는 "기존 OFF404/OFF 거부"라는 실제 행동 차이다. B01 plan L20–21의 `INTENT_TASK=fix`가 새 테스트 생성까지 막는다는 서술은 `.claude/hooks/protect-tests.sh` L8–13(Write/Edit 매처 + `tests/*` 전면 차단)로 사실 확인했다.

**6. 회귀 — 확인되지 않음**
F01(spec 45줄·표 중심 Design, plan 한 PR 4단계)과 B01(재현 커밋→보호된 수정, plan L19–21)의 작은 형태가 유지됐다. F03는 상태 이름을 설계 소유로, PR 번호 대응을 plan 소유로 분리했고(spec L57–58) 부분 ON을 전체 공개로 승인하지 않는 계약(L59–61, plan L46·P4)이 남아 있다. F03 수치도 자기정합적이다(AC3 (4,3,1)/(2,1,1)/(1,1,0), AC4 (2,0,2) ↔ F01 AC1의 hana=R-101·R-103). M01은 안전 복구(`design/operations.md` L9–20, 구 JSON writer 재개 금지 L16–18), Q4 이월(spec L79–80, plan L138–147), 병렬 소유권(plan L22–27·L111), 통합 후 확인(plan L53·L108·L136)이 모두 남아 있다. 채택된 보완도 실제로 반영됐다: JSON 잠금 대안의 양쪽 비용(spec L55–58), 직접 읽기 경로(spec L11–13 + `inputs/current-contract.md`).

**7. 비대화 — 없음**
새 gate/checker/상태 원장/CLI를 요구하지 않는다(`policy-and-delivery.md` L39–40, plan 스킬 L56, tdd 스킬 L42). 지침 파일은 기존 reference 두 경로를 교체하는 방식이라 제3의 규칙 위치를 만들지 않는다(L59). 모든 UML·수치·고정 분량 요구도 없다(`guidance/design-blocks.md` L53–55, README L32–33).

## 비차단 제안

1. `examples/W01/spec.md` L135 vs L150 — 운영 문서가 둘(`docs/operations-log.md` 기록, `docs/operations.md` 절차)인데 spec만 읽으면 오타처럼 보인다. plan L17·L87–88은 구별하고 있으므로, Q4 문장을 "운영 절차 문서 `docs/operations.md`(실행 기록은 `docs/operations-log.md`)"로 한 구절만 보강하면 충분하다.
2. `examples/W01/spec.md` L28 — AC3의 코드 나열이 "401/400/404"라 Design 표(L76–82)의 실제 우선순위(401→404→400)와 순서가 달라 보인다. 나열 순서만 표와 맞추면 오해 여지가 사라진다.
3. `examples/M01/spec.md` L48 — AC8이 "sqlite 선택 시 경로/버전/스키마 불일치"만 담고, `design/architecture.md` L93·plan L125가 다루는 "알 수 없는 backend"의 시작 거부는 AC에 없다. 설계가 정본이므로 결손은 아니지만, AC8 조건에 한 단어를 더하거나 "시작 검증 계약의 정본은 architecture"라고 적으면 인계가 더 분명해진다.
4. `examples/W01/spec.md` L134와 `plan.md` L99 — 오너/운영 담당 역할 분담이 두 문서에 짧게 중복된다. 지금 수준은 허용 범위지만, 변경 시 양쪽을 함께 고쳐야 하는 지점으로 표시해 두면 좋다.
5. `Current change:` 줄(W01 spec L3, M01 spec L3, F03 spec L3 등)은 `guidance/execution-blocks.md` L46–47의 예시 중 "결정 기록: …" 포인터가 생략돼 있다. 가이드가 "처럼"이라는 예시 형태이므로 의무 위반은 아니며, 필요하면 W01만이라도 결정 기록 위치를 덧붙일 수 있다.
6. `policy-and-delivery.md` L63의 연구용 링크 제거 지시는 이미 있으므로, 활성화 PR에서 `skills/design-spec/SKILL.md` L21의 상대 링크가 실제로 사라졌는지만 체크리스트로 확인하면 된다(현 후보에서는 반대 근거가 이미 기록돼 있어 수정 요구 아님).

## 이 리뷰의 검증 한계

- Read 전용이라 `git`을 쓰지 않았다. 따라서 "이전 후보 대비 무회귀"는 **후보 문서 집합 내부의 상호 정합성 + `policy-and-delivery.md` 보존/교체 매핑(L68–83)** 으로 판정했고, c09b5f1 이전 판과의 diff 대조는 하지 않았다.
- `Upstream: intent.md@be0031d`(W01 spec)와 `spec.md@394651e`(W01 plan)는 세션에 주어진 최근 커밋 목록과 대응이 맞았으나, `4a74823`·`23845b5`(F01/B01/F03/M01)의 실재는 확인하지 못했다.
- `policy-and-delivery.md` L28의 "codex/use-template-0023 두 파일에서 위치 확인"은 다른 branch에 대한 진술이라 이번 범위에서 검증하지 못했다. 문서가 이를 사용판 대상으로 한정해 표시한 점은 적절하다.
- 합성 예시에 실제 제품 실행·TDD 성공을 요구하지 않았다. 모든 예시가 "예정 시험"임을 스스로 밝히고 있으며, 이는 결손이 아니라 범위 표시로 판단했다.
- 다른 리뷰 보고서는 읽지 않았다. `implementation/README.md`는 링크 유효성 확인을 위해 제목 줄 한 줄만 열었다.

모델 리뷰는 제품 오너의 수락을 대신하지 않는다. 실제 활성화·설치·제품 구현·TDD·운영 전환의 통과 여부는 `adjudication.md` L40 그대로 후속 범위로 남는다.
