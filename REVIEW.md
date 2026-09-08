# REVIEW.md — 리뷰 규약

레슨 10(`ai-in-the-pr-review-loop`)의 구조를 이 레포 어휘로 옮긴 것. `.github/PULL_REQUEST_TEMPLATE.md`
의 사슬 4문과 짝을 이룬다 — 템플릿이 사슬 정합을 묻고, 이 문서가 코드·문서 리뷰의 기준을 정한다.

## 패스 3

리뷰는 아래 세 패스를 순서대로 돈다. 패스 하나가 findings 0 이어도 다음 패스로 넘어간다(하나가
비었다고 리뷰가 끝난 게 아니다).

1. **bugs** — 코드가 주장한 동작과 다르게 동작하는가. AC(수용 기준)와 실제 구현 사이의 불일치.
2. **security** — 자격증명·PII 노출, 입력 검증 누락, 승인 없는 권한 상승 경로.
3. **compliance** — 이 PR 의 diff 가 `spec.md`·`plan.md` 와 **일치하는가**. `plan.md` 의
   `Files that change` 밖 파일이 바뀌었는가, `spec.md` 의 요구(R#)와 무관한 코드가 섞였는가.
   compliance 는 「좋은 코드인가」가 아니라 「말한 대로 했는가」만 묻는다.

## Important 의 정의

**Important** 로 표시할 수 있는 것은 다음 중 하나에 해당할 때뿐이다:
- 동작을 **깨뜨린다**(AC 미충족·회귀·예외).
- 데이터를 **새게 한다**(PII·자격증명·권한 밖 레코드 노출).
- 정책을 **위반한다**(이 문서·`CLAUDE.md`·`spec.md`의 제약을 어김).

위 셋에 안 걸리면 Important 가 아니라 Nit 이거나, 아예 findings 가 아니다("취향" · "나라면 이렇게" 는
findings 가 아니다).

## Nit 상한

리뷰 1회당 Nit 은 **최대 5개**까지만 개별 서술한다. 그 이상은 개수만 적는다
(예: "그 외 Nit 7건 — 개별 서술 생략"). Nit 이 쌓여 리뷰 자체를 지연시키지 않는다.

## 보고하지 않을 것

- **생성 파일**(빌드 산출물·락 파일 등) — 사람이 손으로 안 고치는 파일의 스타일은 findings 가 아니다.
- **CI 가 이미 강제하는 것** — `make check` 가 이미 red 로 잡는 항목(셸 구문·frontmatter 키 누락 등)을
  리뷰가 중복 지적하지 않는다. CI 가 놓친 것만 findings 로 올린다.

## findings 의 효력

findings 는 **승인도 차단도 하지 않는다**. 승인/차단은 CODEOWNER(`.github/CODEOWNERS`)의 몫이다.
리뷰는 판단 재료를 제공할 뿐 — Important findings 가 있어도 머지 여부의 최종 결정은 CODEOWNER 가
PR 위에서 명시적으로 내린다.
