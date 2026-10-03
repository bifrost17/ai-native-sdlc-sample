# 0012 수백 명 규모 권한 관리 — 설계 완료, 핵심 화면은 미구현

판정: **설계 이력 심층 검토, 구현·효과는 근거 부족**. `main@a08295f`에서 [#335](https://github.com/bifrost17/openwebagent/pull/335)의 문서 이력, 현재 코드의 선택기·역할 목록, 0013과 공유한 쓰기 함수를 확인했다. 0012의 PR-0~3 실행 PR은 수집 색인·main 첫 부모에서 확인되지 않는다.

## 사건 사슬

| 단계 | 관측 | 해석 |
|---|---|---|
| 새 요청, 9/23 | 0010에서 권한 부여가 가능해진 화면을 보고 요청자가 수백 명 규모 적합성을 물었고, 세 개선을 모두 설계하라고 했다. 원격 선택기가 첫 페이지에서 끝나고 역할·그룹 목록이 두 페이지만 읽는 것은 **원본에 있던 페이지 기능의 이식 누락**이다. 구성원 500명 모달 전량 렌더와 일괄 역할 부여·회수는 **원본의 한계/원본에 없는 새 요구**다. [초기 intent](https://github.com/bifrost17/openwebagent/blob/73c8b9f3a343aa754a57540fe8093ee94184aede/intent/0012-sqllab-security-admin-at-scale/intent.md#L4-L72). | 0010 수리 실패 세 건으로 계산하면 원인과 새 요구가 섞인다. |
| 첫 설계·검토 | `73c8b9f`가 세 문서를 한 커밋에 넣었다. 독립 검토 `47d73e0`은 원격 소비처 수, 오류 코드, 역할 저장의 실제 병렬 전송, 경합·원자성, 실증 도구 누락을 바로잡았다. 2차 검토 `9e4e72e`는 닫힌 드롭다운의 과도 적재, 중복 페이지, 오류 종료, 청소 함수의 과삭제 위험, 무력한 jsdom 계기를 고쳤다. [plan 검토 기록](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0012-sqllab-security-admin-at-scale/plan.md#L178-L235). | 초기 설계가 충분했다고 단정할 수 없다. 검토가 실제 코드·원본·DB 사실을 여러 번 수정했다. |
| 요청자 결정 | 기존 `PUT` 전부 교체와 증감 경로의 경합을 모두 없앤다는 약속은 줄이고, **증감 경로끼리** 서로 지우지 않는 것으로 Q6 범위를 제한했다. `11e335b`가 요청자 승인 기록을 intent/spec에 반영했다. [intent Q6](https://github.com/bifrost17/openwebagent/blob/11e335b7dc85a5bffabf41d19edb7827b7f17c76/intent/0012-sqllab-security-admin-at-scale/intent.md#L95-L101), [#335](https://github.com/bifrost17/openwebagent/pull/335). | 동시성 계약의 의도적 한계다. 기존 PUT과의 경쟁은 잔여 위험이다. |
| 실행 여부 | plan은 T00 데이터 시드/청소→T01·T02 복원, T03 증감 API→T04·T05 화면의 의존 순서와 실제 500명 실증을 지정한다. [plan:1–23,139–174](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0012-sqllab-security-admin-at-scale/plan.md#L1-L23). 수집 main의 `AsyncMultiSelect`는 여전히 `fetchOptions(term, 0, pageSize)`만 호출하고 `UserRolesList`는 page 0·1만 읽는다. [선택기](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/apps/open-webui/src/lib/components/sqllab/common/AsyncMultiSelect.svelte#L89-L108), [역할 목록](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/apps/open-webui/src/lib/components/sqllab/security/UserRolesList.svelte#L82-L102). | #335 머지는 **설계 인도**다. 규모 수락·청소 안전성·UI 효과는 미검증이다. |

0013 [#339](https://github.com/bifrost17/openwebagent/pull/339)가 먼저 만든 `membership_delta.apply_membership_delta`와 사용자 고정 증감 API는 0012 T03이 **재사용하도록 plan을 갱신한 공용 기반**이다. 0012의 역할 고정 `PATCH /roles/{id}/users`·`/groups`나 일괄 UI 완료로 바꾸지 않는다. [0012 plan T03](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0012-sqllab-security-admin-at-scale/plan.md#L91-L120), [공용 함수](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/apps/open-webui/backend/open_webui/utils/sqllab/security/membership_delta.py#L85).

## 가설과 기준 대조

H1은 **초기 설계 누락과 검토 수정을 지지**하지만, 새 요구 ②·③을 0003의 설계 결함으로 소급하면 안 된다. H3는 병렬 PR의 선행 계약과 공유 쓰기 함수, 화면이 두 API에 의존한다는 계획으로 **설계상 대응**됐다. 구현 결합 결과는 없다. H4는 500명 시드/청소, 배포 전후 같은 화면·요청 수, 기존 데이터 불변 대조, 경합 삽입 계기까지 plan이 상세히 적어 **계획 수준에서는 지지되지 않는다**. 실제 T00 실행·백업·라이브 왕복 결과는 없다. H2의 화면 심미성 근거는 없다. [plan V2–V4](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0012-sqllab-security-admin-at-scale/plan.md#L139-L177).

여섯 축 판정:

- 의도 보존: 이식 결함과 새 규모 요구를 구분하고 Q6 한계를 수락했다.
- 설계 충실성: 두 차례 검토로 원자성·오류·청소 안전성을 고쳤다.
- 계획 실행성: 의존·500명 실증은 구체적이지만 실행 전이다.
- PR/병렬 분할: #335는 문서 PR이고 뒤 PR 묶음은 계획에만 있다.
- 변경 피드백: 0013이 먼저 만든 공용 함수를 재사용하도록 계획을 바꿨다.
- 검증·보고: 실제 500명 전후 비교와 청소 결과는 미확인이다.

남은 필수 인도는 역할 고정 증감 API, 페이지 구성원 UI, 일괄 부여·회수 UI와 같은 500명 전후 실증이다.
현행 0.1.8+기존 WIP [기준](../baseline.md)은 실제 경계·선행 공유 계약·검증 방법·미실행 구분을 이미 다룬다. 0012는 템플릿의 효과 사례가 아니라 **깊은 사전 검토를 거친 미착수 계획**이다. 설계 검토자가 기록한 파일/DB 확인은 이번 조사에서 전체 원문·실험 로그까지 재검증하지 않았다. OS·모델 수준은 문서의 검토자 언급만으로 추정하지 않는다.
