# 독립 리뷰: spec·plan 설계 후보 r1 (2634f07)

## 판정: **CHANGES REQUIRED**

핵심 산출물(양식·스킬·TDD·네 예시·M01 연결 설계)은 인계 가능한 수준이다. 다만 **활성화 대상 저장소의 기존 정본과의 관계가 정의되지 않아** 같은 결정을 두 곳에서 다르게 관리하게 되는 모순이 남아 있다. 아래 3건은 문서 수준의 작은 수정으로 해소 가능하다.

---

## 차단 (blocking)

### B1. 활성 양식이 가리키던 팀 정책 정본 링크가 후보 양식에서 사라졌다
- 근거: 활성 `templates/spec.md` L15–16은 공개 제어 시 `docs/RELEASE-CONTROL.md`를, 활성 `templates/plan.md` L15·L17은 `docs/RELEASE-CONTROL.md`·`docs/GIT-WORKFLOW.md`·`docs/PR-SIZE.md`를 따르게 한다. 후보 `candidate/templates/spec.md`, `plan.md`, `guidance/execution-blocks.md`에는 이 세 문서가 **한 번도 등장하지 않는다**. `policy-and-delivery.md`의 전달표는 후보 양식을 "루트 templates의 대응 파일"로 교체한다고만 적는다.
- 모순: 교체 시 `RELEASE-CONTROL.md`의 공개 결정 기록·제거 순서, `GIT-WORKFLOW.md`의 단계 수락 기록(문서·SHA·결정자)·merge 방식 규정으로 가는 유일한 진입점이 끊긴다. 동시에 `execution-blocks.md` L5–7(stacked/장기 통합 브랜치 금지), L14–16(일반 OFF 배포 가능)은 `GIT-WORKFLOW.md` L44–47, `RELEASE-CONTROL.md` L23–31을 링크 없이 재서술해, 후보 자신의 규칙(`design-blocks.md` L33–34 "같은 결정을 둘 다 다르게 정의하지 않는다")을 위반한다. 역사 F03 spec(`inputs/f03-spec-historical.md` L68, L79)은 정확히 이 정책을 인용하는데 후보 F03 spec에는 인용이 없다.
- 최소 수정: 후보 spec 양식의 설계 안내와 plan 양식의 Order/Proof 안내에 세 정책 문서 링크 한 줄씩을 복원하고, `execution-blocks.md` 서두에 "판단 기준은 docs/GIT-WORKFLOW.md·PR-SIZE.md·RELEASE-CONTROL.md이며 이 문서는 그 답을 계획에 옮기는 형식만 다룬다"를 명시한다.

### B2. 작성 스킬 "보강"의 병합 매핑이 없어 기존 스킬 본문이 소실된다
- 근거: `policy-and-delivery.md` 전달표는 `skills/design-spec, skills/plan`을 "기존 .claude/skills의 같은 작성 스킬을 보강"이라고만 적는다. 그러나 후보 SKILL.md 두 개는 전체 본문이며, 기존 `.claude/skills/design-spec/SKILL.md`의 L7–13(L3 인용), L28–33(`spec-policy-pass`, `references/skill-provenance.md`), 기존 `.claude/skills/plan/SKILL.md` L16–18(GIT-WORKFLOW 단계 수락), L41–44(`INTENT_TASK=fix` 훅·mutation 시 원본 바이트 복원)이 후보에는 없다. 특히 fix 모드는 실제 존재하는 장치이고(`CLAUDE.md` L32) 후보 B01 plan L20–21이 그것을 전제하는데, 정작 후보 plan 스킬은 그 규칙을 담지 않는다.
- 추가 모순: 기존 `references/design-depth.md`·`references/execution-depth.md`는 후보 `guidance/design-blocks.md`·`execution-blocks.md`와 역할이 동일한데(조건부 상세), 전달표는 후보 guidance를 제3의 위치 `docs/sdlc-authoring/guidance`로 보낸다. 기존 references의 폐기/병합 여부가 없어 활성화 후 두 벌이 공존한다. 기존 `examples/{feature,bug,migration,two-pr}`와 새 F01/B01/F03/M01도 같은 문제다.
- 최소 수정: 전달표에 절별 매핑 행을 추가한다 — 어떤 절이 교체·추가·유지인지, `references/design-depth.md`·`execution-depth.md`와 기존 examples가 폐기인지 유지인지, 유지라면 어느 쪽이 정본인지. 최소한 "기존 본문의 인용·권한 기록·fix 모드·provenance 절은 그대로 두고 이 후보의 해당 절만 대체한다"는 한 문장이 필요하다.

### B3. 의무 TDD 정책 문장의 설치 위치가 특정되지 않았고, 지정 후보 위치가 고정 인용 블록과 충돌한다
- 근거: `policy-and-delivery.md` 전달표 마지막 행은 "CLAUDE.md·사용 템플릿 기본 정책 및 기존 feedback/verifier 기준의 관련 부분만 갱신"이다. 다른 행은 모두 실제 경로를 쓰는데 이 행만 대상 파일·절이 없다. `CLAUDE.md`의 관련 절 "Verifying your work"는 L60에 "(L9 635-645 verbatim)"로 표시된 북극성 원문 복사본이므로 여기에 팀 의무 문장을 넣으면 원문/주석 구분(실행 계획 「고정 설계 조건」 첫 줄)을 깨뜨린다.
- 최소 수정: 대상 절을 명시한다 — 예: "CLAUDE.md의 Conventions에 한 줄로 추가하고 Verifying your work의 L9 원문 블록은 수정하지 않는다", 그리고 feedback/verifier는 `org-skills/skills/sdlc-feedback/SKILL.md`와 `org-skills/agents/sdlc-verifier.md#review-criteria`로 경로를 적는다.

