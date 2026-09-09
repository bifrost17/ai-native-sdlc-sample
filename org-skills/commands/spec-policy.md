---
description: 정책 스킬을 빠짐없이 걸어 spec.md 를 쓴다 — 축자 PO 프롬프트 + 정책 통과 절차 (L3 268 "codify it as an organization-level slash command")
argument-hint: [intent-id]
---
먼저 `spec-policy-pass` 스킬을 연다. 아래 프롬프트를 실행하되, 정책을 거는 방식과 우려를 적는 꼴은
그 스킬이 정한다.

Read the attached intent.md and produce a requirements and design spec for integrating it into our
existing codebase. Apply the skills available to you so the plan conforms to our brand guidelines,
security policies and UX standards.
Document the spec fully as spec.md, ready to hand to the
engineering team. Describe clearly any areas of concern, especially where you cannot satisfy
contradicting policies.

(L3 282, the playbook's prompt, verbatim — 한 글자도 바꾸지 않는다.)

대상 intent 는 `intent/$1/intent.md`. `$1` 이 비면 `intent/` 아래에서 intent.md 는 있고 spec.md 는 없는
폴더를 세어 어느 것인지 묻는다. 뼈대(수락 확인 · `templates/spec.md` · 리뷰 질문)는 `design-spec` 스킬을
따르고, 그 위에 `spec-policy-pass` 의 네 절차를 겹친다.

끝내기 전에 스스로 확인한다 — 연 정책 스킬을 `Skills applied` 에 판(sha)까지 적었는가. 열지 않고 적은
이름은 없는가. 우려 표의 「충돌」 행마다 조항 ID 가 양쪽 다 있는가. 「공백」을 조항의 정신으로 논증하지
않았는가. 결정 칸을 비워 두었는가.
