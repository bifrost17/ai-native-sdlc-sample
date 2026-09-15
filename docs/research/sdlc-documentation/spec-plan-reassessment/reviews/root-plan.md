# Root: 실제 계획서와 우리 plan 비교

2026-09-11. 입력 판 `c09b5f1`. 다른 검토자의 결론 전에 P1/P2/P3와 P3 짝 설계를 읽고 기록했다.

## Read scope

- [조사 README](../../../exemplary-design-and-plans/README.md), methodology, implementation-plans, 원문 보관 안내.
- [P1 Dark Mode](../../../exemplary-design-and-plans/originals/P1-openverse-dark-mode.md) 전체.
- [P2 Ingestion Server Removal](../../../exemplary-design-and-plans/originals/P2-openverse-ingestion-server-removal.md) 전체.
- [P3 Auth Hardening plan](../../../exemplary-design-and-plans/originals/P3-superpowers-auth-hardening-plan.md)와 [짝 spec](../../../exemplary-design-and-plans/originals/P3-superpowers-auth-hardening-design.md) 전체.
- [북극성 원문 발췌](../../spec-plan-design/inputs/north-star-excerpts.md) L3/L4/L6/L7/L9와 북극성 V3/V4 관련 주석.
- 활성 templates/spec.md·plan.md, .claude 작성 스킬, 후보 양식·작성 스킬·설계/실행 블록·F01/B01/F03/M01 plan과 M01 설계 집합·전달안.

외부 프로젝트를 실행하지 않았다. 외부 PR·출시 이력은 제공받은 조사의 구분을 따른다. 이번 직접 관찰은 로컬 문서 내용이다.

## Verdict

plan의 네 정보 역할과 PR/공개/TDD 분리는 유지할 만하다. 우리 후보는 참고 문서보다 짧지만 중요한 규칙이 상당히 있다.
결함은 단순한 상세 부족보다는 **독자가 한 작업을 실행하기 위해 여러 표·문단을 다시 조립해야 하는 구조**, 그리고 **그 밀도를 적절히 조절하는 완성 예시의 편중**이다.
전체를 Superpowers식 코드 전문으로 확장하는 것은 잘못된 보완이다. PR 인도 지도 아래 작업별 읽기·수정·판정 정보를 모으는 방향이 적합하다.

## Findings

### RP1 — 작업을 따라 읽는 지역성이 더 필요함 (높음)

P3의 File Map → Task 2는 수정 파일, 공격/정상 조건, 예상 실패, 실제 명령, 최소 변경, 통과 조건이 한 곳에 있다.
P1은 전체 병렬 지도 다음에 각 작업을 읽으면 그 작업 이후 화면이 바뀌는지까지 알 수 있다.
우리 M01도 PR-A/B/C와 Proof 연결이 있지만, PR-B의 목록·완료·경합·import/export 동작과 테스트·명령·기대는
Files/Order/Proof/설계 정본에 분산된다. 계획을 읽는 에이전트가 그 연결을 다시 복원해야 한다.

반례: F01은 이미 실제 시험 이름·실패 이유·최소 코드 연결을 연속해서 썼다. M01도 P-B1/B2/B3를 명시하므로
실행계획이 없거나 TDD 순서가 없다는 판정은 틀리다. 필요한 것은 같은 정보의 배치 개선이다.

제안: 복수 작업 PR에서는 작업별로 목적·필수 입력/경계·파일·선행 동작 시험·최소 변경·통과 관측을 가까이 둔다.
Proof는 AC/회귀/전체 통합의 색인으로 쓰고 긴 기대를 복제하지 않는다. 작은 PR은 기존 F01처럼 몇 문장으로 충분하다.

### RP2 — 시작 문장이 작업의 기술적 이유를 충분히 안내하지 않음 (높음)

P1은 semantic color/palette swap 원리를 먼저 알려주므로 전역 색 이름 변경·CSS 변수화·토글·캐시 작업의 이유가 보인다.
P2는 현재 데이터 흐름을 풀고 그중 Distributed Reindex에 상세를 집중한다. P3은 Goal/Architecture/Tech Stack이 짧은 진입 문맥이다.
우리 M01의 제목·첫 문단은 병렬 준비/문서 판과 합성 한계는 알리지만, 왜 보고서를 먼저 API로 바꾸고 비활성 저장소를 준비하는지
설명은 독자가 정본과 PR 설명을 합쳐 도출한다. 후속 작업자가 흐름을 먼저 잡을 작은 문단이 있으면 좋다.

