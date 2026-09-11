# spec·plan 상세화와 TDD 설계 패키지

**설계 패키지 완료.** 최종 후보 `979771d`, 작업 branch `codex/spec-plan-design`.
[최종 판정·리뷰·한계](review-record.md).

spec은 중요한 구조·동작·계약을, plan은 실제 파일·선행 시험·작업/PR·통합·검증을 기록하도록 보강했다.
spec.md는 진입점이며 여러 설계 정본을 연결할 수 있다. TDD 공통 절차는 자체 스킬, 의무는 짧은 팀 정책,
실제 작업별 첫 시험은 plan에 둔다. 활성 템플릿/스킬·설치·사용판·북극성 주석은 이 작업으로 바꾸지 않았다.

## 바로 볼 결과
- [spec 양식](candidate/templates/spec.md), [plan 양식](candidate/templates/plan.md)
- [후보 전체와 네 완성 예시](candidate/README.md)
- [M01 여러 파일 설계의 진입점](candidate/examples/M01/spec.md)
- [TDD 스킬 소스](candidate/skills/tdd/SKILL.md), [정책·설치/전달 초안](candidate/policy-and-delivery.md)
- [렌더링한 다이어그램](validation/diagram-record.md)

## 근거와 보존 구조
| 위치 | 내용 |
|---|---|
| [execution-plan](execution-plan.md), [brief](brief.md), inputs/ | 승인된 범위·공통 입력·북극성 원문 발췌·출처/판/고정 데이터 |
| proposals/ | root·Astra·Fable 독립 제안, [선택 근거](proposals/selection.md), 실제 Fable 메타데이터/공개 trace |
| candidate/ | 실제 양식·작성법·스킬·정책 전달안·네 spec→plan 예시·문서 갱신 예 |
| reviews/r1–r3/ | 판별 원 리뷰·프롬프트·발견 처리·Claude 메타데이터, 한도/중단 결과 |
| [handoff](handoff/record.md) | 새 Claude Code 세션의 읽기 전용 인계 대화·최초 오류·피드백/복구 |
| validation/ | 입력·후보 해시·상류 참조, 링크·스킬 형식·Mermaid·기존 make check 출력 |

자료는 연구 결과와 비활성 설계 후보다. 제품 실행 성공이나 사람의 제품 승인을 표시하지 않는다.
비공개 추론·서명·자격증명은 공개 trace 보존에서 제외했다. 초기 실패를 성공 요약으로 덮지 않았다.
