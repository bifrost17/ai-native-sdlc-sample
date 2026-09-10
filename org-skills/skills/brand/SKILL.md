---
name: brand
description: Apply the team's copy policy to any text a person reads — screen labels, buttons, error messages, status text, alerts, docs. Use when writing or reviewing user-facing wording, or when a spec decides names or formats. Covers team clauses B1-B3 and defers names and formats to the project's PROJECT-POLICY.md slot P1. Apply this instead of writing copy from general style sense.
---
<!-- 정본: policies/brand.md (팀 조항 B1~B3) · 프로젝트 값: 그 프로젝트의 PROJECT-POLICY.md 슬롯 P1.
     전제: 사내 임직원용 소프트웨어 — 목적은 브랜드가 아니라 오해를 줄이는 것.
     L6: "A skill is a control, though an advisory one." -->

# 문구 — 팀 조항

문구를 쓰거나 고칠 때, 먼저 그 프로젝트의 `PROJECT-POLICY.md` 의 **P1**(이름·표기)을 연다.
P1 이 비어 있으면 **이름이나 형식을 지어내지 말고** spec 의 Flagged concerns 에 「P1 미정」으로 올린다.

## B1 한 문장에 한 뜻 · 과장 금지
- 한 문장이 두 가지를 말하면 나눈다.
- 값을 부풀리는 말(「최고의」·「완벽한」·「즉시」)은 근거가 없으면 쓰지 않는다. 사실만 적는다.

## B2 한 이름으로 부른다
- 제품 · 기능 · 환경 · 상태를 가리키는 낱말은 **P1 의 목록** 하나로. 같은 것에 두 이름을 쓰지 않는다.
- 목록에 없는 상태를 새로 쓰게 되면 임의로 만들지 말고 P1 에 추가할지를 묻는다.

## B3 날짜·시각은 오해가 없게
- P1 에 형식이 있으면 그대로. 없으면 기본값: 날짜 `YYYY-MM-DD`, 24시간제, **시간대를 적는다**.
- 상대 시간(「3일 전」)만 쓰지 않는다 — 절대 시각을 함께.

## 이 스킬이 하지 않는 것
- 이름·형식을 결정하지 않는다(P1 · 프로젝트 담당).
- 문체 다듬기 자체는 다루지 않는다 — 한국어 어색함은 `stop-slop-ko` 가 본다.
- 강제하지 않는다. 프로젝트가 자기 어휘 체커를 두면 그것이 먼저다
  (예시: `org-skills/examples/claims-status/brand/check-brand-copy.sh`).
