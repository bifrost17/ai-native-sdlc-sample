# openWebAgent 실사용 이력과 템플릿 개선

Status: running. 사용자 수락 계획과 [제작 작업](../../../intent/0028-openwebagent-history-feedback/plan.md)을 실행한다.
조사 기준일은 2026-10-03 Asia/Seoul이다. 원본 수집 시각은 manifest의 UTC 값으로 별도 보존한다.

## 기준과 범위
북극성은 [AI-Native SDLC Playbook](../../verification/north-star-playbook.html)이다.
접근 가능한 모든 개발건을 심층 조사하며, 같은 사건·공통 자료는 중복 읽지 않는다.
원격 저장소는 bifrost17/openwebagent, 초기 main은 a08295f2f7f492efd3ef4787c4ed3d1a1d8f118e다.
현재 PR body와 실행 기록의 주장은 독립 실행 증명과 구별한다. Mac/Windows는 기록 근거가 있을 때만 표시한다.

## 방법
각 건은 요청·결정→당시 spec/plan→구현/시험→리뷰/수정→통합/후속 변경의 사건 사슬로 읽는다.
평가축은 의도 보존, 설계 충실성, 계획 실행 가능성, PR/병렬 분할, 변경 피드백, 검증/보고 정확성이다.
초기 0018/0021/0028로 방법을 교정하고 전 개발건에 적용한다. 의미에 영향이 없는 변경의 제외 이유도 남긴다.

보고서는 판정과 근거를 같이 둔다. 검토 완료·중요한 근거 부족·미검토를 구별한다.
template/skill/project-policy/agent/tool-environment/evidence 원인을 구분한다.
당시판·현재 배포 정본·미커밋 후보를 대조하며 이미 해결된 문제에는 새 규칙을 추가하지 않는다.
동일 commit과 최종 문서만으로 문서 선행 갱신을 추정하지 않는다.

원본/API/Git·기준판·프롬프트·응답·시험은 제작 저장소의
`.local/research/openwebagent-template-history/20261003/`에 보존한다. 현재 제품이나 전역 설치는 변경하지 않는다.
이 폴더에는 원문을 재게시하지 않고 필요한 출처·SHA·관측·한계를 정리한다.

## 완료 결과
아직 수집·분석 중이다. 전체 검토나 개선 효과를 통과로 판단하지 않았다.
