# Spec: 담당자 정확 일치 목록과 열린/완료 건수
Upstream: intent.md@8a43246. Status: draft.
References applied: CLAUDE.md, PROJECT-POLICY.md와 EXPERIMENT.md의 로컬 실험 결정.
HUMAN root가 intent 8a43246을 다음 단계 입력으로 수락했다. 문제·순차 인도·보존 범위가 F02와 맞다.

## Requirements
- R1. list --owner ID는 owner 문자열의 정확 일치, 원래 순서, done 포함이다. 무옵션 list는 전체다.
- R2. summary [--owner ID]는 같은 선택 규칙으로 open/done 건수를 두 줄 출력한다.
- R3. 목록/요약은 바이트를 바꾸지 않고 기존 show/complete·출력 열·저장 필드를 유지한다.

## Acceptance criteria
각 사례는 requests.json의 새 복사본에서 확인한다.
- AC1 → R1,R3: list --owner hana는 R-101/R-103 순서. HANA/nobody/-는 빈 stdout·rc=0.
  무옵션 list는 R-101/102/103/104 네 행을 기존 열·순서로 출력한다. 모두 파일 바이트가 같다.
- AC2 → R2,R3: summary는 `open\t3\ndone\t1\n`, --owner hana는 `open\t1\ndone\t1\n`,
  없는 담당자는 `open\t0\ndone\t0\n`이다. escape는 탭/개행. 모두 rc=0·파일 동일.
- AC3 → R2,R3: complete R-101 후 hana 요약은 open=0/done=2. 요약은 이 상태를 바꾸지 않는다.
  기존 show/complete의 없는 ID 오류·정상 변경·반복 시 바이트 보존을 유지한다.

## Design
argparse와 현재 JSON 읽기/display 흐름을 재사용한다. null은 어떤 문자열 담당자와도 일치하지
않는다. 선택 조건을 두 명령에서 같은 의미로 적용한다. helper 이름·시험 파일 배치는 plan이 정한다.
DB·캐시·서버·추가 의존성은 불필요하다. USAGE.md는 현재 사용법 설명이다.

## Constraints and scope
동료에게 목록부터 먼저 전달한다. 정규화·미배정 선택·저장 형식 변경·외부 통신은 범위 밖이다.

## Open questions
F02 HUMAN의 담당자·요약·보존 결정 D1–D4가 반영됐다. 구현을 막는 미결 제품 결정은 없다.

## Flagged concerns
없음. 가상 데이터만 쓰는 로컬 CLI이며 실제 조직의 정책 검토 성공으로 확대하지 않는다.
