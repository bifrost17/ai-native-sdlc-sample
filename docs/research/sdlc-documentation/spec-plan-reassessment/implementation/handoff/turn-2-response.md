## 1. 근거 자료 재확인 후 이전 판단 정정

`execution-blocks.md`에 명시된 규칙을 다시 인용하면:

> "기존 plan이 spec@A를 참조하는 상황에서 한 구현 커밋에 spec과 plan을 고치면 그 미래 SHA를 쓸 수 없다. 이때 기존 Upstream A를 보존하고 바로 아래에 `Current change: 이 커밋의 spec.md 및 선언된 설계 정본 개정과 함께 읽는다...`처럼 현재 변경을 명시한다. 커밋 후 다음 갱신/인계에서 확정된 실제 SHA를 참조할 수 있다. 존재하지 않는 해시나 '승인됨' 표기로 해결하지 않는다."

W01 plan.md는 정확히 이 패턴을 따르고 있다: `Upstream: spec.md@394651e`(직전 수락 판)를 보존한 채, 바로 아래 `Current change: 함께 개정한 spec의 Q4·운영 기록 위치와 공개 전 AC1–7/cleanup AC8의 구분을 함께 읽는다`로 같은 커밋에서 함께 바뀐 spec 변경을 명시하고 있다. GIT-WORKFLOW.md도 "상위 문서의 수락 판이 바뀌면 그 커밋과 결정을 먼저 남기고 하위 문서의 Upstream을 갱신한다"고 해서, **다음 갱신/인계 시점**에 실제 SHA로 repin하는 것을 정상 흐름으로 규정한다.

즉 이전에 제가 "plan의 Upstream 핀이 오래됐다"를 즉시 고쳐야 할 결함으로 지적한 것은 틀렸다. 이는 문서 스스로 미래 커밋 해시를 쓸 수 없다는 제약 때문에 의도적으로 택한 표기 방식이며, 지금 시점에서는 결함이 아니라 "다음 인계 때 확정 SHA로 repin"이라는 후속 액션 항목으로만 남겨두면 된다. 정정 감사한다.

### 처음 작업의 기준 확인 → 머지 전 결합 확인 → 머지 후 확인 (전체 순서)

**착수 전**
1. 작업 브랜치는 최신 `main`에서 `codex/<목적>` 형태로 생성한다(GIT-WORKFLOW.md).
2. spec.md/plan.md의 `Status: draft`와 Upstream/Current change를 확인해, 이미 허가된 초안 범위(context.md의 "2026-09-11 재검토대로 설계 패키지 보완 허가")인지 재확인하고 같은 질문을 다시 승인받지 않는다.

**PR-A 기준 확인 (plan.md A1 "기준" 절)**
3. context의 기존 서버/화면 계약(`src/server/auth.ts`, `features.ts`, `request-store.ts`, `session.ts`, `app.ts`)을 실제로 읽는다.
4. 코드 변경 전 `npm run test:unit`, `npm run build`를 현재 `main`에서 실행해 기준 결과를 확보한다 — 이 결과를 A1/A2가 공유해서 재사용한다.

**A1/A2 구현 (테스트 우선)**
5. `tests/server/my-requests.test.ts::returns_only_current_users_rows` 작성 → `npm run test:unit -- tests/server/my-requests.test.ts` → 기대 RED: 404(라우트 미등록).
6. 최소 라우트 연결로 GREEN 확인 후, 401/404(OFF)/400(쿼리)/u3 빈 목록/동률 정렬/503을 각각 시험 먼저 추가.
7. `tests/server/session.test.ts::session_exposes_effective_flag_only` 추가 → 기대 RED: bool 필드 부재 → 구현 → 위조 쿼리/쿠키가 서버 판단을 바꾸지 않음도 확인.
8. `docs/api.md` 갱신.

**머지 전 결합 확인**
9. 브랜치를 최신 `main`과 합친 판에서 `npm run test:unit`(전체), `npm run build`, 기존 `npm run test:e2e -- tests/e2e/portal.spec.ts` 회귀를 실행한다(GIT-WORKFLOW.md: "머지 전에는 최신 main과 합쳐진 결과에서 관련 검사와 인접 동작을 확인한다").
10. 필요하면 Draft PR을 열어 범위·의존 PR(B는 A 의존)·검증 근거·미확인 사항(Q4 등)을 남긴다.
11. REVIEW.md에 따른 검토, 발견 수정 후 재검증. 그 사이 main이 바뀌었으면 결합 결과를 다시 확인한다.

**머지**
12. 기본 merge commit으로 통합(Upstream SHA 이력 보존 목적).

**머지 후**
13. 통합된 `main`에서 같은 범위 결과를 다시 확인한다.
14. 완료된 브랜치/worktree 정리, PR·커밋·결정 기록 보존.
15. 다음 인계/갱신 시점에 plan.md의 Upstream을 spec.md의 실제 확정 SHA로 repin한다(지금 당장의 결함이 아니라 이 시점의 정상 작업).

