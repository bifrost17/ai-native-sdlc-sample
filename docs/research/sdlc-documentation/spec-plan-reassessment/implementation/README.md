# Spec·plan 보완 결과

2026-09-11 · **설계 후보 보완 완료.** 독립 리뷰와 피드백을 포함한 읽기 전용 인계 범위를 root가 통과로 판정했다.
후보 판 `2d3f2dc`, branch `codex/spec-plan-design`. 보완 전 기준은 `c09b5f1`이다.

spec은 중요한 설계가 왜 필요하고 어떻게 동작하는지 설명하고, plan은 그 설계를 실제 작업으로 이어가도록 고쳤다.
정확한 계약·TDD·작은 PR·배포 가능한 main·다문서 정본과 같은 커밋의 문서 갱신 원칙은 유지했다.

| 재검토 우선순위 | 반영 결과 |
|---|---|
| 정책 검토 지침 충돌 | [정책 스킬 후보](../../spec-plan-design/candidate/skills/spec-policy-pass/SKILL.md)와 [명령](../../spec-plan-design/candidate/commands/spec-policy.md)을 실제로 수정. 다문서 정본 허용, 중요한 우려/실제 정책 적용에 집중. 활성화 경로까지 명시 |
| spec 구성 | [양식](../../spec-plan-design/candidate/templates/spec.md)에 문제→제약→선택→대표 흐름→계약을 채우는 작성 면. 만능 Design 표를 걷어내고 필요한 계약 표/도식은 유지 |
| plan 구성 | [양식](../../spec-plan-design/candidate/templates/plan.md)에 PR 인도 지도와 작업별 필수 설계·파일·첫 시험/예상 RED·최소 변경·완료 관측을 모음. F03/M01 실행 블록도 같은 흐름으로 보완 |
| 정본을 찾는 경로 | [M01 spec](../../spec-plan-design/candidate/examples/M01/spec.md)의 현재/목표·선택 이유·대표 흐름을 보강. 필요한 현재 계약을 예시 옆 inputs로 직접 연결 |
| 완성 예시의 다양성 | **W01 사내 포털 내 신청 조회** 추가. [spec](../../spec-plan-design/candidate/examples/W01/spec.md) → [plan](../../spec-plan-design/candidate/examples/W01/plan.md)에 UI·서버 인증/본인 데이터·실패/재시도·두 PR·공개/중단/cleanup을 연결 |

작은 F01/B01은 기존의 짧은 형태를 유지했다. 필요한 UML/인터페이스/스키마는 구체적으로 작성하되 모든 그림·내부 메서드·
분량을 강제하지 않는다. 공통 TDD 방법은 자체 스킬, 해당 변경의 첫 행동 시험은 plan에 둔다.
[후보 전체 색인](../../spec-plan-design/candidate/README.md)에서 유형에 맞는 예시를 선택할 수 있다.

## 검토와 검증

- **Astra/ultra + 실제 Claude Code Opus/high:** 독립 전체 검토 후 중요한 모순을 수정하고 수정 범위 재검토 PASS.
  W01의 공개 전 AC와 공개 후 cleanup AC가 순환하던 문장을 고쳤다. 최초 Opus PASS가 이 문제를 놓친 사실도
  [의견 처리 기록](review-decisions.md)에 보존했다.
- **새 세션 인계:** Sonnet/medium에서 시작해 root가 실제 응답을 읽고 추가 개발 요청/피드백을 제공했다.
  계약 변경 영향 판단은 같은 대화를 Opus/high로 이어 확인했다. [최초 오류·정정·한계](handoff/record.md)를 보존했다.
  단독 첫 응답의 완전성, 제품 코드 실행·스킬 자동 로드 실험의 통과는 아니다.
- **도식:** Mermaid 6개 구문·렌더·육안 검사, 경계 초과 0. 수정 뒤 도식 블록/이미지 해시도 동일하다.
- **정적 검증:** 후보 38개 파일 해시, 상대 링크 151개·절 링크 13개, 10개 Upstream 해소, 기존 계약/정책·조사 원문 보존.
- **기존 회귀:** make check exit 0. Python 96개 중 기존 skip 1, hooks 28/28, eval fixture 8/8, managed-settings PASS.
  [원 출력과 상세 범위](validation/README.md)를 함께 보존했다.

## 반영 범위와 이력

이번 완료 범위는 승인된 **설계 패키지의 후보 보완·리뷰·읽기 전용 인계**다. 활성 templates/.claude/org-skills,
영구 설치, 실제 제품 구현/TDD·운영 실험, 북극성 주석은 이 판으로 변경하지 않았다.
[정책·배포 전달안](../../spec-plan-design/candidate/policy-and-delivery.md)에 교체할 스킬·명령·reference·예시/입력·설치 확인 경로까지 준비했다.
이후 활성화/사용판 실험은 그 전달안을 적용하고 실제 관측으로 별도 판정한다.

| Git 판 | 보존 내용 |
|---|---|
| cfb0ec9 | 사용자 조사자료·전면 재검토·이번 실행 범위 보존 |
| be0031d | W01 합성 현재 계약·데이터·오너 답·intent 입력 |
| 394651e | W01 최초 spec — plan의 실제 제작 입력 |
| 1500b16 | 양식/스킬/정책 후보·F03/M01·W01 plan 보완과 독립 리뷰 입력 |
| 2d3f2dc | 리뷰를 반영한 최종 후보. 이후 커밋은 리뷰/인계/검증 기록과 색인 |

[실행 계획](plan.md), [M01 분담 기록](m01-notes.md), 원 리뷰·최초 오류·후속 응답·메타데이터·공개 Read 기록·검증 산출물을
이 폴더에 보존했다. 이전 연구와 후보 판은 덮어쓰지 않았으며 비공개 추론·자격증명은 저장하지 않았다.
