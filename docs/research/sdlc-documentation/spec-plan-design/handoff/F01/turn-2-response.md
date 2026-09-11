## 1. "최신 main과 합친 판에서 PASS = 통합 검증 끝"인가?

아닙니다. plan.md 4번 항목을 다시 보면:

> "최신 main과 합친 판에서 Proof 전체를 실행하고 명령/판/출력·미확인 범위를 PR에 남긴다. **검토 후 통합된 main에서도 같은 검증을 확인한다.**"

즉 두 단계입니다:
1. PR 브랜치에서 main과 합친 상태로 로컬/CI 검증 (PASS → PR에 근거 기록)
2. **리뷰 승인 후 실제로 main에 머지된 뒤**, 그 통합된 main에서 같은 검증을 다시 확인

1번 PASS는 "PR을 낼 준비가 됐다"는 뜻이지 "통합 검증 완료"가 아닙니다. 통합 검증은 머지 후 재확인까지 포함해야 끝납니다. execution-blocks.md도 "개별 테스트 GREEN 이후 최신 main과 합친 전체 계약·데이터·사용 흐름을 검증한다"고 별도로 강조하고 있어 동일한 2단계 구조를 뒷받침합니다.

## 2. 기존 CLI 시험 배치가 tests/cli/test_owner.py라면

plan.md는 파일 경로를 `tests/test_owner.py`로 명시했는데, 저장소 실제 관례가 `tests/cli/`라면 이는 **plan의 "경로" 자체가 발견 시점에 달라진 경우**입니다. execution-blocks.md 표에 따르면:

> "테스트/모듈 경로·작업 순서·PR 범위·증명 방법 변화 → **변경할 정본: plan과 이유** / 유지할 것: 의미가 같은 spec"

**바꿀 문서: plan.md만.**
- Files that change 표의 경로를 `tests/test_owner.py` → `tests/cli/test_owner.py`로 수정
- Proof 표의 명령도 함께 갱신: `python3 -m unittest discover -s tests -p test_owner.py -v` → `-s tests/cli` 등 실제 배치에 맞게
- spec.md는 건드리지 않습니다. spec은 계약(R1–R3, AC1–4)만 정의하며 파일 경로를 규정하지 않으므로 "의미가 같은 spec"에 해당합니다.

**언제 바꾸는지**: execution-blocks.md 안내대로 "관련 구현 커밋에서" — 즉 이 발견을 반영하는 실제 구현/시험 작성 커밋과 같은 커밋에서 plan을 갱신합니다. 별도 문서 전용 PR을 요구하지 않습니다. plan.md 자체에도 "경로·순서·검증 변경은 관련 구현 커밋에서 plan을 갱신한다"는 문장이 이미 있어 이 케이스를 예정해 두었습니다.

## 3. 빈 owner/인자 누락 — 새 사람 결정이 필요한가?

**아니요, 새 사람 결정 불필요.** 계약과 argparse 경계를 구분하면:

- **"인자 누락"** (`--owner` 뒤에 값이 없는 경우, 예: `list --owner`): 이는 spec이 규정하는 애플리케이션 계약이 아니라 **argparse 자체의 파싱 문법 오류**입니다. argparse가 자동으로 `error: argument --owner: expected one argument`를 stderr에 출력하고 rc2로 종료하는 기존 표준 동작이며, 이는 R1/R3가 다루는 "owner 값 비교 로직"의 영역 밖입니다. 다른 옵션(`show`의 `id` 인자 등)도 이미 이 방식에 의존하고 있어 새로운 정책이 아니라 기존 CLI 프레임워크 관례를 그대로 따르는 것입니다.

- **"빈 문자열 owner"** (`--owner ""`): 이것은 반대로 **애플리케이션 계약 안**의 값입니다. spec.md R1은 "정확 일치, null은 어느 문자열과도 일치하지 않음"이라고만 하고, 빈 문자열 자체를 별도로 언급하지 않습니다. 하지만 이는 실은 이미 답이 나와 있는 경우입니다: 빈 문자열은 그냥 "문자열"이므로 R1의 일반 규칙(정확 일치)에 그대로 포함됩니다 — f01-requests.json에 owner가 `""`인 행이 없으므로 AC2(nobody/HANA/- 무매치)와 동일하게 빈 stdout·rc0가 나오면 됩니다. 이는 규칙의 **적용**이지 **새 규칙**이 아니므로, execution-blocks.md 표의 "기존 계약을 그대로 확인하는 사례 추가"에 해당 — **시험에 회귀 케이스로 추가하면 되고 spec을 고칠 필요 없음.**

따라서 둘 다 기존 정본(spec R1 + argparse 표준 동작)으로 결정 가능하며, 별도 사람 승인이나 intent/spec 변경 없이 구현·시험 단계에서 처리할 수 있는 경계입니다.
