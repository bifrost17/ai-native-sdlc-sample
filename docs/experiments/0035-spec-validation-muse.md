# 0035 — Muse Spark의 spec 인계 검토

2026-09-14. 준비·실행 중. 결과를 아직 통과로 판정하지 않았다.

[북극성](../verification/north-star-playbook.html)의 설계 인계·실제 피드백·검토 근거를 기준으로
[보완 설계](../decisions/spec-validation-design/README.md)와 [제작 계획](../../intent/0025-spec-verification/plan.md)을 실행한다.
사용자의 후속 요청에 따라 실제 실험 대상은 OpenCode Muse Spark 1.3/xhigh다. 제품 구현·전체 SDLC 실험은 아니다.

## 실행 전 고정한 조건

- 기본형 0.1.10·선택형 0.1.6에 같은 설계 검토 의미를 반영하고 제공 adapter를 검증한다.
  실제 모델 행동은 **선택형 OpenCode**만 관측한다. 두 판의 TDD 차이와 구현 완료 fresh 검토를 유지한다.
- root는 [HUMAN 페르소나](PERSONA.md)를 맡는다. 실제 제출을 읽고 답하며 고정된 응답 대본을 쓰지 않는다.
- OpenCode 1.18.30, `opencode-go/muse-spark-1.3-contributor`, parent/child `variant: xhigh`를 사용한다.
  [런타임 준비](designs/spec-validation-muse/runtime-prep.md)의 사전 확인과 실제 세션 metadata를 구분한다.
- 기준판 `fa76b89`와 개선판의 순수 제품 사용 브랜치를 만들고 사례별 브랜치를 파생한다.
  팀 스킬은 실험 제품에 선택 설치한다. 사용자 전역 파일이나 원본 제품을 변경하지 않는다.
- 원본 복잡 설계 126파일의 같은 입력을 기준/개선에 전달한다. 선언한 13개 design 정본 전체와 필요한
  기존 계약·source를 보존한다. [선별·미제공 근거](designs/spec-validation-muse/complex-input-review.md)는
  원본 packet의 누락·과거 리뷰 언급·외부 원문 미검증을 명시하며, 완전히 가려진 실험으로 주장하지 않는다.
- 에이전트는 원인분석·평가 정답·선행 standalone PASS·다른 실행 결과를 보지 않는다.
  검토 지침과 제품 입력은 먼저 고정하며 주요 예상은 HUMAN 전용 기록에 둔다.

## 순서와 판단

| 요청 | 조건·관측 |
|---|---|
| 01 기준 r1 | 현행 0.1.5 + 복잡한 원본. 지정한 feedback/검토 기준을 직접 읽고 설계만 검토. 추가 위임 없음 |
| 02 개선 r1 | 개선 0.1.6 + 같은 원본·요청·권한·모델. 지침의 실제 읽기와 계약 공백 근거 확인 |
| 03 작은 문서 | 개선판의 F01 작성 예시. 그림·전체 schema·실행 증거 등 과잉 반려가 없는지 |
| 04 합성 경계 | C/W/R 독립 수명·원장/발행 응답 손실·멱등성과 정당한 내부/배포 이월을 가진 별도 설계. 스킬명을 지정하지 않고 다른 검토자에게 검토받아 인계 준비를 정리하도록 요청 |

04의 native child를 포함해 기본 5회, 중요 문제의 후속/재시험에 1회를 더해 총 6회·30분을 시작 예산으로 둔다.
CLI의 내부 여러 message/tool step과 agent 호출 횟수를 혼동하지 않는다. 같은 제품의 후속은 실제 응답을
읽은 뒤 작성한다. 템플릿 개정 후 효과 재시험은 원 결과를 보존하고 새 브랜치·새 문맥에서 한다.
예산 조정이 필요하면 사유와 새 한도를 적용 전에 기록하며 실패를 숨기기 위해 무한 반복하지 않는다.

개선판이 중요한 공유 의미·독립 장애 공백을 발견하고, 작은 충분한 문서·정당한 이월을 과도하게 반려하지
않으면 해당 부분을 통과시킬 수 있다. 새 유효한 지적도 근거로 평가하며 예상 finding 수를 맞추게 하지 않는다.
기준판도 잘하면 개선 우월성을 주장하지 않는다. 04의 독립 검토는 HUMAN 요청이므로 설계 완료 시점의
완전한 자율 감지와 구분한다. 명시 스킬 사용·자연 선택·설치·읽기·결과 종합을 각각 기록한다.

## 보존 경로

- 제작 구현·설치·검토 자료: [designs/spec-validation-muse](designs/spec-validation-muse/)
- 실행기·원본 입력·prompt·공개 응답·HUMAN 정답과 판정: `/Users/jake/Projects/ai-native-sdlc-experiment-private/0035-spec-validation-muse`
- 순수 사용판과 사례별 제품: `/Users/jake/Projects/ai-native-sdlc-spec-validation-muse-20260914`
- 마감 때 공개 실행 기록·해시·Git bundle은 별도 evidence 저장소에 보존하고 이 문서에서 연결한다.

설계·입력 preflight와 정적 설치 확인은 Muse 행동 실험의 성공으로 세지 않는다. 제품 실행·두 TDD 판의
개발 성공·다른 CLI 행동·일반 탐지율·원본 제품 결함 수정은 이 부분 검증 범위 밖이다.
