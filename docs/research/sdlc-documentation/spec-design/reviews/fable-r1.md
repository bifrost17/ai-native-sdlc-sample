# Claude Code fable result

Filtered CLI export; private reasoning omitted. Final result below is verbatim.

# 독립 리뷰 보고 R1: 결합 spec 양식 후보

## 판정과 검토 범위

**판정: PASS.** 이 범위의 문서 설계 리뷰이며, 사람의 승인이나 구현 검증을 뜻하지 않는다. 잘못된 plan이나 거짓 준비 완료 주장을 만들 만한 누락·모순은 찾지 못했다. 아래 권고 항목은 모두 차단 사유가 아니다.

**검토 대상 식별.** receipt는 `docs/research/sdlc-documentation/spec-design/reviews/candidate-r1.json`의 round 1이다. 결합 해시와 기준 커밋은 receipt에 적힌 값을 그대로 옮긴 것이며 내가 재계산한 값이 아니다.

| 항목 | 값 | 출처 |
|---|---|---|
| combined_sha256 | 35ddaab081efbdb8b5dea875f360ff855d475634c0e6aa7f7ae6a7d6d0c49806 | 제공됨 |
| maker base_head | ac0963b72334b3dedda291a187e5718f6e291dc1 | 제공됨 |
| adopter base_head | dbfd3711e54ce397a73ce11446dd9da69cbe10e8 | 제공됨 |
| 파일별 sha256 및 parity_checks | 전부 제공된 값 | 재계산 불가 |

**해시 한계와 대체 확인.** Bash 도구가 없어 어떤 해시도 재계산하지 못했다. 대신 미러 파일을 실제로 읽어 내용을 눈으로 대조했다. 세 예제의 intent.md와 context.md 여섯 쌍은 본문이 동일했다. 세 spec.md 쌍은 2행의 Upstream SHA와 4행의 Skills applied 대 References applied만 달랐다. design-depth.md 두 판과 intent 템플릿 두 판은 동일했고, spec 템플릿은 3행만 달랐다. 이는 receipt의 parity_checks 서술과 일치한다.

**실제로 읽은 파일.** maker의 receipt 16개 파일 전부, 연구 문서 다섯 개인 README·alternatives·alternative-feature·change-walkthrough·reading-notes, review-request.md, 소비자인 plan 스킬·plan 템플릿·`/spec` 명령·spec-policy-pass 스킬·spec-policy 명령·sdlc-feedback 스킬·policies/README·evals/check.sh·evals/README·eval 04 케이스와 그 과거 출력·CLAUDE.md·PLAYBOOK-MAP 3행, 테스트의 관련 부분, 북극성 Lesson 3 본문과 Lesson 4 도입·plan 예시 구간, 데이터셋의 F01/B01 public.json·requests.json·baseline tracker.py, 그리고 0020·0021 체인의 intent/spec을 읽었다. adopter는 receipt 15개 파일 전부와 CLAUDE.md·README·docs/PROCESS·docs/GIT-WORKFLOW·REVIEW·PROJECT-POLICY·NOTICE·intent/README·plan 예시 스킬·plan 템플릿을 읽었다. human.json, 다른 리뷰어의 보고, reviews 폴더의 fable-r1 호출 기록은 읽지 않았다.

## 질문별 결과와 발견

