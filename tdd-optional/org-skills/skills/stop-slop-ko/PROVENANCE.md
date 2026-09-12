# PROVENANCE — skills/stop-slop-ko

**채택분(원문 유지).**

| 무엇 | 값 |
|---|---|
| 출처 | https://github.com/limleesol/stop-slop-ko — `SKILL.md`(레포 루트) |
| 판(sha) | `43313c9619d1152b110c19bf1ef9ef7341eff3b8` |
| 라이선스 | **MIT** — 레포 `LICENSE` 파일과 `SKILL.md` frontmatter `metadata.license: MIT` 양쪽에서 확인 |
| 저작자 | Lim Leesol (5limleesol5@gmail.com) · `inspired_by: Hardik Pandya (stop-slop)` (frontmatter 표기 그대로) |
| 조사 시각(UTC) | 2026-09-09T22:27:58Z(레포 메타) · 2026-09-09T22:35Z(본문 정독) |
| 그때의 수치 | ★7 · fork 0 · 최근 push 2026-07-30 (`docs/research/brand/raw/10-candidate-repos.txt`) |
| 사본 | `docs/research/brand/raw/stop-slop-ko@43313c9.SKILL.md` |
| **수정** | **없음.** `skills/stop-slop-ko/SKILL.md` 는 원문과 바이트 동일(`diff` 확인). frontmatter·부록 포함 394줄 그대로 |
| 딸린 파일 | 없음. 원본 레포의 `assets/`(배너 png)·`evals/`(자체 시험)는 가져오지 않았다 — 본문이 참조하지 않는다(부록은 SKILL.md 안에 있다) |

## 왜 채택했나
정책 **B1**(과장·감탄 없음, 「최고의」·「완벽한」 금지)을 **축자로** 덮는 유일한 후보다.

> 148행: "과장 형용사: … 완벽한/최고의 → 거의 항상 과장이니 삭제."

정책이 못박은 두 낱말을 그대로 지목한다. 덤으로 `다양한 · 효율적인 · 놀라운 · 강력한` 까지 잡아 B1 의
그물을 넓힌다. B2 와도 방향이 같다 — 91행 "근거 없는 수치·사례를 만들지 않는다(날조 금지는 생성에도 적용)".

정책과 **모순이 없다.** 0단계가 원문 레지스터를 보존하도록 만들어져 있어(102행 "레지스터가 바뀌었다
(존댓말→반말, 격식→구어 등) → 원래 레지스터로 되돌린다") 고객 문구의 존댓말을 깨지 않는다.
한국어 전용이라 우리 정책의 언어와 맞고, 본문이 자족적이라 런타임에 무엇을 받아오지 않는다
(반례: `kskill-korean-humanizer` 는 `npx …@0` 페치라 기각했다).

## 봉인해 둔 자리 (잠재 모순 하나)
43행이 매체별 표에서 마케팅 카피·SNS 행에 "짧은 훅, 청유·감탄" 을 남길 것으로 적었다. 고객 통지 자리에서
그 감탄은 **B7(느낌표 미사용)에 걸린다.** 원문을 고치지 않고 규칙으로 봉인했다:
**`brand` 가 우선한다.** 근거는 `skills/brand/PROVENANCE.md` 「함께 채택한 스킬」과
`docs/research/brand/coverage.md` 「모순」 절. 실측으로도 두 스킬이 함께 로드된 네 번 모두
결과 문구에 느낌표·이모지가 없었다(`docs/research/brand/trigger-tests.md` S3 · P4 · SS2 · SS3).

## 트리거
원문의 `description` 을 그대로 쓴다(고치지 않았다). 3/3 로드 — `docs/research/brand/trigger-tests.md`
P4 · SS2 · SS3(집합 시험 S3 을 더하면 4/4). 우리 자리와 겹치는 문구("문구 다듬어줘", "AI 티 난다",
"새로 써 줘")에서 물리고, spec 작성 자리(T6b)에서는 물리지 않는다 — 그 자리는 `brand` 의 것이다.

## 갱신
상류가 바뀌면 이 파일의 sha 와 사본을 함께 갱신한다. **정책이 바뀔 때 이 파일을 고치는 것이 아니다** —
정책은 `policies/brand.md` 가 정본이고 그것을 옮긴 것은 `skills/brand/` 뿐이다. 이 스킬은 남의 글이다.
