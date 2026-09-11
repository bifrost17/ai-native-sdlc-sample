# Claude Code Fable — R1

CLI final result extracted verbatim. The stored `fable-r1.jsonl` omits private reasoning blocks.

## 판정: PASS

이 범위에서 중요한 차단 사유를 찾지 못했다. 완벽하다는 뜻도, 조직의 승인도 아니다. 세 예시는 입력에 없는 수치·시스템·담당자·원인을 만들지 않았고, 입력이 "아직 답하지 않았다"고 한 항목은 모두 질문으로 남아 있다. 요청자의 제안과 확정 제약이 구별되고, 작성자·담당자를 모르는 경우가 사실처럼 꾸며지지 않았다.

**읽은 파일**
- 후보 5개: `templates/intent.md`, `.claude/skills/capture-intent/SKILL.md`, `examples/feature.md`, `examples/bug.md`, `examples/incomplete-ticket.md`
- 보조: intent-design의 `examples-inputs.md`, `alternatives.md`, `README.md`, `review-request.md`, `reviews/candidate-r1.json`, anthropic-playbook의 `evidence/intent-example.md`, `README.md`
- 원문 대조: `docs/verification/north-star-playbook.html` 340~440행, 영문 원문 `docs/research/intent-template/raw/03-lesson-capture-intent.html` 187~228행
- 입력 원본: `docs/experiments/datasets/v1/F01/public.json`, `B01/public.json`. human.json은 읽지 않았다.
- 소비자·기준선: `tests/test_skill_template.py`, `scripts/emit_intent.py`, `tests/test_bands_workflow.py`, `evals/cases/01-intent-placeholder.json`, `docs/work/baselines/capture-intent.SKILL.md`, `docs/ADOPTING.md` 13행, `intent/0020-intent-form/` 세 문서
- 읽지 않은 것: 다른 리뷰어의 보고서, `reviews/fable-r1-*` 산출물, human.json

## 발견

**중요 발견: 없음.** 아래는 비차단 메모이며 수정 여부는 root의 판단이다.

- **`templates/intent.md:1`, `SKILL.md:38` 제목 안내.** 기준선의 "해결책이 아니라 주제"라는 문구가 "요청자가 바라는 변화"로 바뀌며 사라졌다. I03처럼 제보자가 해결책을 말한 요청에서 제목이 "Redis 캐시 도입"이 될 수 있고, 그러면 사슬 전체가 설계 전 기술 선택의 이름으로 불린다. 예시 `incomplete-ticket.md:1`과 스킬의 제안 보존 지침이 완화하므로 차단은 아니다. 최소 수정은 제목 자리표시자에 "해결책 이름이 아니라 바라는 결과"라는 한 구절이다.
- **`feature.md:16` 사실의 제약화.** 입력 카드는 표준 라이브러리만 쓰고 외부 연결이 없다는 현재 환경 사실인데, 예시는 "도입하지 않는다"는 금지로 굳혔다. 요청자가 확인하지 않은 조건이 확정 제약으로 읽힐 수 있다. 작은 사내 CLI에서 자연스러운 해석이고 요청자가 고칠 수 있어 차단은 아니다. `bug.md:19`처럼 사실 형태로 두거나 요청자 확인 후 유지하면 된다.
- **`bug.md:25` 추가 질문.** ID 내부 공백·대소문자·공백만 있는 입력은 입력에 없던 쟁점이다. 질문으로 남겼으므로 발명이 아니고 분석가 질문의 범위 안이다. 다만 대소문자는 요청자의 문제 밖으로 범위를 넓힐 수 있어, 답이 없으면 범위 밖으로 닫는 편이 자연스럽다. 조치 불필요.
- **생략된 사소한 사실.** `feature.md`는 입력의 "담당자 없음은 null" 사실을, `bug.md`는 "기존 시험은 baseline에서 통과" 사실을 싣지 않았다. 둘 다 저장소에서 바로 확인되는 세부라 intent 손실로 보지 않는다.
- **`SKILL.md:64` 참조.** "0002 and 0007 both hit this"는 이 브랜치의 intent 폴더에 없는 실험 사슬을 가리킨다. 기준선에서 그대로 온 문구라 이번 변경의 결함은 아니다.
- **`incomplete-ticket.md:10` 표현.** "적합성과 원인은 설계 전에 살펴봐야 한다"는 인계 메모로 읽히지만 절차 지시로도 읽힐 수 있다. 그대로 두어도 무방하다.

