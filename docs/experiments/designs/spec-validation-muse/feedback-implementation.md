# feedback・verifier 구현 기록

2026-09-14. 구현 담당: 앞선 보완 설계 분석에 참여한 Astra/high 역할 에이전트.
이 기록은 구현과 정적 확인이며 독립 최종 심사나 Muse 실험 결과가 아니다.
`CLAUDE.md`, 수락된 `docs/decisions/spec-validation-design/README.md`, skill-creator 지침을 읽고 반영했다.

## 변경 범위

다음 양판 공통 상대 경로 4개씩, 선택형 전용 4개, 총 12개 기존 파일을 수정했다.

- `tdd-first/org-skills/skills/sdlc-feedback/SKILL.md`
- `tdd-first/org-skills/agents/sdlc-verifier.md`
- `tdd-first/org-skills/opencode/agents/sdlc-verifier.md`
- `tdd-first/org-skills/opencode/patches/sdlc-feedback.patch`
- `tdd-optional/org-skills/skills/sdlc-feedback/SKILL.md`
- `tdd-optional/org-skills/agents/sdlc-verifier.md`
- `tdd-optional/org-skills/opencode/agents/sdlc-verifier.md`
- `tdd-optional/org-skills/opencode/patches/sdlc-feedback.patch`
- `tdd-optional/org-skills/codex/agents/sdlc-verifier.toml`
- `tdd-optional/org-skills/codex/patches/sdlc-feedback.patch`
- `tdd-optional/org-skills/examples/sdlc-feedback-adoption.md`
- `tdd-optional/org-skills/codex/templates/AGENTS.md`

feedback은 spec 인계 준비·중요 설계 개정을 선택 사건에 포함하고, 전체 인계와 설계 조각의 범위,
필요한 입력, 조건부 새 문맥 검토와 결과 종합을 연결했다. 구현 리뷰의 diff/실행 근거 입력은 구현
범위임을 명시했다. 구현 완료의 기존 fresh verifier 호출·결과 대기 의무는 유지하고, 설계 PASS나
design-only라는 이름으로 실제 구현 변경·완료 주장의 검토를 갈음하지 않게 했다.

verifier는 설계만 검토할 때 존재하지 않는 plan·신규 구현·실행 결과를 요구하지 않는다. 전체 spec
인계는 선언 정본 전체를 읽고, 설계 조각은 관련 결정과 의존 범위를 읽는다. 정합성과 충분성을 구분하고,
공유 입력/결과/오류·해당하는 권한/순서/호환과 중요한 AC 분기를 정본에서 따라가도록 했다.
공통 불변식과 다른 복구 경로를 재사용할 조건, 공유 의미와 이월 가능한 내부 선택의 차이를 명시했다.
새 도식 수·상태 전수·리뷰어 수·승인 단계·스킬·검사기는 만들지 않았다.

기본형의 test-first와 자동 RED 요구 및 기존 예외 연결, 선택형의 방식 선택과 TDD slice별 증거
기준은 유지했다. verifier의 권한·모델 설정은 변경하지 않았다. OpenCode/Codex 차이는 기존
설치 경로·호출 설정·역할 확인 한계에 한정했다.

선택형의 두 채택 안내에는 spec 인계와 중요한 설계 개정도 현재 이벤트에 맞게 스킬을 읽도록
연결했고, 매 설계 편집마다 독립 검토를 요구하지 않음을 명시했다. 추가 요청에 있던 기본형
`org-skills/examples/sdlc-feedback-adoption.md`는 실제로 존재하지 않아 생성하지 않았다.
기본형의 기존 `org-skills/README.md` feedback 소개 절은 root 소유 경로로 전달했다.

## 수행한 확인

