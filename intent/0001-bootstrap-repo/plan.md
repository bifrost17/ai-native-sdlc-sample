---
id: 0001-bootstrap-repo
kind: plan
status: draft
upstream: spec.md@68a5af693203417fa674c7d740afb40b91a8ad82
---
# Plan: 사슬을 기계가 강제하는 샘플 레포 (from intent 0001)

## Files that change
이 브랜치에 실제로 들어온 파일만 적는다. 나머지 요구(R2 훅 · R4 지표 · 문서 5종 ·
스킬 · 밴드 검출기)는 형제 PR 이 지고 있고, 그 PR 들이 머지되면 이 목록에 붙는다.

- docs/DESIGN.md
- docs/STATUS.md
- docs/SOURCE-OF-TRUTH.md
- scripts/check_all.sh
- scripts/check_artifacts.py
- templates/intent.md
- templates/intent-defect.md
- templates/intent-incident.md
- templates/spec.md
- templates/plan.md
- tests/fixture_harness.py
- tests/run_fixtures.py
- tests/test_check_artifacts.py
- intent/0001-bootstrap-repo/intent.md
- intent/0001-bootstrap-repo/spec.md
- intent/0001-bootstrap-repo/plan.md
- .github/workflows/check.yml
- Makefile
- README.md
- LICENSE
- NOTICE

## Order of work
1. W0 골격 — 비공개 레포 · 설계안 · 라이선스와 출처 · 게이트 정본과 CI. 첫 게이트부터
   실질 검사를 넣는다(빈 통과로 시작하면 그 뒤로 아무도 안 본다).
2. W1 강제층 — 검증기를 red 픽스처부터 쓰고(뚫린 자리 8종), 템플릿 5종, 상태 지면,
   훅 5개와 배선 시험, CI 차단. 여섯 레인이 파일을 겹치지 않게 나눠 병렬로 간다.
3. W2 사슬 — 0001(메타)과 0002(기능)를 **실제 순서로** 커밋한다. 여기서 설계 결함이
   드러났다: 검증기가 브랜치 위의 accepted 를 전면 금지하면 승인 PR 이 스스로 빨개져
   사슬이 한 칸도 못 간다. D16 예외를 시험 먼저 세우고 닫은 뒤에 사슬을 태운다.
4. W3 결함 사슬 — 밴드 검출 → intent 초안 → 실패 시험 먼저 → 구현. 지표와 문서 5종.

## Risks
가장 큰 위험은 「강제하는 척」이다. 게이트가 늘 그린이면 그것이 강제의 증거가 아니라
아무것도 안 재고 있다는 증거일 수 있다. 그래서 게이트 안에 **반드시 빨개야 하는 것**을
상주시킨다(템플릿은 rc=1 · red 픽스처는 지정 code). 두 번째 위험은 검증기를 무르게
만들어 통과시키는 유혹이다 — 사슬이 검증기를 통과 못 하면 문서를 고치지 검증기를
고치지 않는다. 예외를 하나 열 때는 폭을 한 줄로 못 박고 열어 두지 않는 자리를 표로
적는다. 세 번째 위험은 detached HEAD 처럼 검사가 아예 안 도는 자리가 조용히 비는
것이다 — 판정 포기를 note 로 출력해 셀 수 있게 만든다.

## Proof
- AC1 ← tests/test_check_artifacts.py 의 RedFixtures · GreenFixtures · Templates
  (픽스처 디렉터리에서 자동 발견 · EXPECT 의 code 다중집합과 정확 대조) ·
  tests/run_fixtures.py
- AC2 ← tests/test_hooks.sh · tests/test_wiring.sh
- AC3 ← .github/workflows/check.yml 이 부르는 scripts/check_all.sh 의 요약 줄과 종료 코드
- AC4 ← tests/test_metrics.py
- AC5 ← scripts/check_all.sh 의 사슬 검사(intent/*/ 전량 rc=0, 없으면 SKIP)와
  사슬 자체 — 이 세 파일이 실제 순서의 커밋으로 남아 있는 것이 증거다

## Options not taken
**설치 키트**(`npx create-…` 류로 남의 레포에 파일을 뿌리는 형태)를 만들지 않았다.
키트는 「설치했다」를 성공으로 보고하는데, 강제가 살아 있는지는 설치가 아니라 **깨뜨려
보는 것**으로만 확인된다. 실측한 참조 레포 중 설치기를 둔 곳들이 정확히 그 자리에서
스캐폴드만 남기고 배선이 0이었다.

**플러그인 형태**(마켓플레이스 배포)도 고르지 않았다. 조직 계정이 필요해 읽는 사람이
재현할 수 없고, 재현할 수 없는 시연은 이 레포의 목적과 어긋난다. 대신 관리형 설정은
비활성 예시 파일과 함정 주석으로 남겨 이월 원장에서 승격 조건을 단다.

**별도 승인 원장 파일**(해시 체인)도 버렸다. 원장은 재체인으로 위조되고, 그때 도구는
rc=0 을 돌려준다. 승인 기록은 git 과 PR 이라는 이미 있는 사실 위에 둔다.

## Parallelisable
W1 의 여섯 레인은 파일이 겹치지 않아 동시에 간다(검증기 · 훅 · 스킬 · 밴드 · 문서 ·
지표). 병렬이 안 되는 자리는 사슬이다 — 0001 의 intent → 승인 → spec → 승인 → plan 은
상류 sha 를 서로 물고 있어 순서가 곧 계약이다. 이 순서를 어기면 검증기가 먼저 운다.
