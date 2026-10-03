# 0009 워크트리 Codex 홈 볼륨 격리 — 등재 뒤 미착수

판정: **중요 근거 부족을 명시한 검토**. 2026-10-03 수집 `main@a08295f`의 문서·실제 Compose·Git 이력과 [#324](https://github.com/bifrost17/openwebagent/pull/324)를 대조했다. 사고 발생, 원래 대화 원문, 실제 두 레인의 동시 실행은 확인하지 않았다.

## 사건 사슬

| 때 | 관측 | 의미 |
|---|---|---|
| 9/21–22 | 0008 T02 재현 스택을 읽다 `docker-compose.wt.yml`의 `CONTAINER_PREFIX`·`VOLUME_PREFIX`와 달리 `CODEX_VOLUME_PREFIX`가 빠진 것을 발견했다. 0008 T08 문서 보완 커밋 `535af674b5`가 0009 intent를 추가했다. [최초 intent](https://github.com/bifrost17/openwebagent/blob/535af674b5b734ebe49d378ad3b133f6804d1edf/intent/0009-worktree-codex-home-volume-isolation/intent.md#L1-L29). | 별건 등재가 0008 수정과 섞이지 않았다. |
| 9/22 | #324는 **0008 도구 출력 소실**의 T03–T08 PR로 머지됐다. 그 PR에 0009 intent가 들어간다는 사실만으로 0009 수정이 구현됐다고 볼 수 없다. [#324](https://github.com/bifrost17/openwebagent/pull/324). | 동일 PR을 두 건의 완료로 세지 않는다. |
| 수집 main | `deploy/docker-compose.wt.yml`에는 여전히 `CODEX_VOLUME_PREFIX` 설정이 없다. `orchestrator/app.py`의 기본값 `codex-home-`과 볼륨 이름 `f"{CODEX_VOLUME_PREFIX}{uid}"`가 남아 있다. [wt Compose](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/deploy/docker-compose.wt.yml#L66-L75), [app.py](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/orchestrator/orchestrator/app.py#L198), [볼륨 조립](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/orchestrator/orchestrator/app.py#L2799). | 같은 uid의 두 레인이 기본 접두어를 쓰면 이름 충돌 가능성이 코드상 남는다. |

intent는 `deploy/docker-compose.llmep.yml`의 별도 접두어 관례를 제시하고, 워크트리 전용 접두어를 제안한다. 그러나 기존 레인의 볼륨명이 바뀌면 Codex 홈·인증 상태가 새 볼륨으로 보일 수 있으므로 영향받는 레인 확인을 제약으로 남겼다. 실제 동시 사용 사고와 수정 시점은 질문으로 열었다. [intent@main:31–58](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/intent/0009-worktree-codex-home-volume-isolation/intent.md#L31-L58), [llmep Compose](https://github.com/bifrost17/openwebagent/blob/a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e/deploy/docker-compose.llmep.yml#L54).

## 판단

의도 보존은 **문서 범위에서 확인**된다. 0008 조사 중 찾은 다른 위험을 독립 intent로 올렸고, 미관측 사고를 실사고로 주장하지 않았다. spec·plan·0009 구현 PR·시험은 수집 색인과 main에서 **미검토 대상이 아니라 부재**다. 설계 충실성·계획 실행성·검증 효과를 평가할 구현 이력은 없다.

H1(설계 부족)은 이 사건의 발생 원인으로 단정할 수 없다. 워크트리 Compose에 두 격리 변수는 있었으나 Codex 홈 접두어만 빠져, **구성요소 간 공유 자원의 빠진 경계**라는 관측이 있다. H3는 정적 코드에서 지지되지만 동시 실행 충돌은 미재현이다. H2·H4는 해당할 UI·실행 검증 자료가 없다. 현재 템플릿의 공유 계약·실제 통합판 검증 지침은 이미 이 질문을 다룬다([기준](../baseline.md)); 0009만으로 새 정책을 제안하지 않는다.

여섯 축의 현재 판정:

- 의도 보존: 발견·제안·영향·열린 질문이 서로 구별된다.
- 설계 충실성: spec이 없어 판정 불가.
- 계획 실행성: plan이 없어 판정 불가.
- PR/병렬 분할: 0008과 별건으로 남긴 경계만 확인.
- 변경 피드백: Q1·Q2의 결정과 후속 수정은 확인되지 않는다.
- 검증·보고: 코드상 충돌 가능성만 확인했고 실사고는 주장하지 않는다.

미확인: 요청자가 Q1·Q2에 답했는지, 실제 영향을 받는 워크트리 볼륨 목록, 수정의 배포 효과. OS·모델 실행 환경은 intent의 작성자 표기 외에 추정하지 않는다. 이 조사에서 Compose 기동과 볼륨 충돌 시험은 실행하지 않았다.