- **Q1 결합 요구·설계와 계획 입력.** 지원한다. 템플릿은 요구·수용 기준·설계·제약·질문·우려 여섯 구획과 앞머리 요약을 두고, 스킬은 시험 파일명·명령·작업 순서를 plan에 남기라고 명시한다. 대안 수 고정이나 별도 설계 승인 절차를 요구하지 않아 RFC 관료화도 피했다. 세 예제 모두 파일 목록이나 PR 순서를 담지 않았고, M01은 계획에 넘길 경계를 별도 소절로 밝혔다.
- **Q2 예제의 입력 보존.** 세 예제 모두 intent의 제약과 context의 후속 답을 빠짐없이 R·제약·질문 처리에 옮겼다. F01/B01 context의 코드 관측은 실제 baseline과 대조해 확인했다. list 출력 열과 탭 구분, show/complete의 공유 조회와 원본 비교, 완료 반복 시 미기록, 오류 문구가 tracker.py의 실제 동작과 같았다. 대표 데이터도 두 requests.json과 같다. 발명된 사실은 없었고, 예시 코드는 B01에서 구현 예시로 명시적으로 구별됐다. M01은 5초 상한·상태 코드·503 본문을 context가 준 값만 썼고 성능 수치를 만들지 않았다.
- **Q3 수용 기준의 유용성.** R 문장 반복이 아니라 대표 성공·실패·회귀를 담았다. F01 AC2의 `-` 사례는 화면 표시용 미배정 기호를 담당자로 오인하는 회귀를 잡는다. B01 AC2는 내부 공백·대소문자·U+00A0·빈 문자열·없는 ID를 묶어 과잉 정규화를 막는다. M01 AC3·AC4·AC5는 이행 거부·복구 실패·경합 초과의 실패 경로를 다룬다. 한 줄당 한 시험을 요구하지 않았다.
- **Q4 상세도 비례와 M01 기술 정합성.** F01은 짧은 단일 흐름, B01은 규칙 하나와 보존 조건, M01만 하위 절을 가진다. 부수적 선택은 세 예제 모두 구현자와 plan에 넘겼다. M01의 이행·중단·복구·보고서 계약은 서로 모순되지 않는다. 검증 전 전환 금지, 실패 시도 격리와 원본 재시작, 전환 후 쓰기를 포함한 내보내기 복구, 복구 미검증 시 DB 보존, 보고서의 API 전환과 옛 파일 대체 금지가 한 방향으로 맞물린다. 아래 권고 1~3은 이 계약을 더 명시적으로 만드는 보완이다.
- **Q5 미결과 우려의 가시성.** 스킬은 carried forward 밑의 이름이 해소가 아니라고 명시하고, 설계를 무효화할 질문이나 정책 충돌은 인계 전에 사람에게 올리라고 적었다. change-walkthrough의 발견 전 발췌는 Q1 이월과 F1 차단을 함께 보여 정직한 미완성 초안의 형태를 제시한다. 템플릿의 질문·우려 프롬프트도 근거·영향·담당·필요 시점을 요구한다.
- **Q6 변경 처리.** 스킬의 변경 절은 영향받는 R·설계·제약·AC와 질문·우려를 고치고, 실행·검증이 달라진 plan과 목적·제약이 달라진 intent만 맞추라고 한다. 이미 주어진 결정을 재승인받지 않고 새 원장을 만들지 않는다. sdlc-feedback 스킬과 adopter의 GIT-WORKFLOW 개정 절차와 충돌하지 않는다.
- **Q7 소비자 호환.** 2행의 Upstream/Status, Skills applied, R/AC 참조, Flagged concerns가 유지됐다. spec-policy-pass가 참조하는 `templates/spec.md`·`Skills applied`·`Flagged concerns`·carried forward 표현은 모두 남아 있다. plan 스킬은 절 이름을 참조하지 않는다. 스킬 템플릿 동일성 테스트는 intent만 고정하므로 spec 템플릿이 스킬 본문에서 빠진 것은 테스트를 깨지 않는다. eval 03은 케이스 프롬프트가 새 절 이름을 안내하고, 두 fixture는 Q1 한 줄만 다르며 Q1 정규식 검사가 남아 있어 질문 누락 실패가 유지된다.
- **Q8 adopter 전달.** 템플릿은 References applied를 쓰고, 세 예시 스킬은 examples 아래에만 있으며 `disable-model-invocation: true`로 선택형이다. 플러그인·스킬 설치를 요구하는 문장은 없고 PROJECT-POLICY와 PROCESS도 이를 명시한다. adopter design-spec은 승인 판 확인, 코드 읽기, 여섯 구획 지침, 이월 비해소 원칙, 변경 반영, 계획·승인 미수행을 모두 담아 설계 실질이 같다. capture-intent 예시는 0020에서 검토한 원칙인 제안 보존, 수치·담당·원인 비발명, 비례적 질문, 관측·추정 구분, 제안자 확인을 담고 있다.

**차단하지 않는 발견과 권고.** 경로와 영향을 함께 적는다.

