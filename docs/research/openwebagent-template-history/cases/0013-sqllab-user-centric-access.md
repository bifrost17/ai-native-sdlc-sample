# 0013 사람 기준 접근 보기·증감 저장 — 0012와 공유 경계

판정: **구현·문서의 범위를 한정한 심층 검토 완료**. `main@a08295f`의 초기/최종 intent·spec·plan, [#336](https://github.com/bifrost17/openwebagent/pull/336)–[#340](https://github.com/bifrost17/openwebagent/pull/340)의 머지 순서, 핵심 라우터·화면·시험 파일을 확인했다. 실행 로그·실사용 권한 화면은 다시 재현하지 않았다.

## 사건 사슬

| 단계 | 관측 | 해석 |
|---|---|---|
| 새 요구, 9/23 | 0010은 관리자에게 역할·권한 부여를, 0012는 **역할 기준 규모 관리**를 설계했다. 여기서는 사람의 직접·그룹·계산 역할 출처와 최종 권한을 한 화면에서 보고, 대상별 접근자와 접근 이유를 보며, 한 사람의 역할 변경을 **차이만 저장**하도록 요구했다. 요청자는 0012와 별건 진행에 동의했다. [intent:14–52,75–83](https://github.com/bifrost17/openwebagent/blob/65d1b03b0b064e70fb4b21efd82d1f3f7e710ec3/intent/0013-sqllab-user-centric-access/intent.md#L14-L52). | 0012 미완료를 그대로 다른 이름으로 반복한 건이 아니다. 역할 기준·사람 기준 조회 방향과 쓰기 표면이 다르다. |
| 설계·PR-0 | `65d1b03` #336에서 세 문서를 추가했다. AC는 직접/그룹/계산 출처, 두 DB의 동일 스키마 PVM, 샘플 허용·거부, 대상 전체와 스키마의 다른 접근자 집합, 동시 편집 보존, 관리 PVM 셋 중 둘만 가진 계정의 403을 구분한다. [spec AC01–16](https://github.com/bifrost17/openwebagent/blob/65d1b03b0b064e70fb4b21efd82d1f3f7e710ec3/intent/0013-sqllab-user-centric-access/spec.md#L20-L41). | 사용자 기대가 서버 판정·보이는 목록·편집 범위에 연결돼 있다. |
| 서버, 9/23 | 첫 부모 머지는 #337 `db0714e` 역할 출처·사용자 접근·판정 미리보기 → #339 `a6339b0` 사용자 역할 증감 → #338 `e4fe6c2` 대상 접근자 순이다. #338·#339는 생성 시각이 가까워도 **머지 순서가 반대**다. [main 이력](https://github.com/bifrost17/openwebagent/commits/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/), [plan 순서](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0013-sqllab-user-centric-access/plan.md#L24-L38). | PR-2·3 병렬과 0012 공유 함수 소유권을 계획했다. |
| 화면·후속 문서 | #340 `430fd0a`가 접근 보기·대상별 접근자 모달을 머지했다. main에는 `UserAccessModal`·`AccessHoldersModal`과 각 컴포넌트 시험, 서버의 `test_sqllab_{user_access,access_check,access_holders,user_role_delta}.py`가 있다. [화면 소비](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/apps/open-webui/src/lib/components/sqllab/security/UserRolesList.svelte#L41-L47), [서버 라우터](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/apps/open-webui/backend/open_webui/routers/sqllab/security.py#L670-L699). | plan 첫머리의 “PR-4 독립 검토 대기”는 **머지된 main보다 오래된 진행 요약**이다. 최종 문서가 자동으로 진행 상태를 증명하지 않는다. |

## 경계·검증

H1·H3에 대해 spec은 “최종 접근”을 역할이 주는 여섯 데이터 권한 목록으로 정하고 개별 테이블의 실제 판정은 **별도 미리보기**로 분리했다. 그룹 경유 역할은 출처만 읽고, 계산 역할은 편집하지 않으며, 관리 보기 API에는 기존 PVM 셋을 모두 요구한다. 대상별 목록은 SQL Lab 메타데이터 라우트의 기능 권한과 데이터 권한을 함께 본다. 이 구별을 생략하면 목록만 허용되고 실제 라우트는 거부하는 결합 오류가 난다. [spec FR/NFR](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0013-sqllab-user-centric-access/spec.md#L6-L18), [SP02–03](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0013-sqllab-user-centric-access/spec.md#L89-L154).

0012의 **역할 고정·사용자 집합 증감**과 0013의 **사용자 고정·역할 집합 증감**은 같은 `membership_delta` 함수를 쓰도록 했다. 0013 구현이 먼저라 공용 함수를 만들고 0012 plan이 재사용으로 갱신됐다. 기존 `PUT /users/{id}` 전부 교체는 남고 새 증감 경로는 편집 사이에 다른 관리자가 추가한 역할을 보존하는 AC12를 겨냥한다. 따라서 **새 PATCH끼리의 보존**과 **기존 PUT과의 경합 해결**을 혼동하지 않는다. [spec SP04](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0013-sqllab-user-centric-access/spec.md#L180-L204), [공용 함수](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/apps/open-webui/backend/open_webui/utils/sqllab/security/membership_delta.py#L85).

H4에 대한 계획상 대응은 독립 기대가 뚜렷하다. 같은 픽스처에서 미리보기와 실제 `table_detail`/`table_sample` 상태 코드를 대조하고, PVM 3개 중 2개만 주는 조합으로 관리 권한 403을 재며, 그룹 경유 역할과 계산 역할의 DB 원천을 변형하는 계기를 적었다. [plan T01–T05](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0013-sqllab-user-centric-access/plan.md#L41-L136). 라이브 V2는 두 탭에서 다른 관리자의 부여를 보존한 뒤 축 계정 역할을 원복하고, 권한 행렬·화면을 대조하도록 **계획**했다. [plan V2](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0013-sqllab-user-centric-access/plan.md#L196-L209). 시험 파일 존재는 확인했지만 이 조사에서 실행 결과를 보지 않았으므로 AC16 전 조합 PASS, 두 탭 보존·원복 순서, 실서버 동시 관리자 경합까지 확정할 수 없다. H2의 심미성·제품 통일성 수락 자료도 없다.

여섯 축 판정:

- 의도 보존: 사람 기준 보기·증감으로 0012와 범위를 나눴다.
- 설계 충실성: 조회·실제 판정·권한 출처·편집 가능 범위를 분리했다.
- 계획 실행성: 서버→화면 의존과 공용 쓰기 함수 소유권을 적었다.
- PR/병렬 분할: #338·#339가 병렬이고 실제 머지는 #339가 먼저다.
- 변경 피드백: 0013 선행 구현을 0012 계획에 반영했으나 PR-4 요약은 오래됐다.
- 검증·보고: 시험 파일·계기 설계는 확인, 라이브 권한 철회/AC16 전량은 미확인이다.

현행 [기준](../baseline.md)은 공유 계약·독립 기대·실제 통합판 검증·진행 요약의 정합성을 이미 요구한다. 이 사례의 잔여 질문은 새 템플릿 규칙보다 **수정 뒤 라이브 권한 변경/철회에서 화면·미리보기·실제 라우트가 같은 판정을 유지했는지**다. 원래 사용자 대화, PR 외부 검토 로그, 실제 런타임·OS·모델 선택은 미확인이다.
