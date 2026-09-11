# 독립 리뷰 조건과 진행

후보 r1: 2634f0792c57af172a30a735bf6804f864ea4907. candidate 파일 해시는 validation/r1-manifest.json.
두 리뷰어 모두 prompt.md를 받으며 다른 제안/리뷰 결과를 보지 않는다.

- Astra: 새 collaboration subagent spec_plan_candidate_review, gpt-6-astra/ultra, fork none.
  읽기 전용 조회와 본인 astra.md 작성만 허용. 공개 결과는 astra.md.
- Fable: 새 Claude Code CLI, fable/max, safe-mode, Read만 허용, permission dontAsk.
  시작 시 429 Fable 한도, 사용량/비용 0, 실제 후보 리뷰 없음. fable-unavailable.json 보존.
- 대체: 사용자에게 모델 대체 선택을 비동기로 요청한 뒤 답변 없이 유용한 작업을 계속했다.
  60초 넘게 기다린 후 권장 기본 가정을 밝히고 같은 prompt로 opus/max 새 CLI 검토를 요청했다.
  사용자가 이어서 “클로드 코드 오퍼스 ... 추론래밸은 적당히”라고 지정했다. 실행 중 opus/max를
  SIGINT로 중단하고 새 opus/high 호출로 조정했다. 중단 결과·비용도 보존한다.
  실제 모델/결과는 해당 응답 메타데이터로 확인하며 Fable 완료로 표시하지 않는다.

제품 구현·설치·스킬 자연 호출 검증은 이번 리뷰 범위가 아니다.