1. **전환 후 쓰기 여부 판단 규칙 부재.** `.claude/skills/design-spec/examples/migration/spec.md:63`은 쓰기 전 원본 복귀와 쓰기 후 내보내기 복구를 나누지만, 쓰기 여부를 확인할 수 없을 때의 기본값이 없다. plan이 단순 복귀 단계를 넣을 여지가 생기므로 "확인 불가 시 쓰기가 있었던 것으로 취급"을 한 줄 추가하길 권한다.
2. **기존 백업 책임 가정.** 같은 파일 66~67행은 디스크 손실을 기존 백업 책임에 맡기지만 context.md에는 백업 체계가 없다. SQLite 활성 파일은 JSON처럼 단순 복사로 백업하기 어려우므로, 가정임을 밝히거나 운영 담당의 확인 질문으로 남기는 편이 정확하다.
3. **복구 검증에서 complete 실행.** 같은 파일 32행의 AC4는 구버전 조회·완료로 내보낸 JSON을 검증한다. complete는 파일을 바꾸므로 사본에서 검증한다는 말을 넣어야 plan이 복구 파일 자체를 변경하지 않는다.
4. **직접 쓰기 프로세스 문구.** 같은 파일 58행은 직접 쓰기 프로세스 중지를 전제하는데 87행의 Q1은 직접 쓰기 소비자가 없다고 확인한다. 모순은 아니지만 "있다면"을 붙이면 독자의 혼동이 준다.
5. **참조로 묶인 계약.** 같은 파일 13~14행은 응답·권한·오류 계약을 context.md 참조로 확정한다. 합성 예시에서는 적절하지만 실제 spec에서는 코드나 API 문서의 판을 지목해야 한다는 점을 design-depth가 이미 요구하므로 예시에 한 줄 주석을 두면 오용이 줄어든다.
6. **eval 03 fixture의 절 순서.** `evals/testdata/03-pass/ws/spec.md`는 새 절 이름을 쓰지만 수용 기준이 마지막에 오는 옛 순서다. 정규식 검사에는 영향이 없다. 새 템플릿 순서로 맞추면 fixture가 양식 예시 역할도 한다.
7. **restate와 참조 허용의 미세한 차이.** `evals/cases/03-spec-carries-questions.json`의 프롬프트는 제약을 다시 적으라 하고, 템플릿과 스킬은 명확한 R 참조를 허용한다. 결정론 검사는 이를 재지 않으며 의미 채점만 영향을 받을 수 있다. 기준을 약화하지는 않았다.
8. **후보 밖의 낡은 참조.** `docs/verification/north-star-playbook.html:512`의 V3-09 주석은 옛 절 이름을 인용한다. 역사적 평가이므로 요구는 아니지만 다음 검증 기록 갱신 때 정리 대상이다. CLAUDE.md의 "skill-embedded templates 복사본" 설명은 이제 intent에만 맞고, `.claude/commands/spec.md`의 "미승인이면 멈춘다" 문구는 스킬의 기록된 초안 예외를 반영하지 않는다. 셋 다 receipt 밖이다.
9. **환경 사실 처리의 편차.** F01 spec은 표준 라이브러리 조건을 다시 적지 않고 B01은 적는다. 스킬 규칙상 환경 사실은 자동 금지가 아니므로 오류는 아니며, 일관성만 다르다.
10. **adopter 스킬의 작은 생략.** `examples/skills/design-spec/SKILL.md`에는 원 프롬프트를 PR 기록에 남기는 거버넌스 항목과 intent의 해결 제안을 제안으로 다루라는 문장이 없다. 후자는 capture-intent 예시와 M01 예제가 보여 주므로 실질 손실은 작다.
11. **미커밋 입력.** maker의 migration/context.md는 작업 트리에서 수정 상태이고 spec의 Upstream은 intent만 고정한다. spec과 같은 커밋에 넣으면 receipt 해시 외의 고정점이 생긴다.

## 읽기-인계 연습과 한계

**F01 담당자 조건 조회.** 바뀌는 것은 `list --owner <ID>` 추가와 정확 일치·순서 유지·완료 포함 필터다. 유지할 것은 옵션 없는 list, show/complete, 출력 열, JSON 필드, 읽기 전용 조회다. 핵심 선택은 기존 순회 뒤 한 번 거르고 display를 재사용하며 인덱스·캐시를 두지 않는 것이고, 이유는 규모·성능 문제가 입력에 없기 때문이다. 수용 증명은 hana 조회의 두 행 순서, nobody·HANA·`-`의 빈 출력과 rc=0, 네 행 전체 목록과 파일 바이트 불변이다. 계획을 막는 판단은 없다.

