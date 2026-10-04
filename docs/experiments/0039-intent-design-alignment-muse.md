# 0039 — 의도·설계 연결의 작은 OpenCode 실험

Status: planned — source 보완·검토 중, 모델 실행 전

사용자 요청: “브랜치 따서 작업 시작하고 opencode cli사용해서 간단하게 실험해”.
북극성의 intent의 무엇/왜/제약과 spec의 문제 해결 대조를 기준으로, 기존 스킬0.1.10의 편입 전
의도·이유·전제 대조를 작은 실제 대화에서 관측한다. root는 HUMAN(Codex simulated),
OpenCode Muse Spark는 개발 에이전트다. 0038의 부분 인계 판정과 전체 AC04 유예는 유지한다.

## 시작판과 예산

제작 branch는 `codex/intent-design-alignment`, base는 main@1d3ffd3이다. 검토/설치를 확인하고
source를 커밋한 뒤 그 정확한 판을 제품 template branch→fixture main→작업 branch에 적용한다.
팀 native11·작성3·수동 자료2·같은 검토자와 전체 동반 자료를 복사하고 source/patch/설치 해시를 고정한다.
이번 의미 판단 관측에는 선택 Git hook을 채택하지 않는다. 전역 스킬·설정·원제품은 바꾸지 않는다.

[제품 입력](datasets/v10/intent-alignment/public.md)은 기존 tracker CLI의 코드/시험과 비정렬 합성4행이다.
[HUMAN 조건](datasets/v10/intent-alignment/human.md)은 제품에 전달하지 않는다. 같은 세션에서 정상
owner 필터 설계→이유 없는 정렬 충돌→명시적 제약 변경과 실제 구현을 진행한다. 첫 두 단계는 설계 전용이다.
후속 메시지는 실제 제출을 읽고 작성한다. 문서 갱신 대상이나 평가 정답을 먼저 지정하지 않는다.

실제 OpenCode CLI 판과 model/variant를 공개 metadata에서 확인한다. 요청 모델은 이전과 같은
`opencode-go/muse-spark-1.3-contributor`, variant는 `xhigh`다. 설치/파싱 확인 후 모델 사전 호출은 하지 않는다.
parent3·native child1·전체15분을 기본 한도로 두며 필요한 추가 호출은 미완료로 남긴다.
이는 HUMAN dispatch 예산이며 모델 내부 도구 round-trip 수는 원문에서 따로 보존한다.

## 판정과 보존

첫 설계는 intent 유지·spec/plan 이유 연결·코드/시험 무변경, 충돌 요청은 편입 전 질문/미결 유지,
명시적 변경은 중복 승인 없이 실제 intent와 하류 문서 개정·동작/회귀·커밋·현재 인계를 확인한다.
root는 기존 시험과 독립 CLI 기대·종료 코드·조회 무변경을 직접 대조한다. 실제 실행/개입/실패는
단계별 PASS/PARTIAL/미관측으로 구분하며 중요한 누락은 보존한다. 작은 표현 차이로 반복하지 않는다.

제품은 `.local/experiments/workspaces/0039-intent-design-alignment-muse/product/`, 원문은
`.local/experiments/private/0039-intent-design-alignment-muse/`에 둔다. 입력·프롬프트·공개 응답/도구·
모델/세션·시간·단계별 파일/dirty diff·source/설치 해시·독립 실행 전문·Git refs/bundle을 보존한다.
인증 값과 숨은 추론은 공개 원본 대상에서 제외한다. 설치 확인을 실제 읽기/사용 증거로 대체하지 않는다.
한 합성 사례는 새 세션 인계·모든 추천 전제 반증·큰 설계 누적·다른 도구 행동·개별 인과 효과를 입증하지 않는다.
