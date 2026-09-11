# Plan: intent 양식 작성과 Astra·Fable 독립 리뷰
Upstream: spec.md@8269b15. Status: draft.
사용자의 root 작성·리뷰 위임으로 draft 위에서 진행한다. 실제 승인 표시는 기존 merge 정책을 따른다.

## Files that change
- intent/0020-intent-form/{intent,spec,plan}.md: 제작 변경의 기록.
- templates/intent.md: 사용 양식.
- .claude/skills/capture-intent/SKILL.md: 동일한 양식과 작성·질문 지침.
- .claude/skills/capture-intent/examples/{feature,bug,incomplete-ticket}.md(new): root 작성의 합성 완성 예시.
- docs/research/sdlc-documentation/intent-design/{README,examples-inputs,alternatives,review-request,review-record}.md(new):
  입력 출처·대안·설계 판단·범위·리뷰 기록.
- docs/research/sdlc-documentation/intent-design/reviews/(new): 후보 해시·리뷰 원문·CLI 기록·검사 결과.
- docs/research/sdlc-documentation/README.md: 설계 결과 링크.
- docs/verification/north-star-playbook.html: 관련 주석에 실제 설계 리뷰 근거만 덧붙임. 원문·기존 판정·과거 증거 보존.

## Order of work
1. 기존 자료와 Lesson 2, 현 양식·스킬의 소비자를 읽고 대표 입력에서 완성 예시를 작성한다.
2. 후보 두 형태를 비교해 선택 이유를 기록하고 양식·기존 스킬을 root가 수정한다.
3. 파일 해시를 고정하여 Astra/ultra와 Claude Code CLI Fable/max에 읽기 전용 독립 리뷰를 요청한다.
   동일 입력을 주고 상호 리뷰 결과는 최초 요청에 넣지 않는다. 원문·중요 발견·판정을 보존한다.
4. 지적을 검토해 root가 필요한 수정을 한다. 중요한 미해결 문제가 없고 같은 최종 후보를 두
   리뷰어가 PASS한 뒤 다음으로 간다. 관련 파일 변경 시 영향받는 검토를 다시 받는다.
5. 기존 make check와 skill quick validation, 독립 verifier의 계획·인접 흐름 대조를 실행한다.
   문서의 의미는 모델·사람의 검토로 판단하고 새 의미 검사기는 작성하지 않는다.
6. 리뷰·검사 범위를 기록하고 관련 북극성 주석과 연구 색인에 결과를 연결한다. 로컬 브랜치에
   커밋하여 보존한다. 외부 PR 승인·전체 개발 실험·양식 사용 성공률을 주장하지 않는다.

## Risks
해결 제안을 삭제하거나 필수 조건으로 승격, 근거·담당자 발명, 단순 요청의 과도한 질문,
형식상의 빈칸을 의미상 결함으로 오인, 이전 판 PASS를 수정된 파일에 적용하는 위험을 본다.
기존 emitter는 다섯 절의 위치에 의존하므로 구조가 바뀌면 소비자 조정이 필요하다.

## Proof
root 작성 입력과 예시 대조, 두 독립 리뷰의 실제 파일 읽기·최종 해시·PASS,
tests/test_skill_template.py의 test_skill_embeds_template_verbatim,
tests/test_monitoring.py의 기존 intent 출력 검사(실제 테스트 이름은 검사 시 확인),
make check 전체 출력, skill-creator quick_validate.py, verifier의 네 부분 보고.
