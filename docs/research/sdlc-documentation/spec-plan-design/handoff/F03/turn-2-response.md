## PR1 순서 재검토

첫 답변의 "판정 함수 → OFF 미등록 확인(RED) → 최소 구현"은 plan 본문과 어긋납니다. plan.md의 PR1 문단을 다시 보면 순서는 다음과 같습니다.

1. 기준 P0(기존 3개 회귀) 통과 확인
2. **ON 환경에서** AC1 시험(`list --owner hana`가 R-101/R-103을 원순서·rc0로 출력)을 먼저 작성·실행 — 현재 코드는 `--owner` 자체를 모르므로 rc2가 예상 RED
3. 최소 목록/제어 연결(판정 함수 + argparse 등록 + 필터)로 GREEN
4. 그 다음에 OFF 거부·설정값별 케이스(P2)를 확인

즉 RED는 **OFF 거부가 아니라 ON에서의 목록 필터 부재**에서 나와야 합니다. plan은 이유를 명시합니다: "OFF는 기존 코드에서도 실패할 수 있으므로 그 자체를 새 기능 RED로 주장하지 않는다." 기존 baseline도 애초에 `--owner`를 모르므로 OFF 거부 시험은 구현 전이든 후든 항상 통과합니다 — 즉 이 실패는 **미구현 기능과 이미 존재하던 기존 제약을 구분해 주지 않습니다.**

TDD 스킬의 기준과 정확히 맞물립니다: "missing behavior... can be expected RED... confirm the behavior assertion discriminates the missing behavior." RED로 인정되려면 그 실패가 "아직 없는 이 기능" 때문이라는 것을 판별할 수 있어야 하는데, OFF 거부는 구현 여부와 무관하게 항상 참이므로 판별력이 없습니다. 판정 함수(게이팅 로직)는 RED 이전 단계가 아니라 GREEN 단계에서 필터 로직과 함께 최소로 구현하는 대상이고, OFF/설정값 검증(P2)은 GREEN 이후 "제어가 실제로 작동하는지"를 보여주는 별도 확인 단계입니다.

## 지금 일반 ON 전환 가능한가

**아니오.** 근거는 세 가지입니다.

- spec Design "공개 단위": 공개 단위는 목록+집계 전체이며, root는 "목록과 집계가 둘 다 완성·검증되기 전에는 일반 기본을 전환하지 않는다"고 명시. PR1만 통합된 지금은 summary가 아예 코드에 없는 상태입니다.
- spec Flagged concerns: "부분 TEST 성공을 전체 공개 승인으로 바꾸지 않는다." 목록 ON 시험 전부 통과는 PR1 범위의 부분 증거일 뿐, 공개 승인 근거가 아닙니다.
- intent 제약: "일반 사용자는 미완성 기능을 보지 않는다." 지금 ON으로 돌리면 summary 없는 반쪽 기능이 일반 사용자에게 노출되어 이 제약을 직접 위반합니다.

따라서 PR1 통합 + 목록 ON 시험 전부 통과는 "제어가 의도대로 작동한다"는 근거이지 "공개해도 된다"는 근거가 아닙니다.

## cleanup 요청 전 남은 조건과 확인 역할

spec Design "정리"와 plan 5단계에 따르면 cleanup 착수 전 아래가 모두 충족·기록돼야 합니다.

1. PR2 통합 및 최신 main에서 목록+집계+기존 list/show/complete 전체 검증 완료
2. root가 실제로 일반 실행 환경에서 ON→OFF(또는 그 반대)를 적용해보고 그 공개/중단 관측을 기록
3. 이 플래그를 읽는 구버전 프로세스나 롤백 대상이 없다는 root의 명시적 선언
4. root의 명시적 정리 요청

역할 분담: 환경 변수 조작·시험 실행·관측 기록은 개발 실행자가 수행하지만, "조건이 충족됐다"는 판단과 정리 착수 승인은 root(공개 담당) 고유의 결정입니다. 개발자가 스스로 조건 충족을 선언하고 cleanup을 시작할 수 없습니다.

## cleanup의 시험 변경은 테스트 약화와 같은가 다른가

**절차적으로는 다르지만, 통제 수준은 같아야 합니다.**

같은 점(왜 위험한지): 둘 다 "기존에 존재하던 assertion을 삭제"하는 행위입니다. TDD 스킬은 "Do not skip/delete/relax assertions merely to get GREEN"이라고 못 박고, 삭제 자체에는 항상 남용 위험이 따릅니다.

다른 점(왜 정당한지): TDD 스킬은 예외를 명시합니다 — "a changed requirement, a demonstrated test defect, or **a retired release-control phase** can justify a test change." cleanup에서 지우는 것은 정확히 이 세 번째 경우, 즉 R6에 의해 플래그 자체가 사라져 "OFF에서는 명령이 존재하지 않는다"는 전제 자체가 무의미해진 것입니다. GREEN을 얻기 위해 편의상 지우는 게 아니라, spec이 먼저 R6로 계약을 갱신하고 나서 그 갱신을 반영해 지우는 것이므로 인과관계가 반대입니다.

또한 plan/스킬 모두 정당화 조건을 요구합니다: exact-match·all/open/done 형식·read-only 등 여전히 유효한 회귀 시험은 그대로 남기고, 제거 이유를 spec/plan/PR에 명시하며, "Review a consequential test change independently"에 따라 이 삭제를 독립적으로 검토받아야 합니다. 이 절차(선행 계약 갱신 + 근거 문서화 + 독립 리뷰 + 나머지 회귀 보존)를 지키지 않고 지운다면 정당한 cleanup이 아니라 일반적인 테스트 약화와 동일하게 취급해야 합니다.
