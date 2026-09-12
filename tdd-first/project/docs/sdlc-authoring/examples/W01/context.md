# W01: 사내 포털의 내 신청 조회 — 작성 입력

> 활성 교육 사본. 원본 경로: `docs/research/sdlc-documentation/spec-plan-design/candidate/examples/W01/`; source commit: `2d3f2dc`.
> 문서의 `Upstream` SHA는 제작 당시 원본 배치를 가리키며, 이 이동 경로나 제품 수락을 뜻하지 않는다.

합성 사례이며 제품 코드/실행 결과는 없다. 아래 경로·기존 계약·명령은 교육용으로 주어진 기준이다.
이를 실제 제품에 적용할 때에는 코드를 읽고 경로와 시험 명령을 확인한다. 이 파일은 W01의 현재 계약 정본이며 과거 자료를 찾아갈 필요가 없다.

## Current system

같은 출처에서 React/TypeScript 포털과 Node/TypeScript API를 제공하는 작은 사내 서비스다.
직원은 포털에서 신청서를 제출하지만, 처리 상태는 담당자에게 별도로 물어야 한다. 담당자의 기존 관리 화면은 그대로 유지한다.
이번 사용자는 신청자 본인이다. 동료 신청을 볼 수 있는 운영자 권한을 새 목록에 자동 적용하지 않는다.

| 기존 파일 | 주어진 역할/계약 |
|---|---|
| src/server/app.ts | Express 라우트 등록. 미등록 경로는 404 JSON {error:"not_found"} |
| src/server/auth.ts | requireUser 미들웨어. 유효한 서버 세션이면 req.user={id,name}; 아니면 401 {error:"unauthenticated"}, 다음 핸들러 실행 안 함 |
| src/server/routes/session.ts | GET /api/session: requireUser 뒤 200 {user:{id,name},features:{}}. Cache-Control: no-store. feature bool 필드 추가를 기존 소비자가 허용 |
| src/server/features.ts | featureEnabled(name,userId): 아래 설정을 읽는 기존 서버 판단. 클라이언트 쿼리/쿠키를 시험 대상 근거로 사용하지 않음 |
| config/features.json | 시작 때 읽는 feature 설정. 재시작해야 반영. 테스트는 별도 설정 사본을 사용 |
| src/server/request-store.ts | readRequests(): Promise<Request[]> — 일관된 조회 사본. 실패는 reject. 기존 제출/관리 쓰기 경로도 이 저장소를 쓰지만 이번 변경은 읽기만 함 |
| src/web/App.tsx, PortalShell.tsx | /portal의 기존 신청 폼·로그인/로그아웃. 시작 시 /api/session을 읽음. 세션을 잃으면 화면 데이터를 비우고 기존 로그인 화면으로 전환 |
| src/web/api.ts | getJson(path,{signal}): 같은 출처 세션 요청, 10초 timeout. 비2xx는 status를 가진 HttpError, 네트워크/timeout은 오류. JSON 타입 판정은 소비자 책임 |
| tests/server/session.test.ts, requests.test.ts | 세션401/200 및 기존 제출/관리 권한·데이터 계약 시험 |
| tests/web/portal.test.tsx, tests/e2e/portal.spec.ts | 기존 폼·로그인/로그아웃 및 브라우저 사용 흐름 시험 |

Feature 설정 값은 `{enabled:boolean,testUsers:string[]}`이다. enabled=true면 모든 인증 사용자 ON,
false면 testUsers의 정확한 사용자 ID만 ON이다. 키 누락·객체/필드 타입 오류·읽기/평가 오류는 해당 기능 OFF.
알 수 없는 기능 이름은 OFF. 기본 설정은 `{}`이며 이번 기능의 키는 아직 없다. 브라우저에는 최종 bool만 전달한다.
이는 W01 입력에 이미 있는 경량 기능 제어이며 새 플래그 플랫폼을 구현하라는 요구가 아니다.

Request = `{id:string,requesterId:string,title:string,status:"open"|"in_progress"|"done",updatedAt:string,internalNote:string}`.
id는 고유, updatedAt은 고정 폭 UTC ISO 문자열(예: 2026-09-01T09:00:00Z), status는 세 값만 있다.
직원당 최대 100건인 현재 범위로 페이지/검색/상세 화면은 요구하지 않는다. 소유자 requesterId는 이번 변경으로 바뀌지 않는다.
title은 일반 텍스트이며 HTML로 해석하지 않는다. 기존 내부 메모는 신청자에게 공개하지 않는다.

## Dataset

각 시험은 새 사본을 사용한다. 행 순서는 아래와 같아 정렬 구현을 구별할 수 있다.

| id | requesterId | title | status | updatedAt | internalNote |
|---|---|---|---|---|---|
| REQ-12 | u1 | 모니터 신청 | done | 2026-09-01T09:00:00Z | 합성 내부 메모 A |
| REQ-13 | u2 | 계정 신청 | in_progress | 2026-09-03T09:00:00Z | 합성 내부 메모 B |
| REQ-11 | u1 | 키보드 신청 | open | 2026-09-02T09:00:00Z | 합성 내부 메모 C |

u1=하나, u2=민, u3=솔이라는 가상 직원 계정이 있다. u3의 신청은 없다. 테스트용 로그인/session fixture를 제공한다.
권한·응답 검증에는 실제 테스트 API와 저장소 사본을 사용하고, 화면 상태 시험에서만 응답/지연을 제어할 수 있다.

## Commands

주어진 package scripts는 `npm run test:unit -- <test-path>`(Vitest, 서버/DOM 환경은 파일별 설정),
`npm run test:unit`(전체), `npm run test:e2e -- <test-path>`(Playwright, 격리된 앱/시험 계정을 시작),
`npm run build`다. 예시에 추가한 파일/테스트는 아직 없으며 어떤 명령도 이번 설계 작업에서 실행됐다고 주장하지 않는다.

## Owner answers and authorization

- Q1: 본인이 제출한 건만. 완료 건도 포함. 최근 갱신순, 같은 시각이면 id 오름차순. 운영자여도 이 목록은 본인 것만.
- Q2: 실패는 빈 목록으로 보이지 않게 하고 수동 재시도. 새로고침 때 다시 읽으면 충분, 자동 polling/실시간 갱신 없음.
- Q3: API와 화면이 한 공개 단위. 개발 중 u1만 시험, 일반 사용자 OFF. 포털 오너가 전체 흐름을 확인한 뒤 공개하고 운영 담당이 설정/재시작을 수행.

원 합성 요청은 [intent](intent.md)의 문장 그대로다. 이 답과 기술 선택은 root가 예시 작성을 위해 만든 자료이며
실제 직원 인터뷰·제품 승인·운영 관측이 아니다. 사용자는 2026-09-11 재검토대로 설계 패키지를 보완하도록 허가했다.
운영 설정 변경/실험 제품 구현은 이 예시의 실행 성공에 포함되지 않는다.
