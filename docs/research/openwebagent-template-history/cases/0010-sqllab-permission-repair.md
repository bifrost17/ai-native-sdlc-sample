# 0010 SQL Lab 권한 수리 — 기존 설계 계약 복구와 남은 훅

판정: **범위를 한정한 심층 검토 완료**. bare Git `main@a08295f`, 초기·최종 intent/spec/plan, [#329](https://github.com/bifrost17/openwebagent/pull/329)·[#332](https://github.com/bifrost17/openwebagent/pull/332)·[#333](https://github.com/bifrost17/openwebagent/pull/333)·[#334](https://github.com/bifrost17/openwebagent/pull/334), 선택한 구현·시험 파일을 대조했다. plan의 실서버·격리 복제 인스턴스 수치와 red/green은 **당시 기록**이며 이번 조사에서 재실행하지 않았다.

## 사건 사슬

| 단계 | 관측과 출처 | 해석 |
|---|---|---|
| 요청·초기 설계, 9/22 | 0003 머지·`:3080` 배포 뒤 권한 심층 점검 요청. 결과를 이식 중 잃은 검사, 권한 부여 불가, rison 목록 계약 미배선으로 나눴다. `228c708`이 intent/spec/plan을 **한 커밋**에 도입했다. [초기 intent](https://github.com/bifrost17/openwebagent/blob/228c708cbf53618052b4434fab2440790a3d26b5/intent/0010-sqllab-permission-repair/intent.md#L4-L56), [초기 spec](https://github.com/bifrost17/openwebagent/blob/228c708cbf53618052b4434fab2440790a3d26b5/intent/0010-sqllab-permission-repair/spec.md#L16-L33). | 문서 세 개의 내부 작성 순서는 증명되지 않는다. 결함은 대체로 0003의 **기존 수락 요구/설계 미구현**이지 새 권한 요구가 아니다. |
| 안전 우선, 9/22 | 요청자 Q3 결정으로 권한 노출 위험을 먼저 분리. plan `3a2031f`가 T00 권한 행렬·독립 기대·원인 되돌림 확인을 구체화했다. #329(T00–T03)가 CSV 캐시 접근 판정, 테이블 술어 3갈래, 잘못 채워진 역할 구성원 칸을 다뤘다. [plan:22–80](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0010-sqllab-permission-repair/plan.md#L22-L80). | PR-1은 뒤의 부여 UI를 기다리지 않게 했다. |
| 계약·부여, 9/22 | #332(T04–T06)는 목록 필터/정렬·역할 오류·내장 역할 가드, #333(T07–T09)은 권한 목록 500·역할 id null·PVM 생성/백필을 다뤘다. main의 `security.py`에는 `apply_column_filters`·`apply_order` 배선이 있고 권한 행렬 시험 파일도 있다. [라우터](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/apps/open-webui/backend/open_webui/routers/sqllab/security.py#L254), [행렬 시험](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/apps/open-webui/backend/open_webui/tests/sqllab/test_sqllab_permission_matrix.py#L1). | 계약 배선·시험 존재는 확인. 실제 모든 역할/엔진의 접근 수락과 같지 않다. |
| 마무리, 9/23 | #334(T10–T12)는 권한 필터 **뒤** 시맨틱 절단, 표시 라벨, C20 게이트와 0003 문서 정정을 다뤘다. plan은 외부 엔진에 보내는 번들, `limit=1` 경합, 게이트의 진짜 우회 양성 대조를 기록한다. [plan:350–476](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0010-sqllab-permission-repair/plan.md#L350-L476). | 모의 엔진이 번들만 보고 답하게 고친 과정은 원인 재현 시험의 판별력을 높였다. |

## 원인과 네 가설

**H1·H3 지지, 단 원인은 구별된다.** 0003 SP06은 캐시에서 새 노출 게이트만 빼는 뜻이었으나 원본 접근 판정까지 빠졌다. SP07의 데이터 소스 권한 생성·데이터셋 수정 훅은 설계에는 있었고 구현 경로 사이에서 누락됐다. 역할 목록 API는 이미 있던 공용 필터 헬퍼를 부르지 않아 화면에 전체 구성원이 채워졌다. 같은 이름의 SQL Lab 권한 기능이라도 **요구 누락**, **설계 문장 해석 오류**, **모듈 연결 누락**이 각각 다르다. [intent:13–56](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0010-sqllab-permission-repair/intent.md#L13-L56), [spec FR01–FR07](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0010-sqllab-permission-repair/spec.md#L20-L27).

**H4 지지.** 기존 시험은 CSV의 캐시 없는 갈래, 시맨틱 검색의 권한 0명, 테이블 술어의 `schema='public'`만 재서 실제 빠진 분기에 닿지 않았다. 새 plan은 권한 행렬의 사용자·역할·PVM을 실제 HTTP 경계에 세우고, 각 T의 독립 기대 출처와 되돌림 계기를 적었다. 이는 수립 시 검증 설계가 더 구체적이었다는 문서 증거이며, 이번 조사에서 그 시험을 실행해 PASS를 확인한 증거는 아니다. [plan V0–V4](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0010-sqllab-permission-repair/plan.md#L486-L576). H2는 라벨 표시의 사용자 이해 문제에는 해당하지만 시각 심미성 근거는 없다.

**남은 범위:** AC06의 데이터셋 수정 후 권한 문자열 재계산(FR03)은 spec에 있고 plan V6에 시험 이름까지 적혔으나, T01–T12 중 담당 작업이 없어 구현되지 않았다고 최종 plan이 직접 기록한다. 이를 #334의 완료나 문서 정정으로 닫지 않는다. [spec AC06](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0010-sqllab-permission-repair/spec.md#L50), [plan:449–452](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0010-sqllab-permission-repair/plan.md#L449-L452). 따라서 전 범위 AC 통과 판정은 불가하다.

여섯 축 판정:

- 의도 보존: 0003 요구와 잔여 위험의 범위를 유지하려는 결정이 명시됐다.
- 설계 충실성: 대부분 기존 0003 SP의 구현 누락을 추적했으나 FR03은 남았다.
- 계획 실행성: T00·T01–T12는 구체적이나 AC06의 담당 T가 비었다.
- PR/병렬 분할: 안전 복구를 먼저 내고 부여·표시를 뒤에 둔 순서가 Git에서 확인된다.
- 변경 피드백: 실제 결함·시험 판별력에 따라 plan이 여러 번 갱신됐다.
- 검증·보고: 시험·격리 복제 실증 주장은 상세하나 이번 조사의 독립 실행 증명은 아니다.

현행 0.1.8 정본과 기존 5개 WIP는 [기준](../baseline.md)처럼 SP→T→파일·방법·기대·검증, 공유 경계, 이탈 갱신, 실제 통합판과 미실행 구분을 이미 요구한다. 이 사건은 특히 **AC가 작업·인도에서 빠졌는지 끝에 대조하는 실행/리뷰 문제**로 남는다. 새 역할별 권한 규칙을 템플릿에 이식할 근거는 없다. 원래 사용자 대화·감사 원문 전체·실서버 로그·브라우저 화면·마이그레이션 왕복은 이번 검토에서 독립 확인하지 않았다. `:3080` 기록을 현재 제품 전체 수락으로 확대하지 않는다.
