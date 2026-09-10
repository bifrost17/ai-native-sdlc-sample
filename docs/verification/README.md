# docs/verification — 플레이북 문단별 검증

이 템플릿이 AI-Native SDLC Playbook 이 지향하는 방향대로 도는지를, **플레이북 한국어판 문서의 가이드 문단마다
증거를 삽입하며** 검증한 기록이다. 플레이북 자신이 검증 기준이다 — 별도 점검표를 만들지 않는다.

이 폴더는 Anthropic 저작물(플레이북 한국어판)의 사본을 담는다. 원문은 Claude Academy,
`courses/ai-native-sdlc-playbook`, Copyright Anthropic.

| 파일 | 무엇 |
|---|---|
| `playbook-annotated.html` | 주석판 — 원문 + 가이드 문단 아래 `<details class="verify …">` 증거 블록 179개(ID `V2-01`~`V13-16`) |
| `source/playbookkoen3.html` | 원문(무변경) |
| `CHAPTERS.md` | 챕터별 집계와 반영 PR · 라운드 이력 |
| `INDEX.md` | 검증 항목 ID 색인(ID · 판정 · 문단) |

이력(챕터별 v1 → 보완 PR → v2 커밋 24개)은 별도 비공개 레포 `bifrost17/intent-sdlc-playbook-verification` 에 있다.

## 결과 (2026-09-09)

블록 179 · 충실 135 · 부분 24 · 팀 몫 20 · 보완 필요 0. 이 검증이 템플릿에 남긴 변경은 PR #44~#54.
챕터 1·14 는 가이드 문단이 없어 대상 밖.

---

## 방식
# ai-native-sdlc-sample 검증 — 플레이북 문단별 증거 주석

`bifrost17/ai-native-sdlc-sample (옛 이름 intent-sdlc-sample)` 이 AI-Native SDLC Playbook 이 지향하는 방향대로 도는지를,
플레이북 한국어판 문서의 **가이드 문단마다 증거를 삽입하며** 검증한 기록이다.
플레이북 자신이 검증 기준이다 — 별도 점검표를 만들지 않는다.

- `source/playbookkoen3.html` — 원문(무변경).
- `playbook-annotated.html` — 원문 + 가이드 문단 아래 `<details class="verify …">` 블록.
  원문 문장은 한 글자도 바꾸지 않는다; 서술 문단은 비워 둔다.
- `CHAPTERS.md` — 챕터별 집계와 반영 PR.
- `INDEX.md` — 검증 항목 ID 색인. ID = `V<챕터>-<문서 순서>`(예 `V4-07`), 주석판의 `#V4-07` 앵커이자 각 블록 제목의 링크.
  ID 는 삽입·치환 뒤 매번 문서 순서로 다시 매긴다 — 블록이 끼어들면 뒤 번호가 밀리므로, 라운드 사이 대조는 커밋 SHA 와 함께 쓴다.

블록 판정은 넷뿐: **충실** · **부분** · **팀 몫(미검증)** · **보완 필요**.
블록 = 템플릿 `경로:줄` 인용 / 실험(사슬·턴·raw·시각·PR) / 보완.
쓰다 드러난 빈틈이 템플릿 몫이면 그 자리에서 샘플 레포에 PR 을 내고 블록에 번호를 적는다 —
주석은 산출물이 아니라 검증 절차다. 이력은 이 레포의 커밋이다(챕터 하나 = 커밋 하나 이상).
