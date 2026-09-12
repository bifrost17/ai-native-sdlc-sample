# Plan: 내 신청 API를 준비하고 화면을 연결해 한 번 공개
Upstream: spec.md@394651e. Status: draft.
Current change: 함께 개정한 spec의 Q4·운영 기록 위치와 공개 전 AC1–7/cleanup AC8의 구분을 함께 읽는다.

[spec](spec.md)의 본인 조회·서버 공개 판단을 먼저 준비하고, 같은 API에 포털을 연결한다.
[현재 계약·명령·입력 데이터](context.md)가 필수 입력이다. 합성 설계로, 아래 추가 시험과 제품 파일은 실제로 작성/실행되지 않았다.

## Files that change

| PR | 경로 | 역할 |
|---|---|---|
| A | src/server/routes/my-requests.ts (new), src/server/app.ts | 인증/제어 뒤 본인 행만 반환하는 API 등록 |
| A | src/server/routes/session.ts, config/features.json | 동일한 서버 판단의 bool 전달·일반 OFF 설정 |
| A | tests/server/my-requests.test.ts (new), tests/server/session.test.ts, docs/api.md (new) | 정확한 API·권한·공개 계약과 사용 설명 |
| B | src/web/PortalShell.tsx, src/web/MyRequestsPanel.tsx (new) | 세션 bool 기반 탐색·화면 상태·조회/취소 |
| B | tests/web/my-requests.test.tsx (new), tests/e2e/my-requests.spec.ts (new), docs/user-guide.md (new) | 화면 상태·실제 서버 사용 흐름·안내 |
| B | docs/operations.md (new), docs/operations-log.md (new) | Q4 명령·공개/중단 절차, 실행 시 채울 결정/관측 위치 |
| cleanup | 위 UI/서버 연결점·제어 설정·관련 시험/설명 | 최종 본인 조회 유지·임시 release 조건만 제거 |

읽기 기준: src/server/auth.ts, features.ts, request-store.ts, src/web/App.tsx·api.ts와 기존 portal/requests 시험.
주어진 연결점으로 충분하지 않으면 실제 코드 확인 근거와 영향받는 spec/plan을 관련 변경에 함께 반영한다.
임의의 새 인증/상태관리 체계를 만들지 않는다.

## Order of work

검증 방식: **혼합**. PR-A의 본인 데이터·서버 제어는 TDD로 권한 경계를 먼저 고정한다.
PR-B의 화면은 spec UI states와 확정 API를 기준으로 동작별 구현 후 테스트를 선택한다.
기존 포털 시험은 회귀로 활용하고 새 전체 사용자 흐름은 실서버 e2e로 추가 검증한다.
각 기대는 spec/독립 입력에서 가져오며 화면 구현의 실제 출력에 맞춰 만들지 않는다.

### Delivery map

| PR/단계 | 선행·목적 | 머지 후 일반/시험 동작 | 남은 일 |
|---|---|---|---|
| A | 최신 main. 조회 API/세션 판단 준비 | 기존 포털 그대로. 일반 OFF; 시험 u1은 API 조회만 가능. UI는 아직 없음 | 화면·전체 사용자 흐름·일반 공개 |
| B | A가 main에 통합된 뒤 최신 main | 일반 OFF; 시험 u1은 화면+API 전체 사용. 기존 폼 유지 | Q4와 리허설·공개 결정/운영 적용 |
| 공개/중단 | B의 전체 흐름/회귀와 Q4 확정 | 같은 완성 코드에서 설정/재시작으로 대상 변경 | 안정화·중단 관측·구버전 의존 확인 |
| cleanup | 위 관측 후 오너 정리 요청 | 인증한 모든 사용자가 본인 조회, 임시 flag 없음 | 배포 확인 후 남은 설정 정리 |

기본은 A→B 순차다. B는 A의 새 API/세션 계약에 의존하므로 파일이 다르다는 이유로 독립 구현이라고 부르지 않는다.
각 PR은 짧은 작업 branch/worktree에서 코드·시험·설명을 같이 검토한다. 작업마다 PR/커밋을 만들지는 않는다.

### PR-A: server-owned self view

**기준:** context의 기존 서버/화면 계약을 읽고 `npm run test:unit`, `npm run build`를 확인한다.
같은 PR의 기준 결과를 재사용한다. 시험 설정/데이터는 각각 별도 사본이다.

**A1 — 인증된 본인 조회.** spec API 우선순위·투영/정렬 계약(AC1–3)이 입력이다.
Files: 새 tests/server/my-requests.test.ts, 새 routes/my-requests.ts와 app.ts.

1. 먼저 `returns_only_current_users_rows`에서 시험 u1 세션과 ON 설정으로 GET /api/my-requests를 호출한다.
   spec의 정확한 두 행·필드·순서를 200으로 기대한다. `npm run test:unit -- tests/server/my-requests.test.ts`의
   예상 RED는 미등록 경로의 404다. 기존 인증/fixture 실패는 그 동작의 RED로 보고하지 않는다.
