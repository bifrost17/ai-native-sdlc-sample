# Astra R1 독립 리뷰

Reviewer: intent_astra_review, gpt-6-astra / ultra. 아래는 반환 보고 원문이다.

**FAIL — spec 후보 R1**

31개 후보 파일의 SHA-256과 결합 해시를 직접 재계산했고 영수증과 일치했습니다.

`35ddaab081efbdb8b5dea875f360ff855d475634c0e6aa7f7ae6a7d6d0c49806`

양식과 작성 지침은 요구·설계 통합, 중요한 보존 동작, R/AC 관계, 미결 판단, 조건부 상세를 적절히 지원합니다. 다만 M01의 복구 설계에 잘못된 구현 계획으로 이어질 중요한 공백이 있습니다.

**수정이 필요한 발견 1건**

- **위치:** maker `.claude/skills/design-spec/examples/migration/spec.md:32-33,63-65,91-96`. adopter `examples/skills/design-spec/examples/migration/spec.md`도 동일합니다.
- **문제:** 최신 DB 값을 JSON으로 내보내고 구버전 조회·완료를 검증하면 복구할 수 있게 설명하지만, **복구 후 구버전의 쓰기를 어떤 조건으로 재개할지 빠져 있습니다.** 그 구버전의 JSON 전체 읽기·쓰기는 이번 변경이 해결하려는 동시 갱신 유실의 원인입니다.
- **구체적 상황:** 전환 후 처리 결과를 포함한 JSON 복구에 성공합니다. 구버전 서비스를 재개하고 서로 다른 두 요청을 동시에 완료하면, 두 요청 모두 성공을 응답하고도 뒤의 파일 저장이 앞의 상태를 덮을 수 있습니다. AC4의 조회·완료 확인을 통과하면서 R1과 원래 데이터 보존 목적에 다시 어긋날 수 있습니다.
- **최소 수정 방향:** 복구 데이터의 최신성과 복구 후 허용할 쓰기 운영 조건을 구별해 명시해야 합니다. 예컨대 복구 후에도 안전한 쓰기 조건을 확보하거나, 확보 전에는 쓰기를 재개하지 않는 범위를 결정할 수 있습니다. 아직 결정하지 않았다면 중요한 미결로 표시해야 합니다. 구체적인 실행 명령은 plan에 남겨도 됩니다. 새 절·검사기·일반 승인 절차는 필요하지 않습니다.

**세 예시의 독자 인계 확인**

- **F01 기능:** `list --owner <ID>`로 정확히 일치하는 담당자의 완료·미완료 요청을 기존 순서로 보여줍니다. 옵션 없는 목록, 다른 명령, 출력·JSON 필드, 조회의 파일 무변경을 유지합니다. 기존 배열 읽기 뒤 필터와 display 재사용을 선택한 이유가 충분합니다. 대표 데이터의 선택 결과·빈 결과·대소문자·미배정 구별과 기존 동작 회귀가 수용 근거입니다. 입력에 남아 있던 세 질문은 명시적인 합성 답변으로 해소됐습니다.
- **B01 버그:** show/complete의 비교 입력 양끝에서 지정된 ASCII 네 문자만 제외합니다. 저장 ID·다른 필드·내부 공백·대소문자·다른 유니코드 공백·기존 오류 표현과 complete의 정상 상태 변경을 보존합니다. 공통 조회 경로에서 입력 사본만 처리하는 이유와 넓은 정규화를 배제한 이유가 읽힙니다. 성공·실패·반복 완료·파일 보존 사례가 수용 근거입니다. 예시 코드와 확정 계약도 구별되며, 현재 입력에서 계획 전에 남은 업무 판단은 없습니다.
- **M01 이행:** SQLite 행 단위 트랜잭션으로 동시 완료를 보존하면서 API·인증·권한·필드·순서를 유지합니다. 단일 호스트와 서비스 중지 허용 조건이 선택 이유입니다. JSON 직접 보고서가 발견되면서 **R5, AC6, 소비자 설계, 전달 범위, Q1과 우려 상태**가 함께 바뀌었습니다. 기존 계정으로 GET API를 사용하고 오류 때 옛 JSON으로 대체하지 않습니다. 동시 완료, 데이터·권한 비교, 중단·재실행, 복구, 경합 오류, 보고서 전환이 수용 근거입니다. 파일·명령·작업 소유·PR 순서·실제 시험은 plan에 남아 있습니다. 위에서 지적한 **복구 후 쓰기 조건**은 아직 설계 판단이 필요합니다.

모든 예시는 실제 조직 수락과 실행 결과가 아님을 명시합니다. 입력 intent의 상류 커밋도 maker `ac0963b`, adopter `dbfd371`에서 실제 파일 내용과 일치함을 확인했습니다.

**호환성과 전달 범위**

- maker/adopter의 intent·context는 동일하며, spec은 상류와 참조 메타데이터를 제외하면 동일합니다. 설계 깊이 참고도 동일합니다.
- adopter는 `References applied`, 선택형 `examples/skills`, `disable-model-invocation: true`를 유지합니다. maker의 플러그인·평가 도구 설치를 요구하지 않습니다.
- 기존 plan·정책 소비자가 사용하는 상류 메타데이터, R/AC, `Flagged concerns`는 유지됩니다.
- Eval 03의 변경은 절 이름과 fixture 배치 조정입니다. Q1 누락을 잡는 음성 fixture, 질문 정규식과 정책 적용 의미 기준은 약화되지 않았습니다. 이 판단은 diff 검토 결과이며 eval 실행 결과는 아닙니다.

비차단 참고로 M01 `spec.md:66-67`의 “기존 백업 책임 범위”는 context에 실제 백업 체계가 제시된 사실과 구별하는 편이 좋습니다. 디스크 손실 복구까지 이번 설계에 추가하라는 요구는 아닙니다.

**실제로 읽고 확인한 파일**

maker에서 다음 16개 후보 본문을 읽었습니다.

- `templates/spec.md`
- `.claude/skills/design-spec/SKILL.md`
- `.claude/skills/design-spec/references/design-depth.md`
- `.claude/skills/design-spec/references/skill-provenance.md`
- `.claude/skills/design-spec/examples/{feature,bug,migration}/{intent,context,spec}.md` — 9개
- `evals/cases/03-spec-carries-questions.json`
- `evals/testdata/{03-pass,03-fail-carry}/ws/spec.md` — 2개

adopter에서는 `examples/README.md`, capture-intent/design-spec 선택 지침, 두 template과 세 spec의 다른 메타데이터를 읽었습니다. 나머지 예시 입력 6개와 깊이 참고는 실제 바이트 해시의 일치로 maker에서 읽은 내용과 대조했습니다.

지원 자료로 spec-design의 `review-request.md`, `reviews/candidate-r1.json`, `README.md`, `alternatives.md`, `alternative-feature.md`, `change-walkthrough.md`, `reading-notes.md`를 읽었습니다. 소비자 확인에는 maker의 plan 스킬, `spec-policy-pass`, Eval 03 입력 fixture도 사용했습니다.

파일을 수정하거나 다른 리뷰어 결과를 읽지 않았습니다. 이번 검토는 문서·입력·인계·소비자 연결 검토이며, 구현·이행·회귀 시험 실행이나 조직 승인을 증명하지 않습니다.
