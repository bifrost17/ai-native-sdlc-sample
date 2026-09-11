## 인계 검토 결과

### 1. 첫 작업 (PR-A / A1)

읽어야 할 실제 코드 경로(plan.md "읽기 기준")부터 확인한다: `src/server/auth.ts`, `src/server/features.ts`, `src/server/request-store.ts`, `src/server/app.ts`, `src/server/routes/session.ts`, `config/features.json`, 그리고 기존 시험 `tests/server/session.test.ts`, `tests/server/requests.test.ts`. 이 저장소는 문서 전용 합성 예시이므로 실제 제품 코드가 이 경로에 있는지부터 확인이 필요하다(context.md도 "제품 코드/실행 결과는 없다"고 명시).

첫 시험 파일: **`tests/server/my-requests.test.ts`** (신규), 첫 케이스명 `returns_only_current_users_rows`.
실행 명령: `npm run test:unit -- tests/server/my-requests.test.ts`
기대하는 RED: 라우트 미등록으로 인한 **404** (spec.md의 우선순위 1이 아니라 "경로 자체가 없음"에 의한 404). 인증/픽스처 오류로 실패하면 그건 유효한 RED가 아니므로 먼저 그 setup부터 고친다.

GREEN 경로: `src/server/routes/my-requests.ts`(신규) + `src/server/app.ts` 등록 → spec.md의 우선순위 표(401/404/400/503/200)와 정렬·투영 규칙을 따라 작은 행동 단위로 401(미인증), 404(OFF), 400(쿼리 파라미터), u3 빈 목록, 동률 정렬, 503(저장소 실패)을 각각 시험 먼저 추가한다. 완료 증거: 거부 케이스에서 `readRequests` 호출이 없었는지, 응답에 `internalNote`/`requesterId`가 없는지까지 확인.

다음은 A2(`tests/server/session.test.ts`, 케이스 `session_exposes_effective_flag_only`, 기대 RED는 새 bool 필드 부재)이고, PR-A 종료 시 `npm run test:unit`, `npm run build`, 기존 `npm run test:e2e -- tests/e2e/portal.spec.ts` 회귀를 최신 main 결합판에서 확인한 뒤 머지, 통합 main에서도 재확인한다.

이후 **PR-B**(`tests/web/my-requests.test.tsx`의 `opens_and_loads_my_requests`, 기대 RED는 버튼/패널 부재 → B2 e2e `tests/e2e/my-requests.spec.ts`)로 이어지고, 마지막으로 **공개/중단 리허설 → cleanup PR**(무설정 u2 본인 조회 시험이 기존 404 게이트에 의해 RED가 되는 것으로 시작) 순으로 진행한다. plan.md의 Delivery map과 Proof 표가 각 단계의 완료 증거 정본이다.

### 2. 문서로 이미 결정된 것 vs 나중에 물어야 할 것

**이미 결정됨** (다시 묻지 않음): Q1–Q3(정렬/실패 처리/공개 범위), API 계약 5단계 우선순위·응답 스키마, UI 7개 상태표, release 설정 값(`{enabled,testUsers}`), PR 순서(A→B→공개→cleanup), 각 작업의 첫 시험명과 기대 RED.

**나중에 물어야 함**: Q4(실제 호스트 설정 배치·재시작/상태 확인 명령, `docs/operations.md`에 확정)는 PR-A/B 코드 작업 시작에는 필요 없고, Release 리허설 직전에만 필요하다. 그 전까지는 "운영 준비 완료"로 표시하지 않는다.

### 3. 결과를 바꿀 수 있는 중요한 공백

- **plan.md의 Upstream 핀이 오래됨**: plan.md는 `spec.md@394651e`를 가리키지만, 실제 spec.md는 이후 개정(Q4·공개전/cleanup 구분 명확화, 후보 리비전 2d3f2dc)을 담고 있다. plan 스킬 자체가 "다운스트림 참조는 실제 기록된 업스트림 리비전으로만 repin"할 것을 요구하므로, 구현 착수 전에 이 핀을 실제 spec SHA로 정정해야 provenance가 맞다. 지금 읽은 spec.md 내용 자체는 최신이라 작업 내용에는 영향 없지만, 기록 정확성 문제로 남겨둘 수 없다.
- **정책 스킬 적용 이력이 "none"**: spec.md의 Skills applied가 "none — 고정 연구자료 기반 합성 예시"로 명시돼 있다. 실제 제품에서 인수한다면, 조직에 실재하는 보안/브랜드/UX 정책 스킬 목록을 spec-policy-pass 절차대로 확인하고 실제 적용 여부를 기록해야 하며, 이 합성 예시는 그 실제 확인을 대신하지 않는다. 실제 정책이 있다면 요구/AC가 달라질 수 있다.
- **GIT-WORKFLOW.md, RELEASE-CONTROL.md 미독**: plan/spec이 이 두 문서를 정본으로 링크하지만 이번 인계 범위에서는 읽지 않았다. 첫 브랜치/커밋/설정 변경 전에 실제로 읽어 SHA·결정권자·사유 기록 방식과 공개/중단 절차 세부를 확인해야 한다.

이 답변은 문서 검토에 근거한 것이며, 실제 명령 실행이나 제품 승인은 하지 않았다.