| 확인 | 실제 결과와 범위 |
|---|---|
| skill-creator `quick_validate.py` | 양판 feedback 각각 `Skill is valid!`, rc=0 |
| `python3 -m unittest discover -s tests -p test_template_editions.py` | 기존 3개 시험, `OK`, rc=0 |
| OpenCode feedback patch 2개 | 임시 디렉터리에서 `patch -p1 -F 0` 적용, 각각 rc=0, offset/fuzz 없음 |
| 선택형 Codex feedback patch | 실제 대상 경로 구조의 임시 디렉터리에서 동일 적용, rc=0, offset/fuzz 없음 |
| 변환 뒤 범위 보존 | 세 patch 모두 새 설계 검토 절이 원본과 동일하며 기존 구현 완료 fresh 문장·설계 PASS 대체 금지·구현 전용 입력 구분 유지 |
| verifier 본문 대조 | 양판 OpenCode 본문은 해당 공통 본문과 일치. Codex는 기존 프로젝트 AGENTS 읽기 안내 차이를 제외하면 선택형 공통 본문과 일치 |
| `git diff --check` | 변경 후 rc=0, 출력 없음 |

quick_validate는 처음 기본 Python과 번들 Python에서 PyYAML이 없어 실행되지 않았다.
기존 `/Users/jake/Projects/ai-native-sdlc-experiment-private/0034-document-handoff/validation-venv/bin/python`을
재사용한 재실행에서 양판 모두 통과했다. 새 의존성 설치나 전역 설정 변경은 하지 않았다.

최초 구현 확인의 임시 변환에서 얻은 feedback 본문 SHA-256(아래 후속 한 문장 보완 전):

| 대상 | SHA-256 |
|---|---|
| 기본형 OpenCode | `ac8c095b222adef119ac42bf93a26443a644098621ab678b9ff43c301a2ca09d` |
| 선택형 OpenCode | `6f11bb40fb2d7c5928de8fdc6df3ceb0b35eca30b7b149eb1f24cb5eca17088d` |
| 선택형 Codex | `f24bae6e3d5695c4987554d86de4db73fd20d44ede37e2f3db4974c415313407` |

## 검토 지적 반영과 한계

앞선 제안 검토에서 지적한 설계 범위 선택과 구현 완료 fresh 의무의 평가 구분은 수락 설계의
정적/adapter 확인 항목에 반영된 것을 읽었다. 이번에는 그 범위가 실제 배포용 본문과 patch 결과에서
보존됨을 대조했다. 기존 설계 안의 과거 리뷰 언급 때문에 평가를 완전한 판정 미노출 실험이라고
부르지 않는 한계도 수락 설계에 반영된 것을 확인했다.

문구 보존·patch 적용은 실제 이벤트의 자연 선택, 독립 검토 호출, 대기·종합 행동의 실행 증거가 아니다.
제품 코드를 실행하거나 Muse 실험을 수행하지 않았고, 전역 설치·커밋·통합도 하지 않았다.
전체 `make check`, 패키지 strict 검증, 후속 실제 설치·행동 평가는 root의 통합 검증 범위로 남긴다.
초기 설계에 참여한 구현자의 검증이므로 독립 최종 PASS로 제시하지 않는다.

## 후속 범위 명확화

선택형 Change or acceptance의 검증 전략 기록 문장에 `For implementation planning,`을 붙였다.
설계만 개정할 때 plan을 새로 만들라는 요구로 읽히지 않도록 적용 범위만 명확히 했으며, 선택 가능한
검증 방식·이유·커버리지 요구는 유지했다. 기본형은 같은 전략 선택 문장이 없고 기존 갱신 시점이
이미 해당 동작의 `test-first cycle` 시작 전으로 한정되어 있어 수정하지 않았다.

기본형 OpenCode·선택형 OpenCode/Codex의 세 patch를 다시 임시 디렉터리에 적용했다.
모두 rc=0, offset/fuzz 없음이며 patch 파일을 고칠 필요는 없었다. `git diff --check`도 rc=0이다.
기본형 변환 SHA는 위와 같고 선택형의 최종 변환 SHA는 다음과 같다.

| 대상 | 최종 SHA-256 |
|---|---|
| 선택형 OpenCode | `ec6bb03d1034c670841ca9197e4b23a74d426aa1644249f87c2dc159dab8008b` |
| 선택형 Codex | `29542e8dc76d3e8c4f6b03e89182e8b044d8d7da3c5c9397fe0c03ecf54c07c3` |