**B01 주변 ASCII 공백 허용.** 바뀌는 것은 show/complete가 양끝의 space·tab·CR·LF만 뗀 사본으로 조회하는 것이다. 유지할 것은 저장 ID와 행, 내부 공백·대소문자·다른 유니코드 공백의 의미, 기존 오류 형식과 rc, 완료의 원래 상태 변경과 반복 완료의 미기록, list, 기존 시험이다. 핵심 선택은 공유 조회 앞에서 비교 사본에만 허용 문자 집합을 적용하는 것이며, 인자 없는 strip은 범위가 넓고 데이터 일괄 보정이나 명령별 정규화는 일관성을 깨기 때문이다. 수용 증명은 제어 문자 감싼 ID의 성공, 여섯 종류 실패 입력의 rc=1과 파일 불변, 공백 붙은 complete의 status만 변경과 재실행 불변, 기존 동작 회귀 없음이다. 계획을 막는 판단은 없다.

**M01 SQLite 전환과 보고서 호환.** 바뀌는 것은 전체 파일 재작성이 행 단위 트랜잭션 갱신으로, 저장소가 검증된 SQLite로, 야간 보고서 입력이 GET /requests로 바뀌는 것이다. 유지할 것은 네 필드와 순서, 정상·오류 응답과 인증·권한 계약, 권한 없는 완료의 무변경, 5초 대기 상한, 원본 JSON, 외부 서비스·계정 미추가다. 핵심 선택은 단일 호스트·중지 허용 조건에서 SQLite를 택하고 JSON 잠금과 외부 DB를 배제한 것, 그리고 영구 미러·이중 쓰기 대신 보고서를 API로 옮긴 것이다. 수용 증명은 겹친 완료의 두 결과 보존, 이행 전후 조회 동일, 잘못된 입력의 전환 거부와 원본 보존, 전환 후 쓰기를 포함한 내보내기 복구, 경합 초과 시 503과 확정 상태 재조회, 보고서의 전환 전후 동일 의미와 API 오류 시 실패 노출이다. 계획을 막는 업무 판단은 남지 않았고, 권고 1~3은 plan 작성 전에 한 줄씩 보완하면 충분하다.

**M01에서 소비자 발견으로 실제로 바뀐 곳.** context.md 36~42행의 결정과 대조했다.

- **R5 신설**: 보고서의 API 전환, 응답 실패 시 보고서 실패 노출, 기존 읽기 계정과 권한 범위 사용.
- **AC6 신설**: 저장소 전환 전후 같은 목록 의미와 신규 완료 반영, API 오류 시 옛 파일 대체 금지.
- **Design 소절 추가**: 미확인 상태에서 인계하지 않았던 경위, 미러·이중 쓰기를 거부한 이유, 호환성 확인을 전환 조건에 포함.
- **Constraints and scope**: 보고서 경로 변경의 범위 포함과 영구 JSON 미러의 범위 제외.
- **Open questions와 Flagged concerns**: Q1이 운영 담당의 확인과 결정으로 answered가 되고, 인계를 막던 우려가 근거와 함께 해소됨.
- **통합 검증 조건**: 최종 전환이 데이터·API·보고서·복구의 통합 검증을 따르도록 계획 경계에 반영.

**plan에 남은 실행 세부.** 스키마와 순서 열 이름, 잠금·트랜잭션 방식과 대기 상한 연결, 이행·내보내기 도구와 운영자 단계, 경합 재현 시험 환경, 보고서 코드 변경과 실행 시각 조정, 저장소 어댑터와 보고서의 작업 분할과 PR 순서, 전환 후 쓰기 여부 확인 방법, 운영 담당과 정할 SQLite 백업 방식이다.

**한계.** 해시를 재계산하지 못했고 테스트나 eval을 실행하지 않았다. git diff를 볼 수 없어 eval 03이 절 이름만 바꿨다는 주장은 현재 상태로만 확인했다. adopter 워크트리의 git 상태와 base_head 대응은 검증하지 못했다. 북극성 기준 기록 north-star-baseline.json은 읽었으나 그 html 해시도 재계산하지 못했다. 이 리뷰는 세 합성 예제와 양식·지침의 문서 설계 검토이며, 실제 정책 스킬 적용 실행이나 미래 대화의 에이전트 성능을 증명하지 않는다.
