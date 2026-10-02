# 0016 — Text2SQL 엔진 재시작 정책

판정: **정적 변경 검토 완료, 실제 재부팅 후 복구는 미검증.** WSL 재기동 뒤 `t2s-engine`만 `Exited (255)`로 남고 생성 요청이 503이 된 운영 관측에 대해 compose 오버레이의 재시작 정책을 한 줄 보완한 작은 사례다.

고정 자료는 `.local/research/openwebagent-template-history/20261003/collection/` inventory·API·bare Git, 초기 main `a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e`다. [PR #345](https://github.com/bifrost17/openwebagent/pull/345)은 2026-09-27 머지됐다. [`8181e9f`](https://github.com/bifrost17/openwebagent/commit/8181e9f493f)는 브랜치에서 intent·spec·plan, `deploy/docker-compose.t2s-engine.yml`, `scripts/tests/compose-invariants.test.sh`를 **같은 커밋**에 추가했고, [`2d4a219`](https://github.com/bifrost17/openwebagent/commit/2d4a219a90c)가 main에 반영했다. 같은 커밋은 문서가 구현보다 먼저 쓰였거나 RED 시험이 실제로 먼저 실행됐다는 증거가 아니다.

intent `:4-30`은 재부팅·503·에어갭 반입 제외를 기록한다. spec `:4-28`의 FR01/AC01은 `docker-compose.u8.yml`과 엔진 오버레이를 함께 렌더할 때 `t2s-engine.restart == unless-stopped`, `open-webui`를 양성 대조로 검사한다. plan `:7-26`은 그 compose 한 줄과 시험 계기를 T01로 연결한다. 제품 diff는 오버레이의 `restart: unless-stopped`, 시험 diff는 렌더된 정책을 확인하는 계약이다. PR 본문은 수정 전 FAIL→수정 후 PASS, `docker compose config -q`와 bind-source guard 통과를 보고한다. `text2sql-contract`는 기준 main에서도 같은 골든 키 집합 불일치로 red였고 full `candidate-contract`는 신뢰 실행 환경 전제 부족으로 미실행이라고 구별했다. 이 주장들의 원시 출력·실제 재부팅 뒤 상태는 이번 수집에 없다.

| 축 | 판정 |
|---|---|
| 의도 보존 | **충족.** 503 원인을 엔진 컨테이너 재시작 정책으로 한정했고 에어갭 반입 문제는 범위 밖으로 유지했다. |
| 설계 충실성 | **정적 확인.** compose 정책과 렌더 계약 시험이 FR01에 직접 대응한다. 실제 운영 컨테이너는 재생성 후 새 정책을 받아야 한다는 spec의 제약도 남겼다. |
| 계획 실행성 | **충분.** 작은 변경의 파일·방법·기대가 명시됐다. 한 커밋 때문에 작성·시험 실행 순서는 미확인이다. |
| PR·병렬 분할 | **한 PR이 적절.** 다른 모듈 공유 계약이나 병렬 통합의 증거가 없다. |
| 변경 피드백 | PR 뒤 추가 수정·리뷰 반영은 확인되지 않는다. API 목록이 비었다면 리뷰 부재로 단정하지 않는다. |
| 검증·보고 | **경계 구분 양호.** 영향 계약 PASS, 선재 red, full gate 미실행을 분리했다. 실제 재부팅 후 503 해소는 미검증이다. |

H1은 초기 설계 복잡도보다 compose 누락이라는 좁은 원인에 맞는다. H2는 UI 외형 사건이 아니어서 해당 없음. H3은 모듈 간 인터페이스보다는 배포 수명주기 계약의 누락을 지지한다. H4는 정적 compose 계약을 추가했지만 실제 재부팅 회복을 증명하지 못한 예다. 현행 0.1.8과 기존 WIP의 계획·검증 기준은 [baseline](../baseline.md)에 분리돼 있고, 당시 실제 스킬 적용은 확인되지 않았다. 새 템플릿 규칙보다 배포·운영 시험의 증거 범위를 정확히 보고하는 사례다.
