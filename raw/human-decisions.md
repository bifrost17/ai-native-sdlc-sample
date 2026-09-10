# HUMAN decisions — R01

HUMAN은 Codex root(모의 제품 책임자), AGENT는 Claude Code Sonnet·low다.
T1: 앞서 수락된 F02 PR2를 구현하도록 허용하고 프로젝트 지침을 먼저 실제 읽도록 했다.
T2: 내부 자동화의 JSON 출력 요구를 이번 PR2 범위로 승인했다. 문서 갱신은 따로 지시하지 않았다.
T2 결과: AGENT가 spec R8/AC9·설계와 plan의 편차·검증을 스스로 갱신했다.
T3: HUMAN은 개정 spec이 업무 조건과 맞음을 읽고 5e6cdd68ed87a7dfdab76b823edafe09a10c9278로
커밋·수락했다. 수락 SHA를 전달하자 AGENT가 plan의 Upstream 문단에 연결했다.
HUMAN의 제품 시험 12개·별도 CLI 관측 13개, 독립 verifier의 시험·동작·문서 대조가 통과했다.
HUMAN은 tracker.py, tests/test_tracker.py, README.md, 개정 plan.md를
9f42449bc786535ceaa1d52df4fd34315a88c842 한 커밋에 담았다. spec 수락 커밋이 바로 부모다.
plan은 원래 SHA와 새 수락 SHA·범위를 같은 문단에 적었다. 단일 SHA 형식과 다르지만 최신 개정과
수락 범위는 명확하여 누락으로 판단하지 않았다. 형식 검사를 새 요구로 추가하지 않는다.

판정: 이번 조건에서 문서 개정·인계와 제품 동작 통과. 이전 실패나 일반 성공률을 대체하지 않는다.
Git은 HUMAN이 실행했다. 새 PR·통합·배포는 이 부분 실험에 없다.
