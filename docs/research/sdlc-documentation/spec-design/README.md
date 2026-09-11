# 우리 spec 양식 설계

2026-09-11. 작성: Codex root. 상태: R2 독립 문서 리뷰 통과, 실제 부분 대화 인계 확인.
목적은 사람이 중요한 변화를 검토하고 에이전트가 구현 계획을 세울 요구·설계를 같은 기록에 남기는 것이다.

## 결과와 읽는 순서

- [조사·설계 방향 재독](reading-notes.md): 가져올 원칙과 가져오지 않을 절차.
- [두 후보 비교](alternatives.md): 실제 F01의 다른 배치, 복합 사례의 공유 계약·검증·갱신 대조.
- [spec 양식](../../../../templates/spec.md)과 [작성 스킬](../../../../.claude/skills/design-spec/SKILL.md).
- 합성 완성 예시: [작은 기능](../../../../.claude/skills/design-spec/examples/feature/spec.md),
  [정밀한 버그](../../../../.claude/skills/design-spec/examples/bug/spec.md),
  [이행과 보고서 소비자](../../../../.claude/skills/design-spec/examples/migration/spec.md).
  각각의 intent.md·context.md가 입력이며 실제 승인·구현·실행 결과가 아니다.
- [새 발견 전후 기록](change-walkthrough.md): 미결을 드러내는 초안과 결정 후의 현재 계약 갱신.
- [리뷰 요청](review-request.md): 같은 파일에 대한 독립 검토 기준.
- [최종 판단과 리뷰](review-record.md): Astra/ultra·실제 Claude Code Fable/max의 R1/R2와 한계.
- [6회 실제 부분 대화](probe/README.md): Sonnet/medium의 설계·리뷰·계획·변경 대응, 초기 오류 보존.
- [사용판 전달](delivery.md): 원본과 선택형 사용 후보 ca87cdb의 대응.
- [최종 독립 검사](reviews/verifier-final.md): 회귀·해시·범위·원문 보존과 미실행 항목.

## 여섯 구획이 맡는 판단

| 구획 | 독자가 이해할 것 |
|---|---|
| Requirements | 이번에 바꿀 동작과 보존할 계약, 의도·제약·정책과의 연결 |
| Acceptance criteria | 대표 조건에서 관측할 성공·실패·회귀 결과. R/AC 연결은 검증할 대상을 찾는 수단 |
| Design | 실제 구조와 흐름, 중요한 선택·이유·단점·계약. 필요한 변화에만 상세 확장 |
| Constraints and scope | 지켜야 할 조건과 제외 범위. 이미 명확히 적힌 계약을 참조할 수 있음 |
| Open questions | 기존/새 질문의 답과 근거, 이월 영향·담당·필요 시점 |
| Flagged concerns | 사람의 판단이 필요한 중요한 우려와 정책 충돌. 이월 표식만으로 해소되지 않음 |

핵심 변화·선택·우려는 앞에서도 짧게 읽힌다. 상세 내용과 별도 권위를 가진 요약은 만들지 않는다.
양식의 프롬프트는 빈칸에 남길 답을 안내하고, 코드 조사·질문·대안 검토·상세 추가·변경 반영은
스킬이 돕는다. 불필요한 수치·대안 수·N/A 목차·새 문서 원장을 요구하지 않는다.

기본 파일명·상류 SHA·draft·R/AC·Flagged concerns를 유지했다. 기존 eval 03의 절 이름 안내와
양성/음성 fixture 배치만 맞췄으며 질문 누락을 실패로 잡는 검사·의미 판단 기준은 유지했다.
plan 사용 양식과 선택 팀 정책 플러그인은 변경하지 않는다.

## 실제 사용판에 전달하는 범위

제작용 원본은 main 계열의 .claude/skills 및 templates에 있다. 기존 사용 후보는 자동으로
생성되지 않아 `codex/use-template-0017@add296d`에서 `codex/use-template-0021`을 별도 파생했다.
사용판은 `References applied`와 선택형 examples/skills를 유지한다. 이 자료를 사용하려고
특정 스킬이나 새 플러그인을 반드시 설치할 필요는 없다.

이번 spec과 앞서 통과한 intent 양식을 함께 전달하고, 제작용 연구·평가·하네스는 포함하지 않는다.
두 판의 실제 차이와 최종 커밋은 리뷰·배포 기록에 남긴다. 후보 작성은 조직 승인이나 전체 SDLC
실험 통과를 뜻하지 않는다. 실제 런타임·인계 관측은 실행한 범위와 함께 별도로 기록한다.
