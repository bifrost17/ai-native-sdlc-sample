# Plan: 가격 할인 계산 추가
Upstream: `SPEC.md` user-supplied working-tree revision. Status: draft.
사용자가 이 범위의 계획·구현·로컬 검증과 **작은 동작 구현 후 테스트** 순서를 허가했다. `SPEC.md`의 계산 계약을 기존 `pricing.py`에 추가하고, 기존 `subtotal` 회귀와 새 경계 동작을 한 로컬 변경 묶음으로 검증한다. 저장소에는 아직 커밋이 없어 SHA 기반 upstream 또는 main diff를 만들 수 없다.

## Files that change
| 경로 | 변경 역할 | spec/AC 참조 |
|---|---|---|
| `pricing.py` | `payable` 범위 검사와 할인 계산 | AC1–AC4 |
| `tests/test_pricing.py` | 예시·경계·오류·불변성과 기존 소계 회귀 자동 검증 | AC0–AC4 |
| `PLAN.md` (new) | 구현 순서와 예정 증명 | 전체 |
| `evidence.md` (new) | 실제 명령·출력·편집 순서와 검토 근거 | 전체 |

## Order of work
검증 방식은 **작은 동작 구현 후 테스트**다. 새 함수가 하나이고 계산식과 경계 기대가 spec의 독립된 예시로 고정되어 있어, 먼저 최소 동작을 구현한 뒤 곧바로 자동 시험을 추가하는 순서가 적합하다. 사후 시험을 TDD 이력으로 주장하지 않는다.

1. 기준판에서 `python3 -m unittest discover -s tests`로 기존 `subtotal` 3개 시험 통과를 확인한다.
2. `pricing.py`에 `payable`을 추가한다. `subtotal`을 재사용하고 정수 바닥 나눗셈으로 할인액을 계산하며, 백분율이 0–100 밖이면 `ValueError`를 낸다. 입력 목록은 읽기만 한다.
3. `tests/test_pricing.py`에 `[1001], 10 → 901`, 0%, 100%, 빈 목록, 양쪽 범위 오류, 입력 불변 시험을 추가한다. 그 뒤 명시된 전체 명령을 실행한다.
4. `SPEC.md`, 이 plan, 실제 diff와 `evidence.md`를 `REVIEW.md` 및 `selected-skills/agents/sdlc-verifier.md` 기준으로 자체 대조하고 전체 회귀를 재실행한다. 이 제한 연습에서는 외부 verifier/PR/배포를 수행하지 않으며, 자체 검토가 독립 검토는 아니라는 한계를 기록한다.

## Risks
| 깨질 동작·위험 | 어떻게 발견하는가 | 대응/중지 조건 |
|---|---|---|
| 할인 계산에서 반올림 또는 연산 순서가 달라짐 | 1001의 10% 기대값 901과 경계 시험 | `total * percent // 100` 할인액을 명시적으로 계산 |
| 범위 경계가 0 또는 100을 거부함 | 0%, 100%, -1%, 101% 시험 | 포함 경계를 유지하고 바깥만 거부 |
| 새 계산이 기존 소계나 입력 목록을 바꿈 | 기존 3개 시험과 새 입력 불변 시험 | `subtotal`을 변경하지 않고 목록에 쓰지 않음 |

## Proof
| ID·AC | 시험/작업의 정본 | 기대/한계 |
|---|---|---|
| P1 AC0 | 기존 `SubtotalTests`; `python3 -m unittest discover -s tests` | 빈 목록·다중 합계·불변성 유지 |
| P2 AC1–AC4 | 새 `PayableTests`; 같은 전체 명령 | 예시, 두 유효 경계, 빈 목록, 두 오류 경계, 입력 불변 확인. 범위 밖 입력 타입은 spec 밖 |
| P3 전체 | `git diff --no-index` 기반 초기/현재 제품 파일 대조와 현재 파일 자체 검토, 결과는 `evidence.md` | 커밋/PR/main 통합 및 독립 verifier는 제한 범위 밖 |
