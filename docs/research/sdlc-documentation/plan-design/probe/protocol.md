# F02 계획·새 세션 구현 부분 실험

데이터는 기존 F02 v2.0.0 seed102와 v1 코드/세 시험을 사용한다. 입력과 HUMAN 결정·oracle은
docs/experiments/datasets/v2/F02에 보존돼 있다. 이번에는 Plan 이후를 관측하므로 root가 합의한
intent/spec을 단계별 커밋으로 제공한다. 요구 발굴·질문 능력이나 전체 Discover→Maintain 평가는 아니다.

사용 후보 95c0933에서 초기 제품 codex/exp-0022-base@34f41ee를 만들고, 로컬 file:// shallow
clone의 main을 제품 통합 기준으로 쓴다. 제작 main과 원격은 바꾸지 않는다. 개발 branch는
제품 main에서 파생하며 필요하면 공유 계획만 먼저 통합한다. 최종 refs는 제작 저장소에도 보존한다.

HUMAN은 기존 PERSONA.md에 따라 업무 오너·검토 엔지니어를 모사하는 root, AGENT는 실제
Claude Code Sonnet/medium이다. 계획의 선택형 스킬을 명시적으로 선택한다. 자동 발견·설치 성공을
측정하는 것이 아니다. 고정 대화 대본을 만들지 않으며 실제 출력과 파일을 읽고 후속 질문/결정을 한다.

관찰할 것:
- 문서 SHA/수락과 현재 코드를 읽고 결과·순서·PR·Proof가 연결되는 계획을 작성하는가.
- plan 작성 대화를 받지 않은 새 세션이 plan과 선언된 문서/정책/코드만으로 첫 기능을 구현하는가.
- 첫 변경만 제품 main에 통합해 사용할 수 있고, 후속 작업은 그 main에서 시작하는가.
- 실행 중 계획 판단이 바뀌면 해당 문서와 이유를 관련 구현 커밋에 보존하는가.
- 각 통합의 기존 동작·새 계약·두 기능의 결합을 실제 시험과 HUMAN oracle로 확인하는가.

증거는 CLI prompt/invocation, 실제 모델·세션 ID, 필터링한 tool I/O/최종 결과, Git refs와 시험 출력이다.
비공개 추론은 저장용 공개 로그에서 제외하고 제외 개수와 raw/stored 해시만 남긴다. root가 고친
부분은 assisted recovery로 구별한다. 계획에서 시험을 나열한 것을 실제 통과로 바꾸지 않는다.

상한은 작은 두 기능과 필요한 피드백·회귀다. hosted PR·CI·배포, 병렬 개발 실행, 실제 M01 이행은
하지 않는다. local merge를 PR-equivalent integration으로만 표시한다. R1 이후 양식이 바뀌면
실험에 사용한 판과 최종 후보를 구별하며 영향 있는 변경은 추가 확인한다.
