# intent-sdlc-sample

Anthropic 「The AI-Native SDLC Playbook」(Claude Academy · 14레슨)의 아티팩트 사슬을
**기계가 지키는 레포**로 시연하는 샘플이다. 비공식이며 Anthropic 공식 프로젝트가 아니다.

```
intent.md  →  spec.md  →  plan.md  →  코드·시험  →  PR·리뷰  →  merge
   ↑                                                              │
   └──────────  Stage 6: 밴드 위반이 다음 intent 를 쓴다  ←────────┘
```

레슨 1 의 주장 — *"Each stage ends by writing [an artifact] to version control … and the next
stage begins by reading it. The chain of commits is also the audit trail"* — 을 문장이 아니라
**검사로** 증명하는 것이 이 레포의 목적이다.

## 지금 상태 — W0 (골격)

설계안이 첫 아티팩트다. 사슬 3본과 강제 장치는 W1~W3 에서 들어온다.

| 읽을 것 | 무엇 |
|---|---|
| `docs/DESIGN.md` | 설계안 v0.2 — 결정 15건 · 14 플레이 전수 판정 · 이월 원장 |
| `NOTICE` | 차용 조각의 출처와 라이선스 |
| `make check` | 지금 있는 것만 검사한다. 빈 통과가 아니다 — 무엇을 재는지는 `scripts/check_all.sh` |

## 앞으로 들어올 것 (설계안 §12)

- W1 아티팩트 검증기 + 훅 5 + CI 차단
- W2 사슬 0001(레포 자체) · 0002(청구 상태 기능)
- W3 사슬 0003(결함 — 실패 시험 먼저) · 밴드 검출기 · 지표

## 이 레포가 검증하지 않는 것

검증기는 **닫힌 어휘만** 잰다: 파일·절·필드·상태·상류 승인·ID 이어받기.
「제목이 해법인가」 · 「산문이 좋은가」 · 「요구가 문제를 실제로 푸는가」는 재지 않는다 —
사람과 리뷰의 몫이고, 안 보는 것을 보는 척하지 않는다.

## 출처

플레이북 인용은 짧은 축자 + 출처 표기만 한다. 원문은 Claude Academy 의
`courses/ai-native-sdlc-playbook` (Copyright Anthropic).

