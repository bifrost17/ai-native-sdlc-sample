# openWebAgent 실사용 이력과 템플릿 개선

Status: [U1–U7 제작 보완](completion/README.md)을 완료했다. 새 사용자 지시의 [Muse 한 사례](../../experiments/0038-document-sync-muse.md)는 계약 갱신·동반 커밋·동작 확인을 통과했다. 현재 plan 요약 누락은 독립 리뷰에서 발견해 인계 상태 갱신을 부분으로 정정했다. 기존 전체 전후 비교는 유예하며 [제작 작업](../../../intent/0028-openwebagent-history-feedback/plan.md)에 대상판·한계를 남긴다.
조사 기준일은 2026-10-03 Asia/Seoul이다. 원본 수집 시각은 manifest의 UTC 값으로 별도 보존한다.

## 기준과 범위
북극성은 [AI-Native SDLC Playbook](../../verification/north-star-playbook.html)이다.
접근 가능한 개발건 전체를 조사 모집단으로 두고 중요한 사건을 심층 분석했다. 같은 사건·공통 자료는 중복 읽지 않으며,
모든 코드·상태 조합·실행 원문을 전량 감사한 것으로 해석하지 않는다. 미검토와 근거 부족은 [전체 색인](coverage.md)에 남긴다.
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
이 폴더에는 개발건별 조사와 검토 **전문**을 저장한다. 요약과 보완안은 별도로 두며 전문을 대체하지 않는다.
Git·PR·웹의 수집 원문과 에이전트 보고 응답 전문은 로컬 원본 보관소에 두고,
[원문 보존 안내](originals.md)에서 출처·SHA·해시·수집 한계를 연결한다.

## 완료 결과
PR340건·브랜치114개에서 번호30개+무번호4개 개발건을 연결했다. [전체 색인](coverage.md)에 각 사건의
보고서와 근거 부족·미검토를 남겼다. 중요한 초기판·구현·리뷰·후속 인계와 대형0018 추가 조사를 포함하며
모든 코드 경로/시험 로그의 전량 감사로 확대하지 않는다.

- [최종 보완안](recommendations.md): 우선3건과 추가 PR/커밋·개발건 기록 정책, 현재 후보·미입증 범위.
- [설계 방법 원전 조사](design-methods.md), [기록 정책 설계](change-records-design.md).
- [기준판](baseline.md), [후보 검토](candidate-review.md), [전달 검토](delivery-review.md).
- [설계 검토](design-review.md), [source 검토 전문](source-review.md), [최종 결론 검토](conclusion-review.md).
- [원문 보존 안내](originals.md), [원격 수집 원문과 보존 감사](collection-originals.md).

실사용 전체 효과·hook의 개별 인과 효과는 미입증이다. 0038은 별도 합성 사례의 실제 행동 관측이며
원제품·운영·전역 스킬은 변경하지 않았다. 추가 실험은 후속 사용자 지시를 받는다.
