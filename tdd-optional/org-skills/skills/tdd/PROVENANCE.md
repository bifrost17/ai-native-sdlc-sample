# 자체 TDD 기본 예시의 출처

2026-09-11, 이 저장소 설계 패키지에서 root가 작성한 팀 기본 예시다. 외부 스킬 본문 복사본이 아니다.
Anthropic AI-native SDLC Playbook L9의 결함 재현·feedback loop와 팀의 새/변경 동작 test-first 의무를
구분해 적용했다. Superpowers, Matt Pocock, Kirjolab, Addy, ECC, Glebis 자료의 비교는
제작 저장소 docs/research/tdd-skills/ (보존 판 efa7339)에 있다. 절차 선택·비채택 이유와 실제 읽기 전용
검토 한계는 docs/research/sdlc-documentation/spec-plan-design/의 기록을 따른다.

설치 시 소스의 실제 Git 판 또는 플러그인 판과 로드 경로를 기록한다. 이 파일의 존재는 설치·자연 호출·
실제 TDD 준수 증거가 아니다. 스킬 본문은 자체 완결적이며 위 연구 자료를 매 구현마다 읽을 필요 없다.

2026-09-12: 계약·설계 또는 plan이 바뀌는 요청과 발견은 해당 test-first cycle 전에 영향
문서에 반영하도록 진입 연결을 보완했다. 새 승인·검사기를 추가하지 않고 기존 같은 구현 커밋과 발견
처리 지침을 유지한다.

## 선택형 파생 — 2026-09-12 / intent-sdlc-skills-optional 0.1.0

기본형 0.1.7에서 파생했다. TDD 적용을 작업/plan의 선택 범위로 한정하고 검토는 선택한 방식의 독립 기대·인수 조건·회귀 근거를 확인한다. 문서 현재화와 사람 승인 권한은 유지한다. 기존 실험 결과는 선택형 실행 증거가 아니다.