---

## 비차단 (개선)

1. **예시 Upstream 핀의 해석 가능성 확인 필요.** 네 spec 모두 `Upstream: intent.md@4a74823`인데 `candidate/examples/*/intent.md`는 후보 폴더 파일이고 후보는 23845b5에서 작성됐다. 4a74823에 이 경로가 없었다면 후보 자신의 규칙(`skills/plan/SKILL.md` L37–38 "존재하는 상류 판에만 repin")을 어긴 핀이 된다. 확인 후 필요하면 23845b5로 재핀하거나 "입력 보존 커밋을 가리킴"을 한 줄 덧붙인다. (본 리뷰는 셸 미사용으로 미확인.)
2. **`change-walkthrough.md`가 전달표에 없다.** `guidance/execution-blocks.md` L37이 `../change-walkthrough.md`를 링크하는데, guidance만 `docs/sdlc-authoring/guidance`로 옮기면 이 링크가 깨진다. 전달표에 행을 추가한다.
3. **M01의 운영 문서 이중화.** spec 정본 `design/operations.md`와 PR-C 산출물 `docs/operations.md`(plan L14, L52)의 소유 범위가 spec.md 정본 목록에 없다. spec.md 표에 "조건은 design/operations.md, 실제 명령·절차는 제품 docs/operations.md" 한 줄을 넣으면 단일 정본 규칙이 유지된다.
4. **F03 공개 결정 기록 위치가 역사보다 약해졌다.** 역사 spec은 `intent/f03-owner-insights/decisions.md`를 지정하는데 후보 plan L42는 "기존 공개 기록"으로만 쓴다. `RELEASE-CONTROL.md` L43은 기록 위치를 요구하므로 예시에 위치 예를 한 개 넣으면 좋다.
5. **후보 README·`policy-and-delivery.md` 자체의 보존 위치**가 전달표에 없다. 연구 폴더 잔류가 의도라면 그렇게 한 줄 적는다.

---

## 통과로 판단한 부분

- 여섯/네 정보 역할 유지와 실제 채울 필드·표 보강, 영문 절 이름 고정(`CLAUDE.md` Conventions 준수).
- spec 단일 파일 강제 없음: M01 spec.md의 정본 표(L9–15)와 세 design 문서가 소유 결정·읽을 범위를 실제로 분담하고, 계약이 plan으로 밀려나지 않았다.
- 데이터 사실 정합: F01 AC1/AC4, F03 AC3/AC4의 (4,3,1)/(2,1,1)/(1,1,0)/(0,0,0)/(2,0,2)가 `inputs/f01-requests.json`과 baseline `tracker.py`의 rc1/rc2·오류 접두사와 일치한다.
- test-first 의무와 예외 처리: `skills/tdd/SKILL.md` 2·3문단이 예상 RED와 환경 실패를 구별하고, 이미 GREEN인 회귀·순수 리팩터링에 억지 RED를 금지하며, 정당한 시험 정정과 기대값 약화를 분리한다. 구현 선행 시 정직한 기록 규정도 있다.
- GitHub Flow/main 배포 가능성: F03 PR1·PR2의 일반 OFF 유지, M01 PR-B의 비활성 저장소 병합, "머지는 운영 전환이 아니다"가 명시적이다.
- 동시 갱신과 SHA: `execution-blocks.md` L30–33의 `Current change` 규칙이 자기 미래 해시 참조 문제를 발명 없이 해결한다.
- 알려진 사실 대 발명 구분: 합성 표기, "예정 증명", M01 아키텍처 L48(401/403/404 바이트 규약 미제공 명시), Q4 이월과 전환 금지 조건이 일관된다.

## 검토 범위와 한계

읽은 것: execution-plan.md, inputs/{spec-document-set, north-star-excerpts, cases, f01-requests.json, f03-spec-historical, baseline/tracker.py}, candidate 전체(README, 양식 2, guidance 2, 스킬 3, policy-and-delivery, change-walkthrough), 예시 4쌍 + M01 design 3편 + F01/M01 intent·context, B01/F03 context, 대조용 활성 파일(CLAUDE.md, templates/ 2, docs/{GIT-WORKFLOW,PR-SIZE,RELEASE-CONTROL}, .claude/skills 2 + references 2, org-skills/README).

읽지 않음(지시): proposals/, reviews/, handoff/, validation/, 과거 모델 리뷰 결론. 미확인: Git 이력·해시 해석(B01 비차단 1), Mermaid 실제 렌더링, `make check`/플러그인 검증 실행, 스킬 실제 로드, `b01-requests.json`·`f03-plan-historical.md`·B01/F03 intent 본문. 도구는 Read만 사용했고 파일을 수정하지 않았다.
