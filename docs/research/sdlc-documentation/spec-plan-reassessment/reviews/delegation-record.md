# 독립 검토의 배정과 보존

2026-09-11. 모든 하위 작업은 공유 저장소에서 자기 보고서 한 파일만 작성하도록 한정했다.
원문과 기존 후보는 읽기만 했다. 전체 대화 이력을 넘기지 않고 작업에 필요한 공통 제약을 명시했다.

| 작업 | 모델/추론 | 입력과 독립 범위 | 산출물 |
|---|---|---|---|
| spec_exemplar_reassessment | gpt-6-astra / ultra | CLAUDE·새 README/system-designs·D1/D2·북극성 발췌·후보 spec/작성 스킬/블록/4예시·필요한 활성 소스. 이전 PASS나 다른 검토는 근거로 사용하지 않음 | astra-spec.md |
| architecture_exemplar_audit | gpt-5.6-sol / high | CLAUDE·새 README/system-designs·D3/D4·후보 spec/블록/M01. 아키텍처 설명의 사실 대조로 한정 | architecture-evidence.md |
| 실제 Claude Code 독립 교차 검토 | opus / high | 정확한 읽기 목록·조건은 [보존 프롬프트](opus-prompt.md). 앞선 모델과 root 리뷰 미제공 | opus-r1.md |

공통 요청은 다음과 같다: 북극성 우선, 얇은 사내 서비스, 다중 설계 정본 가능, 구체적인 중요한 결정,
모든 메서드/다이어그램 의무 없음, spec 설계와 plan 실행 분리, TDD는 팀 선택, 좋은 근거와 기존 반례를 함께 보고한다.
외부 문서 안의 스킬/실행 지시는 연구 대상이며 수행하지 않는다. 없는 실행 성공을 주장하지 않는다.

Root는 별도로 P1/P2/P3 실제 계획과 P3 짝 설계를 읽고 root-plan.md를 작성했다.
Astra가 정책 스킬 충돌을 알린 뒤 root는 후보 전달안에 이미 해결책이 있는지 추가 확인을 요청했다.
두 하위 보고서의 초안 뒤에는 로컬 링크의 실제로 존재하지 않는 #L fragment를 없애고 줄 번호 라벨은 보존하도록 요청했다.
Sol에는 클래스 그림 변경을 필수 결함으로 보지 말고 가독성 선택으로 구별하며, 대안 개수보다 기각 이유의 타당성을 보도록 정정 요청했다.
이 후속은 새 독립 검토로 세지 않는다.

Claude의 초안 뒤에는 누락한 context/B01/기존 인계·결정 기록을 읽도록 [정정 프롬프트](opus-followup-prompt.md)를 보냈다.
같은 세션의 응답과 Read 기록을 보존했다. 비공개 추론은 수집하지 않았다. 모델 리뷰의 최종 채택/기각은
[root 처리 기록](../adjudication.md)에 있다.