---

## 2. 후속 요청: PR-A 머지 후 "보는 중에도 수동 새로고침" 요청

### 상황 재확인
u1은 API 조회만 가능(`enabled:false, testUsers:["u1"]`), UI는 아직 없음(PR-B 미착수). u2는 여전히 404(시험 대상 아님). 일반 공개는 미결정.

### 제안하는 기본 UI 동작
자동 polling 없이, **success/empty 상태에서도** 명시적 "새로고침" 버튼을 노출해 클릭 시 같은 `GET /api/my-requests`를 한 번 재호출한다. 기존 규칙을 그대로 재사용한다:
- 새 요청 진행 중에는 loading 상태로 전이(기존 loading 화면 재사용).
- 이전 진행 중 요청이 있으면 취소(AbortSignal)하고 최신 클릭만 반영 — 기존 "패널 닫기/로그아웃 시 늦은 응답 무시" 로직과 동일 원리.
- 실패 시 기존 error 상태(재시도 버튼)로 전이, 이전 목록은 비움 — AC4 로직 재사용.
- API 계약·정렬·필드·인증/권한 판단은 전혀 바꾸지 않는다(자동 polling 아님, 클라이언트 트리거만 추가).

이 방식이 "API 본인 조회 계약 그대로", "자동 polling 아님"이라는 사용자 요구를 모두 만족하면서 기존 설계에 새 개념을 추가하지 않는다.

### 무엇을 고쳐야 하나

**spec.md**
- Requirements: 새 R을 추가하거나 R3을 일반화한다 — 현재 R3("로딩·빈 결과·오류를 구분. 오류 때 사용자가 다시 시도할 수 있음")는 재시도를 오류 상태에 한정하므로, "성공/빈 상태에서도 사용자가 수동으로 다시 조회할 수 있음"을 명시적으로 추가해야 한다.
- Acceptance criteria: 새 AC(예: success/empty에서 새로고침 클릭 → loading → 최신 결과, 중복 클릭 시 마지막 요청만 반영) 추가. 기존 AC1–8은 그대로 둔다.
- Design/UI states 표: success·empty 행에 새로고침 버튼/트리거를 추가하고, 중복 요청 취소 규칙을 명시. 자동 polling 금지 문구("같은 화면을 보고 있을 때 자동 polling·주기 갱신·임의 중복 요청은 없다")는 유지하고 "사용자 트리거는 예외"임을 명확히 한다.
- Release 절/API/Constraints and scope: 변경 없음(별도 플래그·새 엔드포인트 불필요).

**plan.md**
- PR-B B1 절만 갱신한다. 첫 시험에 새 케이스 추가, 예: `tests/web/my-requests.test.tsx::manual_refresh_updates_list_without_polling`, 기대 RED는 새로고침 버튼/핸들러 부재. 기존 `opens_and_loads_my_requests` 등 나머지 순서는 그대로 두고 이어서 배치한다.
- Files/Proof 표에 새 AC 연결 항목 추가. PR-A 파일 목록(server 쪽)은 변경 없음 — 이미 머지됐고 API 계약이 그대로이므로 재작업 불필요.
- Current change로 "spec.md의 새로고침 AC/Design 추가"를 함께 표기(PR-A 이후 커밋이라 plan Upstream은 실제 PR-A 머지 SHA로 갱신하고, 이번 spec 변경은 같은 구현 커밋의 Current change로 남긴다).

**그대로 둘 것**
- API 라우트/응답 스키마/우선순위(401/404/400/503/200), 정렬 규칙, feature flag 이름과 값 형식, R1/R2/R4/R5, 401/404/close-logout 관련 AC, PR-A의 이미 머지된 코드/시험.

### 현재 u1/u2 가능 동작 및 공개/cleanup 판단
- u1: API 직접 호출로 본인 목록 조회 가능(200). 화면 자체가 아직 없어 새로고침 버튼도 존재하지 않음 — 이번 변경은 PR-B(B1) 안에 접어넣어 처음부터 반영한다.
- u2: 여전히 404(시험 대상 아님), 이번 요청과 무관.
- 일반 공개(enabled:true)는 이 요청으로 앞당겨지지 않는다. RELEASE-CONTROL.md대로 여전히 "PR-B 전체 완성 + 포털 오너의 AC 확인" 이후 결정된다.
- cleanup 시점(AC8)도 변화 없음 — 새로고침은 임시 release 조건이 아니라 최종 계약에 포함되는 정상 기능이므로, cleanup에서 게이트만 제거하고 이 동작은 유지한다.

이 답변은 가정 시나리오에 대한 인계 설명이며, 실제 spec/plan/제품 파일은 수정하지 않았다.