**확인한 사항**
- `SKILL.md` 7~12행의 인용 세 개와 227행 참조는 영문 원문의 203·204·224·227행과 일치한다. 원문의 "what is wanted, why, and under which constraints", 다섯 항목의 예시 목록, 원저자 정정 단계가 양식과 스킬에 대응한다.
- 원문 예시의 Proposed outcome이 "in the portal"이라는 방향을 포함하므로, 제안을 보존하되 확정 제약과 구별한다는 해석은 원문에 근거가 있다.
- 템플릿 본문과 `SKILL.md` 38~54행 펜스는 눈으로 대조해 동일하다.
- `scripts/emit_intent.py:24`는 "## " 제목만 정규식으로 읽으므로 새 빈 줄과 한국어 자리표시자의 영향을 받지 않는다. evals 케이스 01의 검사도 제목·Author 줄·‹ 문자 기준이라 영향이 없다. alternatives.md의 emitter 주장은 사실이다.
- 원저자 정정은 `SKILL.md` 61~64행이 다루고, 정정 반영 시 해당 열린 질문을 닫도록 되어 있다. 후속 단계 경계는 77~83행이 지킨다.

## 인계 읽기 점검

- **F01 `feature.md`.** 원하는 것과 이유: 담당자 ID로 목록을 좁혀 그 담당자의 요청만 보고 싶다. 섞인 목록에서 눈으로 고르는 수고 때문이다. 지켜야 할 것: 기존 세 명령과 JSON 필드, 조회는 파일을 바꾸지 않음, 표준 라이브러리, 업무 코드 2~4파일. 제안됐지만 미결: 명령 사용법. 기술 제안은 없다. 미확인: 완료 포함 여부, 파일 순서 유지, 미배정 처리, ID 일치 방식. 모호함: "담당자 ID로"가 필수 조건인지 표현 방식인지 명시되지 않았으나 세 번째 질문이 부분적으로 덮는다.
- **B01 `bug.md`.** 원하는 것과 이유: 앞뒤 공백이 붙은 복사 ID로도 조회되게 하고 싶다. 붙여 넣는 일상 사용이 실패해 매번 손으로 고치기 때문이다. 지켜야 할 것: 저장 ID와 데이터 행 보존, 기존 시험 보존과 재현/회귀 시험 선행, 표준 라이브러리, 2~4파일. 제안됐지만 미결: 없음. 원인도 추정하지 않았고 없다고 밝혔다. 미확인: 탭·줄바꿈 등 다른 공백, complete 적용 여부, 내부 공백·대소문자·공백만 입력. 모호함 없음.
- **I03 `incomplete-ticket.md`.** 원하는 것과 이유: 검색을 기다리다 업무가 끊기는 일을 줄이고 싶다. 지켜야 할 것: 확인된 것 없음. 제안됐지만 미결: Redis 캐시, 캐시 부재라는 원인 추정. 미확인: 어느 검색·시스템·팀인지, 대기 시간, 개선 판단 기준, 제약, 제보자 신원과 연락 경로, 답변 담당. 모호함 없음. 모르는 것이 모른다고 적혀 있다.

**남은 한계.** 셸 도구가 없어 `candidate-r1.json`의 SHA256을 재계산하지 못했고, 작업 트리의 현재 파일을 읽었다. 시험은 실행하지 않았으며 이 판정은 읽기 점검이다. human.json과 다른 리뷰어의 보고서는 읽지 않았다. 스킬이 실제 대화에서 질문을 얼마나 비례적으로 하는지는 이 리뷰로 알 수 없다.
