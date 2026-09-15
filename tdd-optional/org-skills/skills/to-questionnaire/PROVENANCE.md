# PROVENANCE — to-questionnaire

| 항목 | 값 |
|---|---|
| 판정 | **채택**(원문 그대로) |
| 출처 | https://github.com/mattpocock/skills — `skills/productivity/to-questionnaire/SKILL.md` |
| 판 | commit `3cca18b368ae95cdbdebbff572ccafa662551015`(레포 HEAD, 조사 시각 기준) |
| 라이선스 | MIT — `LICENSE`, "Copyright (c) 2026 Matt Pocock"(원문 사본: `docs/research/intent-template/raw/70-source-paths-and-license.txt`) |
| 최근 갱신 | 2026-09-04T08:45:43Z (레포 `pushed_at`) |
| 사용 신호 | ★257,357 · forks 21,684. Anthropic 공식 플러그인 마켓플레이스 `anthropics/claude-plugins-official` 의 `mattpocock-skills` 항목이 이 레포를 sha `3cca18b…` 로 고정해 배포한다(`raw/12-official-marketplace-entries.txt`) |
| 조사 시각 | 2026-09-09T09:35–09:39 UTC(레포 수치) · 2026-09-09T22:03 UTC(라이선스 원문) |
| 수정 여부 | **없음.** 파일은 상류 원문과 바이트 단위로 같다(sha256 `b5eb9298…`, `raw/to-questionnaire@3cca18b.SKILL.md` 와 동일). 프런트매터의 `disable-model-invocation: true` 를 포함해 한 글자도 고치지 않았다 |
| 왜 이것을 곁에 두는가 | 기준선 `capture-intent` 는 「답을 지어내지 말고 Open questions 에 답할 수 있는 사람 이름과 함께 남겨라」까지만 말하고, 그 사람에게 실제로 묻는 수단은 주지 않는다. 이 스킬이 그 한 칸을 메운다 — 사용자가 답할 수 없는 것을 「누구에게 보내나 · 무엇을 돌려받아야 하나」 두 질문만으로 문서화해 `to-questionnaire-<slug>.md` 로 낸다 |
| 대체가 아니라 병렬 | `capture-intent` 를 건드리지 않는다. `disable-model-invocation: true` 라 모델이 스스로 부르지 못하고 사람이 `/to-questionnaire` 로만 부른다 — intent 를 쓰는 자리를 뺏을 수 없다(시험 `raw/52-tq-natural.txt`: 자연어 요청에는 로드되지 않고 슬래시를 쓰라고 안내) |
| 시험 | `docs/research/intent-template/trigger-tests.md` — 문구 3개 3/3, 집합 충돌 없음 |
| 알려진 제약 | 산출 파일을 현재 디렉터리에 쓴다(`to-questionnaire-<slug>.md`). intent 폴더 규약(`intent/<NNNN>-<slug>/`)에 맞추려면 사람이 옮기거나 오너가 경로 한 줄을 정해야 한다 — README 「정책 오너에게 묻는다」 Q3 |
