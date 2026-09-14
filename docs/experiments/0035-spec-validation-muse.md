# 0035 — Muse Spark의 spec 인계 검토

2026-09-14. **보완·한정 실험 종료.** 정적·설치 검증과 HUMAN 피드백에 따른 문서 갱신을 확인했다.
복잡한 spec의 중요 공백 검출 개선은 입증하지 못했다. 완전한 검증 통과로 표시하지 않는다.

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

첫 01/02가 완료된 뒤, 02가 더 엄격한 결론을 냈지만 주요 두 공백을 놓치고 기존 정본 참조의 중복 정의를
요구한 관측을 받았다. 새 지적 중 유효한 내용과 과잉 반려를 먼저 원문 대조한다. 이 실제 실패의 최소
보완·새 문맥 재시험과 HUMAN 후속 대화를 위해 후속 호출 전에 한도를 **최대 8회·40분**으로 조정했다.
원본 r1 제품과 01/02 응답은 수정하지 않는다. 작은 03 대조는 초기 개선판 조건으로 진행하며 최종 판과 구별한다.

05의 최소 문구 개정 재시험도 중요한 두 공백을 놓쳤다. 06에서는 실제04 결과에 HUMAN이 계약 결정을
전달해 정본 갱신을 관측한다. 마지막07은 같은 r2 설치·전체 입력의 새 브랜치/문맥에서 검토 할당을
공유 계약과 독립 장애의 인계 가능성으로 좁힌다. 정답·특정 누락 위치·선행 결과는 제공하지 않는다.
이 호출은 프롬프트 범위도 바뀌는 진단이며, 지침만의 효과나 넓은 전체 검토의 성공으로 해석하지 않는다.
native child 포함 최대8회 안에서 종료하고 다음 표현 차이마다 규칙을 추가하지 않는다.

개선판이 중요한 공유 의미·독립 장애 공백을 발견하고, 작은 충분한 문서·정당한 이월을 과도하게 반려하지
않으면 해당 부분을 통과시킬 수 있다. 새 유효한 지적도 근거로 평가하며 예상 finding 수를 맞추게 하지 않는다.
기준판도 잘하면 개선 우월성을 주장하지 않는다. 04의 독립 검토는 HUMAN 요청이므로 설계 완료 시점의
완전한 자율 감지와 구분한다. 명시 스킬 사용·자연 선택·설치·읽기·결과 종합을 각각 기록한다.

## 보존 경로

- 제작 구현·설치·검토 자료: [designs/spec-validation-muse](designs/spec-validation-muse/)
- 실행기·원본 입력·prompt·공개 응답·HUMAN 정답과 판정: `/Users/jake/Projects/ai-native-sdlc-experiment-private/0035-spec-validation-muse`
- 순수 사용판과 사례별 제품: `/Users/jake/Projects/ai-native-sdlc-spec-validation-muse-20260914`
- 공개 실행 기록·해시·Git bundle은 [별도 evidence 저장소](/Users/jake/Projects/ai-native-sdlc-experiment-records/0035-spec-validation-muse/README.md)에 보존한다.

설계·입력 preflight와 정적 설치 확인은 Muse 행동 실험의 성공으로 세지 않는다. 제품 실행·두 TDD 판의
개발 성공·다른 CLI 행동·일반 탐지율·원본 제품 결함 수정은 이 부분 검증 범위 밖이다.

## 실제 보완과 결과

제작 후보는 초기 `41c7110`, 실제 실패 뒤 질문을 명료화한 `976c0c2`, 특정 생성물 예시를 일반적인
구현 산출물 표현으로 넓힌 최종 `58891ec`다. 마지막 표현 정리는 별도 행동 재시험으로 세지 않는다.

- 기존 REVIEW와 design-spec에 설계 인계 전 검토를 연결하고 전체 선언 정본·필요한 기존 계약을 읽도록 했다.
- 기존 feedback/verifier에 설계 검토 범위를 추가했다. 새 공유 의미와 기존 정본의 재사용, 중요한 독립
  장애의 진입·복구 조건, 의존 작업을 막는 미결과 정당한 이월을 구분한다. 설계만의 검토에 없는 plan·
  구현·실행 결과를 요구하지 않으며 실제 구현 완료의 fresh 검토는 유지한다.
