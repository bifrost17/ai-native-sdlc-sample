# 설계 판정과 수정 기록

root는 최종 양식·작성 지침과 사용판을 **통과**로 판단했다. 북극성의 네 정보 역할을 지키면서
작업 결과·PR별 main 상태·검증을 연결한다. 작은 기능/결함은 짧게, 여러 PR·병렬/운영에는 필요한
상세만 확장한다. 완전 재현·무오류 강제의 목표는 두지 않는다.

## 정독·예시·대안

[reading-notes.md](reading-notes.md)에 기존 설계 방향·종합 조사·원문 L4/L7/L8/L10·PR 연구
재독의 적용/제외 근거를 남겼다. [네 유형의 예시](../../../../.claude/skills/plan/examples/context.md)는
root가 작성했다. [두 배치 비교](alternatives.md)에서 기본 네 절을 선택하고 작업별 묶음의 장점만
조건부로 가져왔다. [발견 뒤 갱신](change-walkthrough.md)은 plan-only와 spec 변경을 구별한다.

## 독립 리뷰

| 판 | maker / adopter | 결과 |
|---|---|---|
| R1, 20파일 | cea1abf / 95c0933 | [Astra/ultra](reviews/astra-r1.md) PASS, [실제 Fable/max](reviews/fable-r1.md) PASS; 비차단 소비자/경로 지적 |
| R2, 22파일 | 8248910 / 82d7ad2 | [Astra](reviews/astra-r2.md)·[Fable](reviews/fable-r2.md) PASS; 수락·현재 PR 범위·결함 시험 보호 순서·입력 설명 정정 |
| R3, 23파일 | b4ab132 / 82d7ad2 | [Astra](reviews/astra-r3.md)·[Fable](reviews/fable-r3.md) PASS; L4 측정 안내의 한 계획/여러 PR 해석 정정 |

최종 [후보 manifest](reviews/candidate-r3.json)의 결합 SHA256은
bbba590806c2afb160d858553fdf5d86815ce259ed4abdbe003551247e3537b1이다.
Astra는 실제 파일 해시를 재계산했다. Fable은 Read/Glob/Grep로 실제 본문을 읽고 제공 해시를
명시했으며 해시 자체는 계산하지 못했다. 이 차이를 원문 결과에 보존했다. Fable의 실제 모델은
claude-fable-5-1, 설계 effort는 max다. 각 첫 판정에 다른 리뷰어 결과는 제공하지 않았다.

비차단 지적 중 현재 소비자와 혼동을 만드는 부분은 고쳤다. header suffix의 표현 차이와 과거
spec 예시의 축약 경로는 동작 결함이 아니므로 역사 자료를 다시 쓰지 않았다. 원래 skill과 template
만 고쳐 현재 REVIEW·map·metrics가 반대로 안내하는 회귀를 남기지 않았다. 추가 검사기는 없다.

## 실제 실행과 한계

[F02 부분 실험](probe/README.md)은 실제 Sonnet/medium 3개 세션·6회 대화, 두 PR 범위의
순차 로컬 통합을 수행했다. root가 HUMAN으로 출력을 읽고 질문·수락·피드백했다. 새 문맥의 첫
구현에서 plan 설명 누락이 나왔고 이를 보존/복구했다. 이후 검증 방법 보강은 plan과 구현을 같은
커밋에 담았다. 제품 결과 통과와 최초 자발적 문서 갱신 실패를 별도로 기록한다.

독립 verifier의 기존 make check는 96 Python 시험(1skip), hooks28, eval fixtures8,
managed settings를 통과했다. make evals는 키 없음 rc=2이며 의미 평가 통과로 세지 않는다.
모델 검토·부분 대화·기존 검사 각각의 범위가 다르다. hosted PR/CI·실제 병렬 개발·운영 이행은
실행하지 않았다. 최종 검사 원문은 reviews의 verifier 기록에 보존한다.
독립 [최종 보고](reviews/verifier-final.md)와 [전체 명령 출력](reviews/verifier-logs/)에서 maker
검사·최종 통합 16시험·첫 상태 8시험·실제 인접 동작·실패/수정 이력을 확인할 수 있다.
최초 maker 출력이 파일로 보존되지 않아 마지막에 증거 보존용으로 한 번 재실행한 이유도 보고에 남겼다.

핵심 양식/스킬 → 필요한 유형의 예시 → 연동 소비자 → 리뷰/실험 요약 순서로 읽으면 된다.
큰 CLI 원문은 판정의 근거가 필요할 때 해당 턴만 읽는다. 그 기록의 크기를 제품 템플릿의 크기나
모든 reviewer가 반드시 읽어야 할 코드량으로 해석하지 않는다.

[사용판 전달](delivery.md)은 선택 예시 10파일 범위다. 실험 코드·제작 자료·리뷰 원문은 전달하지
않았다. 북극성 주석에는 새 문맥 실행·누락/복구·PR 통합의 이번 관측만 추가하고 기존 등급을 유지한다.
