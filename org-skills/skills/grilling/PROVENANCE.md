# PROVENANCE — grilling

| 항목 | 값 |
|---|---|
| 판정 | **채택**(원문 그대로) |
| 출처 | https://github.com/mattpocock/skills — `skills/productivity/grilling/SKILL.md` |
| 판 | commit `3cca18b368ae95cdbdebbff572ccafa662551015`(레포 HEAD, 조사 시각 기준) |
| 라이선스 | MIT — `LICENSE`, "Copyright (c) 2026 Matt Pocock"(원문 사본: `docs/research/intent-template/raw/70-source-paths-and-license.txt`) |
| 최근 갱신 | 2026-09-04T08:45:43Z (레포 `pushed_at`) |
| 사용 신호 | ★257,357 · forks 21,684. Anthropic 공식 플러그인 마켓플레이스가 sha 고정으로 배포(`raw/12-official-marketplace-entries.txt`) |
| 조사 시각 | 2026-09-09T09:35–09:39 UTC(레포 수치) · 2026-09-09T22:03 UTC(라이선스 원문) |
| 수정 여부 | **없음.** 상류 원문과 바이트 단위로 같다(sha256 `10ff989e…`, `raw/grilling@3cca18b.SKILL.md` 와 동일) |
| 왜 이것을 곁에 두는가 | 기준선 `capture-intent` 는 「네 가지를 묻고 답이 얇은 곳을 더 판다(dig where answers are thin)」고 하지만 *어떻게* 파는지는 말하지 않는다. 이 스킬이 그 방법을 준다 — 결정을 design tree 로 보고, 선행 결정이 끝난 질문만 모아 한 라운드로 묻고(각 질문에 권고안 첨부), 답이 트리를 다시 그리면 다음 라운드를 계산한다. frontier 가 빌 때까지 = 조용히 가정된 것이 없을 때까지 |
| 대체가 아니라 병렬 | 「intent 로 써 달라」는 문구에서는 `capture-intent` 가 이기고(`raw/53-set-idea.txt`), 「grill/stress-test/interrogate 해 달라」는 문구에서만 이쪽이 뜬다(`raw/54,56,57`). 두 스킬을 같이 넣은 집합 시험에서 지시가 어긋난 곳은 없었다 |
| 시험 | `docs/research/intent-template/trigger-tests.md` — 문구 3개 3/3, 집합 충돌 없음 |
| 알려진 제약 | 모델이 스스로 부를 수 있다(`disable-model-invocation` 없음). 「사실은 네가 찾고 결정은 사용자가 한다」가 이 스킬의 규칙이라 originator 의 말을 그대로 적는 `capture-intent` 와 충돌하지 않지만, 원고 없이 grilling 만 돌면 intent.md 는 나오지 않는다 — 산출은 합의이지 파일이 아니다 |
