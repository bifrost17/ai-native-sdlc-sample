# 독립 리뷰 처리

검토 입력 `1500b16`, 수정 판 `2d3f2dc`. 최종 **설계 문서 정합성 PASS**. 제품 수락·설치·실행 PASS와 구별한다.

| 검토 | 최초 판단 | 처리와 재검토 |
|---|---|---|
| [Astra/ultra r1](reviews/astra-r1.md) | W01 공개 전 전체 AC가 공개 후 cleanup AC8까지 요구하는 순환 1건으로 CHANGES REQUIRED | 공개 전 AC1–7/cleanup AC8을 분리. [r2](reviews/astra-r2.md)에서 수정 범위 PASS |
| [실제 Claude Code Opus/high r1](reviews/opus-r1.md) | PASS + 비차단 6건. 위 순환을 처음에는 놓침 | 순환 근거와 수정본을 다시 읽게 함. [r2](reviews/opus-r2.md)에서 필요한 수정임을 인정하고 결합 PASS |

첫 Opus PASS로 다른 발견을 기각하지 않았다. 공개 전 요구와 공개 후 조건을 직접 대조해 R1을 채택했다.
수정 재검토는 기존 리뷰의 후속이며 새로운 독립 전체 리뷰 두 건을 추가한 것으로 세지 않는다.

## 구체 처리

- **W01 공개 범위:** AC7은 같은 완성 판의 격리 사본 리허설로 공개 전에 검증, AC8은 공개 후 cleanup 판에서 검증.
  plan의 Current change도 해당 구분을 연결한다. 새 AC·gate·검사기를 추가하지 않았다.
- **W01 명료화:** AC3 나열을 실제 인증→OFF→쿼리 우선순위와 맞췄다. Q4에서 절차 문서와 실행 기록의 역할을 구분했다.
- **F03 정본:** spec의 PR1/PR2 대응 문장을 plan 링크로 바꾸고 cleanup의 PR 번호를 전체 기능 통합으로 표현했다.
  R/AC와 상태·공개 의미는 그대로다.
- **설치 안내:** 기존 안내를 설치 절차의 정본으로 유지하며 TDD 추가 및 기존 정책 설명을 갱신한다는 의미를 명확히 했다.

비차단 제안 중 M01 AC8 확장, 역할 중복 표시, 모든 Current change에 결정 기록 포인터 추가는 확대하지 않았다.
시작 검증·담당·작성 허가는 이미 연결된 설계/입력과 전달안에서 찾을 수 있다. 같은 의미의 표와 의례를 더 만들 이유는 없다.
Opus r2의 plan 공개 문구 AC 번호 재기입과 F03 내부 상태명 복제도 추가하지 않았다. 현재 문맥과 정본 참조로 범위가
닫히며 두 문서에 같은 번호/상태를 다시 적는 비용이 더 크다. 실제 인계에서 중요한 모호함이 관측되면 해당 부분을 다시 검토한다.

## 검토 방식과 보존

- 최초 [공통 요청](reviews/prompt.md)은 전체 후보와 다섯 예시, 북극성·보존 정책을 읽게 했다. 다른 리뷰 결과는 주지 않았다.
- Astra는 난도·영향이 큰 구조/계약 판단이라 gpt-6-astra/ultra. M01 보완도 같은 수준으로 독립 분담했다.
- Claude Code는 사용자 지시대로 Opus, effort high. 실제 응답 모델은 메타데이터의 `claude-opus-5`다.
  보조 Haiku 호출이 보고된 경우 그대로 남겼다. [최초 호출](reviews/opus-r1-invocation.md), [후속 요청](reviews/opus-r2-prompt.md),
  [r1 메타데이터](reviews/opus-r1-metadata.json), [r2 메타데이터](reviews/opus-r2-metadata.json)에 원 응답과 조건을 연결했다.
- 도식 검증은 Sol/high, 새 세션 인계는 실제 Claude Code Sonnet/medium으로 분담했다. 리뷰와 인계 조건을 같은 모델 실험으로 합치지 않는다.
- Claude는 Read만 허용한 safe-mode/dontAsk로 호출했다. 공개 Read 경로/결과 상태만 보존하고 비공개 추론·서명·원문 반복 복사는 제외했다.

Git 객체·상대 링크·원문 보존은 [정적 검증](validation/README.md)에서 별도로 확인했다. Opus는 Read 전용이라 SHA 실재나
이전 판 diff를 직접 검증하지 못했다는 한계를 원문에 남겼다. 실제 제품 TDD·공개/복구는 어느 리뷰도 수행하지 않았다.
