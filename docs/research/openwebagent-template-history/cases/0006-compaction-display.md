# 0006 압축·모델 전환 표시 — 원인 재현이 초안 설계를 바꾼 사례

판정: **범위를 한정한 심층 검토 완료**. 원본은 수집된 `bifrost17/openwebagent` bare Git `main@a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e`와 PR API다. PR 본문의 시험 수치는 당시 기록이며 이번 조사에서 제품·브라우저·rig를 다시 실행하지 않았다. 원래 사용자 대화·모델 실행 로그·개발자 OS는 미확인이다.

## 요청에서 첫 인도까지

| 시점 | 사건과 근거 | 해석 |
|---|---|---|
| 최초 intent | CP4D 수동 압축 중 일반 작업 행만 보이고 모델 전환 후 이전 컨텍스트 수치가 남는다는 요청. 처음에는 완료 프레임만 도착해 진행 표시가 생략된다고 설명했고, 압축 임계·저장 경로는 범위 밖으로 뒀다. [intent@72db89ca:6–18,20–45](https://github.com/bifrost17/openwebagent/blob/72db89ca642d0c30ad51b0989d29fb34b646933b/intent/0006-compaction-display/intent.md#L6-L45) | 최초 원인 서술은 뒤 재현으로 좁혀졌다. |
| 첫 spec | `4653d032`는 진행 카드의 `contextCompaction` 프레임과 사용량 이벤트의 창을 두 경계로 나눴다. AC01은 진행→완료의 실제 화면, AC03은 모델 전환 **전** 게이지가 보이는 양성 대조를 요구했다. Q1·Q2·Q3는 구현 전 결정으로 표시했다. [spec@4653d032:21–30,34–80](https://github.com/bifrost17/openwebagent/blob/4653d032e3b8fd1559c7a4ed937367942304671a/intent/0006-compaction-display/spec.md#L21-L80) | 검증의 공허 통과 위험을 초기 설계가 인식했다. |
| 관측·변경 | `10ee6363`의 화면 프레임 재현 뒤 `d3965a2c`에서 원인 주장의 무게를 낮췄다. 실제 진행 결핍은 `item/started`가 화면에 닿지 않는 **충분조건**이고, 상류 미발신·전송 유실·호스트 버퍼링 중 원인은 미결로 남겼다. 일반 작업 행과 압축 카드의 이중 표시도 별도 결함으로 발견, 요청자 Q11 결정 후 FR08·AC11–13으로 편입했다. [intent@main:11–37,57–94](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0006-compaction-display/intent.md#L11-L94), [spec@main:22–48](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0006-compaction-display/spec.md#L22-L48) | 새 관측·요청자 결정에 따른 정당한 설계 개정이다. |
| 첫 plan | `286e6d2c`는 실제 `CodexChat`을 렌더하는 하네스의 프레임 열로 DOM RED를 재며, 수동 표시·모델 게이지·자동 압축 관측·rig 400 규명을 네 인도로 분리했다. 같은 `CodexChat.svelte`의 두 변경은 직렬, rig는 별도 저장소라고 적었다. [plan@286e6d2c:4–17,34–53](https://github.com/bifrost17/openwebagent/blob/286e6d2c057e8bc6f47321bb9487db849c2ed743/intent/0006-compaction-display/plan.md#L4-L53) | 공유 파일·선행 관측·검증 방식이 첫 작업 착수 전에 연결됐다. |
| 구현·인도 | 문서의 4개 PR 경계는 실제로 [#318](https://github.com/bifrost17/openwebagent/pull/318) **한 PR**에 통합돼 `71157ef0`로 머지됐다. 호스트 낙관 작업 행에 압축 문면, 벤더 타임라인 선택 prop에 이중 행 억제, 모델 창만 무효화하는 오버레이를 넣었다. [spec@main:68–160,205–246](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0006-compaction-display/spec.md#L68-L160), [#318](https://github.com/bifrost17/openwebagent/pull/318) | 계획의 논리 인도와 실제 GitHub PR 수를 구별해야 한다. 통합 PR 자체가 곧 결함 증거는 아니다. |
| 후속 관측 | 자동 압축 2건의 DB 기록에는 `item/started`가 있었고 완료-only 0건이었다. 따라서 자동 압축 코드를 바꾸지 않고 기존 카드를 회귀로 잠갔다. CP4D 400은 에뮬레이터에서 629,017 토큰 요청이 선언 창 131,072를 넘는 조건으로 재현돼 rig 패치는 하지 않았다. [spec@main:35–46,161–204,247–333](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0006-compaction-display/spec.md#L35-L46), [#318](https://github.com/bifrost17/openwebagent/pull/318) | 관측 범위 밖의 완료-only 자동 압축과 실제 CP4D 상류 전체 거동까지 증명하지 않는다. |

## 여섯 축과 네 가설

| 축 | 판정 |
|---|---|
| 의도 보존 | **확인.** 수동 표시·모델 게이지의 목표를 지키면서 요청자 Q11 이중 표시, Q6 400 규명 범위 확장, GLM을 검증 수단으로 삼지 말라는 정정을 문서에 반영했다. [intent@main:118–153](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0006-compaction-display/intent.md#L118-L153) |
| 설계 충실성 | **부분 확인.** 화면 문면·호스트/벤더 소유·아카이브 보호·링/압축 트리거 공동 소비를 명시했다. Q10 프레임 미도착의 상류 원인은 남아 있으나 표시 수리의 착수 조건은 아니다. [spec@main:343–370](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0006-compaction-display/spec.md#L343-L370) |
| 계획 실행성 | **강점.** T별 파일·선행·DOM 관측·미해결 분기를 적고, 탐색 PR-3/4에는 관측 뒤에 수정을 결정하도록 했다. 같은 파일의 논리 PR이 실제 한 PR로 묶인 이유·위험은 PR 본문에서 확인되지만 개별 인도 후 main 검증은 없었다. [plan@286e6d2c:19–53](https://github.com/bifrost17/openwebagent/blob/286e6d2c057e8bc6f47321bb9487db849c2ed743/intent/0006-compaction-display/plan.md#L19-L53) |
| PR·병렬 분할 | **논리 분리, 실제 단일 PR.** rig는 별도 저장소 작업이고 패치가 필요 없었다. #323·#324의 0006 파일 변경은 타 개발건의 인접 회귀/문서 접점이라 #318의 추가 인도로 세지 않는다. [#318](https://github.com/bifrost17/openwebagent/pull/318), [#323](https://github.com/bifrost17/openwebagent/pull/323), [#324](https://github.com/bifrost17/openwebagent/pull/324) |
| 변경 피드백 | **확인.** 가설→하네스 관측→충분조건으로 주장 축소, 요청자 결정→FR/AC 보강, 독립 검토→`optWorkingLabel` 시험 추가 순서가 커밋에 남았다. 같은 커밋에 문서·코드가 있을 때 문서가 실제로 먼저 갱신됐다는 시간 주장은 하지 않는다. [spec@main:354–371](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0006-compaction-display/spec.md#L354-L371), [#318](https://github.com/bifrost17/openwebagent/pull/318) |
| 검증·보고 | **범위 표기가 좋음.** #318은 프런트 8,089건·브라우저 하네스 23+5건·rig 15건을 주장하지만 실 dev 스택 e2e는 사용자 보류로 미실행이라고 표시했다. 이 조사의 독립 실행 통과는 0건이다. [#318](https://github.com/bifrost17/openwebagent/pull/318) |

H1은 **반증 성격이 강함**: 최초 설계 가설이 뒤집혔으나 재현과 정당한 요구 조정으로 바뀌었고, 막연한 설계 부족으로 설명하기 어렵다. H2는 **직접 대상 아님**: HTML 목업 없이 기존 컴포넌트의 상태·문면을 고친 사례라 심미성 최종 판단 근거가 없다. H3는 **부분 지지**: 호스트 작업 행·벤더 타임라인·툴팁·링/트리거의 여러 소비자를 선행 계약으로 연결했으며 이중 표시가 실제 경계에서 발견됐다. H4는 **부분 반증**: 입력 프레임·양성 대조·DOM 기대가 설계/계획에 있었지만 실 dev 스택 e2e가 빠져 최종 화면 전체 수락은 미확인이다.

현재 0.1.8 정본은 실제 UI 관측, 공유 경계, 독립 기대, 미실행 범위 구분을 이미 요구한다([기준 비교](../baseline.md)). 이 사례의 잔여 위험은 **하네스의 프레임 열과 실제 CP4D·실 dev 화면 사이의 증거 공백**이며, 새 일반 템플릿 규칙 결함으로 확정하지 않는다. 귀속은 주로 프로젝트 관측·도구/환경 제약과 에이전트의 원인 주장 교정이다. 리뷰 API의 빈 formal review 목록으로 독립 검토 부재를 추론하지 않는다.

미검토: 원래 CP4D 서비스의 프레임 전체, rig 별도 Git 커밋의 미푸시 상태, 사용자가 보류한 dev e2e의 이후 실행 여부와 현재 배포 화면. 이 사례의 PR 텍스트만으로 이 항목을 닫지 않는다. [#318](https://github.com/bifrost17/openwebagent/pull/318)
