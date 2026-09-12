# Spec input: 담당자 목록을 먼저 전달하고 상태 요약을 잇기

합성 예시용 합의 입력. 제작 데이터셋 F02 v2의 공개 카드와 HUMAN D1–D4를 정리했다.
실제 승인 문서나 현재 회사 요구가 아니다. 코드 맥락과 표본은 [context.md](context.md)를 읽는다.

## Requirements and acceptance
- R1/AC1: 목록부터 먼저 사용한다. list --owner hana는 R-101(open), R-103(done)을 순서대로
  출력한다. 무옵션 list는 네 행·원래 열을 유지한다. HANA/nobody/문자열 -는 빈 stdout, rc=0이다.
- R2/AC2: 후속 summary [--owner ID]는 목록과 같은 담당자 선택을 쓴다. stdout은
  `open\t1\ndone\t1\n`(hana), `open\t3\ndone\t1\n`(전체),
  `open\t0\ndone\t0\n`(없는 담당자)다. 여기 escape는 실제 탭·개행을 뜻한다. rc=0이다.
- R3/AC3: 조회와 요약은 원본 바이트를 보존한다. 새 복사본에서 complete R-101 후 hana의 요약은
  open=0, done=2가 되며 요약 자체는 쓰지 않는다. 기존 show/complete의 오류·반복 동작을 유지한다.

## Design and scope
기존 JSON 읽기·display·argparse 흐름을 재사용한다. 두 명령의 정확 일치 선택 의미를 공유한다.
함수 이름·시험 파일 구성은 구현 계획에서 정한다. 외부 서비스·새 저장 필드·정규화·미배정 옵션은
추가하지 않는다. 두 기능을 함께 완성할 때까지 첫 기능 전달을 미루지 않는다.
