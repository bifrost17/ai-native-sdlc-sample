# 0011 쓰는 자리의 SQL Lab·Codex 결함 — 죽은 컴포넌트와 실제 화면

판정: **범위를 한정한 심층 검토 완료**. `main@a08295f`의 문서와 [#330](https://github.com/bifrost17/openwebagent/pull/330)·[#331](https://github.com/bifrost17/openwebagent/pull/331) 머지, 선택한 구현을 확인했다. 원래 브라우저·대화·시험 로그는 독립 재생하지 않았다.

## 사건 사슬

| 단계 | 근거 | 판정 |
|---|---|---|
| 요청, 9/22 | 0003 및 0010 PR-1 배포 뒤 실제 화면에서 ① 스키마 선택 불가, ② 좁은 데이터 소스 목록의 겹침, ③ 모델 권한 403에 샌드박스 안내가 붙는 것을 관측했다. 요청자는 셋을 먼저 한 건으로 다루도록 했고, 권한 판정 자체는 범위에서 뺐다. [intent](https://github.com/bifrost17/openwebagent/blob/d34e02053ed31889da1cb9fc9b369dda8d6f2ddc/intent/0011-sqllab-point-of-use-defects/intent.md#L4-L79). | 세 증상은 하나의 원인이 아니다. 권한 수리 0010과의 중복 결함으로 세지 않는다. |
| 최초 설계·계획 | `d34e020`에서 intent/spec/plan을 함께 넣었다. 원본 Superset의 compact 선택기는 팝오버로 전체 선택기로 나가지만, 이식본의 대응 `SqlEditorLeftBar`는 **마운트되지 않았고** 살아 있는 `SqlLabSidebar`에는 스키마를 다시 채울 길이 없었다. [spec SP01](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0011-sqllab-point-of-use-defects/spec.md#L25-L61). | H3의 결합 누락: 컴포넌트 구현 존재와 사용자 경로 존재는 다르다. |
| 구현·검토 | #330(T01·T02)와 #331(T03)을 파일 집합 분리 확인 뒤 병렬 진행했다. 원래 plan의 직렬 문구를 변경 이유와 함께 갱신했다. 독립 검토 뒤 AC05가 재는 실제 레일 목록이 `DataSourceSection`, 초기 SP02가 지목한 `DatabaseSelector`는 모달 목록임을 정정했다(`950e35a`). 또 새로 보이는 모달 버튼에 정의되지 않은 CSS 클래스를 썼던 점을 고쳤다(`8f3e2f9`). [plan:4–23](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0011-sqllab-point-of-use-defects/plan.md#L4-L23), [spec SP02](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0011-sqllab-point-of-use-defects/spec.md#L62-L78). | 문서 수정은 실제 측정 표면과 계획 파일을 맞춘 피드백이다. 같은 사건을 별도 실패 두 건으로 중복 계산하지 않는다. |
| 보고 | plan은 같은 백엔드·DB에서 수식 없는 쿼리 `1146`→`17686`, 스키마 변경 시 오류의 대상 스키마 추적, 240px 목록 겹침 해소를 **당시 브라우저 실증**으로 기록한다. #331은 접근권 전용 detail과 공용 안내표 사용을 기록했다. [plan:88–164](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0011-sqllab-point-of-use-defects/plan.md#L88-L164). | 기록상 실제 화면 증거가 단위 시험보다 깊지만 이번 조사 실행 결과는 아니다. |

## 가설·원인

**H1·H3:** 0003의 이식 컴포넌트 자체에는 원본 선택 경로가 있었지만, 실제 마운트된 레일과 연결되지 않았다. 첫 설계에서도 AC05 관측 지점과 수정 대상 파일을 잘못 연결했고 구현 검토 중 정정했다. 이는 모든 UI 내부를 미리 확정해야 한다는 결론보다, **살아 있는 소비 경로를 기준으로 계약·시험을 연결**해야 한다는 사례다. [spec SP01–02](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0011-sqllab-point-of-use-defects/spec.md#L25-L78).

**H2·H4:** 좁은 폭의 겹침과 정의되지 않은 모달 버튼 스타일은 컴포넌트 시험만으로 사용자 화면 수락을 보장하지 못한다. plan은 단위 시험이 스키마 이벤트 발행만 재며 쿼리 결과와 CSS는 브라우저에서 확인해야 한다고 구분했다. 실제 화면 기반의 수정은 확인되지만 최종 디자인 심미성 평가는 없다. [plan T01–T02](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0011-sqllab-point-of-use-defects/plan.md#L37-L101).

Codex 403은 두 동명 `check_model_access` 중 라우트가 쓰는 함수에는 관리자 우회가 없다는 사실을 추적해 **메시지만** 고쳤다. 다른 함수와 판정을 통합하는 것은 후속 결정으로 남겼다. 접근권이 없는 사용자를 200으로 바꿨다는 해석은 틀리다. T03의 TDD 선언은 시험과 구현이 같은 커밋이라 **RED→GREEN 순서가 Git으로는 미확인**이라고 plan이 스스로 바로잡았다. AC07 샌드박스 미기동의 실제 브라우저 상태와 Oracle 스키마 실행도 미측정이다. [intent Q2–Q3](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0011-sqllab-point-of-use-defects/intent.md#L79-L93), [plan T03](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0011-sqllab-point-of-use-defects/plan.md#L103-L126), [미측정](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0011-sqllab-point-of-use-defects/plan.md#L170-L178).

여섯 축 판정:

- 의도 보존: 403 판정 변경을 제외하고 화면 사용·정확한 안내에 집중했다.
- 설계 충실성: 실제 레일과 최초 지목 파일의 불일치를 정정했다.
- 계획 실행성: 파일·배선·실증 절차는 구체적이며 병렬 변경을 기록했다.
- PR/병렬 분할: UI와 Codex 안내의 파일 집합이 분리돼 두 PR로 머지됐다.
- 변경 피드백: CSS 버튼과 시험 설명의 잘못된 근거를 검토로 고쳤다.
- 검증·보고: 브라우저 수치는 보고됐지만 AC07과 RED→GREEN 순서는 미확인이다.

현행 [기준](../baseline.md)은 실제 UI 관찰, 유효한 코드 지점, 독립 기대와 미실행 구분을 이미 다룬다. 여기서 남는 것은 템플릿 조항 추가보다 **마운트된 경로를 확인하고, 브라우저 결과를 시험 주장과 따로 남기는 실행 품질**이다. 원래 OS와 검토 모델은 경로·PR 이름만으로 추정하지 않는다.
