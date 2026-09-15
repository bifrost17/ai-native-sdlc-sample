# PROVENANCE — skills/brand

**설계분(직접 씀).** 정책 `policies/brand.md` v0(오너 서명 대기)의 B1~B7 을 옮긴 것이다.
조사 기록: `docs/research/brand/README.md` · `candidates.md` · `coverage.md` · `trigger-tests.md`.

- 출처(정본): `policies/brand.md` — 이 레포. 「정책 원문」 절은 B1~B7 을 축자 전사한 것이고,
  나머지 절은 그 조항을 적용하는 방법이다. 조항을 새로 만들지 않았다.
- 라이선스: 이 레포와 같다. 외부 스킬의 문장을 옮겨 오지 않았다(아래 「참고한 것」은 착상만).
- 수정: 해당 없음(원문 채택이 아니라 설계분이다).
- 작성 시각(UTC): 2026-09-09 ~ 2026-09-10. 작성 세션 S2.

## 왜 설계했나
조사 시각(2026-09-09T09:33Z ~ 2026-09-09T22:35Z) 기준으로 B4(청구 상태 5어휘 고정) ·
B7(「○○○ 고객님」·이모지/느낌표 금지) 를 덮는 공개 스킬을 찾지 못했다. 후보 86건 중 27건을
열어 봤고, 어느 것도 이 정책의 값(다섯 낱말 · 존댓말 · 「원」 · KST)을 갖고 있지 않다 —
전부 「가이드라인 파일을 주면 적용해 주는 틀」이다. 근거: `docs/research/brand/candidates.md`.

## 참고한 것 (착상 · 문장 복사 아님)
| 무엇 | 어디서 | 무엇을 가져왔나 |
|---|---|---|
| 조항별 「이렇게 / 이렇게 쓰지 않는다」 대비 예시 | `raw/cookbooks-applying-brand-guidelines@a97b9a2.SKILL.md`, `raw/kwp-brand-review@34e1eae.SKILL.md`(This sounds like / does NOT sound like) | 규칙마다 위반 예를 같이 두면 모델이 규칙을 적용한다는 꼴 |
| 사과·오류 문구를 「무엇이 · 왜 · 다음에 무엇을」 세 토막으로 쓰는 꼴(B3) | `raw/uxwriting-ux-writing@98cacde.SKILL.md` `[What failed]. [Why/context]. [What to do].` | B3 의 「사실 + 다음 행동」을 문장 꼴로 만드는 법 |
| 리뷰 결과를 「조항 · 문구 · 왜 · 이렇게」 표로 내는 것 | `raw/kwp-brand-review@34e1eae.SKILL.md`(Issue/Location/Severity/Suggestion) · `raw/rampstack-editorial-qa@a67dd34.SKILL.md`(halt/flag/auto-fix) | 출력 형식. 등급 대신 조항 번호를 쓰도록 바꿨다 |
| 확약 표현에 근거 조항을 요구하는 규칙(B2 적용 방법) | `raw/korean-report-style@05ce76d.SKILL.md` §3.3 "기한·의무·책임이 걸린 서술은 어느 문서 몇 조에 있는지 확인하고 인용한다" | 「근거 조항이 있을 때만」을 실행 가능한 절차로 만드는 법 |
| 상태 어휘를 고정하고 동의어를 막는 표 | `raw/localize-naturally@be453d2.SKILL.md` "Keep lifecycle states distinct… Never turn an earlier state into a later one" | 상태 낱말을 승격/강등하지 않게 막는다는 착상 |
| 금액 `10,000원` · 시각 `15:30 KST` 표기가 정책 값과 같음을 확인 | `raw/daleseo-style-guide@ae12ba2.SKILL.md` 참조 파일 | 우리 B6 값이 한국어 관행과 어긋나지 않는다는 대조 |
| 기계 훑기(`check-brand-copy.sh`)를 스킬이 부르는 꼴 | `docs/work/baselines/secure-api-review.SKILL.md`(그 파일이 「L6 481-498」로 적은 worked example 의 `check-endpoints.sh` 줄) | 스킬이 결정론적 검사를 부르되 판정은 사람이 한다 |
| description 에 「무엇을 하지 말고 이 스킬을 쓰라」를 넣는 것 | `docs/work/NOTES.md` 3(S8 실측) | 트리거 문장 꼴 |

## 함께 채택한 스킬
`skills/stop-slop-ko/`(B1 보강, MIT, 원문 유지) 하나다. `kwp-brand-review` 는 리뷰 절차의 꼴만 참고하고
**기각**했다 — 우리 자리에서 로드되지 않았다(`docs/research/brand/trigger-tests.md` S1 · S2 · S4).
충돌 시험은 같은 문서의 「집합 시험」 절. 두 스킬이 같은 자리에서 부딪히면 **`brand` 가 우선한다** —
정책 정본을 옮긴 것이 이것뿐이기 때문이다(실측된 부딪힘: `stop-slop-ko` 43행의 매체별 「청유·감탄」 대 B7).

## 딸린 파일
- `check-brand-copy.sh` — 직접 씀. B1·B2·B3·B4·B6·B7 중 낱말·기호로 잡히는 것만 grep 하고,
  조항마다 예외 패턴을 둔다(Vale 의 `exceptions` 를 본떴다). 검사가 실패하면 rc=2 로 멈춘다 —
  초록으로 위장하지 않는다. bash 3.2 · macOS grep(-P 없음)에서 동작하도록 이모지는 UTF-8 바이트로 잡는다.
  실행 원문: `docs/research/brand/raw/15-checker-run-v2.txt` — 정상 문구 15줄 오탐 0(rc=0),
  위반 문구 18줄 전부 검출(rc=1), 가장자리 8경우(이진·빈 파일·대시로 시작하는 이름·없는 파일…) 확인.
  1차 실행 기록은 `13-checker-run.txt`(그때는 픽스처가 작아 오탐을 못 봤다).

## 오너 서명
`policies/brand.md` 는 `Status: draft v0 — 오너 서명 대기`. 이 스킬도 같은 상태다.
정책이 바뀌면 정책을 먼저 고치고(서명 = 개정 PR 머지) 이 파일의 「정책 원문」 절을 다시 전사한다.
스킬 레슨: "When the policy changes, change the skill and have the policy owner sign off on the change."
