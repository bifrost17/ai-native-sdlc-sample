# HUMAN decisions — R02

HUMAN은 Codex root(모의 제품 책임자), AGENT는 Claude Code Sonnet·low다.
T1: 수락된 F02 PR2 구현을 허용하고 프로젝트 지침을 먼저 실제 읽도록 했다.
T2: 파일 출력 요구를 PR2 범위로 승인했다. 문서 갱신은 따로 지시하지 않았고 AGENT가 spec/plan을 갱신했다.
T3: HUMAN은 개정 spec을 1ce4506a7e19e43bf737a43b66bef19891a13b7d로 커밋·수락했다.
SHA만 전달하자 AGENT가 plan Upstream에 연결했다.
별도 설계/제품 리뷰에서 파일 존재 확인과 쓰기 사이 생성된 동료 파일을 덮어쓰는 결함이 발견됐다.
독립 재현에서도 rc0·동료 파일 유실이 관측됐다. 이 시점의 제품은 통과가 아니다.
T4: 파일 보존이라는 업무 동작의 결함을 피드백했다. AGENT는 배타적 생성으로 고치고 spec R9/Design과
plan을 함께 갱신했다. 문서 갱신을 따로 지시하지 않았다.
T5: 개정 spec 8dea18c6f1a6def4c3a645b70331d762a7f7082c를 HUMAN이 커밋·수락했고 AGENT가 plan 참조를 갱신했다.
T6: 기존 시험이 놓친 경쟁 결함의 회귀 시험을 요청했다. AGENT는 결정론적 재현 시험을 추가하고
결함 구현에서 rc1/AssertionError: 0 != 2, 수정 구현에서 전체 12/12 통과를 실제 확인했다.
T6는 이미 합의한 R9/plan 검증을 구체화한 것으로 추가 spec/plan 편집이 없어도 중요한 누락은 아니다.
독립 verifier도 같은 판단이며 과도한 형식 갱신을 요구하지 않는다.

HUMAN의 CLI 15회와 독립 verifier의 전체 시험·CLI·경쟁 재현·기존 AST/fixture 대조가 통과했다.
HUMAN은 tracker.py, tests/test_tracker.py, README.md, 개정 plan.md를
7c7f9e4746f44f30a2735be53b571b89b3b11fc5 한 커밋에 담았다. spec 수락 8dea18c가 바로 부모다.
판정: 요구 변경·설계 수정에서 문서 개정/인계 관측 통과. 제품은 초기 결함 발견 후 복구·회귀 검증 통과다.
초기 제품 결함이나 HUMAN의 테스트 피드백을 숨겨 한 번에 자율 완료했다고 주장하지 않는다.
Git은 HUMAN이 실행했다. 새 PR·통합·배포는 이 부분 실험에 없다.