- 실패 뒤 기존 계약의 중복 재기술 요구를 줄이도록 설명을 보완하고, 요구가 약속한 독립 장애만 나누어
  검토하게 했다. 검토 기록의 부재와 실제 미실행도 구별한다. 문구 개정 자체를 효과의 증거로 세지 않는다.
- 기본형 **0.1.10**, 선택형 **0.1.6**의 패키지·카탈로그·설치 안내와 기존 adapter를 맞췄다.
  새 스킬·검사기·상태 장부·의무 리뷰 수·보편적 도식 요건은 추가하지 않았다.

| 실행 | 실제 관측과 HUMAN 판정 |
|---|---|
| 01 기준판 | 새 내부 protocol operation의 의미 공백(F1), engine만 상실/B·X·M 생존 복구 공백(F2)을 모두 놓쳤다 |
| 02 개선 r1 | 더 엄격하게 반려했지만 F1/F2는 미검출. PTY의 문자/UTF-8 bytes 계약 충돌은 유효한 추가 발견. 여러 다른 지적은 기존 정본의 반복 요구나 미제공 기록을 미실행으로 확대한 판단이었다 |
| 03 F01 | 그림·없는 plan·실행 증거를 요구하지 않고 작은 충분한 문서를 인계 가능으로 판단. 초기 개선판의 한정 과잉 반려 방지 관측 |
| 04 합성 경계 + native child | feedback 스킬을 선택하고 Muse/xhigh verifier의 결과를 받아 종합. 숫자 문법/전송 전제 문제를 발견했지만 plan에만 넘긴 판단은 부족했다 |
| 05 개선 r2 | 같은 입력·prompt로 다시 실행했으나 F1/F2 미검출과 일부 과잉 판단 지속. 검출 개선 미입증 |
| 06 실제 HUMAN 후속 | 숫자 값 기준 수락·정상 생존 시 전달 전제·시간 기준 결정에 따라 spec/contracts/recovery 실제 수정. plan에만 이월한다는 앞선 판단 정정. 실행/사람 수락과 구별 |
| 07 범위 한정 진단 | 새 protocol 의미 공백과 engine 단독 장애 누락을 언급했으나 `finish: length`로 상세 보고가 중간 종료. 일부 반례도 불충분. 조건부 발견 신호만 보존하고 완전한 검출 성공으로 세지 않는다 |

[첫 진단](designs/spec-validation-muse/first-trial-diagnosis.md),
[재시험 진단](designs/spec-validation-muse/second-trial-diagnosis.md),
[합성 입력과 이월 판단 대조](designs/spec-validation-muse/boundary-diagnosis.md),
[마지막 부분 응답 대조](designs/spec-validation-muse/focused-trial-assessment.md)를 보존한다.
이 진단의 Astra/high는 설계·구현에도 참여했으므로 독립 최종 검토자로 표시하지 않는다.

합성 입력도 완벽한 정상 대조군이 아니었다. 초기 preflight에서 숫자 token/값 해석과 정상 생존 시
전달 가정을 놓쳤다. 실제 발견을 인정하고 HUMAN이 결정했으며 원본 네 파일과 최초 판정을 보존했다.
후속 문서판은 `326d19f`다. intent의 문제·정수 제약은 그대로여서 수정하지 않았고 없는 plan도 만들지 않았다.
개정은 HUMAN의 명시 결정에 따른 것이며 자발적인 모든 문서 동기화의 성공으로 확대하지 않는다.

## 실행·검증 근거

실제 **8호출(7 CLI 턴 + native child 1), 25분24.246초**다. 08:16:25.740–08:41:49.986 UTC이며
CLI 실행 합계는17분25.789초다. 부모 시간에 child가 포함되므로 중복 더하지 않는다. 고유89개 assistant
message의 실제 provider/model/variant에서 **Muse Spark 1.3/xhigh**를 확인했다. CLI는 모두 종료0,
timeout·잘못된 event·error event는0이지만 07의 `finish: length`는 응답 미완료다. 종료0을 내용 통과로 쓰지 않는다.

