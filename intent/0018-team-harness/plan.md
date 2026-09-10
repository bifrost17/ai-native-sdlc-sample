# Plan: 설치한 팀 진입점에서 독립 검토와 자동 보완 검증
Upstream: spec.md@a76e107f0676d80d6ed4e4468ef00053680e35a6. Status: draft.
root가 사용자의 목표 달성 위임으로 설계·구현·실험을 진행한다.

## Files that change
- team-harness/sdlc_claude.py, reviewer.md, install.py, README.md(new): 별도 실행 진입점·검토 지침·사용자 설치와 사용법.
- tests/test_team_harness.py(new): 실제 의미 판정을 흉내 내지 않는 실행 순서·오류·상한·설치 회귀 시험.
- README.md, docs/BOUNDARY.md: 수정한 목표와 템플릿/팀 실행 도구/사람의 경계.
- docs/experiments/datasets/v4/manifest.json, cases.json(new): 같은 F02 기반에서 정상·누락·형식 수정·대기 사례.
- docs/experiments/0018-team-harness.md(new), docs/experiments/README.md: 실제 실행·판정·비용·한계와 색인.
- docs/research/artifact-sync-controls/README.md: 제안 중 구현한 부분과 실제 적용 범위.
- docs/verification/north-star-playbook.html, README.md, INDEX.md, CHAPTERS.md: 새 검토 실행 근거와 주석.
- intent/0018-team-harness/{intent,spec,plan}.md: 이 변경의 사슬.
- 제품·공개 대화·검토 입출력은 별도 실험 clone/브랜치에 보존한다. 사용 템플릿 add296d는 바꾸지 않는다.
- 영구 설치 대상은 ~/.local/share/intent-sdlc-harness 및 ~/.local/bin/sdlc-claude, 실행 기록은
  ~/.local/state/intent-sdlc-harness다. 개인 Claude 설정이나 PATH는 수정하지 않는다.

## Order of work
1. 작은 CLI가 개발 응답→독립 검토→필요한 같은 세션 보완을 소유한다. 정상 대기와 통과만 반환하며
   오류·미해결은 명시적으로 인계한다. 코드에는 문서 의미나 승인 상태를 판정하는 규칙을 넣지 않는다.
2. 실행 계층을 모의 백엔드로 시험한 뒤 영구 설치한다. 별도의 실제 Sonnet/low로 의미 판정을 검증한다.
3. 고정 F02 PR1 및 사용 후보를 기반으로 업무 대화를 진행한다. HUMAN은 업무 조건·수락·Git을 맡으며
   문서 갱신을 상기하지 않는다. 예전 실제 누락과 형식만 수정한 입력도 독립 검토한다.
4. 자연 발생 누락이 없어도 자동 보완을 관측하도록 한 실행의 개발 응답 뒤 문서를 원래 판으로
   되돌리는 통제된 결함을 주입할 수 있다. 주입은 실험 측에서 한 번만 수행하며 AGENT 프롬프트나
   검토 판정은 변조하지 않는다. 자연 발생과 주입 결과를 별도로 기록한다.
5. 최소 한 실제 자동 resume과 최종 재검토를 확인한다. 수락 spec을 먼저 커밋하고 관련 plan·구현을
   함께 커밋한다. 정상 질문·수락 대기·문서 영향 없는 변경도 검토한다.
6. 제품 시험·독립 동작·기존 시험과 fixture 보존을 확인하고 원본 기록·입력 해시·실험 커밋을 고정한다.
7. 독립 verifier가 제작 make check, 계획/변경 양방향, 이전 사슬의 자체 핀, 나쁜 hook 입력과 실제
   실험 근거를 확인한다. 북극성 원문·179개 ID·고정 항목은 유지하고 새 관측만 반영한다.

## Risks
개발자 주장만 믿는 검토, 검토 오류를 통과로 처리, 대기를 누락으로 오판, 조용한 입력 잘림,
오래된 검토 결과 사용, 반복 상한 뒤 마지막 판 미검토, 통제된 결함을 자연 실패로 제시하는 위험.
직접 claude 호출은 적용 범위 밖이고, 모델의 무오류나 조직 권한 분리는 보장하지 않는다.

## Proof
설치 파일 해시·실제 버전, 공개 업무 대화와 독립 검토 입력/결과·개발 도구 실행·resume·비용,
문서/코드 diff와 spec 참조·같은 커밋, 제품 unittest 및 독립 CLI, 이전 fixture/시험 보존,
make check 전체 출력과 verifier 네 부분 보고. 실제 대화는 기본 60분/12 HUMAN 턴 안에서 진행한다.
