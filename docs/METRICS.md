# METRICS.md — 플레이북 지표

설계안(`docs/DESIGN.md`) §7 을 확장한 정본. 플레이북 14 플레이의 leading/lagging 을 전부 적고,
이 샘플에서 실제로 계산 가능한지를 「계산 / 부분 / 불가」로 가른다. 「불가」는 빈칸으로 두지
않는다 — 이 레포가 계기보다 강하게 말하지 않기 위해 이유를 함께 적는다.

레슨 1(introduction)·14(closing-thoughts-and-resources)는 서술형이라 플레이북 자체가
leading/lagging 지표 쌍을 정의하지 않는다 — 아래 표는 지표 쌍이 정의된 2~13 을 다룬다.

| # | 레슨(slug) | leading | lagging | 이 샘플에서 | 이유(불가/부분일 때) |
|---|---|---|---|---|---|
| 2 | capture-intent | 첫 대화 → 커밋 시간 | survival rate · 첫 spec 이후 intent 변경 수 | **계산** | `created:` 필드 + git + PR 상태로 계산 가능(아래 계산식) |
| 3 | requirements-and-design | intent→spec 커밋 간격 | 첫 plan 이후 spec 커밋 수 | **계산** | git log 간격으로 계산 가능 |
| 4 | plan-mode | 1차 통과 머지 비율 · plan 승인→머지 시간 | 재작업 회차 · diff↔plan 일치 | **부분** | git·PR 이력으로 계산은 되지만 표본이 사슬 3본뿐이라 통계로서 의미가 약함 |
| 5 | claude-md | 같은 실수 반복 횟수 | 신규 참여자 첫 머지까지 시간 | **불가** | 참여자가 PO 1인이라 "신규 참여자"가 존재하지 않음 — 지면(`CLAUDE.md` 「같은 실수를 두 번 하면 등재」)으로만 대체 |
| 6 | skills-as-institutional-knowledge | 정책 승인→스킬 머지 시간 | 정책 인용 리뷰 지적 수 | **불가** | 정책을 별도로 소유·승인하는 조직 단위가 없음(PO = 정책 작성자 = 승인자) |
| 7 | parallel-sessions-and-subagents | 동시 세션 수(OTel) | 주당 머지 수 | **불가** | OpenTelemetry 수집기가 없고, 1인 레포라 "동시 세션"이 관측 대상으로 성립하지 않음 |
| 8 | give-claude-a-feedback-loop | 1차 CI 성공률 | PR 리뷰 시간 · 변경 실패율 | **부분** | CI 성공률은 GitHub Actions 이력으로 계산 가능, 리뷰 시간·변경 실패율은 리뷰어 다양성이 없어 의미가 약함 |
| 9 | continuous-evals-in-ci | 통과율 추이 | CI 포착 vs 프로덕션 유출 | **불가** | API 키 예산이 없어 evals 가 상시 실행되지 않고, 프로덕션 배포 대상이 없어 "유출"을 관측할 곳이 없음 |
| 10 | ai-in-the-pr-review-loop | 첫 리뷰까지 시간 | 머지 전 결함 vs 유출 결함 | **불가** | 인시던트 트래커가 없어 "유출 결함"을 별도로 셀 방법이 없음 |
| 11 | hooks-as-approval-gates | 게이트 대기 시간(OTel) | 게이트 위반 도달 시도 수 | **불가** | OpenTelemetry 가 없어 대기 시간을 못 재고, 위반 시도는 훅이 즉시 차단해 도달 자체가 로그에 안 남음(`tests/test_hooks.sh` 의 시험 결과로만 간접 확인) |
| 12 | ci-cd-integration-and-deployment | 사람 없이 트리아지된 실패 비율 | DORA 4종 | **불가** | 인시던트 트래커·프로덕션 배포 대상이 없어 DORA 지표(배포 빈도·리드타임·MTTR·변경 실패율)를 정의할 모집단이 없음 |
| 13 | closing-the-loop-on-metrics | 밴드 위반 → intent 큐 시간 | 발견→머지 비율 · 반복 사고 수 | **부분** | `ops/bands.yaml`·`detect_bands.py`(W3)가 합성 입력으로 위반→intent 생성까지는 시연하지만, 라이브 30일 기준선이 없어 반복 사고 재발률은 못 잰다 |

## 계산 가능한 3종 — 계산식 (실값은 W3 `scripts/metrics.py` 가 채운다)

아래 세 지표는 git 명령만으로 계산 가능하다는 뜻이지, 지금 이 문서에 실값이 있다는 뜻이
아니다. **실값은 비워 둔다** — `scripts/metrics.py`(W3, `scripts/gates/10-docs.sh` 밖 소유)가
`make metrics` 실행 시 아래 식을 실제로 돌려 채운다.

### intent leading — 첫 대화 → 첫 커밋 시간
```
# intent.md 의 created: 필드(자기 신고 시각)와, 그 파일의 첫 git 커밋 시각의 차.
CREATED=$(grep '^created:' intent/<id>/intent.md | cut -d' ' -f2)
FIRST_COMMIT=$(git log --follow --format='%aI' --reverse -- intent/<id>/intent.md | head -1)
# 값 = FIRST_COMMIT - CREATED (초 단위 차)
```

### survival rate — accepted 도달 비율
```
TOTAL=$(ls -d intent/*/intent.md 2>/dev/null | wc -l | tr -d ' ')
ACCEPTED=$(grep -l '^status: accepted' intent/*/intent.md 2>/dev/null | wc -l | tr -d ' ')
# 값 = ACCEPTED / TOTAL
```

### 첫 spec 이후 intent 변경 수
```
# 같은 id 의 spec.md 첫 커밋 시각 이후, intent.md 에 가해진 커밋 수(재오픈·정정).
SPEC_FIRST=$(git log --follow --format='%aI' --reverse -- intent/<id>/spec.md | head -1)
git log --since="$SPEC_FIRST" --oneline -- intent/<id>/intent.md | wc -l | tr -d ' '
```