14개 프로젝트 스킬(11 native + 작성 예시3개), 수동 자료2개, verifier를 설치했다. 카탈로그에는
기본 customize-opencode와 전역 aside-browser도 보여 총16개였으며 두 항목은 권한으로 금지했다.
`--pure`는 외부 plugin을 끄지만 모든 전역 metadata를 없애지 않는다. 동명 충돌은 없었다.
스킬명을 주지 않은04에서 feedback을 골랐지만 HUMAN이 별도 리뷰를 요청했고 팀 workflow도 채택했으므로
완전히 자율적인 완료 이벤트 인식으로 해석하지 않는다. 01/02/03/05/07은 기준 읽기를 명시한 조건이다.

- 최종 코드 검증: `make check` 종료0. Python102 tests, skipped1, hooks28/28, eval fixtures8/8,
  managed-settings PASS. [전체 출력](designs/spec-validation-muse/make-check-r2.txt).
- 최종 package/marketplace strict 검증5개, 양 OpenCode·선택형 Codex 새 설치의 patch9개 통과.
  fuzz/offset·orig/rej 없음. 185개 source/설치 hash 불일치0, 버전/경로14대조 실패0.
- 고정 r2 제품은 `976c0c2` 설치와 일치한다. 최종 `58891ec`와는 일반화한 verifier의1문장만 다르며
  그 최종 설치도 따로 확인했다. 원본 r1/r2 실행 입력은 바꾸지 않았다.
- 기본형 test-first와 선택형 방식 선택, 구현 완료 fresh 검토, 작은 문서의 도식 선택성을 대조했다.
  maker verifier의 이전 체인·보호 hook 이웃 검증도 수행했다.

[독립 배포·정적 검토](designs/spec-validation-muse/distribution-review-r2.md)와
[명령·설치판·해시](designs/spec-validation-muse/static-install-r2.json)는 정적 범위의 근거다.
실제 모델 평가와 의미 판정을 대신하지 않는다. 실제 OpenCode 실행·debug에서 생긴 `$schema` 표기만
설정에 추가됐고 각 제품 Git에서 별도 기록했다. 모델·variant·권한은 바뀌지 않았다.

## 마감 판단

제작용 일반 지침·설치 개선은 반영하며, 중요한 복잡 설계의 검출 효과는 **미입증**으로 남긴다.
AC1–AC3·AC5의 지침/설치/기록 범위와 명시 피드백에 따른 문서 개정은 확인했으나, AC4의 핵심 복잡
공백 검출을 완전히 통과했다고 하지 않는다. 위험 범위를 좁힌07은 HUMAN이 실패 뒤 선택한 조건부 진단이다.
새로운 보고서의 인계 불가 결론·발견 개수·검토자 수를 정확성 증거로 삼지 않는다.

사용자가 재강조한 대로 하네스는 설계 무결성을 보장하지 않는다. 중요한 판단에 충분한 역량과
명확한 검토 범위를 주고 사람의 피드백을 연결하는 현재 수준에서 종료한다. 특정 두 공백을 모든
제품의 필수 항목으로 복제하거나 응답 길이 문제를 고치겠다며 템플릿에 새 장치를 추가하지 않는다.
북극성에는 위 관측만 추가하고 기존 실패·부분 판정을 유지한다. 실제 제품 구현과 원본 제품 결함 수정은 하지 않았다.

[Sol/medium 독립 마감 검토](designs/spec-validation-muse/closing-review.md)도 이 현실적 목표 기준의
부분 통과와 AC4 미통과를 확인했고 추가 제작 finding은 없었다. 원본·대화·공개 tool 기록·설치/입력
해시·진단·최종 리뷰를 포함한 evidence의 마지막 커밋은 `3cb3c3ad7eafec0c6f50a30c14979b84f1377ce8`이다.
245개 산출물의 manifest와 6개 완전한 Git history bundle을 보존했다. 제작 기록·주석은 local main에
반영하며 실험 제품은 사례별 별도 저장소·브랜치에 유지한다. 원격 push나 hosted PR 병합은 이번에 하지 않는다.
