# 팀 자료 색인

이 색인은 tdd-optional 0.1.5 전달 자료를 설명한다. 팀 자료 13개와 별도 선택 채택한 작성 예시 최대 3개를 제공한다. 필요한 자료를 현재 업무에 맞춰 선택해 읽는다.
이 목록은 호출 순서나 평가 정답표가 아니다.

## OpenCode native skills

| 이름 | 용도 | 설치 위치 | 판 |
|---|---|---|---|
| `brand` | 조직의 브랜드 문구 원칙 적용 | `.opencode/skills/brand/` | 팀 원본 |
| `data-compliance` | 데이터 수집·보관·동의 정책 검토 | `.opencode/skills/data-compliance/` | 팀 원본 |
| `secure-api-review` | API 설계·구현의 보안 위험 검토 | `.opencode/skills/secure-api-review/` | 팀 원본 |
| `spec-policy-pass` | spec과 연결 설계에 적용할 팀 정책 검토 | `.opencode/skills/spec-policy-pass/` | 팀 원본 |
| `tdd` | TDD를 선택한 범위의 RED→GREEN과 회귀 근거 유지 | `.opencode/skills/tdd/` | 팀 원본 |
| `stop-slop-ko` | 한국어 산출물의 모호하고 기계적인 표현 정리 | `.opencode/skills/stop-slop-ko/` | 팀 원본 |
| `accessibility` | 웹 인터페이스의 접근성 검토 | `.opencode/skills/accessibility/` | 팀 원본과 동반 참조 |
| `secrets-scan` | 커밋·머지 전 비밀값 노출 점검 | `.opencode/skills/secrets-scan/` | 팀 원본과 plays/templates |
| `grilling` | 구현 전 요구·경계·실패 조건 질문 | `.opencode/skills/grilling/` | 팀 원본 |
| `sdlc-feedback` | 합의·spec·plan·구현·검증 정렬 | `.opencode/skills/sdlc-feedback/` | OpenCode 얇은 변환 |
| `ux-copy` | 오류·빈 상태·CTA 등 UX 문구 작성과 검토 | `.opencode/skills/ux-copy/` | OpenCode 얇은 변환 |
| `capture-intent` | 요청자의 문제·범위·제약·성공을 intent로 기록 | `.claude/skills/capture-intent/` | 같은 판 project/examples/skills의 선택 채택본 |
| `design-spec` | 수락된 intent와 실제 맥락으로 spec·설계 작성 | `.claude/skills/design-spec/` | 같은 판 project/examples/skills의 선택 채택본 |
| `plan` | 수락된 설계를 실행 가능한 계획으로 변환 | `.claude/skills/plan/` | 같은 판 project/examples/skills의 선택 채택본 |

`sdlc-feedback`의 기본 독립 검증자는 `.opencode/agents/sdlc-verifier.md`다. 검증자는
현재 합의·문서·diff·실행 근거를 읽고 발견만 보고하며 수정·승인하지 않는다.

## 필요할 때 직접 읽는 파일 자료

| 이름 | 용도 | 위치 | 사용 조건 |
|---|---|---|---|
| `to-questionnaire` | 다른 사람이 답할 발견 질문지 작성 | `team-resources/skills/to-questionnaire/` | 사용자가 명시적으로 질문지를 원할 때만 읽는다 |
| `pr-loop` | hosted PR의 댓글·실패 검사 반복 처리 | `team-resources/skills/pr-loop/` | 실제 hosted PR을 맡았을 때 읽는다 |

각 폴더의 `SKILL.md`만 떼어 내지 말고 `references/`, `examples/`, `plays/`,
`templates/`, `LICENSE*`, `PROVENANCE.md` 등 동반 파일을 같은 상대 위치에서 읽는다.