2. 기존 auth/featureEnabled/readRequests에 최소 연결해 통과시킨다. 이어 미로그인401, OFF404,
   쿼리400, u3 빈 목록, 같은 시각 정렬, 저장소 실패503을 작은 행동별로 시험 먼저 추가/실행하고 구현한다.
   이미 통과하는 인접 회귀는 그대로 보존한다. 응답만 검사하지 않고 거부 시 readRequests 호출 없음과 데이터 불변도 확인한다.
3. 같은 파일의 focused 시험이 AC1–3과 서버 실패 계약을 만족하면 완료다. 출력에 internalNote/requesterId가 없는지도 검사한다.

**A2 — 세션과 직접 API의 같은 제어.** Files: session.ts, config/features.json, session.test.ts, docs/api.md.

1. `session_exposes_effective_flag_only`에서 시험 u1의 features.myRequests=true, 일반 u2=false를 기대하는
   시험을 먼저 추가한다. `npm run test:unit -- tests/server/session.test.ts`의 예상 RED는 새 bool 부재다.
2. 같은 featureEnabled 호출로 bool만 추가한다. 기본 설정은 enabled=false/testUsers=[]로 두고, 시험은 사본에 u1을 지정한다.
   누락/잘못된 설정/평가 오류의 OFF, 위조 쿼리·브라우저 값이 서버 권한을 바꾸지 않음을 먼저 시험하고 필요한 연결만 수정한다.
3. focused 시험과 A1을 함께 확인하고 API 문서를 갱신한다. 시험 u1의 API 성공은 화면 완료 증거가 아니다.

PR-A 끝에는 필요한 정리 후 전체 unit/build와 기존 `npm run test:e2e -- tests/e2e/portal.spec.ts`를 최신 main 결합 판에서 확인한다.
검토/머지 뒤 통합 main에서도 같은 범위의 결과를 확인한다. 새 화면을 보이는 수정은 이 PR에 없다.

### PR-B: observable UI states and real flow

A가 main에 들어간 판에서 시작한다. API/세션 정본과 기존 PortalShell의 화면 전환·세션 만료 처리를 읽는다.

**B1 — 열기·로딩·결과/실패.** Files: PortalShell.tsx, 새 MyRequestsPanel.tsx·tests/web/my-requests.test.tsx.

1. 시험 세션의 myRequests=true에서 “내 신청” 탐색과 loading 패널을 연결한다. 곧바로 키보드 열기·loading을
   보는 `opens_and_loads_my_requests`를 추가하고 `npm run test:unit -- tests/web/my-requests.test.tsx`로 검증한다.
2. 정확한 두 행/상태 라벨, empty, error→재시도 한 요청→success를 한 동작씩 구현한다. 각 동작 직후 응답을 통제하는
   화면 시험을 추가·실행해 spec UI states와 대조한 뒤 다음으로 진행한다.
   기존 getJson을 사용하고 UI 자체 소유자 필터·별도 feature 설정은 만들지 않는다. title HTML 문자열은 텍스트로 표시한다.
3. 세션 OFF에서 버튼/조회 없음, 401 세션 정리, 404 패널/버튼 닫기, 닫은 뒤/로그아웃 뒤 늦은 응답 무시를
   각각 연결한 직후 검증한다. 취소와 응답 무시를 포함하며 role/이름/aria 상태도 같은 focused 명령으로 검사한다.
4. 같은 focused 시험으로 spec의 UI states와 AC4–6이 관측되면 작업 완료다. DOM 모의 시험은 서버 권한 증거가 아니다.

**B2 — 실제 서버에 연결한 사용 흐름.** Files: 새 tests/e2e/my-requests.spec.ts, docs/user-guide.md·운영 문서.

1. B1 구현 뒤 실제 시험 앱/세션/저장소 사본에서 u1이 목록을 보고 u2가 새 기능을 사용할 수 없다는 브라우저 시험을 추가한다.
   `npm run test:e2e -- tests/e2e/my-requests.spec.ts`로 실행한다. 독립 spec의 기대와 대조한 통합 검증으로 기록하며 RED를 만들지 않는다.
2. 실제 API 응답과 화면의 REQ-11/REQ-12를 함께 확인한다. 이 성공 경로에서는 API 응답을 intercept해 가짜 성공으로 바꾸지 않는다.
   지연/네트워크 오류는 별도 제어 시험으로 표시하고, 실서버 성공/권한 근거와 구별한다.
3. 키보드 열기·읽기·기존 신청 화면 복귀·로그아웃을 확인하고, 오류 안내/좁은 화면의 표 읽기를 브라우저로 살핀다.
   실제 발견이 계약/계획을 바꾸면 영향 문서와 같은 구현 커밋에 반영한다. 스크린샷 하나만으로 사용 흐름을 통과시키지 않는다.