반례: plan에 설계 전체를 복제할 이유는 없다. M01 spec와 architecture에는 이미 책임·소비자 경계가 있다.
제안: plan 상단의 기존 짧은 문장에 '이 설계를 어떤 순서로 실제 제품에 넣는가'를 쓰고 spec의 결정 정본에 링크한다.
정책·연구 상태 안내가 제품 변화 설명을 압도하지 않도록 연구 메타데이터는 context/보존 기록에서 설명하고 예시에는 짧은 표시와 링크만 둔다.

### RP3 — 중간 인도 상태는 이미 강함; 빈 양식과 실제 UI 예시가 연결되지 않음 (중간)

P1의 '지금은 시각 변화 없음/시험 설정에서만 변화'와 'toggle만 숨겨도 저장 선호는 남음'은 구현 순서와 사용자 경험을 함께 다룬다.
우리 F03는 일반 OFF/TEST ON/PR1 임시 기대/PR2 전체/cleanup까지 있어 오히려 단계 구분이 더 엄밀하다.
따라서 feature flag 규칙을 새로 추가할 문제가 아니다. **이 강점을 화면·API·데이터에 적용한 실례가 없다.**
M01은 API·운영 사례지만 UI 상태·실제 사용 여정은 맡지 않는다. design-blocks의 UI 예시 칸도 '해당 제품의 실제 mock/계약'이다.

제안: 사내 웹 기능의 작고 완성된 spec→plan 쌍 하나를 대표 예시로 보강한다. 로딩/빈 결과/오류/권한·서버 판단·화면 노출·사용 흐름 검증을
그 사례에서 필요한 만큼만 보여준다. 모든 제품에 SSR/캐시/브라우저 저장을 요구하지 않는다. 기존 네 예시를 전부 대형화하지 않는다.

### RP4 — 외부 plan의 설계 내용을 우리 plan로 그대로 옮기면 spec 경계가 무너짐 (유지할 방어선)

P1 plan에는 색 체계·CSS 전략·ColorMode 타입·쿠키 저장이라는 설계 결정이 들어 있다.
P2 plan에는 EC2/ECS와 로컬 개발·관측·운영 선택이 들어 있다. 그 문서 체계에서는 자연스럽지만 우리의 spec 단계가 맡기로 한 내용이다.
P3 짝 spec는 threat model → current failures → bootstrap/Origin/경로 계약 → testing/AC를 설명하고,
plan은 구체 파일/테스트와 구현 코드까지 중복한다.

제안: 가져올 단위는 파일 이름이 아니라 정보 역할이다. 제품 계약·상태·핵심 기술 선택은 spec 정본,
실제 파일·준비 환경·실행 순서·TDD·PR·검증은 plan. 중요한 알고리즘/계약 의사코드는 spec에,
테스트 fixture/assertion 조각은 plan에서 판단을 정확하게 하는 경우에만 사용한다. 메서드 본문 전체를 두 문서에 고정하지 않는다.

### RP5 — 변경과 복구에 관한 기존 후보 강점을 지워서는 안 됨 (유지)

P2의 ASG→EC2 변경과 filtering 후속 발견은 계획을 수정 가능한 근거로 다루는 사례다.
다만 '새 DAG/인스턴스를 제거하면 언제든 rollback'은 교체한 테이블/인덱스까지 복원하지 않는다.
우리 M01의 최신 쓰기 보존·안전 경로만 재개·실패 시 중지·Q4 단계 한정 미해소는 더 구체적이다.
P3 Task 6의 이미 GREEN이면 RED로 부르지 않는 원칙도 우리 TDD/plan에 이미 반영되어 있다.

제안: 동기화·복구·정직한 증명 원칙은 유지한다. 보고서의 명성이나 분량을 이유로 약한 원문을 채택하지 않는다.

## What a review should prove next

단순 섹션 충족 여부보다, 새 세션이 한 작업을 맡아 ①정본 계약 ②첫 실패 판정 ③수정 경계 ④해당 PR 뒤 제품 상태
⑤최신 통합 확인 ⑥발견 시 바꿀 문서를 원래 대화 없이 재구성하는지 본다.
불명확한 제품 판단을 질문하는 것과 이미 적힌 사실을 놓치는 일을 구분한다.
첫 응답·후속 피드백·문서 수정·재시도의 차이를 기록하며 반복 실수마다 새 규칙을 만들지 않는다.
이번 검토는 그 실험의 결과가 아니다.
