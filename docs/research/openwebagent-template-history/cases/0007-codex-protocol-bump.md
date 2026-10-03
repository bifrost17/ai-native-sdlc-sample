# 0007 — Codex protocol 갱신 의도

상태: 검토 완료(의도 단계); 구현 효과는 평가 대상 아님. frozen branch의 [최초 intent@5007277d701f](https://github.com/bifrost17/openwebagent/blob/5007277d701f/intent/0007-codex-protocol-bump/intent.md)가 유일한 개발건 문서다. main·모든 branch·Git 이력에서 해당 폴더의 spec/plan과 연결 PR은 확인되지 않았다.

## 사건과 기준
- 2026-09-20의 intent는 sandbox Codex 0.148.0과 관측한 Desktop 0.153.4 사이의 protocol 차이, thread/items/list·turns/list 사용 필요를 다룬다. 관측판과 실제 목표판을 구분한다.
- schema 출력 249개와 버전 pin 참조 139개/시험 8개라는 당시 조사 결과를 기록한다. 이 보고서는 수치와 runtime를 다시 실행하지 않았다.
- 0005의 당장 진행을 차단하지 않고 향후 이력 수집의 경계로 분리한다. 실제 오류 수정과 낡은 assertion 수정을 구별하며 asset SHA 및 airgap release 제약을 남긴다.
- 대상판·schema 차이·pin 분류·release 시점은 미정이다. 미정의 존재만으로 제품 결함이나 plan 누락으로 판단하지 않는다.

## 여섯 축과 추가 가설
의도는 문제·관측·제약·후속 조사 질문을 보존했다. 설계·계획·작업 분할·구현 피드백·실행 완료는 아직 주장하지 않으므로 이 단계에서 평가하지 않는다. PR/커밋 형식 또는 과거 spec의 현재 정본 승계 사건도 없다. H1 설계 부족, H2 UI, H3 늦은 통합, H4 검증 설계 부족을 뒷받침하는 구현 사건이 없다.

## 원인과 한계
이 건을 미완성 제품 구현 실패로 집계하지 않는다. 원격에 의도만 있다는 사실은 의도 단계의 기록이며, 별도 비공개 실행이 없었다는 증명이 아니다. 실제 모델·추론·개발 OS·작성 대화는 확인하지 못했다. source root와 scope는 collection manifest/inventory에 보존했다. 과거 지침의 실제 읽기 또는 적용도 버전이나 브랜치 이름으로 추정하지 않는다.