4. 운영 담당과 spec Q4를 docs/operations.md에 확정한다. 미확인인 동안 코드 인계 제한은 표시하고 운영 준비 완료라고 쓰지 않는다.
   docs/operations-log.md는 실제 실행 때 판·설정·담당·결정·관측을 남길 위치이며 성공 행을 미리 채우지 않는다.

PR-B 끝에는 전체 unit/e2e/build를 최신 main 결합 판에서 확인한 뒤 검토/머지하고, 통합 main 결과를 확인한다.
일반 OFF와 기존 기능 유지, 시험 ON의 전체 목록 흐름이 함께 필요하다.

### Release, disable and cleanup

Q4가 정한 명령과 격리한 설정 사본으로 일반 OFF→u1 시험→전체 ON→OFF를 같은 완성 판에서 리허설한다.
각 재시작 이후 API·새로 열린 포털을 확인하고, 기존 열린 화면에는 spec이 명시한 전파 한계가 있음을 관측한다.
기존 포털 회귀도 확인한다. 통합 검증의 유효한 같은 판 근거는 재사용하되 코드/설정이 바뀌면 영향 검증을 갱신한다.

포털 오너가 전체 범위/근거를 확인해 공개 여부를 정하고 운영 담당이 같은 방법으로 실제 환경 설정을 적용한다.
리허설과 실제 운영 관측을 docs/operations-log.md에서 구분한다. 실패하면 OFF/재시작 후 기존 기능을 확인한다.
조회 기능이므로 취소할 새 쓰기·이행은 없으며, 이미 내려받은 데이터는 OFF로 원격 삭제되지 않는다.

cleanup은 오너 요청과 안정화/중단·구버전 의존 해소 뒤 시작한다. 이 작업은 공개 계약 교체를 명확히 검증하려 TDD를 선택한다.
설정 없이 로그인한 u2도 본인 목록을 볼 수 있는
최종 계약 시험을 먼저 실행한다(기존 OFF404가 예상 RED). 임시 gate만 제거해 통과시키고 인증·본인 필터·화면 회귀를 유지한다.
이전 OFF/시험대상 전용 시험은 폐기한 계약이라 spec/plan/시험을 함께 갱신하며 제거 이유를 남긴다.
코드/시험/설명을 배포한 뒤 잔여 설정을 정리한다. 현재 공개/cleanup은 예정이며 미실행이다.

## Risks

가장 중요한 위험은 브라우저 표시 제어를 서버 권한으로 오인하거나 다른 사용자의 행/내부 메모를 내려보내는 것이다.
A1/A2 실서버 시험이 이를 구별한다. 세션 만료/늦은 응답은 B1, 실제 조합은 B2에서 확인한다.
조회 실패를 빈 상태로 보이면 직원이 신청이 사라졌다고 이해하므로 error와 empty는 같은 결과로 취급하지 않는다.
OFF의 즉시 화면 삭제를 약속하지 않는다. 설정/재시작이 불명확하면 해당 운영 실행을 보류하고 Q4를 확인한다.

## Proof

| ID·연결 | 작업/시험 정본 | 증명과 한계 |
|---|---|---|
| P-A AC1–3/R2/R4 | A1/A2 focused 서버 시험 + 기존 requests/session 회귀 | 본인 투영·거부·무쓰기·같은 제어. 화면/실환경 배포 증거는 아님 |
| P-B AC4–6 | B1 focused 화면 시험 | 로딩/빈/오류/재시도/401/404/늦은 응답·키보드. 모의 API라 서버 권한 증거는 아님 |
| P-C AC1/3/6/R4 | B2 실서버 e2e와 기존 portal 흐름 | 실제 세션→API→화면·기존 기능. 오류 주입 시험은 따로 표시 |
| P-I 전체/통합 | npm run test:unit; npm run test:e2e; npm run build | B의 최신 main 결합 및 통합 main, 코드판/설정과 결과 기록 |
| P-R AC7 | Release 절의 Q4 명령·설정별 API/브라우저 관측 | 전체 공개/중단 및 전파 한계. 로컬 리허설과 운영 관측은 별개 |
| P-F AC8 | cleanup의 최종 무설정 계약·전체 회귀 | 임시 gate만 제거, 인증/본인 데이터와 기존 기능 유지 |

각 작업의 명령·기대 정본을 위에 두었다. 선택한 순서·판·출력·미확인은 PR/실행 기록에 남긴다.
TDD 작업은 실제 실패/통과 이유를 기록하고, B1/B2의 사후 시험은 TDD 이력으로 소급하지 않는다.
경로·작업·검증이 바뀌면 plan, 계약/공개 의미가 바뀌면 spec의 해당 정본도 관련 구현 커밋에서 갱신한다.
관련 없는 문서를 형식적으로 수정하거나 실제 성공을 계획에 미리 기록하지 않는다.
