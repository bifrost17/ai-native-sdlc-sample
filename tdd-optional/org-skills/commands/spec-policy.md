---
description: 관련 팀 정책을 실제로 적용해 요구·설계 정본을 작성하고 중요한 우려를 드러낸다 — 축자 PO 프롬프트와 정책 검토 방법
argument-hint: [intent-id]
---
프로젝트의 요구·설계 작성 절차를 따르고, 팀의 `spec-policy-pass`가 제공되면 함께 적용한다.
정책 검토는 문서 파일 수나 형식을 대신 정하지 않는다.

Read the attached intent.md and produce a requirements and design spec for integrating it into our
existing codebase. Apply the skills available to you so the plan conforms to our brand guidelines,
security policies and UX standards.
Document the spec fully as spec.md, ready to hand to the
engineering team. Describe clearly any areas of concern, especially where you cannot satisfy
contradicting policies.

(L3 282, the playbook's prompt, verbatim — 원문은 유지한다.)

대상 intent는 채택한 개발건 경로의 `$1/intent.md`다(새 배포는 `changes/`, 기존 제품은 `intent/`도 가능).
프로젝트의 개발건 README를 먼저 읽는다. 식별자가 없으면 현재 요청·작업 맥락으로 식별하고, 여러 후보라면
대상을 확인한다. 기존에 허가된 draft 작성 범위를 다시 승인받지 않는다.
`design-spec`이 요구·설계 정본과 수락 경계를 맡고, 정책 검토 스킬은 실제 정책 적용·출처·우려를 다룬다.
끝내기 전에 적용 스킬 본문·출처·판, 정책에 영향을 받은 설계 정본, 중요한 미결 판단의 근거를 확인한다.
관련 스킬이 없으면 직접 확인한 정책 근거와 적용 한계를 밝힌다. 같은 요구를 여러 표/파일에 중복 정의하지 않는다.
