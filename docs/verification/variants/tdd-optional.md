# TDD 선택형의 의도한 차이

2026-09-12. [tdd-optional](../../../tdd-optional/README.md)은 검증 방식을 작업별로 선택한다.
최초 분리 당시 새 패키지 이름은 `intent-sdlc-skills-optional`, 버전은 0.1.0이었다.
후속 0.1.1의 설계·검증은 [선택형 SDLC 설계 검증](optional-sdlc-design.md)에 기록한다.
아래 실행 사례는 최초 분리판의 근거로 보존하며 후속판의 실행 결과로 승계하지 않는다.

후속 실제 OpenCode 실험은 [0029](../../experiments/0029-optional-opencode.md)에 있다. 0.1.1 전체 F04는
JSON 문서 선행 갱신을 놓쳤으며 0.1.2의 진입/검토 안내 보완 후 새 부분 세션에서 문서 선행·HUMAN이
선택한 구현 후 테스트·26시험·fresh55명령/9판정을 확인했다. 검토자의 과거 기록 오판은 HUMAN이 복구했다.
아래 최초 분리판의 미검증 범위와 구분하고, 자연적인 비TDD 선택·0.1.2 전체 사슬·방식 우월성으로 확대하지 않는다.

그 뒤 [0030 Sonnet r02](../../experiments/0030-optional-sonnet.md)는0.1.2의 전체 사슬을 실행했다.
일반 구현 후 테스트와 R6 한 경계의 TDD를 자연 선택했고, 후속 JSON에서 문서 선행·같은 커밋을 관측했다.
통합·fresh25시험·55명령/9판정 통과다. 계획 모순·두 검토 누락·실행 기록은 HUMAN이 복구했으며
설치16개 전체의 자연 사용이나 무오류 절차 통과는 아니다. 위0029의 한계를 소급해 지우지 않는다.

[0031](../../experiments/0031-optional-feedback-adoption.md)은 팀0.1.3의 짧은 채택 안내만 연결한
새 부분 세션에서 sdlc-feedback 실제 사용·문서 선행/같은 커밋·최신 native 검토와 대기를 관측했다.
통합·fresh26시험·55명령/9판정 통과 후1회에서 종료했다. 일반 정책·스킬 본문을 더 조이지 않았다.

[0032 Codex Luna](../../experiments/0032-codex-luna-run.md)는0.1.3 전체 실행에서 spec/plan 선행은
지켰지만 intent 제약과 실제 상위 문서 참조를 놓쳤다. 원본과 HUMAN 복구를 보존하고0.1.4에서
기존 feedback/verifier의 두 비교 질문을 명확히 했다. 새 JSON 부분 실행은 intent→spec→plan→
RED→GREEN·같은 커밋·fresh native Sol 검토와 대기를 관측했다. 경미한 표 참조 한 칸은 HUMAN이
정정했고, 통합판의 새 복제본9시험·55명령/3추가 판정 통과 후 종료했다. 새 훅·검사기·승인 단계는
없다. 첫 전체 실행의 단계 인계 공백·마지막 검토 중단, named custom-agent 자동 적용 미검증과
전체0.1.4 사슬 미검증은 유지한다. 프로젝트별 Codex 설치16개와 자연 사용의 관측도 구별한다.

| 영역 | 반영한 차이 |
|---|---|
| PROJECT-POLICY·CLAUDE·PROCESS·REVIEW | TDD·동작별 구현 후 테스트·기존 테스트 활용·혼합을 허용. TDD 미선택 자체에 예외 승인 요구 없음 |
| plan·계획 작성 스킬 | 방식과 이유, 구현에서 독립된 기대, 동작별 구현·검증 순서를 연결 |
| 계획 예시 | F01은 구현 후 테스트, B01·F03은 선택 이유가 있는 TDD, W01은 서버 TDD와 UI 구현 후 테스트, M01은 혼합 |
| TDD 스킬 | 사용자가 요청하거나 plan에서 TDD를 선택한 작업에 적용. 선택한 뒤에는 의미 있는 실패·통과 근거 유지 |
| feedback·Claude/OpenCode 검증자 | 선택한 방식과 실제 증거를 대조. TDD 미사용만으로 결함 판단하지 않음 |
| 평가·패키지 | 기본형과 다른 식별자·로드 경로·출력 폴더. prompt와 채점 자료 모두 선택한 namespace 사용 |

intent/spec 양식은 기본형과 동일하다. 인수 조건·독립 기대·회귀 보호·영향 문서 갱신·사람의 수락 및
병합·운영 권한은 유지한다. 버그의 진단 재현과 영구 회귀 테스트 선작성을 구분하며, 사후 시험의
기준판 재생을 원래 TDD를 수행했다는 증거로 바꾸지 않는다.

별도 제품 사본 두 개에서 구현 후 테스트와 TDD를 각각 명시한 실제 작업을 수행했다.
각 7개 시험과 별도 계산 검증이 통과했다. 구현 후 테스트 작업에서 추가 승인을 요구하지 않았다.
[구현 후 테스트 기록](evidence/optional-after/evidence.md), [TDD 기록](evidence/optional-tdd/evidence.md),
[독립 최종 검증](evidence/verification.json). 후자는 단일 함수에 대한 한 RED→GREEN 주기였으며,
복잡한 작업의 세분화나 자연 선택의 일반적인 정확성을 검증하지 않는다.

선택형이 다른 방식보다 우수하다는 결론이나 기본형의 과거 통과를 승계하지 않는다. 유료 native 평가·
실제 설치·자연어 선택은 미검증이다. [전체 검증 범위와 남은 한계](README.md),
[독립 구현 검토](independent-review.md), [연구 근거와 불확실성](../../research/tdd-vs-test-after/README.md)
