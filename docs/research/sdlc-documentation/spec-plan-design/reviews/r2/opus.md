# 후속 리뷰: r2 (920ca52) — 범위 한정

## 판정: **PASS**

r1의 차단 3건이 실제 본문에서 해소됐다. 남은 발견 2건은 한 줄 보강으로 끝나며 문서 간 모순이나 인계 불능을 만들지 않으므로 활성화 전 처리 권고로 남긴다.

## r1 차단 항목의 해소 확인

1. **정책 정본 링크·권위** — `templates/spec.md` L19–20(RELEASE-CONTROL), `templates/plan.md` L13–14(GIT-WORKFLOW·PR-SIZE·RELEASE-CONTROL), `guidance/execution-blocks.md` L3–5, `guidance/design-blocks.md` L17–18, `skills/plan/SKILL.md` L12–13, `policy-and-delivery.md` L3–4, `examples/F03/spec.md` L7에 정책 링크가 들어갔고 모두 "정책의 정본은 이 양식/지침이 아니다"를 명시한다. 상대 경로 깊이도 실제 `docs/` 위치와 일치한다(양식 5단계, F03 spec 6단계, plan 스킬 6단계 확인). 제3의 규칙 위치 병설 금지(L55)와 기존 `design-depth.md`/`execution-depth.md` 경로 교체가 전달표 L47–48에 명시돼 중복 정본 문제도 닫혔다.
2. **기존 작성 지침·reference·예시 전달 매핑** — 전달표(L43–53)와 「기존 작성 지침 보존/교체 매핑」(L61–71)이 절 단위로 교체/보존을 지정한다. r1에서 소실됐던 항목이 실제 본문에 복귀했다: `skill-provenance.md` 보존본과 참조(design-spec SKILL L18), `spec-policy-pass`(L16–17), GIT-WORKFLOW 단계 수락(plan SKILL L12–13), `INTENT_TASK=fix`·mutation 원본 복구(plan SKILL L27–29), F02용 `two-pr` 예시 유지(L71).
3. **TDD 정책 위치와 원문 보존** — 「넣을 정확한 위치」 표(L17–24)가 maker CLAUDE.md/Conventions, 사용판 PROJECT-POLICY.md·CLAUDE.md, ADOPTING.md, sdlc-feedback, sdlc-verifier의 절까지 특정하고 "Verifying your work의 L9 verbatim 블록은 수정하지 않음"을 못박았다. 검토 기준 정본은 `sdlc-verifier.md`의 Review criteria 한 곳으로 유지(L36)돼 이중 기준이 생기지 않는다. 정책 문장 자체는 북극성 L9(결함 재현 선행)와 팀 선택(전체 동작 TDD)을 계속 구분한다(L14).
4. **예시 입력 전달·상류 핀** — 입력 전달 절(L73–82)이 cases·baseline·JSON·M01 context의 보존 위치와 역사 자료의 연구 폴더 잔류·출처 재표기를 구분한다. `examples/F03/context.md` L6–8이 "인계 정본은 현재 spec/plan, 역사 문서는 출처 추적용"으로 정리해 과거 번호 혼선을 막는다. 상류 핀(intent@4a74823, spec@23845b5)은 제공된 `git cat-file` 검증 결과를 근거로 종결한다.
5. **F03·M01 명료화의 회귀 없음** — F03: 공개 기록 위치가 제품 `intent/f03-owner-insights/decisions.md`로 특정되고(spec L60, plan L44–45), P4가 "사본 리허설 ≠ 실제 일반 환경 관측"으로 분리됐으며 AC6 문구와 충돌하지 않는다. 상태도의 `상시 제공` 개명도 R5/AC7과 일치한다. M01: 기존 DB만 열고 user_version·스키마를 확인하며 실패 시 새 DB 생성·JSON fallback 없이 시작 실패(architecture L62–65)가 plan PR-C 1단계·P-C의 예정 시험과 일치하고, `storage.md`의 "DB 생성은 이행 도구만"과도 모순되지 않는다. 운영 문서 소유(spec L16–17: 조건은 design/operations.md, 명령·리허설 절차는 제품 docs/operations.md)가 명시됐다. 두 plan의 `Current change:` 줄은 execution-blocks L35 규칙대로 Upstream 바로 아래에 있다.

## 남은 발견 (활성화 전 권고)

1. **작성 언어·고정 영문 절 이름 지시가 승계되지 않았다.** 기존 `.claude/skills/design-spec/SKILL.md` L39 "Write in the originator's language and retain the six English section names"가 후보 `skills/design-spec/SKILL.md`(L23 "Preserve the six information roles")에도, 보존 매핑 L65(Writing 절 교체)에도 없다. maker CLAUDE.md L18–19에는 남지만 사용판으로 전달되는 스킬/양식에는 근거가 사라진다. **최소 수정:** design-spec SKILL L23에 해당 한 문장을 추가하고 매핑 L65 행에 "작성 언어·영문 절 이름 유지"를 적는다.
2. **M01 시작 시 DB 검증에 대응하는 R/AC가 없다.** 계약은 `design/architecture.md` L62–65(정본 집합 안)에 있고 plan P-C가 증명하지만, `examples/M01/spec.md`의 R1–R6·AC1–7 어디에도 "없는 경로·잘못된 스키마/버전 → 시작 실패, 새 DB 비생성"이 없어 AC 대조만으로는 이 동작이 보이지 않는다. **최소 수정:** R2 또는 AC2에 "sqlite 선택 시 architecture의 시작 검증 실패는 시작 거부·새 DB 비생성" 한 항목을 더한다.

부수 관찰(수정 불요): 후보 스킬의 북극성 인용이 원문 전체 인용에서 줄 번호 표기 + 축약 인용으로 바뀌었다(design-spec L7–8, plan L7–8). 내용은 발췌 원문과 일치하고 오너 리뷰 질문은 그대로 축자 보존돼 있다.

## 검토 범위와 한계

읽은 것: 지정된 변경 파일 전부(양식 2, design-spec SKILL + skill-provenance, plan SKILL, guidance 2, policy-and-delivery, tdd PROVENANCE, F03 3파일, M01 spec/plan/architecture)와 대조용 r1 기억 및 이전에 읽은 불변 계약(`docs/{GIT-WORKFLOW,PR-SIZE,RELEASE-CONTROL}.md`, 활성 `.claude/skills` 본문, `CLAUDE.md`, M01 `storage.md`/`operations.md`).

한계: 도구는 Read만 사용했고 편집·셸 실행 없음. 동료 리뷰·제안서·인계 답변은 읽지 않았다. 미확인: `codex/use-template-0023`의 PROJECT-POLICY.md 절 이름(작업 트리에 없어 표기의 정확성은 검증 불가), Git 이력·해시 재검증(제공된 결과 신뢰), Mermaid 실제 렌더링, `make check`·플러그인 설치 실행. 이번 판정은 문서 설계 범위에 대한 것이며 실제 설치·런타임 TDD 준수 근거가 아니다.
